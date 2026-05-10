---
kind: interface-contract
content_axis: normative-cli-autofix-protocol
axis_rationale: "riseup-git-logs server→CLI auto-fix protocol; tier-1 hybrid 4-state propose-diff-confirm contract"
---

# `riseup-git-logs` CLI — Auto-Fix Protocol

**Version:** 1.1.0
**Updated:** 2026-05-08 (Phase L2 — §11 Worked Example added; transcript per Lesson #29 `kind: example`; normative contract unchanged)
<!-- verified-phase: 158 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-86). Fifth of the J-series CLI subsystem (§40–§45).
> Per **Lesson #36** (link-don't-restate): the REST endpoint surface is owned by **spec/22 §04**; the upload-side wire envelope and `Idempotency-Key` semantics are owned by **§43**; the classifier outcome set (`NORMAL`/`WARN`/`ERROR`/`INTERNAL`) is owned by **§42 / AC-84**; the pointer-file `autofixDownloadUrl` field is owned by **§41 / AC-83**; SSH-key Lane B auth is owned by **§31**; the `ExitCode` enum is owned by **spec/13 AC-21**; atomic temp-then-rename file writes are owned by **spec/13 AC-22**. This file binds the auto-fix download + apply contract that consumes those surfaces and **does not restate any of their bodies**.
> Per **Lesson #21** (intra-module sibling-file delegation): bound from §97 AC-86 by name; row 38 of AC-80 Sibling File Delegation Map.
> Per **Lesson #19** (audit-boundary pin): the 7-section auto-fix contract is enumerated as a normative tier-1 surface here; restating any of it in §40, §41, §42, §43, or §45 is FORBIDDEN.

---

## 1. Purpose & Scope

After a successful upload (per §43 §6), the server response carries `autofixDownloadUrl` (https or null). When non-null, that URL points to a server-prepared **fix bundle** — a deterministic patch the CLI MAY apply locally to bring the working tree into a state the server classifies as conflict-free. The protocol is a **hybrid 4-state propose → diff → confirm → apply** flow: the user remains in the loop on the **confirm** step by default; `--auto-confirm` is opt-in and disallowed for `MAJOR` schema bumps.

**In scope:** download request shape, fix-bundle envelope, 4-state outcome enumeration (`APPLIED`, `REJECTED_USER`, `REJECTED_PRECONDITION`, `DEFERRED_NETWORK`), preflight preconditions, atomic apply discipline, post-apply pointer-file refresh.

**Out of scope:** REST endpoint catalog (§04); upload wire envelope (§43); classifier outcomes (§42); pointer-file shape (§41); auth lane (§31); rate-limit values (§05); test plan (§45).

## 2. Download Request (Normative)

| Concern | Value |
|---|---|
| Method | `GET` |
| URL | exact string returned in `autofixDownloadUrl` (no rewriting, no query-param mutation) |
| Scheme | `https` ONLY — `http` redirects MUST be rejected with `INTERNAL` |
| Auth header | SSH-key Lane B per spec/22 §31 (link-don't-restate) |
| Accept | `application/vnd.riseup.git-logs.fix+json; v=1` |
| Accept-Encoding | `gzip` |
| If-None-Match | `<etag>` from prior fetch when caching same `batchId` (server MAY 304) |
| Max body size | 4 MiB compressed / 16 MiB decompressed; over-cap → `REJECTED_PRECONDITION` + `GL-FIX-PAYLOAD-TOO-LARGE` |
| Timeout | 30s connect + 60s body; exceed → `DEFERRED_NETWORK` |

**FORBIDDEN:** following cross-origin redirects; re-using a `Idempotency-Key` from §43; sending CLI-derived headers other than the canonical set above; persisting the response body to disk before validation passes (§3 + §4).

## 3. Fix-Bundle Envelope (Normative — closed 7-field set)

The response body is a single JSON object with `additionalProperties: false`:

| Field | Type | Required | Notes |
|---|---|---|---|
| `bundleId` | string (UUIDv4) | yes | server-authoritative bundle identity |
| `batchId` | string (UUIDv4) | yes | MUST equal the `batchId` from §43 §6 that triggered this fix |
| `repoIdentityHash` | string (64-hex sha256, lowercase) | yes | MUST equal the pointer-file value (§41 §2); mismatch → `REJECTED_PRECONDITION` |
| `targetHead` | string (40-hex git SHA) | yes | head the bundle was computed against; mismatch with current `HEAD` → `REJECTED_PRECONDITION` |
| `schemaBump` | enum {`patch`, `minor`, `major`} | yes | drives `--auto-confirm` gating per §5 |
| `patches` | array of patch objects | yes | each: `{ path, mode, beforeSha256, afterSha256, unifiedDiff }`; ≥1 entry; `additionalProperties: false` per element |
| `expiresAt` | string (RFC 3339 UTC) | yes | MUST be in the future at fetch time; expired → `REJECTED_PRECONDITION` |

**FORBIDDEN fields** (server MUST omit; CLI MUST reject if present): `token`, `apiKey`, `secret`, `password`, `sshKey`, `privateKey`, `userId`, `userEmail`, `ownerEmail`, `env`, `platform`, `clientIp`, `hostname`, `cwd`, `username`, `homeDir`, `executablePath`. (16-entry list mirrors §43 §3.)

## 4. 4-State Outcome (Normative — closed set)

| State | When emitted | Exit code (per spec/13 AC-21) | Pointer-file mutation? |
|---|---|---|---|
| `APPLIED` | every patch passed §6 atomic-apply | `OK` | yes — refresh `currentHead` per §7 |
| `REJECTED_USER` | confirm prompt declined OR `--auto-confirm` declined a `MAJOR` bump | `OK` | no |
| `REJECTED_PRECONDITION` | any §3 / §5 / §6 precondition fails (hash mismatch, expired, before-sha mismatch, dirty tree) | `UserError` | no |
| `DEFERRED_NETWORK` | timeout, 5xx, DNS failure, TLS handshake failure | `Internal` | no |

Adding a fifth state name = SPEC VIOLATION. Every emitted state MUST be uploaded as a frame per §43 with `subcommand: "fix"` (server-side reserved) and `outcome` mapped to `NORMAL` (APPLIED), `WARN` (REJECTED_USER), `ERROR` (REJECTED_PRECONDITION), or `INTERNAL` (DEFERRED_NETWORK).

## 5. Preflight Preconditions (Normative — strict order)

Before any patch is applied, the CLI MUST verify in order — first failure short-circuits to `REJECTED_PRECONDITION` with the matching `GL-FIX-*` code:

1. **`autofixDownloadUrl` freshness** — pointer-file value matches the URL the CLI is fetching (no out-of-band substitution); else `GL-FIX-URL-STALE`.
2. **`repoIdentityHash` match** — bundle field equals pointer-file field; else `GL-FIX-IDENTITY-MISMATCH`.
3. **`targetHead` match** — bundle field equals current `HEAD` SHA via the same identity-discovery path as §40 step 4; else `GL-FIX-HEAD-DRIFT`.
4. **`expiresAt` future** — bundle field is strictly after current UTC; else `GL-FIX-EXPIRED`.
5. **Working tree clean** — `git status --porcelain=v2 -z` returns empty; else `GL-FIX-DIRTY-TREE`.
6. **Per-patch `beforeSha256` match** — for each patch, the file at `path` has sha256 equal to `beforeSha256` (or absent iff `beforeSha256 == "0".repeat(64)` for new-file patches); else `GL-FIX-BEFORE-MISMATCH`.
7. **Schema-bump confirm gating** — `schemaBump == "major"` requires interactive `y/N` confirm; `--auto-confirm` flag is IGNORED for `major` bumps (treat as decline → `REJECTED_USER`); for `minor`/`patch`, `--auto-confirm` skips the prompt.

**FORBIDDEN:** reordering these checks; skipping any check via flag; running `git stash` automatically (the user MUST resolve dirty trees themselves).

## 6. Atomic Apply Discipline (Normative)

Once §5 passes and the user confirms (or `--auto-confirm` applies):

1. Compute the full set of `(path, afterContent)` tuples by applying each `unifiedDiff` to its current file content **in memory** — no file mutated yet.
2. Verify each computed result has sha256 equal to its `afterSha256`; mismatch → `REJECTED_PRECONDITION` + `GL-FIX-AFTER-MISMATCH` (no files touched).
3. Write each result via the **temp-then-rename** discipline owned by spec/13 §97 AC-22 (link-don't-restate): `<path>.riseup-fix.<bundleId>.tmp` → `fsync` → `rename()`. Rename is per-file atomic; the bundle as a whole is **NOT** transactionally atomic across files (see Forbidden Patterns).
4. After all renames succeed, emit a single `APPLIED` frame per §43.
5. If any rename fails mid-bundle: **STOP**, do NOT roll back already-renamed files (the user can `git checkout -- <paths>`), emit one `DEFERRED_NETWORK` frame with `payload` listing the partially-applied paths (since this indicates filesystem-class failure, not network), and exit `Internal`.

**FORBIDDEN:** in-place writes; `git apply` invocation (the CLI MUST compute the after-state itself for verifiability); creating a parent directory that did not exist (server bundles MUST list directory-creation as separate `mode: "mkdir"` patches — out of scope for v1.0.0); chmod beyond preserving the existing mode.

## 7. Post-Apply Pointer-File Refresh (Normative)

On `APPLIED` only:

1. Re-derive `currentHead` via `git rev-parse HEAD` (the apply does NOT auto-commit; the head SHA is unchanged from preflight step 3 — this re-derivation is a belt-and-braces invariant check).
2. Update `.riseup-git-logs.json` per §41 §1 atomic write discipline (link-don't-restate spec/13 AC-22): set `uploadedAt`, `expiresAt`, and `autofixDownloadUrl` to `null` (the bundle has been consumed and the URL MUST NOT be reused). `currentHead` is updated only if a follow-up commit changes it (out of scope here — `riseup-git-logs commit` would handle that in a future J-series extension).
3. The user MUST manually `git add` + `git commit` the applied patches (the CLI does NOT auto-commit). This is an explicit user-in-the-loop invariant.

**FORBIDDEN:** auto-committing the applied patches; auto-pushing; mutating any pointer-file field other than the three listed in step 2; running any `git` write command (`commit`/`add`/`push`/`checkout`/`reset`) inside the auto-fix flow.

## 8. Forbidden Patterns Summary

- in-place writes (atomic rename per spec/13 AC-22 ONLY)
- shelling out to `git apply` (CLI computes after-state itself for verifiability)
- following cross-origin or HTTP→HTTP redirects
- auto-committing or auto-pushing applied patches
- treating `--auto-confirm` as bypassing `major` schema bumps
- reordering the §5 preflight check sequence
- restating spec/22 §04 / §05 / §15 / §31 / §41 / §42 / §43 / spec/13 §97 AC-21 / AC-22 inside §44

## 9. Error Envelope Mapping

`GL-FIX-*` error codes are owned by spec/22 §15 (link-don't-restate). The mapping below is a CLI-side reference:

| Condition | HTTP context | Code |
|---|---|---|
| Bundle URL scheme not https | local | `GL-FIX-URL-STALE` |
| `repoIdentityHash` mismatch | local | `GL-FIX-IDENTITY-MISMATCH` |
| `targetHead` ≠ current HEAD | local | `GL-FIX-HEAD-DRIFT` |
| `expiresAt` in past | local | `GL-FIX-EXPIRED` |
| Dirty working tree | local | `GL-FIX-DIRTY-TREE` |
| `beforeSha256` mismatch | local | `GL-FIX-BEFORE-MISMATCH` |
| Computed `afterSha256` mismatch | local | `GL-FIX-AFTER-MISMATCH` |
| Bundle body > size cap | server | `GL-FIX-PAYLOAD-TOO-LARGE` |
| Bundle expired by server | server | `GL-FIX-EXPIRED` |
| Auth failure | server | `GL-FIX-AUTH-INVALID` |
| Server 5xx | server | `GL-FIX-SERVER-ERROR` |

## 10. Out-of-Scope (Future J-series Extensions)

- multi-bundle queueing (server SHOULD emit at most one `autofixDownloadUrl` per upload);
- partial-bundle resumption across CLI invocations;
- patch types beyond unified-diff (binary, mode-only, mkdir) — listed in §3 placeholder for v1.x extension under follow-up §97 extension AC + slot `MINOR` bump;
- auto-commit / auto-push (explicitly FORBIDDEN above to preserve user-in-the-loop invariant).

---

## 11. Worked Example (Non-normative, `kind: example`)

> **Status:** Illustrative transcript per **Lesson #29** module-kind pin — examples are auditor-quoted evidence, NOT normative contract. The normative auto-fix flow lives in §2–§9 above and §97 AC-86; restating it here in transcript form is FORBIDDEN. Any drift between this transcript and §2–§9 is resolved IN FAVOUR OF §2–§9 + AC-86.

### 11.1 Setup (givens)

- CLI: `riseup-git-logs v0.4.2`, `~/.riseup-git-logs.json` pointer file present
- Repo: `/home/alice/widgets`, `currentHead = a1b2c3d4e5f60718293a4b5c6d7e8f9012345678` (clean working tree)
- `repoIdentityHash = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08`
- Pointer-file `autofixDownloadUrl` (set by prior §43 §6 response): `https://logs.acme.example/wp-json/git-logs/v3/autofix/9f86d.../01HZ8K9V3Q7M5N2P4R6T8X0Y1C`
- Bundle contains 1 patch: a `minor` schema bump renaming `widget.json` field `created_on` → `createdAt` (per spec/04 boolean/casing convention link-don't-restate)

### 11.2 Download request (success path)

```http
GET /wp-json/git-logs/v3/autofix/9f86d081.../01HZ8K9V3Q7M5N2P4R6T8X0Y1C HTTP/1.1
Host: logs.acme.example
Authorization: <Lane B per spec/22 §31 — link-don't-restate>
Accept: application/vnd.riseup.git-logs.fix+json; v=1
Accept-Encoding: gzip
```

Server replies (per §47 single-consumption discipline link-don't-restate):

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.riseup.git-logs.fix+json; v=1
ETag: "8a3f1c2d4e5b6a70"
Cache-Control: private, no-store

{"bundleId":"7c4e9d2a-1b3f-4d5e-9a8b-2c1d3e4f5a6b","batchId":"5e1f4a2b-7c8d-4a3b-9e1f-2c3d4a5b6c7d","repoIdentityHash":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","targetHead":"a1b2c3d4e5f60718293a4b5c6d7e8f9012345678","schemaBump":"minor","patches":[{"path":"widget.json","mode":"100644","beforeSha256":"4f8b6c1d2e3a5f70819203a4b5c6d7e8f90123456789abcdef0123456789abcd","afterSha256":"a1c2e3d4f50617283940516273849506172839405a6b7c8d9e0f102132435465","unifiedDiff":"--- a/widget.json\n+++ b/widget.json\n@@ -1,3 +1,3 @@\n {\n-  \"created_on\": \"2026-05-01T10:00:00Z\"\n+  \"createdAt\": \"2026-05-01T10:00:00Z\"\n }\n"}],"expiresAt":"2026-05-09T10:15:01.044Z"}
```

### 11.3 Preflight pass (§5 strict order)

CLI runs the 7-check sequence:

1. URL freshness ✓ (matches pointer-file)
2. `repoIdentityHash` match ✓
3. `targetHead == HEAD` ✓ (`a1b2c3d4...`)
4. `expiresAt` future ✓ (now = 2026-05-08T10:30:00Z)
5. `git status --porcelain=v2 -z` empty ✓
6. `sha256(widget.json) == beforeSha256` ✓
7. `schemaBump=minor` + `--auto-confirm` flag absent → interactive prompt:

```
fix bundle 7c4e9d2a-1b3f-4d5e-9a8b-2c1d3e4f5a6b (minor schema bump)
  M widget.json
Apply? [y/N] y
```

### 11.4 Atomic apply (§6)

CLI computes `widget.json` after-content in memory, verifies `sha256 == afterSha256` ✓, then:

```
write    → widget.json.riseup-fix.7c4e9d2a-1b3f-4d5e-9a8b-2c1d3e4f5a6b.tmp
fsync    → ok
rename() → widget.json (atomic per spec/13 AC-22)
```

CLI emits APPLIED frame via §43:

```json
{"frameId":"01HZ8M3X7P9R2S4T6V8W0Y1Z2A","repoIdentityHash":"9f86d081...","currentHead":"a1b2c3d4...","subcommand":"fix","outcome":"NORMAL","classifierVersion":"2.1.0","payload":"APPLIED bundleId=7c4e9d2a-1b3f-4d5e-9a8b-2c1d3e4f5a6b patches=1","emittedAt":"2026-05-08T10:30:02.118Z","redact":false}
```

### 11.5 Pointer-file refresh (§7)

`~/.riseup-git-logs.json` (atomic temp-then-rename):

```diff
   "currentHead": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
-  "autofixDownloadUrl": "https://logs.acme.example/wp-json/git-logs/v3/autofix/9f86d.../01HZ8K9V3Q7M5N2P4R6T8X0Y1C",
-  "uploadedAt": "2026-05-08T10:15:01.044Z",
-  "expiresAt": "2026-06-07T10:15:01.044Z"
+  "autofixDownloadUrl": null,
+  "uploadedAt": "2026-05-08T10:30:02.118Z",
+  "expiresAt": "2026-06-07T10:30:02.118Z"
```

CLI prints:

```
applied 1 patch. Run `git add widget.json && git commit -m "..."` to record.
```

User-in-loop invariant per §7: CLI does NOT auto-commit.

### 11.6 Negative path A — `MAJOR` bump with `--auto-confirm` (REJECTED_USER)

Same flow but bundle has `schemaBump: "major"` and user passed `--auto-confirm`. Per §5 step 7, `--auto-confirm` is IGNORED for `major` bumps and treated as decline:

```
fix bundle 9d3e1c8f-... (MAJOR schema bump — --auto-confirm ignored)
declined.
```

CLI emits REJECTED_USER frame (`outcome: "WARN"` per §4), exit `OK`, pointer file untouched.

### 11.7 Negative path B — dirty tree (REJECTED_PRECONDITION)

Same flow but `git status --porcelain=v2 -z` reports `scratch.txt` untracked. §5 step 5 fails:

```
ERROR GL-FIX-DIRTY-TREE: working tree has uncommitted changes; resolve and re-run.
```

CLI emits REJECTED_PRECONDITION frame (`outcome: "ERROR"` per §4), exit `UserError` (per spec/13 AC-21), pointer file untouched. CLI MUST NOT run `git stash` (FORBIDDEN per §5).

### 11.8 Negative path C — mid-bundle rename failure (DEFERRED_NETWORK)

Bundle has 3 patches; patch 1 + patch 2 rename successfully, patch 3's `rename()` returns `ENOSPC`. Per §6 step 5: STOP, NO rollback of patches 1+2 (user can `git checkout -- a.txt b.txt`), emit ONE DEFERRED_NETWORK frame with `payload="partially-applied: a.txt, b.txt; failed: c.txt (ENOSPC)"`, exit `Internal`.

### 11.9 What this transcript IS NOT

This §11 is illustrative evidence per `kind: example`. It does not extend, narrow, or supersede any rule in §2–§9. Future contract changes land in §2–§9 + §97 AC-86 first; §11 is then refreshed to mirror — never the inverse. Lesson #29 module-kind pin applies (front-matter `kind: interface-contract`; §11 sub-section is `kind: example` by Lesson #29's quoted-evidence rule).

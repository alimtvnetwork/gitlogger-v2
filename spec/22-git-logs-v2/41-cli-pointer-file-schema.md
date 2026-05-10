---
kind: interface-contract
content_axis: normative-cli-pointer-file-wire-format
axis_rationale: "JSON Schema (Draft-07) for `.riseup-git-logs.json` pointer file written at git root by `riseup-git-logs` CLI; tier-1 wire-format contract for J-series subsystem"
---

# `.riseup-git-logs.json` — Pointer File JSON Schema

**Version:** 1.1.0
**Updated:** 2026-05-10 (Phase L3 — non-normative §7 Worked Example Lifecycle added; pattern from L1/L2)
<!-- verified-phase: 154 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-83). Second of the J-series CLI subsystem (§40–§45).
> Per **Lesson #36** (link-don't-restate): atomic write discipline + `expiresAt` semantics + 5-step identity algorithm are owned by §40 §3–§4 and spec/13 §97 AC-22; this file owns ONLY the wire format. The pattern reference for the schema shape is **spec/14 AC-23** (update interface contract).
> Per **Lesson #21 / Lesson #39**: this slot is bound from §97 AC-83 by name and from AC-80 Sibling File Delegation Map row 35.

---

## 1. File Location & Lifecycle (Normative)

| Aspect | Value |
|---|---|
| Path | `<git-root>/.riseup-git-logs.json` (single file at the toplevel — never nested) |
| Encoding | UTF-8, no BOM, LF line endings |
| Mode | `0644` (world-readable; never `0600` — the file carries no secrets) |
| Write discipline | Atomic temp-then-rename per spec/13 §97 AC-22 (write to `.riseup-git-logs.json.tmp.<pid>` then `rename(2)`) |
| First-write source | `riseup-git-logs init` (per §40 §4 first-run bootstrap) |
| Subsequent writes | Per §43 upload-protocol response handler (refreshes `currentHead`, `uploadUrl`, `uploadedAt`, `expiresAt`, `autofixDownloadUrl`) |
| .gitignore | The CLI MUST NOT add this file to `.gitignore`; that is the user's choice |
| Forbidden | Any write that does NOT pass JSON Schema validation in §3 below; any write before `repoIdentityHash` is computed (§40 §3 step 4) |

## 2. Field Inventory (Normative — Closed Set)

The schema is a **closed object** (`additionalProperties: false`). Adding a 9th top-level field is a SPEC VIOLATION until a follow-up phase ships an extension AC under §97.

| # | Field | Type | Required? | Source | Lifecycle |
|---|---|---|---|---|---|
| 1 | `schemaVersion` | string (SemVer `MAJOR.MINOR.PATCH`) | YES | This document's `Version:` banner | Pinned at write time; consumers MUST reject `MAJOR` mismatch |
| 2 | `repoIdentityHash` | string (64 lowercase hex chars — full sha256) | YES | §40 §3 step 4 algorithm | Immutable across the file's lifetime; mismatch → `INTERNAL` |
| 3 | `repoCanonicalRemote` | string (URL) | YES | Pre-hash canonical form: lowercase + strip `.git` + strip trailing `/` | Documents what was hashed (auditability); never used for routing |
| 4 | `currentHead` | string (40 lowercase hex chars — full git SHA-1) | YES | `git rev-parse HEAD` at write time | Refreshed on every successful upload |
| 5 | `uploadUrl` | string (URL, https only) | NO (absent until first upload) | Returned by §43 upload protocol response | Refreshed when server rotates the endpoint |
| 6 | `uploadedAt` | string (RFC 3339 UTC, e.g. `2026-05-07T12:34:56Z`) | NO (absent until first upload) | Server `Date` header at upload completion | Refreshed on every successful upload |
| 7 | `expiresAt` | string (RFC 3339 UTC) | NO (present iff `uploadUrl` present) | Server-supplied; consumers treat absent ⇒ no expiry | Used to gate "stale pointer" warnings; mirror of spec/13 AC-SD-23 TTL/expiry pattern |
| 8 | `autofixDownloadUrl` | string (URL, https only) or `null` | NO (absent until server proposes a patch) | §44 auto-fix protocol response | `null` means "no fixable findings"; absent means "not yet computed" |

**Forbidden top-level fields** (any presence = SPEC VIOLATION; auditor MUST flag): `token`, `apiKey`, `secret`, `password`, `sshKey`, `privateKey`, `userId`, `userEmail`, `ownerEmail`, `env`, `platform` (the last three mirror the spec/22 §07 locked-decision-12 forbidden set).

## 3. JSON Schema (Draft-07, Normative)

This block is the **single source of truth** for `.riseup-git-logs.json` validation. CLI implementations MUST embed this schema verbatim and run it on every read AND every write. Any divergence between this block and CLI behaviour is a SPEC VIOLATION.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://spec.riseup-it.com/22-git-logs-v2/41-cli-pointer-file.schema.json",
  "title": "RiseupGitLogsPointerFile",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "repoIdentityHash", "repoCanonicalRemote", "currentHead"],
  "properties": {
    "schemaVersion": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "SemVer of this schema document; consumers MUST reject MAJOR mismatch."
    },
    "repoIdentityHash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "sha256(canonical-remote-url) lowercase hex; immutable across file lifetime."
    },
    "repoCanonicalRemote": {
      "type": "string",
      "format": "uri",
      "minLength": 1,
      "maxLength": 2048,
      "description": "Pre-hash canonical form (lowercase, no trailing .git, no trailing /); auditability only."
    },
    "currentHead": {
      "type": "string",
      "pattern": "^[0-9a-f]{40}$",
      "description": "Full 40-char git SHA-1 from `git rev-parse HEAD` at last write."
    },
    "uploadUrl": {
      "type": "string",
      "format": "uri",
      "pattern": "^https://",
      "maxLength": 2048
    },
    "uploadedAt": {
      "type": "string",
      "format": "date-time",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$",
      "description": "RFC 3339 UTC, second precision, trailing Z mandatory."
    },
    "expiresAt": {
      "type": "string",
      "format": "date-time",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "autofixDownloadUrl": {
      "type": ["string", "null"],
      "pattern": "^(https://.+)?$",
      "maxLength": 2048
    }
  },
  "dependencies": {
    "uploadUrl": ["uploadedAt"],
    "uploadedAt": ["uploadUrl"],
    "expiresAt": ["uploadUrl"]
  }
}
```

## 4. Reference Examples

### 4.1 First-run pointer (post-`init`, pre-upload)

```json
{
  "schemaVersion": "1.0.0",
  "repoIdentityHash": "3f2a8b1c9d4e6f7a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a",
  "repoCanonicalRemote": "https://github.com/example/repo",
  "currentHead": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
}
```

### 4.2 Post-upload pointer with no fixable findings

```json
{
  "schemaVersion": "1.0.0",
  "repoIdentityHash": "3f2a8b1c9d4e6f7a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a",
  "repoCanonicalRemote": "https://github.com/example/repo",
  "currentHead": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1",
  "uploadUrl": "https://logs.example.com/u/3f2a8b1c",
  "uploadedAt": "2026-05-07T12:34:56Z",
  "expiresAt": "2026-08-05T12:34:56Z",
  "autofixDownloadUrl": null
}
```

### 4.3 Post-upload pointer with auto-fix patch available

```json
{
  "schemaVersion": "1.0.0",
  "repoIdentityHash": "3f2a8b1c9d4e6f7a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a",
  "repoCanonicalRemote": "https://github.com/example/repo",
  "currentHead": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1",
  "uploadUrl": "https://logs.example.com/u/3f2a8b1c",
  "uploadedAt": "2026-05-07T12:34:56Z",
  "expiresAt": "2026-08-05T12:34:56Z",
  "autofixDownloadUrl": "https://logs.example.com/fix/3f2a8b1c/b2c3d4d4.patch"
}
```

## 5. Validation Discipline (Normative)

Every CLI invocation MUST enforce this validation table:

| Trigger | Action on schema violation |
|---|---|
| Read at startup | Treat as "no pointer file" → enter first-run bootstrap (§40 §4) + emit `WARNING` |
| Write before atomic-rename | Abort write, emit `INTERNAL` per spec/13 AC-21, exit non-zero |
| `MAJOR` schema-version mismatch on read | Refuse to upload until user runs `riseup-git-logs init --force` |
| `repoIdentityHash` mismatch vs recomputed | Refuse to upload, emit `INTERNAL` (likely repo moved or pointer copied between repos) |
| Forbidden field present | Refuse to upload, emit `INTERNAL`, surface `GL-POINTER-FORBIDDEN-FIELD` per spec/22 §15 |

## 6. SemVer Discipline for This Schema

- **PATCH** — clarification of an existing field's `description`; reordering example blocks.
- **MINOR** — adding an optional field (NOT in `required`) with `additionalProperties: false` still satisfied via explicit `properties` entry.
- **MAJOR** — adding a required field; tightening pattern/format on an existing field; removing/renaming a field; adding to the forbidden-fields list.

Every `MAJOR` bump MUST ship in its own §97 extension AC under spec/22 (cannot piggyback on AC-83) and MUST extend AC-80's row 35 with a `**Schema major version:** N` annotation.

---

## 7. Worked Example Lifecycle (Non-Normative)

> **Status:** `kind: example` — non-normative illustration per **Lesson #29**. Walks the pointer file across three lifecycle events: (a) first-run create, (b) upload-success update, (c) `MAJOR` schema-bump migration. Concrete values are fixtures; do not treat as test vectors. The normative wire format is §3, lifecycle is §1, validation is §5.

### 7.1 Setup givens

- Repo: `https://github.com/example/repo` (canonical remote per §40 §3 step 2)
- Local clone has just been freshly cloned; `.riseup-git-logs.json` does not exist
- User runs `riseup-git-logs init` (per §40 §4)

### 7.2 Event A — first-run bootstrap (file create)

1. CLI computes `repoIdentityHash` per §40 §3 step 4 (5-step algorithm)
2. CLI prepares minimal pointer object (no `uploadUrl`/`uploadedAt`/`expiresAt`/`autofixDownloadUrl` yet — those are populated by §43 upload):

```json
{
  "schemaVersion": "1.0.0",
  "repoIdentityHash": "3f2a8b1c9d4e6f7a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a",
  "repoCanonicalRemote": "https://github.com/example/repo",
  "currentHead": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
}
```

3. CLI writes to `.riseup-git-logs.json.tmp.4711` (PID suffix), then `rename(2)` to `.riseup-git-logs.json` (spec/13 AC-22 atomic discipline — link-don't-restate)
4. Mode set to `0644`; UTF-8 no BOM; LF line endings (per §1 row 2-3)
5. Exit 0; user sees `INFO  Pointer file initialised at <git-root>/.riseup-git-logs.json`

### 7.3 Event B — post-upload refresh (success path)

User runs `riseup-git-logs upload`. Per §43 §8 worked transcript, the server responds 200 OK with `OUTCOME_OK_NO_FIXES`. The upload-response handler MUST:

1. Recompute `currentHead` from `git rev-parse HEAD` (may differ from §7.2 if user committed since init)
2. Merge response fields into existing pointer object (do NOT discard `repoIdentityHash` / `repoCanonicalRemote`):

```json
{
  "schemaVersion": "1.0.0",
  "repoIdentityHash": "3f2a8b1c9d4e6f7a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a",
  "repoCanonicalRemote": "https://github.com/example/repo",
  "currentHead": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1",
  "uploadUrl": "https://logs.example.com/u/3f2a8b1c",
  "uploadedAt": "2026-05-10T09:15:42Z",
  "expiresAt": "2026-08-08T09:15:42Z",
  "autofixDownloadUrl": null
}
```

3. Atomic temp-then-rename (same discipline as §7.2 step 3)
4. JSON Schema validation per §3 MUST pass before rename — if validation fails, abort and emit `INTERNAL` per §5 row 2

### 7.4 Event C — MAJOR schema-bump migration (e.g. 1.x → 2.0.0)

Suppose a future Phase ships AC-NN extending AC-83 with a required field `repoIdentityVersion: integer` (forces `MAJOR` per §6).

1. User upgrades CLI binary; old pointer on disk still has `schemaVersion: 1.0.0`
2. Next `riseup-git-logs <any-command>` reads the file, validates against the bundled v2.0.0 schema → MAJOR mismatch detected per §5 row 3
3. CLI emits `WARNING  Pointer file schemaVersion 1.0.0 is incompatible with installed CLI (expects 2.0.0). Run \`riseup-git-logs init --force\` to regenerate.`
4. CLI exits non-zero; refuses to upload until user runs the migration command (per §5 row 3 — "Refuse to upload until user runs init --force")
5. `init --force` performs §7.2 bootstrap fresh, optionally preserving `repoIdentityHash` if the algorithm version is unchanged

### 7.5 Negative path — `repoIdentityHash` mismatch (pointer copied across repos)

User copies `.riseup-git-logs.json` from RepoA into RepoB. Next CLI invocation:

1. Reads pointer; `repoIdentityHash = <RepoA hash>`
2. Recomputes per §40 §3 step 4 against current working tree → `<RepoB hash>` ≠ stored value
3. Per §5 row 4, CLI refuses to upload, emits `INTERNAL` with hint: "pointer file appears to belong to a different repository (hash mismatch); run `riseup-git-logs init --force` to regenerate"
4. Exit non-zero; pointer file is NOT modified (read-only operation on the failure path)

---

## Cross-link

- §97 AC-83 binds this file (governing AC for slot §41)
- §97 AC-80 Sibling File Delegation Map row 35 (`41-cli-pointer-file-schema.md` → AC-83)
- §40 §3–§4 (5-step identity algorithm + first-run bootstrap consume the fields defined here)
- spec/13 §97 AC-22 (atomic write discipline — link-don't-restate)
- spec/14 §97 AC-23 (pattern reference: update-interface-contract pointer-file shape)
- spec/05 §97 AC-SD-23 (TTL/`ExpiresAt` precedent — pattern reference for `expiresAt` semantics)

---
kind: interface-contract
content_axis: normative-cli-test-plan
axis_rationale: "riseup-git-logs CLI test plan; tier-1 J-series test-coverage closure for §40-§44 contract surfaces"
---

# `riseup-git-logs` CLI — Test Plan (J-series tier-1)

**Version:** 1.0.0
**Updated:** 2026-05-07 (Phase J15 — slot ships; AC-87 binds this file in §97)
<!-- verified-phase: 155 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-87). Final J-series slot (§40–§45 sextet now complete).
> Per **Lesson #36** (link-don't-restate): contracts under test are owned by §40 (binary identity), §41 (pointer-file wire format), §42 (classifier outcome rules), §43 (upload protocol envelope + retry), §44 (auto-fix protocol). This file binds **what to assert**, never restates **what the contract is**. The WP-CLI/PHP server-side test plan is owned by §32 (`32-cli-test-plan.md`); §45 is the CLI-binary client-side mirror.
> Per **Lesson #21** (intra-module sibling-file delegation): bound from §97 AC-87 by name; row 42 of AC-80 Sibling File Delegation Map.
> Per **Lesson #19** (audit-boundary pin): the 6-section test-plan contract is enumerated as a normative tier-1 surface here; restating any of it in §40, §41, §42, §43, §44, or §32 is FORBIDDEN.

---

## 1. Purpose & Scope

End-to-end test strategy for the `riseup-git-logs` CLI binary built per spec/13 generic-cli framework. Closes the **coverage-targets contract** for the five J-series tier-1 contract surfaces (§40–§44). Provider-agnostic stages with a GitHub Actions reference implementation per spec/12.

**In scope:** test layer architecture, the closed **5-suite test matrix** (T-CLI-IDENT, T-CLI-PTR, T-CLI-CLASSIFY, T-CLI-UPLOAD, T-CLI-AUTOFIX), per-suite Given/When/Then enumerations bound 1:1 to AC-82..AC-86 sub-contracts, fixture taxonomy, coverage targets, and CI binding.

**Out of scope:** WP-CLI/PHP server-side surface (owned by §32); spec/13 generic-cli framework self-tests (owned by spec/13 §97); spec/12 CI/CD pipeline runner matrix (owned by spec/12 §97 AC-10); UI/visual regression of any admin page (owned by spec/24).

---

## 2. Two-layer test architecture

| Layer | Tool | What it owns | Where it runs |
|---|---|---|---|
| **L1 — Go unit + integration** | Go `testing` + `httptest` | per-package contract assertions: `pointer.Marshal/Unmarshal` (§41), `classifier.Classify` (§42), `upload.Stream` (§43), `autofix.Apply` (§44), `identity.Discover` (§40) | every push (≤30s) |
| **L2 — Bats end-to-end** | Bats + a stub `git-logs-server` mock (Go test binary) | invoke the built `riseup-git-logs` binary; assert exit codes per spec/13 AC-21, NDJSON-on-the-wire frame shapes, atomic on-disk pointer-file rewrites | every push (≤90s) |

Property/fuzz tests (NDJSON parser, JSON-Schema Draft-07 validator) are deferred to spec/13 framework tests; this plan does NOT duplicate them per Lesson #36.

---

## 3. Closed 5-suite test matrix

The matrix is **closed** (no other suites permitted at tier-1 — additions require an AC-87 amendment + AC-80 row update in the same phase). Each suite binds 1:1 to a J-series tier-1 AC.

| Suite ID | Binds AC | Owning §97 contract | Layer | Min cases |
|---|---|---|---|---|
| **T-CLI-IDENT** | AC-82 | §40 (5-step identity discovery + binary identity) | L1 + L2 | 7 |
| **T-CLI-PTR** | AC-83 | §41 (8-field pointer-file wire format + JSON Schema) | L1 + L2 | 9 |
| **T-CLI-CLASSIFY** | AC-84 | §42 (4-outcome closed set + per-subcommand rule tables A/B/C/D) | L1 | 11 |
| **T-CLI-UPLOAD** | AC-85 | §43 (NDJSON-over-HTTPS + 9-field envelope + retry + idempotency) | L1 + L2 | 13 |
| **T-CLI-AUTOFIX** | AC-86 | §44 (download + 7-field bundle + 4-state outcome + 7-step preflight + atomic apply) | L1 + L2 | 12 |

Each row's **Min cases** is the floor enumerated in §4 below. Implementations MAY add cases; they MUST NOT remove.

---

## 4. Per-suite GWT enumerations

### 4.1 T-CLI-IDENT (binds AC-82, owns §40)

| Case | Given | When | Then |
|---|---|---|---|
| `IDENT-01` | repo with `origin` remote `git@github.com:owner/repo.git` | identity discovery runs | `repoIdentityHash` = sha256 of canonical-form `git@github.com:owner/repo.git` (per §40 §3 step 5) |
| `IDENT-02` | repo with multiple remotes (`origin`, `upstream`) | discovery runs | `origin` selected per §40 §3 step 1 priority order |
| `IDENT-03` | repo with no `origin` and only `upstream` | discovery runs | `upstream` selected as fallback per §40 §3 step 2 |
| `IDENT-04` | repo with no remotes | discovery runs | exits `ExitCode.UserError` with `GL-IDENT-NO-REMOTE` per spec/13 AC-21 link-don't-restate |
| `IDENT-05` | repo with `https://github.com/owner/repo` remote | discovery runs | URL canonicalised to SSH form per §40 §3 step 4 BEFORE hashing |
| `IDENT-06` | non-git directory | discovery runs | exits `ExitCode.UserError` with `GL-IDENT-NOT-A-REPO` |
| `IDENT-07` | repo with detached HEAD | discovery runs | `currentHead` = the detached SHA (40-hex); does NOT fail |

### 4.2 T-CLI-PTR (binds AC-83, owns §41)

| Case | Given | When | Then |
|---|---|---|---|
| `PTR-01` | a valid 8-field pointer-file body | `pointer.Marshal` | bytes match the lexicographic key order per §41 §3 (deviation = test fail) |
| `PTR-02` | a valid pointer-file on disk | `pointer.Unmarshal` | all 8 fields populate; `additionalProperties` rejected |
| `PTR-03` | pointer-file with a forbidden top-level field (e.g. `frames`) | `Unmarshal` | rejects with `GL-PTR-FORBIDDEN-FIELD` (per §41 §4 11-entry list) |
| `PTR-04` | pointer-file with `schemaVersion` ≠ supported value | `Unmarshal` | rejects with `GL-PTR-SCHEMA-MISMATCH` |
| `PTR-05` | a fresh `Marshal` followed by atomic write | `os.Stat` | `<path>.riseup-ptr.<uuid>.tmp` removed; final file present (spec/13 AC-22 link-don't-restate) |
| `PTR-06` | atomic write where the `rename()` syscall fails (mocked) | write attempted | NO partial on-disk pointer-file remains; error returned |
| `PTR-07` | pointer-file where `expiresAt` is in the past | freshness check | reports `STALE` (does NOT auto-refresh — refresh is server-issued per §48) |
| `PTR-08` | pointer-file with `autofixDownloadUrl: null` | bundle-presence check | reports `NO_BUNDLE` |
| `PTR-09` | pointer-file with `autofixDownloadUrl: "https://..."` matching §47 path shape | check | reports `BUNDLE_AVAILABLE` |

### 4.3 T-CLI-CLASSIFY (binds AC-84, owns §42)

| Case | Given | When | Then |
|---|---|---|---|
| `CLASSIFY-01` | subcommand A success exit 0, no stderr | `classifier.Classify` | outcome = `NORMAL` per §42 rule table A row 1 |
| `CLASSIFY-02` | subcommand A exit 0, stderr contains `WARN:` | classify | outcome = `WARN` per rule table A row 2 |
| `CLASSIFY-03` | subcommand A exit 1 | classify | outcome = `ERROR` per rule table A row 3 |
| `CLASSIFY-04` | subcommand A exit ≥2 | classify | outcome = `INTERNAL` per rule table A row 4 |
| `CLASSIFY-05..08` | rule table B inputs | classify | outcomes per §42 table B (4 rows) |
| `CLASSIFY-09..10` | rule table C inputs | classify | outcomes per §42 table C (2 rows) |
| `CLASSIFY-11` | subcommand without a rule-table assignment | classify | rejects with `GL-CLASSIFIER-UNBOUND` per §42 forbidden-non-determinism (NO default-to-NORMAL) |

### 4.4 T-CLI-UPLOAD (binds AC-85, owns §43)

| Case | Given | When | Then |
|---|---|---|---|
| `UPLOAD-01` | a 5-frame batch | `upload.Stream` | NDJSON body has 5 LF-terminated frames; each frame conforms to the 9-field closed set per §43 §3 |
| `UPLOAD-02` | a frame with a forbidden field (e.g. `executablePath`) | stream | rejects pre-flight with `GL-UPLOAD-FORBIDDEN-FIELD` (16-entry list per §43 §3) |
| `UPLOAD-03` | a 10 000-frame batch (cap floor) | stream | succeeds; mock-server receives all 10 000 |
| `UPLOAD-04` | a 10 001-frame batch (cap +1) | stream | rejects pre-flight with `GL-UPLOAD-CAP-EXCEEDED` |
| `UPLOAD-05` | mock server returns 503 once then 200 | stream | retries per §43 §5 6-attempt schedule with exponential-backoff + jitter |
| `UPLOAD-06` | mock server returns 503 six times | stream | exits `ExitCode.Internal` with `GL-UPLOAD-RETRY-EXHAUSTED` after 6th attempt |
| `UPLOAD-07` | identical batch retried within idempotency window | stream | mock server sees the SAME `Idempotency-Key` (UUIDv4) for both attempts |
| `UPLOAD-08` | mock server returns 409 `GL-UPLOAD-IDEMPOTENCY-CONFLICT` | stream | exits `ExitCode.UserError`; does NOT retry |
| `UPLOAD-09` | mock server returns 401 `GL-AUTH-LANE-MISMATCH` | stream | exits `ExitCode.UserError`; does NOT retry |
| `UPLOAD-10` | gzipped 16 MiB body (compressed cap) | stream | mock server receives `Content-Encoding: gzip` and accepts |
| `UPLOAD-11` | gzipped 16 MiB + 1 byte body | stream | rejects pre-flight with `GL-UPLOAD-PAYLOAD-TOO-LARGE` |
| `UPLOAD-12` | mock 200 response carries `autofixDownloadUrl` | stream | client surfaces the URL via stdout per §43 §6; pointer-file is NOT auto-rewritten (refresh-pointer is a separate flow per §48) |
| `UPLOAD-13` | server-issued `Idempotency-Key` is REUSED by the client (programmer error) | stream | rejects pre-flight with `GL-UPLOAD-IDEMPOTENCY-REUSE` (key MUST be per-batch-fresh per §43 §4) |

### 4.5 T-CLI-AUTOFIX (binds AC-86, owns §44)

| Case | Given | When | Then |
|---|---|---|---|
| `AUTOFIX-01` | `autofixDownloadUrl: null` | `autofix.Apply` | exits `ExitCode.OK` with `NO_BUNDLE`; NO HTTP request made |
| `AUTOFIX-02` | `autofixDownloadUrl` over plain HTTP | apply | rejects with `GL-FIX-SCHEME-INVALID` (https-only per §44 §2) |
| `AUTOFIX-03` | `autofixDownloadUrl` returns 7-field bundle with `schemaBump: patch` | apply | preflight 7-step succeeds; patches applied; outcome `APPLIED` per §44 §4 |
| `AUTOFIX-04` | bundle with `schemaBump: major`, `--auto-confirm` set | apply | `--auto-confirm` IGNORED for major; user prompt shown; outcome `REJECTED_USER` if user declines per §44 §4 |
| `AUTOFIX-05` | bundle with `expiresAt` in the past | apply | rejects with `GL-FIX-EXPIRED`; outcome `REJECTED_PRECONDITION` |
| `AUTOFIX-06` | bundle's `targetHead` ≠ current HEAD | apply | rejects with `GL-FIX-HEAD-DRIFT` per §44 §4 step 3 |
| `AUTOFIX-07` | working tree dirty (`git status` non-empty) | apply | rejects with `GL-FIX-DIRTY-TREE` per §44 §4 step 5; NO auto-stash |
| `AUTOFIX-08` | bundle patch where `beforeSha256` ≠ on-disk sha | apply | rejects with `GL-FIX-BEFORE-MISMATCH` |
| `AUTOFIX-09` | bundle with 3 patches; mid-bundle `rename()` fails on patch 2 | apply | STOP; outcome `DEFERRED_NETWORK`; patch 1 remains applied; NO automatic rollback per §44 §5 |
| `AUTOFIX-10` | successful `APPLIED` | post-apply observation | pointer-file `autofixDownloadUrl` set to `null`; `uploadedAt` + `expiresAt` refreshed per §44 §6; CLI does NOT run `git add`/`git commit` |
| `AUTOFIX-11` | successful `APPLIED` followed by re-fetch of same URL | second apply | rejects with `GL-FIX-CONSUMED` (single-consumption invariant per §44 §6 + §47 §5) |
| `AUTOFIX-12` | bundle response carries a forbidden field (e.g. `executablePath`) | apply | rejects with `GL-FIX-FORBIDDEN-FIELD` per §44 §3 17-entry list |

---

## 5. Fixture taxonomy

| Fixture kind | Location | Owner |
|---|---|---|
| Mock `git-logs-server` (Go test binary) | `cli/testdata/mock-server/` | §43 + §44 + §47 + §48 contracts |
| Sample pointer files (8 valid + 11 forbidden-field variants) | `cli/testdata/pointer/` | §41 §2 + §41 §4 |
| Sample upload batches (3 frame counts × 3 outcome mixes) | `cli/testdata/upload/` | §43 §3 |
| Sample fix bundles (12 cases mirroring T-CLI-AUTOFIX) | `cli/testdata/autofix/` | §44 §3 |

The `33-bats-test-skeleton.md` Bats skeleton is the reference L2 harness; the `34-phpunit-test-skeleton.md` PHPUnit skeleton stays §32-bound (WP-CLI/PHP server-side). §45 does NOT introduce a new fixture skeleton file — fixtures are co-located with the Go cli source per Go convention.

---

## 6. Coverage targets

| Target | Floor | Owner |
|---|---|---|
| L1 line coverage on `pkg/{identity,pointer,classifier,upload,autofix}` | ≥ 85 % | this AC |
| L2 case count | ≥ 52 (sum of §3 Min cases column: 7+9+11+13+12) | this AC |
| Every `GL-*` error code cited in §40–§44 has at least one negative-path test | 100 % | this AC |
| Every `ExitCode` enum value cited in §40–§44 has at least one positive test | 100 % | this AC |

CI binding: spec/12 §97 AC-10 runner matrix row 1 (`ubuntu-latest`) executes both layers; row 2 (`macos-latest`) executes L1 only (Bats `flock` semantics differ — accepted exception per §32 precedent).

---

## 7. Forbidden patterns

- Restating the §41 8-field shape, §43 9-field envelope, §44 7-field bundle envelope, or §42 4-outcome set inline in this file (Lesson #36 violation — citation by AC + section anchor only).
- Restating the spec/13 AC-21 `ExitCode` enum, AC-22 atomic-write discipline, or spec/12 AC-10 runner matrix inline.
- Adding a 6th tier-1 suite without an AC-87 amendment + AC-80 row update.
- Removing any `Min cases` floor.
- Hard-coding the mock-server's port (must be ephemeral; CI matrix runs in parallel).
- Coupling L1 and L2 fixtures (each layer owns its own fixtures so removing one layer does not blast-radius the other).

---

## Cross-References

- §40 (binary identity + 5-step discovery; AC-82)
- §41 (pointer-file wire format; AC-83)
- §42 (classifier outcomes + rule tables; AC-84)
- §43 (upload protocol; AC-85)
- §44 (auto-fix protocol; AC-86)
- §32 (WP-CLI/PHP server-side test plan — sibling, NOT this file)
- §33 (Bats test skeleton — reference L2 harness)
- spec/12 §97 AC-10 (CI runner matrix)
- spec/13 §97 AC-21 (ExitCode enum), AC-22 (atomic write)

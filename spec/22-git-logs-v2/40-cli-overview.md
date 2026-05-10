---
kind: interface-contract
content_axis: normative-cli-binary-contract
axis_rationale: "riseup-git-logs CLI binary architecture overview; tier-1 entry point for the J-series CLI subsystem (slots §40–§45)"
---

# `riseup-git-logs` CLI — Architecture Overview

**Version:** 1.0.0
**Updated:** 2026-05-07 (Phase J10 — slot ships; AC-82 binds this file in §97)
<!-- verified-phase: 154 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-82). New file slot — first of the J-series CLI subsystem (§40–§45).
> Per **Lesson #36** (link-don't-restate): all generic-CLI framework contract — typed `ExitCode` enum, DB+file concurrency, subcommand checklist binding — is owned by **spec/13-generic-cli §97 AC-21 / AC-22 / AC-23**. This file cites those ACs by anchor and **does not restate their bodies**.
> Per **Lesson #21 / Lesson #39** (intra-module sibling-file delegation): every J-series sibling file (§40–§45) is bound from §97 by name and listed in AC-80's Sibling File Delegation Map.

---

## 1. Purpose & Scope

`riseup-git-logs` is a **standalone client-side CLI binary** that wraps a closed set of read-only `git` subcommands, classifies their output, streams the classified payload to the spec/22 WordPress plugin's REST surface (per `04-rest-api-endpoints.md`), and surfaces a server-returned auto-fix URL inside a JSON pointer file written at the host repository's git root.

Three explicit out-of-scope boundaries:

1. **Server endpoints** that receive uploads — those are owned by spec/22 §04 (REST) + §39 (split-DB log storage).
2. **Patch-generation logic** behind the auto-fix URL — owned server-side; this CLI only consumes the protocol.
3. **Generic-CLI framework concerns** (exit codes, DB concurrency, subcommand wiring) — owned by spec/13 §97; cross-referenced here, never restated.

## 2. Wrap Scope (Normative — Closed Set)

The CLI wraps **exactly four** git subcommands. Adding a fifth is a SPEC VIOLATION until a follow-up phase ships an extension AC under §97.

| Subcommand | Read-only? | Classifier surface | Notes |
|---|---|---|---|
| `git log` | YES | per §42 Section A | Primary use case — full commit history streaming |
| `git status` | YES | per §42 Section B | Working-tree state snapshot |
| `git diff` | YES | per §42 Section C | Unstaged + staged hunks; binary diffs classified `INTERNAL` |
| `git show` | YES | per §42 Section D | Single-commit drilldown; piggybacks on §42 A+C rules |

Forbidden (any invocation = `INTERNAL` exit + non-zero exit code per spec/13 AC-21 typed `ExitCode` enum):

- `git push`, `git pull`, `git fetch`, `git commit`, `git reset`, `git rebase`, `git checkout`, `git merge`, `git stash`, `git clean`, `git config --set` — anything that mutates working tree, index, refs, or remote.

## 3. Identity & Discovery (Normative)

The CLI determines repo identity at every invocation via this **5-step algorithm** (deterministic, no network):

1. Locate repo root: `git rev-parse --show-toplevel`. If non-zero exit → emit `INTERNAL` + exit per spec/13 AC-21.
2. Read `.riseup-git-logs.json` at repo root if present (schema per §41); otherwise enter first-run bootstrap (see §4).
3. Compute current head: `git rev-parse HEAD` (full 40-char SHA).
4. Compute repo identity hash: `sha256(<canonical-remote-url>)[0:32]` where `<canonical-remote-url>` = the `origin` remote's `git config remote.origin.url` value, lowercased, with trailing `.git` and trailing slash stripped (canonicalisation pinned in §41 schema). Stored as `repoIdentityHash` in the pointer file.
5. Bind the discovered identity (`repoIdentityHash` + `currentHead`) to every NDJSON frame uploaded per §43.

**Forbidden:** writing or mutating `.riseup-git-logs.json` BEFORE step 4 succeeds. Atomic temp-then-rename per spec/13 AC-22 is mandatory for every write to this file.

## 4. First-Run Bootstrap

If `.riseup-git-logs.json` is absent at repo root:

- The CLI MUST refuse to upload until the user runs `riseup-git-logs init` (idempotent — no-op if file already exists with valid schema).
- `init` writes a minimal pointer file (per §41 schema) carrying only the discovered identity fields; `uploadUrl`, `autofixDownloadUrl`, `uploadedAt`, `expiresAt` are populated on the first successful upload (per §43).
- The file MUST NOT be added to `.gitignore` automatically — that is the user's decision (this CLI never mutates `.gitignore`).

## 5. Cross-References (Lesson #36 — link-don't-restate)

The following normative surfaces are referenced by anchor only — **restating any of these in this file or in §41–§45 is a SPEC VIOLATION**:

| Concern | Owning surface | What this CLI consumes |
|---|---|---|
| Typed `ExitCode` enum | spec/13 §97 AC-21 | All exit codes from the wrapped subcommands MUST map through the enum; bare `os.Exit(N)` calls FORBIDDEN |
| DB+file concurrency | spec/13 §97 AC-22 | Atomic temp-then-rename for `.riseup-git-logs.json`; PID-locked update file under `~/.local/state/riseup-git-logs/` |
| Subcommand checklist | spec/13 §97 AC-23 | Every wrapped subcommand MUST appear in the spec/13 framework's subcommand registry; orphan subcommands FORBIDDEN |
| REST upload surface | spec/22 §04 + §39 | NDJSON streaming target; payload scoped by `repoIdentityHash` |
| Auth lane | spec/22 §31 (SSH-key Lane B) | Reused as-is; this CLI does NOT add a new auth lane |
| Pointer-file wire format | spec/14 §97 AC-23 (pattern reference only) | Same atomic-write + JSON-Schema-Draft-07 + `expiresAt` discipline; concrete schema lives in §41 |

## 6. Document Scope (J-Series Inventory)

The J-series CLI subsystem comprises six normative slots. This file (§40) is the entry point.

| Slot | File | Owns |
|---|---|---|
| §40 | `40-cli-overview.md` (this file) | Architecture + scope + identity + cross-references |
| §41 | `41-cli-pointer-file-schema.md` | JSON Schema (Draft-07) for `.riseup-git-logs.json` |
| §42 | `42-cli-classifier-rules.md` | Per-subcommand error/normal classification rules |
| §43 | `43-cli-upload-protocol.md` | NDJSON streaming wire format CLI ↔ server |
| §44 | `44-cli-autofix-protocol.md` | Hybrid propose-diff-confirm fix flow |
| §45 | `45-cli-test-plan.md` | GWT scenarios + bats skeleton |

Slots §41–§45 ship in subsequent phases (J11–J15). Each ships under its own §97 AC binding (AC-83..AC-87 reserved).

---

## Cross-link

- §97 AC-82 binds this file (governing AC for slot §40)
- §97 AC-80 Sibling File Delegation Map row 34 (`40-cli-overview.md` → AC-82)
- spec/13 §97 AC-21 / AC-22 / AC-23 (framework contract — link-don't-restate)
- spec/22 §04 (REST endpoints — upload destination)
- spec/22 §39 (split-DB log storage — server-side scoping)

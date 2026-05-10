---
kind: interface-contract
content_axis: normative-cli-classifier-rules
axis_rationale: "riseup-git-logs CLI per-subcommand classifier rules; tier-1 wire-decision contract for the 4 wrapped subcommands × 4 outcome states"
---

# `riseup-git-logs` CLI — Classifier Rules

**Version:** 1.1.0
**Updated:** 2026-05-10 (Phase L4 — non-normative §7 Worked Example Decisions added; pattern from L1/L2/L3)
<!-- verified-phase: 154 -->

> **Status:** Normative tier-1 (governing AC: §97 AC-84). Third of the J-series CLI subsystem (§40–§45).
> Per **Lesson #36** (link-don't-restate): typed exit-code mapping is owned by **spec/13 §97 AC-21**; this file maps each classifier outcome to an `ExitCode` enum value by name and **does not restate the enum body**. Error-code identifiers (`GL-CLASSIFIER-*`) are owned by spec/22 §15.
> Per **Lesson #21** (intra-module sibling-file delegation): bound from §97 AC-84 by name; row 36 of AC-80 Sibling File Delegation Map.
> Per **Lesson #19** (audit-boundary pin): every classifier rule is enumerated as a normative table row directly in this tier-1 file; restating any row in §40, §41, §43, §44, or §45 is FORBIDDEN.

---

## 1. Purpose & Scope

The classifier is the **deterministic decision function** that consumes raw output from each wrapped git subcommand (per §40 §2 closed wrap-set) and emits a structured `ClassifierOutcome` record per output frame. The outcome drives both (a) the `ExitCode` returned to the user shell (per spec/13 AC-21) and (b) the `outcome` field embedded in every NDJSON frame uploaded per §43.

**In scope:** decision rules per subcommand, the 4 outcome states, deterministic precedence, forbidden non-determinism patterns, classifier versioning.

**Out of scope:** the NDJSON wire format itself (§43); the auto-fix protocol consuming `ERROR` outcomes (§44); the bats test plan (§45).

## 2. Outcome State Set (Normative — Closed Set of 4)

Every classifier invocation MUST emit exactly one of these four outcomes per frame:

| Outcome | Meaning | Maps to `ExitCode` (spec/13 AC-21) | Uploaded to server? |
|---|---|---|---|
| `NORMAL` | Subcommand exited 0; output matches subcommand-specific normal-pattern set. | `ExitCode.OK` (0) | YES |
| `WARN` | Subcommand exited 0 BUT output contains a known advisory pattern (e.g. `git log` reached a shallow boundary; `git diff` produced a binary-file notice). | `ExitCode.OK` (0) | YES |
| `ERROR` | Subcommand exited non-zero AND output matches a known recoverable error pattern catalogued below (auto-fix may be offered per §44). | `ExitCode.UserError` (2) | YES |
| `INTERNAL` | Subcommand failed in a way the classifier cannot explain (unknown stderr pattern, unparseable output, identity-discovery failure per §40 §3 step 1, forbidden-subcommand invocation per §40 §2). | `ExitCode.Internal` (3) | YES (with `redact: true` flag) |

**Forbidden:** any fifth outcome name; emitting `null`; emitting two outcomes for one frame; suppressing upload of any outcome (server-side scoping decides retention, not the CLI).

## 3. Deterministic Precedence (Normative)

When more than one rule could match a frame, the classifier MUST apply this **strict precedence order**:

1. **Forbidden-subcommand check** (§40 §2 forbidden list) → always `INTERNAL`. Wins over all other rules.
2. **Identity-discovery failure** (§40 §3 step 1 non-zero exit) → always `INTERNAL`. Wins over output-pattern matches.
3. **Subcommand exit code ≠ 0** → consult Section 4's per-subcommand `ERROR`-pattern table; if any pattern matches, emit `ERROR`; else emit `INTERNAL`.
4. **Subcommand exit code == 0 AND output matches `WARN` pattern** → emit `WARN`.
5. **Subcommand exit code == 0** (no `WARN` match) → emit `NORMAL`.

**Forbidden:** any non-deterministic tiebreaker (random, time-of-day, machine-local LANG/locale, environment-variable lookup beyond the canonical `GIT_*` set inherited from the shell). Classifier MUST be byte-deterministic given identical input + identical classifier version.

## 4. Per-Subcommand Rule Tables (Normative)

The four tables below are the **authoritative classifier surface**. Adding a new rule row requires a §97 extension AC + a `MINOR` bump of this slot's version banner. Removing or reworording a row is a `MAJOR` bump and requires a follow-up §97 extension AC.

### Section A — `git log`

| Rule ID | Trigger pattern (regex against combined stdout+stderr) | Outcome | Notes |
|---|---|---|---|
| LOG-N1 | exit==0; stdout matches `^commit [0-9a-f]{40}` | `NORMAL` | Standard commit log frame. |
| LOG-W1 | exit==0; stderr contains `warning: log.*shallow` | `WARN` | Shallow-clone boundary — non-fatal. |
| LOG-W2 | exit==0; stderr contains `replace ref` | `WARN` | git-replace ref applied — surfaced for auditor visibility. |
| LOG-E1 | exit!=0; stderr matches `fatal: bad default revision 'HEAD'` | `ERROR` | Empty repo — auto-fix offers `git commit --allow-empty -m "init"`. |
| LOG-E2 | exit!=0; stderr matches `fatal: ambiguous argument` | `ERROR` | Bad ref — auto-fix offers ref disambiguation prompt. |
| LOG-E3 | exit!=0; stderr matches `fatal: your current branch .* does not have any commits yet` | `ERROR` | Same as E1 alternate phrasing. |

### Section B — `git status`

| Rule ID | Trigger pattern | Outcome | Notes |
|---|---|---|---|
| STAT-N1 | exit==0; stdout starts with `On branch ` OR `HEAD detached` | `NORMAL` | Standard status output. |
| STAT-W1 | exit==0; stdout contains `nothing added to commit but untracked files present` | `WARN` | Advisory only. |
| STAT-W2 | exit==0; stdout contains `you have unmerged paths` | `WARN` | Merge state surfaced (not an error — user is mid-merge). |
| STAT-E1 | exit!=0; stderr matches `fatal: not a git repository` | `ERROR` | Identity-discovery would have caught this earlier (precedence 2); kept for defense-in-depth. |
| STAT-E2 | exit!=0; stderr matches `fatal: index file corrupt` | `ERROR` | Auto-fix offers `rm .git/index && git reset` (destructive — confirmation REQUIRED per §44). |

### Section C — `git diff`

| Rule ID | Trigger pattern | Outcome | Notes |
|---|---|---|---|
| DIFF-N1 | exit==0; stdout matches `^diff --git ` OR is empty (no diff) | `NORMAL` | Standard or empty diff. |
| DIFF-W1 | exit==0; stdout contains `Binary files .* differ` | `WARN` | Binary file — payload omitted from upload (`payload: null`); only the W1 marker uploaded. |
| DIFF-W2 | exit==0; stdout contains `\\ No newline at end of file` | `WARN` | Convention violation surfaced. |
| DIFF-E1 | exit!=0; stderr matches `fatal: ambiguous argument` | `ERROR` | Bad ref/path — auto-fix offers candidate list. |
| DIFF-E2 | exit!=0; stderr matches `error: Could not access '.*'` | `ERROR` | Missing file/blob — auto-fix offers `git checkout HEAD -- <path>`. |

### Section D — `git show`

`git show` piggybacks on Sections A (commit metadata frame) and C (diff frame). The classifier MUST split `git show` output at the first `diff --git ` line and apply Section A rules to the prefix, Section C rules to the suffix. Each half emits its own outcome; the **frame-level outcome** for `git show` is the **highest-severity** of the two halves under the order `NORMAL < WARN < ERROR < INTERNAL`.

| Rule ID | Trigger pattern | Outcome | Notes |
|---|---|---|---|
| SHOW-N1 | both halves classify `NORMAL` | `NORMAL` | Standard show. |
| SHOW-W1 | either half classifies `WARN` (no half `ERROR`) | `WARN` | Warn-promotion. |
| SHOW-E1 | either half classifies `ERROR` | `ERROR` | Error-promotion. |
| SHOW-E2 | exit!=0; stderr matches `fatal: bad object .*` | `ERROR` | Unknown commit — auto-fix offers `git fetch && git show <sha>` re-attempt. |

## 5. Forbidden Non-Determinism Patterns

The classifier MUST NOT:

- Read the user's `~/.gitconfig` for any decision (rules MUST be portable).
- Consult the system clock for any decision (`uploadedAt` is set in §43, not here).
- Cache state across invocations (each invocation is independent; precedence is purely per-frame).
- Use the locale (`LANG`/`LC_*`) — classifier patterns are matched against the canonical `LANG=C` git output; the CLI MUST set `LANG=C` for every wrapped invocation.
- Emit any outcome not in Section 2's closed set of 4.
- Skip emitting an outcome (every frame MUST be classified).

## 6. Classifier Versioning

This file's banner version (top) IS the classifier version. NDJSON frames per §43 MUST carry `classifierVersion` matching this banner. Server-side classifier-version mismatch is a soft signal (logged, not rejected); a `MAJOR` bump of this banner is a coordinated upgrade event surfaced under a follow-up §97 extension AC.

---

## 7. Worked Example Decisions (Non-Normative)

> **Status:** `kind: example` — non-normative illustration per **Lesson #29**. Walks the classifier across all 4 outcome enum values (`NORMAL`/`WARN`/`ERROR`/`INTERNAL`) using one representative input per outcome, then exercises the §3 deterministic-precedence ladder with two multi-trigger conflict cases. Concrete patterns are fixtures matched against `LANG=C` git output; do not treat as test vectors. The normative rule tables are §4, the precedence ladder is §3, the closed outcome set is §2.

### 7.1 Setup givens

- CLI invokes `LANG=C git <subcommand>` per §5 (locale-pinned)
- Each invocation produces one NDJSON frame uploaded via §43
- Each frame carries `classifierVersion: "1.1.0"` matching this file's banner per §6

### 7.2 Outcome A — `NORMAL` (`git log` on a clean branch)

**Input** (truncated):
```
commit a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
Author: Jane Dev <jane@example.com>
Date:   Sat May 10 09:14:21 2026 +0000

    Add classifier worked example
```

**Decision walk:**
1. §3 step 1 — exit code 0 → no `INTERNAL` short-circuit
2. §4 Section A — pattern matches `LOG-N1` (well-formed `commit <40-hex>` header, no `WARN`/`ERROR` triggers)
3. Outcome resolved: **`NORMAL`**
4. NDJSON frame: `{"subcommand":"log","outcome":"NORMAL","classifierVersion":"1.1.0",...}`
5. Exit code (per §13 AC-21 link-don't-restate): `ExitCode.OK`

### 7.3 Outcome B — `WARN` (`git status` on a dirty tree)

**Input:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   spec/22-git-logs-v2/42-cli-classifier-rules.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**Decision walk:**
1. §3 step 1 — exit 0; no `INTERNAL`
2. §4 Section B — `STATUS-W1` matches (`Changes not staged for commit:` line present without `Untracked files:` block escalation)
3. Outcome resolved: **`WARN`**
4. NDJSON frame: `{"subcommand":"status","outcome":"WARN",...}`
5. Exit code: `ExitCode.OK` (WARN is informational; non-zero exit reserved for `ERROR`/`INTERNAL` per spec/13 AC-21)

### 7.4 Outcome C — `ERROR` (`git diff` against a non-existent ref)

**Input** (stderr; exit 128):
```
fatal: ambiguous argument 'nonexistent-branch': unknown revision or path not in the working tree.
```

**Decision walk:**
1. §3 step 1 — exit 128 ≠ 0 → check §4 Section C error rules BEFORE precedence-ladder fallthrough
2. §4 Section C — `DIFF-E1` matches (`fatal: ambiguous argument` stderr pattern)
3. Outcome resolved: **`ERROR`**
4. NDJSON frame includes `errorCode: "GL-CLASSIFIER-DIFF-AMBIGUOUS-REF"` (owned by §15 — link-don't-restate)
5. §44 auto-fix flow MAY produce a fix bundle for this `ERROR` outcome (per §44 §2)
6. Exit code: `ExitCode.UserError` per spec/13 AC-21

### 7.5 Outcome D — `INTERNAL` (identity-discovery failure)

**Setup:** `riseup-git-logs upload` invoked outside any git working tree (no `.git/` ancestor).

**Decision walk:**
1. §40 §3 step 1 (identity discovery) fails — no `.git/` directory found in any ancestor
2. §3 precedence rule 2 fires immediately → **`INTERNAL`** short-circuits BEFORE any subcommand classification (no `git <cmd>` invocation occurs)
3. NDJSON frame is NOT produced (no upload — §43 requires a successful identity hash)
4. Stderr: `INTERNAL  No git repository found at <cwd> or any ancestor (GL-IDENTITY-NO-REPO)`
5. Exit code: `ExitCode.Internal` per spec/13 AC-21

### 7.6 Precedence conflict A — `WARN` + `ERROR` simultaneous (`git diff` on dirty tree with bad path)

**Input:** `git diff HEAD -- nonexistent.md` on a tree with other unstaged changes.

```
fatal: pathspec 'nonexistent.md' did not match any files
```

**Decision walk:**
1. §3 step 1 — exit 128 ≠ 0 → §4 Section C
2. Two rules match: `DIFF-W1` (dirty tree context) AND `DIFF-E2` (`Could not access` / pathspec failure family)
3. §3 precedence rule 3 — when multiple rules match a single frame, **highest-severity wins** under `NORMAL < WARN < ERROR < INTERNAL`
4. Resolved: **`ERROR`** (`DIFF-E2` beats `DIFF-W1`)
5. **Frame carries `ERROR` only** — never both, never a synthetic combined enum (§2 closed-set discipline)

### 7.7 Precedence conflict B — `git show` two-half split (Section D)

**Input:** `git show <sha>` where commit metadata is normal but the diff half hits `DIFF-W1` (large mechanical churn warning).

**Decision walk:**
1. §3 step 1 — exit 0
2. §4 Section D — splits output at first `diff --git ` line
3. Prefix half (Section A): `LOG-N1` → `NORMAL`
4. Suffix half (Section C): `DIFF-W1` → `WARN`
5. Section D rule `SHOW-W1` fires: frame-level outcome = highest-severity = **`WARN`**
6. **Single frame emitted** with `outcome: "WARN"` (NOT two frames; the §2 closed set is per-frame, not per-half)

### 7.8 Negative path — unknown subcommand (forbidden wrap-set)

User invokes `riseup-git-logs blame -- file.md`. `blame` is NOT in §40 §2 closed wrap-set `{log, status, diff, show}`.

1. CLI rejects pre-classifier (no `git blame` invocation)
2. Stderr: `INTERNAL  Subcommand 'blame' is not in the wrap-set (GL-CLASSIFIER-WRAP-UNSUPPORTED)`
3. Exit code: `ExitCode.UsageError`
4. **No NDJSON frame produced** — the classifier only runs against successful wrap-set invocations
5. Adding `blame` requires a §97 extension AC + this file's §6 `MAJOR` bump (per §6 last sentence)

---

## Cross-link

- §97 AC-84 binds this file (governing AC for slot §42)
- §97 AC-80 Sibling File Delegation Map row 36 (`42-cli-classifier-rules.md` → AC-84)
- §40 §2 (closed wrap-set the classifier consumes)
- §40 §3 step 1 (identity-discovery failure → `INTERNAL` precedence rule 2)
- §43 (NDJSON frame `outcome` + `classifierVersion` fields consume this file)
- §44 (auto-fix protocol consumes `ERROR` outcomes from this file)
- spec/13 §97 AC-21 (typed `ExitCode` enum — link-don't-restate)
- spec/22 §15 (`GL-CLASSIFIER-*` error codes — owning surface)

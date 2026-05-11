# 01 — check-spec-cross-links.py

**Version:** 1.1.0  
**Updated:** 2026-04-28  
<!-- h10-verified-phase: 35 -->
**Source:** [`linter-scripts/check-spec-cross-links.py`](../../linter-scripts/check-spec-cross-links.py)  
**Category:** Validator (read-only, with opt-in `--rewrite-allowlist` mutator)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Verify every internal markdown link inside `spec/` resolves to an existing file, and when an anchor is present, to an existing heading inside that target file. This is the primary defence against broken cross-references after a file rename or split.

## Usage

```bash
python3 linter-scripts/check-spec-cross-links.py
python3 linter-scripts/check-spec-cross-links.py --root spec
python3 linter-scripts/check-spec-cross-links.py --json
python3 linter-scripts/check-spec-cross-links.py --rewrite-allowlist
python3 linter-scripts/check-spec-cross-links.py --strict-line-match
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--root <dir>` | `spec` | Tree to scan |
| `--repo-root <dir>` | `.` | Repo root used to resolve absolute links |
| `--json` | off | Machine-readable failure report on stdout (now also includes `fuzzy_hits`, `fuzzy_count`, `rewritten`) |
| `--github` | off | Emit GitHub Actions `::error::` annotations |
| `--strict-line-match` | off | Require waiver line numbers to match exactly (disables P35 fuzzy match) |
| `--rewrite-allowlist` | off | Auto-bump stale waiver line numbers in-place when fuzzy match resolves them (P35) |

## Inputs

- Every `*.md` file under `--root`.
- [`linter-scripts/spec-cross-links.allowlist`](../../linter-scripts/spec-cross-links.allowlist) — broken-link exceptions (see §61).

## Outputs

Human report on stdout; JSON on stdout when `--json`. Fuzzy-match hints + optional `REWROTE N` line on stdout when waivers drift.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All links resolve (fuzzy-matched waivers do NOT fail the gate) |
| 1 | One or more broken links / missing target sections |
| 2 | Invocation error (bad `--root`, etc.) |

## Why fuzzy waiver matching (P35)

**Problem (P34 root-cause).** The allowlist key format `relpath:line:target` ties each waiver to an exact line number. When an unrelated edit (most commonly a P22/P32-style stamp-batch tool that inserts a `<!-- h10-verified-phase: NN -->` comment line into the §00 banner *above* a waived link) shifts every line below by `+N`, the waiver no longer matches and the cross-link gate goes silently red. P34 caught two such waivers (lines 64→65 and 96→97) that had been broken since Phase P22 and survived 12 phases without anyone noticing.

**Resolution.** A waiver whose `(file, target)` pair still appears as a broken link in the same file at a nearby line (default tolerance: ±5 lines) is **fuzzily matched and accepted**. The drift is reported as an `INFO` line on stdout. Re-run with `--rewrite-allowlist` to auto-bump the stale waiver to the current line number — idempotent on a clean tree.

**Strict mode opt-in.** `--strict-line-match` disables fuzzy matching for contributors who want exact-line enforcement (e.g. when intentionally promoting a waiver to a different occurrence of the same target in the same file).

**Tolerance.** ±5 lines covers single-comment insertions, frontmatter additions, and small banner edits while staying narrow enough that a genuinely-different occurrence of the same target on the other side of the file isn't silently absorbed.

## Acceptance criteria

### AC-01-01 — Broken file link is detected
- **Given** a markdown file in `spec/` containing a link of the form `[x]` followed by `(./missing.md)`,
- **When** the script runs,
- **Then** it MUST exit `1` and report the file path + line + target.

### AC-01-02 — Broken anchor is detected
- **Given** a link of the form `[x]` followed by `(./real.md#non-existent-heading)`,
- **When** the script runs and `real.md` exists but has no matching heading,
- **Then** it MUST exit `1` and categorise the failure as `missing-section`.

### AC-01-03 — Allowlist suppresses known exceptions
- **Given** an entry in `spec-cross-links.allowlist`,
- **When** the script encounters that exact link,
- **Then** the link MUST NOT be reported as broken.

### AC-01-04 — `--json` mode emits parseable JSON
- **Given** `--json`,
- **When** failures exist,
- **Then** stdout MUST be a single JSON document with one object per failure containing `file`, `line`, `target`, `category`, plus top-level `fuzzy_hits`, `fuzzy_count`, `rewritten` keys for P35 introspection.

### AC-01-05 — Fuzzy-match drift tolerance (P35)
- **Given** a waiver `relpath:N:target` and a broken link in the same file at line `N±k` for `0 < k ≤ 5` referencing the **same target**,
- **When** the script runs WITHOUT `--strict-line-match`,
- **Then** the link MUST NOT be reported as broken; an `INFO` line MUST be printed naming the drift; exit code MUST be `0` if no other failures.
- **Verifies:** [`linter-scripts/test/test-check-spec-cross-links.sh`](../../linter-scripts/test/test-check-spec-cross-links.sh) — fuzzy-match assertions.

### AC-01-06 — `--rewrite-allowlist` is idempotent (P35)
- **Given** stale waiver line numbers detected by AC-01-05,
- **When** the script runs with `--rewrite-allowlist`,
- **Then** the allowlist file MUST be rewritten in-place (only stale waiver lines mutated; comments + blank lines preserved verbatim); the next invocation MUST report `fuzzy_count: 0`.
- **Verifies:** [`linter-scripts/test/test-check-spec-cross-links.sh`](../../linter-scripts/test/test-check-spec-cross-links.sh) — rewrite + idempotence assertions.

### AC-01-07 — `--strict-line-match` restores exact-line semantics (P35)
- **Given** a waiver whose line drifted by ≥ 1 from the actual link location,
- **When** the script runs WITH `--strict-line-match`,
- **Then** fuzzy matching MUST be disabled and the link MUST be reported as broken (exit `1`).
- **Verifies:** [`linter-scripts/test/test-check-spec-cross-links.sh`](../../linter-scripts/test/test-check-spec-cross-links.sh) — strict-mode assertion.

## Cross-references

- §12 [`12-suggest-spec-cross-link-fixes.md`](./12-suggest-spec-cross-link-fixes.md) — companion fixer.
- §61 [`61-spec-cross-links-allowlist.md`](./61-spec-cross-links-allowlist.md) — allowlist format.
- §70 [`70-spec-health-yml.md`](./70-spec-health-yml.md) — CI wiring.

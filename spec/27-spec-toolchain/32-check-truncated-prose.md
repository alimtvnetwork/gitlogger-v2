# 32 — check-truncated-prose.py

**Version:** 1.0.0  
**Updated:** 2026-04-29  
**Source:** [`linter-scripts/check-truncated-prose.py`](../../linter-scripts/check-truncated-prose.py)  
**Self-test:** [`linter-scripts/test/test-check-truncated-prose.sh`](../../linter-scripts/test/test-check-truncated-prose.sh)  
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Slot-range note

Slot **32** sits in the 30-39 auditor band, but `check-truncated-prose.py` is a deterministic read-only validator (not AI-driven). Validator slots 01-09, 17-19, and 24-29 are full as of Phase P47-followup-1; renaming would break P107/H1 retros and the Phase 31 lockstep. This placement follows the precedent codified for slots 18/19 (validators in the 10-19 generator band). Future contributors MUST NOT "correct" the band.

---

## Purpose

Mechanically catches the **truncation class** of AI-implementability blockers surfaced in the Phase P47 audit (`/mnt/documents/audit-phase-p47.md`). Files that end mid-sentence or with an unclosed `` ``` `` fence are unimplementable from the spec alone — a mediocre AI cannot infer the missing tail.

The first run on the live tree (Phase P47-followup-1) found one real defect: `spec/17-consolidated-guidelines/14-app-issues.md` had an unbalanced fence at template end (fixed, file bumped to v3.3.1).

---

## Inputs

- `spec/**/*.md` (skips `_archive/`).

## Usage

```bash
python3 linter-scripts/check-truncated-prose.py
python3 linter-scripts/check-truncated-prose.py --verbose
python3 linter-scripts/check-truncated-prose.py --root /custom/spec/path
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--root PATH` | `spec/` | Override scan root (used by self-test fixtures) |
| `--verbose` | off | Emit per-file OK/FAIL classification |

## Detection rules (a file FAILS if)

1. The number of ` ``` ` fences in the file is **odd** (unclosed fenced block).
2. The last non-blank, non-HTML-comment, non-structural line does **not** end with a sentence terminator: `. ! ? : ; ) ] } > " ` * _`.

A line is "structural" (always considered a clean ending) when it is a heading, horizontal rule, list item, table row, blockquote, closing fence, or link-only line.

## Outputs

- stdout: `check-truncated-prose: OK (N files clean)` on success.
- stderr: per-file `FAIL <relpath>  -- <reason>` on failure.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All files clean |
| 1 | At least one truncated file detected |
| 2 | Usage error (e.g., `--root` does not exist) |

## Acceptance criteria

### AC-32-01 — Unclosed fence detected
- **Given** a markdown file with an odd number of ` ``` ` fences,
- **When** the validator runs,
- **Then** exit code MUST be 1 and stderr MUST mention "unclosed code fence".

### AC-32-02 — Mid-sentence ending detected
- **Given** a markdown file whose last meaningful line ends without a terminator,
- **When** the validator runs,
- **Then** exit code MUST be 1 and stderr MUST mention "mid-sentence".

### AC-32-03 — Structural endings pass
- **Given** a markdown file ending with a table row, list item, heading, or horizontal rule,
- **When** the validator runs,
- **Then** exit code MUST be 0 and the file MUST be classified `structural-ending`.

### AC-32-04 — Live spec tree clean
- **Given** the current `spec/` tree,
- **When** the validator runs with no flags,
- **Then** exit code MUST be 0. Any new violation MUST be fixed in the same PR that introduces it.

### AC-32-05 — Self-test parity
- **Given** the self-test `test-check-truncated-prose.sh`,
- **When** it runs,
- **Then** all 5 assertions MUST pass, including the live-tree gate (proves Phase P47-followup-1 fix landed).

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — AI audit that originally surfaced truncation as a recurring blocker class.
- Phase P47 audit report (artifact `/mnt/documents/audit-phase-p47.md`).

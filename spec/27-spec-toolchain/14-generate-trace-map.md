# 14 — generate-trace-map.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/generate-trace-map.py`](../../linter-scripts/generate-trace-map.py)  
**Category:** Generator (writes `spec/27-spec-toolchain/trace-map.md` + `.lovable/memory/audit/trace-map.json`)

---

## Purpose

Produce a bidirectional **Spec ↔ Code trace map** so spec drift and orphan code become visible at a glance:

- **AC → Code** — every traced acceptance criterion and the file/symbol/endpoint that satisfies it.
- **Code → AC** — reverse index so any file can be traced back to the spec it backs.
- **Drift** — ACs that have NO code link → spec promises something the code does not deliver.
- **Orphan** — code files that NO AC references → behaviour exists with no spec coverage.

The single source of truth is [`linter-scripts/trace-map.toml`](../../linter-scripts/trace-map.toml). Each `[[trace]]` entry links one canonical AC id (`<spec-relpath>#<ac-id>`) to one or more code targets (file + optional symbol + optional kind).

## Usage

```bash
python3 linter-scripts/generate-trace-map.py
```

## CLI flags

_(none — reads `trace-map.toml`, writes both reports unconditionally)_

## Inputs

- All `### AC-...` headings under `spec/`.
- [`linter-scripts/trace-map.toml`](../../linter-scripts/trace-map.toml) — hand-curated AC → code links.
- All executable artefacts under `linter-scripts/` and `.github/workflows/` (extensions: `.py .cjs .js .sh .ps1 .go .toml .mjs .allowlist .yml .yaml`).

## Outputs

| Path | Purpose |
|------|---------|
| `spec/27-spec-toolchain/trace-map.md` | Human-readable bidirectional report |
| `.lovable/memory/audit/trace-map.json` | Machine-readable, sorted, byte-stable |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Trace map healthy (no missing-file, no missing-ac) |
| 1 | At least one trace entry points to a missing file or unknown AC |
| 2 | Invocation error (cannot parse `trace-map.toml`) |

## TOML schema

```toml
[[trace]]
ac     = "27-spec-toolchain/31-audit-spec-vs-code-v2.md#AC-31-06"   # canonical AC id (REQUIRED)
files  = ["linter-scripts/audit-spec-vs-code-v2.py"]                 # ≥1 repo-relative path (REQUIRED)
symbol = "deterministic_score"                                       # function/class/route name (optional)
kind   = "function"                                                  # function|endpoint|config|workflow|cli-flag|env-var
note   = "Pure-function rubric → byte-identical raw-results.json"    # optional rationale
```

## Acceptance criteria

### AC-14-01 — Bidirectional report contains both AC→Code and Code→AC sections
- **Given** a successful run,
- **When** `spec/27-spec-toolchain/trace-map.md` is read,
- **Then** it MUST contain a section titled `## AC → Code` AND a section titled `## Code → AC`.

### AC-14-02 — JSON output is sorted and stable
- **Given** an unchanged spec tree and unchanged `trace-map.toml`,
- **When** the script is run twice consecutively,
- **Then** `.lovable/memory/audit/trace-map.json` MUST have identical SHA-256 (sorted keys, deterministic ordering).

### AC-14-03 — Missing file in trace-map fails the run
- **Given** an entry whose `files = ["linter-scripts/does-not-exist.py"]`,
- **When** the script runs,
- **Then** it MUST exit `1` AND list the offending entry under `## ❌ Errors → Missing files`.

### AC-14-04 — Missing AC id in trace-map fails the run
- **Given** an entry whose `ac = "fake/path.md#AC-99-99"` does not appear in any spec heading,
- **When** the script runs,
- **Then** it MUST exit `1` AND list the offending id under `## ❌ Errors → Missing AC ids`.

### AC-14-05 — Drift list is exhaustive
- **Given** N total ACs scanned and M traced in TOML,
- **When** the script runs,
- **Then** the `drift` array in JSON MUST have exactly `N − M` entries (when no errors).

### AC-14-06 — Orphan list excludes documented files
- **Given** a code file referenced in at least one `[[trace]]` entry,
- **When** the script runs,
- **Then** that file MUST NOT appear in the `orphan` array.

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — auditor whose `raw-results.json` complements this trace map.
- §97 [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) — module-level rules (`AC-T-01` bijection is enforced together with this map).

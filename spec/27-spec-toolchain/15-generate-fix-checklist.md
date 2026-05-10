# 15 — generate-fix-checklist.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/generate-fix-checklist.py`](../../linter-scripts/generate-fix-checklist.py)  
**Category:** Generator (consumes deterministic audit results)

---

## Purpose

Translate the deterministic audit's findings into a concrete, file-targeted fix checklist for **every module**. Each action item names:

- **Priority** (`P0` blocker → `P3` polish)
- **Exact target file** (e.g. `spec/22-git-logs-v2/00-overview.md`)
- **Verb-led action** (e.g. *"Inline a ```sql fenced block"*)
- **Acceptance test** in Given/When/Then form so the fix can be objectively verified
- **Effort estimate** in minutes

The script is rules-based and uses no AI — every input produces a stable output (byte-identical JSON across runs).

## Usage

```bash
# 1. Refresh the deterministic audit
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py

# 2. Generate per-module + master checklists
python3 linter-scripts/generate-fix-checklist.py
```

## CLI flags

_(none — reads `raw-results.json`, writes the checklists unconditionally)_

## Inputs

- `.lovable/memory/audit/v2-deterministic/raw-results.json` — produced by §31 in deterministic mode.

## Outputs

| Path | Purpose |
|------|---------|
| `.lovable/memory/audit/v2-deterministic/fix-checklists/<module-slug>.md` | Per-module checklist with detail + acceptance test for each action |
| `.lovable/memory/audit/v2-deterministic/fix-checklists/00-master-checklist.md` | Master roll-up sorted by lowest implementability first |
| `.lovable/memory/audit/v2-deterministic/fix-checklists/raw-checklist.json` | Machine-readable, sorted, byte-stable |

## Action-derivation rules

| Trigger metric | Priority | Target file | Action template |
|----------------|:--------:|-------------|-----------------|
| `has_sql_ddl == false && has_json_schema == false && has_ts_enums == false && has_yaml_openapi == false` | **P0** | `00-overview.md` | Inline a fenced contract block (language hint inferred from module path: database→sql, schema→json, api→yaml, enum/error→ts, workflow→yaml) |
| `ac_count == 0` | **P0** | `97-acceptance-criteria.md` | Run `generate-gwt-acceptance.py`, then hand-edit each AC into a Given/When/Then triplet |
| `gwt_block_count < ac_count` | **P1** | `97-acceptance-criteria.md` | Rewrite the `(ac_count − gwt_block_count)` ACs into Given/When/Then form |
| `links_broken > 0` | **P1** | `spec/<module>/` | Run `check-spec-cross-links.py` then fix or allowlist each |
| `waffle_per_kchar > 3` | **P2** | `spec/<module>/*.md` | Replace should/may/might/optionally per RFC 2119 |
| `consistency_report == false` | **P2** | `99-consistency-report.md` | Run `fill-missing-consistency-reports.cjs`, then hand-edit |
| `todo_density > 0` | **P3** | `spec/<module>/*.md` | Resolve every TODO/TBD/FIXME marker |
| _(any of the above triggered)_ | **P3** | `98-changelog.md` | Bump version + add a row dated `TODAY` |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Checklist written |
| 1 | `raw-results.json` not found — run the deterministic auditor first |
| 2 | Invocation error |

## Acceptance criteria

### AC-15-01 — Master checklist sorts by lowest implementability first
- **Given** a successful run,
- **When** `00-master-checklist.md` is read,
- **Then** the per-module table MUST be sorted ascending by `implementability` (lowest urgency at top).

### AC-15-02 — Every action carries an acceptance test
- **Given** any module checklist,
- **When** parsed,
- **Then** every entry in the "Actions" table MUST have a corresponding "Acceptance test" line in the detail section, AND the acceptance test MUST contain the literal substring `Given` and `Then`.

### AC-15-03 — Missing-contract trigger fires on bare-prose modules
- **Given** a module whose deterministic metrics report `has_sql_ddl=false`, `has_json_schema=false`, `has_ts_enums=false`, `has_yaml_openapi=false`,
- **When** the checklist is generated,
- **Then** that module MUST receive at least one `P0 missing-contract` action targeting `00-overview.md`.

### AC-15-04 — JSON output is byte-stable across runs
- **Given** an unchanged `raw-results.json`,
- **When** the script is run twice consecutively,
- **Then** `raw-checklist.json` MUST have identical SHA-256 (sorted keys, sorted module list).

### AC-15-05 — Effort total matches per-action sum
- **Given** the master checklist,
- **When** all per-module `effort_min` values are summed,
- **Then** the total MUST match the "Estimated total effort" stated in the header.

### AC-15-06 — Missing audit JSON exits 1
- **Given** `.lovable/memory/audit/v2-deterministic/raw-results.json` does not exist,
- **When** the script is run,
- **Then** it MUST exit `1` and print a hint pointing at the auditor command.

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — produces the input JSON.
- §13 [`13-generate-gwt-acceptance.md`](./13-generate-gwt-acceptance.md) — referenced in `P0` AC-scaffolding actions.
- §22 [`22-fill-missing-consistency-reports.md`](./22-fill-missing-consistency-reports.md) — referenced in `P2` consistency-report actions.
- §14 [`14-generate-trace-map.md`](./14-generate-trace-map.md) — sibling generator (trace map vs fix-list).

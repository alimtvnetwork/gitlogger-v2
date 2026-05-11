# 13 — generate-gwt-acceptance.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/generate-gwt-acceptance.py`](../../linter-scripts/generate-gwt-acceptance.py)  
**Category:** Generator (AI-driven)


**Test pair:** N/A — generator  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Generate module-specific Given/When/Then acceptance criteria for low-implementability ("F-tier") spec modules identified by §31 audit. For each module: read overview + body files + sub-overviews → send digest to Gemini with strict GWT schema → write 5–12 module-specific ACs (with inlined contracts: DDL, enums, error codes) to `spec/<module>/97-acceptance-criteria.md` → append `98-changelog.md` entry.

## Inputs

- `/mnt/documents/spec-ai-audit.json` — output of §31 v2 audit.
- `LOVABLE_API_KEY` env var — Lovable AI Gateway credential.
- Every body file under each target module.

## Usage

```bash
python3 linter-scripts/generate-gwt-acceptance.py
```

## CLI flags

_(none — module selection is driven by audit JSON)_

## Outputs

- Overwrites `spec/<module>/97-acceptance-criteria.md` for each F-tier module.
- Appends an entry to `spec/<module>/98-changelog.md` with version bump.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Every selected module regenerated |
| 1 | At least one module failed (AI call error, write error) |
| 2 | `LOVABLE_API_KEY` missing or `spec-ai-audit.json` not found |

## Acceptance criteria

### AC-13-01 — Module selection is driven by audit grade
- **Given** the audit JSON marks 31 modules grade=F,
- **When** the script runs,
- **Then** it MUST regenerate exactly those 31 (minus the `EXCLUDE` set: pure-diagram modules).

### AC-13-02 — Generated AC contains inlined contracts
- **Given** a database-related module,
- **When** the AC is regenerated,
- **Then** the output MUST include at least one `\`\`\`sql` block when the module references DDL.

### AC-13-03 — Changelog version is bumped
- **Given** a successful regeneration,
- **When** `98-changelog.md` is read,
- **Then** the new entry MUST bump at least the MINOR version.

## Cross-references

- §31 [`31-audit-spec-vs-code-v2.md`](./31-audit-spec-vs-code-v2.md) — produces the input JSON.

---
kind: future-spec
drift_acknowledged: 2026-04-27
---

# Lint Rule Catalog (canonical)

**Version:** 1.0.0
**Updated:** 2026-04-27
**AI Confidence:** Production-Ready
**Ambiguity:** None
**Scope:** Cross-folder canonical source of truth for `<DOMAIN>-<NAME>-NNN` lint rule IDs cited by `linter-waive:` SQL comments and prose references.

---

## Keywords

`lint-rules` · `rule-catalog` · `linter-waive` · `sql-linter` · `migration-linter` · `cross-folder-source-of-truth`

---

## 1. Purpose

Closes the gap surfaced by **Phase 126 — AC-SAG-27 enumeration sweep of folder §17**:

> Lint rule IDs (`MISSING-DESC-001`, `DB-FREETEXT-001`, `WAIVER-MALFORMED-001`,
> `MIG-*-001`) are cited from at least **17 spec files** across §02, §04, §05, §06,
> and §17, plus dozens of `linter-waive:` SQL comments — yet **no canonical catalog
> exists**. A rename of any rule ID would silently invalidate every waiver across
> the spec tree.

This file is that catalog. The **Containment harness for Candidate O** (Phase 117)
asserts every cited rule ID resolves to a row here.

`linter-scripts/forbidden-strings.toml` is the SoT for **rename guards**, not for
lint rule IDs. The two registries are deliberately separate.

---

## 2. Rule Categories

Three rule families are catalogued. Each ID follows the pattern
`<DOMAIN>-<NAME>-<NNN>` where `NNN` is a zero-padded 3-digit sequence within
the family.

| Family | Domain prefix | Owner script (planned) | Sites |
|---|---|---|---|
| Free-text column rules | `DB-FREETEXT`, `MISSING-DESC` | `linter-scripts/sql-linter/` | 30+ schema examples + prose |
| Waiver-syntax rules | `WAIVER-MALFORMED` | `linter-scripts/_lib/sql_waivers.py` | All `linter-waive:` comments |
| Migration-file rules | `MIG-NAMING`, `MIG-HEADERS`, `MIG-TARGET`, `MIG-NULLABLE` | `linter-scripts/sql-linter/migrations.py` | §04 §6.5 + §17/18 §20 |

Note: `CODE-RED-NN` markers in `spec/17-consolidated-guidelines/02-coding-guidelines.md`
are a **separate namespace** (coding-guidelines anti-pattern markers), not lint rule
IDs. They are out of scope for this catalog and SHOULD be catalogued separately if
formalised.

---

## 3. Canonical Rule Table

| Rule ID | Family | Severity | What it checks | Canonical definition site |
|---|---|---|---|---|
| `DB-FREETEXT-001` | Free-text column | Block | Every entity / reference / transactional table declares the required free-text columns (`Description` for entities/refs; `Notes` + `Comments` for transactional). Join/bridge tables exempt. | `spec/04-database-conventions/02-schema-design.md` §6.4 + `spec/17-consolidated-guidelines/18-database-conventions.md` §19.1 |
| `MISSING-DESC-001` | Free-text column | Block | Free-text columns conform to Rule 12: `TEXT NULL`, no `NOT NULL`, no `DEFAULT`. Also validates `linter-waive:` syntax on the rule line. | `spec/04-database-conventions/02-schema-design.md` §6.4 + `spec/17-consolidated-guidelines/18-database-conventions.md` §19.1 |
| `WAIVER-MALFORMED-001` | Waiver-syntax | Block | Every `linter-waive:` / `linter:waive` comment contains all four required fields: `@waiver`, `@reason`, `@approved-by`, `@date`. | `spec/17-consolidated-guidelines/18-database-conventions.md` §19.4 |
| `MIG-NAMING-001` | Migration file | Block | Migration file name matches `<timestamp>_<verb>_<scope>.sql`. | `spec/17-consolidated-guidelines/18-database-conventions.md` §20.6 |
| `MIG-HEADERS-001` | Migration file | Block | `@migration`, `@up`, and (`@down` OR `@irreversible`) headers all present. | `spec/17-consolidated-guidelines/18-database-conventions.md` §20.6 |
| `MIG-TARGET-001` | Migration file | Block | `@target` declared and is one of `root` / `app` / `session`. | `spec/17-consolidated-guidelines/18-database-conventions.md` §20.6 |
| `MIG-NULLABLE-001` | Migration file | Block | New columns added by a migration are nullable (aligns with Rule 12). Same waiver syntax as §19.3. | `spec/17-consolidated-guidelines/18-database-conventions.md` §20.6 |

**Total: 7 active rules.** No deprecated rules at v1.0.0.

---

## 4. Citation Conventions

A rule ID may be cited in two shapes; both are recognised by the Phase 117
containment harness.

### 4.1 SQL waiver comment (in-schema)

```sql
-- linter-waive: MISSING-DESC-001 reason="Consolidated DB-conventions example; canonical version in 04-database-conventions/02-schema-design.md §6.4"
CREATE TABLE Example ( ... );
```

The literal token `linter-waive:` (or `linter:waive`) MUST be followed by exactly
one rule ID from §3.

### 4.2 Prose reference (in narrative markdown)

Bare backticked rule IDs anywhere in spec prose:

```
…enforced by `DB-FREETEXT-001` and `MISSING-DESC-001`.
```

The harness resolves every match of the regex
`\b(MISSING|DB|MIG|WAIVER)-[A-Z]+(?:-[A-Z]+)?-[0-9]{3}\b` to §3.

---

## 5. Add-or-modify Workflow

Adding or renaming a rule is a multi-file lockstep change.

1. Add the row to §3 above.
2. Bump `06-lint-rule-catalog.md` banner version (semver: NEW rule = minor; RENAME = major).
3. Append a row to `spec/03-error-manage/03-error-code-registry/98-changelog.md`.
4. Update §99 health row in `spec/03-error-manage/03-error-code-registry/99-consistency-report.md`.
5. Update enforcement script under `linter-scripts/sql-linter/` (or its planned location).
6. Update every cite site (use `rg` to find them).
7. Re-run `bash linter-scripts/run.sh` — must exit 0.

A rename without step 6 is the exact silent-drift failure mode this catalog prevents.

---

## 6. Enforcement Status

As of v1.0.0, the rules in §3 are **documented and waivered against** but the
enforcement scripts under `linter-scripts/sql-linter/` are NOT yet present. This is
acknowledged drift — see top-of-file `kind: future-spec` banner.

Phase 117's containment harness operates at the **catalog layer** (it asserts that
every cited ID resolves to §3) regardless of enforcement script presence. It is the
right gate to land first; the per-rule enforcement scripts can land independently.

---

## 7. Cross-References

- [Module overview](./00-overview.md) — sibling Error Code Registry conventions
- [Error code master JSON](./error-codes-master.json) — sibling registry for runtime error codes (different namespace)
- `spec/04-database-conventions/02-schema-design.md` §6.4 — free-text column rules (Rules 10/11/12)
- `spec/17-consolidated-guidelines/18-database-conventions.md` §19–§20 — consolidated narrative
- `linter-scripts/forbidden-strings.toml` — rename-guard registry (separate concern)
- `.lovable/memory/audit/v2-deterministic/phase-126-folder-17-enumeration-sweep.md` — origin of Candidate O
- `.lovable/memory/audit/v2-deterministic/phase-127-folders-27-18-25-final-sweep.md` — discovery campaign closure

---

*Lint Rule Catalog — v1.0.0 — 2026-04-27 — Phase 128*

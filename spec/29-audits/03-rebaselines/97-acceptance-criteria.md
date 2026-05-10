# Acceptance Criteria — 03-rebaselines (Delegated to Parent)

**Version:** 1.0.0
**Status:** Active

---

## Module Kind

This submodule is `kind: tracker` (audit-corpus, inherited from parent `spec/29-audits/`). All normative governance is provided by the parent `spec/29-audits/97-acceptance-criteria.md` AC-29-01 through AC-29-03.

## Delegated Governance

| AC ID | Severity | Source | Applies to this submodule via |
|-------|----------|--------|-------------------------------|
| AC-29-01 | critical | `../97-acceptance-criteria.md` | Module-kind classification (tracker) inherited by all children |
| AC-29-02 | critical | `../97-acceptance-criteria.md` | Auditor-quoted-evidence rule applies to baseline scores cited in `00-overview.md` |
| AC-29-03 | high | `../97-acceptance-criteria.md` | Inventory-disambiguation rule applies to the snapshot-directory table |

Per Lesson #36 (link, never restate), this file does NOT restate the parent ACs. The parent §97 is the single source of truth.

## No Local ACs

This submodule is a **delegated index** of immutable historical baselines — it carries no local normative surface. Modifying snapshot directories under `.lovable/memory/audit/v2*/` is FORBIDDEN per `mem://specs/full-tree-audit-v4` reference contract; new rebaseline events land as new entries in the live auditor output, not as edits to existing snapshots.

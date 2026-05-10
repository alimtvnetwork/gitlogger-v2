# Changelog — Top-Level Research Index

**Version:** 2.1.0
**Updated:** 2026-04-30 (Phase 153 Task A13 — AC-RESEARCH-05 Verifies clause + AC-RESEARCH-07 domain-registry validator)


## 2026-04-30 — 2.1.0 (Phase 153 Task A13)

- **AC-RESEARCH-05 (Forward-only updates):** Added `**Verifies:**` clause citing the SemVer minor-bump invariant + `check-version-parity.py` enforcement; replaced "reviewed in PR" with concrete diff-derived contract (DEPRECATED-prefix marker for removed properties; alias-pair retention for renames). Closes v6 audit D2 LOW finding "Vague Verification Clauses".
- **AC-RESEARCH-07 (NEW — domain-registry validator):** Binds the existing `domains[]` schema constraint (currently only `type:string + minItems:2`) to a concrete regex `^(?:spec/)?\d{2}-[a-z][a-z0-9-]*(?:/\d{2}-[a-z][a-z0-9-]*)*/?$` AND on-disk resolution against the `spec/` tree (master module list = on-disk inventory per Lesson #36 link-don't-restate; `spec/_archive/` paths INVALID for new entries). Closes v6 audit D3 MEDIUM finding "Undefined Domain Registry".
- AC count 6 → 7. §97 v2.0.0 → v2.1.0 (new content). No schema diff in §00 — AC-RESEARCH-07 enforces existing schema field at validator level.


## 2026-04-27 — 2.0.0 (Phase 69b)

- Promoted from index-stub (Phase 69) to content module.
- Added inlined contract block (JSON Schema / TypeScript interface / SQL DDL as appropriate).
- Added Mermaid lifecycle diagram as standalone `*.mmd` file AND inlined in `00-overview.md`.
- Expanded acceptance criteria from 2 to 6, all in GWT format with severity tags.
- Removed `kind: index` frontmatter — module now carries normative content.

## 2026-04-27 — 1.0.0 (Phase 69)

- Initial creation as index-stub child to lift parent from impl=70 to impl=80.

## 2026-04-27 — Phase 73 (impl 80 → 85)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


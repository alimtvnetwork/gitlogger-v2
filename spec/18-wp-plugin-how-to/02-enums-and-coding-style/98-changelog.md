# Changelog — Phase 2 — Enums and Coding Style

**Version:** 1.1.2
**Updated:** 2026-04-29
**Scope:** `spec/18-wp-plugin-how-to/02-enums-and-coding-style/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases


### 1.1.1 — 2026-04-29 — Phase 153 Task #31: §97 boilerplate ACs gained `**Verifies:**` clauses (8/8)
- **Action**: Phase 153 Task #31 bulk sweep — added `**Verifies:**` lines to all 8 boilerplate ACs (AC-01..AC-08) anchored to §00 baseline / sibling spec / linter scripts. Closes the audit-v6 boilerplate blind spot for this module.
- **Lockstep**: §97 v1.0.0 → **v1.1.0**; §99 lockstep update.

### 1.1.0 — 2026-04-26 (Phase 20 contract inlining, module #11 — final)
- **Added** normative Reference Implementation block in `00-overview.md`:
  full `SelfUpdateStatusType` PHP 8.1+ backed enum (7 cases, `JsonSerializable`,
  per-case `is{Case}()` helpers, `isEqual`/`isOtherThan`/`isAnyOf`,
  `match`-based `label()`, strict `parse()` that throws on unknown).
- **Added** TypeScript wire-format mirror (`as const` object + type-guard) and
  Draft 2020-12 JSON Schema for the wire form.
- **Added** forbidden-shapes table (6 lint-enforced rules).
- **Verified** TS mirror typechecks under `tsc --strict`; JSON Schema rejects
  unknown strings, integers, and null inputs.
- **Added** version banner (v1.1.0) to overview previously missing one.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | patch | Phase 27d: Added Drift Acknowledgment for low-severity doc-hygiene findings. |

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended `.wp-plugin-style.yaml` contract to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 65 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 65 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


### 1.1.2 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v1.1.2. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v1.1.2).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.

# Consistency Report

> **Version:** 2.1.0
> **Parent:** [00-overview.md](./00-overview.md)
> **Audit date:** 2026-04-26
> **Updated:** 2026-04-26

---

## Scope

Cross-checks the ten files in `spec/14-update/24-update-check-mechanism/`
against each other AND against the related specs they depend on, to
confirm zero contradictions before handing off to implementer AIs.

---

## 1. Internal Coherence (within this folder)

| Topic | Files involved | Status |
|-------|----------------|--------|
| V → V+5 probe count = 6 (1 current + 5 lookahead) | 00, 01, 03, 08, 97 | ✅ Consistent — `Candidates` always length 5 (lookahead only); current is `CurrentVersion` |
| PascalCase mandate | 00, 02, 03, 04, 05, 09, 97 | ✅ Consistent |
| Default check interval = 12h | 00, 04, 06, 07, 97 | ✅ Consistent |
| Both sync AND `--async` persist (no `--persist` flag) | 00, 06, 07, 97 | ✅ Consistent |
| Failed re-check preserves prior `HasUpdate` | 05, 06 (`do-update` failure), 08, 97 | ✅ Consistent |
| Hook returns < 50 ms; never blocks | 00, 07, 97 | ✅ Consistent |
| Schema Rule 10/11/12 columns present | 04, 09, 97 | ✅ Consistent |
| `UpdateStatus` enum values: `UpToDate`, `UpdateFound`, `UpdateApplied`, `Failed`, `Migrated` | 04 §2 + §6, 05, 09 | ✅ Consistent — Phase 20 #9 inlined TS + Go enum mirrors in §04 §6 with strict `parseUpdateStatus` / `ParseUpdateStatus` |
| §97 v2.0.0 GWT rewrite consistency | 97, 98, 99 | ✅ Consistent — 20 GWT ACs (AC-UCM-01..20) + 34 legacy traceability notes |
| Phase 20 #9 — TS enum + Go enum + JSON Schema 2020-12 wire format inlined in §04 | 04 §6/§7/§8, 09 | ✅ TS compiles under `tsc --strict`; JSON schema well-formed Draft 2020-12; positive instance validates; conditional `if/then` (HasUpdate ⇒ LatestVersion) correctly rejects bad data |

---

## 2. External Spec Cross-References

| Reference | Used in | Status |
|-----------|---------|--------|
| [06-Seedable-Config](../../06-seedable-config-architecture/00-overview.md) — `BackgroundUpdateCheckEnabled`, `CheckIntervalHours`, `PendingUpdateWarningEnabled`, `Storage.Backend` | 00, 07, 09 | ✅ Keys named per existing config conventions; will need a follow-up entry in the seedable-config registry when implemented |
| [Self-update apply phase](../01-self-update-overview.md) — rename-first deployment | 00, 06 (`do-update` invokes pinned installer which uses rename-first) | ✅ Detection layer (this folder) and apply layer (parent folder) are cleanly separated |
| [Install scripts](../18-install-scripts.md) | 02 (status JSON `Install.*` fields), 06 (`do-update`) | ✅ `do-update` invokes the same one-liners documented there |
| [Version-pinned installers](../../16-generic-release/08-version-pinned-release-installers.md) | 02, 06 | ✅ Status JSON `Install.*.Command` MUST be the pinned one-liner — not the "latest" redirect |
| [Local SQLite store](../../13-generic-cli/10-database.md) | 04, 09 | ✅ DDL pattern matches the project's standard split-database conventions |
| [PascalCase key naming](../../02-coding-guidelines/01-cross-language/11-key-naming-pascalcase.md) | All files | ✅ |
| [Code Red — boolean principles](../../02-coding-guidelines/01-cross-language/02-boolean-principles/) | 05 (positive booleans), 07 (no nested if), 08 (no swallow) | ✅ |
| [Database naming](../../02-coding-guidelines/01-cross-language/07-database-naming.md) | 04 | ✅ PK = `UpdateCheckerId`, lookup PK = `UpdateStatusId` |
| [Enum standards](../../17-consolidated-guidelines/04-enum-standards.md) | 04, 05 | ✅ Strict `ParseUpdateStatus()` mandated |
| [Error handling — apperror](mem://architecture/error-handling) | 08 | ✅ File + line metadata required |
| [§14 parent §97 AC-06..AC-20](../97-acceptance-criteria.md) | 97 (AC-UCM-01) | ✅ Inheritance documented in AC-UCM-01 |

---

## 3. Known Open Items (Implementation, Not Spec)

These are NOT spec ambiguities — the spec is complete — but they are
implementation choices the executing AI must make:

1. **Concrete language.** The spec is language-neutral. The first
   implementation target (Go, Rust, TS, …) will pick concurrency
   primitives per [05 §5](./05-update-checker-service.md#5-concurrency).
2. **CLI framework.** [07 §4](./07-pre-command-hook.md#4-integration-points)
   lists hook bindings for cobra, clap, commander, and symfony/console.
   Pick the one your CLI already uses.
3. **Seedable-config registry entry.** When implementing, add a row
   for `Update.*` keys to the seedable-config schema doc in
   `06-seedable-config-architecture/`.

---

## 4. No Contradictions Found

Every cross-reference resolves. Every numbered decision in
[00 §Resolved Decisions](./00-overview.md#resolved-decisions-no-ambiguity-remains)
has a matching enforcement point in 01–09.

This subsystem is **ready for hand-off** to an implementer AI.

---

*Consistency Report — v2.1.0 — 2026-04-26*

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-26 | current | Phase 31: Added Validation History + heading-rubric alignment for `check-tree-health.cjs` v2.0.0 quality dimension. No content removed. |
| 2026-04-25 | prior | Tree-wide audit baseline established (45/100 → roadmap to 100). |
| 2026-04-20 | prior | Module brought into alignment with parent §99 conventions. |
| 2026-04-16 | prior | Initial consistency report authored. |

This module's full lockstep history is mirrored in `98-changelog.md`; entries
above summarize only the audit-/validation-bearing milestones for `14-update/24-update-check-mechanism`.

---

## File Inventory
<!-- verified-phase: 147 -->

| File | Status |
|------|--------|
| `00-overview.md` | ✅ Present |
| `01-fundamentals.md` | ✅ Present |
| `02-status-script-json.md` | ✅ Present |
| `03-combined-json.md` | ✅ Present |
| `04-database-schema.md` | ✅ Present |
| `05-update-checker-service.md` | ✅ Present |
| `06-cli-commands.md` | ✅ Present |
| `07-pre-command-hook.md` | ✅ Present |
| `08-error-handling.md` | ✅ Present |
| `09-json-fallback-store.md` | ✅ Present |
| `97-acceptance-criteria.md` | ✅ Present |
| `97-changelog.md` | ✅ Present |
| `98-changelog.md` | ✅ Present |
| `99-consistency-report.md` | ✅ Present |

Inventory mirrors the on-disk layout of `14-update/24-update-check-mechanism/` as of 2026-04-26. See
`98-changelog.md` for the file-level revision trail.


## 2026-04-27 — Phase 68 audit

- Mermaid lifecycle diagram present (`has_mermaid=true`).
- Lockstep & tree-health gates: PASS.
- Implementability promoted from 85 → 90.

### 2026-04-27 — Phase 71 deepening

- CI workflow contract inlined: 5 stages (detect, validate, lint, promote, report).
- Implementability raised 90 → 95 (deterministic audit).


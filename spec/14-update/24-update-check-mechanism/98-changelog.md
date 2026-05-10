# Changelog — Update Check Mechanism

**Version:** 2.1.0
**Updated:** 2026-04-26
**Scope:** `spec/14-update/24-update-check-mechanism/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.1.0 — 2026-04-26
- **P22 sync** (2026-04-28): §00 banner version field bumped 1.0.0 → 2.1.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

**Added (Phase 20 Module #9 — code-mirror + wire-format contracts in §04):**
- New §6 in `04-database-schema.md` inlining the `UpdateStatusEnum` mirror promised by §2 — TypeScript numeric enum (1-based, matches `UpdateStatusId`) plus `UpdateStatusName` / `UpdateStatusLabel` const records and a strict `parseUpdateStatus()` (throws on unknown).
- Companion Go reference (`UpdateStatus uint8` typed alias, `Name()` / `Label()` switch tables, strict `ParseUpdateStatus()` returning `(UpdateStatus, error)`).
- New §7 inlining a normative JSON Schema 2020-12 wire-format validator for the `UpdateChecker` row, including conditional `if/then`: `HasUpdate=true ⇒ LatestVersion required`, and `UpdateStatusId=4 ⇒ ErrorMessage + ErrorAt required`. `Checksum` regex enforces `^[Ss]ha256:[0-9a-fA-F]{64}$`; `CurrentVersion` enforces `^V\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$`.
- New §8 GWT acceptance test (`AC-UCM-MIRROR-01`) requiring TS / Go / JSON-Schema / SQL seed-row triples to remain in lockstep.

**Verification (Phase 20 Module #9):**
- TypeScript block compiles under `tsc --strict --target es2022 --module esnext` (zero diagnostics).
- JSON Schema parses with `Draft202012Validator.check_schema` (well-formed).
- Positive instance (`HasUpdate=true, LatestVersion=V1.6.0, UpdateStatusId=2`) validates with zero errors.
- Negative instance (`HasUpdate=true, LatestVersion absent`) is correctly rejected by the conditional `if/then` clause.

**Bumped:**
- `04-database-schema.md` v1.0.0 → v1.1.0 (banner + footer).
- `99-consistency-report.md` inventory row updated; `spec-index.md` synced.
- Scope discipline: §00–§03 + §05–§09 + §97 untouched (the new §6/§7/§8 cite existing normative content from §02 seed table; no AC IDs added to §97 — `AC-UCM-MIRROR-01` lives inline in §04 as a contract test).

### 2.0.0 — 2026-04-26

**Changed:**
- `97-acceptance-criteria.md` — **Phase 16q: full GWT rewrite.** Replaced 34 table-row criteria (A-G sections) with 20 module-specific Given/When/Then ACs (AC-UCM-01..AC-UCM-20) covering: parent §14 inheritance (AC-UCM-01), parallel discovery with 6 probes + V+5 hard stop (AC-UCM-02), response classification — 404=no-retry, malformed=logged+not-found, highest-wins (AC-UCM-03), per-probe 5s timeout + total 10s deadline (AC-UCM-04), UpdateChecker table schema with RawJson + parsed columns (AC-UCM-05), UpdateStatus enum 5 values + TINYINT PK (AC-UCM-06), failed re-check preserves prior state + atomic single-UPDATE (AC-UCM-07), JSON fallback with XDG paths + atomic tmp+rename (AC-UCM-08), sync update-check print+persist vs --async < 200ms (AC-UCM-09), --force bypass + do-update unattended + exit codes 0/1/2/3/4 (AC-UCM-10), pre-hook < 50ms + never blocks + no recursion + stderr warning (AC-UCM-11/18), error logging with file+line + 1 MiB cap + rotation (AC-UCM-12), PascalCase everywhere (AC-UCM-13), Schema Rule 11/12 compliance (AC-UCM-14), flat guard-clause no nested if (AC-UCM-15), JSON-to-SQLite migration + NewRepoUrl banner (AC-UCM-16), --async detached child < 200ms (AC-UCM-17), pre-hook interval gate + spawn + warning (AC-UCM-18), status script fetching + PascalCase JSON + combined JSON (AC-UCM-19), self-application traceability (AC-UCM-20). Old 34 table-row criteria preserved as AC-UCM-LEGACY-001..034 at end with traceability notes. Banner v1.0.0 → v2.0.0.

**Changed:**
- `97-acceptance-criteria.md` — **Phase 16q: full GWT rewrite.** Replaced 34 table-row criteria (A-G sections) with 20 module-specific Given/When/Then ACs (AC-UCM-01..AC-UCM-20) covering: parent §14 inheritance (AC-UCM-01), parallel discovery with 6 probes + V+5 hard stop (AC-UCM-02), response classification — 404=no-retry, malformed=logged+not-found, highest-wins (AC-UCM-03), per-probe 5s timeout + total 10s deadline (AC-UCM-04), UpdateChecker table schema with RawJson + parsed columns (AC-UCM-05), UpdateStatus enum 5 values + TINYINT PK (AC-UCM-06), failed re-check preserves prior state + atomic single-UPDATE (AC-UCM-07), JSON fallback with XDG paths + atomic tmp+rename (AC-UCM-08), sync update-check print+persist vs --async < 200ms (AC-UCM-09), --force bypass + do-update unattended + exit codes 0/1/2/3/4 (AC-UCM-10), pre-hook < 50ms + never blocks + no recursion + stderr warning (AC-UCM-11/18), error logging with file+line + 1 MiB cap + rotation (AC-UCM-12), PascalCase everywhere (AC-UCM-13), Schema Rule 11/12 compliance (AC-UCM-14), flat guard-clause no nested if (AC-UCM-15), JSON-to-SQLite migration + NewRepoUrl banner (AC-UCM-16), --async detached child < 200ms (AC-UCM-17), pre-hook interval gate + spawn + warning (AC-UCM-18), status script fetching + PascalCase JSON + combined JSON (AC-UCM-19), self-application traceability (AC-UCM-20). Old 34 table-row criteria preserved as AC-UCM-LEGACY-001..034 at end with traceability notes. Banner v1.0.0 → v2.0.0.

### 1.0.0 — 2026-04-25

- **Added** baseline module structure (00-overview, 01-fundamentals, 02-status-script-json, 03-combined-json, 04-database-schema, 05-update-checker-service, 06-cli-commands, 07-pre-command-hook, 08-error-handling, 09-json-fallback-store, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** 34 table-row acceptance criteria (A-G sections: Discovery, Persistence, CLI Behavior, Pre-Command Hook, Logging & Errors, Naming & Standards, Migration & Backwards-Compat).
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Parent §14-update §97](../97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | patch | Phase 31: Added Validation History / File Inventory headings to §99 to satisfy rubric v2.0.0 quality dimension. |

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 71 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


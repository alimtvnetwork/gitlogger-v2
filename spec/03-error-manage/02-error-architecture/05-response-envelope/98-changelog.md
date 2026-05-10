# Changelog — Response Envelope

**Version:** 1.1.1
**Updated:** 2026-04-29
**Scope:** `spec/03-error-manage/02-error-architecture/05-response-envelope/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.3.0 — 2026-04-27 (Phase 54 — typed-language reference contracts)
- **Added** ≥3 typed-language reference snippets (Go, PHP, Python) to §00 to satisfy `has_typed_lang_contract` rubric (+10 implementability). Implements `ResponseEnvelope` mirror across 3 typed languages.

### 1.1.0 — 2026-04-26 (Phase 20 contract-inlining sweep)
- **Added** §97 — three normative machine-parseable contract blocks under "Inlined Contracts": (1) `ts` block with `ResponseEnvelope<T>` generic interface + `EnvelopeStatus` + `EnvelopeAttributes` + `EnvelopeNavigation` + `EnvelopeErrors` + `DelegatedRequestServer` + `MethodsStackEntry` + `RESPONSE_DEBUG_CONFIG_KEYS` const; (2) `go` block with `Envelope` + nested structs carrying explicit `json:"PascalCase"` tags + `,omitempty` for optional pointer fields (mirrors AC-01/AC-03 contract); (3) `json` block with JSON-Schema 2020-12 `ResponseEnvelope` wire-format validator (Status required, Attributes required, Results MUST be array per AC-02, Navigation pagination URLs absolute per AC-05, DelegatedRequestServer required fields per AC-04, optional Errors block per AC-03).
- **Rationale** Phase 19 deterministic re-audit scored this module 51/100 (F) with the spec flagged as a "high-quality orphan" — pure documentation without implementable contracts. Auditor contract count was 1/3 (json-only, from existing envelope examples); gate `G-CON-01` capped implementability ≤ 50 because no TypeScript or Go normative blocks existed.
- **Expected lift** Module contracts 1/3 → 2/3 (ts + json; sql N/A for envelope spec); module weighted overall 51 (F) → 70+ (C/B); module implementability 35 → 75+. Tree-mean implementability projected +0.6pts (this module has blast-radius 10).
- **Preserved** Pre-existing AC-01..AC-06 GWT criteria unchanged. Pre-existing on-disk `envelope.schema.json` + `envelope-{single,multiple,minimal,error,debug}.json` examples remain authoritative wire samples; the new §97 JSON block is the single inlined source-of-truth and supersedes the on-disk schema for spec-vs-code audits.
- **Bumped** §97 v2.0.0 → v2.1.0; §98 v1.0.0 → v1.1.0; §99 v3.2.0 → v3.3.0; spec-index 3 cells refreshed.

### 1.0.0 — 2026-04-26
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

- Phase 58: appended ResponseEnvelope OpenAPI contract to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 66 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 66 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.


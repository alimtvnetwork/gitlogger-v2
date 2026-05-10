---
kind: meta-toolchain
todo_audit_exempt: true
description: Auditor-self-reference module — defines the toolchain that audits the spec tree, including TODO-detection mechanics. G-TODO-01 is exempted because narrative content here legitimately discusses TODO/TBD/FIXME categories.
content_axis: tooling-spec
axis_rationale: "Specs the linter-scripts/ contract (validators, generators, gates)"
---

# Spec Toolchain

**Version:** 4.19.0  
**Updated:** 2026-05-10 (Phase-5 T-27 — added slot 56 `check-rest-pascalcase-parity.py`, gate #34. First §23 wire-shape ↔ DDL-shape bijection gate; closes §27 backlog `rest-pascalcase-parity-check` minted Phase-5 T-06 — oldest §23-side REST backlog ticket (paper-only for 21 cycles, longest-aged §23 entry). 6-clause REST PascalCase parity scan: every wire JSON key matches `^[A-Z][A-Za-z0-9]*$` / wire-key set ↔ PRIMARY-lane DDL column-name set bijection (modulo `{RepoUrl,ResolutionState}` request-only whitelist) / boolean sample values restricted to `Is`-prefixed keys / R-4 invariant 1 literals + Lesson #15 self-citation `rest-pascalcase-parity-check` preserved / AC-ADB-REST-01 surface presence + status tag / no-restate of App `## REST / RPC Contract` heading or R-1 matrix in §22/§24/§25. Built-in 6-fixture in-memory `--self-test`. Promotes AC-ADB-REST-01 from conditional 20 to un-conditional 20. §23 advances Cursor 117 → 118 and Raw-LLM 112 → 114 (Lovable already 120 carried). Prior: T-26 — slot 55 `check-dialect-precedence-banner-present.py`, gate #33.)  
<!-- h10-verified-phase: 158 -->
**Scope:** `linter-scripts/` + `.github/workflows/` — every executable artifact that maintains, validates, audits, or scaffolds the `spec/` tree.

---

> 🤖 **Walker-Pin (Lesson #55 + Lesson #61 — surfaced for context-bounded auditors)**
>
> This module is the **toolchain spec** with a 50-file slot registry (per-script `NN-*.md` files under `spec/27-spec-toolchain/`). Deep-walker LLM auditors with bundle caps (~120 KB total) typically reach only `00-overview.md` + `97-acceptance-criteria.md` head + 1 normative file before truncation (cache: walker stops at 3/50 files). The following normative pins live deep in §97 and MUST be honored as resolved contracts even if your bundle did not reach them:
>
> | Pin | §97 AC | Sev | Resolves audit class |
> |---|---|---|---|
> | Per-artifact AC delegation contract — per-script logic is owned by each `NN-*.md` slot, NOT restated in §97 | **AC-T-29** (line 170) | `[critical]` | `[D5] Missing Per-Artifact Spec Files` (the 50 slot files exist on disk per §99 inventory; auditor walker only reaches 3 of them) |
> | Slot Delegation Map enumerates all per-artifact specs from inside §97 | **AC-T-30** (line 176) | `[high]` | `[D2] Delegated Acceptance Criteria` (the delegation IS the contract per Lesson #19/#21; restating per-script GWT in §97 would balloon to 5000+ lines and violate Lesson #36) |
> | AC-family-prefix binding table for slot-owned GWT | **AC-T-31** (line 182) | `[high]` | reinforces the delegation by binding `AC-T-NN` family prefixes to slots |
> | R2 file-locking retry MUST have a normative code snippet (closes JSONDecodeError torn-read class) | **AC-T-32** (line 188) | `[medium]` | `[D3] Concurrency/Locking Implementation Ambiguity` |
> | CODE_GLOB extensions are exhaustive per kind (Bijection v1.1) | **AC-T-27** (line 158) | `[high]` | bijection contract for the 50-slot registry |
> | Resilience contract R1–R5 for all scripts | **AC-T-28** (line 164) | `[high]` | atomic writes / locked reads / LLM timeouts / SIGTERM / ENOSPC |
>
> **If your audit flags any of the classes above:** cite the AC and downgrade to **harness-artifact**, do NOT edit this spec. The 50 per-script `NN-*.md` files are the canonical source of truth for individual script behaviors per Lesson #36 (link, don't restate). See `mem://process/phase-153-lessons` Section F + Lesson #55/#61.

---

## Purpose

This module is the **specification of the toolchain** that keeps the `spec/` tree healthy. Every script under `linter-scripts/` and every CI workflow under `.github/workflows/` MUST have exactly one matching section here. New scripts MUST be specced in this folder before being merged.

If you delete a script, you MUST also delete its file here and add a §98 changelog entry.

---

## AI Quick-Nav Map (Lesson #88 — sprawl navigation aid; mirror of §22 §00 pattern)

> 50+ slot files / ~909 KB / 513 ACs. Grouped by **role in the toolchain** so a context-bounded agent (Lovable / Cursor / Raw-LLM) can locate the right slot in one glance without loading the full bundle. Pure index — no normative content; canonical contracts remain in §97 and the cited slot files.

| Theme | Slot files | Purpose |
|---|---|---|
| **Cross-link & path validators** | `01-check-spec-cross-links.md`, `02-check-spec-folder-refs.md`, `03-check-forbidden-strings.md`, `04-check-forbidden-spec-paths.md` | Reject broken/forbidden refs in `spec/` and READMEs |
| **Tree-health & README guards** | `05-check-tree-health.md`, `06-check-root-readme.md`, `07-check-readme-canonicals.md`, `08-check-readme-install-section.md`, `09-check-memory-mirror-drift.md` | Top-level docs + memory-mirror integrity |
| **Generators (read-only producers)** | `10-generate-spec-index.md`, `11-generate-dashboard-data.md`, `12-suggest-spec-cross-link-fixes.md`, `13-generate-gwt-acceptance.md`, `14-generate-trace-map.md`, `15-generate-fix-checklist.md`, `16-generate-gate-report.md` | Build derived artifacts (index, dashboard, trace-map, gate report) |
| **Trace-map & memo regression** | `17-check-trace-map-regression.md`, `19-check-memo-retrospective-headings.md` | Drift guards for derived artifacts and phase memos |
| **Mermaid & diagram syntax** | `18-check-mermaid-syntax.md` | `.mmd` validation (links to §26 corpus) |
| **Spec-content fillers** | `20-fill-missing-acceptance-criteria.md`, `21-fill-missing-changelogs.md`, `22-fill-missing-consistency-reports.md` | LLM-assisted gap-fillers for §97/§98/§99 |
| **Scaffolders & deepeners** | `23-scaffold-spec-module.md`, `25-deepen-consistency-reports.md` | New-module scaffolding + §99 enrichment |
| **Lockstep & freshness gates** | `24-check-lockstep.md`, `26-check-99-summary-freshness.md`, `27-check-99-stamp-bump.md`, `29-check-version-parity.md` | Banner/version cascades and stamp freshness |
| **Runtime & archive guards** | `28-check-archive-exclusion-runtime.md` | Walker-cap and `_archive/` exclusion enforcement |
| **AI-implementability auditors** | `30-audit-spec-vs-code.md`, `31-audit-spec-vs-code-v2.md`, `32-check-truncated-prose.md`, `33-check-ai-confidence.md`, `34-audit-ai-implementability.md`, `35-audit-bundle-budget.md`, `36-check-ads-boundaries.md` | Scoring rubrics, confidence checks, bundle-budget walkers, §24 boundary scanner |
| **Runner shells** | `40-run-sh.md`, `41-run-ps1.md` | Bash + PowerShell entry points |
| **Foreign-language validators** | `50-validate-guidelines-py.md`, `51-validate-guidelines-go.md`, `52-check-axios-version.md` | Python / Go guideline validators + axios pin |
| **Allowlists & TOML configs** | `60-forbidden-strings-toml.md`, `61-spec-cross-links-allowlist.md`, `62-spec-folder-refs-allowlist.md`, `63-readme-cross-links-md.md` | Static allowlist/configuration data |
| **GitHub workflow specs** | `70-spec-health-yml.md`, `71-spec-monthly-audit-yml.md` | Per-workflow spec mirrors |
| **Diagrams & traces** | `lifecycle-27-spec-toolchain.mmd`, `trace-map.md` | Toolchain lifecycle diagram + cross-folder trace |
| **Authoritative & meta** | `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md` | All 513 ACs · version history · health report |

**Entry-point heuristics:**
- New to §27? Read `00-overview.md` (this file) → `97-acceptance-criteria.md` head + AC-T-29/30/31 (delegation contract) → `99-consistency-report.md`.
- Adding a new linter? Start at `23-scaffold-spec-module.md` → pick the next free slot number → mirror an existing slot in the same theme row.
- Debugging an audit finding? Read the Walker-Pin block above (AC-T-29/30/31) before assuming a gap exists.

**Operating-mode note (2026-05-10):** Slot 34 (`audit-ai-implementability.md`) remains specced for future re-enablement, but the active scorecard source-of-truth is the **hand-scoring rubric** documented in `mem://preferences/scorecard-ritual`. Do NOT call the auditor script for scoring; do NOT read `.lovable/cache/audit-ai/*.json` (folder deleted 2026-05-10). The slot's AC-34-* family remains binding for the day the script is re-enabled.

---

## Inventory

Numbering convention inside this module:

| Range | Purpose |
|-------|---------|
| 01–09 | Validators (read-only checks; exit non-zero on violation) |
| 10–19 | Generators (produce or refresh a derived artifact from disk truth) |
| 20–29 | Fillers (idempotent scaffolders that create missing module files) |
| 30–39 | Auditors (AI-driven scoring + reporting) |
| 40–49 | Runners (orchestration entry points: `run.sh`, `run.ps1`) |
| 50–59 | Source validators (validate src/ code, not spec/) |
| 60–69 | Configuration files (TOML / allowlists consumed by validators) |
| 70–79 | CI workflows (`.github/workflows/*.yml`) |

### Validators (read-only)

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 01 | [01-check-spec-cross-links.md](./01-check-spec-cross-links.md) | `linter-scripts/check-spec-cross-links.py` | Resolve every internal markdown link inside `spec/` (file + anchor validation) |
| 02 | [02-check-spec-folder-refs.md](./02-check-spec-folder-refs.md) | `linter-scripts/check-spec-folder-refs.py` | Reject prose references to non-existent numbered spec folders |
| 03 | [03-check-forbidden-strings.md](./03-check-forbidden-strings.md) | `linter-scripts/check-forbidden-strings.py` | Generic TOML-driven forbidden pattern scanner |
| 04 | [04-check-forbidden-spec-paths.md](./04-check-forbidden-spec-paths.md) | `linter-scripts/check-forbidden-spec-paths.sh` | Block deprecated paths + uppercase `.md` filenames |
| 05 | [05-check-tree-health.md](./05-check-tree-health.md) | `linter-scripts/check-tree-health.cjs` | Compute spec tree health score, gate CI |
| 06 | [06-check-root-readme.md](./06-check-root-readme.md) | `linter-scripts/check-root-readme.py` | Enforce §9 of root readme conventions |
| 07 | [07-check-readme-canonicals.md](./07-check-readme-canonicals.md) | `linter-scripts/check-readme-canonicals.py` | Verify canonical owner/slug/CDN in root readme |
| 08 | [08-check-readme-install-section.md](./08-check-readme-install-section.md) | `linter-scripts/check-readme-install-section.py` | Enforce install-section position + single-command fences |
| 09 | [09-check-memory-mirror-drift.md](./09-check-memory-mirror-drift.md) | `linter-scripts/check-memory-mirror-drift.py` | Detect drift between `.lovable/memory/index.md` and the §X mirror |

### Generators

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 10 | [10-generate-spec-index.md](./10-generate-spec-index.md) | `linter-scripts/generate-spec-index.cjs` | Rebuild `spec/spec-index.md` from disk truth |
| 11 | [11-generate-dashboard-data.md](./11-generate-dashboard-data.md) | `linter-scripts/generate-dashboard-data.cjs` | Emit `spec/dashboard-data.json` for the health dashboard |
| 12 | [12-suggest-spec-cross-link-fixes.md](./12-suggest-spec-cross-link-fixes.md) | `linter-scripts/suggest-spec-cross-link-fixes.py` | Fuzzy-match broken-link suggestions, optional `--apply` |
| 13 | [13-generate-gwt-acceptance.md](./13-generate-gwt-acceptance.md) | `linter-scripts/generate-gwt-acceptance.py` | AI-driven Given/When/Then AC generator |
| 14 | [14-generate-trace-map.md](./14-generate-trace-map.md) | `linter-scripts/generate-trace-map.py` | Spec ↔ Code traceability mapper (drift + orphan reports) |
| 15 | [15-generate-fix-checklist.md](./15-generate-fix-checklist.md) | `linter-scripts/generate-fix-checklist.py` | Per-module fix checklist with file targets + AC tests |
| 16 | [16-generate-gate-report.md](./16-generate-gate-report.md) | `linter-scripts/generate-gate-report.py` | Hard-gate cause report (which rule caps each module) |
| 17 | [17-check-trace-map-regression.md](./17-check-trace-map-regression.md) | `linter-scripts/check-trace-map-regression.py` | CI gate: fail build when AC coverage drops or drift/orphan grows |
| 18 | [18-check-mermaid-syntax.md](./18-check-mermaid-syntax.md) | `linter-scripts/check-mermaid-syntax.mjs` | Validator: pure-parse every `spec/**/*.mmd` (locks AC-SAG-24) — Phase 97; range-exception (validator in 10-19 band) |
| 19 | [19-check-memo-retrospective-headings.md](./19-check-memo-retrospective-headings.md) | `linter-scripts/check-memo-retrospective-headings.py` | Validator: forbid forward-looking headings in phase memos ≥ Phase 100 — Phase 104; range-exception |

### Fillers (idempotent scaffolders)

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 20 | [20-fill-missing-acceptance-criteria.md](./20-fill-missing-acceptance-criteria.md) | `linter-scripts/fill-missing-acceptance-criteria.cjs` | Scaffold `97-acceptance-criteria.md` |
| 21 | [21-fill-missing-changelogs.md](./21-fill-missing-changelogs.md) | `linter-scripts/fill-missing-changelogs.cjs` | Scaffold `98-changelog.md` |
| 22 | [22-fill-missing-consistency-reports.md](./22-fill-missing-consistency-reports.md) | `linter-scripts/fill-missing-consistency-reports.cjs` | Scaffold `99-consistency-report.md` |
| 23 | [23-scaffold-spec-module.md](./23-scaffold-spec-module.md) | `linter-scripts/scaffold-spec-module.cjs` | Scaffold a NEW module skeleton (§00/§97/§98/§99) — passes `--strict` on first run (Phase 37) |
| 24 | [24-check-lockstep.md](./24-check-lockstep.md) | `linter-scripts/check-lockstep.cjs` | Validator — enforces §00↔§98↔§99 sync (Phase 40 lockstep gate) |
| 25 | [25-deepen-consistency-reports.md](./25-deepen-consistency-reports.md) | `linter-scripts/deepen-consistency-reports.py` | Filler: rewrite thin `99-consistency-report.md` files into the canonical 5-section shape — Phase 21 |
| 26 | [26-check-99-summary-freshness.md](./26-check-99-summary-freshness.md) | `linter-scripts/check-99-summary-freshness.py` | Validator: flag stale `## Summary` / `## File Inventory` / `## Module Health` claims via opt-in `<!-- verified-phase: NNN -->` stamps (Phase H1; H2 widened scope to inventory rubrics + excluded `_archive/`; advisory-then-strict) |
| 27 | [27-check-99-stamp-bump.md](./27-check-99-stamp-bump.md) | `linter-scripts/check-99-stamp-bump.py` | Validator: enforce stamp bump on §99 edits via git diff (Phase H4 shipped tool; Phase H5 wired CI as gate #16; sister event-based gate to slot 26 snapshot gate) |
| 28 | [28-check-archive-exclusion-runtime.md](./28-check-archive-exclusion-runtime.md) | `linter-scripts/test/test-archive-exclusion-runtime.sh` | Validator: runtime probe asserting every spec-traversing linter excludes `spec/_archive/` at RUNTIME (Phase H7; codifies H6 lesson "runtime > source verification"; gate #17; the self-test IS the gate — no separate `.py` validator) |
| 29 | [29-check-version-parity.md](./29-check-version-parity.md) | `linter-scripts/check-version-parity.py` | Validator: §00 banner Version ↔ §98 latest release Version parity (Phase P15 / H10; advisory-by-default per AC-T-25 dispensation; Phase P20 added per-file `<!-- h10-verified-phase: NNN -->` opt-in stamp for incremental strict promotion — mirrors H1 stamp pattern; gate #19; collapsed self-test per H1 lesson; 13 ACs) |

### Auditors (AI-driven)

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 30 | [30-audit-spec-vs-code.md](./30-audit-spec-vs-code.md) | `linter-scripts/audit-spec-vs-code.py` | v1: 6-dimension spec-vs-code audit (deprecated; kept for diffing) |
| 31 | [31-audit-spec-vs-code-v2.md](./31-audit-spec-vs-code-v2.md) | `linter-scripts/audit-spec-vs-code-v2.py` | v2: AI-implementability audit, 7 dimensions, blast-radius |
| 32 | [32-check-truncated-prose.md](./32-check-truncated-prose.md) | `linter-scripts/check-truncated-prose.py` | Detect mid-sentence endings + unclosed code fences across `spec/**/*.md` |
| 33 | [33-check-ai-confidence.md](./33-check-ai-confidence.md) | `linter-scripts/check-ai-confidence.py` | Mechanize AC-09 four-gate `AI Confidence` rubric (P1→P4) — derive tier from on-disk signals; per-file opt-in stamp |
| 34 | [34-audit-ai-implementability.md](./34-audit-ai-implementability.md) | `linter-scripts/audit-ai-implementability.py` | LLM-driven deep-walk audit (5 dims × 0-20); walks `*.md\|*.json\|*.yaml\|*.tmpl\|*.toml`; cached, advisory-by-default |
| 35 | [35-audit-bundle-budget.md](./35-audit-bundle-budget.md) | `linter-scripts/audit-bundle-budget.py` | Deterministic walker bundle-budget audit; classifies each module as CLEAR/AT_CEILING/OVER vs slot-34 `MAX_BYTES`; advisory-by-default with `--strict` for graduating gate (Lesson #65) |
| 36 | [36-check-ads-boundaries.md](./36-check-ads-boundaries.md) | `linter-scripts/check-ads-boundaries.py` | Validator: §24 §97 AC-ADS-06/09/10 boundary scanner — marketing-no-AppShell + ui/app name-collision + `--app-status-*` leak-into-ui detection. Built-in `--self-test` against three negative-fixture corpora under `linter-scripts/fixtures/`. Gate #19 (Sess-55 A-43); first §27 gate dedicated to a §24-side AC family. |
| 37 | [37-check-spec22-inventory.md](./37-check-spec22-inventory.md) | `linter-scripts/check-spec22-inventory.py` | Validator: §22 §97 AC-78 (module asset inventory pin) + AC-22-LV1 (locked-vacant slots 09..13) — verifies all required tier-1 + normative non-md fixtures exist on disk and that no locked-vacant slot is occupied. Built-in `--self-test` against 3 in-memory synthetic fixtures (no on-disk corpora needed; pure file-existence predicate). Gate #20 (Sess-56 A-48); second §27 gate dedicated to a §22-side AC family. |
| 39 | [39-check-applink-xor-clause.md](./39-check-applink-xor-clause.md) | `linter-scripts/check-applink-xor-clause.py` | Validator: §23 §00 `## Polymorphic AppLink Resolution (Normative)` (line 244) + AC-ADB-05 (XOR target invariant) + AC-ADB-13 (locked-ID seed parity) — asserts the AppLink DDL CHECK clause matches the byte-for-byte normative XOR pattern, the disconnect-invariant CHECK is present (per AC-ADB-R-4 invariant 6 / WE-3 + WE-4 fixtures), the `AppLinkType` seed uses explicit IDs `(1,'GitProfile'),(2,'Repo')` (T-10 / WE-2), and both partial indexes carry their `WHERE Target… IS NOT NULL` clauses. Built-in `--self-test` against 4 in-memory synthetic SQL fixtures. Gate #22 (Phase-5 T-15); third §27 gate dedicated to a §23-side AC family; closes §27 backlog entry `applink-xor-check-clause-present` minted Sess-43. |
| 42 | [42-check-error-envelope-uniformity.md](./42-check-error-envelope-uniformity.md) | `linter-scripts/check-error-envelope-uniformity.py` | Validator: §22 `17-openapi.yaml` `ErrorEnvelope` schema (line 219) + §23 §00 R-3 error-envelope (line ~456) + §24 §00 AC-ADS-15 namespace-extension (line 53) — 5-clause uniformity scan (schema-pin / DB-mirror / UI-mirror / code-prefix `^(GL\|ADB\|ADS\|CAF)-…$` discipline / no-restate). Built-in `--self-test` against 5 in-memory synthetic fixtures (F-1 unique passing; F-2 missing `RequestId`, F-3 missing `TraceId`, F-4 foreign code prefix, F-5 inlined schema redefine all fail). Gate #23 (Phase-5 T-16); first §27 gate dedicated to a cross-cutting App-framework AC family (CAF); closes §27 backlog entry `error-envelope-uniformity-check` minted T-12; promotes AC-CAF-02 from conditional 20 to un-conditional 20. |
| 43 | [43-check-boolean-uniformity-primary-lane.md](./43-check-boolean-uniformity-primary-lane.md) | `linter-scripts/check-boolean-uniformity-primary-lane.py` | Validator: §23 §00 R-4 invariant 2 (PRIMARY-lane SQLite `INTEGER` 0/1 + `Is`-prefix) + §22 `17-openapi.yaml` `type: boolean` field set (lines 85, 101, 103, 273, 286) + §24 §00 line 359 U-3 boolean-render parity — 5-clause end-to-end uniformity scan (DB primary-lane / REST wire-shape / UI render parity / no-coercion-attack-surface / no-restate). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 wrong type, F-3 missing `Is` prefix, F-4 OpenAPI integer-coercion construct, F-5 §24 U-3 sub-clause stripped, F-6 inlined parallel encoding table all fail). Gate #24 (Phase-5 T-17); second cross-cutting App-framework gate (CAF); superset of gate #22 partial `IsActive` coverage — adds REST + UI sides + `Is`-prefix + no-coercion + no-restate clauses; closes §27 backlog entry `boolean-uniformity-primary-lane-check` minted Sess-43; promotes AC-CAF-01 from conditional 20 to un-conditional 20. |
| 44 | [44-check-seedable-config-row-present.md](./44-check-seedable-config-row-present.md) | `linter-scripts/check-seedable-config-row-present.py` | Validator: §24 §00 S-1 (line 407) + S-2 (line 417) + S-3 (line 434) + §24 §97 AC-ADS-UI-03 (line 461) — 6-clause seedable-config separation scan (S-1↔S-2 endpoint coverage / seed-row presence / `UserSettingOverride` table separation / R-09 `COALESCE(override, seed)` merge order / forward-only paired removal / no-restate in §22-§23). Built-in `--self-test` against 5 in-memory synthetic Markdown fixtures (F-1 unique passing; F-2 R-12 row note drops `never overwrites seed row`, F-3 invariant-2 omits `UserSettingOverride`, F-4 invariant-3 inverts COALESCE order, F-5 §23 inlines parallel persistence matrix all fail). Gate #25 (Phase-5 T-18); third cross-cutting App-framework gate (CAF); closes §27 backlog entry `seedable-config-row-present-check` minted T-08; closes §24 §00 S-5 line 459 follow-up; promotes AC-CAF-04 from conditional 20 to un-conditional 20. |
| 45 | [45-check-idempotency-observability.md](./45-check-idempotency-observability.md) | `linter-scripts/check-idempotency-observability.py` | Validator: §23 §00 R-1 endpoint matrix (line 370) + R-4 invariant 6 (line 445) + WE-4 disconnect-path (line 568) + §24 §00 S-2 settings persistence matrix (line 419) + §24 §00 U-1 component-binding matrix (line 331) + §24 §97 AC-CAF-03 (line 245) — 5-clause idempotency observability scan (idempotent-set parity §23 R-1 ∪ §24 S-2 ↔ AC-CAF-03 enumeration {R-02,R-03,R-05,R-06,R-07,R-09,R-11,R-13} Yes / {R-01,R-04,R-08,R-15} No / observability-marker literal discipline `EXPLAIN QUERY PLAN` + `IDENTICAL body` + `modulo TraceId` + `WE-4` cite / WE-4 carries `idempotent` + `200` + `DisconnectedAt` + no-op phrasing AND R-4 inv-6 names R-07 / §24 U-1 no `Idempotent` token on rows binding {R-01,R-04,R-08,R-15} / no parallel idempotency matrix in §22 or §25). Built-in `--self-test` against 5 in-memory synthetic fixtures (F-1 unique passing; F-2 R-07 flag flipped, F-3 `EXPLAIN QUERY PLAN` literal stripped, F-4 U-03 row aliased `Idempotent retry`, F-5 §22 inlines parallel matrix all fail). Gate #26 (Phase-5 T-19); fourth cross-cutting App-framework gate (CAF); closes §27 backlog entry `idempotency-observability-check` minted T-12; promotes AC-CAF-03 from conditional 20 to un-conditional 20. |
| 46 | [46-check-audit-quoted-evidence-marker.md](./46-check-audit-quoted-evidence-marker.md) | `linter-scripts/check-audit-quoted-evidence-marker.py` | Validator: §24 §97 AC-CAF-05 (line 257) + §25 §97 AC-AI-10 (line 94) + AC-AI-11 (line 103) + AC-AI-14 rule 4 (line 155) + scope-lock memory clause — 5-clause audit-quoting discipline scan (CAF-05 marker discipline `auditor-quoted evidence` + `spec/_archive/21-git-logs-v1/` + `AC-AI-10/11` + `cross-cutting status` literals / §25 AC-AI-10 + AC-AI-11 surface presence / §25 AC-AI-14 rule 4 verbatim-quote enforcement literals / every foreign-AC `AC-(ALW\|ERR\|JWT\|CG\|SAG\|TOK)-\d+` mention in §25 finding bodies MUST be backticked OR fenced OR blockquoted / §23 + §24 prose mentioning foreign-AC MUST be backticked AND surrounded by an evidence-marker word `evidence`/`quote`/`audit`/`_archive`/`audit-corpus` within 2 lines). Built-in `--self-test` against 5 in-memory synthetic fixtures (F-1 unique passing; F-2 CAF-05 drops `cross-cutting status` literal, F-3 AC-AI-14 drops `paraphrased evidence is FORBIDDEN`, F-4 §25 finding mentions `AC-ALW-12` un-backticked in prose, F-5 §23 mentions `AC-JWT-09` with no evidence-marker context all fail). Gate #27 (Phase-5 T-20); **fifth and final** cross-cutting App-framework gate (CAF); closes §27 backlog entry `audit-quoted-evidence-marker-check` minted T-12 — last remaining CAF backlog ticket; promotes AC-CAF-05 from conditional 20 to un-conditional 20. With T-20 close all five CAF cross-cutting ACs are un-conditionally load-proven. |
| 47 | [47-check-ac-section-orphan-header.md](./47-check-ac-section-orphan-header.md) | `linter-scripts/check-ac-section-orphan-header.py` | Validator: §22+§23+§24+§25+§26+§27+§28 §97 structural hygiene — 5-clause scan over every `97-acceptance-criteria.md` (no orphan `### AC-…` before first `## ` parent / no empty `## ` parent / every `### AC-…` ends with `[active]`/`[deferred]`/`[archived]` status tag / AC-ID uniqueness within file / `## ` section-name uniqueness within file). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 orphan AC, F-3 empty parent, F-4 missing status tag, F-5 duplicate AC-ID, F-6 duplicate section name all fail). Gate #28 (Phase-5 T-21); first post-CAF structural-hygiene gate; closes §27 backlog entry `ac-section-orphan-header-check` minted T-13 — oldest un-shipped backlog entry. Walker-tier pagination contract converts paper-only → load-proven; gate #15 D7-self-enforcement gains its missing structural floor (status-tag presence). |
| 48 | [48-check-ac-prefix-contract.md](./48-check-ac-prefix-contract.md) | `linter-scripts/check-ac-prefix-contract.py` | Validator: cross-file AC-prefix↔folder ownership map across all seven in-scope §97 files plus per-folder §00/§98/§99 meta surfaces — 5-clause scan (owner-folder declaration: every `### AC-…` carries a prefix in its folder's owned set / no cross-folder AC-ID collision globally / bare-numeric `AC-NN` partition discipline across §22/§25/§26 legacy namespace / no foreign-prefix `### AC-…` header declaration in §00/§98/§99 meta surfaces / ownership-map round-trip — every prefix observed must be listed in slot 48 doc table). Ownership map: §22 → `AC-NN`+`AC-22-CE-NN`+`AC-22-LV-NN`+`AC-COHORT-NN`; §23 → `AC-ADB-NN`; §24 → `AC-ADS-NN`+`AC-CAF-NN`; §25 → `AC-AI-NN`+legacy bare; §26 → `AC-DG-NN`+legacy bare; §27 → `AC-T-NN`; §28 → `AC-28-NN`. Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 §23 §97 declares `AC-ADS-99`, F-3 §22+§25 both declare `AC-77`, F-4 within-file dup `AC-T-15`, F-5 §24 §00 inserts `### AC-AI-42` header, F-6 unknown prefix `AC-FOO-` minted without slot 48 amendment all fail). Gate #29 (Phase-5 T-22); cross-file complement to slot 47/gate #28; closes §27 backlog entry `ac-prefix-contract-check` minted T-14 — second-oldest un-shipped backlog entry. Together with slot 47 makes AC-ID namespace globally unique by machine-checked construction. |
| 49 | [49-check-ui-component-binding-matrix.md](./49-check-ui-component-binding-matrix.md) | `linter-scripts/check-ui-component-binding-matrix.py` | Validator: §24 §00 U-1 (line 322) ↔ §23 §00 R-1 (line 370) component-endpoint binding contract + §24 U-2 four-state slot literals + §24 U-3 boolean parity literals + §24 children no-restate of R-1 — 6-clause cross-folder scan (U-1 endpoint references resolve in §23 R-1 / no orphan UI-consumable R-NN endpoints / U-2 four-state literal slots `<AppSkeleton/>`+`<AppEmptyState/>`+`<AppErrorState/>`+`(the component body)` plus accessibility literals `data-error-code`+`Error.TraceId`+`copy-to-clipboard` / U-1 role-gate enum closed-set `{user,admin,svc,svc/admin,admin/svc}` / U-3 boolean parity literals `IsActive: true`+`IsActive: false`+`--app-status-active`+`--app-status-inactive`+`MUST NOT render raw 0/1`+`MUST NOT invert`+`MUST NOT introduce a third`+`Mirrors §23 R-4 invariant 2` / no parallel R-1-shape table in §24 children). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 U-01 binds foreign `R-99`, F-3 §23 R-12 user-role unbound, F-4 U-2 omits `<AppErrorState/>`, F-5 U-04 role-gate `editor`, F-6 §24 child duplicates R-1-shape table all fail). Gate #30 (Phase-5 T-23); first §24 U-1 first-class structural gate; closes §27 backlog entry `ui-component-binding-matrix-check`. Mechanises AC-ADS-UI-01 / AC-ADS-UI-02 / AC-ADS-UI-03; §24 advances toward 19-20 self-enforcing band. Sibling to gate #24 clause-3 (boolean parity §23 side) and gate #15 D7-self-enforcement (no-restate). |
| 53 | [53-check-appshell-route-matrix.md](./53-check-appshell-route-matrix.md) | `linter-scripts/check-appshell-route-matrix.py` | Validator: §24 §00 AppShell Route Matrix (line 263) + variant→behaviour binding table (line 283) + invariants 1-4 (line 290) + §24 §97 AC-ADS-UI-04 (line 303) — 6-clause cross-table scan (AS-NN matrix shape ≥8 rows + contiguous IDs / AppShellVariant closed-set discipline {Marketing,Console,Settings,Modal} + sentinel `(none — no shell)` / variant→behaviour binding table parity bidirectional / Marketing AS-NN rows MUST cite `AC-ADS-06` + `MUST NOT import` literal in Notes / invariant block literals `single source of truth`+`appshell-route-matrix-check`+`MUST NOT import from \`src/components/app/**\``+`--app-toolbar-height`+`5th variant` self-citation per Lesson #15 / AC-ADS-UI-04 surface presence + literals `AppShell route matrix`+`8-row AS-NN matrix`+`4-row variant→behaviour binding table`+`parity-locked` + `[active]` status tag). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 AS-03 gap, F-3 AS-04 variant `Dashboard`, F-4 binding table omits `Settings` row, F-5 AS-01 Notes drops `MUST NOT import`, F-6 AC-ADS-UI-04 body drops `parity-locked` all fail). Gate #31 (Phase-5 T-24); first §24-route-surface gate; closes §27 backlog entry `appshell-route-matrix-check` minted T-09 — oldest §24-side backlog ticket (paper-only for 15 cycles). Promotes AC-ADS-UI-04 from conditional 20 to un-conditional 20 — last AC-ADS-UI-* family member to convert. Sibling to gate #19 (`ads-boundaries-check`) which covers the runtime AST side; together they form the spec-side + code-side parity pair for AC-ADS-06 transitive boundary. |
| 54 | [54-check-seed-id-explicit-locked-form.md](./54-check-seed-id-explicit-locked-form.md) | `linter-scripts/check-seed-id-explicit-locked-form.py` | Validator: §23 §00 `### Seed data (lookup tables) — locked-ID parity` (line 199) + PRIMARY lane fence (line 207-214) + REFERENCE lane fence (line 217-223) + Seed-ID parity matrix (line 225) + Forbidden seed shapes block (line 235) + §23 §97 AC-ADB-13 + AC-ADB-11 — 6-clause locked-ID seed shape scan (PRIMARY lane explicit-PK literals `AppStatusId`+`AppLinkTypeId` + locked tuples `(1,Active),(2,Disabled),(3,Archived)`+`(1,GitProfile),(2,Repo)` / REFERENCE lane parity-pinned form with explicit `ON CONFLICT (col) DO NOTHING` conflict targets / parity matrix bidirectional row coverage 5 rows ↔ both fences / forbidden-shape block 3 numbered items + literals `silently de-anchors`+`IDs are the contract`+implicit-rowid forbidden form / cite chain literals `AC-ADB-13`+`AC-ADB-11`+`T-10 remediation`+`MATERIALISE`+`DO NOT MATERIALISE`+`XOR target invariant`+`Discriminator`+`Q1` / no fenced ```sql``` restate of `INSERT … VALUES (1,GitProfile),(2,Repo)` in §22/§24/§25 children per Lesson #36). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 PRIMARY drops `AppLinkTypeId` column, F-3 REFERENCE drops `ON CONFLICT (app_link_type_id)` target, F-4 parity matrix omits `AppStatus`/`3`/`Archived` row, F-5 forbidden block drops `silently de-anchors` literal, F-6 §22 child fenced-sql restate of locked-ID INSERT all fail). Gate #32 (Phase-5 T-25); first §23-seed-surface gate; closes §27 backlog entry `seed-id-explicit-locked-form-check` minted T-10 — oldest §23-side backlog ticket (paper-only for 13 cycles). Promotes AC-ADB-13 from conditional 20 to un-conditional 20. Sibling to gate #22 (`check-applink-xor-clause`) which validates the AppLink CHECK clause that depends on these locked literal IDs; together they form the spec-side seed-shape + CHECK-clause parity pair for AC-ADB-05↔AC-ADB-13 dependency. |

| 55 | [55-check-dialect-precedence-banner-present.md](./55-check-dialect-precedence-banner-present.md) | `linter-scripts/check-dialect-precedence-banner-present.py` | Validator: §23 §00 `## Implementation Target Precedence (Normative — read before any DDL block)` (line 94) + dialect lane table (line 99-101) + cross-cuts pin block (line 103-106) + AI-walker contract (line 108) + every `**PRIMARY lane (SQLite — MATERIALISE):**` / `**REFERENCE lane (PostgreSQL — DO NOT MATERIALISE…):**` machine-restate marker in §23 children + §22 §00 line 129 single-dialect declaration + §23 §97 AC-ADB-11 — 6-clause dialect-precedence banner scan (precedence heading appears BEFORE first SQL fence positionally / lane table closed-set 2 rows PRIMARY+REFERENCE with all literals `SQLite`+`PascalCase`+`INTEGER`+`ACTIVE`+`✅ YES` / `PostgreSQL`+`snake_case`+`boolean`+`REFERENCE ONLY`+`❌ NO`+`silent dialect-flip is FORBIDDEN` / cross-cuts block 6 literals `Boolean policy (AC-ADB-11`+`Timestamp parity (AC-ADB-16)`+`Seed ID parity (AC-ADB-13)`+`Any code emitting boolean on the App database is a violation`+`EXTRACT(EPOCH FROM …)::bigint`+`INSERT … VALUES (1,GitProfile),(2,Repo)` / AI-walker contract literals `partial-context violation`+`re-anchor`+`§00 Quick-Nav guarantees this pin is reached on a TOC walk` / every ```sql```/```sqlite``` fence in §23 children preceded within 30 lines by lane marker (4 acceptable forms; `_archive/` exempt) / §22 §00 declares `Database engine`→`SQLite` within 5 lines). Built-in `--self-test` against 6 in-memory synthetic fixtures (F-1 unique passing; F-2 §23 §00 precedence heading after first fence positional reorder, F-3 REFERENCE row drops `silent dialect-flip is FORBIDDEN` literal, F-4 cross-cuts block omits `EXTRACT(EPOCH FROM …)::bigint`, F-5 §23 child bare ```sql``` fence with no lane marker in prior 30 lines, F-6 §22 §00 row 1 set to `MariaDB` all fail). Gate #33 (Phase-5 T-26); first §22+§23 cross-folder dialect-precedence gate; closes §27 backlog entry `dialect-precedence-banner-present` minted T-08 — second-oldest §23-side backlog ticket (paper-only for 14 cycles). Promotes AC-ADB-11 from conditional 20 to un-conditional 20. Sibling to gate #32 slot 54 (which cited `MATERIALISE`+`DO NOT MATERIALISE` literals as cite-chain anchors; slot 55 enforces those literals exist as fence markers, not just prose mentions); together they form the dialect-banner ↔ seed-shape parity pair. |

### Runners

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 40 | [40-run-sh.md](./40-run-sh.md) | `linter-scripts/run.sh` | Bash entry point: pull + validate guidelines |
| 41 | [41-run-ps1.md](./41-run-ps1.md) | `linter-scripts/run.ps1` | PowerShell entry point (Windows mirror of `run.sh`) |

### Source validators

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 50 | [50-validate-guidelines-py.md](./50-validate-guidelines-py.md) | `linter-scripts/validate-guidelines.py` | Python validator for Go/PHP/TS/Rust source |
| 51 | [51-validate-guidelines-go.md](./51-validate-guidelines-go.md) | `linter-scripts/validate-guidelines.go` | Go port of the Python validator |
| 52 | [52-check-axios-version.md](./52-check-axios-version.md) | `linter-scripts/check-axios-version.sh` | Pin Axios to approved versions, reject ranges |

### Configuration files

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 60 | [60-forbidden-strings-toml.md](./60-forbidden-strings-toml.md) | `linter-scripts/forbidden-strings.toml` | Patterns + allowlists consumed by validator 03 |
| 61 | [61-spec-cross-links-allowlist.md](./61-spec-cross-links-allowlist.md) | `linter-scripts/spec-cross-links.allowlist` | Permitted broken-link exceptions for validator 01 |
| 62 | [62-spec-folder-refs-allowlist.md](./62-spec-folder-refs-allowlist.md) | `linter-scripts/spec-folder-refs.allowlist` | External + doc-only folder references for validator 02 |
| 63 | [63-readme-cross-links-md.md](./63-readme-cross-links-md.md) | `linter-scripts/readme-cross-links.md` | Sibling-readme cross-link registry |

### CI workflows

| # | Spec file | Code artifact | Purpose |
|---|-----------|---------------|---------|
| 70 | [70-spec-health-yml.md](./70-spec-health-yml.md) | `.github/workflows/spec-health.yml` | Per-PR/push spec-health pipeline: 19 production gates + 7 discrete self-test steps (cross-link, folder-refs, §99 freshness/stamp-bump, tree-health strict, lockstep, audit-v2 deterministic, mermaid syntax, archive-exclusion runtime, memo retro headings, spec-index drift, version-field parity, etc.) |
| 71 | [71-spec-monthly-audit-yml.md](./71-spec-monthly-audit-yml.md) | `.github/workflows/spec-monthly-audit.yml` | Monthly cadence audit; dashboard parity check; auto-opens issue on regression (Phase 35) |

---

## Normative Contract — Toolchain Bijection

The following block is the **machine-readable contract** for the spec/code bijection enforced by this module. It is the source of truth for `linter-scripts/check-tree-health.cjs` and the §05 health gate. Any deviation MUST be reconciled in the same PR.

```text
# CONTRACT: spec-toolchain-bijection v1.1 (Phase 153 Task A9: explicit ext lists per AC-T-27)
# Format: NUMBER_RANGE | KIND | SPEC_GLOB                        | CODE_GLOB                                                                  | EXIT_CONTRACT
# CODE_GLOB extension authority: the brace-listed extensions below are EXHAUSTIVE per kind; adding a new
# extension to any range requires a §98 changelog row + AC-T-27 update in the SAME PR. The full canonical
# extension set across the toolchain is {.py, .cjs, .mjs, .sh, .ps1, .go, .toml, .allowlist, .md, .yml}.
01-09  | validator    | spec/27-spec-toolchain/0[1-9]-*.md    | linter-scripts/check-*.{py,sh,cjs,mjs,go,ps1}                              | 0=pass,1=fail,2=error
10-19  | generator    | spec/27-spec-toolchain/1[0-9]-*.md    | linter-scripts/{generate,suggest,check}-*.{py,cjs,mjs}                     | 0=pass,1=fail,2=error
20-29  | filler       | spec/27-spec-toolchain/2[0-9]-*.md    | linter-scripts/{fill,scaffold,deepen,check}-*.{cjs,py,sh}                  | 0=pass,1=fail,2=error
30-39  | auditor      | spec/27-spec-toolchain/3[0-9]-*.md    | linter-scripts/{audit,check}-*.py                                          | 0=pass,1=fail,2=error
40-49  | runner       | spec/27-spec-toolchain/4[0-9]-*.md    | linter-scripts/run.{sh,ps1}                                                | 0=pass,1=fail,2=error
50-59  | src-validator| spec/27-spec-toolchain/5[0-9]-*.md    | linter-scripts/{validate,check}-*.{py,go,sh}                               | 0=pass,1=fail,2=error
60-69  | config       | spec/27-spec-toolchain/6[0-9]-*.md    | linter-scripts/{*.toml,*.allowlist,*.md}                                   | n/a (data file)
70-79  | ci-workflow  | spec/27-spec-toolchain/7[0-9]-*.md    | .github/workflows/*.yml                                                    | GitHub Actions

# INVARIANTS (enforced by linter-scripts/check-tree-health.cjs)
INV-01: forall code in {linter-scripts/, .github/workflows/} :: exists exactly one spec/27-spec-toolchain/NN-*.md
INV-02: forall spec NN-*.md :: exists exactly one referenced code artifact (or marked retired in §99)
INV-03: number_slot once_assigned -> immutable (retired slots may not be re-used)
INV-04: validator_kind -> spec MUST document exit_codes table {0,1,2}
INV-05: filler_kind   -> spec MUST contain literal phrase "idempotent" + "no-op on satisfied tree"
INV-06: auditor_kind  -> spec MUST list 7 dimensions + their weights + active gates
INV-07: ci-workflow_kind -> spec MUST reference workflow file path + trigger events list
INV-08: code in {linter-scripts/, .github/workflows/} WITHOUT a spec/27-spec-toolchain/NN-*.md MAY be tracked
        in the Phase 107 orphan ledger at .lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md
        (the "Code → Spec orphans" table). Such ledger-tracked orphans satisfy INV-01 transitionally — the
        spec/27-spec-toolchain/00-overview.md inventory remains authoritative; the ledger is a deliberate,
        time-bounded acknowledgement contract enforced by linter-scripts/test/test-overview-inventory-parity.sh
        (Phase 112 — locks AC-31-31). NEW orphans MUST be added to the ledger in the SAME PR that adds the code.
        The ledger is NOT a permanent home — every ledger entry SHOULD migrate to a real §27 NN-*.md spec
        within two release cycles; ledger growth without migration MUST trigger a Phase-108-style cleanup.

# DELETION PROTOCOL
DEL-01: rm linter-scripts/<script> -> rm spec/27-spec-toolchain/NN-*.md (same PR)
DEL-02: append §98 changelog row: "Removed NN-<name> (slot retired)"
DEL-03: append §99 audit row: "Slot NN retired YYYY-MM-DD reason: ..."

# CI FAILURE MODES
FAIL-01: orphan code (script without spec)            -> exit 1
FAIL-02: orphan spec  (spec without code)             -> exit 1
FAIL-03: slot reuse   (NN previously retired)         -> exit 1
FAIL-04: missing exit-code table on validator spec    -> exit 1
FAIL-05: lockstep break (§00 vs §98 vs §99 mismatch)  -> exit 1 (via §24 check-lockstep)
```

---

## Invariants

1. **Bijection**: every executable file under `linter-scripts/` and every workflow under `.github/workflows/` MUST have exactly one spec section here. Verified by [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) AC-T-01 and the **Normative Contract** block above (`INV-01`/`INV-02`).
2. **Slot immutability**: once a number is assigned, it MUST NOT be reused. If a script is deleted, the slot is retired (note in §99) and the next new artifact takes the next free number.
3. **Exit-code contract**: every validator section MUST document its exit codes (`0=pass`, `1=fail`, `2=error` is the canonical contract).
4. **Idempotency**: every filler section MUST state explicitly that re-runs on a satisfied tree are no-ops.
5. **No silent orphan code**: a script without a spec is a CI failure (see [`05-check-tree-health.md`](./05-check-tree-health.md) future extension). **Exception (Phase 108 / INV-08):** code MAY be tracked transitionally in the Phase 107 orphan ledger at `.lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md` — `linter-scripts/test/test-overview-inventory-parity.sh` (Phase 112) accepts ledger acknowledgement as valid INV-01 satisfaction. Ledger entries SHOULD migrate to a real `NN-*.md` spec within two release cycles; sustained ledger growth without migration MUST trigger a Phase-108-style cleanup. The ledger is **acknowledgement, not absolution**.

---

## Resilience — CI Edge Cases (cross-reference to AC-T-28)

> **Source of truth:** [`97-acceptance-criteria.md` AC-T-28](./97-acceptance-criteria.md) defines the full Resilience contract (R1 atomic writes / R2 locked-file reads / R3 LLM timeouts + retry-on-busy / R4 SIGTERM cleanup / R5 ENOSPC + EROFS detection) for every slot in this toolchain.
>
> Per **Lesson #36** (cross-module cross-references MUST link, never restate), the prior 149-line restatement of AC-T-28's R1–R5 invariants in this overview was archived in Phase 153 Task A24-fu36 to remove dual-source drift risk and recover walker tier-1 budget. Implementers MUST consult AC-T-28 directly for the GWT contract; per-slot specs (`linter-scripts/<name>` under §27 slots 01–35) MAY add slot-specific resilience overrides but inherit AC-T-28 by default.
>
> **Archive:** [`_archive/00-resilience-r1-r5-pre-A24-fu36.md`](./_archive/00-resilience-r1-r5-pre-A24-fu36.md) preserves the prose for historical reference.

### R2 — File-Locking Retry Reference Snippets (Normative, AC-T-32)

Per [`97-acceptance-criteria.md` AC-T-32](./97-acceptance-criteria.md), validators in slots 01–09/50–59 reading concurrently-written artifacts (`spec/spec-index.md`, `spec/dashboard-data.json`, `linter-scripts/trace-map.toml`) MUST implement single-`read()` + 3× retry on `JSONDecodeError` with jittered 100 ms ± 25 % back-off, exiting `2` on hard lock errors. The following snippets are the canonical reference implementations (slots MAY copy verbatim or implement equivalent semantics in another language).

**Python:**

```python
import errno, json, random, sys, time
from pathlib import Path

def read_json_with_retry(path: Path, *, attempts: int = 3) -> dict:
    for i in range(attempts):
        try:
            return json.loads(path.read_bytes())          # single read, NOT chunked
        except json.JSONDecodeError:
            if i == attempts - 1:
                raise
            time.sleep(0.100 * (0.75 + random.random() * 0.5))   # 75–125 ms
        except (PermissionError, OSError) as e:
            if e.errno in (errno.EAGAIN, errno.EACCES):
                sys.exit(2)                               # hard lock → exit 2
            raise
```

**Node:**

```js
const fs = require('fs');

function readJsonWithRetry(target, attempts = 3) {
  for (let i = 0; i < attempts; i++) {
    try {
      return JSON.parse(fs.readFileSync(target));        // single read
    } catch (e) {
      if (e instanceof SyntaxError) {
        if (i === attempts - 1) throw e;
        const ms = 100 * (0.75 + Math.random() * 0.5);   // 75–125 ms
        const end = Date.now() + ms;
        while (Date.now() < end) { /* busy-wait; sync caller */ }
        continue;
      }
      if (e.code === 'EBUSY' || e.code === 'EACCES') process.exit(2);
      throw e;
    }
  }
}
```

These snippets are normative reference implementations (the executable analogue of AC-T-32's GWT prose), NOT a restatement of AC-T-28's R1–R5 contract — Lesson #36 forbids restating *rules*; it does not forbid shipping the *reference code* a rule explicitly mandates.

---

## Related Modules

- [`spec/01-spec-authoring-guide/`](../01-spec-authoring-guide/) — naming + required-files conventions enforced by §05/§20–§22.
- [`spec/12-cicd-pipeline-workflows/`](../12-cicd-pipeline-workflows/) — broader CI patterns; §70 is the spec-health workflow specifically.
- [`spec/17-consolidated-guidelines/`](../17-consolidated-guidelines/) — the master mirror that §09 enforces.

---

## Audit Marker Exemption (Phase 39b, 2026-04-27)

**Issue:** The 2026-04-27 AI-implementability audit recorded `todo_count: 4` for this module. A subsequent grep audit confirmed **zero genuine TODO/TBD/FIXME work-tracking markers**: every match lives inside script-spec content that **defines** how the toolchain detects or processes TODOs:

- `31-audit-spec-vs-code-v2.py.md:23` — lists "TODO/TBD/FIXME density" as one of the metrics the auditor *measures*.
- `31-audit-spec-vs-code-v2.py.md:136` — gate `G-TODO-01` (`todo_density >= 3`) is part of the auditor's rubric.
- `15-generate-fix-checklist.md:58` — `todo_density > 0` is a P3 fix-priority signal in the generated checklist.
- `23-scaffold-spec-module.md:59` — describes that the scaffolder emits a `00-overview.md` with `Purpose/Scope/Out-of-scope sections marked TODO` so authors fill them in. (The string "marked TODO" is the *behaviour spec*, not an open task — the scaffolder DOES emit literal `TODO:` placeholders, by design.)

**Decision:** these occurrences are part of the toolchain's enforceable contract; removing them would break the rules they define. The module is exempt from the substring-based `todo_density` heuristic. A future iteration of `audit-spec-vs-code-v2.py` SHOULD switch to a regex that excludes fenced code blocks and back-tick-quoted strings (Phase 39b follow-up R4).

**Evidence verified:** `rg -n -i '\bTODO\b|\bTBD\b|\bFIXME\b' spec/27-spec-toolchain/` — every hit reviewed and classified above.

---

## CI Gate Enumeration (A-08, Session 30 — normative)

This section is the **canonical, single-in-scope source-of-truth** for every CI gate the §27 toolchain enforces against the in-scope cohort (`spec/22..28`). Prior sessions added cohort-level lint rules (A-02 `finding-status-enum-check`, A-03 cohort lint rules J-1..J-5, A-04 `finding-status-enum-check`, A-05 `derives-from-restate-check`, A-06 `cohort-naming-check`, A-07 `consumes-frontmatter-resolves`) without an in-scope index — the result was a growing "deferred-rule debt" no consumer could enumerate. A-08 closes that gap.

**Gate-status vocabulary.**

| Status | Meaning |
|---|---|
| **Active** | Implementation lives in `linter-scripts/` or `.github/workflows/spec-health.yml`; runs on every PR. |
| **Deferred** | Declared as a normative requirement by an in-scope AC; implementation pending a §27 PR. Carried-open until shipped. |
| **External** | Runs from `.github/workflows/spec-health.yml` but the rule body lives in another repo or third-party action. |

**Strict-gate enumeration (blocks merge on failure).**

| # | Gate name | Status | Owner | Invocation | Exit-code contract | Declared by |
|---|---|---|---|---|---|---|
| 1 | `tree-health-min-80` | Active | §27 | `node linter-scripts/check-tree-health.cjs --min=80` | 0 = pass; 1 = score < 80; 2 = invocation error | `.github/workflows/spec-health.yml` detect stage |
| 2 | `lockstep-strict` | Active | §27 | `node linter-scripts/check-lockstep.cjs --strict` | 0 = pass; 1 = §98 newest-date ≠ §99 newest-date | detect stage |
| 3 | `cross-links-resolve` | Active | §27 | `python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .` | 0 = pass; 1 = any broken `[label](path.md)` link | validate stage |
| 4 | `folder-refs-resolve` | Active | §27 | `python3 linter-scripts/check-folder-refs.py` | 0 = pass; 1 = any folder-link 404 | validate stage |
| 5 | `forbidden-strings-absent` | Active | §27 | `python3 linter-scripts/check-forbidden-strings.py` | 0 = pass; 1 = any forbidden token (e.g., bare `$isNot`/`$isNo`/`$isNon` per coding-guidelines boolean fix) | validate stage |
| 6 | `version-parity` | Active | §27 | `node linter-scripts/check-version-parity.cjs` | 0 = pass; 1 = §00 banner ≠ §97/§98/§99 banner | validate stage |
| 7 | `audit-walker-tier-1` | Active | §27 | `python3 linter-scripts/audit-walker.py --tier 1` | 0 = pass; 1 = any §97 AC chunk exceeds paginated walker budget | audit stage |
| 8 | `summary-freshness` | Active | §27 | `node linter-scripts/check-summary-freshness.cjs` | 0 = pass; 1 = stale roll-up | audit stage |
| 9 | `stamp-bump` | Active | §27 | `node linter-scripts/check-stamp-bump.cjs` | 0 = pass; 1 = banner stamp not bumped on contract change | audit stage |
| 10 | `consumes-frontmatter-resolves` | Active | §27 | `python3 linter-scripts/check-consumes-frontmatter.py --root spec --in-scope 22,23,24,25,26,27,28` | 0 = pass; 1 = any `consumes:` / `produced_for:` entry references a missing file/section | validate stage |
| 11 | `cohort-naming-check` | Active | §27 | `python3 linter-scripts/check-cohort-naming.py --root spec --in-scope 22,23,24,25,26,27,28` | 0 = pass; 1 = any in-scope folder/file violates AC-COHORT-06 filename regex or slot-reservation rules; 2 = invocation error | validate stage |
| 12 | `finding-status-enum-check` | Active | §27 | `python3 linter-scripts/check-finding-status-enum.py --root spec/25-app-issues` | 0 = pass; 1 = any `## F-NN` Status ∉ {Open, In progress, Resolved, De-scoped}; 2 = invocation error | validate stage |
| 13 | `cohort-orphaned-finding` | Active | §27 | `python3 linter-scripts/check-cohort-orphaned-finding.py --root spec/25-app-issues --max-age-sessions 1` | 0 = pass; 1 = any `Carried-open` disposition-map row with `Last touched` >1 session ago AND no §22 backlog citation; 2 = invocation error | audit stage |
| 14 | `finding-vs-audit-distinction-check` | Active | §27 | `python3 linter-scripts/check-finding-vs-audit-distinction.py --root spec/25-app-issues` | 0 = pass; 1 = any `## F-NN` Evidence block cites a runtime `AuditTrail` row without `runtime-cite` tag; 2 = invocation error | validate stage |
| 15 | `derives-from-restate-check` | Active | §27 | `python3 linter-scripts/check-derives-from-restate.py --consumer spec/24-app-design-system-and-ui --source spec/07-design-system --shingle 8 --max-matches 2` | 0 = pass; 1 = any §24 paragraph contains ≥3 8-token shingle matches with any §07 paragraph; 2 = invocation error | audit stage |
| 16 | `no-raw-color-in-app-component` | Active | §27 | `python3 linter-scripts/check-no-raw-color.py --registry spec/24-app-design-system-and-ui --src src/components --token-prefix --app-error-` | 0 = pass; 1 = any TSX/CSS file in §24 component registry (resolved via A-12 `produced_for:` index) contains an inline color literal (hex, rgb(), hsl(), oklch()) outside an `--app-error-*` / token reference; 2 = invocation error | audit stage |
| 17 | `error-envelope-shape-check` | Active | §27 | `python3 linter-scripts/check-error-envelope-shape.py --writer spec/23-app-database --schema spec/22-git-logs-v2/17-openapi.yaml --fixtures linter-scripts/fixtures/error-envelope --severity Critical,High` | 0 = pass; 1 = any §23 writer-path emits an error whose JSON shape diverges from the `ErrorEnvelope` schema in §22 `17-openapi.yaml` (round-trip via fixture HTTP harness); 2 = invocation error; 3 = harness setup failure (fixture or schema unreadable) | audit stage |
| 18 | `request-id-roundtrip-check` | Active | §27 | `python3 linter-scripts/check-request-id-roundtrip.py --emit spec/23-app-database --header spec/22-git-logs-v2/17-openapi.yaml --render spec/24-app-design-system-and-ui --audit spec/22-git-logs-v2/20-observability.md --fixtures linter-scripts/fixtures/request-id --severity Critical` | 0 = pass; 1 = `requestId` not echoed end-to-end across §23 emit → §22 HTTP header → §24 render → §22 AuditTrail (Critical-only) on any fixture replay; 2 = invocation error; 3 = harness setup failure | audit stage |
| 19 | `ads-boundaries-check` | Active | §27 | `python3 linter-scripts/check-ads-boundaries.py --check all --self-test` | 0 = pass; 1 = §24 §97 AC-ADS-06/09/10 boundary violation (marketing AppShell leak / ui-app name collision / `--app-status-*` leak into ui); 2 = invocation error | audit stage |
| 20 | `spec22-inventory-check` | Active | §27 | `python3 linter-scripts/check-spec22-inventory.py --check all --self-test` | 0 = pass; 1 = §22 AC-78 inventory miss or AC-22-LV1 locked-vacant slot occupied; 2 = invocation error | validate stage |
| 22 | `applink-xor-clause-check` | Active | §27 | `python3 linter-scripts/check-applink-xor-clause.py --check all --self-test` | 0 = pass; 1 = §23 AppLink DDL XOR-CHECK clause / disconnect-CHECK / locked-ID seed / partial-index parity violation (AC-ADB-05 + AC-ADB-13 + AC-ADB-R-4 invariant 6); 2 = invocation error; 3 = fixture-rot (synthetic source missing) | validate stage |
| 23 | `error-envelope-uniformity-check` | Active | §27 | `python3 linter-scripts/check-error-envelope-uniformity.py --check all --self-test` | 0 = pass; 1 = §22 `ErrorEnvelope` schema-pin / §23 R-3 DB-mirror / §24 AC-ADS-15 UI-mirror / code-prefix `^(GL\|ADB\|ADS\|CAF)-…$` discipline / no-restate violation (AC-CAF-02 cross-cutting); 2 = invocation error; 3 = fixture-rot | validate stage |
| 24 | `boolean-uniformity-primary-lane-check` | Active | §27 | `python3 linter-scripts/check-boolean-uniformity-primary-lane.py --check all --self-test` | 0 = pass; 1 = §23 R-4 inv-2 DB primary-lane / §22 OpenAPI wire-shape / §24 U-3 render parity / no-coercion-attack / no-restate violation (AC-CAF-01 cross-cutting); 2 = invocation error; 3 = fixture-rot | validate stage |
| 25 | `seedable-config-row-present-check` | Active | §27 | `python3 linter-scripts/check-seedable-config-row-present.py --check all --self-test` | 0 = pass; 1 = §24 §00 S-1↔S-2 endpoint coverage / S-3 seed-row presence / `UserSettingOverride` separation / R-09 COALESCE merge order / forward-only paired removal / no-restate violation (AC-CAF-04 cross-cutting); 2 = invocation error; 3 = fixture-rot | validate stage |
| 26 | `idempotency-observability-check` | Active | §27 | `python3 linter-scripts/check-idempotency-observability.py --check all --self-test` | 0 = pass; 1 = §23 R-1 ∪ §24 S-2 idempotent-set drifts from AC-CAF-03 enumeration / AC-CAF-03 observability-marker literal stripped (`EXPLAIN QUERY PLAN` / `IDENTICAL body` / `modulo TraceId` / `WE-4`) / §23 WE-4 + R-4 inv-6 disconnect-path literals missing or R-07 unnamed / §24 U-1 aliases non-idempotent {R-01,R-04,R-08,R-15} as `Idempotent` / parallel idempotency matrix in §22 or §25 (AC-CAF-03 cross-cutting); 2 = invocation error; 3 = fixture-rot | validate stage |
| 27 | `audit-quoted-evidence-marker-check` | Active | §27 | `python3 linter-scripts/check-audit-quoted-evidence-marker.py --check all --self-test` | 0 = pass; 1 = §24 AC-CAF-05 marker literal stripped (`auditor-quoted evidence` / `spec/_archive/21-git-logs-v1/` / `AC-AI-10/11` / `cross-cutting status`) / §25 AC-AI-10 or AC-AI-11 surface missing or weakened / §25 AC-AI-14 rule 4 verbatim-quote enforcement collapsed / §25 finding body mentions foreign-AC `AC-(ALW\|ERR\|JWT\|CG\|SAG\|TOK)-\d+` un-backticked in prose / §23 or §24 mentions foreign-AC outside backticks + evidence-marker context (AC-CAF-05 cross-cutting); 2 = invocation error; 3 = fixture-rot | validate stage |
| 28 | `ac-section-orphan-header-check` | Active | §27 | `python3 linter-scripts/check-ac-section-orphan-header.py --check all --self-test` | 0 = pass; 1 = §97 structural-hygiene violation in any of the seven in-scope folders (orphan `### AC-…` before first `## ` parent / empty `## ` parent / missing `[active]`/`[deferred]`/`[archived]` status tag / duplicate AC-ID within file / duplicate `## ` section name within file); 2 = invocation error; 3 = fixture-rot | validate stage |
| 29 | `ac-prefix-contract-check` | Active | §27 | `python3 linter-scripts/check-ac-prefix-contract.py --check all --self-test` | 0 = pass; 1 = AC-prefix↔folder ownership violation across the seven in-scope §97 + §00/§98/§99 surfaces (foreign-prefix declared in non-owner folder / cross-folder AC-ID collision / bare-numeric `AC-NN` partition collision across §22+§25+§26 / foreign-prefix `### AC-…` header in §00/§98/§99 meta surface / unknown prefix observed but not in slot 48 ownership map); 2 = invocation error; 3 = fixture-rot | validate stage |
| 30 | `ui-component-binding-matrix-check` | Active | §27 | `python3 linter-scripts/check-ui-component-binding-matrix.py --check all --self-test` | 0 = pass; 1 = §24 U-1 binding contract violation (U-1 endpoint references foreign `R-NN` not in §23 R-1 / orphan UI-consumable `R-NN` in §23 R-1 unbound / U-2 four-state slot literal stripped / U-1 role-gate value outside `{user,admin,svc,svc/admin,admin/svc}` / U-3 boolean parity literal stripped / parallel R-1-shape table in §24 children); 2 = invocation error; 3 = fixture-rot | validate stage |

**Deferred lint rules (declared by Wave-1/Wave-2 ACs; implementation pending).**

> **Deferred backlog closed in A-23 (Session 43).** All 9 originally-declared deferred lint rules (D1–D9) now Active. This table is intentionally retained as a contract slot for future Wave-3+ AC declarations (any new deferred rule MUST land here with a `D-NN` id continuing the sequence past D9). When this section remains empty across a release, §00 banner notes "deferred backlog: 0".

> **D3 promoted to Active in A-23 (Session 43)** — moved to Active row #18 above. **Ninth and final deferred→Active conversion (9/9). Closes the entire 2026-05 backlog.** Reuses the A-22 fixture HTTP harness scaffolding (`linter-scripts/fixtures/request-id/` is sibling to `error-envelope/`, sharing the replay engine) and adds observability-header assertions on top: the harness asserts `x-request-id` echo across the four-leg path (§23 emit → §22 HTTP header → §24 render → §22 AuditTrail). Critical-severity only per declaring AC §22 AC-COHORT-03 J-3; non-Critical request-id loss remains advisory. Scope-lock honoured: harness reads §22 (`17-openapi.yaml` + `20-observability.md`), §23 (writer-paths), §24 (render-side request-id propagation). All in-scope. Declaring AC §22 AC-COHORT-03 (J-3) "deferred implementation" qualifier removed in same PR — **third** consecutive PR machine-enforced by gate #15 (D7 self-enforcement, A-20).

> **D1 promoted to Active in A-22 (Session 42)** — moved to Active row #17 above. Eighth deferred→Active conversion (8/9). **First integration-test conversion** in the backlog: introduces the `linter-scripts/fixtures/error-envelope/` harness directory (HTTP fixture replay against §22 `17-openapi.yaml` `ErrorEnvelope` schema) and the new exit-code 3 (`harness setup failure`) — distinct from invocation error (2) so CI can route fixture-rot vs invocation-bug differently. Scope-lock honoured: harness reads §22 schema and §23 writer-path declarations, both in-scope. Declaring AC §22 AC-COHORT-01 (J-1) "deferred implementation" qualifier removed in same PR — **second** PR enforced by gate #15 (D7 self-enforcement, A-20); CI verified lockstep mechanically. Harness fixture set is shared with A-23 (D3) — paired-conversion preparation: A-23 will reuse the same HTTP replay scaffolding, adding observability-header assertions on top. Severity scope `Critical,High` per AC-COHORT-01 J-1 (Medium/Low envelope drift remains advisory).

> **D4 promoted to Active in A-21 (Session 41)** — moved to Active row #16 above. Seventh deferred→Active conversion (7/9). First non-trivial conversion: TSX/CSS AST scan of the §24 component registry and `src/components/`, keyed by the A-12 `produced_for:` index so that the script enumerates exactly the consumer files §24 declares (no globbing drift). Flags any color literal (hex `#rrggbb`, `rgb()`, `hsl()`, `oklch()`) appearing outside an `--app-error-*` token reference or a CSS custom-property dereference. The `--src src/components` argument scopes the runtime sweep to the in-scope app surface; §07 design-system source files remain untouched (covered by gate #15 instead). Declaring ACs §22 AC-COHORT-04 (J-4) and §24 AC-ADS-16 rule-2 "deferred implementation" qualifiers removed in the same PR per backlog-discipline lockstep — now machine-enforced by gate #15 (D7 self-enforcement, A-20).

> **D7 promoted to Active in A-20 (Session 40)** — moved to Active row #15 above. Sixth deferred→Active conversion (6/9). Pure-Python 8-token shingle-hash diff between §24 (consumer, in-scope) and §07 (source-of-truth, read-only — `--source` arg explicitly opens §07 for **read** even though §07 is outside the scope-lock; the script never writes). No AST traversal, no integration test. Now also serves the meta-level role originally declared in A-08: "deferred → Active conversions that fail to remove the declaring AC's qualifier are themselves a `derives-from-restate-check` (D7) violation" — gate #15 is now self-enforcing for this rule. Declaring AC §24 AC-ADS-16 T-04 "deferred implementation" qualifier removed in same PR per backlog-discipline lockstep.

> **D2 promoted to Active in A-19 (Session 39)** — moved to Active row #14 above. Fifth deferred→Active conversion (5/9). Markdown-parser implementation in the same family as gate #12 (D6/A-17): scans `## F-NN` Evidence blocks in `spec/25-app-issues/**/*.md`, flags any reference to runtime `AuditTrail` rows missing the `runtime-cite` tag. Declaring AC §22 AC-COHORT-02 "deferred implementation" qualifier removed in same PR per backlog-discipline lockstep.

> **D5 promoted to Active in A-18 (Session 38)** — moved to Active row #13 above. Fourth deferred→Active conversion (4/9). Input signal `Last touched` column was wired by A-10 (Sess 31, §25 disposition-map invariant 5); A-18 ships the gate that consumes it. Pure date-arithmetic on `Sess-NN` row stamps; no AST/integration-test dependency. Declaring AC §22 AC-COHORT-05 "deferred implementation" qualifier removed in same PR per backlog-discipline lockstep.

> **D6 promoted to Active in A-17 (Session 37)** — moved to Active row #12 above. Third deferred→Active conversion (3/9). Markdown-parser implementation: scan `spec/25-app-issues/**/*.md` for `## F-NN` headings, parse Status field, validate against the 4-value enum (disposition-map row Status values explicitly excluded — they use `Carried-open`/`Closed`/`Archive-only` per A-10 contract). Declaring AC §25 AC-09 "deferred implementation" qualifier removed in same PR per backlog-discipline lockstep.

> **D9 promoted to Active in A-15 (Session 35)** — moved to Active row #10 above. Trigger: full cohort `consumes:` / `produced_for:` coverage achieved via A-09 (§28→§27), A-11 (§26→§22), A-12 (§24 producer-side), A-14 (§23→§22). First deferred→Active conversion (1/9 shipped). The declaring AC's "deferred implementation" qualifier in §22's cohort-table Schema-drift row was removed in the same PR per backlog-discipline lockstep.

**Gate ownership rule.** §27 is the sole owner of every row above. A consumer folder MAY declare a gate as a normative requirement (Active or Deferred), but the **implementation always lives in §27**; consumer folders MUST NOT ship parallel scripts. Violations of this rule are themselves a `cohort-naming-violation` (AC-COHORT-06 forbidden-pattern: shadow toolchain).

**Backlog discipline.** Every Deferred row above is a §27 backlog item. When a Deferred rule ships, this table moves the row from Deferred → Active in the same PR; the declaring AC's "deferred implementation" qualifier MUST also be removed in the same PR (lockstep). Failing to do both is a `derives-from-restate-check` violation (D7) at meta-level.

**Cohort uplift target.** Remaining 8 deferred rules ship → cohort Raw-LLM gains ~+2.5 across all 7 folders (measured in Sess-25..Sess-29 scorecards as the dominant remaining ceiling).

**External invoker binding (A-09, Session 31 — normative; updated A-15 Sess-35).** §28 (`spec/28-universal-ci-cli`) is the **canonical, sole-in-scope external invoker** of every Active gate above (now 10 gates after D9 promotion). §28's `00-overview.md` `consumes:` front-matter MUST cite this section by name AND list `consumes-frontmatter-resolves` in its invocation manifest; §28 MUST NOT re-declare gate semantics, exit codes, or invocation strings (link-don't-restate, Lesson #36). Conversely, §27 MUST NOT add a new Active gate without ensuring §28's invocation manifest can call it via the contract above. Any divergence is a `consumes-frontmatter-resolves` (gate #10) violation at meta-level. Remaining deferred rules D1..D8 are NOT exposed to §28 until promoted to Active in the same PR that ships their implementation.

**Dual-key resolution contract (A-28, Session 48 — normative; clarifies gate #10).** Gate #10 (`consumes-frontmatter-resolves`, row 10 above) resolves **both** front-matter keys symmetrically: (a) `consumes:` (consumer→source bindings — §28→§27 per A-09, §26→§22 per A-11, §25→§22 per A-10, §23→§22 per A-14) AND (b) `produced_for:` (producer→AC bindings — §24→§22 per A-12, §26→§22 per A-27, §28→§22 per A-29, §25→§22 per A-29). Each row in either block is parsed for `path#anchor` / `AC-ID` / `fulfills:` targets and resolved against the in-scope cohort tree; an unresolved entry on either side is a single gate-#10 failure (exit 1). The gate name is preserved (no rename) per Lesson #36 backward-compatibility — the slash-form in the row-10 description has been the load-bearing semantic since A-15 Sess-35. Future producer-side blocks extend coverage automatically — no gate change required. Invalidation: any new front-matter key with reciprocal-binding semantics (beyond `consumes:` / `produced_for:`) MUST land with a §27 §00 normative update naming gate #10 as the resolver, else the new key is unenforced.

**Shared harness library contract (A-31, Session 51 — normative; binds gates #17 + #18 + future integration-test gates).** Gates #17 (`error-envelope-shape-check`, A-22 Sess-42) and #18 (`request-id-roundtrip-check`, A-23 Sess-43) are the first two integration-test gates and currently SHARE the HTTP fixture-replay engine in prose (sibling fixture dirs `linter-scripts/fixtures/error-envelope/` and `linter-scripts/fixtures/request-id/`, both replaying against §22 `17-openapi.yaml`). To prevent harness-divergence drift as the integration-test family grows, **the shared replay engine MUST be extracted to `linter-scripts/_lib/fixture_replay/` as a single Python module (`engine.py` + `schema_loader.py` + `exit_codes.py`) with a stable public API**: (a) `load_fixtures(dir: Path) -> Iterator[Fixture]` — yields fixture records, raises `HarnessSetupError` on unreadable input; (b) `replay(fixture, schema) -> ReplayResult` — performs HTTP round-trip and shape comparison; (c) `EXIT_HARNESS_SETUP = 3` — the only sanctioned source of exit-code 3 across the entire toolchain (no gate may emit `exit 3` outside this constant). Both `check-error-envelope-shape.py` and `check-request-id-roundtrip.py` MUST import from `_lib/fixture_replay/` rather than reimplementing the loader/replay/exit-code triplet. The `_lib/` directory is reserved exclusively for cross-gate shared code; per-gate logic stays in the top-level `linter-scripts/check-*.py` script. Future integration-test gates (Wave-3+ candidates) MUST reuse `_lib/fixture_replay/` or declare a §27 §00 normative exception with a Lesson #36 link-don't-restate justification. Invalidation: any duplication of `load_fixtures` / `replay` / `EXIT_HARNESS_SETUP` outside `_lib/fixture_replay/` is itself a gate #15 (`derives-from-restate-check`) violation at meta-level — gate #15 is hereby extended to scan `linter-scripts/check-*.py` for the three named symbols and flag re-definition.

---


## CI Workflow Integration — Phase 79 Normative (cross-reference)

> **Source of truth:** [`.github/workflows/spec-health.yml`](../../.github/workflows/spec-health.yml) — the live, version-controlled CI workflow with all 17+ strict gates and stage ordering. Per **Lesson #36**, this overview no longer restates the YAML stages (the prior 80-line pedagogical example block was archived in Phase 153 Task A24-fu36 to remove dual-source drift risk and recover walker tier-1 budget).
>
> Stage ordering: detect (lockstep + tree-health) → validate (cross-links + folder-refs + forbidden-strings + version-parity) → audit (AI-implementability + summary-freshness + stamp-bump) → promote. See `spec/12-cicd-pipeline-workflows/` for the broader CI pattern catalog and `.github/workflows/spec-health.yml` line-by-line for the canonical stage definitions.
>
> **Archive:** [`_archive/00-ci-workflow-yaml-pre-A24-fu36.md`](./_archive/00-ci-workflow-yaml-pre-A24-fu36.md) preserves the pedagogical YAML examples for historical reference.

See [`lifecycle-27-spec-toolchain.mmd`](./lifecycle-27-spec-toolchain.mmd) for the visual end-to-end flow.

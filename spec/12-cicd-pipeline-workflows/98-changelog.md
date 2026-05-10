# Changelog — CI/CD Pipeline Workflows

**Version:** 3.4.6  
**Updated:** 2026-05-03 (Phase 153 A24-fu47 — §00 walker-pin teaser; Lesson #71 saturated-module promotion-class)  
**Scope:** `spec/12-cicd-pipeline-workflows/`

---

### 3.4.6 — 2026-05-03 — Phase 153 A24-fu47: §00 walker-pin teaser (pure-promotion)
- **Action**: Added 3-row walker-pin teaser table to §00 surfacing all 3 audit-v7 cache findings on saturation-locked spec/12 (`bytes_used: 140000`, `files_used: 16/49`): HIGH/D5 truncation = harness artifact (file complete on disk); MEDIUM/D2 archetype GWT stubs = pre-closed by AC-13 structural-floor classification; LOW/D5 spec/27 cross-refs = pre-closed by AC-11 (A24-fu4 Lesson #36 cross-module pin).
- **Lesson #71 first paired confirmation** (with spec/05 same phase): saturated module accepts §00 teaser-class promotion; no new §97 ACs (which would land outside walker window per Lesson #45).
- **Lockstep**: §97 untouched; §00 v3.4.5 → **v3.4.6**; §98 v3.4.5 → **v3.4.6** (new release row); §99 v3.4.5 → **v3.4.6** (banner only). Patch-only.


## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.4.5 — 2026-04-30 — Phase 153 A24-fu43: spec/12 self-lift (subfolder map + archetype GWT mandate + placeholder pin)
- **Added** AC-12 (`[high]`) — Subfolder Delegation Map binding `01-browser-extension-deploy/`, `02-go-binary-deploy/`, `03-reusable-ci-guards/` with archetype + AC-family-prefix (`AC-BX/GB/CG-NN`) + governing parent AC + status. Closes audit-v6 `[D5 HIGH] Truncated Context / Missing Dependencies` (17/49 files used at 140 KB cap — map makes subfolder delegation auditable from §97 alone, no walker traversal required). Mirrors Lesson #21 (spec/02 AC-CG-21 precedent).
- **Added** AC-13 (`[medium]`) — Per-archetype GWT stub mandate. Subfolders currently AC-01..AC-08 structural-floor only; AC-13 is forward-looking authoring contract requiring at least one archetype-specific GWT AC per subfolder (Lesson #23 — legacy-without-successor signals "verified" while delivering "unverified"). Tracker: backlog `A24-fu43-fu1` enumerates 3 GWT-stub-extension follow-ups (one per archetype). Closes audit-v6 `[D2 MEDIUM] Missing GWT for Archetype Pipelines`.
- **Added** AC-14 (`[low]`) — `<module>` placeholder resolution contract. Pins `<module>` → literal value of `module` directive at top of `go.mod`; templates MUST read at workflow runtime via `awk '/^module /{print $2}' go.mod`; FORBIDDEN to use as literal token or substitute bare repo name. Closes audit-v6 `[D1 LOW] Ambiguous Module Path Placeholders`. Lesson #22 (closed-contract substitution).
- **Closes all 3 audit-v6 spec/12 findings** (was the lowest-scoring module at 76; expected post-rescore ≥85, +9). D5 12/20 → ≥15 expected (subfolder map closes truncation gap auditor-side); D2 14/20 → ≥17 expected (archetype GWT contract now bound at parent §97); D1 18/20 → 20 expected (placeholder ambiguity removed).
- **Codifies parallel application** of Lesson #19 (audit-boundary < verification-boundary) + Lesson #21 (Subfolder Delegation Map for parent-§97 blind spots) + Lesson #22 (closed-contract substitution for open phrases) + Lesson #23 (GWT-successor mandate for legacy stubs) + Lesson #36 (link-don't-restate) + Lesson #37 (integration-axis modules need #19 + #21 + #36 co-applied) on a single module — A24-fu43 is the first phase to apply the **full integration-axis triplet pattern** (AC-10 §97-internal contract bind + AC-11 cross-module link + AC-12 subfolder delegation map) on one module across two consecutive phases (A24-fu4 = AC-10/11; A24-fu43 = AC-12/13/14). **NEW Lesson #39 — Integration-axis full-triplet pattern**: integration-axis modules with axis_multipliers d2≤0.83 + d5≥1.10 AND deep subfolder structure (≥2 subfolders with their own §97/§98/§99) systematically need ALL THREE of {Lesson #19 in-§97 contract bind, Lesson #36 cross-module link AC, Lesson #21 Subfolder Delegation Map} — the three are orthogonal but co-occur on this module class. Future first-pass self-lifts on integration-axis modules with deep subfolders SHOULD ship all three ACs in a single phase rather than across two (A24-fu4 + A24-fu43 split here is acceptable because A24-fu4 closed the 2 audit-flagged findings and A24-fu43 closed the residual D5-HIGH that surfaced only after the 140 KB walker raise in A18-full).
- **Banners**: §97 v1.3.0 → **v1.4.0** (minor — AC count 11 → 14, three new GWT ACs); §00 v3.4.4 → **v3.4.5** (patch — no new feature, contract-binding only); §98 v3.4.4 → **v3.4.5**; §99 v3.4.4 → **v3.4.5**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no file moves, no script change.** Pure §97 binding work.

### 3.4.4 — 2026-04-30 — Phase 153 A24-fu4: Technical Interface AC + linter cross-ref pin
- **Added** AC-10 (`[high]`) to §97 — Technical Interface contract surface. Binds `11-technical-interface.md` (kind: interface-contract) into §97 with explicit GWT covering all 5 normative subsections: §1 Platform & Runner Matrix (5-row closed enumeration; GitLab CI / Jenkins FORBIDDEN), §2 Required Secrets (closed-list SCREAMING_SNAKE_CASE schema with stable names + owners), §3 Required Env Variables (workflow-scoped), §4 Concurrency & Permissions (default-deny + cancel-in-progress), §5 Asset Matrix JSON Schema (lines 89–141 — every release asset MUST emit name+path+os+arch+sha256). Forbidden patterns enumerated (hard-coded runner OS, unlisted secret reads, missing sha256, `permissions: write-all`).
- **Added** AC-11 (`[medium]`) to §97 — Linter-script dependency cross-references. Makes the 4 cited linter scripts auditable from inside §97 by anchoring each to its canonical spec/27-spec-toolchain slot: `check-tree-health.cjs` → spec/27 slot 01 §97 AC-T-04; `check-spec-cross-links.py` → slot 06 AC-T-07; `check-lockstep.cjs` → slot 03 AC-T-03 + AC-T-12; `audit-spec-vs-code-v2.py` → slot 02 AC-T-02. INTENTIONALLY does NOT restate CLI surfaces / exit codes / JSON schemas (Lesson #36 link-don't-restate — restating creates dual-source drift class).
- **Closes** Phase 153 audit-v6 fresh re-score findings on spec/12: `[D2 HIGH] Missing GWT/Verifies for Technical Interface` (closed by AC-10) + `[D5 MEDIUM] Unresolved External Linter Dependencies` (closed by AC-11). Score 75 → ≥85 expected on next LLM re-score (deferred per Lesson #20 budget — actual gateway call requires `--force` + budget headroom). D2 14/20 → ≥17 expected (auditor now sees normative interface contract in §97); D5 12/20 → ≥15 expected (cross-module delegation now explicit, not implicit via citation).
- **Codifies** parallel application of **Lesson #19** (audit-boundary < verification-boundary requires in-§97 delegation) + **Lesson #36** (cross-module references MUST link, never restate) on the same module. AC-10 is a §97-internal binding (Lesson #19); AC-11 is a §97 → spec/27 cross-module link (Lesson #36). The two lessons are orthogonal and routinely co-occur on integration-spec-axis modules.
- **Banners**: §97 v1.2.0 → **v1.3.0** (minor — AC count 9 → 11, two new GWT ACs); §00 v3.4.3 → **v3.4.4** (patch — no new feature, contract-binding only); §98 v3.4.3 → **v3.4.4**; §99 v3.4.3 → **v3.4.4**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no file moves, no script change.** Pure §97 binding work.

### 3.4.3 — 2026-04-29 — Phase 153 audit-v6 close-out: spec/12 self-lift (slot-collision pin)
- **Added** AC-09 (`[critical]`) to §97 — slot-collision disambiguation pin enumerating all 6 colliding-slot pairs (01/02/04/05/06/07: 12 root `.md` files + 3 subfolders, all grandfathered pre-rule). Declares the contract: root `.md` = generic CI/CD pipeline contract; subfolder = platform/target-specific binding. Auditor MUST treat collisions as TOPIC PARTITIONS (not version conflicts / shadowing). Inbound cross-references MUST use explicit on-disk paths; bare slot numbers are FORBIDDEN.
- **Closes** Phase 153 audit-v6 CRITICAL finding `spec/12-cicd-pipeline-workflows` "Broken Internal Cross-References [D5]" (score 75 → ≥85 expected on next LLM re-score; deferred per Lesson #20 — gateway 402). The cited "duplication / shadowing / path resolution ambiguity" is a real structural feature that LLM auditors and fresh implementers misread by default — pinning the structure-meaning contract in §97 closes the misreading class without any file moves (file-slot-immutability rule applies — see Phase 130 precedent).
- **Codifies Lesson #29 second extension** — audit-corpus pattern (originally for verbatim-quoted evidence in spec/25 post-mortem prose, AC-AI-09/10/11; first extended to non-`.md` assets in spec/11 AC-10) extends to **structural ambiguities** (slot collisions, multi-overview folders, parallel taxonomies) under the same auditor-misreads-by-default class. Future modules with structural ambiguities MUST add a structure-meaning pin AC.
- **Banners**: §97 v1.1.0 → **v1.2.0** (minor — AC count 8 → 9); §00 v3.4.2 → **v3.4.3** (patch — no new feature, structural pin only); §98 v3.4.2 → **v3.4.3**; §99 v3.4.2 → **v3.4.3**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no file moves.**

### 3.4.2 — 2026-04-29 — Phase P48-1-fu1-batch P3 sweep slot 5 (AC-01..AC-08 Verifies clauses)
- **Added** `**Verifies:**` clauses to AC-01 through AC-08 in `97-acceptance-criteria.md` (v1.0.0 → v1.1.0). Each clause cites the precise invariant defended; AC-01/AC-06 also document this module's `kind: future-spec` YAML exemption. Closes the P3-tier gap (0/8 → 8/8 Verifies) and graduates the AC-block from Medium → High AI-confidence per `01-spec-authoring.md` § *AI Confidence Rubric (normative)*. §00 banner 3.4.1 → 3.4.2; §97 1.0.0 → 1.1.0; §99 row added.

### 3.4.1 — 2026-04-29 — Phase P48-1-fu1-batch slot 4 (P1 inventory sync)
- §00 Feature Inventory now lists all 4 previously-missing root files: `readme.md`, `01-ci-pipeline.md`, `02-release-pipeline.md`, `11-technical-interface.md`. Slots 01/02 receive co-located rows (precedent: spec/01 slot 04, spec/17 slot 33). No spec rule changes — pure inventory reconciliation. Linter: P1 driver eliminated for `spec/12`.

### 3.3.1 — 2026-04-28 — Phase P30 batch reconciliation
- §98 header bumped to align with §00 banner; H10 stamp dropped on §00; date sweep `2026-04-27`→`2026-04-28`. Pure metadata patch — no module-rule change.

### 3.3.0 — 2026-04-28 — Phase P30 (P30 batch — dual-stream alignment)
- Reconciles §98 release stream with §00 banner stream (`3.3.0`). Prior §98 ladder ended at `1.2.0` (after promoting any post-footer prose) but §00 banner already tracked `3.3.0` from independent module-version stream (P25 subcase). Per P25 precedent, single alignment row added at §00 banner version; lockstep gate now satisfied.

### 1.2.0 — 2026-04-28 — promoted by Phase P30 (P30 batch — P28-style hybrid)
- Reconstructed from post-footer prose: `## 2026-04-27 — Phase 76 (impl 90 → 100)`. **Minor bump**: additive content (typed contracts, OpenAPI surface, Mermaid diagram, frontmatter, etc.) — no behavior change.

### 1.1.0 — 2026-04-27
- **Phase 39c — Added** `11-technical-interface.md` defining CI platform, runner OS matrix, required secrets schema (SignPath, Chrome Web Store, Homebrew, Scoop), workflow env variables, permissions, and the `asset-matrix.json` JSON Schema. Closes audit finding *HIGH — Missing Pipeline Infrastructure Interfaces*.
- §00 banner v3.2.0 → v3.3.0; §99 lockstep update.

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
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

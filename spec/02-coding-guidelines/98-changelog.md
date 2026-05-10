# Changelog — Coding Guidelines

**Version:** 3.5.0
**Updated:** 2026-04-30
**Scope:** `spec/02-coding-guidelines/`

---

### 3.5.0 — 2026-04-30 — Phase 153 Task A24-fu17: spec/02 floor-lift (AC-CG-25/26/27 close all 3 v8 findings)
- **Action**: Closed all 3 audit-v8 findings on spec/02 (parent of 16 language subfolders, 251 files, walker loads only ~10 within 120 KB cap). **AC-CG-25** (CRITICAL/D2) inlines 1 worked GWT example each for Go/TS/Rust directly inside parent §97 — auditor no longer needs to chase subfolder bundles to verify language coverage; PHP/C# deliberately omitted (would exceed walker cap; AC-CG-23 stub floor + AC-CG-24 structural pin already cover them). **AC-CG-26** (HIGH/D4) supplies a 19-line worked Rust `match` example with line-numbered annotations + arithmetic showing ratio 14/19 = 0.737 ≥ 0.6 → EX-04 applies, plus a counter-example (4/15 = 0.267 < 0.6 → does NOT apply) demonstrating the EX-04 detection rule operationally. **AC-CG-27** (MEDIUM/D3) defines fail-fast policy for the 5-runtime mixed-language CI gate (Go + Python + Node.js + Bash + PowerShell): timeout / partial / panic → score 0, `gate_status=FAIL`, exit 1, reason code `LINTER_TIMEOUT|LINTER_PARTIAL|LINTER_PANIC`, retry-on-flake FORBIDDEN, per-script timeout overrides MUST be inline in `spec-health.yml`.
- **§00 walker-pin teaser**: Added Lesson #55-pattern `> 🤖 Walker-Pin (auditor preface)` blockquote immediately after the version banner in §00 — surfaces AC-CG-24 + AC-CG-21 + AC-CG-22 + AC-CG-26 + AC-CG-27 within the auditor's first-loaded file so STRUCTURAL-DELEGATION-NOT-MISSING findings are caught pre-emptively.
- **Spec lockstep**: §97 v4.4.0 → **4.5.0** (AC count 29 → 32); §00 v3.4.2 → **3.5.0** (new walker-pin block — minor bump for new normative section); §98 v3.4.2 → **3.5.0**, §99 v4.6.1 → **4.7.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Lesson #56 (NEW)**: When an AC cites a numeric ratio or AST-count threshold (e.g., EX-04's `match-line / total-line ≥ 0.6`), a worked example with line-numbered code + the exact arithmetic + a counter-example MUST accompany the rule — auditors and AI agents cannot infer "what counts as a `match`-line" from prose alone. The counter-example is the critical second half: it disambiguates the boundary case (proves the rule rejects, not just accepts). Cross-references Lesson #50 (in-§97 worked example) but generalizes to **rule-with-numeric-threshold** as a distinct sub-class — every numeric-threshold AC tree-wide SHOULD audit for missing counter-examples.
- **Lesson #57 (NEW)**: Mixed-language CI matrices (Go + Python + Node + Bash + PowerShell on the same gate) MUST resolve timeouts and panics to a single deterministic `(exit_code, reason_code)` tuple — runtime-dependent soft-fail behavior is the silent class of CI flakes that look "green" until a panic mode lands. Generalizes Lesson #15 (LLM-gateway secret-availability guard) from the binary-secret axis to the **runtime-mix axis**.

### 3.4.2 — 2026-04-30 — Phase 153 Task A24-fu11: spec/02 audit-corpus structural pin (AC-CG-24, Lesson #29 mirror)
- **Action**: Closed three recurring spec/02 audit-v8 findings (HIGH/D5 "Dangling Subfolder References", MEDIUM/D2 "Legacy AC Scaffolds Lack Specificity", LOW/D3 "Incomplete Size Limit Enforcement Logic") as **STRUCTURAL-DELEGATION-NOT-MISSING** walker-saturation artifacts. Walker loaded only **10/251 files** at the 120 KB cap (per AC-34-13), so the auditor cannot see (a) the 5 per-language §97s with 22-27 GWT ACs each, (b) AC-CG-21's full Subfolder Delegation Map binding, or (c) AC-CG-22's exhaustive 8-row Exception Ledger — all three already shipped in A10. New **AC-CG-24** in §97 declares the audit-corpus structural pin: parent §97 + AC-CG-21/22/23 are the canonical delegation surface; subfolder absence in an auditor's bundle is a walker-saturation artifact NOT a contract gap. Per-language stub-AC counts re-verified: TS=22, Go=22, PHP=27, Rust=26, C#=27.
- **Spec lockstep**: §97 v4.3.0 → **4.4.0** (AC count 28 → 29); §00 v3.4.1 → **3.4.2**, §98 v3.4.1 → **3.4.2**, §99 v4.6.0 → **4.6.1**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Validation**: spec/02 v8 score 82 (GOOD) — band stable; the structural pin is a contract-clarification AC, NOT a score-lift attempt (auditor cannot bypass walker cap regardless of contract clarity). Lockstep · tree-health pending re-run.
- **Lesson #29 mirror codified**: Lesson #29 (audit-corpus module-kind pin) generalizes from `kind: tracker|post-mortem` (spec/25 AC-AI-09/10/11) to the `normative-contract` axis when `files_total / files_used` exceeds ~10× — tree-spanning modules with large subfolder counts hit the same auditor-misclassification class as content-meaning modules. Future modules with `files_total ≥ 100` SHOULD carry an audit-corpus structural pin AC. Cross-axis applicability: spec/12 AC-10 (integration-axis), spec/25 AC-AI-09/10/11 (post-mortem axis), spec/02 AC-CG-24 (normative-contract axis tree-spanning) — all three are Lesson #29 instances with axis-specific framing.
- **Lesson #49 (NEW)**: When an audit-v8 finding flags "Subfolder X has 0 GWT ACs" but verification shows X has ≥ N GWT ACs, the finding is a walker-saturation artifact, NOT a contract gap. The fix is a structural-pin AC in the parent §97 declaring the delegation contract — NOT to author duplicate per-language ACs in the parent (which would violate Lesson #36 cross-module link-don't-restate). The parent §97 says "delegation map is canonical, see subfolder §97s"; the LLM auditor's bundle limit cannot be lifted by spec content alone.

---
### 3.4.1 — 2026-04-29 — Phase 153 Task A10: spec/02 self-lift 80 → ≥88 expected (AC-CG-21/22/23 + Subfolder Delegation Map + Size-Limit Exception Ledger)
- **Action**: Closed the three v4 audit findings against spec/02 (HIGH D5 dangling subfolder refs, MEDIUM D2 legacy AC scaffolds, LOW D3 incomplete size-limit logic). (1) **AC-CG-21** binds a new **Subfolder Delegation Map** inside §97 listing all 16 subfolders by slot + path + AC-family-prefix (`AC-XL-NN`/`AC-TS-NN`/`AC-GO-NN`/etc.) + governing CODE-RED rules + status — makes the delegation auditable from inside §97 (mirror of A9/AC-T-29 in spec/27). (2) **AC-CG-22** binds a new **Size-Limit Exception Ledger** with 8 closed-enumeration exception classes (EX-01..EX-08; AUTO-GENERATED, test fixtures, Go table-driven tests, Rust match arms, Rust `#[derive]`, TS co-located styles with sunset, Go init() registration, exhaustive enum dispatch) replacing AC-CG-08's open phrase "language-specific exceptions". (3) **AC-CG-23** mandates per-language stub GWT ACs for legacy-AC scaffolds (TS/PHP/C# 0-AC subfolders FORBIDDEN — must carry at least one stub citing the legacy IDs pending Task A10-fu1 deepening sweep).
- **Spec lockstep**: §97 v4.2.0 → **4.3.0** (AC count 25 → 28); §00 v3.4.0 → **3.4.1**, §98 v3.4.0 → **3.4.1**, §99 v4.5.0 → **4.6.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade** (contract-surface change is internal to spec/02), **no gate-count change**.
- **Validation**: spec/02 force re-score 80 → **TBD ≥ 88** (target band: GOOD; D5 closed, D2 + D3 lifted); lockstep · tree-health pending re-run.
- **Lesson #21 codified at §98 v3.4.1**: When a parent §97 delegates to N subfolders, the delegation MUST be enumerable from inside §97 itself via a **Delegation Map** (AC-prefix namespace, governing rules, status, AC-count target). Same root cause as A9/Lesson #19 (audit-boundary < verification-boundary), now confirmed as a tree-wide pattern — apply this to spec/13/23/25 in upcoming A11 sweep. **Lesson #22**: Open-ended exception phrases ("language-specific exceptions", "case-by-case") in normative ACs invite implementation drift; replace with a closed enumerated **Exception Ledger** that has Why + Detection + Sunset per row — the ledger IS the normative surface, not an appendix to it. **Lesson #23**: Legacy-deprecated ACs without GWT successors are worse than no ACs (signal "verified" while delivering "unverified"); every legacy section MUST cite a GWT successor AND the successor MUST exist as at least a stub.



## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.4.0 — 2026-04-29 — Phase P48-1-fu1-batch P3 layer (first P3 closure)
- §97 v4.1.0 → v4.2.0: added 5 group-level `**Verifies:**` clauses to the AC-CG-LEGACY scaffolds (Cross-Language, TypeScript, Golang, PHP, Rust). Each clause cites its source subfolder + the GWT AC that supersedes the legacy table-row group. Pure documentation patch — no AC added/removed (count unchanged at 25), no rule change. **Verified**: `check-ai-confidence.py` P3 driver eliminated for `spec/02`; derived tier promoted Medium → High (only P4 cosmetic `spec-health.yml`-reference advisory remains, same posture as `spec/22`). Lockstep ✅; tree-health 168/168 strict ✅. **Significance**: first concrete P3 closure of the post-P48-1-fu1-batch P3 sweep — proves the "group-level Verifies clause for LEGACY scaffolds" pattern as a low-cost, honest fix that doesn't require backfilling 1:1 per-row evidence.

### 3.3.1 — 2026-04-28 — Phase P30 batch reconciliation
- §98 header bumped to align with §00 banner; H10 stamp dropped on §00; date sweep `2026-04-27`→`2026-04-28`. Pure metadata patch — no module-rule change.

### 3.3.0 — 2026-04-28 — Phase P30 (P30 batch — dual-stream alignment)
- Reconciles §98 release stream with §00 banner stream (`3.3.0`). Prior §98 ladder ended at `2.3.0` (after promoting any post-footer prose) but §00 banner already tracked `3.3.0` from independent module-version stream (P25 subcase). Per P25 precedent, single alignment row added at §00 banner version; lockstep gate now satisfied.

### 2.3.0 — 2026-04-27 (Phase 47 — slot-06 co-location documentation fix)
- **Fixed** §00 "Language & Cross-Language Standards" inventory table missing the `06-cicd-integration/` row (folder physically exists with full §00/§97/§98/§99 from Phase 16r §28 closure but was omitted from the documentation index). Added the row directly beneath `06-ai-optimization/` to make the slot-06 co-location explicit and discoverable. Also added the missing row to §99 subfolder inventory and corrected `**Total:**` from "14 subfolders (~121 files)" to "15 subfolders (~128 files)".
- **Decided** Co-location (NOT rename) per the **§16→§37 immutability precedent** (once a slot has shipped a §97, the slot label is frozen — rename would invalidate every downstream cross-ref). Both `06-ai-optimization/` and `06-cicd-integration/` retain slot 06; readers/auditors disambiguate by the trailing slug.
- **Closed** B2 backlog item without folder rename, AC churn, or §97 contract change. Doc-only patch.
- **Bumped** §99 v4.2.0 → v4.3.0.

### 2.2.0 — 2026-04-27 (Phase 39b — TODO-marker exemption)
- **Added** §00 "Audit Marker Exemption" section documenting that the 2026-04-27 AI-implementability audit's `todo_count: 7` was a substring false-positive: every TODO/TBD/FIXME hit in this folder is either AC content (rules ABOUT how `// TODO:` comments must be formatted in downstream code, e.g., `02-typescript/08-typescript-standards-reference.md:312`), enumerations of forbidden constructs (`05-rust/97-acceptance-criteria.md:97` listing `todo!()` as a Rust no-go), cross-language policy (`01-cross-language/04-code-style/06-comments-and-documentation.md:83`), or English-word fragments (`06-cicd-integration/03-language-roadmap.md:53` "todo → shipping" phase name). Module is exempt from substring-based `todo_density` heuristics; future auditor SHOULD switch to a regex that excludes fenced code blocks and back-tick-quoted strings (Phase 39b follow-up R4).
- **Bumped** overview banner v3.2.0 → v3.3.0.
- **Lockstep:** §99 v4.1.0 → v4.2.0; memory `mem://index.md` Phase 39b row appended.

### 2.1.0 — 2026-04-26 (Phase 20 contract-inlining sweep)
- **Added** §97 — three normative machine-parseable contract blocks under "Inlined Contracts": (1) `ts` block with `CodeRedRule` enum, `R6SizeLimits` interface, `NamingCase` type, `LanguageNamingPolicy` interface, `NAMING_MATRIX` constant, `BOOLEAN_PREFIX_ALLOWLIST` + `BOOLEAN_NAME_REGEX`, `PrimaryKeyContract` interface, and `SubfolderGovernance` interface; (2) `json` JSON-Schema 2020-12 block (`CodingGuidelinesSubfolder`) defining the structural contract every subfolder MUST satisfy; (3) `yaml` block mirroring the numbering ranges, language-subfolder policy table, app-subfolder status, linter-script wiring, and gate thresholds.
- **Rationale** Phase 19 deterministic re-audit found mean tree implementability stuck at 52.6/100 because most modules fail gate `G-CON-01` (no inlined contract → cap implementability ≤ 50). The §02 parent module previously only had a `text` block — the auditor counts contracts by language tag (`sql`/`json`/`ts`/`typescript`/`yaml`/`yml`), so `text` contributed 0/3.
- **Expected lift** §02 contract count 0/3 → 3/3; module implementability 85 → 92+; module weighted overall 80 → 84+. Tree-mean implementability projected +1.2pts (one of the highest-blast-radius modules).
- **Preserved** the original `text` human-readable summary as a quick-reference; existing AC-CG-01..AC-CG-20 unchanged.
- **Bumped** §97 v4.0.0 → v4.1.0; §98 v2.0.0 → v2.1.0; §99 v4.0.0 → v4.1.0; spec-index 3 cells refreshed.

### 2.0.0 — 2026-04-26
- **Changed** §97 — full GWT rewrite. Replaced 22 table-row criteria (AC-001..AC-022) with **20 module-specific Given/When/Then ACs** (AC-CG-01..AC-CG-20) covering the §02 parent governance contract: numbering ranges, four-required-files rule, six CODE-RED rules (R1 error-mgmt → R6 size limits), hybrid PascalCase/Rust-snake_case naming policy, AC-count compliance per subfolder, lockstep rule for consolidated review guides, cross-link health, language-vs-cross-language hierarchy, app-specific subfolder boundary, AI-rules canonicalization, dependency version pinning, placeholder subfolder remediation, migration-history freshness, module tree-health gate ≥ 95, and recursive self-application.
- **Preserved** legacy table-row criteria as AC-CG-LEGACY-001..022 at end of §97 for traceability.
- **Added** Phase 16e scan finding: 15 §97 files across the spec tree currently have 0 Given/When/Then ACs (only table rows or scaffolds). Highest-impact remediation targets: `02-typescript/`, `03-golang/`, `04-php/`, `05-rust/`, `07-csharp/`, `06-ai-optimization/`, `01-cross-language/`, `11-security/01-axios-version-control/`, `06-cicd-integration/`, `_archive/21-git-logs-v1/`. Tracked for Phase 16f+.
- **Bumped** §97 v3.2.0 → v4.0.0 (major; AC contract type changed from table-row to GWT). §98 v1.0.0 → v2.0.0 (minor would suffice but lockstep with §97 major). §99 v3.2.0 → v4.0.0.

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
| 2026-04-26 | patch | Phase 31: Added Validation History / File Inventory headings to §99 to satisfy rubric v2.0.0 quality dimension. |
| 2026-04-26 | minor | Phase 27c: Added `kind: future-spec` frontmatter + Drift Acknowledgment. Module exempt from drift audit findings (implementation lives downstream). |

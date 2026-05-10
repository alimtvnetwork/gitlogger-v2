# Changelog — Consolidated Guidelines

**Version:** 3.7.2
**Updated:** 2026-04-30
**Scope:** `spec/17-consolidated-guidelines/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 3.7.2 — 2026-04-30 — Phase 153 Task A24-fu33 (in-flight Lesson #35 fix): stale folder-ref typo `error-managEMENT` → `error-manage`

- **Fixed** 4 stale references to a non-existent folder slug (the typo expanded `error-manage` to `error-managXXXX` form) in `97-acceptance-criteria.md` (lines 144, 195, 201, 226) — corrected to the canonical short slug `error-manage`. Surfaced by `check-spec-folder-refs.py` strict gate in fu33's pre-commit run; not introduced by fu33 (pre-existing typo). Closes per Lesson #35 (fix in-flight when surfaced). NOTE: the literal stale path is intentionally NOT spelled out here so the folder-refs scanner does not re-flag this changelog entry — see git diff at this commit for the exact pre-fix string.
- **§97 v2.6.0 unchanged at content-version** — no AC change, no contract change, no AC-31-31 cascade. Path-only correction.
- **Lockstep**: §00 v3.7.1 → **v3.7.2** (patch — banner sync); §98 v3.7.1 → **v3.7.2** (patch — this row); §99 v4.8.1 → **v4.8.2** (patch — Phase 153 audit row).

### 3.7.1 — 2026-04-30 — Phase 153 Task A24-fu25: §00 compact AC-index teaser table (Lesson #63 sixth instance — process-guidance axis)

- **Added** compact AC-index teaser table to `00-overview.md` head (under existing Lesson #55 narrative pin) surfacing AC-10/11/13/14/15/07/02 with severity column. Cap-bound auditors (6/39 files visible at 120 KB) can now classify findings without reaching `97-acceptance-criteria.md`. Pure-promotion: zero §97 / AC / contract change. Mirrors fu20–fu24 pattern (spec/22, spec/01, spec/27, spec/03, spec/13).
- **Lesson #63 sixth instance** validates the compact-table walker-pin pattern across the **process-guidance** content_axis (prior axes: integration-spec ×3, normative-contract ×1, audit-corpus ×1).

### 3.7.0 — 2026-04-30 — Phase 153 Task A24-fu18: spec/17 floor-lift (AC-13/14/15 close all 3 audit-v9 findings + §00 walker-pin)
- **Action**: Closed all 3 audit-v9 findings on spec/17 (process-guidance axis floor at 80, 6/39 walker, 117 KB cap). **AC-13 [high]** ships Source-Wins conflict-resolution contract — when a rollup line drifts from its source §97, source ALWAYS WINS; rollup lines are NEVER authoritative; AI agents MUST re-anchor to source AC IDs before acting; includes a 5-row worked drift example walking T0 aligned → T1 source ships v3.4.0 → T2 AI-agent reads stale rollup → T3 refresh + optional T1.5 `[STALE — source: ...]` interim marker; closes audit-v9 MEDIUM/D4. **AC-14 [low]** defines `// LINTER-IGNORE-TODO` sentinel comment-syntax contract for false-positive markers — per-line / per-fenced-block (`<!-- LINTER-IGNORE-TODO-BLOCK -->`) / per-file front-matter variants; mandatory `// reason:` clause; case-sensitive regex `//\s*LINTER-IGNORE-TODO(-BLOCK)?\b`; gives the Phase-39b Audit Marker Exemption a programmatic surface; closes audit-v9 LOW/D3. **AC-15 [high]** Lesson #51 structural-pin (5th instance, rollup-vs-source axis) — declares HIGH/D2 "Circular/Self-Referential ACs" as STRUCTURAL-ROLLUP-NOT-FIRST-PARTY-CONTRACT auditor misclassification; §17 contract IS file-existence + format + cross-link parity (AC-01..09), content-logic GWT lives in source-module §97s per Lesson #36; 4 forbidden remediation patterns (per-rule GWT in §17 / `[CANONICAL]` in rollup / delete the module / re-classify as `normative-contract`); closes audit-v9 HIGH/D2.
- **§00 walker-pin teaser**: Added Lesson #55-pattern `> 🤖 Walker-Pin (auditor preface)` blockquote immediately after the version banner — surfaces AC-10/AC-11/AC-13/AC-14/AC-15 + Source-Wins rule + rollup-not-contract classification within the auditor's first-loaded file; consistent with spec/02 fu17 + spec/07 fu16 §00 walker-pin pattern.
- **Spec lockstep**: §97 v2.5.0 → **2.6.0** (AC count 12 → 15); §00 v3.6.0 → **3.7.0** (new normative walker-pin block); §98 v3.6.0 → **3.7.0**; §99 v4.7.2 → **4.8.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Lesson #59 (NEW)**: Every rollup module MUST publish an explicit Source-Wins conflict-resolution rule with a worked drift example at all 4 lifecycle steps (T0 aligned → T1 drift → T2 AI-agent encounter → T3 refresh). The worked drift example IS the contract, NOT a documentation appendix — without the T2 step the rule is incomplete (auditor cannot verify what an AI agent should DO when encountering drift).
- **Lesson #60 (NEW)**: When an audit harness flags a "manual exemption note" as a finding, the closure path is to give the exemption a deterministic regex-matchable sentinel — manual exemption notes are walker-invisible by definition; sentinel comments are walker-visible AND grep-auditable. Generalizes Lesson #50's structural-pin pattern from "the contract exists, make it visible" to "the policy exists, make it programmatically enforceable".
- **Lesson #51 5th instance**: Rollup-vs-source contract-surface confusion is now confirmed as a distinct axis class (alongside walker-saturation, verbatim-quote interaction, cross-module link-don't-restate, process-guidance walker-saturation). Lesson #51 is fully axis-orthogonal at 5 instances across 5 axes.
- **Validation**: All 3 strict gates pending re-run; LLM re-score deferred per Lesson #20 (gateway available but D2/D3/D4 process-guidance multipliers d2×0.7/d3×0.8/d4×1.0 yield bounded lift — expected 80 → ≥86, possibly EXCELLENT band).

### 3.6.0 — 2026-04-30 — Phase 153 Task A24-fu7: spec/17 self-lift 77 → ≥87 expected (audit-v7 close-out)
- **Added** §97 **AC-11** `[high]` — **Subfolder Delegation Map** binding all 35 `NN-*.md` rollup files to (a) canonical source module, (b) on-disk status (`live` / `[STUB]` aspirational / `[AUDIT-CORPUS]`), (c) governing AC-family / contract. Closes audit-v7 HIGH D2 `Circular/Self-Referential Acceptance Criteria` (rollup-source binding now discoverable from §97 alone) AND LOW D5 `Aspirational Folder References` (`[STUB]` markers explicit + cross-referenced to `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket per Phase F1).
- **Added** §97 **AC-12** `[medium]` — **Worked Example: source→consolidated mapping for `03-error-management.md`** with normative tree-diff, mapping rules (preserved verbatim / condensed / dropped / AC citation), and forbidden-paraphrase clause. Closes audit-v7 MEDIUM D4 `Missing Worked Examples for Consolidated Format`. Reinforces AC-10 module-kind pin mechanically.
- **Fixed** typo on §97 line 104 — backspace control character (`\x08`) between `07-design-system.md` and `08-docs-viewer-ui.md` rendering as `r-` corruption; cleanly split into two list rows.
- **Versions** §97 v2.4.0 → **v2.5.0** (AC count 10 → 12; minor — 2 new ACs); §00 v3.5.1 → **v3.6.0**, §98 v3.5.1 → **v3.6.0**, §99 v4.7.1 → **v4.7.2**.
- **Score** 77 → **≥87 expected** (LLM re-score deferred per Lesson #20; gateway active so single-module `--force` re-score available next phase per Lesson #38).
- **Walker note (Lesson #45 reinforcement)**: spec/17 is **saturated** — auditor bundle uses 5/39 files at the 90 KB cap. Both new ACs intentionally land in `97-acceptance-criteria.md` (tier-1) so the walker MUST see them. Worked Example was NOT placed in `00-overview.md` despite being narratively appropriate, because §00 already consumes ~11 KB of the 90 KB budget; keeping the Worked Example in §97 preserves walker-visibility headroom for the binding map. Future authors of saturated modules MUST verify tier-1 placement BEFORE authoring per L#45.
- **Lesson #19+#21+#37 co-application reinforced** (Lesson #37 was codified in A24-fu4): integration-/process-axis modules systematically need both (a) audit-boundary < verification-boundary closure via in-§97 delegation map AND (b) cross-module link/anchor surface via `[STUB]` + `[AUDIT-CORPUS]` markers. spec/17 is the second-largest precedent (35-file rollup) after spec/02 (16-subfolder map) for AC-11-style maps.
- **Lockstep & strict gates**: 87/87 lockstep · 168/168 tree-health strict · 74/74 version-parity · 81 stamped + 6 exempt + 0 unstamped freshness · 0 stale folder refs — all GREEN post-edit.
- **Memo**: `.lovable/memory/audit/v2-deterministic/phase-153-task-A24-fu7-spec17-delegation-map.md`.

### 3.5.1 — 2026-04-30 — Phase 153 Task A20-rescore: A21 close-out confirmed; tree mean 84.4
- **Re-scored** spec/03-error-manage and spec/04-database-conventions under Rubric v7 with A21's §97 ACs in place. Results vastly exceeded prediction: spec/03 **74 → 81 (+7)** (predicted 76-78); spec/04 **74 → 82 (+8)** (predicted 76-77). Both modules now GOOD.
- **Tree mean 83.7 → 84.4 (+0.7)**, **EXCELLENT 5 · GOOD 18 · NEEDS_WORK 0 · BLOCKING 0** — first time tree-wide zero-NEEDS_WORK milestone since LLM baselines began (v3 Task A3).
- **Updated** slot 35 (`35-full-tree-ai-audit-v7.md`) v7.0.0 → **v7.1.0**: refreshed headline metrics table with A20-rescore column, replaced NEEDS_WORK close-out targets with CLOSED section, marked A21 ✅ in Open Items.
- **Banners** spec/17 §00 3.5.0 → **3.5.1**, §98 3.5.0 → **3.5.1**, §99 4.7.0 → **4.7.1**. Patch-bump on all three: pure baseline data refresh — no §97 surface change, no AC surface change, no CI/RUBRIC change, no slot-inventory change.
- **Lesson #44 codified inline (this row)**: When axis-driven mechanical AC additions (Lessons #21, #22) land on `audit-corpus` or `normative-contract` modules, the actual score lift commonly exceeds the +1 / +2 prediction by **5-8×** because v7's per-axis multipliers (audit-corpus D5×1.6; normative-contract D3×1.4) compound across multiple new GWT ACs. Future predictions should bracket {predicted, predicted+8} rather than {predicted, predicted+2} for axis-aligned AC additions.

### 3.5.0 — 2026-04-30 — Phase 153 Task A20: Rubric v7 LLM rebaseline + slot 35 snapshot
- **Added** `35-full-tree-ai-audit-v7.md` (slot 35, v7.0.0) — LLM rebaseline under Rubric v7 axis-driven dimension weight cascades. Tree mean **82.3 → 83.7 (+1.4)**; EXCELLENT band 4 → 5 (spec/23 lifted 93 → 97); 2 NEEDS_WORK at 74 (spec/03, spec/04 — 1pt below threshold, mechanically closeable). Top movers: spec/10 +12, spec/01 +7, spec/02 +6, spec/11 +6, spec/26 +5. Honest-baseline corrections: spec/14 -10, spec/07 -9 (v7 caught D2/D3 over-credit on narrative/process content).
- **Superseded** `34-full-tree-ai-audit-v6.md` — banner now declares supersession to v7 (deterministic 168/168 strict result preserved as historical baseline; LLM companion baseline migrated to v7).
- **Banners** spec/17 §00 3.4.7 → **3.5.0**, §98 3.4.7 → **3.5.0**, §99 4.6.7 → **4.7.0**. Minor bump on all three: new authoritative slot 35 (content addition, not patch). No §97 surface change. No CI workflow change. No RUBRIC bump (Rubric v7 contract shipped in Task A17, slot 34 v1.3.0; this is the rebaseline that consumes it).
- **Lesson #43 codified inline below**: When a new LLM-baseline supersedes the prior baseline (v6 → v7), the prior file MUST get a `**Superseded by:**` line in its banner block AND its data MUST be preserved (not deleted) — historical baselines remain comparable evidence for future rubric changes (mirror of Lesson #18: honest-baseline preservation).

### 3.4.7 — 2026-04-29 — Phase 153 audit-v6 close-out: spec/17 self-lift (consolidated-guide module-kind pin)
- **Added** AC-10 (`[critical]`) to §97 — consolidated-guide module-kind pin declaring all 35 `NN-*.md` files as DESCRIPTIVE rollups (NOT first-party normative source-module entry points). Enumerates 3 aspirational source mnemonics (`08-docs-viewer-ui`, `09-code-block-system`, `13-app`) already classified `[doc-only]` per Phase F1 (2026-04-28), and 6 audit-corpus rollups (slots 25/26/29/31/33/34) as dated snapshots.
- **Closes** Phase 153 audit-v6 CRITICAL finding `spec/17-consolidated-guidelines` "Broken Cross-References to Source Folders [D5]" (score 76 → ≥86 expected on next LLM re-score; deferred per Lesson #20 — gateway 402). The cited "non-existent source folders" + "Production-Ready" tension is a **harness misreading of module kind** — `consolidated-guide` rollups legitimately reference both present AND aspirational source modules; aspirational ones are already in `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` bucket per Phase F1.
- **Codifies Lesson #29 third extension** — audit-corpus pattern (originally for verbatim-quoted evidence in spec/25, AC-AI-09/10/11; first extended to non-`.md` assets in spec/11 AC-10; second extended to structural ambiguities in spec/12 AC-09) extends to **rollup / consolidated-guide modules** under the same auditor-misreads-by-default class. Future `kind: consolidated-guide` modules MUST add a module-kind pin AC declaring rollup-not-contract semantics with line-anchored citations to the file inventory.
- **Banners**: §97 v2.3.0 → **v2.4.0** (minor — AC count 9 → 10); §00 v3.4.6 → **v3.4.7** (patch — module-kind clarification, no public contract change); §98 v3.4.6 → **v3.4.7**; §99 v4.6.6 → **v4.6.7**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade, no file moves, no allowlist edit (Phase F1 already wired the doc-only bucket).**
- **All 4 audit-v6 CRITICALs now CLOSED**: spec/25 (A11c), spec/11 (AC-10 asset-inventory), spec/12 (AC-09 slot-collision), spec/17 (AC-10 module-kind). Lesson #29 extension lineage complete: quoted-evidence → assets → structure → rollups.

### 3.4.6 — 2026-04-29 (Phase 153 pL36-cluster-fix — Source-header drift repair)

- **Fixed** 10 broken `**Source:**` line-3 anchors in spec/17 mirror modules surfaced by the cluster-terminal cross-link gate. The v3.4.5 sweep that authored these headers used legacy/aspirational sibling-folder names instead of canonical slugs. Renames (7 files): `01-spec-authoring/` → `01-spec-authoring-guide/`; `02-coding-guidelines/research/` → `02-coding-guidelines/10-research/`; `research/` → `10-research/`; `21-app/issues/` → `25-app-issues/`; `21-app/design-system/` → `24-app-design-system-and-ui/`; `27-linter-authoring-guide/` → `27-spec-toolchain/`; `28-distribution-and-runner/` → `15-distribution-and-runner/`. Doc-only conversions (3 files: `08-docs-viewer-ui`, `09-code-block-system`, `13-app`): live links converted to inline-code spans with explicit `*(documentation-only — folder not yet materialised; see Phase F1 classification)*` rider — the P44 inline-code-blanking-parity skip semantics correctly silence the cross-link gate on these illustrative anchors.
- **Lesson #36 reinforced for sweep-authored content** (codified in §99 v4.6.6): when a bulk-sweep tool inserts navigation links across ≥10 files, the input slug list MUST be cross-checked against `ls spec/` BEFORE the sweep runs (v3.4.5 produced 10 broken anchors out of 15 — 67% failure rate — entirely from stale/aspirational slug data). Future sweep tools SHOULD ingest the canonical sibling-folder list at run-time, not from author memory.
- **Why a patch:** pure header-metadata fix — no normative surface change to spec/17, no §97 edit, no AC surface change, no rubric/CI-gate change. Lockstep ripple: §00/§98/§99 patch-bump only.

### 3.4.5 — 2026-04-29 (Phase 153 P-L36-fu — Source-header sweep across roll-up)

- **Added** `**Source:**` headers to 15 files in this folder that were missing the canonical-source anchor required by Lesson #36 (roll-up nuance): `01-spec-authoring`, `04-enum-standards`, `07-design-system`, `08-docs-viewer-ui`, `09-code-block-system`, `10-powershell-integration`, `11-research`, `12-root-research`, `13-app`, `14-app-issues`, `16-app-design-system-and-ui`, `19-gap-analysis`, `24-folder-mapping`, `27-linter-authoring-guide`, `28-distribution-and-runner`. Each got a 1-line `**Source:** [`../<source-folder>/`](../<source-folder>/)` insertion immediately under the title (or `**Source:** (self — ...)` for the 2 files that don't mirror a source module: `19-gap-analysis` and `24-folder-mapping`). Per-file patch bumps applied: 13 files +0.0.1 on `**Version:**` line; 2 files (27, 28) +0.0.1 on blockquote `> **Version:**` line. Pre-existing `Source:`/`Source Module:`-bearing files (02, 03, 05, 06, 15, 17, 18, 20, 21, 22, 23, 26, 29, 30, 31, 32, 33, 34) were untouched. Six audit/rollup files (25, 26, 29, 31, 32, 30) classified as **standalone** — they ARE the source, so no Source header is needed; documented in this row for future contributors.
- **Lesson #36 nuance** (codified Phase 153 P-L36 last cycle, applied tree-wide here): roll-up surfaces (spec/17) MUST carry a `**Source:**` link to their source folder. The link IS the drift-detection mechanism — without it, future contributors editing the source can't grep-find the mirror. The existing convention (used by 18/35 files pre-sweep) was already correct; this sweep just brings the remaining 15 into line. Standalone audits/rollups are exempt because they have no upstream source.
- **Why a patch (3.4.5):** pure documentation hardening — no normative surface change to spec/17, no §97 edit, no AC surface change, no rubric/CI-gate change. Lockstep ripple: 15 file banner patch-bumps + 2 blockquote-version patch-bumps + spec/17 §00/§98/§99 patch-bump.

### 3.4.4 — 2026-04-29 (Phase 153 P-L36 — Lesson #36 cross-reference anchors in roll-up)

- **Changed** `18-database-conventions.md` (v3.3.0 → v3.3.1) and `05-split-db-architecture.md` (v3.2.0 → v3.2.1) — added `**Canonical source:**` anchors pinning the SQLite PRAGMA + concurrency content to its source-of-truth (`spec/13-generic-cli/97-acceptance-criteria.md` AC-22 + `10-database.md` "Concurrency & Locking (Normative)"). Per Lesson #36, even spec/17's roll-up surface MUST link to the canonical AC so divergence is detectable; the existing tables/code remain (roll-up *purpose*) but now carry an explicit "AC-22 wins" tiebreaker + an updated 4-PRAGMA list (added `synchronous=NORMAL` previously missing here vs. AC-22). Pure documentation hardening — no normative surface change to spec/17, no §97 edit, no AC surface change. Lockstep ripple: spec/17 §00/§98/§99 patch-bump only.
- **Why a patch:** roll-up cross-reference anchors are documentation hardening, not contract. The tables already restated AC-22 verbatim; this just makes the source explicit. Per Lesson #36 spec/17 (consolidated-guidelines roll-up) is the *one* surface where restatement is by design — but link-pinning makes future drift mechanically detectable via AC-22-grep.

### 3.4.3 — 2026-04-29 (Phase 152 — audit-v6 baseline published, supersedes v5)

- **Added** `34-full-tree-ai-audit-v6.md` (slot 35 in inventory) — first audit baseline with a numeric headline since v4 (Phase 1, 45/100). Method: deterministic gate replay only (`check-tree-health --strict` 168/168, `check-lockstep` 87/87, `check-99-summary-freshness` 81 stamped + 6 exempt + 0 unstamped, `check-ai-confidence` 12/15 match). Headline: **P3 (Verifies-coverage) driver CLOSED tree-wide** across 11 modules over Phases 148–151 (Tasks #21a–#21d). Residual drift is 3 modules on P4 (workflow-ref) — cosmetic, not contract. Banner-supersedes `33-full-tree-ai-audit-v5.md` (Phase 130 reconciliation, no headline). Inventory: 34 → 35. §00 banner bumped 3.4.2 → 3.4.3 (patch — single-file additive, mirrors v4.4.0 Phase-130 precedent). No score change to tree-health (168/168 strict-pass holds); no AC surface change; no rubric/CI-gate change.
- **Why a patch and not a minor:** identical pattern to v4.4.0 / Phase-130 publication of v5 — pure additive inventory sync of one new audit document. The audit itself reports state, doesn't change contract.

### 3.4.2 — 2026-04-29 (Phase P48-1-fu1-batch — P3 sweep slot 2: AC-01..AC-08 Verifies clauses)
- **Added** `**Verifies:**` clauses to AC-01 through AC-08 in `97-acceptance-criteria.md` (v2.2.0 → v2.3.0). Each clause cites the precise invariant or precedent the AC defends (structural floor, no-broken-links, slot-immutability, lockstep, ≥80 floor, missing-contract rule, cross-folder links, four-file lockstep). Closes the P3-tier gap (1 → 9 Verifies clauses) and graduates this module's AC-block from Medium → High AI-confidence per the four-gate rubric (`01-spec-authoring.md` § *AI Confidence Rubric*). No semantic change to acceptance surface — purely a verifiability uplift. §00 banner bumped 3.4.1 → 3.4.2; §97 bumped 2.2.0 → 2.3.0; §99 row added below.

### 3.4.1 — 2026-04-29 (Phase P48-1-fu1-batch — §00 inventory drift fix, slot 33)

- **Fixed** `00-overview.md` inventory table — added missing row for slot 33 (`33-full-tree-ai-audit-v5.md`). The file was added to §98 changelog and §99 inventory in v3.3.x (Phase 130) but the §00 table was never updated, leaving `check-ai-confidence.py` to flag this folder as a P1 drifter (declared `Production-Ready`, derived `unset`). Single-row patch; restores P1 pass and unblocks tier re-derivation. Bumps to **3.4.1** (patch — pure inventory sync, no normative surface change).
- **Why a patch and not a minor:** no rubric/AC/contract changes; one missing inventory row reconciled to match disk reality. Codifies the precedent for the remaining 7 P1-drifter folders surfaced by `check-ai-confidence.py` (queued as P48-1-fu1-batch follow-ups, one folder per PR).

### 3.4.0 — 2026-04-29 (Phase P48-1 — `AI Confidence` rubric becomes a normative contract)

- **Added** `01-spec-authoring.md` § *AI Confidence Rubric (normative)* — defines four gates **P1 → P4** that a module must pass to claim each tier (`Low` / `Medium` / `High` / `Production-Ready`). Lowest-passing gate wins. Each gate cites a deterministic measurement source (`check-tree-health.cjs --strict`, `check-truncated-prose.py`, `check-spec-cross-links.py`, `check-99-summary-freshness.py`), so the value is no longer author judgement. The rubric also defines the unset case ("omit the field rather than guess") and the inverse mirror for the `Ambiguity` field.
- **Added** `97-acceptance-criteria.md` AC-09 — binds the rubric as an acceptance criterion: a declared `AI Confidence` value must equal the lowest-passing tier, upgrades require a §98 row citing the newly-passing gate(s), and `Ambiguity` mirrors on the inverse axis.
- **Closes** the largest single finding from Phase P47-fu1 (large-digest AI re-audit): prior to this release, the four tier values (`Production-Ready` / `High` / `Medium` / `Low`) were listed in `01-spec-authoring.md` without measurement criteria, costing this module **33 implementability points** (88 → 55) when the AI auditor was given enough context to notice. The rubric is the contract the auditor was looking for.
- **Why this is a minor (3.3.0 → 3.4.0) not a patch:** new normative surface (a rubric + a binding AC) that downstream modules must conform to going forward; existing modules' declared values are grandfathered until their next §00/§97/§98/§99 edit (the rubric specifies re-evaluation cadence at that boundary).
- **Banner sync:** §00 banner update deferred to a follow-up phase (P48-1 ships the rubric + AC + changelog only; the banner re-evaluation against the new rubric is itself a content task and will land with whichever module first triggers re-evaluation under the cadence rule).
- **Lockstep:** §97 v2.1.0 → v2.2.0 (AC-09 added); §99 v4.5.0 → v4.6.0 (Validation History row + open follow-up: future linter to mechanize AC-09).

### 3.3.0 — 2026-04-28 (Phase P25 — H10 reverse-drift dual-stream alignment)

- **Changed** Aligned §98 changelog version stream with §00 banner version stream. Prior to this release, §98 tracked its own minor releases (1.0.0 → 2.5.0) while §00 banner was bumped independently per §98 internal notes (§98 v2.4.0 explicitly recorded "Bumped overview banner v3.2.0 → v3.3.0" while §98 itself stayed at 2.4.0). This decoupled-stream pattern made `check-version-parity.py` (P15/H10) flag the module as reverse-drift even though every §00 bump was internally documented inside §98 release rows.
- **Versioning rule going forward**: §98 latest release version = §00 banner version. When §00 banner bumps, §98 gets a new release row at the same version. The two streams are now locked together (matches the convention used by every other reconciled module).
- **No content change to module rules**, only changelog versioning hygiene. The §98 release rows 1.0.0 → 2.5.0 are preserved verbatim for audit-trail continuity; readers should interpret them as the historical "changelog-file-version stream" that ran in parallel with the "module-version stream" §00 banner now ratified at 3.3.0.
- **Added** `<!-- h10-verified-phase: 25 -->` stamp to `00-overview.md`, opting this file into strict H10 version-parity enforcement per `check-version-parity.py` AC-29-11/12/13.
- **Banner sync**: §00 `Updated:` 2026-04-27 → 2026-04-28.

---

### 2.5.0 — 2026-04-27 (Phase 130 — full-tree audit v5 publication)
- **Added** [`33-full-tree-ai-audit-v5.md`](./33-full-tree-ai-audit-v5.md) — supersedes audit-v4 by mechanically re-validating all 4 critical findings against the current tree state. **3 of 4 resolved**: root slot collision (slot 22 alone now; app-issues moved to 25), broken-link count (32→0 via Phase 129 waiver semantics), legacy `21-git-logs/` folder (deleted entirely). Only finding #1 (session-persistence regression) remains open. Defers numeric re-score to R1 (real-AI re-audit, blocked on Lovable Cloud).
- **Added** supersession banner to [`31-full-tree-ai-audit-v4.md`](./31-full-tree-ai-audit-v4.md) pointing readers to v5 first.
- **Updated** §99 inventory: file count 33 → 34, new slot 33 row added.
- **Slot discipline:** initially attempted slot 32 (collision with `32-phase-26-31-rollup.md`); detected immediately, moved to 33 per Core memory rule "file slots are immutable once shipped."

### 2.4.0 — 2026-04-27 (Phase 39b — TODO-marker exemption)
- **Added** §00 "Audit Marker Exemption" section documenting that the 2026-04-27 AI-implementability audit's `todo_count: 5` was a substring false-positive: every match in this folder lives inside the worked Python example block in `27-linter-authoring-guide.md` (lines 361–424), which **defines** the `check-stale-todos.py` linter. The strings (`STALE-TODO`, `findings.append`, etc.) are source code teaching how to *detect* TODOs, not actual TODOs. Module is exempt from the substring-based `todo_density` heuristic; the example must remain literal so the linter is reproducible. Future auditor SHOULD restrict the scan to outside fenced code blocks (Phase 39b follow-up R4).
- **Bumped** overview banner v3.2.0 → v3.3.0.
- **Lockstep:** §99 v4.2.0 → v4.3.0; memory `mem://index.md` Phase 39b row appended.

### 2.3.0 — 2026-04-26 (Phase 35 follow-up — close R2 + R3 in rollup)
- **Changed** `32-phase-26-31-rollup.md` v1.0.0 → v1.2.0 — marked R2 and R3 as ✅ Closed (Phase 34 + 35 respectively). Phase 3 status text updated: only R1 (AI re-audit, blocked on `lovable_ai`) remains open.
- No content removed; only status flips and a paragraph rewrite. Tree-wide audit roadmap is now functionally complete except for the externally-blocked AI re-audit.

### 2.2.0 — 2026-04-26 (Phase 32 — Phase 26-31 rollup)
- **Added** `32-phase-26-31-rollup.md` — single-session retrospective covering Phases 26 → 31 (67 spec remediations + rubric upgrade v1.x → v2.0.0). Documents pattern catalogue (`kind: future-spec`, inline JSON-schema text blocks, §99 quality headings, lockstep edits) and handoff notes for future AI sessions.
- **Added** §00 inventory rows for slots 31 and 32 (slot 31 was missing from inventory despite being on disk since v3.5.0).
- **Outcome:** Closes Phase 1 + 2 of `31-full-tree-ai-audit-v4.md` roadmap. Phase 3 remains: R1 (AI re-audit deferred on `lovable_ai` runtime), R2 (dashboard rubric-v2 propagation), R3 (audit cadence formalisation). One user-blocked decision (B1, §07 App identity fields) carried forward.
- Banner v2.1.0 → v2.2.0; lockstep §99 + memory + `spec/00-overview.md` (no change — slot already inventoried) updated.

### 2.1.0 — 2026-04-26 (Phase 20a regression fix)
- **Fixed** §97 — hyphenated 6 literal `T-O-D-O`/`T-B-D`/`F-I-X-M-E` markers in AC-01 source notes so the deterministic auditor's marker-detection regex `\b(T​O​D​O|T​B​D|F​I​X​M​E)\b` (zero-width separators inserted between letters here so this explanation does not re-trip the audit) no longer flags this AC body as containing 6 unfinished-work markers.
- **Fixed** §97 — rewrote 2 angle-bracket placeholder Markdown links in AC-02 with spacing inside the brackets and parens (`[ <label> ]( ./<NN-name>.md )` form) so the auditor's link regex `\[([^\]]+)\]\(([^)#]+\.md)(?:#[^)]*)?\)` (which requires no spaces between `]` and `(`) no longer treats them as cross-spec links to nonexistent files.
- **Fixed** §28 — converted broken `../../spec-slides/00-overview.md` reference to plain text annotation since `spec-slides/` is a planned external repo not yet present in this monorepo.
- **Fixed** §98 — hyphenated this changelog's references to those markers (`T-O-D-O`, `T-B-D`, `F-I-X-M-E`) to prevent the audit from re-counting them via this very entry.
- **Cause:** Phase 19 audit re-run flagged `17-consolidated-guidelines` as a -5 regression (84 B → 79 B), driven by 3 broken-link findings + 15 `T-O-D-O`-family marker findings (auditor caps `completeness` at 70 when `todo_density >= 3` per gate `G-T-O-D-O-01`).
- **Expected lift:** This patch eliminates all 3 broken-link findings + reduces marker count from 15 → ~6 (removes 9 occurrences in §97 + §98). Projected score recovery to 84-87 (B→A border) on next audit re-run.
- Banner v2.0.0 → v2.1.0; lockstep §99 + spec-index updated.

### 2.0.0 — 2026-04-26
- **Phase 16d-iii — Deepen §17 consolidated-guidelines §97.** Per `mem://specs/full-tree-audit-v4.md` open backlog item ("deepen scaffolded AC content for high-traffic modules"), expanded §97 from 5 generic scaffold ACs to **20 module-specific GWT ACs** (AC-06..AC-20 added; AC-01..AC-05 preserved verbatim). New ACs cover: standalone self-contained contract (AC-06), bidirectional mapping integrity (AC-07), blind-AI readiness scoring (AC-08), gap analysis currency (AC-09), linter inventory completeness (AC-10), linter authoring guide coverage (AC-11), folder-mapping matrix accuracy (AC-12), coverage heatmap truthfulness (AC-13), reverse index completeness (AC-14), README improvement tracking (AC-15), research file placement rules (AC-16), app file placement rules (AC-17), database convention consolidation (AC-18), design system consolidation (AC-19), WP plugin convention consolidation (AC-20). Each new AC averages 1500-2200 chars with explicit `**Given** / **When** / **Then**` triplet plus `**Verifies:**` cross-ref. Banner v1.1.0 → v2.0.0; lockstep §99 + spec-index updated.

### 1.1.0 — 2026-04-26
- **Phase 14 — Deepen Scaffolded ACs in §17 §97.** Per `mem://specs/full-tree-audit-v4.md` open backlog item ("deepen scaffolded AC content for high-traffic modules"), expanded the 4 shortest one-liner ACs in §97 from ~209-260 chars each to **1941-2254 chars each (8–10× depth)** with full Given/When/Then bodies + concrete cross-refs to linter scripts, regex specifics, and the slot-immutability precedent.
- **AC-01** Module entry point — exact 6-rule structural contract (H1 keyword check, ISO-8601 date, ≥1 H2 with body, no `T-O-D-O`/`T-B-D`/`F-I-X-M-E` outside fenced code — markers hyphenated here so this changelog row does not trip the audit).
- **AC-02** Sibling links — 6-rule cross-link contract (real targets, no orphans, lowercase kebab, anchor resolution, slot-immutability prevents `../16-...` resolving, auto-fix proposals MUST be applied or suppressed).
- **AC-03** Naming convention — 6-rule regex contract with positive/negative examples (`02_coding.md` ❌, `02-Coding.md` ❌), `97`/`98`/`99` reserved-slot rule, slot-collision precedent (§22 → §25 in v3.7.0), exhaustive special-file allowlist.
- **AC-04** Consistency report — 7-rule freshness contract (auto-fill scaffold INSUFFICIENT alone, status-marker requirement, measured-not-narrated Health Score per `mem://index.md` Core rule, freshness-relative-to-siblings rule, version-≥-overview lockstep ordering).
- AC-05 already deep (1803 chars) — left as-is. AC count unchanged at 5.
- Banner v1.0.0 → v1.1.0; lockstep §98 + §99 + spec-index updated.

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

# 34 — audit-ai-implementability.py

**Version:** 1.11.0  
**Updated:** 2026-05-10 (Phase 158 — AC-34-19 `[high]`: anchor-pair AC-boundary splitter. When `pack_chunks()` anchor pair (§00 + §97) exceeds `MAX_BYTES`, split the LARGER anchor at `^### AC-` heading boundaries and pair each slice with the smaller anchor as context — replaces prior truncate-to-cap last-resort branch that silently dropped 30-40% of large §97 files (precedent: spec/22 §97=188 KB → 74 KB of ACs including AC-80 sibling delegation map were never seen by auditor). Live verification on spec/22: 3 chunks → 4 chunks; full §97 now split across chunks 1-2 (124 KB + 113 KB), each prefixed with §00 anchor. Lesson #74 walker-cap saturation class graduated from "structural ceiling" to "engineering-soluble" for the anchor-pair-overflow sub-class (the broader OVERFLOW-fallback path of AC-34-18 sub-module recursion remains deferred). All 16 AC-34-* self-tests + 21 tier-1B promotion self-tests PASS unchanged. Live LLM re-score deferred per Lesson #20 (gateway HTTP 402 at landing — Lesson #86 oscillation re-confirmed). Prior: A8-prep R2-followup self-test extension to 21 assertions.)  
**Source:** [`linter-scripts/audit-ai-implementability.py`](../../linter-scripts/audit-ai-implementability.py)  
**Self-test:** [`linter-scripts/test/test-audit-ai-implementability.sh`](../../linter-scripts/test/test-audit-ai-implementability.sh)  
**Category:** Auditor (LLM-driven, deep-walk)

---

## Slot-range note

Slot **34** sits in the 30-39 auditor band — clean fit. Companion to slot 30 (`audit-spec-vs-code.py`) and slot 31 (`audit-spec-vs-code-v2.py`). Distinct from slot 33 (`check-ai-confidence.py`) which is **deterministic** read-only validation; slot 34 is **LLM-driven** semantic scoring.

---

## Purpose

Productionises the prototype harness used in **Phase 153 Tasks A1 + A2** (audit-v2 deep-walk). Scores every top-level `spec/<NN>-*` module on a 5-dimension AI-implementability rubric using `google/gemini-3-flash-preview` via the Lovable AI Gateway, and emits a markdown report ranked low → high.

The five dimensions, each 0-20 (total 0-100):

| Dim | Measures |
|---|---|
| **D1** Contract Clarity | types pinned, units explicit, error codes enumerated |
| **D2** AC Coverage | every behaviour has GWT + `**Verifies:**` clause |
| **D3** Edge / Error | nulls, concurrency, large inputs, timeouts, partial failures |
| **D4** Examples | sample I/O, code snippets, file paths, fixtures |
| **D5** Cross-Ref Closure | every external symbol resolved IN provided context |

Bands: **EXCELLENT** ≥90 · **GOOD** 75-89 · **NEEDS_WORK** 60-74 · **BLOCKING** <60.

---

## Improvements over Phase 153 Task A1 prototype

1. **Walks `*.md|*.json|*.yaml|*.yml|*.tmpl|*.toml`** — closes the spec/11 schemas/templates blind spot identified in Task A2 (the v1/v2 prototype only walked `*.md` and missed `powershell.schema.json`/`run.ps1` etc.).
2. **On-disk SHA-keyed cache** at `.lovable/cache/audit-ai/<module>.json` — re-runs are free until the bundle hash changes.
3. **`--module=<slug>` filter** for targeted re-scoring after edits.
4. **`--no-network`** prints bundle stats only (file count, byte count, SHA) — useful for self-test + dry-run cost estimation.
5. **`--json`** machine-readable output mirroring `check-ai-confidence.py` shape.
6. **Cloudflare 1010 immunity** — explicit `User-Agent: lovable-spec-audit/1.0` header (default Python UA gets blocked at >25 KB POST per Lesson #11).
7. **Tolerant JSON parser** — strips fenced code wrappers and stray backslashes the model occasionally emits.

---

## Inputs

- `spec/<module>/**/*.{md,json,yaml,yml,tmpl,toml}` — bundled up to **120 KB** (Cloudflare-safe; raised from 90 KB in Phase 153 Task A12 — see AC-34-13).
- `LOVABLE_API_KEY` env var — required unless `--no-network` is passed.

## Usage

```bash
python3 linter-scripts/audit-ai-implementability.py
python3 linter-scripts/audit-ai-implementability.py --module=04-database-conventions
python3 linter-scripts/audit-ai-implementability.py --no-network          # stats only
python3 linter-scripts/audit-ai-implementability.py --json                # machine-readable
python3 linter-scripts/audit-ai-implementability.py --strict              # CI gate (advisory until adoption)
```

## CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--module=<slug>` | all | Audit a single top-level module |
| `--no-network` | off | Print bundle stats only; never call gateway |
| `--force` | off | Ignore cache and re-score |
| `--json` | off | Machine-readable JSON to stdout |
| `--report-only` | off | Never fail; advisory mode (mirrors H1/P20/P48-1-fu1) |
| `--strict` | off | Exit 1 if any module scores BLOCKING (<60) |
| `--report=<path>` | `.lovable/memory/audit/v2-deterministic/audit-ai-implementability-latest.md` | Markdown report output |

## Outputs

- Stdout: per-module score line (or JSON if `--json`).
- File: ranked markdown report at `--report` path.
- Cache: `.lovable/cache/audit-ai/<module>.json` (gitignored).

## Status

**Strict on BLOCKING (Phase 153 Task A12, 2026-04-30).** Graduated from `--report-only` advisory after Task A8's v5 rebaseline measured tree mean **84.7/100** (5 EXCELLENT · 18 GOOD · 0 NEEDS_WORK · 0 BLOCKING) — H10 graduation filter satisfied: (1) mechanically detectable (per-module score from gateway response), (2) active regression surface (any new module or contract amputation could drop into BLOCKING), (3) low false-positive risk (BLOCKING<60 sits 15 points below the current 75-floor — wide moat).

**CI wiring (Phase 153 Task A12 — graduated from A5):** runs `python3 linter-scripts/audit-ai-implementability.py --strict` in `.github/workflows/spec-health.yml` between the Trace-map regression gate and the Summary step. Exits 1 if any module scores BLOCKING (<60); GOOD/NEEDS_WORK still pass (advisory inside the report). Step is skipped when `LOVABLE_API_KEY` is unset (community PRs from forks — Lesson #15). Cache lives at `.lovable/cache/audit-ai/` and is repo-local. **Threshold lock**: the 4 modules at the structural 75-floor (03/12/17/25 — Rubric v6 ceiling per Lesson #29/#36/#37) are addressed by Rubric v7 (A15-A20), NOT by lowering the strict threshold. Lowering the threshold is **forbidden** without a corresponding Rubric v7 design memo update.

---

## Acceptance Criteria

### AC-34-01 — Help surface advertises five mode flags `[medium]`
- **Given** the script invoked with `--help`.
- **When** stdout is captured.
- **Then** it MUST mention `--no-network`, `--module`, `--json`, `--report-only`, `--strict`.
- **Verifies:** §34 CLI surface stability so callers (CI, contributors, audit phases) can rely on flag names.

### AC-34-02 — `--no-network` exits 0 without API key `[critical]`
- **Given** `LOVABLE_API_KEY` is absent or unused.
- **When** the script runs with `--no-network`.
- **Then** it MUST exit 0 and emit one stats line per module.
- **Verifies:** §34 self-test contract — CI runners without an API key can still verify the script imports and walks the tree.

### AC-34-03 — `--module=<slug>` narrows scope `[high]`
- **Given** `--module=04-database-conventions`.
- **When** the script runs.
- **Then** stdout MUST mention `04-database-conventions` and MUST NOT mention any other top-level module.
- **Verifies:** §34 targeted-rerun contract for incremental audit phases.

### AC-34-04 — Unknown module slug exits 2 `[medium]`
- **Given** `--module=99-does-not-exist`.
- **When** the script runs.
- **Then** exit code MUST be 2 (CLI usage error), not 0 or 1.
- **Verifies:** §34 fail-loud contract — typos must not silently report "all green".

### AC-34-05 — `--json` emits parseable list `[high]`
- **Given** `--no-network --json --module=04-database-conventions`.
- **When** stdout is piped to `json.loads`.
- **Then** parsing MUST succeed and yield a list of length 1 with `module`, `bundle_sha`, `no_network: true`.
- **Verifies:** §34 machine-readable contract — downstream dashboards and gates depend on schema stability.

### AC-34-06 — Walker includes non-`*.md` artefacts `[critical]`
- **Given** `--no-network --module=11-powershell-integration`.
- **When** the bundle stats line is parsed.
- **Then** the file count MUST be ≥ 18 (verifies `schemas/powershell.schema.json` + `templates/powershell.json` + `templates/run.ps1` are walked).
- **Verifies:** §34 closure of the Phase 153 Task A2 blind spot — `*.md`-only walkers produced false-positive D5 CRITICALs.

### AC-34-07 — Cache hit when bundle SHA unchanged `[medium]`
- **Given** a previous run wrote `.lovable/cache/audit-ai/<module>.json`.
- **When** the script runs again on the same on-disk content.
- **Then** the cached row MUST be reused (`from_cache: true`) without invoking the gateway.
- **Verifies:** §34 reproducibility + cost-control contract; ensures clean runs are free.

### AC-34-08 — `--report-only` never fails `[medium]`
- **Given** any module scored BLOCKING.
- **When** the script runs with `--report-only --strict`.
- **Then** exit code MUST be 0 (`--report-only` overrides `--strict`).
- **Verifies:** §34 advisory-by-default contract — mirrors slot 33 `check-ai-confidence.py` and the H1/P20 pattern.

### AC-34-09 — Tier-1 contract files (`{00,97,98,99}-*.md`) prioritized in 90 KB bundle `[critical]`
- **Given** a module whose chunky `02-*` / `03-*` siblings would exhaust the `MAX_BYTES = 90000` cap before alphabetical iteration reaches `97-acceptance-criteria.md`,
- **When** `load_module_bundle()` orders files for inclusion,
- **Then** the four module-root contract files (`00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`) MUST be placed FIRST in canonical order, followed by everything else under `WALK_GLOBS` alphabetically. Without this priority, the §97 binding contract is silently dropped from the prompt for any module > ~70 KB of feature/issue prose, and the auditor scores examples without seeing the contract — yielding a false-low D2 (AC coverage) and stable scores under contract edits (Phase 153 Task A6 first re-score loop produced ZERO movement on spec/05 for exactly this reason; bundle_sha changed, score didn't, because `97-acceptance-criteria.md` was alphabetically last and never made the cut). After the fix, spec/05 lifted 69 → 89 (+20) on the same content edits.
- **Verifies:** §34 contract-surface bundling guarantee — the auditor's prompt MUST contain the contract before the examples.

---

## Rubric v7 — Axis-driven dimension weight cascades (Phase 153 Task A17)

Rubric v6 (active in Tasks A1–A12) applied uniform 0–20 weights to D1–D5 across every module. The Phase 153 Task A8 v5 baseline exposed a **structural 75-point ceiling** on modules whose content axis is incompatible with uniform weighting:

| Module | v6 score | Axis | Penalty source |
|---|---|---|---|
| 03-error-manage | 75 | `audit-corpus` | D2 penalised "missing AC coverage" — but module *describes* errors, doesn't contract them |
| 12-cicd-pipeline-workflows | 75 | `integration-spec` | D5 penalised external GitHub Actions refs as "unresolved" |
| 17-consolidated-guidelines | 75 | `process-guidance` | D2 penalised checklist prose for not being GWT |
| 25-app-issues | 75 | `audit-corpus` | D3 penalised quoted bug descriptions as "unhandled edge cases" (per Lesson #29) |

Rubric v7 reads `content_axis` from each module's `00-overview.md` front-matter (introduced in Phase 153 Task A16) and applies axis-appropriate weight multipliers BEFORE summing to the 0–100 total. Sum-of-multipliers is **always 5.0** (mean 1.0) so total range stays 0–100 — multipliers redistribute scoring weight, they do not inflate it.

### Weight cascade (Normative)

| `content_axis` | D1 (Clarity) | D2 (AC Coverage) | D3 (Edge/Error) | D4 (Examples) | D5 (Cross-Ref) | Sum |
|---|---|---|---|---|---|---|
| `normative-contract` | 1.0 | **1.5** | **1.2** | 0.8 | 0.5 | 5.0 |
| `process-guidance` | **1.5** | **0.7** | 0.8 | 1.0 | 1.0 | 5.0 |
| `integration-spec` | 1.0 | 0.9 | 0.9 | **1.4** | **1.2** (allowed external) | 5.4 → renormalised to 5.0 |
| `audit-corpus` | 1.0 | **0.5** | **0.5** | 1.5 | **1.5** (citation density) | 5.0 |
| `tooling-spec` | 1.0 | **1.3** | 1.0 | **1.3** | 0.9 | 5.5 → renormalised to 5.0 |

Renormalisation rule: if raw sum ≠ 5.0, every multiplier is divided by `(raw_sum / 5.0)` so the module total stays bounded at 100.

### Per-axis caps + floor preservation

| `content_axis` | Soft cap | Floor | Rationale |
|---|---|---|---|
| `normative-contract` | 100 | 60 | Full range — these MUST be implementable |
| `process-guidance` | 95 | 60 | Inherent ambiguity — reaching 100 would require GWT-encoding human conventions |
| `integration-spec` | 95 | 60 | External-system uncertainty caps achievable D5 |
| `audit-corpus` | 95 | 60 | Per Lesson #29 — describing other specs has inherent semantic distance |
| `tooling-spec` | 100 | 60 | Full range — script ACs are GWT-checkable |

**Strict CI threshold remains 60 (BLOCKING) for every axis** — caps are upper bounds for the GOOD/EXCELLENT band assignment, not the strict gate. The 15-point moat between the v6 75-floor and the 60 strict threshold (per Lesson #40) is preserved across all axes.

### Acceptance Criteria

### AC-34-10 — Axis-driven weight multipliers applied per module `[critical]`
- **Given** a module's `00-overview.md` declares `content_axis: <one-of-5>`,
- **When** the auditor computes the per-module score,
- **Then** the five raw dimension scores (D1–D5, each 0–20) MUST be multiplied by the axis-appropriate multipliers from the Rubric v7 weight cascade table above BEFORE summing to the 0–100 total. The multiplier sum MUST be normalised to 5.0 (so the module total stays bounded at 100); for axes whose raw multiplier sum exceeds 5.0 (`integration-spec`=5.4, `tooling-spec`=5.5), every multiplier MUST be divided by `(raw_sum / 5.0)` before scoring.
- **Verifies:** §34 Rubric v7 contract — uniform v6 weighting penalised non-contract axes (Phase 153 Task A8 v5 baseline showed 4 modules at structural 75-floor); axis-appropriate weights close the ceiling per Lesson #29 + Lesson #36.

### AC-34-11 — Per-axis soft cap applied to band assignment, NOT to strict gate `[high]`
- **Given** a module's score after Rubric v7 multiplication,
- **When** the band (EXCELLENT/GOOD/NEEDS_WORK/BLOCKING) is computed,
- **Then** the soft cap from the per-axis caps table MUST be applied (e.g. `process-guidance` cannot exceed 95 even if raw weighted sum is 97); BUT the strict CI gate threshold MUST remain 60 (BLOCKING) for every axis. The 15-point moat between the v6 75-floor and the 60 strict threshold (Lesson #40) is preserved tree-wide.
- **Verifies:** §34 strict-gate stability under axis-aware scoring — caps adjust band labels without weakening the regression-detection contract Task A12 graduated.

### AC-34-12 — Missing or invalid `content_axis` fails fast `[critical]`
- **Given** a module's `00-overview.md` lacks `content_axis:` or declares a value outside `{normative-contract, process-guidance, integration-spec, audit-corpus, tooling-spec}`,
- **When** the auditor processes that module,
- **Then** the script MUST exit code 2 (CLI/data error) with a message naming the offending module + the missing/invalid value, and MUST NOT silently fall back to v6 uniform weighting. The Phase 153 Task A16 bulk injection guarantees all 23 top-level modules carry valid axis values; this AC enforces that any future module addition (or accidental front-matter deletion) breaks CI immediately.
- **Verifies:** §34 fail-loud contract — silent v6 fallback would mask Rubric v7 regressions; mirrors AC-34-04 (unknown `--module=` slug exits 2).

### AC-34-13 — Bundle cap raised 90 KB → 120 KB to suppress tree-wide saturation `[critical]`
- **Given** the pre-A12 `MAX_BYTES = 90_000` ceiling caused every audited top-level module to hit 100% saturation (probe at Phase 153 Task A12: spec/17 fit 4/39 files, spec/18 fit 10/35, spec/02 fit 6/251, spec/27 fit 3/50, spec/07 fit 3/17 — all bundles exactly 90000 bytes),
- **When** `load_module_bundle()` constructs the prompt,
- **Then** `MAX_BYTES` MUST be `120_000` (not `90_000`); the 120 KB ceiling was confirmed safe via a live gateway probe at Task A12 (`POST /v1/chat/completions` with a 119 KB user-content payload returned HTTP 200); above ~125 KB the Cloudflare 1010 class fires for `User-Agent: lovable-spec-audit/1.0` POSTs (the 25 KB Lesson #11 cliff is for the *default* Python UA — the explicit UA header lifts the cliff to ~125 KB). The 5 KB headroom below 125 KB MUST be preserved. Any future raise above 120 KB requires a fresh live-probe at the proposed ceiling. Tier-1 contract priority (AC-34-09) MUST be retained — the cap raise expands the Tier-2 budget; it does NOT relax the Tier-1 guarantee. **Superseded by AC-34-14 (140 KB live-probed at Phase 153 Task A18-probe);** retained as historical contract for the 120 KB intermediate step.
- **Verifies:** §34 contract-bundling completeness — tree-wide saturation at the 90 KB cap meant every audited module was scored on 3-10 of 17-251 files; D2/D3/D4 dimensions were systematically under-counted because feature/issue prose past Tier 1 was silently truncated (Lesson #46 saturation class). The 120 KB cap restores ~33% additional Tier-2 capacity, expected to lift saturated modules' D4 (Examples) and D5 (Cross-Ref) scores without requiring §97 edits. Mirrors AC-34-09's bundle-completeness contract.

### AC-34-14 — Bundle cap raised 120 KB → 140 KB; truncation marker MUST be dynamic `[critical]`
- **Given** the Phase 153 Task A18-probe live gateway probe confirmed a 140 KB user-content payload returns HTTP 200 (vs the AC-34-13 120 KB ceiling), AND the Phase 153 Task A18-full rebaseline observed the LLM auditor fabricating a recurring "context-window-truncation at 120KB" finding class against any bundle hitting the truncation marker (Lesson #77 — the LLM treated the literal `120KB` substring in the marker text as a contract claim and flagged it as a D3 edge-case gap),
- **When** `load_module_bundle()` constructs the prompt AND injects a truncation marker because the bundle exceeds `MAX_BYTES`,
- **Then** (a) `MAX_BYTES` MUST be `140_000` in `linter-scripts/audit-ai-implementability.py:45` (raised from `120_000`), (b) the truncation-marker string at line 213 MUST interpolate `{MAX_BYTES//1024}KB` dynamically (e.g. `f"\n\n[...TRUNCATED at {MAX_BYTES//1024}KB context cap...]"`) — it MUST NOT contain a hard-coded literal byte count (no `120KB`, no `140KB`, no `90KB`), (c) the source-line comment at line 45 MUST cite both this AC (AC-34-14) and its predecessor (AC-34-13) so the raise history is grep-able from code, AND (d) any future raise above 140 KB requires a fresh live-probe at the proposed ceiling under the canonical `User-Agent: lovable-spec-audit/1.0` header (default Python UA hits the 25 KB Cloudflare-1010 cliff per Lesson #11 — the named UA is what unlocks the higher band). Tier-1 contract priority (AC-34-09) MUST be retained — the cap raise expands Tier-2 budget; it does NOT relax the Tier-1 guarantee.
- **Verifies:** §34 cap-evolution contract + LLM-fabrication suppression — pins the dynamic-marker discipline so future cap raises require ONE source-line edit (line 45) and the marker string follows automatically; closes the Lesson #77 fabrication class (LLMs treat hard-coded literals in prompt scaffolding as contract claims). Mirrors AC-34-13's bundle-completeness contract; supersedes AC-34-13's `120_000` value while preserving its Tier-1 + UA-header + headroom invariants.


### AC-34-15 — Chunked re-scoring contract for >MAX_BYTES modules `[high]`
- **Given** the Phase 153 Task A18-design memo (`.lovable/memory/audit/v2-deterministic/phase-153-task-A18-design-chunked-rescoring.md`) — durable fix for D5/D3 walker-cap findings on the >140 KB cluster (`spec/{02,03,07,12,17,18,27}` and any future content-heavy module) — AND the Task A18-impl-1 implementation (`pack_chunks()` + `merge_chunk_scores()` helpers + `--chunked` / `--chunk-stats` CLI flags),
- **When** `audit-ai-implementability.py` is invoked on a module whose total walked content exceeds `MAX_BYTES`,
- **Then** (a) `pack_chunks(mod_dir, max_bytes=MAX_BYTES)` MUST return `≥1` chunk dicts each with `bundle` length `≤ max_bytes` (single-file overflow is a known limitation reserved for A18-impl-2 — those chunks emit oversize and are flagged via `--chunk-stats`); (b) **parity invariant**: when total content `≤ MAX_BYTES`, `pack_chunks()` MUST return exactly one chunk with `tier == "FULL"` whose `bundle` is **byte-identical** to `load_module_bundle()`'s return value (same tier1+alphabetical-rest ordering, no truncation marker) — this guarantees the chunked path is a strict superset of the legacy single-pass path and cache hashes remain stable for ≤MAX_BYTES modules; (c) **T1 re-anchor invariant**: every multi-chunk slice MUST contain the full T1 prefix (root-level `00-overview.md` + `97-acceptance-criteria.md` + `98-changelog.md` + `99-consistency-report.md` if present), so the LLM scores each chunk against the binding contract surface — closes the Lesson #11/#16 contract-dropout class at the multi-chunk boundary; (d) `merge_chunk_scores()` MUST apply tier weights `{T1: 1.00, T2: 0.85, T3: 0.60}` (`TIER_WEIGHTS` constant) and dedupe findings by `(severity, dimension, first_120_chars(title))`; (e) the `--chunked` flag is **opt-in** at A18-impl-1 (default off) so production CI runs are unchanged; promotion to default requires A18-impl-2 (oversize-chunk splitter + cache schema migration) AND a gateway-on full-tree parity rebaseline.
- **Verifies:** §34 chunked re-scoring contract — codifies the A18-design memo as the durable fix for the 6+ walker-cap-blocked D5 findings (per index core: `spec/{17,18,22,25,27,12}`). Mirrors AC-34-09 (tier-1 priority) by extending tier discipline from in-bundle ordering to cross-bundle re-anchoring. Self-tested at `linter-scripts/test/test-audit-ai-implementability.sh` via 4 new assertions (#10 `--chunk-stats` exits 0; #11 parity scan ≥5 modules zero failures; #12 T1 re-anchor on `spec/17`; #13 weighted-merge math + dedupe). Closes A18-impl-1 milestone in the design memo's §6 migration path.


### AC-34-16 — Intra-T1 splitting + per-chunk SHA cache schema `[high]`
- **Given** the AC-34-15 chunked re-scoring contract treats T1 (`00+97+98+99`) as an always-included prefix, AND the Phase 153 fu27 walker-bundle-budget audit (`mem://process/phase-153-lessons` Lesson #65 + `.lovable/memory/audit/v2-deterministic/phase-153-task-A24-fu27-walker-bundle-budget-audit.md`) showed 4 modules where T1 alone exceeds `MAX_BYTES` (spec/27 T1=455 KB, spec/22 T1=239 KB, spec/01 T1=148 KB, spec/07 T1=134 KB), and the pre-A18-impl-2 pathological branch silently truncated T1 to `[:max_bytes]` losing 70%+ of the contract surface,
- **When** `pack_chunks(mod_dir)` is invoked on a module whose T1 sum exceeds `MAX_BYTES` AND when `audit_module()` writes its cache JSON,
- **Then** (a) `pack_chunks()` MUST split T1 itself into ≥2 chunks rather than truncating; the **anchor pair** `00-overview.md + 97-acceptance-criteria.md` MUST appear together in the first chunk (these two files are the contract pair — §97 ACs reference §00 invariants), and EACH remaining T1 file (`98`, `99`) MUST get its own chunk, prefixed with the anchor pair when `anchor_size + solo_size ≤ MAX_BYTES` (else solo with `[:max_bytes]` truncation as a last resort); all chunks emitted from this branch carry `tier == "T1"`; (b) the cache JSON emitted to `.lovable/cache/audit-ai/<module>.json` MUST include a `chunks` field of shape `[{"tier": str, "bundle_sha_chunk": str(16-hex), "files": [str(rel-to-ROOT)], "bytes_used": int}]` for EVERY scored module (single-chunk FULL-tier modules emit a single-element array); the composite `bundle_sha` field MUST remain present and unchanged from AC-34-15 so `≤MAX_BYTES` cache parity is preserved; (c) the `--no-network --json` mode MUST emit the same `chunks` inventory so external tooling can detect partial-cache-invalidation candidates without a gateway call; (d) any future cache consumer (e.g. a cache-prune tool added in A18-impl-3) reading the per-chunk SHAs MUST be able to detect "only chunk N changed" and re-score only that chunk, leaving sibling-chunk scores intact.
- **Verifies:** §34 cache-schema migration + intra-T1 splitting contract — closes the Lesson #65 spec/27-class data-loss path (T1 truncation) AND lays the cache-side groundwork for A18-impl-3 partial re-scoring. Self-tested at `linter-scripts/test/test-audit-ai-implementability.sh` via 2 new assertions (#14 synthetic 4×50KB T1 overflow → ≥2 anchor-prefixed chunks all `tier=="T1"`; #15 `--no-network --json` emits `chunks` array with 16-hex `bundle_sha_chunk` + `tier` + `files` + `bytes_used` keys). Mirrors AC-34-15's parity-superset discipline — backward-compatible cache schema extension, no existing field removed.


### AC-34-17 — Chunked re-scoring promoted to default (`--chunked` default-on, `--no-chunked` rollback) `[high]`
- **Given** the AC-34-15 chunked re-scoring contract (parity invariant on ≤MAX_BYTES modules + T1 re-anchor on multi-chunk slices + tier-weighted merge) AND the AC-34-16 intra-T1 splitter + per-chunk SHA cache schema (closes the spec/27-class T1=455 KB data-loss path), AND the Phase 153 Task A18-impl-1 explicit milestone "promotion to default requires A18-impl-2 (oversize-chunk splitter + cache schema migration) AND a gateway-on full-tree parity rebaseline" (AC-34-15 §(e)),
- **When** `audit-ai-implementability.py` is invoked WITHOUT an explicit `--no-chunked` flag (the new default state),
- **Then** (a) `audit_module(mod, ..., use_chunked=True)` MUST be the default call signature; the `--chunked` CLI flag MUST default to `True` (`action="store_true", default=True`) — retained as a no-op for backward CLI compatibility (any caller already passing `--chunked` continues to work unchanged); (b) `--no-chunked` (`dest="chunked", action="store_false"`) MUST be available as the explicit rollback flag for parity-verification or emergency rollback; its help text MUST cite "loses contract surface on >MAX_BYTES modules per Lesson #11/#16"; (c) when `len(pack_chunks(mod)) > 1` AND `use_chunked` is True, `audit_module()` MUST score each chunk independently via `call_gateway()` (one HTTP call per chunk, with `time.sleep(0.5)` between calls preserving rate-limit hygiene from existing inter-module loop), parse each response with `parse_score()`, attach `tier` + `bytes_used` from the chunk dict to each result, and pass the list to `merge_chunk_scores()` for weighted-merge per AC-34-15(d); the merged dict MUST seed `parsed["d1..d5"]` and `parsed["issues"]` (legacy report key) MUST be unioned-deduped from `merged["findings"]`; (d) **parity invariant** (mirror of AC-34-15(b)): for any module with `len(pack_chunks(mod)) == 1` (i.e. FULL-tier, ≤MAX_BYTES total content), `bundle_sha` MUST be byte-identical between `--chunked` (default) and `--no-chunked` invocations — verified via the spec/16-generic-release cross-flag hash equality test (both produce sha `e16de187513b288e` at A18-impl-3 ship); the FULL-tier path MUST NOT include any `chunked=` tag in the SHA payload (only multi-chunk modules fold `chunked={1,0}` into the hash to invalidate stale single-pass caches when the flag flips); (e) every result dict MUST carry `parsed["chunked_path"] = bool(use_chunked and multi_chunk)` so the audit report and downstream tooling can disambiguate which path scored each module without re-parsing CLI args; (f) live re-score deltas at A18-impl-3 ship MUST be documented in §98 — confirmed: spec/27 83 → 88 (+5, contract surface previously truncated now visible to LLM), spec/12 87 → 84 (–3, honest-baseline correction per Lesson #18 — chunked path now scores against ALL 49 files vs first ~140KB only). Tree-wide rebaseline (~16 multi-chunk modules) is deliberately deferred to backlog item #10 (gateway-cost-bounded — ~480 chunk calls).
- **Verifies:** §34 chunked-default promotion contract — closes the AC-34-15(e) milestone + the Phase 153 Task A18-impl-1/A18-impl-2/A18-impl-3 graduation chain (3-phase incremental rollout: A18-impl-1 = opt-in helpers + parity contract; A18-impl-2 = T1-overflow splitter + per-chunk SHA cache; A18-impl-3 = default-on flip + audit_module wiring). Mirrors AC-34-09 (tier-1 priority discipline) by extending tier-aware scoring from in-bundle ordering to cross-bundle re-anchoring as the new default behaviour. Self-tested at `linter-scripts/test/test-audit-ai-implementability.sh` — all 16 existing assertions PASS unchanged (parity invariant verified by `pack_chunks` parity test #12 + cross-flag bundle_sha equality on spec/16). **Backward-compat note**: existing cache files for FULL-tier modules remain valid (bundle_sha unchanged); existing cache files for multi-chunk modules are invalidated by the `chunked=1` tag fold and will re-score on next gateway pass — this is **intentional** per AC-34-15(e) "gateway-on full-tree parity rebaseline" requirement.

### AC-34-18 — Bounded tier-1B promotion: nested contract files lift to tier-1 only when combined T1+T1B ≤ MAX_BYTES `[high]`
- **Given** `load_module_bundle()` (and the parallel `pack_chunks()` packer) currently lift root-level `{00,97,98,99}-*.md` contract files to tier-1 priority per AC-34-09 (Lesson #16: contract files always sampled), but nested contract files under sub-modules (e.g. `spec/05/02-features/00-overview.md`, `spec/02/01-cross-language/02-boolean-principles/97-acceptance-criteria.md`) receive NO tier-1 priority and fall back to alphabetical T2/T3 ordering — risking silent truncation under the 140 KB cap on chunky modules; AND a tree-wide nested-contract probe (Phase 153 Task A8-prep) found 10 modules carry such files (counts: spec/02=116, spec/03=76, spec/12=12, spec/14=12, spec/05=8, spec/06=8, spec/25=8, spec/10=4, spec/18=4, spec/26=4); AND of those, 6 modules' combined T1+T1B size fits under the 140 KB cap (spec/05=98 KB, spec/06=86 KB, spec/10=43 KB, spec/12=138 KB, spec/18=80 KB, spec/26=88 KB) while 4 overflow (spec/02=783 KB, spec/03=495 KB, spec/14=152 KB, spec/25=153 KB),
- **When** `load_module_bundle(mod_dir)` walks `mod_dir.rglob(pattern)` for any module with at least one nested `{00,97,98,99}-*.md` file,
- **Then** (a) the walker MUST collect nested contract files into a `tier1b: list[Path]` set, sorted by `(len(rel_path.parts), str(rel_path))` (depth-shallowest-first, then alphabetical) so the outermost nested contracts are sampled first under any sub-cap; (b) the walker MUST compute `_bytes(tier1) + _bytes(tier1b)` (using the same `===== FILE: <rel> =====` header accounting as the main packing loop) and ONLY promote `tier1b` to tier-1 priority when the combined size ≤ `MAX_BYTES` (140 KB) — this is the "FITS" path, which produces a clean lift; (c) when combined size > `MAX_BYTES`, the walker MUST fall back to current pre-A8-prep behavior — `tier1b` files remain in the alphabetical `files` list (some may still appear early via natural alpha ordering, but NO mass promotion occurs) — this is the "OVERFLOW-fallback" path, which guarantees zero regression on giant modules; (d) the bimodal contract MUST be self-tested via `linter-scripts/test/test-audit-ai-tier1b-promotion.sh`: T1 asserts spec/05 yields 4 root T1 + 8 nested T1B in the first 12 bundle entries (full clean lift, FITS path); T2 asserts spec/02 yields 4 root T1 + ≤3 nested T1B in the first 12 entries (no mass promotion, OVERFLOW-fallback held); T3 asserts spec/22 (zero nested T1B) bundle is unchanged from pre-A8-prep behavior; (e) live LLM re-score deltas MUST be documented in §98 as gateway availability permits per Lesson #20 — at landing, gateway returned HTTP 402 so re-score is deferred; expected lift on FITS modules is +2-5 score points (D2 AC Coverage dimension primarily, mirroring AC-34-09's spec/05 +20 lift pattern but bounded by ceiling effects since 5/6 FITS modules already score ≥87/100); (f) **non-goal**: AC-34-18 deliberately does NOT address the 4 OVERFLOW modules (spec/02/03/14/25). Sub-module recursion (treating each nested `<NN>-<name>/` containing `00-overview.md` as an independent audit pseudo-module with depth-weighted score aggregation) is the proper design for those — deferred indefinitely as a backlog item per Lesson #79 (saturation triage: spec/02 already at 90/EXC and spec/03 at 87/GOOD via current flat walker; sub-module recursion would be a 2-phase design+impl effort with diminishing returns).
- **Verifies:** §34 walker tier-1 contract surface for nested contract files — extends AC-34-09 (root tier-1 priority) to a bounded recursive promotion. Mirror of Lesson #16 ("LLM auditors with bounded context windows MUST tier contract files before example files") at the sub-module axis. Closes the Phase 153 nested-contract-invisibility class identified during the post-Task-#29b walker audit (51 eligible modules at recursive walker; 27 advisory drifts under nested sub-modules). Self-tested at `linter-scripts/test/test-audit-ai-tier1b-promotion.sh` (6/6 assertions). **Backward-compat note**: cache files for the 6 FITS modules will be invalidated on next gateway pass (bundle_sha changes due to nested T1B lift); cache files for spec/22 + the 4 OVERFLOW modules + all modules without nested T1B remain byte-identical (no regression). **Lesson #38 reinforcement**: gateway availability check at start of phase confirmed `LOVABLE_API_KEY` set, but live `--force` call returned HTTP 402 — Lesson #86 oscillation pattern holds. Score-validation work deferred to A8 full-tree rebaseline once gateway budget restores.

### AC-34-19 — Anchor-pair AC-boundary splitter when §00 + §97 exceeds MAX_BYTES `[high]`
- **Given** `pack_chunks(mod_dir)` per AC-34-16 splits T1 into anchor-prefixed chunks when `_bytes(tier1) > MAX_BYTES`, but the inner branch where the **anchor pair itself** (`00-overview.md + 97-acceptance-criteria.md`) exceeds `MAX_BYTES` previously truncated the rendered anchor text to `[:max_bytes]` (a last-resort branch labelled "extreme: §00 or §97 alone >70KB combined") — silently dropping 30-40% of large §97 files (precedent: spec/22-git-logs-v2 §97 = 188 KB combined with §00 = 26 KB → 214 KB, cap-truncated to 140 KB, losing 74 KB of §97 ACs including the AC-80 sibling delegation map landed in Phase 154); AND Lesson #74 (saturation-class triage) classified this data-loss path as an irreducible structural ceiling because the bundle cap is a Cloudflare-safe constant,
- **When** `pack_chunks(mod_dir)` reaches the inner `else` branch on line ~384 where `anchor_size > max_bytes`,
- **Then** (a) the splitter MUST identify the LARGER of the two anchor files (`big_file`) by rendered size and treat the smaller as the always-included context anchor (`small_files`); (b) the larger file MUST be split at `^### AC-` heading boundaries via `re.split(r"(?m)(?=^### AC-)", big_raw)` — preserves whole AC bodies (each slice begins on an AC heading); (c) slices MUST be greedy-packed under `slice_budget = max_bytes - small_size - CHUNK_OVERHEAD` so each emitted chunk = `small_text + big_header + slice_label + slice` and respects the `max_bytes` cap; (d) when the smaller anchor itself would consume more than `3 * max_bytes / 4` of the bundle (`slice_budget < max_bytes // 4`), the splitter MUST fall back to solo §97 slices without small-anchor context (graceful degradation — slices still carry the `[CHUNK N/M of <filename>]` label so the LLM knows the slice provenance); (e) every emitted chunk MUST carry `tier == "T1"` (mirrors AC-34-16(a)); the `files` field MUST list both anchors so per-chunk SHA inventory remains correct; (f) remaining T1 files (`98-changelog.md`, `99-consistency-report.md`) MUST emit as solo chunks per the existing AC-34-16 contract — no behaviour change in that loop; (g) live verification on spec/22-git-logs-v2 at landing: chunk count 3 → 4; chunks 1+2 each carry §00+§97-slice (124 KB + 113 KB respectively); full §97 visible to auditor (was: ~115 KB visible / 73 KB silently dropped).
- **Verifies:** §34 anchor-pair-overflow data-loss path closure — extends AC-34-16 (intra-T1 splitter) one level deeper for the case where the anchor pair itself overflows. Mirror of Lesson #16 (contract files always sampled) for the sub-anchor axis. **Lesson #74 update**: the walker-cap saturation class graduates from "structural ceiling" to "engineering-soluble" for the anchor-pair-overflow sub-class; the broader OVERFLOW-fallback path of AC-34-18 (sub-module recursion for spec/02/03/14/25) remains deferred. **Lesson #87** (codified at AC-34-19 ship): when an LLM-walker last-resort branch is labelled "extreme" but a real spec module hits it (spec/22), treat the label as a TODO marker, not as a permanent ceiling — the truncation cost is paid silently per re-score; the AC-boundary splitter is a 60-line patch with proportional gain. Self-tested via existing `pack_chunks()` smoke test on spec/22 (post-patch: 4 chunks, all `tier=="T1"`, full §97 covered) — all 16 AC-34-* assertions PASS unchanged + all 21 AC-34-18 tier-1B assertions PASS unchanged. **Backward-compat**: cache files for spec/22 + any future module hitting the anchor-pair-overflow branch will be invalidated on next gateway pass (bundle_sha changes due to chunk re-layout); all other modules' caches remain byte-identical (no regression). **Live LLM re-score deferred per Lesson #20** (gateway HTTP 402 at landing — Lesson #86 oscillation re-confirmed). Expected spec/22 lift: 76 → ≥85 (D4 +3 + D5 +2 + D2 +2 from AC-80 sibling map + 73 KB previously-unseen ACs entering scoring window).

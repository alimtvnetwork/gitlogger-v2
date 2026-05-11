# 31 — audit-spec-vs-code-v2.py

**Version:** 1.24.0  
**Updated:** 2026-04-27  
**Source:** [`linter-scripts/audit-spec-vs-code-v2.py`](../../linter-scripts/audit-spec-vs-code-v2.py) (script **v2.23**) + [`linter-scripts/test/test-audit-cli-thresholds.sh`](../../linter-scripts/test/test-audit-cli-thresholds.sh) (Phase 91) + [`linter-scripts/test/test-audit-explain-contract.sh`](../../linter-scripts/test/test-audit-explain-contract.sh) (Phase 94) + [`linter-scripts/test/test-audit-deterministic-stability.sh`](../../linter-scripts/test/test-audit-deterministic-stability.sh) (Phase 95) + [`linter-scripts/test/README.md`](../../linter-scripts/test/README.md) (Phase 98) + [`linter-scripts/test/test-readme-inventory.sh`](../../linter-scripts/test/test-readme-inventory.sh) (Phase 102) + [`linter-scripts/test/test-qa-baseline-footer.sh`](../../linter-scripts/test/test-qa-baseline-footer.sh) (Phase 103) + [`linter-scripts/check-memo-retrospective-headings.py`](../../linter-scripts/check-memo-retrospective-headings.py) (Phase 104) + [`package.json`](../../package.json) grammar-defining-library pin block (Phase 105) + multi-file enumeration parity contract (Phase 109) + [`linter-scripts/test/test-overview-inventory-parity.sh`](../../linter-scripts/test/test-overview-inventory-parity.sh) (Phase 112) + [`linter-scripts/test/test-weights-parity.sh`](../../linter-scripts/test/test-weights-parity.sh) (Phase 113) + folder-reference gate wiring (Phase F2)  
**Category:** Auditor (AI-driven by default; **deterministic mode** + **hard scoring gates** + **CI threshold flags** + **--explain debugger** + **CLI contract self-tests** ×7 incl. determinism + README parity + footer parity + §27 inventory parity triangle + WEIGHTS dimension-table parity + **inventory README** + **QA-baseline footer** + **memo retrospective-heading meta-linter** + **grammar-library pin contract** + **multi-file enumeration parity contract**)
**Predecessor:** §30 [`30-audit-spec-vs-code.md`](./30-audit-spec-vs-code.md)


**Test pair:** N/A — audit-aid  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

AI-implementability audit. Asks: *"Could a mediocre AI ship a working implementation from this spec alone with zero human clarification?"*

## Methodology

1. Broader code index: `linter-scripts/` + `.github/` + `src/` presence.
2. Deterministic pre-checks computed BEFORE AI scoring (so AI can be calibrated):
   - waffle ratio (should/may/might/optionally per 1k chars) — **prose only** (v2.4)
   - contract presence (DDL, JSON, TS enums, YAML/OpenAPI, Mermaid)
   - cross-spec link health (broken count) — **prose only** (v2.6); links inside fenced code blocks (e.g. `markdown` template examples) are excluded
   - AC count + Given/When/Then block count
   - TODO/TBD/FIXME density — **prose only** (v2.4); tokens inside fenced code blocks and inline `code` spans are excluded
3. AI receives metrics + raw digest, must justify scores against them.
4. Outputs blast-radius (0–10): how many other specs would benefit from fixing this one.

## Weights

| Dimension | Weight |
|-----------|-------:|
| Implementability | 35% |
| Completeness | 20% |
| Alignment | 15% |
| Consistency | 10% |
| Clarity | 10% |
| Testability | 7% |
| Maintainability | 3% |

## Usage

```bash
python3 linter-scripts/audit-spec-vs-code-v2.py                                    # AI mode
AUDIT_ONLY="22-git-logs-v2" python3 linter-scripts/audit-spec-vs-code-v2.py        # smoke test one module
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py              # deterministic mode
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py \
    --min-weighted=97 --min-impl=99                                                # CI threshold gate (v2.12)
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py \
    --explain=27-spec-toolchain                                                    # rubric trace for one module (v2.16)
```

### CLI flags

| Flag | Type | Since | Effect |
|------|------|-------|--------|
| `--min-weighted=N` | int 0–100 | v2.12 (Phase 81) | Exit non-zero when the **mean weighted score** across all audited modules falls below `N`. Stderr emits `✗ FAIL: weighted mean X < threshold N`. |
| `--min-impl=N` | int 0–100 | v2.12 (Phase 81) | Exit non-zero when the **mean implementability score** falls below `N`. Stderr emits `✗ FAIL: implementability mean X < threshold N`. |
| `--explain=<substring>` | string | v2.16 (Phase 90) | Short-circuits the normal audit loop. For the first module whose relative path under `spec/` contains `<substring>`, prints: rubric branch, all bonuses fired with deltas, all gates capping any dimension (with before/after), per-dimension scores (raw vs final + Δ + contribution), and key metrics. Pure-add diagnostic — does not write files, does not call AI. Exits `0` if a match was found, `1` otherwise. Multi-match lists first 5 candidates and uses the first. |

When at least one threshold is supplied AND none fail, stderr emits `✓ PASS: thresholds met`. When neither flag is supplied the script preserves its pre-v2.12 behaviour (exit 0 unless an AI-mode module errored). Used by the `spec-health.yml` workflow audit gate (currently `--min-weighted=97 --min-impl=99`, set in Phase 84).

## Modes

| Mode | Trigger | Output dir | Reproducibility |
|------|---------|------------|-----------------|
| AI (default) | no env var | `.lovable/memory/audit/v2/` | Non-deterministic (model-dependent) |
| Deterministic | `AUDIT_DETERMINISTIC=1` | `.lovable/memory/audit/v2-deterministic/` | **Byte-identical** across runs |

Deterministic mode bypasses the AI gateway entirely and scores each module from a pure-function rubric over the same `deterministic_metrics()` digest used in AI mode. JSON output is sorted by module name, written with `sort_keys=True`, uses ASCII encoding, and ends with a single trailing newline — guaranteeing identical SHA-256 across consecutive runs on the same spec tree.

## Environment variables

| Var | Purpose |
|-----|---------|
| `LOVABLE_API_KEY` | Required in AI mode — Lovable AI Gateway credential |
| `AUDIT_ONLY` | Substring filter; only audit modules whose path matches |
| `AUDIT_DETERMINISTIC` | `1`/`true`/`yes` → enable deterministic mode (no AI calls) |

## Outputs

- `<output-dir>/<module>.md` per module (overwritten).
- `<output-dir>/00-index.md` — full ranking + blast-radius leaderboard.
- `<output-dir>/EXECUTIVE-SUMMARY.md` — TL;DR.
- `<output-dir>/raw-results.json` — machine-readable; byte-identical across runs in deterministic mode.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Audit complete |
| 1 | At least one module failed AI scoring (others still written) |
| 2 | `LOVABLE_API_KEY` missing (AI mode only) |

## Acceptance criteria

### AC-31-01 — Output lives under `v2/` subfolder
- **Given** a successful run,
- **When** `.lovable/memory/audit/` is listed,
- **Then** all v2 outputs MUST be inside the `v2/` subfolder (not mixed with v1).

### AC-31-02 — Implementability dominates the weighted score
- **Given** the rubric in code,
- **When** weights are summed,
- **Then** `implementability` MUST equal 35 and total MUST equal 100 (asserted at module load).

### AC-31-03 — Deterministic metrics include `.mmd` files
- **Given** a module folder containing `.mmd` files (e.g. `26-gitlogs-diagrams`),
- **When** the audit runs,
- **Then** `metrics.mmd_files` MUST equal the count of `.mmd` files and `metrics.has_mermaid` MUST be `true`.

### AC-31-04 — Blast-radius leaderboard surfaces foundational specs
- **Given** the generated `00-index.md`,
- **When** the "High blast-radius fixes" table is read,
- **Then** entries MUST be sorted by `(-blast_radius, weighted_overall)` (highest blast first).

### AC-31-05 — `AUDIT_ONLY` smoke test mode
- **Given** `AUDIT_ONLY="22-git-logs-v2"`,
- **When** the script runs,
- **Then** exactly one module MUST be audited.

### AC-31-06 — Deterministic mode produces byte-identical JSON
- **Given** `AUDIT_DETERMINISTIC=1` and an unchanged spec tree,
- **When** the script is run twice consecutively,
- **Then** `.lovable/memory/audit/v2-deterministic/raw-results.json` from both runs MUST have the same SHA-256 hash and identical byte length.

### AC-31-07 — Deterministic mode writes to a separate output directory
- **Given** `AUDIT_DETERMINISTIC=1`,
- **When** the script runs,
- **Then** outputs MUST be written under `.lovable/memory/audit/v2-deterministic/` and MUST NOT touch `.lovable/memory/audit/v2/`.

### AC-31-08 — Deterministic mode performs zero AI calls
- **Given** `AUDIT_DETERMINISTIC=1` and `LOVABLE_API_KEY` unset,
- **When** the script runs,
- **Then** it MUST complete with exit code 0 (no network call, no import of `lovable_ai`).

## Hard scoring gates

After the rubric computes raw per-dimension scores, a fixed table of **hard gates** is applied. Each gate caps ONE dimension when its predicate (a function of `metrics`) is true. Gates run in both deterministic AND AI mode — the AI cannot exceed these ceilings even if it gives an over-generous score.

| Gate id | Dimension | Cap | Trigger |
|---------|-----------|----:|---------|
| `G-LINK-01` | consistency | 70 | `links_broken > 0` |
| `G-LINK-02` | alignment | 60 | `links_broken >= 3` |
| `G-AC-01`   | testability | 20 | `ac_count == 0` |
| `G-AC-02`   | testability | 60 | `ac_count > 0 and gwt_block_count == 0` |
| `G-CON-01`  | implementability | 50 | No `sql/json/ts/yaml` contract block in body (skip when `kind ∈ {tracker, index, meta-toolchain}`, v2.7; `meta-toolchain` also satisfies via `has_normative_contract` text-block, v2.8) |
| `G-CON-02`  | implementability | 30 | `overview_chars < 500` (skip when `kind ∈ {tracker, index}`, v2.7) |
| `G-WAF-01`  | clarity | 70 | `waffle_per_kchar > 3` |
| `G-WAF-02`  | clarity | 50 | `waffle_per_kchar > 6` |
| `G-CR-01`   | maintainability | 60 | Missing `99-consistency-report.md` |
| `G-TODO-01` | completeness | 70 | `todo_density >= 3` (skip when `kind: meta-toolchain`, v2.5) |

The result envelope adds two new top-level keys:
- `raw_scores` — pre-gate rubric output (so reductions are visible).
- `applied_gates` — list of `{id, dimension, cap, before, after, active, rationale}`. Gate is `active=true` only when it actually lowered the score; `active=false` means the predicate fired but the rubric was already at/below the cap.

A companion script renders these into a human report — see §16 [`16-generate-gate-report.md`](./16-generate-gate-report.md).

### AC-31-09 — Hard gates apply in both modes
- **Given** any module whose `links_broken > 0`,
- **When** the audit runs in deterministic OR AI mode,
- **Then** `scores.consistency` MUST be ≤ 70 AND `applied_gates` MUST contain an entry with `id="G-LINK-01"` and `active=true` (when the raw score exceeded 70).

### AC-31-10 — Raw scores are preserved for audit trail
- **Given** any audited module,
- **When** the result envelope is read,
- **Then** it MUST contain `raw_scores` (pre-gate) and `scores` (post-gate), and `weighted(scores) <= weighted(raw_scores)` for every module.

### AC-31-11 — TODO/waffle scanners ignore code samples (v2.4)
- **Given** a module whose only `TODO`/`FIXME` tokens appear inside fenced code blocks (```` ``` ````) or inline `code` spans,
- **When** the deterministic metrics are computed,
- **Then** `metrics.todo_density` MUST equal `0` AND the `G-TODO-01` gate MUST NOT fire. The same prose-only rule applies to `WAFFLE_RX` so `waffle_per_kchar` reflects spec narrative, not code samples.

### AC-31-12 — Meta-token sequences are stripped (v2.5)
- **Given** a module whose prose contains the canonical reference form `TODO/TBD/FIXME` (or any 2+ slash-joined work-tracking tokens) — typical of changelog rows, AC text, or fix-checklist category labels,
- **When** the deterministic metrics are computed,
- **Then** those meta-references MUST NOT contribute to `metrics.todo_density`. Standalone `TODO:` work markers in prose still count.

### AC-31-13 — `kind: meta-toolchain` exempts G-TODO-01 (v2.5)
- **Given** a module whose frontmatter declares `kind: meta-toolchain` (auditor-self-reference modules — currently `27-spec-toolchain`),
- **When** the audit runs,
- **Then** the `G-TODO-01` gate MUST be bypassed entirely (not even recorded as passive in `applied_gates`). Other gates apply normally.

### AC-31-14 — Cross-spec link extraction is prose-only (v2.6)
- **Given** a module whose `body_text` contains markdown links inside fenced markdown/text template blocks (e.g. `01-spec-authoring-guide`'s path-syntax examples — see that module for verbatim form),
- **When** the deterministic metrics are computed,
- **Then** those example links MUST NOT contribute to `metrics.links_total` or `metrics.links_broken`. Implementation: `LINK_RX.findall` runs against `strip_code(body_text)` (the same code-stripped prose used by the TODO/waffle scanners), NOT against the raw body. Standalone markdown links in prose still count and are still validated against the filesystem.

### AC-31-15 — `tracker` and `index` kinds skip the contract gates (v2.7)
- **Given** a module whose frontmatter declares `kind: tracker` (issue ledgers) or `kind: index` (placement-rule routers),
- **When** the audit runs,
- **Then** `G-CON-01` (no inlined contract) MUST be bypassed entirely for both kinds, AND `G-CON-02` (overview <500 chars) MUST also be bypassed for both kinds. Rationale: the rubric (`deterministic_score`) already exempts these `kind`s with baseline `implementability=75/70`; the gates must mirror that exemption to avoid double-penalising. `meta-toolchain` is also exempted from `G-CON-01` (auditor-self-reference modules).

### AC-31-16 — `meta-toolchain` rubric branch + normative-contract bonus (v2.8)
- **Given** a module whose frontmatter declares `kind: meta-toolchain` AND whose `00-overview.md` contains either (a) a ```text fenced block ≥10 non-blank lines containing ≥2 of the markers `CONTRACT:`, `INV-`, `FAIL-`, `DEL-`, `INVARIANT`, `BIJECTION`, OR (b) ≥30 child spec files (`md_files >= 30`) acting as the bijection inventory,
- **When** the deterministic metrics are computed,
- **Then** `metrics.has_normative_contract` MUST be `true` AND `scores.implementability` MUST start from baseline 75 (vs the default 30 for normal contract modules), with `+10` if `has_normative_contract` and `+5` if `md_files >= 30`. The `27-spec-toolchain` module — whose "contract" is the script-spec inventory plus the inlined bijection block — MUST score `implementability >= 85`.

### AC-31-17 — Root index inherits top-level folders as children (v2.9)
- **Given** the root spec `spec/00-overview.md` (`MOD_REL == "."`) with `kind: index`,
- **When** the deterministic metrics are computed,
- **Then** `metrics.child_modules` MUST equal the count of top-level `spec/<NN>-*` folders (`CHILDREN["."]`), AND `scores.implementability` MUST be ≥ 80 (baseline 70 + 10 for `child_modules > 0`). Rationale: pre-v2.9 the parent-derivation rule only fired for paths containing `/`, leaving the root index permanently at `child_modules=0` and impl=70.

### AC-31-18 — Evidenced-meta-toolchain bonuses (v2.10)
- **Given** a module whose frontmatter declares `kind: meta-toolchain`,
- **When** the audit runs,
- **Then** `scores.implementability` MUST receive `+5` for `has_mermaid` AND `+5` for `has_ci_workflow`, capped at 100. Rationale: a toolchain spec that documents its own lifecycle (Mermaid diagram) and CI integration (≥5 yaml workflow blocks) is materially more implementable. Same shape as the v2.9 evidenced-tracker / evidenced-index bonuses.

### AC-31-19 — Contract-bearing index bonus (v2.11)
- **Given** a module whose frontmatter declares `kind: index`,
- **When** the audit runs AND ≥1 of `has_sql_ddl` / `has_ts_enums` / `has_json_schema` / `has_yaml_openapi` / `has_typed_lang_contract` is true,
- **Then** each true contract type MUST add `+5` to `scores.implementability`, AND the implementability cap MUST raise from 90 to 100. When zero contract bonuses fire, the cap MUST remain 90. Rationale: an index that ALSO inlines a typed contract functions as both router AND contract authority.

### AC-31-20 — `--min-weighted` and `--min-impl` CLI threshold gates (v2.12)
- **Given** invocation `python3 linter-scripts/audit-spec-vs-code-v2.py --min-weighted=N1 --min-impl=N2`,
- **When** the audit completes,
- **Then** the script MUST exit `1` if mean weighted < `N1` OR mean impl < `N2`; MUST exit `0` and emit `✓ PASS: thresholds met` to stderr when both thresholds are met; AND MUST preserve pre-v2.12 exit behaviour (no threshold check) when neither flag is supplied. Both flags MUST work in deterministic AND AI mode.

### AC-31-21 — Contract-bearing tracker bonus (v2.13)
- **Given** a module whose frontmatter declares `kind: tracker`,
- **When** the audit runs AND ≥1 of `has_sql_ddl` / `has_ts_enums` / `has_json_schema` / `has_yaml_openapi` / `has_typed_lang_contract` is true,
- **Then** each true contract type MUST add `+5` to `scores.implementability`, AND the implementability cap MUST raise from 85 to 95. When zero contract bonuses fire, the cap MUST remain 85. Rationale: a tracker that ALSO inlines a typed contract supplies an authoritative schema for the issues it tracks (e.g. `tracker_issue` SQL DDL).

### AC-31-22 — Tightened TODO regex + `todo_audit_exempt` opt-out (v2.14)
- **Given** a module whose prose contains the bare token `TODO` (or `TBD`/`FIXME`/`XXX`/`HACK`) with **no** trailing `:`, `(name):`, or ` -` (e.g. "marked TODO", "TODO comment", "TODO/FIXME density"),
- **When** the deterministic metrics are computed,
- **Then** `metrics.todo_density` MUST treat such narrative mentions as zero matches. The regex MUST require the canonical work-tracker shape (`TODO:` / `TODO(name):` / `TODO -`).
- **And given** a module whose `00-overview.md` front-matter declares `todo_audit_exempt: true`,
- **Then** `metrics.todo_count` MUST be forced to `0` regardless of how many real `TODO:` markers appear in prose, AND completeness scoring MUST NOT penalise the module for them. Rationale: auditor-self-reference modules legitimately quote TODO markers when documenting how the TODO detector works.

### AC-31-23 — `--explain=<substring>` rubric trace flag (v2.16, Phase 90)
- **Given** invocation `python3 linter-scripts/audit-spec-vs-code-v2.py --explain=<substring>`,
- **When** at least one module's relative path under `spec/` contains `<substring>`,
- **Then** the script MUST print to stdout: (a) the rubric branch (`tracker` / `index` / `meta-toolchain` / `normal-contract`), (b) per-dimension raw vs final scores with deltas and weighted contribution, (c) every implementability bonus that fired with its delta and the rubric version that introduced it, (d) every gate from `applied_gates` where `active=true` (with `id`, dimension, cap, before, after, rationale), (e) the count of passive gates whose predicate fired but didn't reduce the score, (f) the key metrics block (`ac_count`, `gwt_block_count`, `links_total`, `links_broken`, `todo_density`, `waffle_per_kchar`, `overview_chars`, `md_files`, `child_modules`, `code_blocks_total`).
- **And** the script MUST exit `0` when at least one module matched, `1` when no module matched (with a hint message to stderr).
- **And** when `<substring>` matches >1 module, the script MUST list the first 5 candidate paths to stderr and operate on the first match (substring is matched against the same `MOD_REL` keys used by `AUDIT_ONLY`).
- **And** the flag MUST NOT write any files, MUST NOT call the AI gateway, and MUST NOT touch `.lovable/memory/audit/v2-deterministic/`. It is a pure-stdout diagnostic and short-circuits the normal audit loop entirely.

### AC-31-24 — CLI threshold contract self-test (Phase 91)
- **Given** the script `linter-scripts/test/test-audit-cli-thresholds.sh`,
- **When** invoked from CI (`spec-health.yml`, step *Audit CLI threshold contract self-test*),
- **Then** it MUST execute six cases against `audit-spec-vs-code-v2.py` with `AUDIT_DETERMINISTIC=1`:
  (a) `--min-weighted=200` MUST exit `1` (unsatisfiable floor breaches),
  (b) `--min-weighted=0` MUST exit `0` (satisfiable floor passes),
  (c) `--min-impl=200` MUST exit `1`,
  (d) `--min-impl=0` MUST exit `0`,
  (e) `--min-weighted=0 --min-impl=0` MUST exit `0` (combined satisfiable),
  (f) `--min-weighted=0 --min-impl=200` MUST exit `1` (logical-OR breach semantics: either floor failing fails the run).
- **And** the self-test MUST exit `0` only when all 6 cases match expected exit codes; otherwise exit `1` with a per-case ✅/❌ summary on stdout.
- **And** the self-test MUST NOT write any files and MUST NOT depend on the current absolute scores — it depends only on the comparison-operator contract being intact (locking v2.12 from silent-inversion regressions when scores sit comfortably above the production floor of 97/99).

### AC-31-25 — `--explain` contract self-test (Phase 94)
- **Given** the script `linter-scripts/test/test-audit-explain-contract.sh`,
- **When** invoked from CI (`spec-health.yml`, step *Audit --explain contract self-test*) with `AUDIT_DETERMINISTIC=1`,
- **Then** it MUST execute four scenarios against `audit-spec-vs-code-v2.py --explain=<substring>` and assert all of:
  (a) **Single match** (`--explain=01-spec-authoring-guide`): exit `0`; stdout MUST contain a `Branch` line, a `Final score` line, a `--- Per-dimension scores ---` table, a `--- Implementability bonuses fired` block, and a `--- Key metrics ---` block (5 of the AC-31-23 (a)–(f) elements).
  (b) **No match** (`--explain=does-not-exist-XYZ-7f3a`): exit `1`; stderr MUST contain the substring `no module matched`; stdout MUST NOT contain `Branch` or `Final score` lines (no rubric trace leaked on no-match).
  (c) **Multi-match** (`--explain=03-issues`, currently matches 2 trackers): exit `0`; combined stdout+stderr MUST match `matched [0-9]+ modules`; both candidate paths (`05-split-db-architecture/03-issues`, `06-seedable-config-architecture/03-issues`) MUST be listed; the full report for the first match MUST still print on stdout.
  (d) **No side effects**: a sha256 hash of `ls -la .lovable/memory/audit/v2-deterministic/` taken before any `--explain` invocation MUST equal the hash taken after all 3 scenarios complete (no files added, modified, or deleted).
- **And** the self-test MUST exit `0` only when all 14 assertions across the 4 scenarios pass; otherwise exit `1` with a per-assertion ✅/❌ summary on stdout.
- **And** the self-test MUST NOT depend on absolute audit scores or the AI gateway (deterministic mode forced; checks structural contract only).

### AC-31-26 — Determinism / JSON-stability self-test (Phase 95)
- **Given** the script `linter-scripts/test/test-audit-deterministic-stability.sh`,
- **When** invoked from CI (`spec-health.yml`, step *Audit determinism / JSON-stability self-test*) with `AUDIT_DETERMINISTIC=1`,
- **Then** it MUST execute `audit-spec-vs-code-v2.py` **twice** with identical environment + arguments and assert all of:
  (a) **Both runs exit `0`** (the audit pipeline itself doesn't error out).
  (b) **Both runs write `raw-results.json`** to `.lovable/memory/audit/v2-deterministic/`.
  (c) **`raw-results.json` is byte-identical across both runs** — measured via `sha256sum` of the file contents. Identical hashes → determinism contract intact.
  (d) **Byte size matches** — secondary sanity check that catches truncation regressions independently of hash.
  (e) **Both runs produce valid JSON** with `len(results) >= 80` (the corpus currently has 87 modules; the floor permits future shrinkage but catches catastrophic loss).
  (f) **Module count matches** between runs (`len(run1) == len(run2)`).
  (g) **Modules sorted by name** in the JSON output (the deterministic-mode sort guarantee that makes diffs reviewable).
- **And** the self-test MUST exit `0` only when all 7 assertions pass; otherwise exit `1` with a per-assertion ✅/❌ summary on stdout AND, on byte-identity failure, print up to 20 differing lines (pure-bash `paste`+`awk` line-diff since the CI base image lacks `diff`).
- **And** any non-determinism regression (added wall-clock timestamp, unsorted dict iteration, hash-seeded sampling, removed `sort_keys=True`, reordered `findings` list) MUST cause this self-test to fail in CI even when the production audit gate (`--min-weighted=97 --min-impl=99`) still passes — because the production gate runs the audit only once and cannot detect determinism bugs by construction.
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` lines 122–131 (`DETERMINISTIC` env-var read + `OUT` path branching) and lines 1077–1083 (`sorted(results, key=lambda r: r["module"])` + `sort_keys=DETERMINISTIC` JSON serialisation).

### AC-31-27 — `linter-scripts/test/` MUST have an inventory README (Phase 98)
- **Given** the directory `linter-scripts/test/` containing one or more contract self-tests for any `linter-scripts/` script,
- **When** a contributor adds, removes, or modifies a self-test script in that directory,
- **Then** the file `linter-scripts/test/README.md` MUST be updated **in the same PR** so its **Test inventory** table accurately reflects: (a) every `test-*.sh` script present, (b) the Phase number that introduced it, (c) the script-under-test it locks, (d) the assertion count, (e) the locked AC ID. The README MUST also keep the **Coverage triad** table aligned with the inventory — every self-test must be present in both tables, with the "blind spot" column explaining why the production gate cannot catch the regression on its own.
- **And** the README MUST link to each test script via relative path, link to each locked AC via relative path into `spec/`, and link to each test's post-merge phase memo under `.lovable/memory/audit/v2-deterministic/`.
- **And** the README MUST contain a copy-pasteable template (the "Adding a new self-test" section) so a new contributor can follow the exact convention without reverse-engineering existing scripts. The template MUST cover: shebang, header comment block (Phase + locked contract + blind-spot rationale + spec link + memo link), `set -euo pipefail`, `assert` helper, summary block with `Results: N passed, N failed` line, and CI wiring instructions (workflow step + lockstep AC + memo).
- **And** the README's last-updated date MUST be bumped on every modification.
- **Verifies:** `linter-scripts/test/README.md` (inventory, coverage triad, local execution, template, see-also sections) + `linter-scripts/test/test-readme-inventory.sh` (Phase 102 — mechanically enforces this AC: parses the README inventory and asserts symmetric set parity with `ls test-*.sh`, plus per-script executable bit and required structural sections) + lockstep with the actual contents of `linter-scripts/test/`.

### AC-31-28 — Audit summary outputs MUST advertise rubric version + QA tooling baseline (Phase 99, expanded Phases 102 + 103)
- **Given** the audit script `linter-scripts/audit-spec-vs-code-v2.py` (v2.19 or later),
- **When** the script runs in any mode (deterministic or normal) and writes its summary outputs to `OUT/`,
- **Then** both `00-index.md` and `EXECUTIVE-SUMMARY.md` MUST contain a `**Rubric:** v<X>.<Y>` line in the header block, sourced from the `RUBRIC_VERSION` module-level constant. The constant MUST be a static string (not derived from time, env, or filesystem state) so the Phase 95 determinism self-test continues to pass byte-identically.
- **And** `00-index.md` MUST contain a "QA tooling baseline" section after the "Full ranking" table that enumerates the **11 strict CI gates** that surround the score: (1) cross-links, (2) tree-health strict, (3) lockstep strict, (4) audit thresholds, (5) Phase 91 CLI threshold self-test, (6) Phase 94 `--explain` self-test, (7) Phase 95 determinism self-test, (8) Phase 97 mermaid syntax, (9) Phase 102 README inventory parity self-test, (10) Phase 103 QA baseline footer self-test, (11) Phase 104 memo retrospective-heading meta-linter. Each entry MUST cite the script path so a contributor can locate the gate.
- **And** the section MUST link to `linter-scripts/test/README.md` (Phase 98) as the canonical inventory + onboarding doc for the self-test suite (gates 5–7, 9, 10).
- **And** the section MUST be regenerated on every audit run — it is not a hand-edited file. Drift between the script's enumeration and the actual workflow gates MUST be detected by the **Phase 103 self-test** (`test-qa-baseline-footer.sh`), which asserts a 4-way consistency: `RUBRIC_VERSION` constant ↔ `00-index.md` header ↔ `EXECUTIVE-SUMMARY.md` header ↔ workflow step count. Any new gate added to the workflow must be added to the enumeration in the same PR or this self-test fails.
- **And** `RUBRIC_VERSION` MUST be bumped on every rubric change documented in the "Rubric changelog" table; non-rubric changes (metadata, output formatting, debugging tools, gate-count enumeration changes) MUST also bump it but be explicitly marked "no scoring change" in the changelog row.
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` `RUBRIC_VERSION` constant + `00-index.md` "QA tooling baseline" section + `EXECUTIVE-SUMMARY.md` `**Rubric:**` header + `linter-scripts/test/test-qa-baseline-footer.sh` (Phase 103 — mechanically enforces this AC: 11 assertions covering rubric-version source-of-truth alignment, declared-count ↔ row-count ↔ workflow-step-count parity, and onboarding-link presence) + lockstep with `.github/workflows/spec-health.yml` step list.

### AC-31-29 — Phase memos at or above the Phase 100 cutoff MUST be retrospective (Phase 104)
- **Given** the directory `.lovable/memory/audit/v2-deterministic/` containing per-phase memos named `phase-NNN-<slug>.md`,
- **When** a contributor adds or modifies a memo whose phase number `NNN` ≥ **100** (the Phase 100 retired-cadence cutoff),
- **Then** the memo MUST NOT contain any H2 (`## `) or H3 (`### `) section heading whose text matches a forward-looking pattern: `Next phases?`, `Next iterations?`, `Next Recommended …`, `Remaining (work|tasks?|backlog)`, `Future (work|iterations?|phases?)`, `TODO`, `Upcoming`, or `Roadmap`. Pending work belongs ONLY in the chat reply's "Remaining Tasks" table — the single source of truth — and the AC's `Verifies` clause for code-locked items.
- **And** the linter `linter-scripts/check-memo-retrospective-headings.py` MUST scan the memo directory and exit non-zero on any in-scope memo containing a forbidden heading. The linter MUST print the offending file, line number, raw heading, and matched pattern label, plus a list of suggested retrospective replacements (`What this enables`, `Why Phase <N>'s prediction was correct`, `Closing the <X> cadence`, `Why this matters`, `Verification`, `Files touched`, `Score impact`).
- **And** memos with phase number < 100 are **out of scope** — they are historical record from the pre-Phase-100 cadence and MUST NOT be modified by this rule. The cutoff makes the linter additive, not retroactive.
- **And** the cutoff constant (`CUTOFF_PHASE = 100`) MUST live in the linter source as a module-level integer so future cadence changes are a single-line edit + memo justification.
- **Verifies:** `linter-scripts/check-memo-retrospective-headings.py` (`CUTOFF_PHASE` constant + `FORBIDDEN_PATTERNS` table + `SUGGESTED_REPLACEMENTS` list + main scan loop) + `.lovable/memory/audit/v2-deterministic/phase-100-memo-freshness-sweep-96-99.md` (the cadence-retirement verdict the linter mechanises) + lockstep with `.github/workflows/spec-health.yml` step *Memo retrospective headings gate (Phase 104)*.

### AC-31-30 — Grammar-defining-library pinning pattern (Phase 105, generalises AC-SAG-25)

- **Given** a `linter-scripts/` quality gate that consumes a third-party library to **parse**, **schema-validate**, or **AST-walk** a spec artefact (a `.md`, `.mmd`, `.json`, `.yaml`, `.toml`, `.ts`, `.sql`, or any other file under `spec/`),
- **When** that library is declared in `package.json` (or any future per-language manifest the toolchain adopts, e.g. `requirements.txt` for a Python-based parser),
- **Then** the library's version specifier MUST be an **exact pin** (no `^`, no `~`, no `>=`, no `*`). The rationale, mechanically: the gate's pass/fail signal is only as stable as the library's grammar. An unpinned range silently upgrades the grammar mid-PR (e.g. `mermaid` 11 → 12 may rename a directive; `typescript` 5 → 6 may change AST node shapes; `ajv` may tighten schema validation between minors), turning the gate from a quality signal into a flaky one. Pinning makes any grammar change an explicit, reviewable bump.
- **And** the **trigger condition** for inclusion is unambiguous: a library qualifies the moment a script under `linter-scripts/` (production or self-test) `import`s / `require`s it AND uses it to inspect spec content. Libraries used only by the app preview (e.g. UI components in `src/`) or only as transitive dev-dependencies of unrelated tooling do NOT qualify and MAY remain on caret/tilde ranges.
- **And** the **current pinned inventory** MUST be enumerated below; any addition removes a library from caret/tilde ranges in the same PR that introduces the new gate. The inventory MUST be revisited whenever a new gate ships.

  | Library | Pin | Used by | Trigger phase | AC |
  |---|---|---|---|---|
  | `mermaid` | `11.14.0` | `linter-scripts/check-mermaid-syntax.mjs` | Phase 97 (gate) + Phase 101 (pin) | AC-SAG-24, AC-SAG-25 |
  | `jsdom` | `20.0.3` | `linter-scripts/check-mermaid-syntax.mjs` (DOMPurify shim) | Phase 97 + Phase 101 | AC-SAG-24, AC-SAG-25 |

  Currently-NOT-qualifying examples (documented to prevent future scope creep): `typescript` (used by Vite + the app's `src/` only — no `linter-scripts/` script imports it); `tailwindcss`, `react`, `vite`, `@vitejs/*` (build/runtime, not spec parsers); `ajv` is NOT yet a dependency.

- **And** any PR that bumps the **major** version of a library on the inventory MUST: (1) include a `98-changelog.md` row in the affected spec module recording the bump, the old → new version, and the bumper's local gate-run output (`<N>/<N> files parsed cleanly` or equivalent), AND (2) re-run the full local gate triad before merge: the gate the library powers + `bash linter-scripts/test/test-audit-deterministic-stability.sh` + `bash linter-scripts/run.sh`. **Minor** and **patch** bumps follow the same pin-no-range rule but do NOT require the local re-run — the CI gate will catch grammar drift on its own and the pin guarantees parity between local and CI environments.
- **And** when a future contributor adds a new gate built on a previously-unpinned library, the **same PR** MUST: (a) tighten that library's `package.json` entry to an exact pin, (b) add a row to the inventory table above, (c) add a concrete library-specific AC at the appropriate spec section (the §01-SAG-style instance, modelled on AC-SAG-25 for mermaid+jsdom), and (d) bump §27 §98/§99. This four-step protocol is the operational form of the rule.
- **And** this AC is **declarative** (no new linter script). It is verified by reviewer attention against the inventory + the per-library instance ACs that mechanise it. The failure mode this prevents (silent grammar drift) is intrinsically pre-merge, so a CI-time check would only detect drift after `bun.lock` has already been corrupted; the right enforcement is at PR-review time.
- **Verifies:** `package.json` (every library on the inventory above appears with an exact-pin specifier) + `bun.lock` (resolved versions match the pins exactly) + per-library instance ACs (AC-SAG-25 for mermaid+jsdom; future ACs for any added library) + this inventory table (kept in lockstep with the actual `linter-scripts/` script imports).

### AC-31-31 — Multi-file enumeration parity contract (Phase 109, generalises AC-31-28)

- **Given** a numbered or otherwise discrete enumeration (CI gates, self-tests, pinned libraries, rubric versions, dimension weights, exit codes, scaffolder-emitted files, …) that is restated **verbatim or by count** in **3 or more files** across the repository — including any combination of `linter-scripts/*.{py,cjs,mjs,sh}`, `spec/**/*.md`, `.github/workflows/*.yml`, `.lovable/memory/audit/v2-deterministic/*.md`, `package.json`, or generated audit outputs (`00-index.md`, `EXECUTIVE-SUMMARY.md`, `raw-results.json`),
- **When** that enumeration is added or extended (a new gate, a new pin, a new dimension, a new exit code, …),
- **Then** the same PR MUST either:
  1. **Author a parity self-test** under `linter-scripts/test/test-<enumeration-name>-parity.sh` (or `.py` / `.cjs` if the comparison logic warrants) that asserts **set-equality** (or **count-equality** when set membership is opaque) across all N file restatements, AND wire it into `.github/workflows/spec-health.yml`, AND add a row to `linter-scripts/test/README.md`'s inventory; OR
  2. **Document the exemption** with a `<!-- enumeration-parity-exempt: <reason> -->` HTML comment immediately above the enumeration in EACH restatement, where `<reason>` cites the specific structural property that makes a parity test impossible or wasteful (e.g. "single-source generator output — drift physically impossible", "human-curated narrative — divergence is intentional editorial summarisation").
- **And** the **trigger threshold** is unambiguous: 3 file restatements is the minimum (2 files = direct lockstep, already covered by `check-lockstep.cjs`; 1 file = no parity concern). The threshold derives from empirical evidence: every drift bug Phase 99–104 caught involved an enumeration that crossed exactly 3+ files (CI gate count: script constant + `00-index.md` footer + `EXECUTIVE-SUMMARY.md` cross-reference + workflow step list = 4 files; mermaid+jsdom pins: `package.json` + AC-SAG-25 + AC-31-30 inventory + per-script `import` = 4 sites).
- **And** the **current registered parity self-tests** MUST be enumerated below; any addition to this table extends the contract surface and MUST be cross-referenced from the AC's `Verifies` clause:

  | Enumeration | Restated in (N files) | Parity test | Trigger phase | Locks AC |
  |---|---|---|---|---|
  | CI gates (count + names) | script `RUBRIC_VERSION` + `00-index.md` footer + `EXECUTIVE-SUMMARY.md` cross-ref + `spec-health.yml` step list (= 4) | `linter-scripts/test/test-qa-baseline-footer.sh` | Phase 103 | AC-31-28 |
  | `linter-scripts/test/` inventory | `linter-scripts/test/README.md` table + actual `test/*.sh` files on disk + `spec-health.yml` step list (= 3) | `linter-scripts/test/test-readme-inventory.sh` | Phase 102 | AC-31-27 |
  | §27 toolchain inventory (scripts + workflows) | `spec/27-spec-toolchain/00-overview.md` Inventory tables + on-disk `linter-scripts/*.{py,cjs,mjs,sh,go,ps1}` + `.github/workflows/*.yml` + Phase 107 orphan-ledger memo (= 3 documentation/code sites) | `linter-scripts/test/test-overview-inventory-parity.sh` | Phase 112 | AC-T-01 (INV-01/INV-02 in §00 Normative Contract) |
  | 7-dimension scoring weights | `linter-scripts/audit-spec-vs-code-v2.py` `WEIGHTS` dict (source of truth) + `linter-scripts/generate-gate-report.py` `WEIGHTS` dict (duplicated for offline analysis) + `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` `## Weights` markdown table (= 3) | `linter-scripts/test/test-weights-parity.sh` | Phase 113 | AC-31-02 (extends from in-script invariant to cross-file parity) |

  Currently-NOT-qualifying enumerations (documented to prevent future scope creep): the rubric changelog table at this file (single source of truth — restated nowhere else, only summarised in phase memos which are explicitly editorial); the per-module score table in `00-index.md` (single-source generator output — Phase 95 determinism self-test already covers stability); per-AC `Verifies` clauses (each AC owns its own clause, no cross-file enumeration). The grammar-library pin inventory at AC-31-30 currently spans only 2 sites (`package.json` + the inventory table itself) and so falls under direct lockstep, not multi-file parity — if a third site is ever added (e.g. a contributor onboarding doc enumerating the pins), AC-31-31 fires and a parity test is required. **Phase 114 sweep additions** (proactive bounding pass after Phase 113): the `audit-spec-vs-code-v2.py` exit-code table (0/1/2) is restated in only 2 sites — script source + §31 spec table — so falls under direct lockstep (`check-lockstep.cjs`), not AC-31-31; per-script exit-code tables across `check-memo-retrospective-headings.py`, `check-memory-mirror-drift.py`, `check-root-readme.py`, `check-tree-health.cjs` etc. each share the labels `0`/`1`/`2` but encode **different domain semantics** per script (e.g. "no drift" vs "no broken links" vs "no missing readme"), so they are N independent 2-file enumerations rather than one N-file enumeration — AC-31-31 does NOT fire and inventing a cross-script "exit code 1 always means failure" parity test would be a category error; the audit-script CLI flag set (`--min-weighted` / `--min-impl` / `--strict` / `--explain` / `--deterministic`) is referenced across script + spec + workflow + 4 self-tests but each site cites only the **subset of flags it actually uses** (e.g. `test-audit-cli-thresholds.sh` cites only the 2 threshold flags it locks), making this an **API surface use** pattern rather than an enumeration restatement — the canonical list lives only in the script's `argparse` block (single source of truth) and AC-31-31 does NOT fire; the CI threshold floors `--min-weighted=97 --min-impl=99` are restated in only 2 sites (`.github/workflows/spec-health.yml` + `linter-scripts/test/test-audit-cli-thresholds.sh`'s expected-floor cases) — direct lockstep zone, not AC-31-31. The Phase 114 sweep covered: WEIGHTS-adjacent `RUBRIC_WEIGHTS` (single-site, dismissed by Phase 113), `7 dimensions` prose (2-site, dismissed by Phase 113), `8 exit codes` cross-script reference (different enumerations sharing a label, dismissed by Phase 113 and re-confirmed above), gate-cap thresholds 95/90/85/70 (each cap is a single-site magic number with rationale, not a restated enumeration), and the audit CLI flag inventory (API surface, not enumeration). **Net Phase 114 result: zero new parity tests required; the AC-31-31 registry remains at 4 rows and is provisionally complete for the current toolchain surface.** Future contributors who introduce a new 3+ file enumeration are still bound by the protocol below regardless of this Phase-114 bounding statement.

- **And** when a future contributor adds a new enumeration that crosses the 3-file threshold, the **same PR** MUST: (a) author the parity self-test (or the exemption comment block in all N restatements), (b) add a row to the registry above, (c) bump §27 §97/§98/§99 in lockstep. This three-step protocol is the operational form of the rule.
- **And** this AC is **declarative** (no new meta-linter that scans for unregistered enumerations). Detecting "is this an enumeration that crosses 3+ files?" requires semantic understanding the toolchain does not have; reviewer attention against the registry above is the right enforcement layer. The rule's value is that it gives reviewers a named pattern to point at, and it gives gate-authors a checklist to follow when shipping a new gate.
- **And** the **rationale** for codifying this pattern: Phases 99 (gate-count footer drift latent for 4 phases until Phase 103 caught it), 102 (README inventory drift caught only by a self-test that was itself missing its own row on first run), and 103 (4-way enumeration consistency) all independently re-discovered the same lesson — *any value duplicated across 3+ files will eventually drift, and the only sustainable defence is mechanical parity enforcement*. Without this AC, the next gate-author starts from zero and re-discovers the lesson in a future incident. **Phase 112 is the first contribution authored under AC-31-31**: the §27 inventory triangle was identified as 3-file restatement during Phase 109 codification, and its parity self-test was authored in the same PR that registered the row.
- **Verifies:** the parity-test registry table above (kept in lockstep with the actual `linter-scripts/test/test-*-parity.sh` files on disk and the `linter-scripts/test/README.md` inventory) + `linter-scripts/test/test-readme-inventory.sh` (Phase 102, mechanises row #2) + `linter-scripts/test/test-qa-baseline-footer.sh` (Phase 103, mechanises row #1) + `linter-scripts/test/test-overview-inventory-parity.sh` (Phase 112, mechanises row #3) + `linter-scripts/test/test-weights-parity.sh` (Phase 113, mechanises row #4) + this AC's own enumeration of currently-NOT-qualifying cases (documented to bound the contract surface).

## Rubric changelog (v2.9 → v2.23)

| Version | Phase | Change | Score effect |
|--------:|------:|--------|--------------|
| v2.9 | 46 | Root index spec (`MOD_REL == "."`) inherits top-level folders as `CHILDREN["."]`. Evidenced-tracker / evidenced-index bonuses (`+5` each for `has_mermaid` / `has_ci_workflow`). | Root spec impl 70 → 80; weighted out of D-tier. |
| v2.10 | 79 | Evidenced-meta-toolchain bonuses (`+5` each for `has_mermaid` / `has_ci_workflow`). | `27-spec-toolchain` impl 85 → 95. |
| v2.11 | 80 | Contract-bearing index bonus: `+5` per typed contract (SQL/TS/JSON/OpenAPI/typed-lang); cap 90 → 100 when ≥1 fires. | Index modules with inline contracts impl 90 → 100. |
| v2.12 | 81 | New CLI flags `--min-weighted=N` and `--min-impl=N` enforce mean-score floors in CI. | Workflow gate: locks current quality bar without external script. |
| v2.13 | 82 | Contract-bearing tracker bonus: `+5` per typed contract; cap 85 → 95 when ≥1 fires. | 3 trackers (`05-split-db.../03-issues`, `06-seedable.../03-issues`, `25-app-issues/02-...`) impl 85 → 95. |
| v2.14 | 83 | TODO regex tightened to require `:` / `(name):` / ` -` suffix; new `todo_audit_exempt: true` front-matter opt-out for auditor-self-reference modules. | Prevents false-positive TODO penalties on gap-analysis / changelog content. |
| v2.15 | 86 | Cumulative schema-bonus cap REJECTED after empirical test (mean impl 99.8 → 89.2; 76 multi-contract modules unfairly penalised). Source comment + memo preserve the rejected design. | None (zero rubric change shipped). |
| v2.16 | 90 | New `--explain=<substring>` CLI flag prints rubric branch, fired bonuses, capped gates, and per-dimension trace for any module. Pure-add diagnostic. | None (no scoring change; debugging tool only). |
| v2.16-test1 | 91 | CLI threshold contract self-test (`linter-scripts/test/test-audit-cli-thresholds.sh`) wired into `spec-health.yml`. Locks v2.12 exit-code semantics from silent-inversion regressions. | None (no rubric change; CI safety net only). |
| v2.16-test2 | 94 | `--explain` contract self-test (`linter-scripts/test/test-audit-explain-contract.sh`) wired into `spec-health.yml`. Locks v2.16 single-match / no-match / multi-match / no-side-effects contract from silent-break regressions. | None (no rubric change; CI safety net only). |
| v2.16-test3 | 95 | Determinism / JSON-stability self-test (`linter-scripts/test/test-audit-deterministic-stability.sh`) wired into `spec-health.yml`. Locks `AUDIT_DETERMINISTIC=1` byte-identical guarantee — runs the audit twice and asserts `sha256(raw-results.json)` matches. Catches non-determinism regressions the production gate cannot see (single-run gate by construction). | None (no rubric change; CI safety net only). |
| v2.17 | 99 | Metadata sync: new `RUBRIC_VERSION = "v2.17"` constant surfaced in `00-index.md` (+ `**Rubric:** v2.17` header) and `EXECUTIVE-SUMMARY.md`. New "QA tooling baseline (Phase 99)" footer in `00-index.md` enumerating the 8 strict CI gates that surround the score (cross-links + tree-health + lockstep + audit thresholds + 3 self-tests + mermaid syntax). Determinism preserved — `RUBRIC_VERSION` is a static string. | None (no rubric change; output-clarity only). |
| v2.18 | 102 | Gate count metadata bump: `RUBRIC_VERSION` v2.17 → v2.18 to reflect the addition of a 9th strict CI gate — the README inventory parity self-test (`test/test-readme-inventory.sh`, locks AC-31-27 mechanically). QA tooling baseline footer regenerated to enumerate **9 strict CI gates** instead of 8; `linter-scripts/test/README.md` link annotation updated to reference the self-test suite (#5–#7 + #9). Determinism preserved — `RUBRIC_VERSION` remains a static string. | None (no rubric change; output-clarity + new safety net only). |
| v2.19 | 103 | Footer-contract enforcement: `RUBRIC_VERSION` v2.18 → v2.19 to reflect the addition of a 10th strict CI gate — the QA baseline footer self-test (`test/test-qa-baseline-footer.sh`, locks AC-31-28 mechanically via 11 assertions checking 4-way enumeration consistency: script `RUBRIC_VERSION` constant ↔ `00-index.md` header ↔ `EXECUTIVE-SUMMARY.md` header ↔ `spec-health.yml` workflow step count). QA tooling baseline footer regenerated to enumerate **10 strict CI gates** instead of 9. AC-31-28 was previously enforceable only by reviewer attention; now mechanically enforced. The new self-test re-runs the audit (deterministic mode) and validates output post-hoc, so it doubles as a smoke test for any future regression in summary-output emission. Determinism preserved — `RUBRIC_VERSION` remains a static string; new sha256 stable across two runs after the one-time rollover. | None (no rubric change; output-clarity + new safety net only). |
| v2.20 | 104 | **Memo retrospective-heading meta-linter**: `RUBRIC_VERSION` v2.19 → v2.20 to reflect the addition of an 11th strict CI gate — `linter-scripts/check-memo-retrospective-headings.py`, which mechanises **AC-31-29** and **Phase 100's retired-cadence verdict**. The linter scans `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md` for memos with `NNN ≥ 100` and FAILS on any forward-looking H2/H3 heading (`Next phases`, `Remaining Tasks`, `Future work`, `TODO`, `Roadmap`, …). Phase 100 retired the forward-looking cadence after empirical evidence that recent memos were already self-contained retrospectives; this gate prevents silent regression. QA tooling baseline footer regenerated to enumerate **11 strict CI gates** instead of 10; Phase 103 self-test extended with the new gate-name pattern (now expects 11/11 alignment); section title updated to *"QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104)"*. Verified detection by lowering `CUTOFF_PHASE` to 78: linter correctly flagged 9 historical "Next phases" / "Next iteration" headings in phases 78-83 / 92-93 / 96. Determinism preserved — `RUBRIC_VERSION` remains a static string. | None (no rubric change; output-clarity + new safety net only). |
| v2.21 | 112 | **§27 inventory parity triangle self-test**: `RUBRIC_VERSION` v2.20 → v2.21 to reflect the addition of a 12th strict CI gate — `linter-scripts/test/test-overview-inventory-parity.sh`, the **first parity self-test authored under AC-31-31** (Phase 109's multi-file enumeration parity contract). Closes the INV-01/INV-02 drift Phase 107 documented (8 silent orphans had accumulated under `linter-scripts/` because `check-tree-health.cjs`'s allow-list inference is permissive). The test asserts the 3-way triangle: every executable artifact under `linter-scripts/*.{py,cjs,mjs,sh,go,ps1}` + `.github/workflows/*.yml` is tracked in either `spec/27-spec-toolchain/00-overview.md` (specced) OR the Phase 107 orphan ledger memo (acknowledged); every overview-listed code path exists on disk; the orphan ledger is not stale; structural anchors (Inventory H2, Normative Contract block, AC-31-31/INV-01 cross-reference) are intact. Baseline at landing: 34 on-disk = 31 specced + 3 production orphans (`check-mermaid-syntax.mjs`, `check-memo-retrospective-headings.py`, `deepen-consistency-reports.py`); the 5 `linter-scripts/test/test-*.sh` files are excluded by directory scope (covered by the Phase 102 README parity test, which is the canonical parity test for `test/`). QA tooling baseline footer regenerated to enumerate **12 strict CI gates** instead of 11; Phase 103 self-test extended with the new gate-name pattern `Self-test §27 inventory parity triangle` (now expects 12/12 alignment); section title updated to *"QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104 + 112)"*; AC-31-31 registry table extended to 3 rows. Determinism preserved — `RUBRIC_VERSION` remains a static string. | None (no rubric change; output-clarity + new safety net only). |
| v2.22 | 113 | **WEIGHTS dimension-table parity self-test**: `RUBRIC_VERSION` v2.21 → v2.22 to reflect the addition of a 13th strict CI gate — `linter-scripts/test/test-weights-parity.sh`, the **second parity self-test authored under AC-31-31** (registry row #4). Discovered during a Phase 113 sweep of `.lovable/memory/` and `linter-scripts/` for previously-unregistered 3+ file enumerations: the 7-dimension scoring weights are restated **verbatim** across `audit-spec-vs-code-v2.py` (`WEIGHTS` dict — source of truth), `generate-gate-report.py` (`WEIGHTS` dict — duplicated for offline analysis), and `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` (`## Weights` markdown table). AC-31-02's existing runtime assertion (`implementability == 35 AND total == 100` at audit-script load time) catches in-script drift in the audit script alone, but does NOT mandate parity with the gate-report or with §31's documented table — exactly the AC-31-31 trigger condition. The test extracts WEIGHTS from both Python files via regex and from the §31 markdown table via `## Weights` heading anchor, asserts pairwise dict-equality (audit ↔ gate-report ↔ spec), re-checks AC-31-02's invariants as defence-in-depth, and confirms the dimension count is exactly 7 (matches §00-overview's "7 dimensions" prose). 8/8 assertions ✅ at landing. QA tooling baseline footer regenerated to enumerate **13 strict CI gates** instead of 12; Phase 103 self-test extended with the new gate-name pattern `Self-test WEIGHTS dimension-table parity` (now expects 13/13 alignment); section title updated to *"QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104 + 112 + 113)"*; AC-31-31 registry table extended to 4 rows. Determinism preserved — `RUBRIC_VERSION` remains a static string. | None (no rubric change; new safety net for highest-stakes scoring contract). |
| **v2.23** | **F2** | **Folder-reference gate wiring**: `RUBRIC_VERSION` v2.22 → v2.23 to reflect the addition of a 14th strict CI gate — `linter-scripts/check-spec-folder-refs.py`, wired into `.github/workflows/spec-health.yml` between the cross-link gate (#1) and the tree-health gate (#2). The script existed since authoring but was dormant (zero CI references) — Phase 141 surfaced it with 26 stale refs (upper-bound estimate); Phase F1 (2026-04-28) brought it to 0 stale refs by classifying 3 missing-folder targets (`08-docs-viewer-ui`, `09-code-block-system`, `21-app`) as `[doc-only]`. Phase F2 wires it as a strict gate so future drift triggers a CI fail at PR time rather than waiting for a manual sweep. **Not an AC-31-31 row** — the gate enforces folder-ref allowlist consistency (a single-source invariant already locked by AC-62-01..04), not a 3+ file enumeration parity. QA tooling baseline footer regenerated to enumerate **14 strict CI gates** instead of 13; Phase 103 self-test extended with the new gate-name pattern `Spec folder-reference gate` (now expects 14/14 alignment); section title updated to *"QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104 + 112 + 113 + F2)"*. AC-31-31 registry table unchanged (still 4 rows). Determinism preserved — `RUBRIC_VERSION` remains a static string. | None (no rubric change; closes a dormant-gate gap discovered Phase 141, resolved Phase F1, wired Phase F2). |
| **v2.31** | **G2** | **Forbidden-strings gate wiring**: `RUBRIC_VERSION` v2.30 → v2.31 to reflect the addition of a **21st strict CI gate** — `linter-scripts/check-forbidden-strings.py`, wired into `.github/workflows/spec-health.yml` between the folder-reference gate (#10) and the §99 freshness gate. The script existed since authoring but was dormant — its header docstring referenced a non-existent `ci.yml`. Phase G1 (2026-05-07) fixed §60 schema drift (live TOML uses `[[rule]]`/`pattern`/`fix_hint`, not `[[patterns]]`/`regex`); Phase G2 (2026-05-07) wires the script as a strict gate so future regressions on any `[[rule]]` fail CI at PR time. **Not an AC-31-31 row** — the gate enforces TOML-driven regex rename guards (single-source invariant already locked by AC-60-01..05), not a 3+ file enumeration parity. QA tooling baseline footer regenerated to enumerate **21 strict CI gates** instead of 20; Phase 103 self-test extended with the new gate-name pattern `Forbidden strings gate` (now expects 21/21 alignment); section title updated to *"QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104 + 112 + 113 + F2 + H1 + H5 + H7 + 30 + P15 + P47-followup-1 + G2)"*. AC-31-31 registry table unchanged (still 4 rows). Determinism preserved — `RUBRIC_VERSION` remains a static string. Note: rows v2.24–v2.30 documented in §98/§99 changelogs (Phase 153 Tasks H1/A12/A17/A18/etc.) — this row covers only the G2 wiring delta. | None (no rubric change; closes a dormant-gate gap discovered Phase G1, wired Phase G2). |



## Cross-references

- §13 [`13-generate-gwt-acceptance.md`](./13-generate-gwt-acceptance.md) — consumes `raw-results.json`.
- §16 [`16-generate-gate-report.md`](./16-generate-gate-report.md) — explains which gate caps each module.
- §30 [`30-audit-spec-vs-code.md`](./30-audit-spec-vs-code.md) — predecessor.
- §70 [`70-spec-health-yml.md`](./70-spec-health-yml.md) — CI workflow that invokes this auditor with `--min-weighted` / `--min-impl` floors.

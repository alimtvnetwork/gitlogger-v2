# `linter-scripts/test/` — Self-Tests for the Spec-Toolchain CLI

**Last updated:** 2026-05-07 (Phase G3 — added `test-check-forbidden-strings.sh` (#17) to inventory locking the §60 `check-forbidden-strings.py` exit-code + allowlist + empty-config + real-tree contract per AC-60-01..05; mechanizes the schema-drift guard introduced in Phase G1 + the CI wiring landed in Phase G2. Totals 16 → 17 scripts; ~41 → ~42 s CI time.)
**Source of truth for:** the contract guarantees of every script under
`linter-scripts/` that has user-visible CLI semantics (exit codes,
stdout/stderr structure, idempotency, determinism).

---

## Why this directory exists

The pre-existing CI gates (tree-health, lockstep, audit thresholds,
trace-map regression, mermaid syntax) all check the **state of the spec
tree** — they answer *"does the repo currently satisfy the rules?"*.

They do **not** answer *"do the linters that enforce those rules still
behave correctly?"*. A subtle bug in `audit-spec-vs-code-v2.py` — flipping
a comparison operator, swapping an exit code, breaking the `--explain`
output, or losing determinism — could go unnoticed for months because:

- The production audit gate runs **once per CI build**, so it cannot detect
  non-determinism.
- All 87 modules currently sit comfortably above the score floors
  (98.0 / 99.8 vs 97 / 99), so a comparison-operator inversion wouldn't
  flip the gate's verdict.
- The `--explain` flag is only invoked manually by contributors, never by
  CI, so a silent regression in its stdout structure would be invisible
  until the next time someone debugged a score outlier.

The self-tests in this directory close those blind spots. Each one is a
**contract test**: it pins one specific behaviour of one specific script
with a small number of high-signal assertions, and it runs in CI on every
PR so any regression fails the build at the assertion level (with
`✅`/`❌` per-check output) rather than as a downstream symptom.

---

## Test inventory

| # | Test script | Phase | Asserts about | Assertions | Runtime | Locked AC |
|---|---|---|---|:-:|:-:|---|
| 1 | [`test-audit-cli-thresholds.sh`](./test-audit-cli-thresholds.sh) | 91 | `audit-spec-vs-code-v2.py` `--min-weighted=N` / `--min-impl=N` exit-code contract | 6 | ~3 s | [AC-31-22](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 2 | [`test-audit-explain-contract.sh`](./test-audit-explain-contract.sh) | 94 | `audit-spec-vs-code-v2.py --explain=<substring>` stdout structure, exit codes, no-side-effects | 14 | ~6 s | [AC-31-23](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) + [AC-31-25](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 3 | [`test-audit-deterministic-stability.sh`](./test-audit-deterministic-stability.sh) | 95 | `audit-spec-vs-code-v2.py` produces byte-identical `raw-results.json` across two runs under `AUDIT_DETERMINISTIC=1` | 7 | ~12 s | [AC-31-26](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 4 | [`test-readme-inventory.sh`](./test-readme-inventory.sh) | 102 | This README's inventory table is in sync with the actual `test-*.sh` files on disk; required structural sections present; every script linked + executable | 14+ | ~1 s | [AC-31-27](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 5 | [`test-qa-baseline-footer.sh`](./test-qa-baseline-footer.sh) | 103 | The audit script's "QA tooling baseline" footer (in `00-index.md` + `EXECUTIVE-SUMMARY.md`) is consistent with `RUBRIC_VERSION` constant + `.github/workflows/spec-health.yml` step list — declared gate count = footer rows = workflow gate steps | 11+ | ~3 s | [AC-31-28](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 6 | [`test-overview-inventory-parity.sh`](./test-overview-inventory-parity.sh) | 112 | The §27 inventory triangle: every executable artifact under `linter-scripts/` + `.github/workflows/` is tracked in either `spec/27-spec-toolchain/00-overview.md` (specced) OR the Phase 107 orphan ledger memo (acknowledged); every overview-listed code path exists on disk; structural anchors intact | 6+ | ~1 s | [AC-31-31](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) |
| 7 | [`test-weights-parity.sh`](./test-weights-parity.sh) | 113 | The 7-dimension `WEIGHTS` triangle: `audit-spec-vs-code-v2.py` `WEIGHTS` dict ↔ `generate-gate-report.py` `WEIGHTS` dict ↔ `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` `## Weights` table — pairwise dict-equality + AC-31-02 invariants (impl == 35, total == 100) + dimension count == 7 | 8 | ~1 s | [AC-31-31 row #4](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) (extends [AC-31-02](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md)) |
| 8 | [`test-check-99-summary-freshness.sh`](./test-check-99-summary-freshness.sh) | H1 | §26 `check-99-summary-freshness.py` exit-code contract: unstamped files don't fail (advisory), stamped+stale files exit 1 in strict mode and 0 with `--report-only`, stamped+fresh files exit 0, missing-phase-token exits 2. Phase H2 widened to inventory rubrics + `_archive/` exclusion (T8/T9/T10). Synthetic sandbox. | 17 | ~1 s | [AC-26-01..08](../../spec/27-spec-toolchain/26-check-99-summary-freshness.md) |
| 9 | [`test-check-99-stamp-bump.sh`](./test-check-99-stamp-bump.sh) | H4 | §27 `check-99-stamp-bump.py` exit-code contract: empty/unstamped/stamp-only diffs skip (exit 0); materially-edited stamped files without bump exit 1; `--report-only` never fails; `_archive/` excluded; bad base-ref/missing phase token exit 2. Uses `--changed-files` test injection to bypass git (sandbox forbids `git add`). | 23 | ~1 s | [AC-27-01..08](../../spec/27-spec-toolchain/27-check-99-stamp-bump.md) |
| 10 | [`test-archive-exclusion-runtime.sh`](./test-archive-exclusion-runtime.sh) | H7 | §28 runtime archive-exclusion gate: every spec-traversing linter MUST exclude `spec/_archive/` at RUNTIME (not just by source-reading). importlib-loads 3 critical linters (`check-99-summary-freshness.find_99_files()`, `audit-spec-vs-code-v2.ALL_MODULES`, `generate-trace-map.collect_ac_ids()`), calls each enumerator, asserts 0 archive-leaked results. Floor: probe count ≥ 3. Codifies the H6 lesson "runtime > source verification". | 10 | ~3 s | [AC-28-01..05](../../spec/27-spec-toolchain/28-check-archive-exclusion-runtime.md) |
| 11 | [`test-check-version-parity.sh`](./test-check-version-parity.sh) | P15/P31 | §29 `check-version-parity.py` exit-code contract: §00 banner version vs §98 latest release row mismatches are reported; default mode is advisory (exit 0); `--strict` and `<!-- h10-verified-phase: NNN -->` per-file stamps promote to exit 1; `--report-only` overrides stamps; `--spec-root` outside repo no longer crashes. Sandbox-injected drift (real tree at 0 mismatches post-P30). | 13 | ~1 s | [AC-29-01..14](../../spec/27-spec-toolchain/29-check-version-parity.md) |
| 12 | [`test-check-spec-cross-links.sh`](./test-check-spec-cross-links.sh) | P35 | §01 `check-spec-cross-links.py` fuzzy waiver matching: stale waiver line numbers (drifted by ≤ 5 lines from the actual link location, e.g. after a stamp-batch tool inserted a comment line above) are accepted with an `INFO` hint; `--rewrite-allowlist` auto-bumps stale lines in-place and is idempotent; `--strict-line-match` restores exact-line semantics; out-of-tolerance drift (> 5 lines) does NOT fuzzy-match. Codifies the P34 lesson #1: stamp-batch tools (P22/P32) silently broke CI for 12 phases by drifting waiver line numbers. Synthetic sandbox. | 19 | ~1 s | [AC-01-05..07](../../spec/27-spec-toolchain/01-check-spec-cross-links.md) |
| 13 | [`test-inline-code-blanking-parity.sh`](./test-inline-code-blanking-parity.sh) | P45 | JS↔Python inline-code blanking parity: `linter-scripts/check-spec-cross-links.py::strip_inline_code()` and `linter-scripts/generate-dashboard-data.cjs::blankInlineCode()` MUST produce byte-identical output for any input line, with same-length space runs (char offsets preserved → line numbers stay accurate). 8-fixture corpus probes the P44 root-cause pattern (inline-code wrapping a markdown link target — `` `./test-foo.sh` `` inside `[…](…)`), bare/multi/triple-backtick spans, link-adjacent code, and empty input. Floor: fixture count ≥ 8. Mechanically locks the AC-11-05 dual-implementation parity contract (P44 closure). | 17 | ~1 s | [AC-11-05](../../spec/27-spec-toolchain/11-generate-dashboard-data.md) |
| 14 | [`test-check-truncated-prose.sh`](./test-check-truncated-prose.sh) | P47-followup-1 | §27 slot 32 `check-truncated-prose.py` exit-code contract: clean fixtures (terminator + structural endings) exit 0; dirty fixtures (unclosed code fence + mid-sentence ending) exit 1 with both flagged in stderr; live `spec/` tree gate proves the linter passes on the real tree. Mechanically catches the **truncation class** of AI-implementability blockers surfaced by the Phase P47 audit. First production run found one real defect: `spec/17-consolidated-guidelines/14-app-issues.md` had an unbalanced fence at template end (fixed in same phase). | 5 | ~0.3 s | [AC-32-01..05](../../spec/27-spec-toolchain/32-check-truncated-prose.md) |
| 15 | [`test-check-ai-confidence.sh`](./test-check-ai-confidence.sh) | P48-1-fu1 | §27 slot 33 `check-ai-confidence.py` exit-code contract: live-tree default mode exits 0; `--json` schema includes `scanned_modules`/`eligible`/`matches`/`mismatches`/`stamped`/`stamped_failed`/`rows`; `--strict` exits 1 when any drift exists (current 13 drifters), 0 once tree converges; `--report-only` always exits 0; importlib-loaded `derive_tier()` returns `Medium` when P3 fails (no `**Verifies:**`) and promotes to `High` when added — proves AC-33-04 lowest-passing-gate logic. Mechanizes the AC-09 `AI Confidence` four-gate rubric introduced in P48-1, eliminating the entire class of author-judgement drift. | 5 | ~1 s | [AC-33-01..06](../../spec/27-spec-toolchain/33-check-ai-confidence.md) |
| 16 | [`test-audit-ai-implementability.sh`](./test-audit-ai-implementability.sh) | 153 Task A4 | §27 slot 34 `audit-ai-implementability.py` CLI surface contract (no-network mode only — never invokes the LLM gateway): `--help` advertises five mode flags incl. `--no-network`; `--no-network` exits 0 on full tree; `--module=<slot>` walks a single module bundle; `--json` produces parseable JSON; non-md walker (slot 11 `spec/11-powershell-integration` schemas/templates) returns ≥18 files per AC-34-06. Mechanically locks the deep-walk + non-md tier-1 walker contract (Lessons #11/#16) without LLM gateway dependency. | 6 | ~5 s | [AC-34-01..06](../../spec/27-spec-toolchain/34-audit-ai-implementability.md) |
| 17 | [`test-check-forbidden-strings.sh`](./test-check-forbidden-strings.sh) | G3 | §60 `check-forbidden-strings.py` exit-code + behavioural contract: clean fixture exits 0; dirty fixture exits 1 with rule-id + offending line + fix-hint in stdout; `allowlist` entries suppress findings; empty config (no `[[rule]]` entries) exits 0 with warning; live repo tree must be clean (real-tree gate). Mechanically locks the schema-drift guard introduced in Phase G1 (AC-60-05) + the CI wiring landed in Phase G2 — together they form a closed loop: G1 = correct schema in spec, G2 = strict CI gate, G3 = the gate itself stays correct. | 6 | ~1 s | [AC-60-01..05](../../spec/27-spec-toolchain/60-forbidden-strings-toml.md) |
| 18 | [`test-audit-ai-tier1b-promotion.sh`](./test-audit-ai-tier1b-promotion.sh) | 153 R2-fu | Locks AC-34-18 bounded tier-1B promotion: for each FITS module (≤12 nested contract files) the bundle includes all root-tier `00/97/98/99` plus all nested tier-1B; for OVERFLOW modules (e.g. spec/02 with 116 nested) nested promotions are capped (`nT1B_first12 ≤ 3`); zero-T1B modules behave unchanged. Mechanically pins the R2 audit-walker contract that closed the spec/05 truncation defect class. | 8+ | ~3 s | [AC-34-18](../../spec/27-spec-toolchain/34-audit-ai-implementability.md) |
| 19 | [`test-audit-bundle-budget.sh`](./test-audit-bundle-budget.sh) | 153 Task A24-fu32 | Locks `audit-bundle-budget.py` CLI + JSON contract: `--module=<slot>` returns per-module budget telemetry (`bundle_bytes`, `cap_bytes`, `headroom_pct`, `chunked_path`, `tier_split`); `--json` parses; `--threshold-pct` exits non-zero when any module's headroom falls below the floor. Mechanically pins the Lesson #71 saturation-class triage contract: budget telemetry MUST be queryable by external scorecard tooling without re-running the full LLM audit. | 6+ | ~2 s | [AC-34-N6](../../spec/27-spec-toolchain/34-audit-ai-implementability.md) |
| 20 | [`test-audit-chunked-cache-advisory.sh`](./test-audit-chunked-cache-advisory.sh) | 153 Task N8 | Locks the Lesson #82 chunked-cache advisory emitted by `audit-ai-implementability.py` (Phase 153 Task N6): sub-90 modules with `chunked_path=false` MUST appear in the advisory list; modules at `chunked_path=true` MUST NOT; advisory section header + per-module rows are present in both `--report-only` and `--strict` modes. Mechanizes the Lesson #82 cache-class hygiene rule so plateau-diagnosis tooling can be trusted across rebaselines. | 5+ | ~1 s | [AC-34-N8](../../spec/27-spec-toolchain/34-audit-ai-implementability.md) |
 | 17 | [`test-audit-bundle-budget.sh`](./test-audit-bundle-budget.sh) | 153 Task A24-fu32 | `linter-scripts/audit-bundle-budget.py` deterministic stat-only walker-budget analyzer: scans every `spec/NN-*/` module, classifies tier-1 (§00+§97+§98+§99) vs siblings against the 120 KB walker cap, emits CLEAR/AT_CEILING/OVER status per Lesson #65. Self-test exercises the analyzer on the live tree, asserts stable status for known-OVER modules (spec/27, spec/22, spec/01) and known-CLEAR modules. | 6 | ~1 s | (advisory — no AC binding; supports Lesson #65/#73 diagnostics) |
 | 18 | [`test-audit-chunked-cache-advisory.sh`](./test-audit-chunked-cache-advisory.sh) | 153 Task N8 | `audit-ai-implementability.py` Lesson #82 advisory contract: injects three fixture caches (sub-90+chunked=false, sub-90+chunked=true, ≥90+chunked=false) into `.lovable/cache/audit-ai/`, runs `--no-network --report-only`, asserts the failing fixture appears in the advisory block and the two safe fixtures do NOT, asserts header presence and that the advisory never changes exit code. Snapshot-restore contract per Lesson #31 keeps the real cache byte-identical pre/post. Mechanically locks Lesson #82 (chunked-cache class hygiene) so a future refactor cannot silently drop the warning. | 5 | ~2 s | (advisory — locks Lesson #82 emit contract in `audit-ai-implementability.py`) |

**Totals:** 18 scripts · 187+ assertions · ~44 s of CI time.

All thirteen scripts are reachable from [`.github/workflows/spec-health.yml`](../../.github/workflows/spec-health.yml).
Seven run as discrete self-test steps (`Audit CLI threshold contract self-test (Phase 91)`,
`Audit --explain contract self-test (Phase 94)`, `Audit determinism / JSON-stability self-test (Phase 95)`,
`Self-test README inventory parity (Phase 102)`, `Self-test QA baseline footer (Phase 103)`,
`Self-test §27 inventory parity triangle (Phase 112)`, `Self-test WEIGHTS dimension-table parity (Phase 113)`).
The remaining six are folded into their broader-contract production gates per the H1
workflow-step parity lesson (footer rows = workflow gates = declared count): `test-check-99-summary-freshness.sh`
runs inside `§99 Summary freshness gate (Phase H1 / H8 / H9)`, `test-check-99-stamp-bump.sh` inside
`§99 Stamp-bump gate (Phase H5)`, `test-archive-exclusion-runtime.sh` inside
`Runtime archive-exclusion gate (Phase H7)`, `test-check-version-parity.sh` inside
`Version-field parity gate (Phase P15 / H10)`, `test-check-spec-cross-links.sh` inside
`Spec cross-link gate (zero broken links allowed)` (Phase P35), and `test-inline-code-blanking-parity.sh`
also inside `Spec cross-link gate (zero broken links allowed)` (Phase P45) — both lock the
strict-cross-link contract from different angles (waiver fuzzy-match + JS↔Python helper parity).

---

## Coverage triad: what each test catches

The ten tests together form a **complete blind-spot coverage matrix** for
the audit subsystem (gates 1–3), the meta-suite itself (gates 4–7), and the
§99 lifecycle / archive-exclusion contracts (gates 8–10):

| Blind spot | Why production gate misses it | Self-test catching it |
|---|---|---|
| Comparison-operator inversion (`<` vs `≤`, `≥` vs `>`) | All scores currently above floor; bug invisible | **Phase 91** (6 cases at the boundary) |
| `--explain` diagnostic tool silently broken | Production gate never invokes `--explain` | **Phase 94** (14 assertions across single-match / no-match / multi-match) |
| Non-determinism introduced into the rubric | Production gate runs only once per build | **Phase 95** (sha256 byte-identity across two runs) |
| Self-test added/removed without updating this README | Reviewer-attention only; AC-31-27 was unenforced | **Phase 102** (filesystem ↔ inventory parity, structural sections, executable bit) |
| QA-baseline footer drifting from `RUBRIC_VERSION` / workflow / declared count | Production audit gate still passes while docs lie; AC-31-28 was unenforced | **Phase 103** (4-way enumeration consistency: script constant ↔ 00-index ↔ EXECUTIVE-SUMMARY ↔ workflow steps) |
| New script silently added to `linter-scripts/` or `.github/workflows/` without a §27 spec row OR an entry in the Phase 107 orphan ledger | `check-tree-health.cjs` allow-list inference is permissive (Phase 107 found 8 silent orphans); AC-31-31 / INV-01 / INV-02 were unenforced | **Phase 112** (3-way triangle: §27 overview ↔ filesystem ↔ Phase 107 orphan memo) |
| Dimension `WEIGHTS` drifting between `audit-spec-vs-code-v2.py`, `generate-gate-report.py`, and §31's `## Weights` table | AC-31-02's runtime assertion only catches in-script drift in the audit script alone; gate-report and §31 docs were unenforced and could silently produce divergent scoring | **Phase 113** (3-way dict-equality + AC-31-02 invariants + dimension count == 7) |
| §99 `## Summary` prose stamped `<!-- verified-phase: NNN -->` going stale (claimed phase older than newest §98 row) | Production audit gate scores §99 structurally; stale narrative claims are invisible to it (Phase 136 over-counted, Phase 139 found real count was 1) | **Phase H1** (advisory→strict per opt-in stamp; sandbox-tested 17 assertions covering unstamped/stamped-stale/stamped-fresh/missing-token paths) |
| §99 stamped+materially-edited without a phase-token bump | No production gate enforces "edited-then-stamp-must-bump"; reviewer-attention only | **Phase H4** (`--changed-files` injection bypasses git sandbox; 23 assertions across empty/unstamped/stamp-only/material-edit/`_archive/` exclusion/bad-base-ref paths) |
| Spec-traversing linters reading `_archive/` paths at RUNTIME despite source-level allow-list (the H6 lesson) | Source-reading proves intent, not behavior; only runtime enumeration proves a linter actually skips the directory | **Phase H7** (importlib-loads 3 critical enumerators, asserts 0 archive-leaked results; floor: probe count ≥ 3) |
| Cross-link allowlist waiver line numbers drifting after stamp-batch tools insert comment lines above (the P34 lesson #1 — silent CI failure that survived 12 phases) | Exact-line key match made the gate fragile to unrelated edits; reviewer-attention only | **Phase P35** (synthetic sandbox: 19 assertions across fuzzy-match drift ≤ 5 lines, `--rewrite-allowlist` idempotence, `--strict-line-match` opt-in, out-of-tolerance non-match) |

If you add an eleventh contract guarantee to the audit script (or any other
linter), add an eleventh self-test here following the same template — see
**"Adding a new self-test"** below. The Phase 102 gate will fail on your
PR if you forget to add the row; the Phase 103 gate will fail if you wire
the new step into the workflow without bumping the audit footer's
gate-count enumeration in lockstep; the Phase 112 gate will fail if you
add a script without updating §27 §00-overview or the Phase 107 ledger;
the Phase 113 gate will fail if you change scoring weights in only one
of the three sites that restate them.

---

## Test-discovery policy (Phase F3 — keep `.sh`-only)

The ten scripts above are **shell tests**, and the parity gate
([`test-readme-inventory.sh`](./test-readme-inventory.sh)) discovers them
via `ls test-*.sh`. This is **deliberate**, not an oversight:

- **CI uniformity** — every shell test runs under the same `bash` runtime
  the workflow already provisions; no Python venv coupling, no
  hyphenated-module-name `importlib` dance, no per-test interpreter
  detection.
- **Side-effect surface** — `set -euo pipefail` + `assert` helper give us
  a uniform pass/fail/exit-code contract. A Python `unittest`/`pytest`
  test would need its own contract restatement (Phase 102 was authored
  against the shell shape).
- **Readability for spec authors** — most contributors editing
  `spec/27-spec-toolchain/` are spec authors first, not Python
  developers; a 30-line bash assertion file is more approachable than
  an `importlib.util.spec_from_file_location` incantation.

**Rule (codified Phase F3):** New self-tests SHOULD be `.sh`. The only
sanctioned exception is when the script-under-test fundamentally requires
Python introspection that bash cannot reproduce ergonomically — for
example, exercising a `load_allowlist()` function as a unit (rather than
its CLI surface) requires `importlib`-loading a hyphenated source file
([`test-check-spec-folder-refs.py`](./test-check-spec-folder-refs.py),
Phase 144 — locks AC-62-04). Such Python tests are listed in **Adjacent
`.py` tests** below; they are NOT covered by the README inventory parity
gate (which remains `.sh`-only by design) and instead rely on
[`test-overview-inventory-parity.sh`](./test-overview-inventory-parity.sh)
for filesystem-level acknowledgement.

If you find yourself reaching for `.py` for any other reason (better
assertion library, prettier diff output, etc.), that is **not** a
sanctioned exception — write the `.sh` test instead. The cost of
multi-runtime tests grows non-linearly; we pay the bash-test ergonomic
tax intentionally.

### Adjacent `.py` tests (acknowledged, not parity-gated)

| Test script | Phase | Asserts about | Why `.py` (sanctioned exception) |
|---|---|---|---|
| [`test-check-spec-folder-refs.py`](./test-check-spec-folder-refs.py) | 144 | `check-spec-folder-refs.py::load_allowlist()` strips inline `# comment` trailers (AC-62-04) — 4 `tempfile`-based unit tests | Exercises an internal function, not the CLI; loading the hyphenated source requires `importlib.util.spec_from_file_location`, which is awkward in bash. |

These are CI-runnable via `python3 linter-scripts/test/test-*.py` but
not yet wired as discrete steps in `spec-health.yml`. Acknowledgement
flows through `test-overview-inventory-parity.sh` (Phase 112) instead of
the README parity gate, which remains `.sh`-only by design.

### Adjacent runners (acknowledged, exempt from both parity gates by design)

| Runner | Phase | Composes | Why no `test-` prefix |
|---|---|---|---|
| [`cluster-terminal-sweep.sh`](./cluster-terminal-sweep.sh) | P40 | All 9 critical CI gates (tree-health `--strict`, lockstep, version-parity `--strict`, cross-links, folder-refs, freshness `--strict-position`, trace-map regression, §27 inventory parity, README inventory parity) — single-command runner with formatted PASS/FAIL counters and remediation hints citing Phase 18 rebaseline rule, P35 `--rewrite-allowlist`, and the P23/P24/P25/P26 reverse-drift subcase taxonomy | This file is a **runner**, not a self-test — it composes existing tests and gates rather than asserting new behaviour. Naming without the `test-` prefix is intentional: the [`test-readme-inventory.sh`](./test-readme-inventory.sh) parity gate scopes to `test-*.sh` glob, so runners are exempt from inventory-table membership. The [`test-overview-inventory-parity.sh`](./test-overview-inventory-parity.sh) gate scopes to `linter-scripts/` top-level only (via `find linter-scripts -maxdepth 1`), so files under `linter-scripts/test/` are also exempt from §27 §00 inventory enumeration. The runner sits in a deliberate dead-zone between both parity surfaces — visible to contributors via this subsection, exempt from both parity contracts by glob/scope.

**Use case:** run `bash linter-scripts/test/cluster-terminal-sweep.sh` at the END of any cluster of phases (advisory→strict landings, batch sweeps, refactors, dashboard refreshes, etc.) BEFORE declaring the cluster closed. Mechanizes the P34/P38 cadence rule (codified in `mem://index.md` Core P34/P38/P40 entries): both P34 and P38 caught silent regressions (stale cross-link waivers; stale trace-map baseline) that strict CI would have flagged only at next PR — proving the cadence catches real failures the strict-mode CI does not pre-catch.

**When to add another runner:** if you find yourself memorizing a multi-gate procedure that runs at a recurring lifecycle moment (cluster-end, pre-release, post-rebaseline, etc.), graduate it to a runner here. Use the same naming dead-zone (no `test-` prefix, under `linter-scripts/test/`). Document it in this subsection with the same "Composes" + "Why no `test-` prefix" + "Use case" + "When to add another" structure. The graduation cost is one-shot; the discipline cost recurs every cycle. Codified P40 lesson #2.



---

## Adjacent gates (not in this directory but logically siblings)

These are full-tree linter gates rather than per-script contract tests, so
they live one level up in `linter-scripts/`. They are listed here for
discoverability:

| Script | Phase | Gate type | What it parses |
|---|---|---|---|
| [`../check-mermaid-syntax.mjs`](../check-mermaid-syntax.mjs) | 97 | Full-tree | Every `spec/**/*.mmd` file with the `mermaid` library under a `jsdom` shim — catches broken diagram syntax pre-merge |
| [`../check-tree-health.cjs`](../check-tree-health.cjs) | (multiple) | Full-tree | Every `spec/<module>/` for the four-required-files rule + naming + structure |
| [`../check-lockstep.cjs`](../check-lockstep.cjs) | (multiple) | Full-tree | §97/§98/§99 version-bump synchronicity per module |
| [`../check-spec-cross-links.py`](../check-spec-cross-links.py) | (multiple) | Full-tree | Every internal `[link](./path)` resolves |
| [`../check-trace-map-regression.py`](../check-trace-map-regression.py) | 30 | Full-tree | AC coverage doesn't drop, drift doesn't grow, no orphan code |

---

## Local execution

Run any single test directly:

```bash
bash linter-scripts/test/test-audit-cli-thresholds.sh
bash linter-scripts/test/test-audit-explain-contract.sh
bash linter-scripts/test/test-audit-deterministic-stability.sh
bash linter-scripts/test/test-readme-inventory.sh
bash linter-scripts/test/test-qa-baseline-footer.sh
bash linter-scripts/test/test-overview-inventory-parity.sh
bash linter-scripts/test/test-weights-parity.sh
bash linter-scripts/test/test-check-99-summary-freshness.sh
bash linter-scripts/test/test-check-99-stamp-bump.sh
bash linter-scripts/test/test-archive-exclusion-runtime.sh
bash linter-scripts/test/test-audit-ai-implementability.sh
```

Run all ten sequentially:

```bash
for t in linter-scripts/test/test-*.sh; do
  echo "═══ $(basename "$t") ═══"
  bash "$t" || { echo "❌ $t FAILED"; exit 1; }
done
echo "✅ All self-tests passed."
```

Each script:
- Sets `AUDIT_DETERMINISTIC=1` internally (no external env required).
- Uses `set -euo pipefail` — exits non-zero on first unhandled failure.
- Prints per-assertion `✅`/`❌` lines with the asserted condition.
- Ends with `Results: <pass> passed, <fail> failed` summary.
- Exits 0 on full pass, 1 on any failure, 2 on infrastructure failure
  (audit script missing, etc.).

No script writes to `.lovable/memory/` or `spec/` — they're
side-effect-free against the repository (Phase 94 and Phase 95 explicitly
verify this with sha256 snapshots).

---

## Adding a new self-test

When you add a new contract guarantee to a `linter-scripts/` script
(new flag, new exit code, new output format, new determinism guarantee),
add a paired self-test here. Template:

```bash
#!/usr/bin/env bash
# linter-scripts/test/test-<script>-<contract>.sh
#
# Phase NN — <one-line description of the locked contract>.
#
# Locks: <which behaviour, e.g. "v2.17 (Phase 99) --foo=<bar> exit codes">
#
# Without this self-test, <describe the regression that could ship
# unnoticed and why the production gate wouldn't catch it>.
#
# Spec: spec/<module>/<file>.md (AC-<MOD>-NN)
# Memo: .lovable/memory/audit/v2-deterministic/phase-NN-<slug>.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$SCRIPT_DIR/<script-under-test>"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

[ -f "$TARGET" ] || { echo "❌ target script not found: $TARGET"; exit 2; }

cd "$REPO_ROOT"
PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then echo "✅ $label"; PASS=$((PASS+1))
  else          echo "❌ $label"; FAIL=$((FAIL+1)); fi
}

# ── Assertions ───────────────────────────────────────────────────
# assert "label" command-that-exits-0-on-success

# ── Summary ──────────────────────────────────────────────────────
echo "======================================="
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
echo "✅ <contract name> intact."
```

Then:

1. `chmod +x` the new script.
2. Add a new step to `.github/workflows/spec-health.yml` (modelled on
   the existing three, with a 6-line comment block explaining the
   blind spot it covers).
3. Add a row to the **Test inventory** and **Coverage triad** tables
   in this README.
4. Add the corresponding `AC-<MOD>-NN` to the relevant `97-acceptance-criteria.md`,
   bumping that module's `97`/`98`/`99` in lockstep.
5. Write the post-merge phase memo at
   `.lovable/memory/audit/v2-deterministic/phase-NN-<slug>.md`.

---

## See also

- **Spec:** [`spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`](../../spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md) — the canonical contract for the audit script (all `AC-31-*` IDs).
- **CI workflow:** [`.github/workflows/spec-health.yml`](../../.github/workflows/spec-health.yml).
- **Local runner:** [`linter-scripts/run.sh`](../run.sh) — runs the full-tree gates locally; the self-tests run in CI.
- **Phase memos:**
  [Phase 91](../../.lovable/memory/audit/v2-deterministic/phase-91-cli-self-test.md) ·
  [Phase 94](../../.lovable/memory/audit/v2-deterministic/phase-94-explain-contract-test.md) ·
  [Phase 95](../../.lovable/memory/audit/v2-deterministic/phase-95-determinism-stability.md) ·
  [Phase 97](../../.lovable/memory/audit/v2-deterministic/phase-97-mermaid-syntax-gate.md) ·
  [Phase 98](../../.lovable/memory/audit/v2-deterministic/phase-98-test-readme.md) ·
  [Phase 102](../../.lovable/memory/audit/v2-deterministic/phase-102-readme-inventory-test.md) ·
  [Phase 103](../../.lovable/memory/audit/v2-deterministic/phase-103-qa-baseline-footer-test.md) ·
  [Phase 107](../../.lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md) ·
  [Phase 112](../../.lovable/memory/audit/v2-deterministic/phase-112-overview-inventory-parity-test.md) ·
  [Phase 113](../../.lovable/memory/audit/v2-deterministic/phase-113-weights-parity-test.md)

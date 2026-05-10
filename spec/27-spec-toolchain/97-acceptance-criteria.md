# Acceptance Criteria — Spec Toolchain

**Version:** 2.17.0
**Updated:** 2026-05-07 (Phase J9 — AC-T-35 binds slot 35 `audit-bundle-budget.py` into §97 with delegation-map + family-prefix + trace-map triplet (Lesson #19 + #21 + #36 + #65). AC count 32 → 33; module-level total 33 + delegated ≥105 = ≥138.)
**Updated-prev:** 2026-05-05 (Phase 153 Task A18-impl-3: slot 34 §00 v1.7.0 → v1.8.0 codifies AC-34-17 — chunked re-scoring promoted to default-on; `audit_module()` routes multi-chunk modules through gateway-per-chunk + `merge_chunk_scores()` weighted-merge; FULL-tier parity invariant preserved verbatim (spec/16 cross-flag bundle_sha equality `e16de187513b288e`); new `--no-chunked` rollback flag. Live re-scores: spec/27 83→88, spec/12 87→84 (honest baseline per Lesson #18). Closes AC-34-15(e) "promotion to default" milestone.)
**Scope:** `spec/27-spec-toolchain/`

---

## Module-level criteria

### AC-T-01 — Bijection between code and spec
- **Given** the set of executable files under `linter-scripts/` (extensions `.py`, `.cjs`, `.sh`, `.ps1`, `.go`) plus configuration files (`.toml`, `.allowlist`, `readme-cross-links.md`) and the set of workflows under `.github/workflows/*.yml`,
- **When** the spec sections in this module are enumerated,
- **Then** every code artifact MUST appear in exactly one spec section, and every spec section MUST point to exactly one code artifact that exists on disk.
- **Worked example:** `comm -3 <(ls linter-scripts/*.{py,cjs,sh,ps1,go} 2>/dev/null | xargs -n1 basename | sort) <(grep -hoE '(linter-scripts|\.github/workflows)/[A-Za-z0-9._-]+' spec/27-spec-toolchain/*.md | xargs -n1 basename | sort -u)` MUST output zero lines (perfect bijection); any line on the left = orphan code (no spec); any line on the right = orphan spec (dangling reference).

### AC-T-02 — Inventory matches numbering convention
- **Given** the inventory tables in [`00-overview.md`](./00-overview.md),
- **When** each spec filename is checked against its category range (01–09 validators, 10–19 generators, 20–29 fillers, 30–39 auditors, 40–49 runners, 50–59 source validators, 60–69 configs, 70–79 CI),
- **Then** every entry MUST sit in the documented range for its category.
- **Worked example:** `01-check-spec-cross-links.md` (validator, slot 01–09) ✓; `10-generate-spec-index.md` (generator, slot 10–19) ✓; a hypothetical `15-fill-missing-foo.md` (filler in generator range) MUST FAIL — fillers belong to slots 20–29.

### AC-T-03 — Exit-code contract
- **Given** any spec file in slots 01–09 or 50–59 (validators),
- **When** the file is read,
- **Then** it MUST contain a section titled "Exit codes" listing at minimum `0` (pass), `1` (fail), and where applicable `2` (error / invocation problem).
- **Worked example:** `grep -l '^## Exit codes$' spec/27-spec-toolchain/{01..09}-*.md spec/27-spec-toolchain/{50..59}-*.md | wc -l` MUST equal the count of validator files; for each: `awk '/^## Exit codes$/,/^## /' <file> | grep -E '^\| ?(0|1) '` MUST match both rows.

### AC-T-04 — Idempotency declaration on fillers
- **Given** any spec file in slots 20–29,
- **When** the file is read,
- **Then** it MUST contain the literal phrase `idempotent` and explicitly state that re-runs on a satisfied tree are no-ops.
- **Worked example:** `for f in spec/27-spec-toolchain/{20..29}-*.md; do grep -qi 'idempotent' "$f" || echo "MISSING: $f"; done` MUST print zero lines; cross-checked at runtime by AC-T-12's `git diff --exit-code` invariant after a second filler run.

### AC-T-05 — Each spec lists the script's CLI surface
- **Given** any per-artifact spec section in this module,
- **When** the file is read,
- **Then** it MUST include a "Usage" code block showing the canonical invocation, and a list of supported CLI flags (or `_(none)_` if there are none).
- **Worked example:** `01-check-spec-cross-links.md` contains ` ```\npython3 linter-scripts/check-spec-cross-links.py [--github]\n``` ` plus a flag table listing `--github`; a spec section with no Usage block MUST FAIL the linter `check-spec-cli-surface.py` (Phase 153 Task A9).

### AC-T-06 — Each spec links back to the source file with a relative repo path
- **Given** any per-artifact spec section,
- **When** the file is read,
- **Then** it MUST link to the source file using a markdown link whose label is `` `linter-scripts/<name>` `` and whose target is `../../linter-scripts/<name>` (or `../../.github/workflows/<name>` for CI workflows).
- **Worked example:** `01-check-spec-cross-links.md` contains `` [`linter-scripts/check-spec-cross-links.py`](../../linter-scripts/check-spec-cross-links.py) ``; alternative absolute paths (`/linter-scripts/...`) or bare names (`check-spec-cross-links.py`) MUST FAIL the §10 spec-index generator's link-shape assertion.

### AC-T-07 — Slot immutability
- **Given** the §99 consistency report,
- **When** a script is deleted,
- **Then** its slot number MUST be marked "retired" in [`99-consistency-report.md`](./99-consistency-report.md) and MUST NOT be reused for a new artifact.
- **Worked example:** When `audit-spec-vs-code.py` (slot 30) is superseded by `audit-spec-vs-code-v2.py`, slot 30 MUST be marked `retired (superseded by §31)` in §99 and the new script MUST take a fresh slot (31), NOT reclaim 30. Reuse triggers `mem://index.md` Core "slot immutability" violation caught by `check-99-stamp-bump.py`.

### AC-T-08 — Spec-health workflow trigger paths cover this module
- **Given** the workflow file `.github/workflows/spec-health.yml`,
- **When** its `on.push.paths` and `on.pull_request.paths` are inspected,
- **Then** they MUST include `spec/27-spec-toolchain/**` (so changes here re-run the gate) — see [`70-spec-health-yml.md`](./70-spec-health-yml.md) §3.
- **Worked example:** `yq '.on.push.paths[], .on.pull_request.paths[]' .github/workflows/spec-health.yml | grep -Fx 'spec/27-spec-toolchain/**'` MUST return a match on BOTH triggers; absence means a §27 spec edit ships unchecked, defeating the meta-linter purpose.

### AC-T-09 — Tree-health gate
- **Given** the entire `spec/` tree,
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run,
- **Then** this module MUST contribute `required=2/2` (overview + consistency report present) and the overall score MUST be ≥ 80.
- **Worked example:** `node linter-scripts/check-tree-health.cjs --min=80 --json | jq '.modules["spec/27-spec-toolchain"].required'` MUST emit `"2/2"`; `jq '.score >= 80'` MUST emit `true`. Removing `00-overview.md` drops `required` to `1/2` and fails the gate with exit `1`.

### AC-T-10 — Spec cross-link gate (zero broken links)
- **Given** every relative link inside `spec/**/*.md`,
- **When** `python3 linter-scripts/check-spec-cross-links.py --github` is run as a CI gate (see `.github/workflows/spec-health.yml` step "Spec cross-link gate"),
- **Then** the script MUST exit 0 with `OK All internal spec cross-references resolve` and ANY broken target MUST fail the build (zero-broken-link contract). Allowlist exceptions live in `linter-scripts/spec-cross-links.allowlist`; entries there bypass the gate intentionally and MUST carry an inline comment justifying the exemption.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` (binds the AC to its implementation per `linter-scripts/trace-map.toml:115-118`).
- **Worked example:** `python3 linter-scripts/check-spec-cross-links.py --github; echo "exit=$?"` MUST print `OK All internal spec cross-references resolve` then `exit=0`. Inserting `[broken](./does-not-exist.md)` into any spec file MUST flip the run to `exit=1` with a stderr `<file>:<line>: broken-link: ...` line consumable by the GitHub problem matcher.

### AC-T-11 — Validator output goes to the correct stream
- **Given** any validator script in slots 01–09 or 50–59 (extensions `.py`, `.cjs`, `.sh`, `.ps1`, `.go`),
- **When** the script is executed and produces findings,
- **Then** ALL violation messages MUST be written to **stderr** (not stdout) and structured as `<file>:<line>: <rule-id>: <message>` so CI log parsers + IDE problem-matchers can extract them deterministically; success-summary lines (e.g. `0 findings`, `OK`) MAY go to stdout; mixing the two streams is FORBIDDEN because downstream tooling pipes stdout to JSON parsers and stderr to log aggregators.
- **Verifies:** AC-T-03 exit-code contract; `linter-scripts/run.sh` orchestrator (relies on stderr separation to surface failures); `.github/workflows/spec-health.yml` problem-matcher convention.
- **Worked example:** `python3 linter-scripts/check-spec-cross-links.py >/tmp/out 2>/tmp/err; wc -l </tmp/err` MUST be `0` on a clean tree; after injecting one broken link, `/tmp/err` MUST contain a `<file>:<line>: broken-link: <msg>` line and `/tmp/out` MUST stay parseable as a one-line summary (no findings interleaved).

### AC-T-12 — Filler scripts MUST be safe to run in a tight loop
- **Given** any filler script in slots 20–29 (`fill-missing-acceptance-criteria.cjs`, `fill-missing-changelogs.cjs`, `fill-missing-consistency-reports.cjs`),
- **When** the script is executed N times consecutively against the same `spec/` tree,
- **Then** the second through Nth runs MUST produce **byte-identical** output to the disk state at the end of the first run — no new files created, no existing files mutated, no banner timestamps bumped, no AC bodies regenerated. Idempotency is verified by the `git diff --exit-code` invariant in `linter-scripts/run.sh` after the self-heal pipeline. Re-running a filler against an already-complete tree MUST exit `0` with a stdout summary like `0 files created` and zero stderr output.
- **Verifies:** AC-T-04 idempotency declaration; SELF-HEAL pipeline contract in `mem://index.md` Core; `linter-scripts/run.sh` post-fill `git diff` gate.
- **Worked example:** `for i in 1 2 3; do node linter-scripts/fill-missing-acceptance-criteria.cjs; done; git diff --exit-code spec/` MUST exit `0` after run 2 and run 3 (run 1 may legitimately create files). Any non-zero exit means a filler is non-idempotent and MUST be patched before merge.

### AC-T-13 — Generators are deterministic given identical disk truth
- **Given** any generator in slots 10–19 (e.g. `generate-spec-index.cjs`, `generate-dashboard-data.cjs`, `generate-trace-map.py`),
- **When** the generator is run twice on the same `spec/` snapshot (no edits between runs),
- **Then** the produced artifact MUST be **byte-identical** between runs — no embedded `Date.now()`, no `Math.random()`, no environment-leaked values (`$USER`, `$HOSTNAME`, `process.env.CI`), no map-iteration order non-determinism (use `Array.from(map).sort()` or equivalent). Embedded `Generated: <date>` lines MUST use a **content-derived** timestamp (`git log -1 --format=%cI` of the latest spec-tree change) rather than `new Date()` — non-deterministic generators trigger phantom diffs that drown real changes in PRs.
- **Verifies:** AC-T-01 bijection (regenerated artifacts must round-trip); `linter-scripts/generate-spec-index.cjs`; `linter-scripts/generate-dashboard-data.cjs`; `linter-scripts/audit-spec-vs-code-v2.py` (extended coverage). **Mechanical lock (P49):** `linter-scripts/test/test-audit-deterministic-stability.sh` runs each generator twice on the live `spec/` tree and asserts byte-identical output (sha256 + byte-count) across runs — auditor + spec-index + dashboard-data, snapshot-restore-safe (working tree byte-identical pre/post). 13/13 assertions GREEN.
- **Worked example:** `node linter-scripts/generate-spec-index.cjs && sha256sum spec/INDEX.md > /tmp/a; node linter-scripts/generate-spec-index.cjs && sha256sum spec/INDEX.md > /tmp/b; diff /tmp/a /tmp/b` MUST be empty. A non-empty diff implies wall-clock leakage (`new Date()`) or unsorted map iteration — fix by switching to `git log -1 --format=%cI` and `Array.from(map).sort()`.

### AC-T-14 — Auditor scripts MUST emit machine-readable JSON alongside human-readable Markdown
- **Given** any auditor script in slots 30–39 (`audit-spec-vs-code.py`, `audit-spec-vs-code-v2.py`),
- **When** the auditor is invoked with `--format json` (mandatory flag),
- **Then** the output MUST be valid JSON parseable by `json.loads()` / `JSON.parse()` with a fixed top-level shape `{score: number, max_score: number, grade: string, findings: Array<{rule_id: string, severity: "low"|"medium"|"high"|"critical", file: string, line: number|null, message: string}>, generated_at: string}`. The default invocation (no flag) emits Markdown for humans. Auditors WITHOUT a JSON mode are FORBIDDEN because the dashboard generator (§11) consumes JSON only. Schema versioning: bumping the JSON shape is a major version of the auditor and triggers a §98 changelog entry.
- **Verifies:** AC-T-05 CLI surface; §11 `generate-dashboard-data.cjs` (consumer); `mem://index.md` measured-not-narrated rule.
- **Worked example:** `python3 linter-scripts/audit-spec-vs-code-v2.py --format json | jq -e '.score, .max_score, .grade, (.findings | type == "array")'` MUST exit `0` and emit four non-null values; `jq -e '.findings[0] | has("rule_id") and has("severity") and has("file")'` MUST emit `true`. An auditor returning Markdown under `--format json` MUST FAIL the dashboard build (§11) with a JSON parse error.

### AC-T-15 — Configuration files (slots 60–69) MUST be self-validating
- **Given** any configuration file in slots 60–69 (`forbidden-strings.toml`, `spec-cross-links.allowlist`, `spec-folder-refs.allowlist`, `readme-cross-links.md`),
- **When** the file is loaded by its consumer validator,
- **Then** the consumer MUST refuse to start (exit `2`, NOT exit `1`) if the config is malformed: TOML files MUST be parseable by `tomllib.load()`; `.allowlist` files MUST follow the documented `# comment` + `<path>` line format; every allowlist entry MUST carry a trailing `# reason: <free-text>` comment explaining why the exception exists (silent allowlist entries accumulate as zombie waivers). The consumer's spec section MUST cite the config's spec section bidirectionally — §03 ↔ §60, §01 ↔ §61, §02 ↔ §62.
- **Verifies:** AC-T-06 bidirectional source links; §03/§60 contract; §01/§61 contract; §02/§62 contract.
- **Worked example:** `python3 -c "import tomllib; tomllib.load(open('linter-scripts/forbidden-strings.toml','rb'))"` MUST exit `0`; `awk '!/^#/ && NF && !/# reason:/' linter-scripts/spec-cross-links.allowlist` MUST print zero lines (every entry carries a `# reason:` comment). A malformed TOML config MUST cause its consumer to exit `2` (config error), NOT `1` (findings).

### AC-T-16 — Runners (slots 40–49) MUST be functionally equivalent across platforms
- **Given** the two orchestrator entry points `linter-scripts/run.sh` (slot 40) and `linter-scripts/run.ps1` (slot 41),
- **When** both are executed against the same `spec/` tree on Linux + Windows respectively,
- **Then** they MUST execute the SAME ordered pipeline: (1) validate → (2) fill-consistency → (3) fill-AC → (4) fill-changelogs → (5) regen-index → (6) tree-health gate. Each pipeline step MUST exit with the same code on both platforms (deterministic to within line-ending normalization). Adding a new step requires editing BOTH runners in the same PR — drift between `run.sh` and `run.ps1` is a CI failure caught by a future twin-diff linter. The shared step list lives in `mem://index.md` Core ("SELF-HEAL pipeline") so a single source of truth governs both.
- **Verifies:** AC-T-01 bijection; SELF-HEAL pipeline in `mem://index.md` Core; §40/§41 spec sections.
- **Worked example:** `diff <(grep -oE '(validate|fill-[a-z-]+|regen-[a-z-]+|check-[a-z-]+)' linter-scripts/run.sh | nl) <(grep -oE '(validate|fill-[a-z-]+|regen-[a-z-]+|check-[a-z-]+)' linter-scripts/run.ps1 | nl)` MUST be empty (same ordered step list). Adding a step to `run.sh` only — without the matching `run.ps1` edit — MUST fail the twin-diff check in CI.

### AC-T-17 — Trace-map (§14) MUST round-trip from spec to code and back
- **Given** the spec ↔ code traceability map produced by `linter-scripts/generate-trace-map.py` (slot 14) consuming `linter-scripts/trace-map.toml`,
- **When** the trace map is rebuilt from disk truth,
- **Then** every spec module folder MUST appear as either a `[[mappings]]` entry (with at least one `target` path that exists on disk) OR an explicit `[[orphans]]` entry (with a written justification ≥ 20 chars). `target` paths MUST resolve to files that exist (no dangling code references); spec sections MUST resolve to existing folders (no dangling spec references). Orphan growth (delta ≥ 1 since main branch) fails CI via `check-trace-map-regression.py` (slot 17). The three FORBIDDEN trace-map ideas (auto-proposer, OpenAPI export, sub-file endpoint extraction) per `mem://constraints/forbidden-trace-map-ideas` MUST NOT be implemented or scaffolded — hard-block.
- **Verifies:** §14 generator; §17 regression gate; `mem://constraints/forbidden-trace-map-ideas` (FORBIDDEN ideas).
- **Worked example:** `python3 linter-scripts/generate-trace-map.py --validate` MUST exit `0`; for every `[[mappings]]` entry, `test -e "$target"` MUST succeed; `python3 linter-scripts/check-trace-map-regression.py --base origin/main` MUST report `orphan_delta=0`. A new `[[orphans]]` entry without a ≥20-char justification MUST fail with `orphan-justification-too-short`.

### AC-T-18 — Twin implementations (Python + Go) MUST agree byte-for-byte
- **Given** the validator twins `linter-scripts/validate-guidelines.py` (slot 50) and `linter-scripts/validate-guidelines.go` (slot 51), or any future twin-pair where Python is the reference and Go is the port,
- **When** both binaries are run against the same source tree,
- **Then** the union of findings MUST be identical: same rule IDs, same file paths, same line numbers, same severity, same message text (modulo language-specific quote characters which MUST be normalized to ASCII `"`). Drift is detected by a daily CI job that diffs `validate-guidelines.py --format json` against `validate-guidelines.go --format json` and fails on any mismatch. The Python implementation is the SOURCE OF TRUTH — when adding a new rule, the Python version lands first; the Go port follows in the same PR. Shipping the Go port WITHOUT the Python rule update is FORBIDDEN.
- **Verifies:** AC-T-14 JSON output contract; §50/§51 spec sections; `mem://specs/full-tree-audit-v4.md` twin-implementation invariant.

### AC-T-19 — CI workflows (slots 70–79) MUST trigger on every relevant path
- **Given** the CI workflow `.github/workflows/spec-health.yml` (slot 70),
- **When** its `on.push.paths` and `on.pull_request.paths` arrays are inspected,
- **Then** they MUST include ALL of: `spec/**` (any spec edit re-runs the gate), `linter-scripts/**` (any toolchain edit re-runs the gate), `.github/workflows/spec-health.yml` (workflow edits self-validate), `linter-scripts/spec-cross-links.allowlist` (allowlist edits re-validate), `linter-scripts/forbidden-strings.toml` (config edits re-validate). Workflow MUST run on `push` to `main` AND on `pull_request` to `main` — single-trigger workflows are FORBIDDEN because they leak unguarded merges. The minimum-score threshold MUST be `100` (locked at A+ per `mem://index.md` Core) — lowering the threshold is a major version bump of slot 70 and requires a §98 entry with written justification.
- **Verifies:** AC-T-08 trigger paths; §70 spec section; `mem://index.md` Core "CI threshold locked at 100".

### AC-T-20 — `trace-map.md` is informational, NOT acceptance surface
- **Given** the `trace-map.md` file present in this module (alongside slots 01–79),
- **When** the file inventory in `99-consistency-report.md` is built,
- **Then** `trace-map.md` MUST be classified as a **rendered output** of slot 14 (`generate-trace-map.py`) and MUST NOT carry a slot number, version banner, or §97 acceptance criteria of its own. The file is regenerated by §14 on every spec change and is NOT hand-edited. Its acceptance surface is delegated entirely to AC-T-17 (round-trip integrity). Adding a slot number to `trace-map.md` (e.g. `80-trace-map.md`) is FORBIDDEN — slots 80+ are reserved for future categories not yet defined. The file MUST be referenced from §14's spec section as "Output: `./trace-map.md`" so readers can discover the rendered artifact without searching.
- **Verifies:** AC-T-17 trace-map round-trip; §14 spec section; slot-immutability rule (slots 80+ reserved).

### AC-T-21 — Phase 107 orphan ledger as transitional INV-01 satisfaction (Phase 108-min, INV-08)
- **Given** an executable file under `linter-scripts/` or `.github/workflows/` exists WITHOUT a corresponding `spec/27-spec-toolchain/NN-*.md` slot,
- **When** `linter-scripts/test/test-overview-inventory-parity.sh` (Phase 112) enumerates the §27 inventory triangle (filesystem ↔ §00 overview ↔ Phase 107 orphan ledger),
- **Then** the script MUST exit 0 if AND ONLY IF the orphan code file is listed in the "Code → Spec orphans" table of `.lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md`. A code file that is neither specced in §27 NOR ledgered in Phase 107 MUST cause exit 1; AND every ledger entry MUST migrate to a real `NN-*.md` spec within two release cycles (sustained ledger-only tracking is technical debt, not a permanent home — see Phase 108 Strategy B for the migration cleanup); AND adding a new orphan to the ledger MUST happen in the SAME PR that adds the code (no after-the-fact ledger backfills); AND the ledger is **acknowledgement, not absolution**: it satisfies the INV-01 gate transitionally but does NOT exempt the code from the eventual `NN-*.md` spec requirement.
- **Verifies:** INV-08 (Normative Contract block in §00 overview), Phase 112 self-test (`linter-scripts/test/test-overview-inventory-parity.sh`), AC-31-31 (the upstream invariant Phase 112 enforces), Phase 107 orphan ledger (`.lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md`), Phase 108 backlog (Strategy B migration plan).

### AC-T-22 — Slot 18 (`check-mermaid-syntax.mjs`) is bijection-satisfying (Phase 108-full)
- **Given** [`spec/27-spec-toolchain/18-check-mermaid-syntax.md`](./18-check-mermaid-syntax.md) exists and references `linter-scripts/check-mermaid-syntax.mjs`,
- **When** `linter-scripts/test/test-overview-inventory-parity.sh` and `node linter-scripts/check-tree-health.cjs --strict` run,
- **Then** both MUST exit 0 with the script counted as specced (NOT ledger-tracked); AND the §00 inventory row in the Generators table MUST point at the slot-18 spec; AND the script's slot-range exception (validator inside the 10-19 generator band) MUST be documented in §18 and acknowledged in this AC as a Phase 108-full deliberate choice (not a violation of INV-03 — the slot is new, not relabelled).
- **Verifies:** INV-01, INV-02, INV-08 (this AC moves O1 OUT of the ledger), Phase 107 ledger row O1 (now marked migrated), Phase 108-full retrospective.

### AC-T-23 — Slot 19 (`check-memo-retrospective-headings.py`) is bijection-satisfying (Phase 108-full)
- **Given** [`spec/27-spec-toolchain/19-check-memo-retrospective-headings.md`](./19-check-memo-retrospective-headings.md) exists and references `linter-scripts/check-memo-retrospective-headings.py`,
- **When** `linter-scripts/test/test-overview-inventory-parity.sh` and `node linter-scripts/check-tree-health.cjs --strict` run,
- **Then** both MUST exit 0 with the script counted as specced (NOT ledger-tracked); AND the §00 inventory row in the Generators table MUST point at the slot-19 spec; AND the slot-range exception (validator inside the 10-19 band) MUST be documented in §19 alongside the Phase 100 cadence-retirement rationale this script enforces.
- **Verifies:** INV-01, INV-02, INV-08, Phase 100 cadence retirement, Phase 107 ledger row O2 (now marked migrated), Phase 108-full retrospective.

### AC-T-24 — Slot 25 (`deepen-consistency-reports.py`) is bijection-satisfying (Phase 108-full)
- **Given** [`spec/27-spec-toolchain/25-deepen-consistency-reports.md`](./25-deepen-consistency-reports.md) exists and references `linter-scripts/deepen-consistency-reports.py`,
- **When** `linter-scripts/test/test-overview-inventory-parity.sh` and `node linter-scripts/check-tree-health.cjs --strict` run,
- **Then** both MUST exit 0 with the script counted as specced; AND the §00 inventory row in the Fillers table MUST point at the slot-25 spec; AND slot 25 satisfies the kind-range bijection (filler in 20-29 band) — no exception note required.
- **Verifies:** INV-01, INV-02, INV-08, Phase 21 deepen-sweep origin, Phase 107 ledger row O3 (now marked migrated), Phase 108-full retrospective.

### AC-T-25 — Spec-index drift gate MUST be strict (Phase 30)
- **Given** the `Spec-index drift gate` step in `.github/workflows/spec-health.yml` (Phase 29 root-cause: previously named "Regenerate spec-index.md (drift check)" and exited 0 with a `⚠️` warning when `git status --porcelain spec/` reported a delta after `node linter-scripts/generate-spec-index.cjs`),
- **When** any future commit causes `node linter-scripts/generate-spec-index.cjs` to produce a `spec/` filesystem delta (e.g. a file/version bump landed without re-running `bash linter-scripts/run.sh` locally),
- **Then** the workflow step MUST `exit 1` (strict mode), printing the `git diff --stat` and a `head -100` of `git diff` so the contributor can locate the stale entries; AND the script enumeration footer in `audit-spec-vs-code-v2.py` MUST list this gate as entry #18 of the QA tooling baseline; AND `linter-scripts/test/test-qa-baseline-footer.sh`'s workflow-gates awk MUST include `/Spec-index drift gate/` so footer-rows = workflow-gates = declared-count parity holds at 18/18/18.
- **Verifies:** AC-31-31 (multi-file enumeration parity at the 4-file site: script `RUBRIC_VERSION` + `00-index.md` footer + `EXECUTIVE-SUMMARY.md` cross-ref + `spec-health.yml` step list — gate count 17 → 18, RUBRIC v2.26 → v2.27); codifies the **Phase 29 root-cause lesson** "advisory CI gates silently rot" (second instance after the Phase H1 session-persistence-regression class — first instance never cleanly auto-detected); also codifies the **second-order lesson** "generator artifacts in `run.sh` need CI parity" (treat `spec-index.md` as a build artifact whose canonical source is the regenerator, not a hand-edited document).

### AC-T-26 — §00 ↔ §98 Version-field parity gate (Phase P15 / H10; Phase P31 strict-flip)
- **Given** [`spec/27-spec-toolchain/29-check-version-parity.md`](./29-check-version-parity.md) and `linter-scripts/check-version-parity.py` exist as gate #19 of the QA tooling baseline (advisory-by-default at P15 landing per AC-T-25 dispensation; reverse-drift backlog cleared P22→P30; **strict-by-CI-invocation as of Phase P31** — workflow-only flip, script default unchanged for local/backward-compat callers),
- **When** the `Version-field parity gate (Phase P15 / H10)` step runs in `.github/workflows/spec-health.yml`,
- **Then** the step MUST first execute `bash linter-scripts/test/test-check-version-parity.sh` (13/13 assertions T1–T13 — Phase P20 extended T11/T12/T13 covering the per-file stamp lifecycle) and then `python3 linter-scripts/check-version-parity.py --strict` (Phase P31: strict mode — exit 1 on any §00 ↔ §98 mismatch); AND the script enumeration footer in `audit-spec-vs-code-v2.py` MUST list this gate as entry #19 with the `--strict` invocation reflected in its description; AND `test-qa-baseline-footer.sh`'s workflow-gates awk MUST include `/Version-field parity gate/` so footer-rows = workflow-gates = declared-count parity holds at 19/19/19; AND per the H1 workflow-step-parity lesson the self-test MUST be collapsed into this gate's step (no standalone self-test step) since it exclusively exercises one numbered footer gate.
- **Verifies:** AC-31-31 (multi-file enumeration parity at the now-2-file site for P31's contract-tightening: `RUBRIC_VERSION` v2.28 → v2.29 + `spec-health.yml` step `--strict` flag; gate count unchanged at 19, so `00-index.md` footer + `EXECUTIVE-SUMMARY.md` cross-ref unchanged this phase — codifies the **P31 lesson** "AC-31-31's 4-file site is contract-dependent: new gates need all four, contract-tightening of an existing gate may need only two"); AC-T-25 (advisory dispensation lifecycle: justified at P15 by 59/74 surface; retired at P31 by P30 backlog clearance to 0/74); codifies the **Phase 21 lesson** "lockstep gate L1 only checks date relations, not version strings — §00 banner can drift many releases behind §98 while lockstep stays green"; also codifies the **Phase P15 secondary lesson** "audit retrospective surface estimates are unreliable until validated by a mechanical sweep" (the Phase 21 disposition note "1/3 historical incident, low surface" understated the real surface by ~60×); also codifies the **Phase P20 lesson** "advisory gates with no per-file strict-promotion path stall — the H1 stamp pattern (`<!-- verified-phase: NNN -->`) is the canonical migration tool" (slot 29 v1.1.0 + AC-29-11/12/13 + self-test T11/T12/T13 lock the per-file lifecycle); also codifies the **Phase P31 lesson** "workflow-only flip is the canonical advisory→strict migration tool when (a) backlog is fully cleared and (b) backward compatibility for local users matters — invert the CI invocation, not the script default" (slot 29 v1.2.0 + AC-29-14 + workflow step `--strict` lock the strict-by-CI-invocation contract).

### AC-T-27 — CODE_GLOB extensions are exhaustive per kind (Phase 153 Task A9)
- **Given** the `Normative Contract — Toolchain Bijection` block in [`00-overview.md`](./00-overview.md) at version `v1.1` or higher,
- **When** any new script is added to `linter-scripts/` with an extension NOT listed in the brace-set for its slot range (the canonical universe is `{.py, .cjs, .mjs, .sh, .ps1, .go, .toml, .allowlist, .md, .yml}`),
- **Then** the SAME PR MUST (a) bump the `CONTRACT: spec-toolchain-bijection` version comment, (b) extend the affected `CODE_GLOB` brace-list, AND (c) append a §98 changelog row referencing this AC; the `linter-scripts/check-tree-health.cjs` bijection check MUST treat any unlisted-extension script as an `FAIL-01` orphan even if a matching `NN-*.md` spec exists. This codifies the **Task A9 audit finding** "Ambiguous Code_Glob — globs may overlap or miss .mjs / .go files" and locks the contract surface so ambiguity cannot recur silently.
- **Verifies:** AC-T-01 bijection (extension drift creates phantom orphans); INV-01/INV-02 enforcement clarity; the **Phase 153 Task A9 lesson** "machine-readable contracts MUST enumerate their full extension universe — wildcard '*' or partial brace-lists invite orphan-creep that surfaces only as cryptic CI failures three phases later".

### AC-T-28 — Resilience contract for all scripts (Phase 153 Task A9)
- **Given** any executable in `linter-scripts/` (slots 01–59) or any runner (slots 40–49),
- **When** the script writes disk artifacts, reads concurrently-mutated artifacts, calls external LLM gateways, receives SIGTERM/SIGINT, or hits `ENOSPC`/`EROFS`,
- **Then** the script MUST satisfy the five rules R1–R5 documented under "Resilience — CI Edge Cases" in [`00-overview.md`](./00-overview.md): (R1) atomic temp-then-rename writes with `fsync` + `finally` cleanup; (R2) single-`read()` + 3× retry on parse failure + exit `2` on lock errors; (R3) ≤ 60s LLM timeout + 3× exponential back-off + exit `2` on exhaustion + content-keyed cache; (R4) runner SIGTERM/SIGINT trap with 5s graceful child wait + temp-file sweep + exit `130`; (R5) `ENOSPC`/`EROFS` exit `2` not `1`. Auditors (slots 30–39) calling external gateways MUST additionally guard CI invocations on `LOVABLE_API_KEY != ''` per the **Phase 153 Task A5 lesson**.
- **Verifies:** AC-T-03 exit-code contract (extends with `2`-for-environmental-failures discipline); AC-T-04 idempotency (atomic writes are a precondition for second-run-byte-identical); AC-T-12 filler tight-loop safety; AC-T-13 generator determinism (atomic rename prevents torn-read non-determinism); codifies the **Task A9 audit finding** "Incomplete Error/Concurrency Handling — locked files, network timeouts, partial disk writes" with executable rules per kind.

### AC-T-29 — Per-artifact AC delegation contract (Phase 153 Task A9)
- **Given** the §97 file aggregates module-level rules (AC-T-01 … AC-T-29) but delegates per-script logic to slots 01–79,
- **When** any per-artifact spec file (`spec/27-spec-toolchain/NN-*.md` for `NN ∈ [01..79]`) is read,
- **Then** the per-artifact file MUST contain its own `## Acceptance criteria` section with at least one Given/When/Then block AND at least one `**Verifies:**` clause binding the AC to a concrete code path (per AC-09 P3 audit-confidence rubric); the §97 file MUST NOT be the sole home of per-script GWT — slot-internal ACs are the source of truth for per-script verifiability and §97 references them by spec-file link, never by inlining their bodies. This codifies the **Task A9 audit finding** "Missing GWT/Verifies for individual artifacts — module aggregates ACs but delegates per-artifact ACs to 79 separate files which are not provided in this context, leaving the actual tool logic unverified" by making the delegation contract explicit + auditable instead of implicit + invisible-to-context-window-bounded auditors.
- **Verifies:** AC-T-05 per-spec CLI surface; AC-T-06 source-file link; AC-09 P3 Verifies-clause requirement (binds the §97-vs-slot delegation to the audit-confidence rubric); codifies the **Phase 153 Task A9 lesson** "context-window-bounded LLM auditors will systematically under-score modules that delegate ACs to files outside the audited bundle — the spec MUST make the delegation auditable from inside §97 itself, e.g. by enumerating which slots own which AC-T-NN family".

### AC-T-30 — Slot Delegation Map MUST enumerate all per-artifact specs from inside §97 (Phase 153 Task A24-fu6)
- **Given** the §97 file delegates per-script logic to slots 01–79 (AC-T-29) AND a context-window-bounded LLM auditor receives only tier-1 files (`{00,97,98,99}-*.md`) per AC-34-09 walker tiering,
- **When** any auditor (LLM or human reviewer) reads §97 to assess module verification coverage,
- **Then** §97 MUST include a `## Slot Delegation Map` section enumerating EVERY occupied slot in the range 01–79 as a row with five columns: (1) slot number, (2) per-artifact spec link `[NN-name.md](./NN-name.md)`, (3) governing code artifact path (`linter-scripts/<name>` or `.github/workflows/<name>`), (4) AC-family-prefix the slot owns (e.g. `AC-CL`, `AC-FR`, `AC-TH`, `AC-VP`, etc. — or `_(slot-internal AC-NN)_` if the slot uses bare numbering), (5) governing module-level AC from this file (one of `AC-T-01..29`). Empty slot ranges MUST be marked `_(reserved)_`. The map MUST be regenerable from disk truth (`ls spec/27-spec-toolchain/[0-9][0-9]-*.md`) — drift between the map and the filesystem MUST cause `linter-scripts/check-tree-health.cjs --strict` to fail via the existing `INV-01` bijection rule. This codifies the **Phase 153 Task A24-fu6 audit finding** CRITICAL D5 "Missing Per-Artifact Spec Files — module references 79 external spec files which are not provided in the context, AI coder cannot implement the toolchain logic without the individual script specs": the Slot Delegation Map is the canonical fix because it surfaces the delegation universe inside the bundle the auditor sees, mirroring Phase 153 Task A10's `Subfolder Delegation Map` pattern that lifted spec/02 from 80 → ≥91.
- **Verifies:** AC-T-01 bijection (Slot Delegation Map is a denormalised projection of the bijection); AC-T-29 per-artifact AC delegation contract (Map makes the delegation visible); AC-34-09 walker tier-1 contract (Map ensures §97 carries delegation info that survives bundle truncation); codifies **Lesson #19** (audit-boundary < verification-boundary requires in-§97 delegation surface) + **Lesson #21** (Subfolder Delegation Map = canonical fix for parent-§97 audit-boundary blind spots, here applied at slot-granularity instead of subfolder-granularity) + **Lesson #37** (integration-axis modules co-apply Lesson #19 + Lesson #36).

### AC-T-31 — AC-family-prefix binding table for slot-owned GWT (Phase 153 Task A24-fu6)
- **Given** AC-T-30's Slot Delegation Map enumerates all per-artifact slots AND AC-T-29 mandates each slot carries its own GWT,
- **When** an LLM auditor scoring D2 (AC Coverage) sees only the §97 file (per AC-34-09 walker tiering),
- **Then** §97 MUST include an `## AC Family Prefix Index` subsection immediately after the Slot Delegation Map, listing each AC family prefix used across slots 01–79 as one row per prefix with three columns: (a) AC-family-prefix (e.g. `AC-CL`, `AC-TH`, `AC-VP`, `AC-29-*`, `AC-33-*`, `AC-34-*`), (b) owning slot file link, (c) AC count in that family (a positive integer; `0` is FORBIDDEN — empty slots fail AC-T-29). The index MAY be flat (one row per prefix) or grouped by slot range (validators / generators / fillers / auditors / configs / CI). Drift between the index and the actual slot-file AC counts MUST be detected by a `linter-scripts/check-ac-family-index.py` validator (a future tool tracked under Task A24-fu6-followup). This codifies the **Phase 153 Task A24-fu6 audit finding** HIGH D2 "Delegated Acceptance Criteria — AC-T-29 explicitly delegates per-script logic to external files. Without these, the AI has no Given/When/Then criteria for the actual script behaviors": the family-prefix index is the canonical fix because it lets a context-window-bounded auditor count the per-script AC surface without seeing the actual files, raising D2 from "0 visible per-script ACs" to "N family prefixes × M ACs/family = visible verification surface".
- **Verifies:** AC-T-29 per-artifact AC delegation (Index makes the per-script AC count auditable); AC-T-30 Slot Delegation Map (Index is its second-order projection); codifies **Lesson #21** Subfolder Delegation Map pattern for the AC-family axis (vs Map's slot axis); satisfies **Lesson #45** bundle-saturation diagnostic (when 3/50 files used, every byte of §97 must carry maximum delegation-visibility per character).

### AC-T-32 — R2 file-locking retry MUST have a normative code snippet (Phase 153 Task A24-fu6)
- **Given** the `R2 — File locking` rule in [`00-overview.md`](./00-overview.md) requires "single-`read()` call, retry up to 3 times with 100ms back-off on `JSONDecodeError`, exit code `2` on Windows `PermissionError` / POSIX `EAGAIN`",
- **When** any validator in slots 01–09 or 50–59 reads a generated artifact (`spec/spec-index.md`, `spec/dashboard-data.json`, `linter-scripts/trace-map.toml`) that may be mid-rewrite by a concurrent generator,
- **Then** §00's `R2` subsection MUST carry a normative reference-implementation code snippet in BOTH Python and Node (mirroring the R1 atomic-write snippets at lines 205–248 of `00-overview.md`). The Python snippet MUST demonstrate: (1) single `Path.read_bytes()` or `open(...).read()` (NOT chunked reads); (2) try/except on `json.JSONDecodeError` with a 3× retry loop; (3) jittered 100ms ± 25% back-off between retries (mirroring R3's exponential-backoff pattern); (4) `except (PermissionError, OSError) as e: if e.errno in (errno.EAGAIN, errno.EACCES): sys.exit(2)`. The Node snippet MUST demonstrate: (1) single `fs.readFileSync(target)`; (2) try/catch on `SyntaxError` from `JSON.parse()` with the same 3× retry pattern; (3) `if (e.code === 'EBUSY' || e.code === 'EACCES') process.exit(2)`. Slots 01–09/50–59 MAY copy the snippets verbatim (preferred) or implement equivalent retry semantics in their language of choice. This codifies the **Phase 153 Task A24-fu6 audit finding** MEDIUM D3 "Concurrency/Locking Implementation Ambiguity — R2 requires retries on JSONDecodeError to handle 'torn reads', but doesn't specify if this applies to all readers or just specific slots, and lacks a code example for the retry logic": the normative snippet eliminates the ambiguity by binding R2 to executable reference code, mirroring the AC-T-28 R1 closure pattern A13 shipped at v2.74.3.
- **Verifies:** AC-T-28 Resilience contract (R2 sub-rule); AC-T-03 exit-code contract (`2` for environmental failures); codifies the **Phase 153 Task A13 closure pattern** "lift resilience rules from prose-only to prose + normative reference snippets" applied to the R2 axis (A13 closed R1).

### AC-T-33 — R2 read-target scope is a closed ledger (Task S27-02) [medium]
- **Given** AC-T-28's R2 rule + AC-T-32's normative snippet are silent on **which file reads** require the retry loop (the audit-v6 MEDIUM/D3 finding "doesn't explicitly state if *all* scripts must use this for *all* file reads, or only for the specific 'concurrent-write' targets"),
- **When** any script in `linter-scripts/` performs a file `read()`,
- **Then** R2 retry-on-`JSONDecodeError` + lock-error exit-2 semantics are MANDATORY only for reads of artifacts in the **R2 Read-Target Ledger** below; reads of any path NOT in the ledger MAY use a single unguarded `read()` (R2 is opt-in for non-ledger paths and MUST NOT be retrofitted speculatively — speculative retries mask real bugs in single-writer artifacts and inflate CI runtime).

#### R2 Read-Target Ledger (closed enumeration)

| # | Path glob | Why R2 applies | Concurrent writer |
|---|---|---|---|
| RT-01 | `spec/spec-index.md` | Regenerated by `generate-spec-index.cjs` (slot 10) on every CI run; readers in slots 01–09/50–59 may race the writer | `linter-scripts/generate-spec-index.cjs` |
| RT-02 | `spec/dashboard-data.json` | Regenerated by `generate-dashboard-data.cjs` (slot 11); JSON parse failures during torn writes are the documented P44/P45 root-cause class | `linter-scripts/generate-dashboard-data.cjs` |
| RT-03 | `linter-scripts/trace-map.toml` | Regenerated by `generate-trace-map.py` (slot 12); TOML parse failures surface as opaque "expected ']' got EOF" without R2 | `linter-scripts/generate-trace-map.py` |
| RT-04 | `.lovable/cache/audit-ai/*.json` | Rewritten by `audit-ai-implementability.py` (slot 34) per-module under SHA-keyed cache; concurrent reader in CI summary step may catch mid-rewrite | `linter-scripts/audit-ai-implementability.py` |
| RT-05 | `~/.local/state/<binary-name>/update.lock` | PID-file discipline per spec/13 AC-22 concurrency contract; cross-process lock contention is the entire point of the file | downstream CLI binary (per spec/13 §10) |

Any future generator that writes an artifact consumed by a sibling validator MUST add a row to this ledger in the SAME PR (lockstep budget: §97 patch + new row, no new AC). Drift between the ledger and the actual `extractWriters()` output of `check-tree-health.cjs --strict` is caught in the next H-series rebaseline.

#### Forbidden patterns
- ❌ Wrapping every `read_text()` in the codebase with R2 retry (inflates CI runtime, masks single-writer bugs).
- ❌ Silently extending the ledger via prose-only mention in a §98 row — the table is the normative surface.
- ❌ Using R2 retry on **read-only fixtures** under `linter-scripts/test/fixtures/` (those are committed, never rewritten — a `JSONDecodeError` there is a real bug, not a torn read).

- **Verifies:** AC-T-28 R2 (scope binding); AC-T-32 R2 normative snippet (binding-target enumeration); codifies the **Lesson #22** "Open exception phrases in normative ACs MUST be replaced with closed Exception Ledger" pattern applied to the R2 read-target axis (the ledger IS the normative surface, mirroring AC-CG-22 EX-01..EX-08 in spec/02).

### AC-T-34 — Audit "AC-11-05 truncated" finding is a walker-cap artifact, NOT a contract gap (Task S27-01) [high]
- **Given** the AI-implementability auditor (slot 34 `audit-ai-implementability.py`) bundles spec/27 at the 140 KB walker cap (AC-34-14) and reports `files_used: 15/57` against this module — meaning ~42 of 57 sub-files (including most of `11-generate-dashboard-data.md` past the bundle horizon) are NEVER in the auditor's visible context window,
- **When** the auditor surfaces a HIGH/D4 finding such as "AC-11-05 ends mid-sentence due to the 136KB cap, leaving the Verifies clause and final logic for inline-code blanking undefined" (audit-v6 cache `.lovable/cache/audit-ai/27-spec-toolchain.json`),
- **Then** the finding MUST be classified as an **auditor walker-cap artifact, NOT a contract gap**, because: (a) `spec/27-spec-toolchain/11-generate-dashboard-data.md` is **107 lines / on-disk-complete** as of 2026-05-03 (`wc -l` confirms); (b) AC-11-05 lives at lines 83–89, ends with a complete `**Verifies:**` block citing three sources (`generate-dashboard-data.cjs:137-176` + `check-spec-cross-links.py:57-66` + `test-inline-code-blanking-parity.sh`); (c) the file's `## Cross-references` + `## Changelog` sections (lines 90–107) close cleanly. The "mid-sentence" appearance is the auditor's bundle horizon falling inside the AC body — fixing it requires either a walker re-tier (out of scope for spec/27 self-lift; tracked under spec/27 §00 R3) OR an explicit auditor-misreading pin (this AC). This codifies **Lesson #11** "audits MUST walk the full sub-tree" + **Lesson #16** "tier contract files first" + **Lesson #29** "module-kind / auditor-misreading pin in §97 is the canonical fix when the audit-corpus surface is misread by a context-window-bounded LLM" — applied here at the **truncation-as-evidence axis** (vs Lesson #29's quoted-evidence-as-evidence axis in spec/25). Future contributors who see "AC-NN-NN ends mid-sentence" findings against ANY spec/27 slot file MUST first run `wc -l spec/27-spec-toolchain/<NN>-*.md` + `tail -10` + grep for the AC-ID end-marker on disk; if the file is on-disk-complete, the finding is walker-cap noise and resolves under this AC's classification rule, NOT under a content edit.
- **AND** the canonical evidence-bundle for any walker-cap dispute is the triple `(wc -l, tail -10, grep "Verifies:" or last-line-of-AC)` against the cited slot file — these three commands constitute the "on-disk completeness" verification surface; if all three pass, the AC stands and the finding closes under AC-T-34.
- **Verifies:** `spec/27-spec-toolchain/11-generate-dashboard-data.md` lines 83–89 (AC-11-05 on-disk-complete with 3-source `**Verifies:**` block); `spec/27-spec-toolchain/11-generate-dashboard-data.md:107` (file end-of-content); slot 34 AC-34-14 (140 KB walker cap declaration); slot 34 `audit-ai-implementability.py` `files_used` field in cache JSON (proves 42/57 sub-files never bundled); codifies **Lesson #11 + #16 + #29 + #37** at the truncation-as-evidence axis; mirrors AC-AI-09/10/11 in spec/25 (audit-corpus pin pattern from L29-codify).

### AC-T-35 — Slot 35 `audit-bundle-budget.py` is the deterministic walker-cap regression gate (Phase J9) [critical]
- **Given** slot 34 `audit-ai-implementability.py` enforces the 140 KB walker cap (AC-34-14) and slot 35 `audit-bundle-budget.py` (`spec/27-spec-toolchain/35-audit-bundle-budget.md`, kind: auditor) classifies every top-level `spec/NN-*/` module into `{UNDER, NEAR, OVER}` against that cap with self-test `linter-scripts/test/test-audit-bundle-budget.sh` (10 assertions),
- **When** any spec edit, content lift, or sibling-file addition risks pushing a module past the 140 KB tier-1 bundle horizon (mechanical regression class identified by Phase 153 Task A24-fu27 → Lesson #65 "structural surgery > pure-promotion"),
- **Then** slot 35's CLI surface (`audit-bundle-budget.py [--json] [--report PATH] [--strict]`) MUST be the single source of truth for OVER-class detection: (a) AC-35-01 binds the cap to slot 34's `MAX_BYTES` constant (NOT a duplicated literal — Lesson #36 link-don't-restate); (b) AC-35-02 makes classification deterministic + zero-network; (c) AC-35-03 makes `--strict` the graduating CI gate after the OVER class hits 0; (d) AC-35-04 keeps default mode advisory until graduation; (e) AC-35-05 mechanically locks the script under `test-audit-bundle-budget.sh` (10 assertions) per Lesson #31 snapshot-restore + Lesson L21 mechanical-lock parity-AC rule.
- **AND** the slot 35 spec file (`35-audit-bundle-budget.md`) MUST stay bound from §27 §97 via THREE surfaces in lockstep: (1) Slot Delegation Map row in the Auditors (30–39) band; (2) AC Family Prefix Index row binding `AC-35-*` family to ≥5 GWT minimum; (3) trace-map entries (`linter-scripts/trace-map.toml`) covering each AC-35-NN to `linter-scripts/audit-bundle-budget.py`. Drift between any of these three surfaces and disk truth fails `check-tree-health.cjs --strict` (AC-T-30) + `check-trace-map.py` (AC-T-17) respectively.
- **Forbidden patterns:** (a) restating the 140 KB cap literal in `35-audit-bundle-budget.md` instead of binding to slot 34's `MAX_BYTES` (dual-source drift class per Lesson #36); (b) declaring slot 35 in the delegation map without a matching trace-map entry (audit-boundary < verification-boundary class per Lesson #19); (c) graduating `--strict` to CI without first verifying the OVER class is empty (per AC-35-03 sequencing); (d) renaming or relocating slot 35 — slots are immutable per AC-T-07.
- **Verifies:** `spec/27-spec-toolchain/35-audit-bundle-budget.md` (slot file present, 90 lines, 5 ACs); `linter-scripts/audit-bundle-budget.py` (productionised from `/tmp/a24-fu27-bundle-budget.py` per Phase 153 Task A24-fu32); `linter-scripts/test/test-audit-bundle-budget.sh` (10 assertions, snapshot-restore-safe); slot 34 AC-34-14 (140 KB cap source); Slot Delegation Map row 35 + AC Family Prefix Index `AC-35-*` row (this §97); trace-map entries (`linter-scripts/trace-map.toml` `[[trace]]` blocks for AC-35-01..05). Codifies **Lesson #19** (audit-boundary < verification-boundary closure for slot 35) + **Lesson #21/#39** (intra-module sibling delegation, second-axis instance after spec/22 AC-80 and spec/14 AC-23) + **Lesson #36** (link-don't-restate for the cap literal) + **Lesson #65** (structural-surgery > pure-promotion regression-protection).

---

## Slot Delegation Map (Phase 153 Task A24-fu6)

The following map enumerates every occupied slot in the range 01–79 with its governing per-artifact spec, code artifact, slot-internal AC family, and module-level governing AC. Empty rows in a range are marked `_(reserved)_`. Drift between this map and disk truth (`ls spec/27-spec-toolchain/[0-9][0-9]-*.md`) is caught by `linter-scripts/check-tree-health.cjs --strict` per AC-T-30.

### Validators (01–09)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 01 | [01-check-spec-cross-links.md](./01-check-spec-cross-links.md) | `linter-scripts/check-spec-cross-links.py` | `AC-CL-*` | AC-T-03, AC-T-15 (↔ §61 allowlist) |
| 02 | [02-check-spec-folder-refs.md](./02-check-spec-folder-refs.md) | `linter-scripts/check-spec-folder-refs.py` | `AC-FR-*` (incl. AC-62-01..04) | AC-T-03, AC-T-15 (↔ §62 allowlist) |
| 03 | [03-check-forbidden-strings.md](./03-check-forbidden-strings.md) | `linter-scripts/check-forbidden-strings.py` | `AC-FS-*` | AC-T-03, AC-T-15 (↔ §60 TOML config) |
| 04 | [04-check-forbidden-spec-paths.md](./04-check-forbidden-spec-paths.md) | `linter-scripts/check-forbidden-spec-paths.sh` | `AC-FSP-*` | AC-T-03 |
| 05 | [05-check-tree-health.md](./05-check-tree-health.md) | `linter-scripts/check-tree-health.cjs` | `AC-TH-*` | AC-T-01, AC-T-03, AC-T-22, AC-T-23, AC-T-24, AC-T-27 |
| 06 | [06-check-root-readme.md](./06-check-root-readme.md) | `linter-scripts/check-root-readme.py` | `AC-RR-*` | AC-T-03 |
| 07 | [07-check-readme-canonicals.md](./07-check-readme-canonicals.md) | `linter-scripts/check-readme-canonicals.py` | `AC-RC-*` | AC-T-03 |
| 08 | [08-check-readme-install-section.md](./08-check-readme-install-section.md) | `linter-scripts/check-readme-install-section.py` | `AC-RI-*` | AC-T-03 |
| 09 | [09-check-memory-mirror-drift.md](./09-check-memory-mirror-drift.md) | `linter-scripts/check-memory-mirror-drift.py` | `AC-MM-*` | AC-T-03 |

### Generators (10–19)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 10 | [10-generate-spec-index.md](./10-generate-spec-index.md) | `linter-scripts/generate-spec-index.cjs` | `AC-SI-*` | AC-T-13, AC-T-25 (drift gate) |
| 11 | [11-generate-dashboard-data.md](./11-generate-dashboard-data.md) | `linter-scripts/generate-dashboard-data.cjs` | `AC-DD-*` | AC-T-13, AC-T-14 (consumer of JSON output) |
| 12 | [12-suggest-spec-cross-link-fixes.md](./12-suggest-spec-cross-link-fixes.md) | `linter-scripts/suggest-spec-cross-link-fixes.py` | `AC-SCLF-*` | AC-T-13 |
| 13 | [13-generate-gwt-acceptance.md](./13-generate-gwt-acceptance.md) | `linter-scripts/generate-gwt-acceptance.py` | `AC-GG-*` | AC-T-13 |
| 14 | [14-generate-trace-map.md](./14-generate-trace-map.md) | `linter-scripts/generate-trace-map.py` | `AC-GTM-*` | AC-T-17, AC-T-20 |
| 15 | [15-generate-fix-checklist.md](./15-generate-fix-checklist.md) | `linter-scripts/generate-fix-checklist.py` | `AC-GFC-*` | AC-T-13 |
| 16 | [16-generate-gate-report.md](./16-generate-gate-report.md) | `linter-scripts/generate-gate-report.py` | `AC-GGR-*` | AC-T-13 |
| 17 | [17-check-trace-map-regression.md](./17-check-trace-map-regression.md) | `linter-scripts/check-trace-map-regression.py` | `AC-TMR-*` | AC-T-17 (regression gate) |
| 18 | [18-check-mermaid-syntax.md](./18-check-mermaid-syntax.md) | `linter-scripts/check-mermaid-syntax.mjs` | `AC-CMS-*` | AC-T-22 (slot-range exception ledgered) |
| 19 | [19-check-memo-retrospective-headings.md](./19-check-memo-retrospective-headings.md) | `linter-scripts/check-memo-retrospective-headings.py` | `AC-CMR-*` | AC-T-23 (slot-range exception ledgered) |

### Fillers (20–29)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 20 | [20-fill-missing-acceptance-criteria.md](./20-fill-missing-acceptance-criteria.md) | `linter-scripts/fill-missing-acceptance-criteria.cjs` | `AC-FAC-*` | AC-T-04, AC-T-12 |
| 21 | [21-fill-missing-changelogs.md](./21-fill-missing-changelogs.md) | `linter-scripts/fill-missing-changelogs.cjs` | `AC-FCL-*` | AC-T-04, AC-T-12 |
| 22 | [22-fill-missing-consistency-reports.md](./22-fill-missing-consistency-reports.md) | `linter-scripts/fill-missing-consistency-reports.cjs` | `AC-FCR-*` | AC-T-04, AC-T-12 |
| 23 | [23-scaffold-spec-module.md](./23-scaffold-spec-module.md) | `linter-scripts/scaffold-spec-module.cjs` | `AC-SSM-*` | AC-T-04 |
| 24 | [24-check-lockstep.md](./24-check-lockstep.md) | `linter-scripts/check-lockstep.cjs` | `AC-LS-*` | AC-T-03 |
| 25 | [25-deepen-consistency-reports.md](./25-deepen-consistency-reports.md) | `linter-scripts/deepen-consistency-reports.py` | `AC-DCR-*` | AC-T-24 |
| 26 | [26-check-99-summary-freshness.md](./26-check-99-summary-freshness.md) | `linter-scripts/check-99-summary-freshness.py` | `AC-SF-*` | AC-T-03 |
| 27 | [27-check-99-stamp-bump.md](./27-check-99-stamp-bump.md) | `linter-scripts/check-99-stamp-bump.py` | `AC-SB-*` | AC-T-03 |
| 28 | [28-check-archive-exclusion-runtime.md](./28-check-archive-exclusion-runtime.md) | `linter-scripts/check-archive-exclusion-runtime.py` | `AC-AER-*` | AC-T-03 |
| 29 | [29-check-version-parity.md](./29-check-version-parity.md) | `linter-scripts/check-version-parity.py` | `AC-29-*` (incl. AC-29-15) | AC-T-26 |

### Auditors (30–39)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 30 | [30-audit-spec-vs-code.md](./30-audit-spec-vs-code.md) | `linter-scripts/audit-spec-vs-code.py` | `AC-ASC-*` | AC-T-14 (JSON output) |
| 31 | [31-audit-spec-vs-code-v2.md](./31-audit-spec-vs-code-v2.md) | `linter-scripts/audit-spec-vs-code-v2.py` | `AC-31-*` (incl. AC-31-31) | AC-T-14, AC-T-25, AC-T-26 |
| 32 | [32-check-truncated-prose.md](./32-check-truncated-prose.md) | `linter-scripts/check-truncated-prose.py` | `AC-CTP-*` | AC-T-03 |
| 33 | [33-check-ai-confidence.md](./33-check-ai-confidence.md) | `linter-scripts/check-ai-confidence.py` | `AC-33-*` (incl. AC-33-08..12) | AC-T-14 |
| 34 | [34-audit-ai-implementability.md](./34-audit-ai-implementability.md) | `linter-scripts/audit-ai-implementability.py` | `AC-34-*` (incl. AC-34-09/10/11/12/13/14) | AC-T-14, AC-T-28 (R3 LLM timeouts) |
| 35 | [35-audit-bundle-budget.md](./35-audit-bundle-budget.md) | `linter-scripts/audit-bundle-budget.py` | `AC-35-*` (incl. AC-35-01..05) | AC-T-14, AC-T-30 (slot-cap walker) |
| 36–39 | _(reserved)_ | _(reserved)_ | _(reserved)_ | _(reserved)_ |


### Runners (40–49)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 40 | [40-run-sh.md](./40-run-sh.md) | `linter-scripts/run.sh` | `AC-RUN-*` | AC-T-16, AC-T-28 (R4 signal handling) |
| 41 | [41-run-ps1.md](./41-run-ps1.md) | `linter-scripts/run.ps1` | `AC-RUN-*` | AC-T-16, AC-T-28 (R4 signal handling) |
| 42–49 | _(reserved)_ | _(reserved)_ | _(reserved)_ | _(reserved)_ |

### Source validators (50–59)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 50 | [50-validate-guidelines-py.md](./50-validate-guidelines-py.md) | `linter-scripts/validate-guidelines.py` | `AC-VG-*` | AC-T-03, AC-T-18 (twin) |
| 51 | [51-validate-guidelines-go.md](./51-validate-guidelines-go.md) | `linter-scripts/validate-guidelines.go` | `AC-VG-*` | AC-T-03, AC-T-18 (twin) |
| 52 | [52-check-axios-version.md](./52-check-axios-version.md) | `linter-scripts/check-axios-version.py` | `AC-CAV-*` | AC-T-03 |
| 53–59 | _(reserved)_ | _(reserved)_ | _(reserved)_ | _(reserved)_ |

### Configuration (60–69)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 60 | [60-forbidden-strings-toml.md](./60-forbidden-strings-toml.md) | `linter-scripts/forbidden-strings.toml` | `AC-FST-*` | AC-T-15 (consumed by §03) |
| 61 | [61-spec-cross-links-allowlist.md](./61-spec-cross-links-allowlist.md) | `linter-scripts/spec-cross-links.allowlist` | `AC-SCLA-*` | AC-T-15 (consumed by §01) |
| 62 | [62-spec-folder-refs-allowlist.md](./62-spec-folder-refs-allowlist.md) | `linter-scripts/spec-folder-refs.allowlist` | `AC-62-*` (incl. AC-62-01..04) | AC-T-15 (consumed by §02) |
| 63 | [63-readme-cross-links-md.md](./63-readme-cross-links-md.md) | `linter-scripts/readme-cross-links.md` | `AC-RCL-*` | AC-T-15 |
| 64–69 | _(reserved)_ | _(reserved)_ | _(reserved)_ | _(reserved)_ |

### CI workflows (70–79)

| # | Spec | Code | Slot AC family | Module-level governing AC |
|---|------|------|----------------|----------------------------|
| 70 | [70-spec-health-yml.md](./70-spec-health-yml.md) | `.github/workflows/spec-health.yml` | `AC-SH-*` | AC-T-08, AC-T-19 |
| 71 | [71-spec-monthly-audit-yml.md](./71-spec-monthly-audit-yml.md) | `.github/workflows/spec-monthly-audit.yml` | `AC-SMA-*` | AC-T-19 |
| 72–79 | _(reserved)_ | _(reserved)_ | _(reserved)_ | _(reserved)_ |

---

## AC Family Prefix Index (Phase 153 Task A24-fu6)

Per AC-T-31, this index lets a context-window-bounded auditor count the per-script AC verification surface without reading the 50+ slot files. Each row binds an AC-family prefix to its owning slot file. Counts are AC-T-29-mandated minimums (every slot MUST carry ≥1 GWT); actual counts may be higher and are tracked inside each slot file's `## Acceptance criteria` section.

| AC family prefix | Owning slot | Min AC count |
|------------------|-------------|--------------|
| AC-CL-* | [01-check-spec-cross-links.md](./01-check-spec-cross-links.md) | ≥1 |
| AC-FR-*, AC-62-01..04 | [02-check-spec-folder-refs.md](./02-check-spec-folder-refs.md) + [62-spec-folder-refs-allowlist.md](./62-spec-folder-refs-allowlist.md) | ≥4 |
| AC-FS-* | [03-check-forbidden-strings.md](./03-check-forbidden-strings.md) | ≥1 |
| AC-FSP-* | [04-check-forbidden-spec-paths.md](./04-check-forbidden-spec-paths.md) | ≥1 |
| AC-TH-* | [05-check-tree-health.md](./05-check-tree-health.md) | ≥1 |
| AC-RR-*, AC-RC-*, AC-RI-* | [06-08-readme-*.md](./06-check-root-readme.md) | ≥3 |
| AC-MM-* | [09-check-memory-mirror-drift.md](./09-check-memory-mirror-drift.md) | ≥1 |
| AC-SI-*, AC-DD-* | [10-11-generate-*.md](./10-generate-spec-index.md) | ≥2 |
| AC-GTM-*, AC-TMR-* | [14-17-trace-map-*.md](./14-generate-trace-map.md) | ≥2 |
| AC-FAC-*, AC-FCL-*, AC-FCR-*, AC-SSM-* | [20-23-fill-*.md](./20-fill-missing-acceptance-criteria.md) | ≥4 |
| AC-LS-* | [24-check-lockstep.md](./24-check-lockstep.md) | ≥1 |
| AC-DCR-* | [25-deepen-consistency-reports.md](./25-deepen-consistency-reports.md) | ≥1 |
| AC-SF-*, AC-SB-* | [26-27-check-99-*.md](./26-check-99-summary-freshness.md) | ≥2 |
| AC-AER-* | [28-check-archive-exclusion-runtime.md](./28-check-archive-exclusion-runtime.md) | ≥1 |
| AC-29-* (incl. AC-29-15) | [29-check-version-parity.md](./29-check-version-parity.md) | ≥15 |
| AC-31-* (incl. AC-31-31) | [31-audit-spec-vs-code-v2.md](./31-audit-spec-vs-code-v2.md) | ≥31 |
| AC-33-* (incl. AC-33-08..12) | [33-check-ai-confidence.md](./33-check-ai-confidence.md) | ≥12 |
| AC-34-* (incl. AC-34-09..14) | [34-audit-ai-implementability.md](./34-audit-ai-implementability.md) | ≥14 |
| AC-35-* (incl. AC-35-01..05) | [35-audit-bundle-budget.md](./35-audit-bundle-budget.md) | ≥5 |
| AC-RUN-* | [40-run-sh.md](./40-run-sh.md) + [41-run-ps1.md](./41-run-ps1.md) | ≥2 |
| AC-VG-* (twin) | [50-validate-guidelines-py.md](./50-validate-guidelines-py.md) + [51-validate-guidelines-go.md](./51-validate-guidelines-go.md) | ≥2 |
| AC-60-*, AC-SCLA-*, AC-RCL-* | [60-forbidden-strings-toml.md](./60-forbidden-strings-toml.md), [61-spec-cross-links-allowlist.md](./61-spec-cross-links-allowlist.md), [63-readme-cross-links-md.md](./63-readme-cross-links-md.md) | ≥3 |
| AC-SH-*, AC-SMA-* | [70-spec-health-yml.md](./70-spec-health-yml.md) + [71-spec-monthly-audit-yml.md](./71-spec-monthly-audit-yml.md) | ≥2 |

**Total minimum verification surface from delegated slots: ≥100 GWT criteria** across 36 occupied slots — orthogonal to and NOT double-counted with the 32 module-level AC-T-* + AC-29/31/33/34 criteria above.

---

## Per-artifact criteria

Per-script acceptance criteria live inside each per-artifact spec file (slots 01–79) under their own "Acceptance criteria" section. The §97 file aggregates only module-level rules.

---

## Validation

```bash
bash linter-scripts/run.sh                          # full pipeline
node linter-scripts/check-tree-health.cjs --min=80  # gate
python3 linter-scripts/check-spec-cross-links.py    # link check
```

All commands MUST exit `0` for this module's acceptance to hold.

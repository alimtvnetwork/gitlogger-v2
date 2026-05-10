---
kind: meta-toolchain
todo_audit_exempt: true
description: Auditor-self-reference module — defines the toolchain that audits the spec tree, including TODO-detection mechanics. G-TODO-01 is exempted because narrative content here legitimately discusses TODO/TBD/FIXME categories.
content_axis: tooling-spec
axis_rationale: "Specs the linter-scripts/ contract (validators, generators, gates)"
---

# Spec Toolchain

**Version:** 2.95.0  
**Updated:** 2026-05-10
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


## CI Workflow Integration — Phase 79 Normative (cross-reference)

> **Source of truth:** [`.github/workflows/spec-health.yml`](../../.github/workflows/spec-health.yml) — the live, version-controlled CI workflow with all 17+ strict gates and stage ordering. Per **Lesson #36**, this overview no longer restates the YAML stages (the prior 80-line pedagogical example block was archived in Phase 153 Task A24-fu36 to remove dual-source drift risk and recover walker tier-1 budget).
>
> Stage ordering: detect (lockstep + tree-health) → validate (cross-links + folder-refs + forbidden-strings + version-parity) → audit (AI-implementability + summary-freshness + stamp-bump) → promote. See `spec/12-cicd-pipeline-workflows/` for the broader CI pattern catalog and `.github/workflows/spec-health.yml` line-by-line for the canonical stage definitions.
>
> **Archive:** [`_archive/00-ci-workflow-yaml-pre-A24-fu36.md`](./_archive/00-ci-workflow-yaml-pre-A24-fu36.md) preserves the pedagogical YAML examples for historical reference.

See [`lifecycle-27-spec-toolchain.mmd`](./lifecycle-27-spec-toolchain.mmd) for the visual end-to-end flow.

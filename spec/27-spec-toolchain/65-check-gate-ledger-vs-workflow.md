# Slot 65 — `check-gate-ledger-vs-workflow.py`

**Status:** Active gate #43 (Phase-5 T-40 / P19a)
**Source:** [`linter-scripts/check-gate-ledger-vs-workflow.py`](../../linter-scripts/check-gate-ledger-vs-workflow.py)
**Self-test:** built-in (`--self-test`) — 6 in-memory fixtures (F-1 clean / F-2 phantom-cite / F-3 unwired / F-4 duplicate-numbers / F-5 small-gap-ok / F-6 happy-multi)
**Workflow step:** `.github/workflows/spec-health.yml` "Gate-ledger ↔ workflow drift check (Phase-5 T-40 / P19a)"
**Wired-mode:** **warn-only** (until P19b..P19e ship the missing scripts; then the `|| true` MUST be removed and this becomes a hard gate)

---

## Purpose

Closes the **phantom-gate epidemic** identified by the Sess-65 reality-check audit (Findings **F-1** and **F-2**):

- **F-1**: §27 slot docs cite **80** distinct linter scripts as "Mechanically enforced by …"; only **42** exist on disk. **38 are phantoms**.
- **F-2**: 22 slot docs carry `**Status:** Active gate #N` markers; many of those scripts are NOT wired into `.github/workflows/spec-health.yml` — the contract claims CI enforcement that does not happen.

This gate makes both lies impossible to add and impossible to keep. It is **reflexive**: it checks itself (slot 65 + this very doc + its own workflow step would all be subject to the same three invariants).

This gate is the precondition for the Rubric v2 18-20 band rule (per `mem://preferences/scorecard-ritual` and core memory) to be **honest**: a score of 20 REQUIRES citing a self-enforcing mechanism, and now "self-enforcing" is mechanically defined as "exists on disk AND wired to CI workflow".

---

## Contract — three invariants

| ID  | Name      | Rule                                                                                               | Exit |
|-----|-----------|----------------------------------------------------------------------------------------------------|------|
| I-1 | EXISTS    | Every `linter-scripts/<name>` cited by any `spec/27-spec-toolchain/NN-*.md` MUST exist on disk.    | 1    |
| I-2 | WIRED     | Every slot doc with `**Status:** Active gate #N` MUST have its companion script referenced in `.github/workflows/spec-health.yml`. | 2    |
| I-3 | NUMBERED  | Active gate numbers MUST be unique; gaps >5 across the contiguous range are a failure.             | 3    |

Citation discovery regex: `linter-scripts/([a-z0-9_.-]+\.(?:py|sh|cjs|mjs|js))` (matches both fenced `Source:` rows and inline prose).

Companion-script resolution: prefer `**Source:** [`linter-scripts/<X>`]` line; fall back to filename convention `NN-<stem>.md → linter-scripts/<stem>.{py,sh,cjs,mjs}`.

Carve-outs: none. Reflexively, this very file is subject to I-1/I-2/I-3 — the script `check-gate-ledger-vs-workflow.py` exists, is wired (warn-only), and gate #43 is unique.

---

## Exit-code contract

Exit codes: `0` pass · `1` violation (I-1 EXISTS — phantom script cited) · `2` invocation error (also: I-2 WIRED — active gate not in workflow) · `3` fixture-rot (also: I-3 NUMBERED — duplicate or large gap in gate numbers) · `99` FATAL — `spec/27-spec-toolchain/` or workflow file not found.

| Exit | Meaning                                                              |
|------|----------------------------------------------------------------------|
| `0`  | pass — all three invariants hold.                                    |
| `1`  | violation — I-1 EXISTS failure (phantom script cited).               |
| `2`  | invocation error — I-2 WIRED failure (active gate not in workflow).  |
| `3`  | fixture-rot — I-3 NUMBERED failure (duplicate or large gap in gate numbers) OR self-test fixture corpus drift. |
| `99` | FATAL — `spec/27-spec-toolchain/` or workflow file not found.        |

When multiple invariants fail simultaneously, the script surfaces the most-severe (lowest-numbered) failing exit code.

## R5 — vacuously-passing scanner is auto-fail

A run that finds zero slot docs, zero citations, or an empty workflow file is **itself a violation** (`vacuous-pass: empty corpus → exit 3 fixture-rot`). The `--self-test` mode is mandatory in CI: it asserts the scanner REJECTS six synthetic fixtures rather than silently passing on absence.

---

## Self-test fixtures (6)

| ID       | Name                | Setup                                                              | Expected exit |
|----------|---------------------|--------------------------------------------------------------------|---------------|
| **F-1**  | clean               | 1 active gate, script exists, wired                                | 0             |
| **F-2**  | phantom-cite        | Slot doc references a script that doesn't exist                    | 1             |
| **F-3**  | unwired             | Active gate marker present; script exists; NOT in workflow         | 2             |
| **F-4**  | duplicate-numbers   | Two slot docs both claim `Active gate #1`                          | 3             |
| **F-5**  | small-gap-ok        | Gate #1 + Gate #3 (gap of 1) — passes                              | 0             |
| **F-6**  | happy-multi         | 2 active gates, both scripts exist, both wired                     | 0             |

Self-test runs in-memory using `tempfile.TemporaryDirectory()`; no disk mutation outside `/tmp`.

---

## Current real-disk state (Sess-65 baseline — what this gate reports)

```
scanned 75 slot docs, 80 unique script citations, 22 active gates, 43 scripts on disk
Exit code 1 (38 failures) — 38 phantom-script citations
```

This is the **exact list** P19b..P19e will ship scripts for, in priority order:
- P19b: `check-no-sql-ddl-in-ui-folder.py` (gate #36, AC-ADS-17 enforcer)
- P19c: `check-ci-cli-self-test-harness.py` (gate #40, AC-28-49 enforcer)
- P19d: `meta-verify-lockstep.py` (gate #42, §27 reflexivity claim)
- P19e: `check-no-out-of-scope-spec-folder-link.py` (gate #39, scope-lock perimeter)

Once these four ship, phantom count drops from 38 → 34, and the four highest-profile Rubric v2 score-20 promotions become honest. Removing all 38 phantoms requires the full P19b..P19z sweep.

---

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-65/`) and run `python3 linter-scripts/check-gate-ledger-vs-workflow.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #43 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-gate-ledger-vs-workflow.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #43 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Self-enforcing mechanism (Rubric v2 18-20 band requirement)

`linter-scripts/check-gate-ledger-vs-workflow.py` (this slot, gate #43, all 3 invariants I-1/I-2/I-3); built-in `--self-test` runs the 6-fixture corpus above. Workflow step: `.github/workflows/spec-health.yml` "Gate-ledger ↔ workflow drift check (Phase-5 T-40 / P19a)" (warn-only mode active until phantom backlog cleared).

Self-enforcing via §27 backlog gate `gate-ledger-vs-workflow-check` (this slot — reflexive).

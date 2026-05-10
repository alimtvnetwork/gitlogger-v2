## Goal

Lift the 7 in-scope modules (mean **92.0/100**) to a state where any AI can build the application blindly from the spec — i.e. every dimension ≥ **19/20** and zero open issues.

The audit measures 5 dimensions (each /20):

| Dim | What it measures | What "100%" looks like |
|---|---|---|
| **D1 Contract clarity** | One unambiguous source of truth per fact | Every type/enum/DDL/JSON-schema has exactly one canonical home; no dialect or unit ambiguity |
| **D2 AC coverage** | §97 GWT ACs cover every normative claim | Every prose rule has a `**Verifies:**` AC; no underclaim banners |
| **D3 Edge & error** | All failure modes enumerated | Closed-set outcome enums; explicit timeouts/retries/concurrency rules; no "should handle errors" handwaving |
| **D4 Examples** | Runnable, copy-pasteable artifacts | Every contract has an example payload, every flow has a worked transcript |
| **D5 Cross-refs** | External pointers resolve in-tree | Every link/citation lands inside a canonical AC slot; no dangling external dep |

## Current state (from cache)

```text
Module                            Tot   D1   D2   D3   D4   D5  Open issues
22-git-logs-v2                     76   18   14   16   12   16   0  (cache pre-AC-80)
23-app-database                    97   19   20   18   20   20   3
24-app-design-system-and-ui        95   20   20   18   20   15   3
25-app-issues                      93   18   19   17   20   18   3
26-gitlogs-diagrams                94   20   20   18   19   15   3
27-spec-toolchain                  92   18   19   18   17   20   0
28-universal-ci-cli                97   20   20   18   19   20   3
```

Two distinct workloads: **spec/22 self-lift** (single big push, +24 expected) and **15 specific issues** spread across the other 6 modules (most are 1-AC fixes).

---

## Phase plan

Sequenced largest-leverage first. Each phase is independently shippable; lockstep budget noted per phase.

### Phase 1 — spec/22 self-lift (76 → ≥92), ~3 sub-phases

**Why first:** lifts tree mean from 92.0 → 95.4 alone.

Cache D2=14, D4=12, D1=18 — three weakest dims:

- **1a (D4 Examples, +6 expected):** Add worked transcripts to the 11 "governed-but-unnamed" sibling files identified in AC-80; each gets a `## Example` block (sample request, sample response, sample DB row). Lockstep: §97 patch + §00/§98/§99 patch.
- **1b (D2 AC coverage, +5 expected):** Walk the §97 AC index against `01-foundation/*` and `02-features/*` prose; every normative paragraph without a `**Verifies:**` link gets an AC stub. Lockstep: §97 minor + §00/§98/§99 patch.
- **1c (D1 Contract clarity, +2 expected):** Promote inline DDL fragments scattered across §10–§13 into a single `10-database/00-schema.sql` canonical file; everywhere else `link, never restate` (Lesson #36). Lockstep: §97 patch + §00/§98/§99 patch.

### Phase 2 — spec/26 D5 + D4 (94 → 99)

- **2a:** "Missing Authoritative Source (spec/22)" — every `.mmd` diagram cites the §22 AC it visualises in front-matter `verifies:` field. Add JSON-schema for diagram metadata.
- **2b:** Inline `.mmd` source content into the spec body (currently file-only); ensures auditor walker sees it.
- **2c:** Replace `xmllint` external dep with a vendored Node check (or document the Lesson #36 cross-ref to §27).

### Phase 3 — spec/24 D5 + D3 (95 → 99)

- **3a:** "External Dependency §07 Missing" — §07 is out-of-scope per scope lock; add an in-§24 "Design Token Contract" section that fully self-contains the tokens needed (no §07 dependency). This converts a cross-ref into a local contract.
- **3b:** "Missing linter-scripts" — bind the design-system-related linters to canonical §27 slots (Lesson #36 link, never restate).
- **3c:** Sidebar State Concurrency — add closed-state enum `{COLLAPSED, EXPANDED, PINNED, FLOATING}` + transition table.

### Phase 4 — spec/25 D5 + D3 + D1 (93 → 98)

- **4a:** "Truncated context" — apply Lesson #11 walker tier-1 fix locally (already shipped in audit harness; this phase verifies it lands per-file).
- **4b:** "Inconsistent Severity Enums" — pick one severity enum (suggest `{BLOCKING, CRITICAL, HIGH, MEDIUM, LOW, INFO}`) and pin in §97 as canonical AC; both child trackers link.
- **4c:** "Ambiguous 'Phase 153'" references — convert every bare `Phase 153` to `Phase 153 Task X` with link.

### Phase 5 — spec/28 D3 + D4 (97 → 99)

- **5a:** "Parallel runtime failures" — add a closed outcome enum + state machine for parallel-step failures (mirrors spec/13 AC-22 concurrency pattern).
- **5b:** "SSH signature generation example" — add a worked `ssh-keygen -Y sign` transcript with sample stdin/stdout.
- **5c:** "Log shipping timeout" — add explicit `TIMEOUT_MS=30000` constant + retry policy (mirror spec/27 AC-T-28 R3).

### Phase 6 — spec/23 D3 + D1 (97 → 99)

- **6a:** "Conflicting DDL Dialects" — declare canonical engine (suggest SQLite per Core memory) at §00; every other dialect block is moved to an explicit `## Migration target: <engine>` annexe.
- **6b:** "SQLite Busy Timeout/WAL" — link to §13 AC-22 + §05 AC-SD-22 (Lesson #36, do NOT restate).
- **6c:** "Timestamp unit ambiguity" — pin `ALL timestamps are UTC ISO-8601 strings; INTEGER columns are seconds-since-epoch` in §00 + AC.

### Phase 7 — spec/27 D4 + D1 (92 → 96)

- **7a:** Add a worked end-to-end transcript: `linter-scripts/audit-ai-implementability.py spec/22-git-logs-v2 --json` → sample output → interpretation.
- **7b:** Tighten 2 D1 ambiguities (TBD until we run a fresh `--force` re-score; gateway is up per Lesson #38).

### Phase 8 — Final tree-wide re-score (gate to 100%)

- Run `python3 linter-scripts/audit-ai-implementability.py --modules 22,23,24,25,26,27,28 --force --report-only` against `.lovable/cache/audit-ai/`.
- Any module < 100 → open a follow-up sub-phase against its remaining `issues[]`.
- Update scorecard memory snapshot with new totals.

---

## Cross-cutting principles enforced every phase

1. **Lockstep:** every spec edit touches `§97 + §98 row + §99 inventory` in one commit; banner bumps follow Lesson #25 (minor for new content, patch for prose).
2. **Lesson #36 always:** new cross-module facts **link, never restate** — eliminates a whole drift class.
3. **Closed enumerations always:** any "etc." or "language-specific exception" gets converted to an explicit Exception Ledger (Lesson #22).
4. **`**Verifies:**` on every new AC** (Lesson #16/#17), authored via `linter-scripts/fill-missing-acceptance-criteria.cjs` not by hand.
5. **5 strict gates GREEN before declaring phase closed:** lockstep · tree-health strict · version-parity · freshness · folder-refs.
6. **Re-score after every spec/22 phase + at end of every other phase** (gateway is up per Lesson #38; single-module `--force` is cheap).

---

## What I need from you

Pick the entry point — recommended order is the impact ranking above (**Phase 1 = spec/22**), but you may want a different driver:

1. **Phase 1 (spec/22 self-lift)** — biggest single-module lift, highest leverage.
2. **Phase 8-style "quick wins" sweep first** — close all 15 small issues across modules 23/24/25/26/28 before tackling spec/22; faster green-checks but smaller mean lift.
3. **Re-score first** — burn one gateway call to refresh all 7 cache entries (cache may already be stale; numbers above could change), then re-plan.
4. **Different module first** — pick any of the 7 by name.

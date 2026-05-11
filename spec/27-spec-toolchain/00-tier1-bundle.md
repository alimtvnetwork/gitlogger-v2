---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §27 source files an LLM must read to understand the spec-toolchain, navigate the active gate set, and know which slot doc to consult for any specific gate. Targets the Raw-LLM persona (single context window, no file-tool access). All other §27 files are tier-2 (per-gate slot docs, read on demand) or tier-3 (changelog archaeology, allowlists, runner stubs). Out-of-bundle files MUST NOT introduce cross-gate contracts not pinned by tier-1.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §27 spec set"
---

# Spec Toolchain — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-67 B-6 — initial tier-1 / tier-2 / tier-3 partition; introduced to lift §27 Raw-LLM persona score by carving a ~1.6K-line navigable subset out of the 12,546-line full §27 corpus.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §27 is a *meta-module*: it specifies the gates that audit the other six in-scope cohorts (§22-§26, §28). Most §27 files are per-gate slot docs (one file per active gate, ~50-200 lines each). To **navigate** §27 you only need the four tier-1 files below (~1,573 lines). To **work on a specific gate**, add the corresponding tier-2 slot doc on demand. The 1,080-line `98-changelog.md` is tier-3 — never required for current work.

---

## Tier-1 — Navigable minimum (read in order)

| # | File | Lines | Role | Why tier-1 |
|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 465 | Module pin + active-gate count (26) + invariants triple (I-1 EXISTS, I-2 WIRED, I-3 NUMBERED) + slot-numbering scheme + retired-gate frozen list (INV-03 anchor) | Establishes the toolchain's vocabulary, the gate-counting rule, and the perimeter for slot numbers. Read first. |
| 2 | [`trace-map.md`](./trace-map.md) | 419 | Gate dependency DAG: which gates are prerequisites for which others; per-gate `consumes` / `produced_for` rows | The single source for "which gate to consult / extend first". Without this, an implementer cannot order changes correctly. |
| 3 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 429 | 36 ACs for the toolchain itself (AC-T-* family — gate hygiene, slot reflexivity, ledger lockstep) | Every gate-side contract is here. Read after the trace map so each AC's `Verifies:` cell already names a known gate slot. |
| 4 | [`99-consistency-report.md`](./99-consistency-report.md) | 260 | Newest banner block + per-version scorecard delta + current Sess-NN tasks | Tells the reader where the toolchain is **right now** (versions, last-shipped gate, open tickets). Read last in tier-1. |
| **Σ** | **4 files** | **~1,573** | **Tier-1 footprint** | Below the 8K-token "single context window" comfort threshold. |

**Read-order rationale:** vocabulary + invariants (1) → gate dependency graph (2) → contracts (3) → current state (4). After tier-1 the reader knows: how many active gates exist, which slot file owns each gate, what each gate guarantees, and which gate(s) are currently open work.

---

## Tier-2 — Per-gate slot docs (read on demand, one file per gate)

§27 follows a **one-file-per-slot** convention: every active gate gets a numbered slot file (`NN-<short-name>.md`) describing its purpose, clauses, self-test fixture roster, and CI wiring. Read the slot doc only when working on that specific gate. The slot files are listed in `00-overview.md` Active Gate Inventory section in canonical numeric order — duplicate the read-order from there.

**Categories** (all tier-2; read by category as needed):

| Category | Slot range | Examples | When to read |
|---|---|---|---|
| Cross-link / structural hygiene | 01-09, 18, 19 | spec cross-links, forbidden strings, mermaid syntax | When editing inter-spec navigation or adding a new spec file. |
| Generators (produce ledgers/reports) | 10-17 | spec-index, dashboard-data, gwt-acceptance, trace-map regenerator | When the auto-generated artefact drifts from its source spec. |
| Scaffolders / fillers | 20-23 | fill-missing-acceptance-criteria, scaffold-spec-module | When introducing a new spec module from scratch. |
| Lockstep + version parity | 24, 27, 29 | check-lockstep, check-99-stamp-bump, check-version-parity | When bumping a banner triple (§00/§97/§98/§99) on any cohort. |
| §99 freshness + audit cadence | 25, 26, 38, 46 | deepen-consistency-reports, check-99-summary-freshness, audit-quoted-evidence-marker | When editing any §99 file. |
| Audit-AI implementability | 33, 34, 35 | check-ai-confidence, audit-ai-implementability, audit-bundle-budget | When tuning auditor scoring or bundle sizes. |
| Cohort-specific surface gates | 39, 42-45, 49, 53-60, 63 | applink-xor, error-envelope-uniformity, ui-component-binding-matrix, appshell-route-matrix, no-sql-ddl-in-ui-folder, diagram-parity | When the named cohort surface gains a new contract. |
| Boundary / scope perimeter | 36, 58, 59, 60, 61 | ads-boundaries, no-sql-ddl-in-ui-folder, no-ci-yaml-in-issues-folder, no-toolchain-enum-in-issues-folder, no-out-of-scope-spec-folder-link | When the locked-7 perimeter is touched. |
| §97 hygiene + AC structure | 47, 48 | ac-section-orphan-header, ac-prefix-contract | When adding/removing/renaming any AC. |
| Sub-cohort boundary checks | 50, 51, 52, 56, 57 | validate-guidelines, axios-version, rest-pascalcase-parity, rest-boolean-parity | When editing platform contracts (REST surface, dependency pins). |
| §28 / §26 self-test harness | 62, 63 | check-ci-cli-self-test-harness, check-diagram-parity | When extending §28 self-tests or §26 diagram contracts. |
| Meta gates (audit the toolchain itself) | 64, 65 | meta-verify-lockstep, check-gate-ledger-vs-workflow | When making any structural change to §27 itself. |

**Per-gate slot doc anatomy** (canonical sections, mirrored across all slot files):
1. Status banner (`Active gate #N (Phase / Sess-NN tag)`)
2. Purpose + 1-paragraph "what does this gate guarantee?"
3. Clauses (numbered, each with Given/When/Then)
4. R5 anchor (vacuous-pass condition)
5. Self-test fixture roster (F-1..F-N)
6. CI invocation block (workflow step name, `--self-test` + live disk)
7. Failure modes + invalidation triggers
8. Cross-references to consumed/produced files

---

## Tier-3 — Specialised / archival (read only for the named purpose)

| File | Lines | Purpose | When to read |
|---|---|---|---|
| [`98-changelog.md`](./98-changelog.md) | 1,080 | Full version history of the toolchain (every banner since v1.0) | Spec-history archaeology only. Never required for current work — current state lives in §99. |
| `60-forbidden-strings-toml.md` | 85 | Forbidden-string list source | Read when adding a new forbidden literal to the perimeter. |
| `61-spec-cross-links-allowlist.md` | 71 | Allowlist for clauses that intentionally cross the perimeter | Read when adding a new cross-link exemption. |
| `62-spec-folder-refs-allowlist.md` | 86 | Allowlist for spec-folder reference checker | Read when adding a new folder-ref exemption. |
| `63-readme-cross-links-md.md` | 44 | README cross-link spec | Read when editing the repo README. |
| `40-run-sh.md` | 66 | `run.sh` runner stub spec | Read when editing the runner. |
| `41-run-ps1.md` | 59 | `run.ps1` runner stub spec | Read when editing the PowerShell runner. |
| `70-spec-health-yml.md` | 86 | `spec-health.yml` workflow spec | Read when editing the health workflow contract. |
| `71-spec-monthly-audit-yml.md` | 89 | `spec-monthly-audit.yml` workflow spec | Read when editing the monthly audit workflow contract. |
| `80-lib-fixture-replay.md` | 85 | Shared fixture-replay helper spec | Read when factoring fixtures across slot self-tests. |

---

## Reader pre-flight checklist (per persona)

| Persona | Read order | Stop reading after | Navigation guarantee |
|---|---|---|---|
| **Raw-LLM** (single context window) | Tier-1 only | After file 4 (`99-consistency-report.md`) | High for "what is §27, what gates exist, what is open right now". To work on a specific gate, request a follow-up turn that loads only the relevant slot doc + the cohort it audits. |
| **Cursor / Claude-Code** (file access + shell) | Tier-1 in order, then load tier-2 slot doc(s) on demand | When the gate under work is covered | Very high; meta-gates (slots 64, 65) catch drift in real time. |
| **Lovable** (full agent + Cloud + UI preview) | Tier-1 as primer, jump to whichever tier-2 the current sub-task names | n/a — agent re-loads files on demand | Very high; same as Cursor. |

---

## Drift contract (Lesson #36 + Lesson #15 reflexivity)

- **Add or retire a gate** → update both the relevant tier-2 category row here AND the Active Gate Inventory in `00-overview.md` in the same commit. Failure to do so MUST be flagged by the next §99 entry.
- **Add a new tier-3 file class** (e.g. a new runner stub) → add a row to the tier-3 table here in the same commit.
- **Tier-1 footprint MUST stay ≤ 1,800 lines** (the soft Raw-LLM ceiling for a meta-module). Breach triggers a tier-1 candidate-removal review in the same commit. Note: this ceiling is intentionally tighter than §22's 2,500 because §27 is a meta-module — its tier-1 should be navigation-only, not contract-bearing.
- **Forbidden:** introducing a new normative cross-gate contract in any tier-2 / tier-3 file that is not also surfaced (by reference) in tier-1. The four tier-1 files pin the cross-gate contract surface; per-slot files pin only their own gate.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Gate dependency trace map](./trace-map.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§22 tier-1 essential bundle](../22-git-logs-v2/00-tier1-bundle.md) — sibling navigation-aid for §22 (Sess-67 B-1)

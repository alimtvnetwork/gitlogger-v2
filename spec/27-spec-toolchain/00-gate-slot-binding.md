---
kind: gate-slot-binding-table
todo_audit_exempt: true
description: Canonical, single-source-of-truth binding between every active gate number (#20..#46, 26 gates total) and its owning slot file under spec/27-spec-toolchain/. Closes the Sess-67 B-9 gap where §00 §"CI Gate Enumeration" stopped at gate #30 while the on-disk `**Status:** Active gate #N` headers extended to #46. Pure navigation-aid surface — no new gates, no new ACs, no implementation. Reflexive Lesson #15 anchor for any future gate addition: bumping the active count without adding a row here MUST fail the next gate-ledger lockstep audit.
content_axis: gate-inventory
axis_rationale: "Single-page binding map: gate-# ↔ slot file ↔ AC family ↔ workflow step name"
---

# Active Gate ↔ Slot Binding Map

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-67 B-9 — initial flat binding extracted from on-disk `**Status:** Active gate #` headers across `spec/27-spec-toolchain/*.md`. Total active gates: **26** — banner-triple parity with §00/§98/§99.)
**Authoritative:** Yes for the binding map (gate-# → slot file). Per-gate clauses, fixtures, and CI step body remain authoritative in their own slot files (Lesson #36 link-don't-restate).

> 🤖 **Reader pin.** §00 §"CI Gate Enumeration" lists rows up to gate #30 in narrative form (the prose history of how the first ten Phase-5 gates landed). It is **not** a complete inventory — the cohort-surface gates #31..#46 land via individual slot files (slots 50..65). This document is the **flat lookup table** an LLM/auditor needs to answer "which slot file owns gate #N?" without scanning 26 files.

> **Recount basis (frozen):** `grep -lE '^\*\*Status:\*\*\s+Active\s+gate\s+#' spec/27-spec-toolchain/*.md | wc -l` MUST equal **26**. Any divergence between this count, the §00/§98/§99 banner triple, and the row count in the table below is a `meta-verify-lockstep` (gate #42, slot 64) clause-5 failure.

---

## Active Gate Inventory (canonical ordering by gate number)

| Gate # | Slot file | AC family / cohort owned | Workflow step substring | Phase / Sess tag | Status anchor |
|---|---|---|---|---|---|
| #20 | [`37-check-spec22-inventory.md`](./37-check-spec22-inventory.md) | §22 AC-78 + AC-22-LV1 (locked-vacant slots 09..13) | `§22 inventory gate (#20 / G-6h / slot 37)` | Sess-56 A-48 | Self-test 3/3 + live disk |
| #22 | [`39-check-applink-xor-clause.md`](./39-check-applink-xor-clause.md) | §23 AC-ADB-05 + AC-ADB-13 + AC-ADB-R-4 invariant 6 (AppLink XOR + disconnect + locked-ID seed + partial index) | `§23 AppLink XOR clause gate (#22 / G-6w / slot 39)` | Phase-5 T-15 | Self-test 6/6 + live disk |
| #23 | [`42-check-error-envelope-uniformity.md`](./42-check-error-envelope-uniformity.md) | AC-CAF-02 cross-cutting (§22 ErrorEnvelope schema-pin / §23 R-3 mirror / §24 AC-ADS-15 UI-mirror) | `§22/§23/§24 ErrorEnvelope uniformity gate (#23)` | Phase-5 T-16 | Self-test + live disk |
| #24 | [`43-check-boolean-uniformity-primary-lane.md`](./43-check-boolean-uniformity-primary-lane.md) | AC-CAF-01 cross-cutting (§23 R-4 inv-2 / §22 OpenAPI / §24 U-3 boolean parity) | `§23/§22/§24 boolean primary-lane gate (#24)` | Phase-5 T-17 | Self-test + live disk |
| #25 | [`44-check-seedable-config-row-present.md`](./44-check-seedable-config-row-present.md) | AC-CAF-04 cross-cutting (§24 §00 S-1↔S-2↔S-3 seedable config) | `§24 seedable config row gate (#25)` | Phase-5 T-18 | Self-test + live disk |
| #26 | [`45-check-idempotency-observability.md`](./45-check-idempotency-observability.md) | AC-CAF-03 cross-cutting (§23 R-1 ∪ §24 S-2 idempotent set + WE-4 disconnect + observability marker) | `§23/§24 idempotency observability gate (#26)` | Phase-5 T-19 | Self-test + live disk |
| #27 | [`46-check-audit-quoted-evidence-marker.md`](./46-check-audit-quoted-evidence-marker.md) | AC-CAF-05 cross-cutting (§24 marker + §25 AC-AI-10/11/14 verbatim-quote enforcement) | `§24/§25 audit quoted evidence marker gate (#27)` | Phase-5 T-20 | Self-test + live disk |
| #28 | [`47-check-ac-section-orphan-header.md`](./47-check-ac-section-orphan-header.md) | All seven §97 hygiene (orphan headers / status-tag vocab / empty-parent allowlist) | `§97 hygiene gate (#28 / T-21+T-22 clauses 4+5)` | Phase-5 T-21; T-22 (Sess-67 G-T-22) | Self-test 8/8 + live disk |
| #29 | [`48-check-ac-prefix-contract.md`](./48-check-ac-prefix-contract.md) | All seven §97 + §00/§98/§99 (AC-prefix↔folder ownership map) | `§97 AC-prefix contract gate (#29)` | Phase-5 T-22 | Self-test 6/6 + live disk |
| #30 | [`49-check-ui-component-binding-matrix.md`](./49-check-ui-component-binding-matrix.md) | §24 U-1 ↔ §23 R-1 binding + U-2 four-state + U-3 boolean parity | `§24 U-1 component binding gate (#30 / T-23)` | Phase-5 T-23 | Self-test 6/6 + live disk |
| #31 | [`53-check-appshell-route-matrix.md`](./53-check-appshell-route-matrix.md) | §24 AppShell route matrix (first §24 route-surface gate) | `§24 AppShell route matrix gate (#31 / T-24)` | Phase-5 T-24 | Self-test + live disk |
| #32 | [`54-check-seed-id-explicit-locked-form.md`](./54-check-seed-id-explicit-locked-form.md) | §23 seed-ID explicit/locked-form (sibling to gate #22) | `§23 seed-ID explicit/locked-form gate (#32 / T-25)` | Phase-5 T-25 | Self-test + live disk |
| #33 | [`55-check-dialect-precedence-banner-present.md`](./55-check-dialect-precedence-banner-present.md) | §22 §00 + §23 §00 dialect-precedence banner + cross-cuts pin + §23 children lane markers | `§22/§23 dialect-precedence banner gate (#33 / T-26)` | Phase-5 T-26 | Self-test 6/6 + live disk |
| #34 | [`56-check-rest-pascalcase-parity.md`](./56-check-rest-pascalcase-parity.md) | §22 OpenAPI ↔ §23 R-2 PascalCase parity (REST surface) | `§22/§23 REST PascalCase parity gate (#34 / T-27)` | Phase-5 T-27 | Self-test + live disk |
| #35 | [`57-check-rest-boolean-parity.md`](./57-check-rest-boolean-parity.md) | §22 OpenAPI ↔ §23 R-2 + R-4 inv-2 ↔ §24 U-3 REST boolean parity | `§22/§23/§24 REST boolean parity gate (#35 / T-28)` | Phase-5 T-28 | Self-test + live disk |
| #36 | [`58-check-no-sql-ddl-in-ui-folder.md`](./58-check-no-sql-ddl-in-ui-folder.md) | §24 perimeter — no SQL DDL fences in UI folder | `§24 no-SQL-DDL boundary gate (#36 / T-29)` | Phase-5 T-29 | Self-test + live disk |
| #37 | [`59-check-no-ci-yaml-in-issues-folder.md`](./59-check-no-ci-yaml-in-issues-folder.md) | §25 perimeter — no CI workflow YAML fences in Issues folder | `§25 no-CI-yaml boundary gate (#37 / T-30)` | Phase-5 T-30 | Self-test 6/6 + live disk |
| #38 | [`60-check-no-toolchain-enum-in-issues-folder.md`](./60-check-no-toolchain-enum-in-issues-folder.md) | §25 perimeter — no toolchain-enum claims in Issues folder | `§25 no-toolchain-enum boundary gate (#38 / T-31)` | Phase-5 T-31 | Self-test + live disk |
| #39 | [`61-check-no-out-of-scope-spec-folder-link.md`](./61-check-no-out-of-scope-spec-folder-link.md) | Locked-7 perimeter — no out-of-scope spec folder links from §22..§28 | `Locked-7 perimeter gate (#39 / T-32)` | Phase-5 T-32 | Self-test + live disk; Lesson #15 reflexivity (cites itself in §00) |
| #40 | [`62-check-ci-cli-self-test-harness.md`](./62-check-ci-cli-self-test-harness.md) | §28 self-test harness contract | `§28 CI/CLI self-test harness gate (#40 / T-33)` | Phase-5 T-33 | Self-test + live disk |
| #41 | [`63-check-diagram-parity.md`](./63-check-diagram-parity.md) | §26 AC-DG-* diagram parity (6 clauses incl. clause-6 narrative-header schema) | `§26 diagram parity gate (#41 / G-6x / slot 63)` | Phase-5 T-34 (clause-6 Sess-67 G-8) | Self-test 8/8 + live disk |
| #42 | [`64-meta-verify-lockstep.md`](./64-meta-verify-lockstep.md) | Meta — banner-triple lockstep + gate-count parity across §00/§98/§99 | `§27 meta-verify lockstep gate (#42 / T-36)` | Phase-5 T-36 | Self-test + live disk; Lesson #15 reflexivity (cites itself in §00 line 17) |
| #43 | [`65-check-gate-ledger-vs-workflow.md`](./65-check-gate-ledger-vs-workflow.md) | Meta — ledger-vs-workflow (I-1 EXISTS / I-2 WIRED / I-3 NUMBERED) + retired-gate set | `§27 gate-ledger vs workflow gate (#43 / T-40 / P19a)` | Phase-5 T-40 / P19a | Self-test 9/9 + live disk; LAST ledger failure class cleared Sess-67 G-6aa |
| #44 | [`50-validate-guidelines-py.md`](./50-validate-guidelines-py.md) | Python coding-guidelines static-surface validator (slot in 50-59 src-validator band; gate-# assigned in 40s family) | `validate-guidelines.py static-surface gate (#44)` | Sess-67 G-6r | Self-test load-proven |
| #45 | [`51-validate-guidelines-go.md`](./51-validate-guidelines-go.md) | Go coding-guidelines static-surface validator (companion-resolver patch G-6y) | `validate-guidelines.go static-surface gate (#45 / G-6s / slot 51)` | Sess-67 G-6s | Static-surface probe (no Go runtime in CI) |
| #46 | [`52-check-axios-version.md`](./52-check-axios-version.md) | Axios dependency-pin perimeter (`package.json` walker) | `axios-version pin gate (#46 / G-6t / slot 52)` | Sess-67 G-6t | Self-test 6/6 + live disk |

**Row count:** 26 — MUST equal the on-disk grep recount (frozen above). Any future addition lands as a new row in canonical numeric order; any retirement moves the row to the §00 §"Retired Gate Numbers" frozen list AND removes it here in the same commit.

---

## Slot-range → gate-# coverage map (read-direction reverse lookup)

| Slot range | Slot files in range | Active-gate # range | Coverage notes |
|---|---|---|---|
| 01-09 | 9 (validators) | — (none yet promoted to numbered Active-gate ledger) | Pre-Phase-5 numbering retired (#1..#19); current ledger starts at #20. |
| 10-19 | 10 (generators + 17/18/19 validators) | — | Generators are not "gates" — they produce artefacts consumed by gates. |
| 20-29 | 10 (fillers + lockstep + freshness) | — | Same as 10-19 — these are scaffolders; their *behaviour* is gated by audit-stage gates. |
| 30-39 | 7 (auditors + boundary scanners) | #20 (slot 37) | Slot 37 is the first slot-mapped numbered gate. |
| 40-49 | 10 (runner stubs + cohort-surface gates) | #22..#30 (slots 39, 42-49) | Slots 40-41 = runner stubs (no gate). Slot 47 owns gate #28; slot 48 owns gate #29; slot 49 owns gate #30. |
| 50-59 | 10 (src-validators + cohort-surface gates) | #31..#37 + #44..#46 (slots 50-58) | Slots 50/51/52 = src-validator gates (#44/#45/#46). Slots 53-58 = cohort-surface gates (#31..#36). |
| 60-69 | 10 (configs + perimeter gates + meta gates) | #37..#43 (slots 59-65) | Slot 60 also overloaded with `forbidden-strings.toml` (config — see §00 row range 60-69 KIND). |
| 70-79 | 2 (workflow specs) | — | Workflow files are the *consumers* of gates, not gates themselves. |
| 80-89 | 1 (`80-lib-fixture-replay.md` shared helper) | — | Shared library spec; not a gate. |

**Single-direction invariant:** every Active-gate-# in the table above MUST resolve to exactly one slot file; every slot file with a `**Status:** Active gate #N` header MUST appear here. Reverse-coverage failure is itself a `meta-verify-lockstep` (gate #42) clause-5 failure.

---

## Reader workflow — "I have a gate number, what do I read?"

1. Look up the gate-# in the canonical table above.
2. Open the named slot file. Per the §27 §00-tier1-bundle anatomy, the slot file contains: status banner, purpose, clauses, R5 anchor, fixture roster, CI invocation, failure modes, cross-references.
3. If the gate audits a cohort surface (e.g. #30 audits §24 U-1 ↔ §23 R-1), open the consumed cohort spec next using the slot file's cross-references.
4. Never read `98-changelog.md` for current state — it is tier-3 archaeology only. Current state lives in `99-consistency-report.md` newest banner.

## Reader workflow — "I have a slot file, what gate does it own?"

1. `grep '^\*\*Status:\*\*' <slot-file>` — yields the gate-# immediately.
2. Cross-check against the row in this document. Mismatch is a `meta-verify-lockstep` failure.

## Reader workflow — "I am adding a new gate"

1. Pick the next free slot number per §00 inventory and §00 numbering convention table (slots 01-79 + special 80+).
2. Pick the next free gate-# (current high water = #46; next = #47 unless a retired number is being reclaimed — which is forbidden by INV-03).
3. In the **same commit**:
   - Create `spec/27-spec-toolchain/NN-<short-name>.md` with the 8-section anatomy.
   - Add the row here in canonical numeric order.
   - Bump §00 / §98 / §99 banner triple's `Total active gates` literal.
   - Wire the workflow step in `spec/27-spec-toolchain/70-spec-health-yml.md` (the spec; the YAML lives in `.github/workflows/spec-health.yml` and is updated by §28).
4. Run `python3 linter-scripts/check-gate-ledger-vs-workflow.py --self-test` (must stay green) and `python3 linter-scripts/64-meta-verify-lockstep.md` per its slot-doc invocation contract.

---

## Drift contract (Lesson #15 reflexivity + Lesson #36 link-don't-restate)

- **Adding / retiring a gate:** the row here MUST be added/removed in the same commit as the slot file change AND the §00/§98/§99 banner-triple bump. Failure is a `meta-verify-lockstep` (gate #42) clause-5 failure on next CI cycle.
- **Renumbering a gate:** forbidden by INV-03 (slot-immutability). To replace a gate, retire the old number (move to §00 §"Retired Gate Numbers" frozen list) and assign the next free number.
- **Restating clause bodies here:** forbidden by Lesson #36. This document is the **binding map** only — clauses, fixtures, and CI invocation bodies live in the slot files.
- **Cross-link integrity:** every `[\`NN-…\`](./NN-…)` link in the canonical table MUST resolve (gate #3 `cross-links-resolve`).
- **Banner-triple parity:** `Total active gates: 26` MUST agree across §00 line 15, §98 line 5, §99 line 5, and the row count here. Mismatch is a gate #42 clause-5 failure.

---

## Cross-References

- [Module overview (gate inventory in §00)](./00-overview.md)
- [Tier-1 essential bundle (read-order anchor)](./00-tier1-bundle.md)
- [Module acceptance criteria (AC-T-* family)](./97-acceptance-criteria.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [`64-meta-verify-lockstep.md`](./64-meta-verify-lockstep.md) — gate that enforces banner-triple + row-count parity
- [`65-check-gate-ledger-vs-workflow.md`](./65-check-gate-ledger-vs-workflow.md) — gate that enforces I-1 EXISTS / I-2 WIRED / I-3 NUMBERED on this very table

---
kind: bundle-manifest
todo_audit_exempt: true
description: Tier-1 essential bundle — the minimum subset of §28 source files an LLM (especially the Raw-LLM persona, no file-tool access) must read to understand the universal CI CLI (`glci`), invoke its command surface correctly, ship logs to a §22 server, and decode error envelopes. All other §28 files are tier-2 (recommended adjuncts) or tier-3 (config schemas, lifecycle diagrams, ledgers). Out-of-bundle files MUST NOT introduce normative cross-surface contracts not pinned by tier-1.
content_axis: navigation-aid
axis_rationale: "Single-page read-order anchor for the §28 CLI spec set"
---

# Universal CI CLI — Tier-1 Essential Bundle

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-68 B-7 — initial tier-1 / tier-2 / tier-3 partition; mirrors the §22 B-1 (Sess-67) and §27 B-6 (Sess-67) tier-1 manifest pattern. Targets the Raw-LLM persona; lifts §28 Raw-LLM C1 (Clarity) audit-defensibility 19 → 20 by surfacing read order on disk with self-cited gate enforcement.)
**Authoritative:** Yes — the partition below is normative for read-order claims; individual file contents remain authoritative in their own files (Lesson #36 link-don't-restate).

> 🤖 **Raw-LLM Reader Pin.** §28 is a *behavioural contract* for the `glci` binary (the canonical external invoker of the §27 gate suite and the client-side complement to spec/22's `riseup-git-logs` server-side endpoints). Read tier-1 in order; do NOT infer read order from `ls`, alphabetical slot order, or §00's "consumes:" frontmatter list. Tier-1 footprint = ~1 763 lines (well under the 2 500-line single-context-window comfort ceiling). To **work on a specific surface** (config resolution, CI-provider bindings, output classification), add the corresponding tier-2 file on demand.

---

## Tier-1 — Navigable minimum (read in order)

| # | File | Lines | Role | Why tier-1 |
|---|---|---|---|---|
| 1 | [`00-overview.md`](./00-overview.md) | 390 | Module pin + scope statement + `consumes:` cross-cohort frontmatter (§22/§27 anchors) + Raw-LLM Auditor Pin block + invariants | Establishes the CLI's vocabulary, its sole-in-scope external-invoker role for §27 gates, and the Lesson #36 link-don't-restate perimeter. Read first. |
| 2 | [`01-glossary-and-enums.md`](./01-glossary-and-enums.md) | 83 | Closed-set enums for runtime modes, push outcomes, error families | The single source of truth for every enum value used in the command surface, log-shipping contract, and error catalog. Read second so §04/§06/§07 enum citations resolve. |
| 3 | [`04-command-surface.md`](./04-command-surface.md) | 134 | `glci` subcommand inventory + global flag set (`--self-test`, `--check <mode>`) + per-subcommand argument shape | The canonical CLI surface contract. Without this, an implementer cannot pattern-match `glci push`, `glci verify`, `glci doctor`, or `glci --self-test` invocations in CI. |
| 4 | [`06-log-shipping-contract.md`](./06-log-shipping-contract.md) | 218 | Frame transport (NDJSON over HTTPS), retry/backoff with ±25% jitter, per-request + total-deadline timeouts, SSH-mode signing transcript | The behavioural core: how `glci` ships logs to a spec/22 server. Mirrors spec/22 §43 client-side wire shape per Lesson #36. |
| 5 | [`07-error-catalog.md`](./07-error-catalog.md) | 124 | Every `GLCI-*` error code + 4-row `--self-test` exit-code table (gate #40) + envelope shape pointer to §22 §15 | The canonical failure surface; required to interpret any non-zero exit from `glci` or any `GLCI-*` error in a server response. |
| 6 | [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) | 533 | All 49 `AC-28-*` ACs (behavioural + harness + cohort-discipline) + AC-T-* delegation table | Every CLI-side contract is here. Read after §04/§06/§07 so each AC's `Verifies:` cell already names a known surface. |
| 7 | [`99-consistency-report.md`](./99-consistency-report.md) | 145 | Newest banner block + version delta tail + open-task tail | Tells the reader where the §28 spec is **right now** (versions, last-shipped gate, open tickets). Read last in tier-1. |
| **Σ** | **7 files** | **~1 627** | **Tier-1 footprint** | Below the 2 500-line single-context-window comfort threshold. |

**Read-order rationale:** vocabulary + scope (1) → enum closed-sets (2) → CLI surface (3) → behavioural core (4) → failure catalog (5) → contract aggregator (6) → current state (7). After tier-1 the reader knows: every `glci` subcommand and flag, exactly how to ship a frame and decode failures, and which AC governs every behaviour.

---

## Tier-2 — Recommended adjuncts (read on demand)

Read these only when implementing or auditing the named surface. None of them introduce a normative contract that is not already pinned in tier-1; they expand on a tier-1 surface with implementer-grade detail.

| File | Lines | When to read |
|---|---|---|
| [`02-architecture.md`](./02-architecture.md) | 125 | When wiring `glci` into a new CI provider's process model (subprocess vs daemon, stdin/stdout disposition) — expands on §00. |
| [`03-runtime-detection.md`](./03-runtime-detection.md) | 123 | When the auto-detect logic for "am I in GitHub Actions / GitLab CI / Azure / local" needs review — expands on §08. |
| [`05-config-resolution.md`](./05-config-resolution.md) | 130 | When debugging precedence between env vars, `.glci.toml`, and CLI flags — pairs with `18-config-schema.json`. |
| [`08-ci-provider-bindings.md`](./08-ci-provider-bindings.md) | 82 | When writing or reviewing the example pipeline YAML for a CI provider (mirror the existing GitLab/Azure blocks). |
| [`09-output-classification.md`](./09-output-classification.md) | 120 | When tuning the rules that decide `outcome ∈ {OK, UserError, Internal}` for a captured log row. |

---

## Tier-3 — Specialised surfaces (out-of-bundle)

These files exist for completeness but are not required for any persona to understand the CLI's contract. They are typically machine-readable schemas, ledgers, or diagrams.

| File | Lines | Purpose |
|---|---|---|
| [`17-openapi-client.yaml`](./17-openapi-client.yaml) | (yaml) | OpenAPI client for the §22 server endpoints `glci` consumes. Use only when generating typed client bindings. |
| [`18-config-schema.json`](./18-config-schema.json) | (json) | JSON-Schema for `.glci.toml` and equivalent env-var shape. Use only when validating a config file. |
| [`98-changelog.md`](./98-changelog.md) | 258 | Per-version changelog tail. Use only when archaeology is required (e.g., "when did `--self-test` ship?"). |
| [`lifecycle-28-universal-ci-cli.mmd`](./lifecycle-28-universal-ci-cli.mmd) | (mermaid) | Mermaid lifecycle diagram for the `glci push` flow. Visualises §06; never the source of truth. |

---

## Per-persona pre-flight checklist

- **Raw-LLM persona** — Stops after file 7 (`99-consistency-report.md`). Tier-2 / tier-3 are out of context-window reach; do not attempt to load them. If a question demands tier-2 detail, the answer is "tier-2 file `NN-…md` would resolve this — please load it" and stop.
- **Cursor / Claude-Code persona** — Reads tier-1 in order, then loads tier-2 files on demand for the specific sub-task (e.g., add a CI-provider binding → load §03 + §08). Tier-3 schemas only when generating client bindings or validating a config file.
- **Lovable persona** — Uses tier-1 as primer (it has file-tool access already), then jumps directly to the relevant tier-2 / tier-3 file per current sub-task. Treats §97 as the contract index against which any code change must reconcile.

---

## Drift contract (Lesson #15 reflexivity)

1. Adding a new normative cross-surface contract (any `AC-28-*` clause governing ≥ 2 files, any new global flag, any new CLI subcommand, any new error family) MUST in the **same commit**: (a) author the contract in its owning tier-1 file, (b) update this manifest's Σ row + banner if line count crosses a 100-line bucket, (c) cite the new contract in §99's audit-row tail under that turn's task tag.
2. Adding a new tier-2 file that introduces a contract not yet pinned in tier-1 is **forbidden** — surface the contract in tier-1 first, then author the tier-2 file that delegates to it (mirror of §22 AC-22-CE1 + §27 AC-T-30 same-PR cohort discipline).
3. Promoting a tier-2 or tier-3 file to tier-1 MUST cite the AC family that newly depends on it AND re-tally the Σ row in the same commit.
4. Demoting a tier-1 file is allowed only when its normative obligations have been migrated into the surviving tier-1 set (Lesson #36 link-don't-restate audit required); the demotion commit MUST update the per-persona pre-flight checklist above.
5. Restating any clause body, fixture roster, or CI invocation body inside this manifest is **forbidden** (Lesson #36); this file is the partition + read-order map only.
6. **Line-budget invariant:** `wc -l spec/28-universal-ci-cli/{00-overview.md,01-glossary-and-enums.md,04-command-surface.md,06-log-shipping-contract.md,07-error-catalog.md,97-acceptance-criteria.md,99-consistency-report.md} | tail -1 | awk '{print $1}'` MUST be ≤ **2 500** (single-context-window comfort threshold). Any commit pushing the seven-file sum above 2 500 MUST in the same commit either (a) trim the offending file, or (b) demote a tier-1 file to tier-2 with a Lesson #36 link-don't-restate audit confirming all normative obligations are reachable from the surviving tier-1 set.

---

## Self-citation (Lesson #15 reflexivity, 20-band anchor)

This file's drift contract is **mechanically enforced by** `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §28 §00 / §98 / §99. Any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The line-budget invariant (clause 6 above) MAY be additionally enforced by a future extension of `audit-bundle-budget.py` (slot 35, gate #34) loading the seven-file tier-1 set as a named bundle target with the 2 500-line ceiling — until that extension ships, the line-budget is enforced by reviewer attestation that `wc -l` of the seven tier-1 files was checked in the same PR. The closed-set perimeter (clauses 1–5) is **mechanically enforced by** `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) on the link-target axis (any tier-1 file linking out to a non-locked-7 folder is a SPEC VIOLATION).

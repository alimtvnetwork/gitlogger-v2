---
kind: module
description: App-cohort runtime integration overview. Normative composition view of §23 (App database) ↔ §24 (App design-system & UI) ↔ §25 (App issues/audit-findings tracker) at runtime — data-flow, ownership boundaries, ErrorEnvelope propagation, joint-failure modes. Companion to §22's operational-pattern parent role declared in A-01 (Session 23).
content_axis: normative-contract
axis_rationale: "Cross-folder integration contract for the App cohort (§23+§24+§25) anchored to §22 as operational parent"
---

# App Cohort Integration Overview

**Document ID:** `GL2-COHORT-2026-05-10`
**Version:** 1.1.0
**Updated:** 2026-05-10 (Session 28 audit-task A-06 — added AC-COHORT-06 + normative `## Cohort Naming Convention` section)
**AI Confidence:** Production-Ready
**Ambiguity:** Low

---

## Keywords

`app-cohort` · `cohort-integration` · `cross-folder-composition` · `error-envelope-propagation` · `joint-failure-modes` · `ownership-boundary` · `runtime-data-flow`

---

## Why this file exists (forced-guess closure)

The Phase-3/Phase-4 implementability audits (Sessions 22–24) measured a **cohort-level joint-failure forced-guess** (X-1): a blind-AI implementer reading §23, §24, or §25 in isolation has no in-scope source telling them how the three folders compose at runtime — who emits an `ErrorEnvelope`, who renders it, who tracks the resulting issue, and where the boundary between them sits.

Without this file:
- §23 (App database) reads as a self-contained DDL contract, but its writer-paths emit errors that §24 must render and §25 must catalog.
- §24 (App design-system & UI) declares an `app-toolbar` slot for error/issue surfacing but does not name the upstream emitter.
- §25 (App issues) tracks findings but has no contract for **how a runtime issue becomes a finding row** (vs. an audit-tracker entry).

This file resolves all three blind spots with a single normative composition view, anchored to §22 as the operational-pattern parent (A-01, Session 23).

---

## AI Implementer Quickstart

**Read in this order to land a cross-cohort change in ≤30 min:**

1. **Cohort map** — `## Cohort Map` (below) for the 3-folder data-flow diagram.
2. **Ownership boundaries** — `## Ownership Boundaries` for the rule about which folder owns which contract surface.
3. **ErrorEnvelope propagation** — `## ErrorEnvelope Propagation` for the §23→§24→§25 flow.
4. **Joint-failure modes** — `## Joint-Failure Modes (X-1 closure)` before changing any cross-folder boundary.
5. **AC bindings** — [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) for `AC-COHORT-*` enforcement.

**Hard rules (do not violate):**
- §23 MUST emit the canonical `ErrorEnvelope` shape declared in §22 (per A-01); it MUST NOT define a parallel error shape.
- §24 MUST render envelope fields by token (`--app-error-bg`, `--app-error-text`); it MUST NOT inline-style.
- §25 MUST treat each persisted finding as an audit row anchored to a specific §22/§23/§24 file path + line; it MUST NOT invent finding rows that lack an in-scope anchor.
- The cohort scope-lock (`spec/22..28` only) applies transitively — no cohort integration step may emit a hop into `_archive/` or §00–§21.

---

## Cohort Map

The three App-cohort folders compose along a single runtime axis: **persistence → presentation → audit**.

```text
┌─────────────────────────────┐    write/read     ┌─────────────────────────────┐
│  §23 — App Database         │  ◀──────────────▶ │  §22 — git-logs-v2          │
│  (App, AppLink, AppStatus)  │                   │  (operational-pattern        │
│  Owns: DDL, polymorphic     │                   │   parent: ErrorEnvelope,    │
│  resolver, migration shape  │                   │   GL-* error family,        │
│                             │                   │   RequestId, AuditTrail)    │
└──────────────┬──────────────┘                   └──────────────┬──────────────┘
               │ emits ErrorEnvelope                             │ schema
               │ (per §22 contract)                              │ (envelope shape,
               ▼                                                 │  GL-* codes,
┌─────────────────────────────┐                                  │  RequestId)
│  §24 — App Design-System    │ ◀────────────────────────────────┘
│  & UI                       │
│  (App overlay tokens,       │     renders envelope by token
│  AppShell, AppToolbar,      │     (--app-error-bg, etc.);
│  error surfaces)            │     never inline-styles errors
│  Owns: token additions,     │
│  composite app components   │
└──────────────┬──────────────┘
               │ surfaces user-facing failure;
               │ persists structured AuditTrail row
               │ (per §22 contract)
               ▼
┌─────────────────────────────┐
│  §25 — App Issues           │
│  (consolidated audit        │
│   findings tracker;         │
│   v1→v2 disposition map)    │
│  Owns: spec-time finding    │
│  catalog + dispositions     │
│  (NOT runtime error log;    │
│   that is §22 AuditTrail)   │
└─────────────────────────────┘
```

**Critical distinction.** §25 is a **spec-time** tracker (audit of the spec itself, F-NN findings). It is **NOT** the runtime audit log — that is `AuditTrail` owned by §22. Conflating the two is the most common joint-failure mode (J-2 below).

---

## Ownership Boundaries

| Surface | Owner | Consumers | Forbidden in non-owners |
|---|---|---|---|
| `ErrorEnvelope` shape (`code`, `message`, `requestId`, `details`) | **§22** (per A-01) | §23, §24, §25 | Re-declaring fields, renaming `requestId`, adding sibling envelopes |
| `GL-*` error-code family + extension rules | **§22** (`15-error-codes.md`) | §23 (DB-class codes), §24 (UI-class codes) | Inventing a `GL-*` code without registering it in `15-error-codes.md` |
| `RequestId` correlation header (`X-Request-Id` ↔ `Traceparent` precedence) | **§22** (`20-observability.md`) | §23 (logged on every write), §24 (echoed in error toasts), §25 (cited in finding `Linked` column) | Inventing per-folder request-id schemes |
| `AuditTrail` event emission contract | **§22** (`20-observability.md`) | §23 (writer-paths), §24 (user-action paths) | §25 emitting AuditTrail rows (it is spec-time, not runtime) |
| App DDL (`App`, `AppLink`, `AppStatus`) | **§23** | §22 (consumes table names in endpoint contracts), §26 (renders ER diagram) | §24 redefining tables; §25 inventing new tables in finding text |
| App-overlay tokens (`--app-*`) | **§24** | §23 admin-UI hooks (per `03-admin-ui.md`), §25 dashboard slot 11 (per §27 toolchain) | §22 inlining raw HSL; §23 styling its admin-UI without tokens |
| Spec-time finding catalog (F-NN tracker) | **§25** | §27 toolchain (dashboard slot 11), §22 backlog (Carried-open rows from disposition map) | §22/§23/§24 forking parallel finding lists |
| **Schema-drift gate (§22 §97 AC-23 — PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog)** | **§22** (`97-acceptance-criteria.md` AC-23) | **§23** (App DDL — every `CREATE TABLE` and migration MUST satisfy AC-23 catalog), **§28** (CI binary — emits `drift-warning` rows when server schema diverges from the AC-23 catalog) | §23 inventing non-PascalCase columns or non-AUTOINCREMENT PKs; §28 silently swallowing schema-drift signals; any folder restating the AC-23 catalog instead of citing it (Lesson #36 link-don't-restate). Cross-flag added by A-07 (Sess-29) — §23 + §28 declare `consumes: [spec/22-git-logs-v2 §97 AC-23]` in front-matter. |

**Boundary enforcement rule.** When a cross-folder change is needed, the **owner** folder ships the contract change first; consumer folders update in the **same PR** to keep §99 lockstep intact. Reverse order (consumer-first) is forbidden because it leaves the cohort in a transiently inconsistent state that the §27 dashboard will flag.

---

## ErrorEnvelope Propagation

A runtime failure originating in §23 propagates as follows. Each step names the in-scope source-of-truth so a blind-AI implementer never has to guess.

| Step | Origin | Contract source | Action |
|---|---|---|---|
| 1 | §23 writer-path detects failure (e.g., polymorphic-FK violation) | §22 `15-error-codes.md` | Compose `ErrorEnvelope { code: "GL-DB-NN", message, requestId, details }`; emit `AuditTrail` row with same `requestId` |
| 2 | §22 endpoint handler returns envelope | §22 `04-rest-api-endpoints.md` + `17-openapi.yaml` | HTTP body = envelope verbatim; `X-Request-Id` echoed in response header per §22 `20-observability.md` precedence rule |
| 3 | §24 client receives envelope | §24 `00-overview.md` `## Phase 61 Reference: App UI Component Registry API` | Renders via `<AppErrorToast />` styled with `--app-error-bg` / `--app-error-text` (no inline styles); shows `requestId` in copyable footer |
| 4 | If the error class is `severity: Critical`, §22 emits an additional `AuditTrail` row | §22 `20-observability.md` | Persisted to runtime audit log (NOT §25 tracker) |
| 5 | If a recurring spec-level pattern emerges from runtime errors, an auditor may file a §25 finding | §25 `00-overview.md` `## How to Use This Document` | New `F-NN` row anchored to a specific §22/§23/§24 file + line; **never** to a runtime log entry |

**Invariant.** The `requestId` field MUST appear in steps 1, 2, 3, and 4. If any step drops it, the cohort fails the `AC-COHORT-03` correlation contract.

---

## Joint-Failure Modes (X-1 closure)

The Phase-3 audit identified five joint-failure modes that no single folder's contract can prevent. Each is enumerated here with its detection signal and remediation owner.

| ID | Failure mode | Detection signal | Remediation owner | Linked AC |
|---|---|---|---|---|
| **J-1** | §23 emits a non-§22 error shape (e.g., bare string) | §27 lint rule `error-envelope-shape-check` | §23 (must adopt §22 envelope) | AC-COHORT-01 |
| **J-2** | §25 finding row treated as a runtime audit entry | §27 lint rule `finding-vs-audit-distinction-check` (forbids `AuditTrail` references inside §25 `Evidence` blocks unless explicitly tagged `runtime-cite`) | §25 (must clarify in finding text) | AC-COHORT-02 |
| **J-3** | `requestId` lost between §23 emit and §24 render | §22 `20-observability.md` integration test (round-trip header echo) | §22 (correlation contract owner) | AC-COHORT-03 |
| **J-4** | §24 component inline-styles an error surface, breaking dark/light parity | §27 lint rule `no-raw-color-in-app-component` | §24 (token-discipline owner) | AC-COHORT-04 |
| **J-5** | §25 Carried-open backlog row left unrouted (no matching §22 backlog ticket) | §25 `## v1→v2 Finding Disposition Map` row stuck in `Carried-open` for >1 session without a §22 backlog citation | §22 (must open the ticket) + §25 (must add the citation) | AC-COHORT-05 |

**Failure-likelihood ranking** (highest first): J-2 > J-3 > J-1 > J-5 > J-4. J-2 is highest because the spec-time vs runtime distinction is non-obvious to a blind-AI reader; the §25 disposition map (A-02, Session 24) and this file together are the only in-scope sources that name it explicitly.

---

## Acceptance Criteria (cohort-level)

Cohort ACs live alongside per-folder ACs and are enforced by the §27 toolchain. They are summarized here and rolled up in [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) under the `AC-COHORT-*` family.

| AC ID | Statement | Verifies |
|---|---|---|
| **AC-COHORT-01** | Every error emitted by §23 writer-path uses the §22 `ErrorEnvelope` shape verbatim — no extra fields, no missing `requestId`. | §22 `15-error-codes.md` envelope schema · §27 `error-envelope-shape-check` lint rule |
| **AC-COHORT-02** | Every §25 finding row anchors to a spec file path + line under `spec/22..28/`; no row anchors to a runtime log entry. | §25 `00-overview.md` "How to Use" table · §27 `finding-vs-audit-distinction-check` lint rule |
| **AC-COHORT-03** | A `requestId` minted at the §23 writer-path is echoed in the §22 HTTP response header AND surfaced in the §24 error component AND (if `severity: Critical`) persisted in the §22 `AuditTrail` row — same value across all four. | §22 `20-observability.md` round-trip integration test |
| **AC-COHORT-04** | No App-cohort component (under §24's component registry) inline-styles any error surface; every error color resolves via `--app-error-*` tokens with light + dark values present. | §24 `## Phase 61 Reference: App UI Component Registry API` · §27 `no-raw-color-in-app-component` lint rule |
| **AC-COHORT-05** | Every `Carried-open` row in §25's v1→v2 disposition map has a matching §22 backlog ticket within 1 spec-improvement session of being added; otherwise the §27 dashboard slot 11 raises a `cohort-orphaned-finding` warning. | §25 `## v1→v2 Finding Disposition Map` rollup · §27 dashboard slot 11 |
| **AC-COHORT-06** | Every in-scope folder + file MUST satisfy the canonical naming convention declared in `## Cohort Naming Convention (A-06)` below: folders match `^spec/2[2-8]-[a-z0-9-]+/$`; files match `^[0-9]{2}-[a-z0-9-]+\.md$` (or recognised special files: `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`, `lifecycle-*.mmd`, `error-codes.json`, `_archive/`); and slot reservations (00 overview · 49–59 detail-AC family · 60+ cohort/integration · 97/98/99 governance trio) MUST hold. Any violation is a `cohort-naming-violation` lint failure (blocks merge). | §27 `cohort-naming-check` lint rule (deferred) · `linter-scripts/check-spec-cross-links.py` filename pattern subset |

---

## Cohort Naming Convention (A-06, Session 28 — normative)

The naming convention below is the single in-scope source-of-truth for all 7 cohort folders. A blind-AI implementer creating a new file MUST consult this section before choosing a slot or filename — without it, the most common failure mode is collision with a reserved slot or governance file.

**Folder pattern.** `^spec/2[2-8]-[a-z0-9-]+/$` — exactly 7 folders, immutable under the active scope-lock. Adding an 8th folder requires a memory-level scope-lock change, NOT a spec change.

**File pattern.** `^[0-9]{2}-[a-z0-9-]+\.md$` for normative content; the following special files are allowed and required where listed:

| Slot | Filename pattern | Required? | Owner | Purpose |
|---|---|---:|---|---|
| `00` | `00-overview.md` | **Required** in every folder | folder owner | H1 + Version + Updated banner + AI Implementer Quickstart + content router |
| `01..48` | `^(0[1-9]\|[1-3][0-9]\|4[0-8])-[a-z0-9-]+\.md$` | Optional | folder owner | Per-topic normative content (DDL, endpoints, flows, etc.) |
| `49..59` | `^(49\|5[0-9])-ac-[a-z0-9-]+-detail\.md$` | Optional, reserved | folder owner | AC-detail family (deep-dive per-AC contracts; §22 uses 49–59 today) |
| `60..96` | `^(6[0-9]\|[7-9][0-9])-[a-z0-9-]+\.md$` | Optional | folder owner | Cohort/integration files, cross-cutting overlays (e.g., `60-app-cohort-integration.md`) |
| `97` | `97-acceptance-criteria.md` | **Required** in every folder | folder owner | Per-folder AC roll-up |
| `98` | `98-changelog.md` | **Required** in every folder | folder owner | Reverse-chronological release log |
| `99` | `99-consistency-report.md` | **Required** in every folder | folder owner | Health/inventory + open items + drift acknowledgment |
| n/a | `lifecycle-*.mmd` | Optional | folder owner | Mermaid lifecycle diagrams (rendered by §26) |
| n/a | `error-codes.json` | Optional, reserved | §22 | Machine-readable error catalog (currently §22-only) |
| n/a | `_archive/` | Optional | folder owner | Frozen historical content; invisible to active gates |
| n/a | `README.md` | Allowed | folder owner | Human-facing landing page (non-normative) |

**Reserved slots (binding):**
- Slot `00` is **always** the module overview — never a per-topic file.
- Slots `49..59` are **reserved** for the `*-detail.md` AC family. A non-AC-detail file in this range is a violation.
- Slots `60..96` are **reserved** for cohort/integration files. A per-topic content file SHOULD land in `01..48`.
- Slots `97`, `98`, `99` are **always** the governance trio.

**Forbidden patterns:**
- `^[A-Z]` anywhere in a filename (kebab-case is the only allowed casing for content files).
- `_` (underscore) in slot-numbered files (only `_archive/` and `_*` non-content directories may use underscores).
- Two files claiming the same slot number in the same folder.
- A folder under `spec/` that does not match the in-scope folder pattern (enforced by scope-lock memory rule, not by this AC).

**Cohort linkage.** This section is the normative anchor for naming. The following consumers cite it:
- §25 `02-consolidated-audit-findings/97-acceptance-criteria.md` AC-03 (filename pattern check) — narrows here for the cohort-level invariant.
- §27 toolchain rule `cohort-naming-check` (to be implemented) — programmatic enforcement.
- A-22 (Wave-4 cross-folder glossary) will cite this section when defining "module slot" terminology.

A-06 closes the blind-AI naming-guess failure mode: previously a new-file author had to read the §25 prose-AC + scan filenames in a sample folder to infer the convention; now a single normative section answers "which slot, which filename, which folder" in one place.

---

## Cross-References

| Reference | Location |
|---|---|
| Operational-pattern parent declaration (A-01) | [`./00-overview.md`](./00-overview.md) §Operational Pattern Parent (Session 23) |
| ErrorEnvelope schema | [`./15-error-codes.md`](./15-error-codes.md) |
| RequestId / Traceparent precedence | [`./20-observability.md`](./20-observability.md) |
| App DDL | [`../23-app-database/00-overview.md`](../23-app-database/00-overview.md) |
| App-overlay tokens + component registry | [`../24-app-design-system-and-ui/00-overview.md`](../24-app-design-system-and-ui/00-overview.md) |
| Spec-time finding catalog + v1→v2 disposition map (A-02) | [`../25-app-issues/02-consolidated-audit-findings/00-overview.md`](../25-app-issues/02-consolidated-audit-findings/00-overview.md) |
| Cohort lint rules | [`../27-spec-toolchain/00-overview.md`](../27-spec-toolchain/00-overview.md) |

---

## Drift Acknowledgment

**Date:** 2026-05-10
**Status:** Forward-looking cohort contract — drift expected as §22..§28 evolve.

This file is intentionally a thin composition view, not a re-statement of any owner contract. If a cell in the Ownership Boundaries table conflicts with the owner folder's own contract, **the owner folder wins** and this file MUST be updated in the same PR.

```
Do you understand?
```

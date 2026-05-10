# 71 — spec-monthly-audit.yml

**Version:** 1.0.0  
**Updated:** 2026-04-26  
**Source:** [`.github/workflows/spec-monthly-audit.yml`](../../.github/workflows/spec-monthly-audit.yml)  
**Category:** CI workflow (cadence)

---

## Purpose

Phase 35 (R3) deliverable from [`32-phase-26-31-rollup.md`](../17-consolidated-guidelines/32-phase-26-31-rollup.md) §4. Provides a **time-driven** companion to the **event-driven** [`70-spec-health-yml.md`](./70-spec-health-yml.md):

| Workflow | Trigger | Catches |
|----------|---------|---------|
| `spec-health.yml` | Push/PR touching `spec/` or any linter | Regressions caused by spec edits |
| `spec-monthly-audit.yml` | `cron: '17 3 1 * *'` (monthly) + manual | Drift that no spec edit produced (rotted external links, dependency upgrades, scorer drift, deferred re-audits) |

Without the cadence workflow, the only way to discover (e.g.) a sibling-repo rename that broke 4 cross-links is the next time someone touches `spec/`. That delay accumulated the 67-item Phase 26-31 backlog.

---

## Cadence rationale

Monthly is the slowest cadence that still catches drift before it accumulates into multi-phase debt:

- **Daily** — too noisy; would flag transient GitHub Actions outages as audit failures.
- **Weekly** — surfaces regressions fast but inflates issue tracker for low-signal events.
- **Monthly** — Phases 26-31 took one session at 67 items; quarterly would have been ~200 items and unworkable in one sweep. Monthly bounds the worst-case backlog at ~25 items.

Cron `17 3 1 * *` chosen for off-peak (03:17 UTC = 11:17 Asia/Kuala_Lumpur), avoiding hourly scheduler congestion.

---

## Job

Single job `monthly-audit` running:

1. Checkout + Node 20 + Python 3.12.
2. **Cross-link gate** — `check-spec-cross-links.py --github` (zero broken).
3. **Tree health gate** — `check-tree-health.cjs --min=100 --report` (rubric v2.0.0).
4. **Dashboard parity check** — Phase 34 invariant: `dashboard-data.json` `Health.Score` MUST equal `check-tree-health.cjs` reported score. Failure means one of the two scorers has drifted.
5. **Trace-map regression gate** — `check-trace-map-regression.py`.
6. **Build summary** — markdown summary block in the GitHub Actions step summary.
7. **Open tracking issue on failure** — auto-files an issue labelled `spec-audit`, `regression`, `automated`, linking to the failed run and pointing triagers at the Phase 26-31 rollup pattern catalogue.

---

## Acceptance criteria

### AC-71-01 — Workflow file exists at canonical path
- **Given** the repository,
- **When** the path `.github/workflows/spec-monthly-audit.yml` is checked,
- **Then** it MUST exist (asserted by §31 audit code-mapping and Phase 35 closure).

### AC-71-02 — Cron schedule matches monthly cadence
- **Given** the workflow file,
- **When** `on.schedule` is parsed,
- **Then** it MUST contain exactly one cron expression of the shape `<minute> <hour> 1 * *` (1st of every month).

### AC-71-03 — `workflow_dispatch` is enabled
- **Given** the workflow file,
- **When** `on.workflow_dispatch` is checked,
- **Then** it MUST be present so manual re-runs are possible without waiting for the next scheduled tick.

### AC-71-04 — Dashboard parity step is present
- **Given** the `monthly-audit` job,
- **When** its steps are inspected,
- **Then** there MUST be a step that compares `dashboard-data.json` `Health.Score` to `check-tree-health.cjs --report` and fails the build on mismatch (Phase 34 invariant).

### AC-71-05 — Failure opens a tracking issue
- **Given** the `monthly-audit` job fails for any reason,
- **When** the workflow finishes,
- **Then** a new GitHub issue MUST be opened with labels `spec-audit`, `regression`, `automated` and a link to the failing run.

### AC-71-06 — Permissions follow least-privilege
- **Given** the workflow file,
- **When** `permissions:` is inspected,
- **Then** it MUST grant `contents: read` and `issues: write` and nothing else.

---

## Cross-references

- [`05-check-tree-health.md`](./05-check-tree-health.md) — rubric source of truth.
- [`11-generate-dashboard-data.md`](./11-generate-dashboard-data.md) — dashboard scorer (must remain in parity).
- [`17-check-trace-map-regression.md`](./17-check-trace-map-regression.md) — trace-map regression gate.
- [`70-spec-health-yml.md`](./70-spec-health-yml.md) — event-driven companion workflow.
- [`spec/17-consolidated-guidelines/32-phase-26-31-rollup.md`](../17-consolidated-guidelines/32-phase-26-31-rollup.md) §4 — R3 deliverable definition.

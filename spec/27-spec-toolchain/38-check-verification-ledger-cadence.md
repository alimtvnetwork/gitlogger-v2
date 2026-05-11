# Slot 38 — `check-verification-ledger-cadence.py` (gate #21)

> **Status:** Active (Sess-63 A-53)
> **Owner:** §27 spec-toolchain · **Beneficiary:** §25 app-issues invariant 5
> **Wired:** `.github/workflows/spec-health.yml` step "§25 verification ledger cadence gate"

## What it does

**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->

Mechanically enforces the §25 `02-consolidated-audit-findings/00-overview.md`
**invariant 5** verification-cadence rule (A-46 Sess-56): every spec-improvement
session that does NOT materially edit a `Carried-open` row MUST append a row
to the **Verification cadence ledger** with a sweep session id (`Sess-NN`)
that is at most `--tolerance` (default 1) sessions behind `--current-session`.

Without this gate the rule is contract-only: the latent failure mode is that
the ledger silently drifts and §27 gate #13 D5 (`cohort-orphaned-finding`)
fires next session for all 8 Carried-open rows simultaneously, with no PR-time
warning.

## Contract

| Aspect | Value |
|---|---|
| Script | `linter-scripts/check-verification-ledger-cadence.py` |
| Default ledger | `spec/25-app-issues/02-consolidated-audit-findings/00-overview.md` |
| Sentinel | `**Verification cadence ledger.**` (paragraph header) |
| Parser | Markdown table immediately after sentinel; first column matched against `Sess-(\d+)` |
| Pass criterion | `current_session - max(sweep_sessions) <= tolerance` |
| Default tolerance | `1` |

## Exit codes (per §27 §00 A-31 shared exit-code contract)

| Code | Meaning |
|---|---|
| `0` | Cadence honored (latest sweep within tolerance window) |
| `1` | Cadence violation (ledger stale; sweep row required) |
| `2` | Bad CLI invocation (missing `--current-session`) |
| `3` | Harness setup error (file unreadable, sentinel missing, no Sess-NN rows) |

## Invocations

```
# Live CI gate (CURRENT_SESSION env-injected each session)
python3 linter-scripts/check-verification-ledger-cadence.py \
  --current-session 63

# Self-test (5 in-memory fixtures: pass-same, pass-1-behind, fail-2-behind,
# multi-row-takes-latest, missing-sentinel-error)
python3 linter-scripts/check-verification-ledger-cadence.py --self-test
```

## Self-test fixtures (R5 vacuously-passing-scanner clause)

A scanner that returns 0 because it found nothing to inspect is itself a
fail. The five built-in fixtures cover:

| Fixture | Asserts |
|---|---|
| `pass-same-session` | Latest sweep == current session → exit 0 |
| `pass-1-behind` | Latest sweep == current - 1 → exit 0 (boundary) |
| `fail-2-behind` | Latest sweep == current - 2 → exit 1 (cadence violation) |
| `pass-multi-rows-takes-latest` | Multiple rows; uses `max(sweeps)` not `last` row |
| `setup-error-missing-sentinel` | Sentinel absent → exit 3 (not silent pass) |

## Self-enforcement chain (5 links)

1. **Source-of-truth pin** — §25 `02-consolidated-audit-findings/00-overview.md`
   invariant 5 paragraph + ledger table.
2. **Rule pin** — §25 §98 v1.6.0 changelog entry (Sess-56 A-46) defining the
   cadence requirement.
3. **State pin** — `Last touched` column on each Carried-open F-NN row
   (verification sweep bumps it).
4. **Existing-gate pin** — §27 gate #13 D5 (`cohort-orphaned-finding`) consumes
   the `Last touched` state and fires backlog warnings.
5. **CI-gate pin (THIS SLOT)** — gate #21 evaluates the ledger directly at PR
   time, surfacing drift before D5 fires.

## Invalidation triggers

- Sentinel string `**Verification cadence ledger.**` renamed without script update.
- Ledger table format changed (e.g. column order) breaking the first-cell parser.
- `CURRENT_SESSION` env var not bumped each session → gate goes silently green
  when it should fail (mitigation: workflow comment requires hand-bump).
- §25 invariant 5 weakened or removed → revert this slot.

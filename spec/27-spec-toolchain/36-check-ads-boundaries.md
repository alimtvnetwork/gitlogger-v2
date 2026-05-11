# 36 — check-ads-boundaries.py

**Version:** 1.0.0
**Updated:** 2026-05-10 (Session 55 audit-task A-43 — slot promotion of Sess-55 A-42 fixture-shipped scanner; first §27 gate dedicated to a §24-side AC family.)
**Source:** [`linter-scripts/check-ads-boundaries.py`](../../linter-scripts/check-ads-boundaries.py)
**Self-test:** `python3 linter-scripts/check-ads-boundaries.py --self-test` (built-in; no separate `.sh` wrapper needed — three negative-fixture corpora live under `linter-scripts/fixtures/`)
**Category:** Validator (read-only)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Slot-range note

Slot **36** sits in the 30-39 auditor band, but `check-ads-boundaries.py` is a deterministic read-only validator (not AI-driven). Same precedent as slots 32/33 (validators in non-validator bands per the Phase 31 lockstep). Future contributors MUST NOT "correct" the band.

---

## Purpose

Mechanizes the three §24 design-system boundary contracts established by §24 §97 AC-ADS-06 / AC-ADS-09 / AC-ADS-10 (test invariant blocks added by Sess-55 A-41, fixture-shipped by Sess-55 A-42). Promotes them from contract-proven (prose) to **CI-enforced (load-proven)**.

Each AC's contract:

| AC | Boundary enforced | Forbidden pattern |
|---|---|---|
| AC-ADS-06 | Marketing routes MUST NOT import `AppShell` | `from "src/components/app/AppShell"` inside `pages/(marketing)/**` |
| AC-ADS-09 | `src/components/ui/**` ∩ `src/components/app/**` basenames MUST be empty | Same component name living in both §07 and §24 territories |
| AC-ADS-10 | `--app-status-*` MUST NOT appear under `src/components/ui/**` | `var(--app-status-*)` referenced from §07 primitive code |

---

## Inputs

- `pages/(marketing)/**/*.{ts,tsx}` (AC-ADS-06 scan target)
- `src/components/ui/**/*.tsx` and `src/components/app/**/*.tsx` (AC-ADS-09 set-intersection)
- `src/components/ui/**/*.{tsx,ts,css,scss}` (AC-ADS-10 grep target)
- Three negative-fixture corpora under `linter-scripts/fixtures/`:
  - `marketing-appshell-violation/`
  - `ownership-matrix-collision/`
  - `status-token-leak/`

## Usage

```bash
# Full sweep (recommended in CI)
python3 linter-scripts/check-ads-boundaries.py --check all

# Single-AC sweep
python3 linter-scripts/check-ads-boundaries.py --check ac-ads-06
python3 linter-scripts/check-ads-boundaries.py --check ac-ads-09
python3 linter-scripts/check-ads-boundaries.py --check ac-ads-10

# Self-test (asserts every fixture is rejected)
python3 linter-scripts/check-ads-boundaries.py --self-test
```

`--root <path>` overrides the default project root (used by self-test to point at fixture directories).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | All checks pass (no violations) |
| 1 | At least one violation; per-line `ADS-NN-VIOLATION:` message on stderr |
| 2 | Harness/usage error (bad flag, missing root) |

Exit code 2 is reserved for harness errors per the §27 R3 resilience contract (does NOT block merge unless CI policy escalates). Exit code 1 is the merge-blocking signal.

## Self-test contract (R5 — vacuously-passing scanner is an auto-fail)

Every gate that uses a regex/AST scan MUST ship at least one negative fixture proving the scan rejects synthetic violations. `check-ads-boundaries.py --self-test` runs each AC's check against its hostile fixture and asserts non-zero exit. If any fixture passes (rc=0), the harness exits 1 with `SELF-TEST FAIL: <check> accepted hostile fixture <path>`.

Smoke-tested 2026-05-10 Sess-55 A-42: all three fixtures correctly rejected.

## CI invocation

Wired into `.github/workflows/spec-health.yml` as a hard-fail gate (this slot is **§27 §00 gate #19**). Step name: `check-ads-boundaries`. Runs `--check all` followed by `--self-test`; both must exit 0.

## Cross-references

- §24 §97 AC-ADS-06 / AC-ADS-09 / AC-ADS-10 (the three contracts this script enforces)
- §24 §97 AC-ADS-15 T-05 (boundary regex precedent)
- §24 §97 AC-ADS-16 (dependency boundary; this gate is the runtime peer of AC-ADS-16's static rules)
- §27 §00 "CI Gate Enumeration" — gate #19
- §27 §97 AC-T-43 (this slot's GWT)
- `linter-scripts/fixtures/{marketing-appshell-violation,ownership-matrix-collision,status-token-leak}/README.md`

## Lockstep history

| Version | Date | Phase | Change |
|---|---|---|---|
| 1.0.0 | 2026-05-10 | Sess-55 A-43 | Slot promotion of A-42 fixture-shipped scanner. First §27 gate dedicated to §24-side AC family. CI workflow row landed same PR. |

# 35 — `audit-bundle-budget.py` (Walker Bundle Budget Audit)

**Version:** 1.0.0  
**Updated:** 2026-05-01 (Phase 153 Task A24-fu32 — productionised from `/tmp/a24-fu27-bundle-budget.py`)  
**Slot:** 35 (auditor band 30-39 — next available after slot 34 `audit-ai-implementability.py`)  
**Code artifact:** `linter-scripts/audit-bundle-budget.py`  
**Self-test:** `linter-scripts/test/test-audit-bundle-budget.sh` (10 assertions)

## Purpose

Deterministic, zero-network audit that enumerates which modules are at risk of being silently truncated by the LLM auditor in slot 34 (`audit-ai-implementability.py`). The slot-34 walker concatenates files until `MAX_BYTES` (currently 120 KB ≈ Cloudflare-1010 ceiling per AC-34-13) is hit; once exceeded, all remaining files are invisible to the LLM regardless of contract content. Slot 35 surfaces this physics deterministically so OVER-class regressions are caught the next CI run, not the next quarterly rebaseline.

## Origin

Phase 153 Task A24-fu27 ran a one-off ephemeral script (`/tmp/a24-fu27-bundle-budget.py`) that surfaced the OVER class (4 modules: spec/01/07/22/27) and produced **Lesson #65** ("structural surgery > pure-promotion"). The fu28→fu31 sweep then mechanically closed the OVER class via §98 archive splits. Phase 153 Task A24-fu32 productionises the script as a permanent CI gate so the gain is regression-protected.

## CLI surface

```
audit-bundle-budget.py [--json] [--report PATH] [--strict]
```

- (default) — print human-readable markdown report to stdout; exit 0.
- `--json` — emit machine-readable JSON `{cap, counts, modules}` to stdout.
- `--report PATH` — write markdown report to PATH (in addition to stdout).
- `--strict` — exit 1 if any module is OVER (use as graduating CI gate after the OVER class hits 0).

## Classification (Normative)

For each top-level `spec/NN-*/` module:

- `tier1` = sum of `00-*.md` + `97-*.md` + `98-*.md` + `99-*.md` byte sizes (always loaded by slot-34 tier-1 walker per AC-34-09).
- `siblings` = sum of `01-*.md` through `96-*.md` byte sizes (loaded after tier-1 if budget allows).
- `headroom` = `max(0, cap − §00 − §97)` — bytes available for siblings before §97 itself is forced past cap.

| Status | Rule | Meaning |
|---|---|---|
| **CLEAR** | `tier1 ≤ cap AND siblings ≤ headroom` | Auditor sees full bundle; pure §97 quality work translates 1:1 to score. |
| **AT_CEILING** | `tier1 ≤ cap AND siblings > headroom` | Pure-promotion teasers (Lesson #55) ineffective per Lesson #64. Sibling extraction is the only lever. |
| **OVER** | `tier1 > cap` | STRUCTURAL EMERGENCY (Lesson #65). Apply §98 archive split (precedent: fu28-fu31) or §97 sub-folder extraction. |

## Anti-drift contract

`MAX_BYTES` MUST be read from `linter-scripts/audit-ai-implementability.py:45` at runtime, never duplicated as a constant in slot 35. Verifies AC-34-13 SemVer-locked single source of truth (Lesson #36 — link, never restate).

## Acceptance Criteria

### AC-35-01: Cap source-of-truth is slot 34 [critical]

**Given** `audit-ai-implementability.py` declares `MAX_BYTES = N` at module scope  
**When** `audit-bundle-budget.py` runs  
**Then** the cap reported in `--json` output (`cap` field) MUST equal N exactly (no hard-coded fallback unless slot 34 file is missing)  
**Verifies:** §00 anti-drift contract — slot 35 reads slot 34's `MAX_BYTES` per Lesson #36 (link, never restate)

### AC-35-02: Status classification is deterministic [critical]

**Given** a module with `tier1` bytes and `siblings` bytes  
**When** classified  
**Then** status MUST be exactly one of `{CLEAR, AT_CEILING, OVER}` per the rule table above; multiple invocations on byte-identical input MUST produce byte-identical JSON output.  
**Verifies:** §00 Classification table

### AC-35-03: Strict mode fails on OVER [high]

**Given** `--strict` is passed  
**When** any module has status `OVER`  
**Then** exit code MUST be 1 and a `FAIL:` line MUST be written to stderr.  
**When** all modules are `CLEAR` or `AT_CEILING`  
**Then** exit code MUST be 0.  
**Verifies:** §00 CLI surface — graduating-gate contract

### AC-35-04: Default mode is advisory [high]

**Given** no `--strict` flag  
**When** any number of OVER modules exist  
**Then** exit code MUST be 0 (does not fail CI by default).  
**Verifies:** §00 CLI surface — advisory-by-default per Lesson #15 (CI gates that surface real but non-blocking work MUST default to advisory).

### AC-35-05: Self-test parity [high]

**Given** the production script ships  
**When** `linter-scripts/test/test-audit-bundle-budget.sh` runs  
**Then** all 10 assertions (T1-T9) MUST pass.  
**Verifies:** §00 self-test reference

## Verifies (rollup)

- AC-31-31 (single-source slot inventory)
- AC-34-09 (slot 34 tier-1 walker ordering — slot 35 mirrors this physics)
- AC-34-13 (slot 34 `MAX_BYTES = 120_000` Cloudflare-safe ceiling — slot 35 reads it without restating)
- Lesson #65 (structural surgery > pure-promotion) — slot 35 makes the lesson mechanically enforceable

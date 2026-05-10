# 52 — check-axios-version.sh

**Version:** 1.1.0  
**Updated:** 2026-05-10 (Sess-66 G-6t — added `--self-test` mode + `--pkg <path>` flag; wired into spec-health.yml as **gate #46** with both --self-test and live disk run; six fixtures lock AC-52-01/02/03 + vacuous-pass anchor; phantom 7 → 6)  
**Source:** [`linter-scripts/check-axios-version.sh`](../../linter-scripts/check-axios-version.sh)  
**Category:** Source validator  
**Status:** Active gate #46 (load-proven via `--self-test` 6/6 fixtures + live disk run on repo `package.json`)

---

## Purpose

Validate that Axios is pinned to an approved safe version in `package.json` and not using any range symbols (`^`, `~`, `>=`, `*`).

## Policy

| Approved | Blocked |
|----------|---------|
| `1.14.0` | `1.14.1` |
| `0.30.3` | `0.30.4` |

Range specifiers (`^1.14.0`, `~0.30.3`, `>=1.14.0`, `*`) are ALL forbidden — only exact pins are allowed.

## Usage

```bash
bash linter-scripts/check-axios-version.sh
```

## CLI flags

_(none)_

## Inputs

`package.json` at repo root.

## Exit codes

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

| Code | Meaning |
|------|---------|
| `0` | pass — axios pinned to an approved exact version OR axios not declared (vacuous-pass) |
| `1` | violation — blocked version, range symbol, or unknown exact version |
| `2` | invocation error — unknown CLI flag |
| `3` | fixture-rot — `--self-test` self-check inconsistency (reserved) |

## R5 — vacuously-passing scanner is auto-fail

`vacuous-pass:` a bare disk run on a repo without `axios` declared returns `0` with no enforcement. To prevent this from masking a fixture-rot regression, gate #46 in `.github/workflows/spec-health.yml` ALWAYS runs `--self-test` first (six fixtures including the F-6 vacuous-pass anchor itself), and only then the live disk run.

## Self-test fixtures (Sess-66 G-6t)

`--self-test` exercises six in-memory `package.json` fixtures via `mktemp -d`:

- **F-1** AC-52-01 — `"axios": "^1.14.0"` (range) → MUST exit `1`
- **F-2** AC-52-02 — `"axios": "1.14.1"` (blocked) → MUST exit `1`
- **F-3** AC-52-03 — `"axios": "1.14.0"` (approved) → MUST exit `0`
- **F-4** AC-52-03 — `"axios": "0.30.3"` (approved, devDep path) → MUST exit `0`
- **F-5** AC-52-02 — `"axios": "0.30.4"` (blocked) → MUST exit `1`
- **F-6** R5 vacuous-pass — axios absent → MUST exit `0`


## Acceptance criteria

### AC-52-01 — Range symbol fails
- **Given** `"axios": "^1.14.0"`,
- **When** the script runs,
- **Then** it MUST exit `1`.

### AC-52-02 — Blocked exact version fails
- **Given** `"axios": "1.14.1"`,
- **When** the script runs,
- **Then** it MUST exit `1`.

### AC-52-03 — Approved exact version passes
- **Given** `"axios": "1.14.0"`,
- **When** the script runs,
- **Then** it MUST exit `0`.

### AC-52-04 — Approved + blocked lists are kept in sync with the spec
- **Given** [`spec/02-coding-guidelines/11-security/01-axios-version-control/`](../02-coding-guidelines/11-security/01-axios-version-control/),
- **When** the policy changes,
- **Then** both that spec and the BLOCKED_VERSIONS / APPROVED_VERSIONS arrays in this script MUST be updated together.

## Cross-references

- [`spec/02-coding-guidelines/11-security/01-axios-version-control/`](../02-coding-guidelines/11-security/01-axios-version-control/) — policy source.

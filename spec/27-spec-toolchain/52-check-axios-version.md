# 52 — check-axios-version.sh

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-axios-version.sh`](../../linter-scripts/check-axios-version.sh)  
**Category:** Source validator

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

| Code | Meaning |
|------|---------|
| 0 | Axios pinned to an approved exact version |
| 1 | Axios pinned to a blocked version OR uses a range symbol OR not present when expected |

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

# 02 — check-spec-folder-refs.py

**Version:** 1.0.0  
**Updated:** 2026-04-25  
**Source:** [`linter-scripts/check-spec-folder-refs.py`](../../linter-scripts/check-spec-folder-refs.py)  
**Category:** Validator (read-only)

---

## Purpose

Reject prose references to numbered spec folders (`spec/12-cicd-pipeline-workflows/`) that do not exist on disk and are not allowlisted. Catches stale references after a folder rename or merge.

## Usage

```bash
python3 linter-scripts/check-spec-folder-refs.py
```

## CLI flags

_(none)_

## Inputs

- Every `*.md` under `spec/` and `readme.md` at repo root.
- [`linter-scripts/spec-folder-refs.allowlist`](../../linter-scripts/spec-folder-refs.allowlist) with two sections: `[external]` and `[doc-only]`.

## Outputs

Human report on stderr listing each stale reference with the nearest fuzzy-matched real folder when one is plausible.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Every numbered-folder reference resolves OR is allowlisted |
| 1 | At least one stale reference |
| 2 | Allowlist file malformed (missing required section header) |

## Acceptance criteria

### AC-02-01 — Stale folder reference is detected
- **Given** a markdown file referencing `spec/99-nonexistent/`,
- **When** the script runs and `99-nonexistent/` is on disk in neither category nor in the allowlist,
- **Then** it MUST exit `1`.

### AC-02-02 — Fuzzy suggestion when close match exists
- **Given** a reference to `spec/12-cicd-pipelines/` and the real folder is `spec/12-cicd-pipeline-workflows/`,
- **When** the script reports the failure,
- **Then** the message MUST include the suggested real folder.

### AC-02-03 — `[external]` and `[doc-only]` allowlist sections behave differently
- **Given** an entry under `[external]`,
- **When** the same reference appears in prose,
- **Then** it MUST pass; entries under `[doc-only]` MUST also pass but MUST NOT be linkified (enforced by §01).

## Cross-references

- §62 [`62-spec-folder-refs-allowlist.md`](./62-spec-folder-refs-allowlist.md) — allowlist format.

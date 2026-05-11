# 60 — forbidden-strings.toml

**Version:** 2.0.1
**Updated:** 2026-05-07
**Source:** [`linter-scripts/forbidden-strings.toml`](../../linter-scripts/forbidden-strings.toml)
**Category:** Configuration (consumed by §03)


**Test pair:** N/A — convention  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

TOML config defining forbidden patterns and per-pattern allowlists for §03 [`check-forbidden-strings.py`](./03-check-forbidden-strings.md). Each `[[rule]]` defines a regex pattern that MUST NOT appear in the repository (outside of excluded dirs and allowlisted paths).

## Schema (Normative — matches actual file)

```toml
[[rule]]
id            = "STALE-REPO-SLUG"                 # required, unique short identifier
description   = "Pre-renumber repo slug ..."     # required, human-readable explanation
pattern       = 'coding-guidelines-v(1[0-4]|[1-9])\b'  # required, ERE/Python re syntax
fix_hint      = "grep -rlE '$PATTERN' . | xargs sed -i ..."  # required, suggested bulk-fix command
exclude_dirs  = ["release-artifacts"]            # optional, dirs to skip entirely (always-skipped: .git, node_modules, dist, build)
exclude_files = ["forbidden-strings.toml", "check-forbidden-strings.py"]  # optional, glob patterns
allowlist     = [                                # optional, repo-relative paths/globs that may legitimately contain the pattern
  "spec/06-seedable-config-architecture/97-changelog.md",
  "CHANGELOG.md",
]
```

**Field contract:**

| Field | Required | Type | Default | Notes |
|-------|----------|------|---------|-------|
| `id`            | yes | string  | — | unique across all rules |
| `description`   | yes | string  | — | shown in failure output |
| `pattern`       | yes | string  | — | Python `re` syntax |
| `fix_hint`      | yes | string  | — | shown on failure (literal `$PATTERN` replaced with `pattern`) |
| `exclude_dirs`  | no  | list[str] | `[]` | combined with always-skipped `{.git, node_modules, dist, build}` |
| `exclude_files` | no  | list[str] | `[]` | `fnmatch`-style globs against basename |
| `allowlist`     | no  | list[str] | `[]` | `fnmatch`-style globs against repo-relative path |

There is no top-level `[scan]` table — include/exclude scope is implicit (full repo minus `ALWAYS_EXCLUDE_DIRS` and per-rule excludes).

## Acceptance criteria

### AC-60-01 — File parses as valid TOML  `[critical]`
- **Given** the file `linter-scripts/forbidden-strings.toml`,
- **When** loaded with `tomllib.load()`,
- **Then** parsing MUST succeed (no `tomllib.TOMLDecodeError`).
- **Verifies:** §60 schema (this file) + `linter-scripts/check-forbidden-strings.py` `load_config()`.

### AC-60-02 — Each `[[rule]]` has required keys  `[critical]`
- **Given** any `[[rule]]` entry in the parsed config,
- **When** the entry is read,
- **Then** it MUST contain ALL of: `id`, `description`, `pattern`, `fix_hint`. Optional keys: `exclude_dirs`, `exclude_files`, `allowlist` (each defaulting to `[]` when absent).
- **Verifies:** §60 schema field contract above + script `load_config()` rule shape.

### AC-60-03 — `id` is unique across all rules  `[critical]`
- **Given** the full config,
- **When** all rule `id` values are collected into a list,
- **Then** there MUST be no duplicates (`len(ids) == len(set(ids))`).
- **Verifies:** §60 schema (this file).

### AC-60-04 — `pattern` compiles as a valid Python regex  `[critical]`
- **Given** any rule,
- **When** `re.compile(rule["pattern"])` is invoked,
- **Then** compilation MUST succeed (no `re.error`).
- **Verifies:** §60 schema + script regex consumption.

### AC-60-05 — Schema/spec drift guard  `[critical]`  *(new in v2.0.0, Phase G1)*
- **Given** this §60 file (`60-forbidden-strings-toml.md`) and the live config (`linter-scripts/forbidden-strings.toml`),
- **When** the schema fence in `## Schema (Normative — matches actual file)` is parsed,
- **Then** the documented top-level table name MUST equal the actual table name in the TOML (`rule`); AND the documented required-key set MUST equal `{id, description, pattern, fix_hint}`; AND the documented optional-key set MUST equal `{exclude_dirs, exclude_files, allowlist}`. Drift between this spec and the live TOML is FORBIDDEN — when the script's `load_config()` shape changes, BOTH this file (banner minor-bump) AND `linter-scripts/forbidden-strings.toml` MUST be updated in the same commit, with a §98 changelog row.
- **Verifies:** §60 schema field contract; closes the Phase G1 dual-source drift class (mirror of Lesson #36 — single source of truth between docs + config).
- **Why:** Pre-G1 §60 documented `[[patterns]]` + `regex` field while the actual TOML used `[[rule]]` + `pattern`/`fix_hint`. AC-60-02/03/04 would have failed validation against the real file. This AC formalises the link.

## Cross-references

- §03 [`03-check-forbidden-strings.md`](./03-check-forbidden-strings.md) — consumer script.
- §97 inventory row uses prefix `AC-60-*` (was `AC-FST-*` pre-G1 — see §97 row 349).

## Changelog

- **v2.0.0 (2026-05-07, Phase G1)** — Schema fence rewritten to match actual TOML (`[[rule]]` not `[[patterns]]`; `pattern`/`fix_hint`/`exclude_dirs`/`exclude_files` not `regex`+`[scan]`). AC-60-02/04 fixed to reference real keys. AC-60-05 added as drift guard. Major bump because schema contract changed.
- **v1.0.0 (2026-04-25)** — Initial.

# 62 — spec-folder-refs.allowlist

**Version:** 1.3.0  
**Updated:** 2026-04-28 (Phase F4: bind Phase 144 sanctioned `.py` regression test `linter-scripts/test/test-check-spec-folder-refs.py` to AC-62-05 — closes spec-vs-code gap where the test existed on disk + in `linter-scripts/test/README.md` "Adjacent" subsection but was unreferenced from any §27 slot.)  
**Source:** [`linter-scripts/spec-folder-refs.allowlist`](../../linter-scripts/spec-folder-refs.allowlist)  
**Category:** Configuration (consumed by §02)

---

## Purpose

Two-section allowlist consumed by §02 [`check-spec-folder-refs.py`](./02-check-spec-folder-refs.md).

## Format

```ini
[external]
# Real folders that live in a sibling repository.
# References are valid; we just don't host them here.
spec/30-cross-repo-foo/
spec/31-cross-repo-bar/

[doc-only]
# Illustrative / historical names. They do NOT exist anywhere.
# They are prose only and MUST NEVER become live links.
spec/14-generic-update/
spec/15-self-update-app-update/
```

## Section semantics

| Section | Allowed in prose? | Allowed as a markdown link? |
|---------|:-----------------:|:---------------------------:|
| `[external]` | yes | yes (linked to sibling repo URL) |
| `[doc-only]` | yes | NO — doc-only entries MUST NEVER be linkified |

## Acceptance criteria

### AC-62-01 — Both section headers are required
- **Given** the file is missing `[external]` OR `[doc-only]`,
- **When** §02 loads it,
- **Then** §02 MUST exit `2` (structural error).

### AC-62-02 — Doc-only entries are not linkified
- **Given** an entry under `[doc-only]`,
- **When** §01 (link validator) sees a markdown link of the form `[x]` followed by `(spec/<entry>)`,
- **Then** §01 MUST report it as broken (this allowlist does NOT cover §01).

### AC-62-03 — External entries pass §02
- **Given** an entry under `[external]`,
- **When** the same path appears in prose,
- **Then** §02 MUST NOT report it stale.

### AC-62-04 — Inline comments on entry lines are forbidden (Phase 143)
- **Given** a non-blank, non-section-header line in this allowlist,
- **When** the line contains a `#` after the folder name (i.e. an inline trailing comment like `04-some-feature  # narrative example`),
- **Then** the entry IS BROKEN — `check-spec-folder-refs.py:128` (`buckets[current].add(line.strip())`) stores the entire string including the `#` and trailing comment, so the resulting bucket entry never matches the bare folder name. Documentation MUST go in a **separate `#`-prefixed comment line ABOVE** the entry. Phase 143 discovered this empirically: the first allowlist write attempt used inline trailers and the stale-refs count did not drop until the comments were moved above.
- **Verifies:** `linter-scripts/spec-folder-refs.allowlist` (Phase 143 v1.1.0 entries follow this rule); `linter-scripts/check-spec-folder-refs.py:128` (parser line that mandates the rule); `linter-scripts/test/test-check-spec-folder-refs.py` (Phase 144 regression test — see AC-62-05).

### AC-62-05 — Sanctioned `.py` regression test locks AC-62-04 (Phase 144 / F4)
- **Given** [`linter-scripts/test/test-check-spec-folder-refs.py`](../../linter-scripts/test/test-check-spec-folder-refs.py) exists as the sanctioned `.py` exception under the F3 test-discovery policy (exercises an internal function — `load_allowlist()` — of the hyphenated `.py` source `check-spec-folder-refs.py` via `importlib`, which is the SOLE F3-sanctioned reason for a `.py` self-test alongside the default `.sh` discipline),
- **When** the test runs (`python3 linter-scripts/test/test-check-spec-folder-refs.py`),
- **Then** it MUST exit 0 with all four `tempfile`-based cases passing: (1) plain-entry routing into `[external]`/`[doc-only]` buckets, (2) AC-62-04 inline-comment strip on entry lines, (3) whitespace-then-comment edge case (`folder/   #trailer`), (4) `[doc-only]` bucket isolation from `[external]`; AND the test MUST be listed in `linter-scripts/test/README.md` "Adjacent `.py` tests (acknowledged, not parity-gated)" subsection (NOT the main inventory table — the `.sh`-only parity gate `test-readme-inventory.sh` does not enforce it); AND the test MUST NOT appear in `spec/27-spec-toolchain/00-overview.md` inventory tables (which enumerate production `linter-scripts/*` artifacts only — `linter-scripts/test/` is excluded by `test-overview-inventory-parity.sh`'s scope rule).
- **Verifies:** AC-62-04 (the rule this test locks); `linter-scripts/test/README.md` Adjacent subsection (Phase F3); `linter-scripts/test/test-overview-inventory-parity.sh` scope-exclusion of `linter-scripts/test/` (which is why this `.py` test does not need a §27 slot of its own); F3 sanctioned-exception policy (`mem://index.md` Core test-file rule).

## Cross-references

- §02 [`02-check-spec-folder-refs.md`](./02-check-spec-folder-refs.md) — consumer.
- §01 [`01-check-spec-cross-links.md`](./01-check-spec-cross-links.md) — separate concern (link resolution).
- [`linter-scripts/test/test-check-spec-folder-refs.py`](../../linter-scripts/test/test-check-spec-folder-refs.py) — Phase 144 regression test, locks AC-62-04 + AC-62-05.

## Changelog

### 1.3.0 — 2026-04-28 — Phase F4: bind Phase 144 `.py` regression test to AC-62-05
- Added AC-62-05 codifying the four-case contract of `linter-scripts/test/test-check-spec-folder-refs.py` (the sanctioned F3 `.py` exception that locks AC-62-04). Closes the spec-vs-code gap discovered while auditing `linter-scripts/test/` coverage: the test existed on disk + in the README "Adjacent" subsection but was unreferenced from any §27 slot, so a contributor reading the spec alone could not discover it.
- Extended AC-62-04's `**Verifies:**` clause with the new test reference so the bidirectional spec↔test link is intact.
- Added the test to the `## Cross-references` block.
- No code change. Pure spec lockstep — the test itself is unchanged from Phase 144.

### 1.1.0 — 2026-04-28 — Phase 143: bulk-classify 13 documentation/historical refs
- Added 13 entries under `[doc-only]` covering: 4 narrative-example folder names (`04-some-feature`, `30-cross-repo-foo`, `31-cross-repo-bar`, `99-nonexistent` — all used as deliberate fake paths inside §27 spec GWT bodies and audit-memo prose), 4 archived/historical folder names (`21-git-logs`, `21-git-logs-v1`, `22-app-issues`, `29-app-issues-cli` — historical references in `_archive/`, audit memos, and full-tree audit-v4 memo), and 3 deprecated/typo-example folder names used as deliberate negative examples in §27 linter specs (`12-cicd-pipelines` typo, `14-generic-update` and `15-self-update-app-update` deprecated pre-consolidation).
- Result: stale-refs count dropped from 29 → **11** (-62%). Remaining 11 refs across 6 unique missing targets (`08-docs-viewer-ui`, `09-code-block-system`, `21-app`, plus a few in `01-spec-authoring-guide`, `07-design-system`, `17-consolidated-guidelines`) require user intent classification — defer under Phase F.
- **Format note (caught during Phase 143 implementation):** the allowlist parser at `check-spec-folder-refs.py:128` does `buckets[current].add(line)` on the stripped line — inline `# comment` suffixes on entry lines are NOT stripped and corrupt the bucket. Phase 143 documents intent in **separate full-line comments above the entries**, not as inline trailers. AC-62-04 added to enforce this.

### 1.0.0 — 2026-04-25
- Initial version. Two-section format `[external]` + `[doc-only]`.

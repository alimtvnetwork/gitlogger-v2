# 61 — spec-cross-links.allowlist

**Version:** 1.1.0  
**Updated:** 2026-04-28 (Phase P39: bind P37 surface-survey lesson — AC-61-04 codifies that this file's `<relpath>:<line>:<target>` format is the SOLE line-keyed allowlist tree-wide and any future line-keyed waiver MUST inherit the P35 fuzzy-match contract.)  
**Source:** [`linter-scripts/spec-cross-links.allowlist`](../../linter-scripts/spec-cross-links.allowlist)  
**Category:** Configuration (consumed by §01)


**Test pair:** N/A — convention  <!-- AC-T-41 closed-set axis-class stub -->
---

## Purpose

Suppression list for known broken-link exceptions consumed by §01 [`check-spec-cross-links.py`](./01-check-spec-cross-links.md). Each entry is one path+anchor that the validator should ignore.

## Format

- One entry per line.
- Lines beginning with `#` are comments.
- Blank lines are ignored.
- Entries match the literal `target` string of a markdown link of the form `[x]` followed by `(target)` — no globbing.

```
# Example
spec/_archive/old-doc.md
spec/21-git-logs/00-overview.md#renamed-section
```

## Policy

Adding a new entry MUST be accompanied by a §99 audit row in the relevant module explaining the temporary suppression and the planned fix.

## Acceptance criteria

### AC-61-01 — Comment lines are ignored
- **Given** a line starting with `#`,
- **When** §01 loads the allowlist,
- **Then** that line MUST NOT match any link.

### AC-61-02 — Entries are exact-match
- **Given** an entry `spec/x.md`,
- **When** a link points to `./spec/x.md`,
- **Then** it MUST NOT be considered allowlisted (relative-vs-absolute mismatch); both forms must be normalised before comparison by §01.

### AC-61-03 — File is UTF-8
- **Given** the allowlist,
- **When** read,
- **Then** decoding as UTF-8 MUST succeed.

### AC-61-04 — Line-keyed waiver formats MUST inherit the P35 fuzzy-match contract (Phase P39)
- **Given** this file's `<relpath>:<line>:<target>` triple format embeds a 1-indexed source-line number as a discriminator,
- **And** Phase P37's surface-survey verified this is the **SOLE line-keyed allowlist** tree-wide (`spec-folder-refs.allowlist` is path-only, `forbidden-strings.toml` is regex-keyed, `trace-map.toml` is symbol-keyed) — confirmed by `grep -l ':[0-9]'` over `linter-scripts/*.allowlist linter-scripts/*.toml`,
- **And** Phase P34 caught a CI-silent regression where unrelated stamp-batch sweeps (P22/P32 inserting `<!-- h10-verified-phase: NN -->` comment lines into §00 banners) shifted every per-link waiver below the insertion by +N, drifting two waivers off-by-one,
- **When** any future contributor introduces a NEW line-keyed waiver format (i.e. an allowlist that embeds `:<line>:` or any other source-position token as a match discriminator) anywhere under `linter-scripts/`,
- **Then** that new format MUST inherit the P35 fuzzy-match drift-resistance contract: (1) default tolerance window of ±5 lines around the recorded line number; (2) `--rewrite-allowlist` flag that idempotently bumps stale line numbers in-place when the target is found within the tolerance window; (3) `--strict-line-match` opt-in flag that disables fuzzy matching for callers that need exact-line semantics; (4) the consuming linter's spec slot MUST add ACs equivalent to §01 AC-01-05/06/07 contracting these three behaviours; (5) a self-test under `linter-scripts/test/test-<consumer>.sh` MUST cover all three behaviours per the F3 `.sh`-default policy.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` (the reference implementation, slot §01 v1.1.0 since Phase P35); §01 `01-check-spec-cross-links.md` AC-01-05/06/07 (the contract being mirrored); `linter-scripts/test/test-check-spec-cross-links.sh` (the reference self-test, 19 assertions since Phase P35); `mem://index.md` Core P37 entry (the surface-survey lesson that establishes this file as the sole current line-keyed surface).
- **Rationale:** absent this AC, a future contributor adding a second line-keyed allowlist would re-discover the P34 drift class the hard way (CI-silent regression visible only at next stamp-batch sweep). Codifying the contract at the slot level inverts the burden — **format authors** carry the drift-resistance requirement, not **sweep tool authors** (who would otherwise need a growing per-allowlist remediation matrix). Mirrors the established pattern of slot-level format contracts (e.g. §62 AC-62-04 inline-comment forbidden) protecting downstream consumers from parser-shape footguns.

## Cross-references

- §01 [`01-check-spec-cross-links.md`](./01-check-spec-cross-links.md) — consumer; reference implementation of the AC-61-04 P35 fuzzy-match contract (AC-01-05/06/07).
- [`linter-scripts/test/test-check-spec-cross-links.sh`](../../linter-scripts/test/test-check-spec-cross-links.sh) — Phase P35 self-test exercising the P35 fuzzy-match contract that AC-61-04 mandates for any future line-keyed waiver format.
- §62 [`62-spec-folder-refs-allowlist.md`](./62-spec-folder-refs-allowlist.md) — sibling allowlist; confirmed PATH-ONLY (no line discriminator) per Phase P37 survey, so AC-61-04 does not apply.

## Changelog

### 1.1.0 — 2026-04-28 — Phase P39: bind P37 surface-survey lesson via AC-61-04
- Added AC-61-04 codifying the **format-author contract** for any future line-keyed waiver: must inherit the P35 fuzzy-match drift-resistance pattern (±5 tolerance + `--rewrite-allowlist` + `--strict-line-match` + spec ACs + self-test). Closes the gap between Phase P37's mem-index lesson and the slot-level spec — without this AC, a future contributor introducing a new `:line:` format would have no spec-level signal that drift-resistance is mandatory.
- Updated `## Cross-references` block to add §01 reference-implementation + §62 sibling-confirmation + test self-test pointer.
- Pure spec lockstep — no script change. The P35 reference implementation already ships the contract; this AC binds future contributors to mirror it.

### 1.0.0 — 2026-04-25
- Initial version. Three ACs (comment-ignore, exact-match, UTF-8).

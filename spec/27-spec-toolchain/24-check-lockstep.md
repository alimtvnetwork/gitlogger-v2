---
kind: tooling-spec
---

# `check-lockstep.cjs` — Lockstep Enforcement Gate

> **Version:** 1.1.0
> **Created:** 2026-04-27
> **Updated:** 2026-04-27
> **Status:** Active (CI strict gate — Phase 41 baseline cleared, `--strict` enforced in `spec-monthly-audit.yml`)
> **Parent:** [00-overview.md](./00-overview.md)


**Test pair:** N/A — advisory  <!-- AC-T-41 closed-set axis-class stub -->
---

## Phase 41 — Strict mode flipped

The Phase 40 adoption baseline (24 modules drifted: 8 L0 / 17 L1 / 3 L2) was cleared in Phase 41 via:

- 17 stale §99 banner-date bumps (mechanical, via `/tmp/sweep-l1.cjs`).
- 5 missing §98 `Updated:` banners injected (via `/tmp/sweep-l0-banners.cjs`).
- 2 missing release rows added (`spec/98-changelog.md` v3.4.1, `spec/03-error-manage/98-changelog.md` v3.2.0 witness row).
- 2 banner additions to `14-update/24-update-check-mechanism/` §00 + §99 (canonical `Updated:` line alongside existing `Created:` / `Audit date:`).

Result: **79/79 enforced modules pass; 3 skipped (no §98/§99 by design).** The workflow flag `node linter-scripts/check-lockstep.cjs` was changed to `... --strict` in `.github/workflows/spec-monthly-audit.yml` step "Spec lockstep gate (Phase 41 — strict)".

---

## Purpose

Mechanises the Core memory rule:

> Spec edits keep these in lockstep:
> §00 banner + §98 changelog row + §99 health/inventory + queued-decisions trail.

Before Phase 40, lockstep was enforced by author discipline alone. This
script adds a deterministic gate so a banner bump without the matching
§98 entry (or a stale §99) is caught before merge.

---

## 1. Rules Implemented

| Rule | Definition | Severity |
|------|------------|----------|
| **L0** | Each of `00-overview.md`, `98-changelog.md`, `99-consistency-report.md` MUST have a parseable `Updated:` (or `Generated:`) date in the first 40 lines. | error |
| **L1** | `99-consistency-report.md.Updated` ≥ `00-overview.md.Updated`. The receipt cannot pre-date what it certifies. | error |
| **L2** | `98-changelog.md` MUST contain a release entry whose date ≥ `00-overview.md.Updated`. Banner bumps without a changelog row are forbidden. | error |
| **L3** | `98-changelog.md.Updated` ≥ `max(§00.Updated, all release dates)`. The changelog file's own banner must move when releases are added. | error |

A module is *skipped* if any of `00`, `98`, `99` is absent. Skipping is
not a pass — it's "not enforced here." The companion file-existence gate
is `check-tree-health.cjs --strict`.

---

## 2. Recognised Formats

The gate is format-tolerant to support legacy modules:

**Banner Updated line** — first 40 lines, any of:
```
**Updated:** 2026-04-27
> **Updated:** 2026-04-27
Last Updated: 2026-04-27
**Generated:** 2026-04-27
```

**Release entries** — any of:
```
### 1.2.0 — 2026-04-27
## v4.0.0 — 2026-04-26
## [4.1.0] — 2026-04-26
| 3.8.7 | 2026-04-27 | … |          ← table-row format (folder 22)
```

If a project introduces a new format, extend `releaseDates()` in the
script and add a recognized-format example here in the same commit.

---

## 3. CLI

```
node linter-scripts/check-lockstep.cjs           # warn-only, exit 0
node linter-scripts/check-lockstep.cjs --strict  # fail on any drift, exit 1
node linter-scripts/check-lockstep.cjs --json    # machine output
```

Strict mode is the CI gate. Warn-only is the local default so that
incremental migration does not block routine work.

---

## 4. Baseline (Phase 40 Adoption Snapshot)

At adoption, the project had **24 modules drifted** out of 82 scanned
(48 already passed, 7 reduced after format-tolerance broadening, 3 skipped):

| Rule | Count | Typical cause |
|-----:|------:|---------------|
| L0   | 8     | `98-changelog.md` lacks an `Updated:` banner line |
| L1   | 17    | §99 banner Updated date 1 day older than §00 |
| L2   | 3     | §98 has no release entry covering the latest §00 banner date |

The gate is **warn-only** until Phase 41 sweeps the baseline to zero.
After that, `--strict` will be the default in `spec-monthly-audit.yml`
and `run.sh`.

---

## 5. Acceptance Criteria

### AC-24-01: Pass for compliant module
- **Given** a module with §00, §98, §99 all dated `2026-04-27` and §98
  containing `### 1.0.0 — 2026-04-27`
- **When** `node linter-scripts/check-lockstep.cjs --strict` runs
- **Then** that module is reported `pass` and the script exits `0`.

### AC-24-02: L1 fires on stale §99
- **Given** a module with §00 dated `2026-04-27` and §99 dated `2026-04-26`
- **When** the script runs
- **Then** an L1 finding is emitted citing both dates.

### AC-24-03: L2 fires on missing changelog row
- **Given** §00 dated `2026-04-27` and §98 with latest release `2026-04-25`
- **When** the script runs
- **Then** an L2 finding is emitted.

### AC-24-04: L3 fires on stale §98 banner
- **Given** §98 banner Updated `2026-04-25` but contains release row
  dated `2026-04-27`
- **When** the script runs
- **Then** an L3 finding is emitted.

### AC-24-05: Strict mode exit code
- **Given** at least one module fails any rule
- **When** the script runs with `--strict`
- **Then** exit code is `1`.

### AC-24-06: Warn-only mode does not block
- **Given** the same baseline
- **When** the script runs without `--strict`
- **Then** exit code is `0` and the summary line begins with `⚠ WARN`.

### AC-24-07: JSON mode shape
- **Given** any run
- **When** invoked with `--json`
- **Then** stdout is a single JSON object with `summary` and `results`
  keys, where `results` contains only failing modules with `findings[]`.

### AC-24-08: Format tolerance documented
- **Given** any new release-line format introduced into a §98 file
- **When** that format is added
- **Then** §2 of this spec MUST be updated in the same commit.

---

## 6. Cross-References

- [05-check-tree-health.md](./05-check-tree-health.md) — sibling rubric gate
- [Memory: Project Memory](../../.lovable/memory/index.md) — Core lockstep rule
- [01-spec-authoring-guide/12-queued-decisions-trail.md](../01-spec-authoring-guide/12-queued-decisions-trail.md) — fourth lockstep leg

---

*check-lockstep.cjs spec — v1.0.0 — 2026-04-27*

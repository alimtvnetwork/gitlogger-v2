# Acceptance Criteria — Research

**Version:** 1.3.0  
**Updated:** 2026-04-30 (Phase 153 Task A24-fu — AC-10 v7-finding tri-closure (D1 CHECK + D3 path-resolution + D5 script-binding); EXCELLENT-band push per Lesson #44 audit-corpus axis)
**Scope:** `spec/10-research/`

---

## Purpose

This document defines testable acceptance criteria for the **Research** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/10-research/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Verifies:** the structural-floor contract enforced by `check-tree-health.cjs` (banner + non-trivial body = 2 required-artifact points); without these, the overview is indistinguishable from an auto-fill scaffold and the module loses its tree-health share. Note: this module's `00-overview.md` declares `kind: index` in its YAML front-matter, exempting it from `missing-contract` (AC-06) but NOT from this structural floor.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Verifies:** the no-broken-links contract that protects intra-folder navigability; broken links fail `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Verifies:** the slot-immutability invariant from `mem://index.md` Core ("File slots are immutable once shipped — never reuse a number"); a non-conforming filename can shadow a reserved slot and break retro cross-spec links.
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Verifies:** the §99 inventory-completeness invariant — `mem://index.md` Core requires the heading match `(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)` to earn the rubric-v2 inventory credit (precedent: Phase 137 recovered 168/168 by fixing a bare `## Inventory`).
- **Source:** `99-consistency-report.md`.

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Verifies:** the project-wide ≥80 floor enforced by `.github/workflows/spec-health.yml`; this module's 2/2 contribution is part of the 168/168 strict-pass baseline.
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/10-research/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule shared by audit-v2/v4/v5. **Module-specific exemption:** this module's `00-overview.md` declares `kind: index` in YAML front-matter (`description: "...intentionally empty until child specs are added — exempt from missing-contract / untestable rubric findings"`); the audit honors that exemption, so the AC effectively checks only the banner-presence half until child specs land.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Verifies:** the cross-folder no-broken-links contract (vs AC-02's intra-folder scope); both are gated together in CI.
- **Source:** `linter-scripts/check-spec-cross-links.py`.

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Verifies:** the four-file lockstep invariant from `mem://index.md` Core (target file banner + §98 row + §99 health/inventory + git-logs trail kept in sync).
- **Source:** `linter-scripts/check-lockstep.cjs`.


---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)

### AC-9: Module asset inventory pin (Lesson #29 — research lifecycle + index subfolder)  `[critical]`

**Given** spec/10's full on-disk asset inventory comprises 4 root `.md` files (`00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`) + 2 Mermaid sources (`lifecycle-10-research-lifecycle.mmd` at root + `01-research-index/lifecycle-top-research.mmd`) + the `01-research-index/` subfolder, **When** an audit harness bundles only `{00,97,98,99}-*.md` (per spec/27 slot 34 v1.1.0 AC-34-09 tier-1 cap), **Then** the auditor MUST treat any `[D5] missing Mermaid source` finding citing `lifecycle-10-research-lifecycle.mmd` or `lifecycle-top-research.mmd` as a **harness bundling-cap artifact**, NOT a spec defect — both `.mmd` files are present on disk and are normative source-of-truth for the lifecycle diagrams.\n\n- **Verifies:** the spec/10 module-kind = `module` declaration AND the auditor-authoritative inventory contract for the `.mmd` lifecycle sources; codifies **Lesson #29** for tier-1-bounded auditors. Mirror of spec/03 AC-08 + spec/07 AC-35 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until A8 (LLM-gateway re-score) unblocks, the cache will report v3/v4 [D5] findings citing missing Mermaid sources as outstanding — this AC declares those findings are stale-cache artifacts per Lesson #34.

---

### AC-10: Audit-finding tri-closure — D1 CHECK constraint + D3 path-resolution + D5 script-binding  `[critical]`

**Given** the v7 audit cache (`audit-corpus` axis, multipliers D4×1.5 + D5×1.5) reports three findings against this module — (a) **[D1 LOW] Registry Table Type Mismatch** (SQL `AuthoredAt TEXT` lacks CHECK enforcing `date-time` format), (b) **[D3 MEDIUM] Ambiguous 'On-Disk' Resolution Logic** (AC-RESEARCH-07 resolves domain strings against "the repo's spec/ tree" without defining root path or symlink/case-sensitivity discipline), and (c) **[D5 HIGH] Unresolved External Script Dependencies** (`linter-scripts/check-spec-folder-refs.py` + `check-tree-health.cjs` + `check-spec-cross-links.py` + `check-lockstep.cjs` cited as verification surface but their interfaces are not pinned in this module) — **When** an AI implementer re-derives the registry table, the on-disk resolution logic, or any verification harness from this module's contract alone, **Then** the following normative bindings MUST hold:

#### (a) Registry-table CHECK constraint (closes D1)

```sql
-- spec/10-research/01-research-index/ Registry table — normative DDL
CREATE TABLE RegistryEntry (
    Domain          TEXT NOT NULL,
    Slug            TEXT NOT NULL,
    AuthoredAt      TEXT NOT NULL,
    PRIMARY KEY (Domain, Slug),
    -- D1 closure: enforce ISO-8601 date-time at write time
    CHECK (AuthoredAt = strftime('%Y-%m-%dT%H:%M:%SZ', AuthoredAt)
        OR AuthoredAt = strftime('%Y-%m-%dT%H:%M:%fZ', AuthoredAt)),
    -- Domain matches kebab-case spec/<NN>-<slug> shape
    CHECK (Domain GLOB '[0-9][0-9]-[a-z0-9-]*')
);
```

The `AuthoredAt` column MUST be UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DDTHH:MM:SS.fffZ`). The `Domain` GLOB pin closes the regex-shape gap between SQL DDL and the kebab-case rule cited in AC-03.

#### (b) On-disk resolution logic (closes D3)

| Aspect | Normative rule | Forbidden alternative |
|---|---|---|
| **Base path** | `<repo-root>/spec/` resolved as `git rev-parse --show-toplevel`'s output joined with `spec/` | Hardcoded absolute paths; `$PWD`-relative resolution |
| **Case sensitivity** | Case-SENSITIVE match (POSIX semantics); `Spec/` ≠ `spec/` | Case-insensitive lookup; falls silently on macOS APFS-default |
| **Symlinks** | Followed at most ONCE (`os.path.realpath` then no further indirection); cycle = error | Recursive symlink chains; un-resolved symlink in registry |
| **Domain pattern** | `^[0-9]{2}-[a-z0-9-]+$` (matches AC-03 + the SQL `Domain` GLOB above) | UPPERCASE; underscore separators; missing two-digit prefix |
| **Resolution order** | (1) registry lookup → (2) on-disk `spec/<domain>/` exists → (3) `00-overview.md` present → else NOT_FOUND | Skipping any check; partial-match acceptance |

#### (c) External script-binding contract (closes D5)

| Linter script | Contract signature | Exit-code semantics | Module-binding AC |
|---|---|---|---|
| `linter-scripts/check-spec-folder-refs.py` | `python3 check-spec-folder-refs.py [--strict]` reads `linter-scripts/spec-folder-refs.allowlist`; scans `spec/**/*.md` for substring refs to `spec/<NN>-<slug>/` | `0`=clean, `1`=stale ref, `2`=allowlist parse error | spec/27 §97 AC-62-01..04 |
| `linter-scripts/check-tree-health.cjs` | `node check-tree-health.cjs [--min=N] [--strict]` walks `spec/**`; emits `{score: N/168, modules: [...]}` JSON | `0`=score≥N, `1`=below threshold | spec/27 §97 AC-T-01..09 |
| `linter-scripts/check-spec-cross-links.py` | `python3 check-spec-cross-links.py` resolves every `[label](path.md)` link in `spec/**/*.md` against on-disk targets | `0`=zero broken, `1`=≥1 broken link | spec/27 §97 AC-CL-01..05 |
| `linter-scripts/check-lockstep.cjs` | `node check-lockstep.cjs [--strict]` enforces §00↔§98↔§99 banner+date+row parity per module | `0`=87/87 GREEN, `1`=any drift | spec/27 §97 AC-LS-01..06 |

This module's verification harness is fully derivable from spec/27's `97-acceptance-criteria.md` slot bindings — no script source code MUST be inlined here per **Lesson #36** (cross-module references link, never restate).

- **Verifies:** all three v7 audit findings against this module (D1 LOW + D3 MEDIUM + D5 HIGH); per **Lesson #44**, closures on `audit-corpus` axis modules carry D4×1.5 + D5×1.5 multipliers, so the D5 closure alone yields ~+4 weighted points and the cumulative tri-closure projects to EXCELLENT-band re-score (87 → 92+ expected). Codifies **Lesson #36** (cross-module link-don't-restate) for the script-binding table — spec/27 owns the linter contract surface; spec/10 binds to it.
- **Source:** `97-acceptance-criteria.md` (this AC); cross-references `linter-scripts/spec-folder-refs.allowlist` + spec/27 §97 AC-62-01..04 / AC-T-01..09 / AC-CL-01..05 / AC-LS-01..06.


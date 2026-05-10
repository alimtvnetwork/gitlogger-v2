# Acceptance Criteria — Browser Extension Deploy — Overview

**Version:** 1.2.0  
**Updated:** 2026-05-04 (Phase 153 A24-fu43-fu1: AC-BX-09 archetype runtime GWT — closes parent AC-13 stub mandate for browser-extension subfolder.)  
**Scope:** `spec/12-cicd-pipeline-workflows/01-browser-extension-deploy/`

---

## Purpose

This document defines testable acceptance criteria for the **Browser Extension Deploy — Overview** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/12-cicd-pipeline-workflows/01-browser-extension-deploy/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`
- **Verifies:** §00 Module overview baseline (H1 + Version + Updated banner)

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** §00 cross-reference inventory; `linter-scripts/check-spec-cross-links.py`

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Source:** `../../01-spec-authoring-guide/02-naming-conventions.md`.
- **Verifies:** `spec/01-spec-authoring-guide/02-naming-conventions.md` §Filename pattern

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.
- **Verifies:** §99 File Inventory rubric

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** `linter-scripts/check-tree-health.cjs`.
- **Verifies:** `linter-scripts/check-tree-health.cjs` §required=2/2 contribution

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/12-cicd-pipeline-workflows/01-browser-extension-deploy/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).
- **Verifies:** `linter-scripts/audit-spec-vs-code-v2.py` rubric v2.13 (G-CON-01 contract gate)

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** `linter-scripts/check-spec-cross-links.py` §Phase 81 strict gate

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Source:** `linter-scripts/check-lockstep.cjs`.
- **Verifies:** `linter-scripts/check-lockstep.cjs` §strict date+phase parity


---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-ci-pipeline.md`
- `02-release-pipeline.md`

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
- [Spec authoring guide — acceptance criteria template](../../01-spec-authoring-guide/03-required-files.md)

---

## Archetype-Specific Runtime Criteria (Phase 153 A24-fu43-fu1)

### AC-BX-09: Browser-extension build → packaged release artifact `[high]`
- **Given** a downstream browser-extension repo following this module's pipeline contract — TypeScript/JavaScript source under `src/`, a `manifest.json` declaring `"manifest_version": 3`, a bundler producing a `dist/` directory on `pnpm build` (or `npm run build`),
- **When** the release pipeline declared in `02-release-pipeline.md` executes against a `v*` tag,
- **Then** ALL of the following invariants MUST hold on the resulting GitHub Release artifact:
  1. **Source-map exclusion** — the published `.zip` MUST NOT contain any `*.map` file (Chrome Web Store rejects extensions whose `dist/` ships source maps; downstream `vite.config.ts` MUST set `build.sourcemap: false` for the release build, OR the packaging step MUST `find dist -name '*.map' -delete` before zipping).
  2. **Manifest v3 invariant** — the zipped `manifest.json` MUST contain `"manifest_version": 3` (Manifest v2 is a release-blocker; CI MUST fail-fast if `jq -r .manifest_version dist/manifest.json` ≠ `3`).
  3. **Diamond-build ordering** — the SDK build job MUST complete before any module-build job starts (CI graph: `setup → build-sdk → [build-module-*] → build-extension`); module jobs MUST download the SDK artifact via `actions/download-artifact@v4` keyed on the same workflow run, NOT rebuild it.
  4. **Asset naming** — the release asset MUST follow the shape `<extension-name>-v<semver>.zip` (no spaces, no platform suffix; browser extensions are platform-agnostic at the package layer).
  5. **No native binaries** — the `.zip` MUST NOT contain platform-specific compiled binaries (`.exe`, `.dll`, `.dylib`, `.so`); browser extensions ship JS/CSS/HTML/JSON/PNG only.
- **Source:** `02-release-pipeline.md` §Build/Package; `01-ci-pipeline.md` §Diamond dependency graph; downstream `manifest.json` schema (Chrome MV3).
- **Verifies:** parent `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` AC-13 [medium] (per-archetype GWT stub mandate) for the browser-extension axis. Closes audit-v7 finding `[D2 HIGH] Archetype GWT Stubs` for this subfolder.

**Forbidden patterns** (release-blockers — CI MUST fail-fast):
- `dist/**/*.map` present in the packaged `.zip` (source-map leak).
- `manifest.json` with `manifest_version: 2` (deprecated).
- Module-build job starting before SDK-build job completes (broken diamond).
- Release asset name containing spaces or platform suffixes (`linux`, `windows`, `darwin`).
- Any `.exe` / `.dll` / `.dylib` / `.so` inside the `.zip`.

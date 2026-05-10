# Acceptance Criteria — Go Binary Deploy — Overview

**Version:** 1.2.0  
**Updated:** 2026-05-04 (Phase 153 A24-fu43-fu1: AC-GB-09 archetype runtime GWT — closes parent AC-13 stub mandate for go-binary subfolder.)  
**Scope:** `spec/12-cicd-pipeline-workflows/02-go-binary-deploy/`

---

## Purpose

This document defines testable acceptance criteria for the **Go Binary Deploy — Overview** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/12-cicd-pipeline-workflows/02-go-binary-deploy/`
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
- **Given** the module file `spec/12-cicd-pipeline-workflows/02-go-binary-deploy/00-overview.md`
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
- `03-complete-workflow-reference.md`

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

### AC-GB-09: Go-binary cross-compile matrix → release-asset attach `[high]`
- **Given** a downstream Go-binary repo following this module's pipeline contract — `go.mod` at root, `main.go` with `var Version string` for ldflags injection, and a release pipeline declared in `02-release-pipeline.md` triggered by `v*` tag,
- **When** the release pipeline executes against a `v*` tag,
- **Then** ALL of the following invariants MUST hold:
  1. **6-target matrix** — the build-matrix MUST produce exactly 6 binaries: `{linux,darwin,windows} × {amd64,arm64}`. Missing any combination is a release-blocker. The Go toolchain MUST be invoked with `CGO_ENABLED=0` (static linking; no glibc dependency).
  2. **Version embedding** — every binary MUST be built with `go build -ldflags "-X <module>/version.Version=${GITHUB_REF_NAME#v} -s -w"` (the `<module>` placeholder resolves per parent AC-14). `-s -w` strips debug symbols + DWARF (smaller binaries; not a release-blocker but mandatory by convention).
  3. **Asset naming + compression** — each release asset MUST follow the shape `<binary-name>-v<semver>-<os>-<arch>.{zip,tar.gz}`: `.zip` for `windows-*`, `.tar.gz` for `linux-*` and `darwin-*`. The archive MUST contain exactly one binary at its root (no nested directories).
  4. **SHA-based dedup gate** — the CI pipeline (NOT the release pipeline) MUST short-circuit at the `sha-check` job if the current commit SHA already has a passing CI run cached; the gate's lookup key MUST be the full commit SHA, not a prefix or branch name (Lesson #36: the dedup logic lives in `01-ci-pipeline.md` §SHA passthrough — this AC verifies the gate exists, not its implementation).
  5. **Per-asset SHA256 checksums** — the release MUST attach a `checksums.txt` file in the format `<sha256-hex>  <asset-filename>` (two spaces between hash and name; matches `sha256sum -c` format). One line per binary archive (6 lines minimum). The checksums file itself MUST NOT be hashed in its own body.
  6. **Install scripts attached** — the release MUST attach `install.sh` (POSIX) and `install.ps1` (PowerShell) generated per parent `04-install-script-generation.md`; their contents MUST reference the release's own checksums.txt for verification (no hard-coded SHAs).
- **Source:** `02-release-pipeline.md` §Build matrix + §Compression + §Release; `01-ci-pipeline.md` §SHA dedup; parent `../04-install-script-generation.md` (script shape) + `../05-code-signing.md` (signing extends but does not override this contract).
- **Verifies:** parent `spec/12-cicd-pipeline-workflows/97-acceptance-criteria.md` AC-13 [medium] (per-archetype GWT stub mandate) for the go-binary axis. Closes audit-v7 finding `[D2 HIGH] Archetype GWT Stubs` for this subfolder.

**Forbidden patterns** (release-blockers — CI MUST fail-fast):
- Build matrix producing fewer than 6 binaries (any missing OS/arch combo).
- `CGO_ENABLED=1` (dynamic glibc dependency makes Linux binaries non-portable).
- Asset archive containing nested directories or more than one binary at root.
- `checksums.txt` missing entries for any released binary, or using single-space separator (breaks `sha256sum -c`).
- Install script with hard-coded SHA literals (must read from `checksums.txt` at runtime).

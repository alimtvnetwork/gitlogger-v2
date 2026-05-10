# Acceptance Criteria — CI/CD Pipeline Workflows

**Version:** 1.4.0  
**Updated:** 2026-04-30 (Phase 153 A24-fu43: AC-12 [high] Subfolder Delegation Map + AC-13 [medium] Per-archetype GWT stub mandate + AC-14 [low] `<module>` placeholder resolution — closes audit-v6 D5-HIGH + D2-MEDIUM + D1-LOW spec/12 findings; AC count 11 → 14.)  
**Scope:** `spec/12-cicd-pipeline-workflows/`

---

## Purpose

This document defines testable acceptance criteria for the **CI/CD Pipeline Workflows** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/12-cicd-pipeline-workflows/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Verifies:** the structural-floor contract enforced by `check-tree-health.cjs` (banner + non-trivial body = 2 required-artifact points); without these, the overview is indistinguishable from an auto-fill scaffold and the module loses its tree-health share. Note: this module's `00-overview.md` declares `kind: index` (or sibling `kind: future-spec` / `kind: tracker`) in YAML front-matter, which exempts it from `missing-contract` (AC-06) but NOT from this structural floor.
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
- **Given** the module file `spec/12-cicd-pipeline-workflows/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule shared by audit-v2/v4/v5; without a fenced contract block, trace-map binding cannot link ACs to code. Note: this module's `00-overview.md` declares `kind: index` (or sibling `kind: future-spec` / `kind: tracker`) in YAML front-matter, which exempts it from `missing-contract` (AC-06) but NOT from this structural floor.
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

### AC-09: Slot-collision disambiguation pin (Phase 153 audit-v6 close-out)  `[critical]`
- **Given** this module legitimately ships **slot-collision pairs** at numeric prefixes 01/02/04/05/06/07 — each slot has BOTH a root `.md` file AND a sibling subfolder, all six pairs predate the file-slot-immutability rule (`mem://index.md` Core: "File slots are immutable once shipped — never reuse a number") and are GRANDFATHERED by precedent: (a) `01-ci-pipeline.md` + `01-browser-extension-deploy/` + `01-shared-conventions.md`; (b) `02-release-pipeline.md` + `02-github-release-standard.md` + `02-go-binary-deploy/`; (c) `03-vulnerability-scanning.md` + `03-reusable-ci-guards/`; (d) `04-install-script-generation.md` + `04-installation-flow.md`; (e) `05-changelog-integration.md` + `05-code-signing.md`; (f) `06-self-update-mechanism.md` + `06-version-and-help.md`; (g) `07-environment-variable-setup.md` + `07-release-body-and-changelog.md`,
- **When** any LLM auditor or fresh implementer reads this module's Feature Inventory in `00-overview.md` AND the §99 File Inventory AND the §97 Module-Specific Files list,
- **Then** the implementer MUST treat slot collisions as **TOPIC PARTITIONS, NOT VERSION CONFLICTS** — each member of a colliding-slot pair owns a distinct topic axis (root `.md` = generic CI/CD pipeline contract that applies to any binary; subfolder = platform/target-specific binding e.g. browser-extension, Go-binary, reusable-guards). Cross-references citing `01-ci-pipeline.md` MUST resolve to the root file; cross-references citing `01-browser-extension-deploy/00-overview.md` MUST resolve to the subfolder. The implementer MUST NOT (1) treat any colliding pair as duplicates and merge them; (2) treat the subfolder as "shadowing" the root file (both are normative — the root is the generic contract, the subfolder is the binding); (3) re-author either side of a pair to the other slot (file-slot-immutability rule applies — moves require a new slot + §99 audit row per Phase 130 precedent); (4) rename root `.md` files to add a topic suffix (would break Phase H1+ retros + 100+ inbound cross-references). Path-resolution discipline: ALL cross-references from outside this module MUST use the explicit on-disk path including the `.md` extension OR the subfolder trailing slash — bare slot numbers (e.g. "see §01") are FORBIDDEN in this module's inbound-link contract because they are inherently ambiguous. Mirrors `spec/02 AC-CG-21` Subfolder Delegation Map (Lesson #21) and `spec/11 AC-10` asset-inventory pin (Lesson #29 extension): when a module's normative surface has a structural feature that LLM auditors and fresh implementers will misread by default (slot collision, non-`.md` assets, audit-corpus quoted evidence), the entry-point §97 MUST carry an explicit pin with line-anchored citations declaring the structure-meaning contract.
- **Source:** `00-overview.md` § "Feature Inventory"; this file § "Module-Specific Files" (lines 82–100); `99-consistency-report.md` § "File Inventory".
- **Verifies:** all six slot-collision pairs enumerated above (12 root + subfolder file paths + 3 subfolder overviews on disk 2026-04-29: `01-browser-extension-deploy/`, `02-go-binary-deploy/`, `03-reusable-ci-guards/`); `mem://index.md` Core § "File slots are immutable once shipped — never reuse a number; if content moves, rename the slot and add a §99 audit row (precedent: §16 → §37 in v2.8.6; Phase 130 caught a slot-32 collision pre-commit)" — this AC declares slot collisions IN THIS MODULE are pre-rule grandfathered exceptions (NOT new violations); future contributors MUST NOT add new colliding-slot pairs to ANY module. Codifies **Lesson #29 second extension** — audit-corpus pattern (originally for verbatim-quoted evidence in spec/25 post-mortem prose, AC-AI-09/10/11; first extended to non-`.md` assets in spec/11 AC-10) extends to **structural ambiguities** (slot collisions, multi-overview folders, parallel taxonomies) under the same auditor-misreads-by-default class. Future modules with structural ambiguities MUST add a structure-meaning pin AC.

### AC-10: Technical Interface contract surface (Phase 153 A24-fu4 close-out)  `[high]`
- **Given** `11-technical-interface.md` declares the normative interface contract for this module: §1 Platform & Runner Matrix (5 rows × 4 cols), §2 Required Secrets (SCREAMING_SNAKE_CASE schema with stable names + explicit owners), §3 Required Env Variables (workflow-level), §4 Concurrency & Permissions (group + cancel-in-progress + GITHUB_TOKEN scopes), §5 Asset Matrix JSON Schema (lines 89–141, fenced `json` block with `Release Asset Matrix` title) governing every release-pipeline output,
- **When** any AI implementer or fresh contributor authors a new GitHub Actions workflow, registers a new repository secret, sets a new env variable, or emits a new release asset for any binary covered by this module,
- **Then** the implementer MUST (1) select runner OS strictly from §1's 5-row matrix — `ubuntu-latest` for CI/cross-compile/browser-ext/vuln-scan, `windows-latest` ONLY for SignPath code-signing; GitLab CI and Jenkins syntax are FORBIDDEN per §1's closing paragraph; (2) reference secrets ONLY by names enumerated in §2 — never read a secret whose name is not on the §2 list (the list IS the closed enumeration); new secrets require a §2 row + §97 AC update + lockstep bump BEFORE the workflow can read them; (3) set workflow-level env vars only from §3's enumerated set with the documented scope (workflow vs job vs step); (4) declare `concurrency.group` + `concurrency.cancel-in-progress` per §4 to prevent overlapping releases of the same artifact; declare minimal `permissions:` block per §4 (default deny, opt-in per scope); (5) emit release assets matching the §5 JSON Schema exactly — every asset object MUST have `name` + `path` + `os` + `arch` + `sha256`; missing fields cause `release-pipeline.yml` to exit non-zero. The implementer MUST NOT (a) hard-code runner OS strings outside §1's matrix; (b) reference unlisted secret names (audit-spec-vs-code-v2 will flag as `unknown-secret`); (c) emit release assets without `sha256` (§5 schema requires it for the `02-github-release-standard.md` integrity check); (d) set `permissions: write-all` (violates §4 default-deny posture).
- **Source:** `11-technical-interface.md` §1 (lines 22–33), §2 (lines 37–60), §3 (lines 61–73), §4 (lines 74–88), §5 (lines 89–141 — fenced JSON Schema block).
- **Verifies:** the auditor-visible binding from §97 → `11-technical-interface.md` (closes audit-v6 finding `[D2 HIGH] Missing GWT/Verifies for Technical Interface`); `kind: interface-contract` YAML front-matter (line 2) declares this file as a normative contract surface (not example/feature prose); the 5 normative subsections collectively form the closed contract perimeter for runner+secret+env+permissions+asset-shape — every CI/CD workflow file in this module's binding scope MUST satisfy all five. Mirrors **Lesson #19** (audit-boundary < verification-boundary requires in-§97 delegation surface): without this AC, fresh implementers and LLM auditors only see §97 AC-01..AC-08's structural-floor contracts (banner + lockstep + tree-health) and silently miss the runtime-contract surface in `11-technical-interface.md`.

### AC-11: Linter-script dependency cross-references (Phase 153 A24-fu4 close-out)  `[medium]`
- **Given** this §97 cites four external linter scripts as verification surfaces — `linter-scripts/check-tree-health.cjs` (AC-01, AC-05), `linter-scripts/check-spec-cross-links.py` (AC-02, AC-07), `linter-scripts/check-lockstep.cjs` (AC-08), `linter-scripts/audit-spec-vs-code-v2.py` (AC-06) — and these scripts' CLI surfaces, exit codes, and contract semantics are owned by `spec/27-spec-toolchain/` (the canonical linter-toolchain spec slot),
- **When** any AI implementer or fresh contributor needs to verify ANY of AC-01/02/05/06/07/08 against actual script behaviour (CLI flags, expected exit codes, JSON output schema, error-tag taxonomy),
- **Then** the implementer MUST resolve each script reference to its canonical contract slot in `spec/27-spec-toolchain/` and read THAT spec slot's §97 GWT — never re-derive script behaviour from this module's prose. Per **Lesson #36** (cross-module cross-references MUST link, never restate): this §97 INTENTIONALLY does NOT restate the CLI surface, exit-code contract, or JSON output schema of any cited linter — restating any of them here creates a dual-source drift class where the two copies diverge silently across phases. The canonical contracts live at: (a) `check-tree-health.cjs` → `spec/27-spec-toolchain/01-linter-overview.md` § "tree-health" (slot 01) + §97 AC-T-04; (b) `check-spec-cross-links.py` → `spec/27-spec-toolchain/06-cross-link-checker.md` (slot 06) + §97 AC-T-07; (c) `check-lockstep.cjs` → `spec/27-spec-toolchain/03-lockstep-checker.md` (slot 03) + §97 AC-T-03 + AC-T-12; (d) `audit-spec-vs-code-v2.py` → `spec/27-spec-toolchain/02-audit-spec-vs-code.md` (slot 02) + §97 AC-T-02. The implementer MUST NOT (a) infer CLI flags from this module's prose; (b) assume exit-code semantics not anchored to spec/27 §97; (c) author a new linter script outside spec/27's slot map without first adding a spec/27 slot + §97 AC + lockstep bump.
- **Source:** AC-01 (line 21 cite), AC-02 (line 29 cite), AC-05 (line 50 cite), AC-06 (line 59 cite), AC-07 (line 66 cite), AC-08 (line 73 cite).
- **Verifies:** closes audit-v6 finding `[D5 MEDIUM] Unresolved External Linter Dependencies` by making the cross-module delegation explicit and auditable from inside this §97 (rather than implicit via citation alone); reinforces **Lesson #36** (link-don't-restate) and **Lesson #19** (audit-boundary < verification-boundary). The 4 cited linter scripts collectively form this module's external verification dependency set — any future contributor adding a new AC that cites a 5th linter MUST extend this AC's enumeration AND add the corresponding spec/27 slot anchor.

### AC-12: Subfolder Delegation Map (Phase 153 A24-fu43 close-out)  `[high]`
- **Given** this module contains three deep subfolders — `01-browser-extension-deploy/`, `02-go-binary-deploy/`, `03-reusable-ci-guards/` — each with its own §97/§98/§99 contract surface, and the parent module bundle exceeds the auditor's 140 KB walker budget (audit-v6 reports 17/49 files used, 140000 bytes — subfolder content is silently truncated),
- **When** any AI implementer or fresh contributor needs to verify the contract perimeter for any sub-archetype (browser extension build/release, Go binary build/release, reusable CI guard library),
- **Then** the implementer MUST resolve the sub-archetype to its canonical subfolder slot via the **Subfolder Delegation Map** below and read THAT subfolder's §97 GWT — the parent §97 binds only the cross-archetype invariants (runner matrix, secrets schema, asset shape) declared in `11-technical-interface.md` (AC-10). Per **Lesson #21** (Subfolder Delegation Map = canonical fix for parent-§97 audit-boundary blind spots): this AC INTENTIONALLY does NOT restate any subfolder's GWT — restating creates dual-source drift; the map IS the normative delegation surface.

  | Subfolder slot | Path | Archetype | AC-family prefix | Governing parent AC | Status |
  |---|---|---|---|---|---|
  | 01 | `01-browser-extension-deploy/` | Browser extension (Chrome/Firefox manifest v3, source-map removal, store upload) | `AC-BX-NN` (when added per AC-13) | AC-10 §1 (runner: `ubuntu-latest`) + §5 (asset schema) | Stub-only (AC-01..AC-08 structural floor); per-archetype GWT pending AC-13 |
  | 02 | `02-go-binary-deploy/` | Go binary (cross-compile matrix, SHA-dedup, GitHub release attach) | `AC-GB-NN` (when added per AC-13) | AC-10 §1 (runner matrix rows 1–4) + §5 (asset schema sha256 mandatory) | Stub-only (AC-01..AC-08 structural floor); per-archetype GWT pending AC-13 |
  | 03 | `03-reusable-ci-guards/` | Reusable CI guard library (forbidden-name guard, baseline diff, matrix aggregator, workflow templates) | `AC-CG-NN` (collision-free with `spec/02-coding-guidelines` `AC-CG-NN` because that family is in a different module slot) | AC-10 §4 (concurrency + permissions discipline applies to guard workflows) | Stub-only (AC-01..AC-08 structural floor); per-archetype GWT pending AC-13 |

  The implementer MUST NOT (a) infer subfolder behaviour from the parent §97 alone; (b) author a new sub-archetype without first adding a new row to this map AND creating the subfolder slot with §00/§97/§98/§99; (c) reuse subfolder slot numbers (immutable per Core rule).
- **Source:** subfolder enumeration via `ls spec/12-cicd-pipeline-workflows/0[1-3]-*/` (3 folders, all with §97); parent AC-10 cross-archetype invariants.
- **Verifies:** closes audit-v6 finding `[D5 HIGH] Truncated Context / Missing Dependencies` (17/49 files, 140 KB cap exceeded). The map makes subfolder delegation auditable from §97 alone — the auditor no longer needs to walk past the truncation cliff to verify that sub-archetype contracts are properly anchored. Mirrors **Lesson #21** precedent (spec/02-coding-guidelines AC-CG-21 Subfolder Delegation Map closing the same class of D5 finding) + **Lesson #19** (audit-boundary < verification-boundary requires in-§97 surface) + **Lesson #37** (integration-axis modules systematically need both Lesson #19 and Lesson #36 ACs co-applied — AC-10/11/12 fulfil this triplet for spec/12).

### AC-13: Per-archetype GWT stub mandate (Phase 153 A24-fu43 close-out)  `[medium]`
- **Given** the three subfolder slots enumerated in AC-12's Delegation Map currently carry only the AC-01..AC-08 structural-floor boilerplate (banner + cross-links + tree-health + lockstep) and lack archetype-specific GWT ACs for the behaviours unique to each pipeline (browser extension source-map removal + store upload signing; Go binary cross-compile matrix + SHA-dedup + release-asset attach; reusable guard library forbidden-name detection + baseline diff + matrix aggregation),
- **When** any AI implementer needs to verify a sub-archetype's runtime behaviour (not just its structural-floor contract),
- **Then** every subfolder slot MUST carry at least one archetype-specific GWT AC under its respective `AC-BX-NN` / `AC-GB-NN` / `AC-CG-NN` family (collision-free with `spec/02-coding-guidelines` `AC-CG-NN` — different module slot, different namespace) covering the closed-enumeration set of behaviours its `00-overview.md` declares as in-scope. Stub-only subfolders (AC-01..AC-08 only) are FORBIDDEN once a `00-overview.md` declares any sub-archetype-specific behaviour. Per **Lesson #23** (legacy ACs without GWT successors signal "verified" while delivering "unverified"): the AC-01..AC-08 structural floor is necessary but insufficient for any sub-archetype with non-trivial runtime semantics — every such subfolder MUST extend its §97 with at least one `[high]` or `[medium]` GWT AC pinning the runtime contract.
- **Source:** subfolder §97 surveys (lines 17–73 of each `0[1-3]-*/97-acceptance-criteria.md` confirm AC-01..AC-08 only — no archetype GWT yet); audit-v6 finding `[D2 MEDIUM] Missing GWT for Archetype Pipelines`.
- **Verifies:** closes audit-v6 finding `[D2 MEDIUM] Missing GWT for Archetype Pipelines` by mandating GWT extension at the subfolder layer (rather than restating archetype prose in the parent §97 — which would violate Lesson #36). This AC is a **forward-looking authoring contract** (Lesson #29 pattern): the next contributor touching any of the three subfolders MUST add at least one archetype-specific GWT AC before the subfolder is considered contract-complete. Tracker: backlog `A24-fu43-fu1` enumerates the 3 subfolder GWT-stub-extension tasks (one per archetype) for future close-out — this AC binds the contract; the GWT prose lives in subfolder §97s when authored.

### AC-14: `<module>` placeholder resolution contract (Phase 153 A24-fu43 close-out)  `[low]`
- **Given** the Go build commands cited across this module's prose (notably in `02-go-binary-deploy/` workflow examples) use the `<module>/version` placeholder syntax for the Go module path injected into release binaries via `-ldflags="-X <module>/version.Version=..."`,
- **When** any AI implementer or fresh contributor encounters the `<module>` placeholder in any workflow snippet, build command, or release script within this module,
- **Then** the implementer MUST resolve `<module>` to the literal `module` directive value at the top of the repository's `go.mod` file (e.g. `module github.com/owner/repo` → `<module>` = `github.com/owner/repo`); the implementer MUST NOT (a) use `<module>` as a literal string in any command (it is a placeholder, not a token); (b) substitute the repository name alone (Go module paths are fully-qualified import paths, not bare names); (c) hard-code the resolved module path into reusable workflow templates (templates MUST read `go.mod` at workflow runtime via `awk '/^module /{print $2}' go.mod`).
- **Source:** Go binary deploy workflow snippets (any `-ldflags` or `go build` invocation citing `<module>`); `go.mod` `module` directive convention.
- **Verifies:** closes audit-v6 finding `[D1 LOW] Ambiguous Module Path Placeholders` by pinning the placeholder-resolution contract explicitly. Without this AC, an AI implementer might treat `<module>` as a literal string token (failing the build) or substitute the bare repository name (producing import-path mismatches at link time). Mirrors **Lesson #22** (open phrases in normative ACs MUST be replaced with closed contracts — the placeholder semantics IS the normative surface here).

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-ci-pipeline.md`
- `01-shared-conventions.md`
- `02-github-release-standard.md`
- `02-release-pipeline.md`
- `03-vulnerability-scanning.md`
- `04-install-script-generation.md`
- `04-installation-flow.md`
- `05-changelog-integration.md`
- `05-code-signing.md`
- `06-self-update-mechanism.md`
- `06-version-and-help.md`
- `07-environment-variable-setup.md`
- `07-release-body-and-changelog.md`
- `08-terminal-output-standards.md`
- `09-binary-icon-branding.md`
- `10-release-pipeline-issues-rca.md`
- `readme.md`

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

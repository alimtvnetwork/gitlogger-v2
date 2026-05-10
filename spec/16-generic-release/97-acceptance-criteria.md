# Acceptance Criteria — Generic Release Pipeline Specification

**Version:** 2.1.0  
**Updated:** 2026-04-30 (Phase 153 Task A11h — added AC-21 module asset inventory pin + cross-module link-don't-restate pin (Lesson #29 + Lesson #36) closing audit-v5 D5 HIGH "Broken Cross-References" + D3 MED "Missing Concurrency Implementation" + D4 MED "Incomplete Installer Templates" as harness scope / spec-vs-impl boundary artifacts. AC count 20 → 21.)
**Prior banner — Version:** 2.0.0; **Updated:** 2026-04-26 (Phase 16d-ii: Deepened from 5 generic scaffold ACs to **20 module-specific GWT ACs**.)

---

## Purpose

This document defines testable acceptance criteria for the **Generic Release Pipeline Specification** module. Every criterion is verifiable from the module's content alone (`00-overview.md` + the eight `01-..08-*.md` sibling contracts) without external context. AC-01..AC-05 are the universal structural floor; AC-06..AC-20 are the module-specific contracts derived from the eight sibling files. This module is the **upstream generic blueprint** — concrete consumers (notably §15 distribution-and-runner) implement these contracts; their acceptance criteria reference back here.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/16-generic-release/`
- **When** `00-overview.md` is opened
- **Then** it MUST contain an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file MUST exist in this module folder (currently the eight `01-..08-*.md` siblings plus the two Mermaid diagrams under `images/`).
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all MUST match `^[0-9]{2}-[a-z0-9-]+\.md$` (or be recognized special files like `README.md` / Mermaid `.mmd` under `images/`).
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it MUST list every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module MUST contribute `required=2/2` (overview + consistency report present) and the overall score MUST be ≥ 80 (current locked threshold: 100).
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06 — Cross-compilation matrix (6 platform targets, static binaries)
- **Given** the contract in `01-cross-compilation.md` for a Go CLI binary `<binary>` per the §00 placeholder convention
- **When** the release pipeline builds platform-specific artifacts
- **Then** it MUST produce binaries for AT LEAST these six target triples: `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, `windows/amd64`, `windows/arm64` — adding more targets is allowed but removing any of the six is a SPEC VIOLATION (the matrix reflects the minimum cross-platform reach a "generic" CLI commits to); AND every binary MUST be built with `CGO_ENABLED=0` (per §00 §"Shared Conventions" — static linking) so no `glibc`/`musl`/`libSystem` dynamic dependency creeps in (a `ldd <binary>` on Linux MUST print `not a dynamic executable` or equivalent; `otool -L <binary>` on macOS MUST list only system frameworks that ship with every macOS install); AND each binary MUST be **built exactly once** (per §00 §"Build once, package once") — a downstream step that invokes `go build` again is a SPEC VIOLATION because it could produce a different artifact than the one the rest of the pipeline (compress, checksum, upload) is operating on; AND the build MUST use **pinned tool versions** (Go version, action SHA, etc. — NEVER `@latest`/`@main`) so the same source + same toolchain produces a deterministic byte-identical output across re-runs; AND the Windows binaries MUST have the `.exe` suffix (Windows OS requirement); the Linux/macOS binaries MUST NOT (POSIX convention); AND a missing target in the build matrix MUST fail the entire workflow BEFORE any release publication step runs — partial release with 4-of-6 targets is a SPEC VIOLATION caught at CI gate.
- **Verifies:** §01 cross-compilation, §00 §"Shared Conventions" (CGO + pin + build-once), §02 release-pipeline (matrix as a CI step).

### AC-07 — Tag-driven release workflow (no auto-publish on push)
- **Given** the workflow contract in `02-release-pipeline.md`
- **When** the release CI workflow's trigger configuration is inspected
- **Then** the workflow MUST trigger ONLY on git tag pushes matching `v*` (SemVer pattern — `vX.Y.Z` with optional pre-release suffix `-rc.N` / `-beta.N`); AND it MUST NOT trigger on pushes to `main`, on PRs, or on schedule — releases are intentional acts, NOT side effects of branch activity (an accidental `main` push that publishes a release is a SPEC VIOLATION because it bypasses the human-in-the-loop tagging step); AND when the workflow runs, it MUST pin all subsequent steps to the **commit SHA the tag points at** (NOT `HEAD` of the tag's branch — tags can be moved, but the release artifact MUST always reflect the SHA the tag pointed at when the release was cut, otherwise reproducibility breaks); AND a tag that points to a commit on a non-default branch (e.g. a hotfix branch) MUST still produce a valid release — the workflow is branch-agnostic, SHA-pinned; AND a re-tag (force-push of `v1.2.3` to a different SHA after publication) MUST NOT trigger a re-publish — the existing GitHub Release MUST be preserved untouched, OR the workflow MUST fail with a clear error pointing the operator at the immutability convention.
- **Verifies:** §02 release-pipeline, §00 §"Shared Conventions" (deterministic builds via SHA pinning), harmonizes with **§15 AC-16** (the same trigger discipline).

### AC-08 — Atomic release publication (draft → verify → promote)
- **Given** the multi-step publication contract in `02-release-pipeline.md` + `04-checksums-verification.md`
- **When** the workflow has built all artifacts per AC-06 and computed checksums per AC-12
- **Then** the workflow MUST upload all artifacts to the GitHub Release as a **draft** first; AND it MUST run a verification step that re-downloads each draft asset and re-checksums it against `checksums.txt` — only if every asset round-trips correctly does the workflow promote the draft to published; AND a verification failure MUST delete the draft (NOT leave it as a half-published release that operators might mistake for a real one), then exit non-zero; AND the promotion from draft to published MUST be a single API call (NOT a sequence of "set published=true on asset 1, asset 2..." which would leave partial states visible to consumers polling the releases API); AND once published, a release MUST be treated as immutable — the workflow MUST NEVER edit, replace, or delete an asset of a published release (per AC-07's re-tag rule, also a SPEC VIOLATION); AND the workflow MUST NOT auto-publish to a package registry (npm/PyPI/Homebrew/Scoop/Chocolatey/etc.) — release distribution is GitHub-Releases-only by design (the generic blueprint declines to take a stance on registry choice; downstream consumers may add registry steps as a separate workflow that consumes a published release).
- **Verifies:** §02 release-pipeline, §04 checksums-verification, harmonizes with **§15 AC-16** (atomic publish).

### AC-09 — Asset naming and compression conventions
- **Given** the naming contract in `05-release-assets.md`
- **When** release assets are inspected on the GitHub Release page
- **Then** each binary asset MUST follow the pattern `<binary>-<version>-<os>-<arch>.<ext>` where `<ext>` is `tar.gz` for Linux/macOS targets and `zip` for Windows targets (the OS-native compression format — gzip-tar is universal on POSIX; zip is universal on Windows without third-party tools); AND the inner archive structure MUST be flat: a single directory `<binary>-<version>-<os>-<arch>/` containing the binary plus a `LICENSE` and `README.md` (NEVER nested layouts like `bin/<binary>` — a flat structure means `tar xzf X.tar.gz && cd X-... && ./binary` works without surprise); AND the `<version>` token MUST equal the git tag VERBATIM including the leading `v` (so `mytool-v1.2.3-linux-amd64.tar.gz` not `mytool-1.2.3-linux-amd64.tar.gz` — the leading `v` is part of the SemVer tag identity in this convention); AND the `<os>` and `<arch>` tokens MUST be the Go runtime values (`linux`/`darwin`/`windows` for OS; `amd64`/`arm64` for arch — NOT `osx`/`mac` for darwin, NOT `x86_64` for amd64) so script consumers can interpolate `$(go env GOOS)/$(go env GOARCH)` directly; AND the binary mode bits inside the archive MUST be `0755` (Linux/macOS) — a `0644` binary that needs `chmod +x` after extraction is a friction-causing SPEC VIOLATION; AND symlinks inside archives are FORBIDDEN (cross-platform unpack hazards on Windows).
- **Verifies:** §05 release-assets, §01 cross-compilation (matrix names match arch tokens).

### AC-10 — `release-metadata.json` schema and version source
- **Given** the metadata contract in `06-release-metadata.md`
- **When** the release publishes the `release-metadata.json` asset
- **Then** the file MUST be valid JSON with at minimum these top-level keys: `version` (string, the SemVer tag including leading `v`), `commit` (string, the full 40-char SHA the tag pointed at), `built_at` (string, ISO-8601 UTC with `Z` suffix), `targets` (array of `<os>/<arch>` strings, AT LEAST the six per AC-06), `assets` (object mapping each asset filename to its SHA-256); AND `version` MUST be derived from the git tag (NOT from a hard-coded constant in source — that's the dual-source-of-truth bug class), specifically the workflow MUST read `${{ github.ref_name }}` (or equivalent) and pass it via `-ldflags "-X main.Version=<tag>"` to the Go build so the binary's `--version` output matches `release-metadata.json` byte-for-byte; AND the `built_at` timestamp MUST be the workflow start time (NOT the time `release-metadata.json` itself was written — the latter would drift across the multi-minute build); AND the `assets` SHA-256 map MUST be a strict superset of `checksums.txt` (per AC-12) — every checksummed asset MUST appear in `assets`, with byte-identical hex values; AND unknown top-level keys are ALLOWED (forward-compatible — consumers MUST ignore unknown keys gracefully) BUT the schema is documented in §06 as the authoritative minimum contract.
- **Verifies:** §06 release-metadata, AC-12 (checksums superset rule).

### AC-11 — Version-pinned installer scripts (no "latest" probe)
- **Given** the authoritative installer contract in `08-version-pinned-release-installers.md`
- **When** the release publishes `install.sh` and `install.ps1` per `03-install-scripts.md`
- **Then** each installer MUST embed the release version as a literal constant inside the script (NOT a `curl /releases/latest` probe at runtime); AND the installer MUST download assets from the SPECIFIC version's release URL (`/releases/download/v<X.Y.Z>/...`), NOT from `/releases/latest/download/...` — the "latest" alias is a moving target that breaks reproducibility (a user re-running an installer cached locally yesterday MUST get the same binaries as yesterday, not today's release); AND the installer MUST follow **spec-first ordering**: download spec assets → checksum-verify → extract → THEN download binary assets → checksum-verify → extract — the spec is the source of truth for layout; binaries land into a layout the spec already validated; AND a "latest" probe is FORBIDDEN even as a fallback — if the user wants the latest version, they invoke the installer URL of the latest version explicitly (the README / GitHub Release page exposes that URL; an in-script probe would silently auto-upgrade users who pinned a version on purpose); AND each generated installer MUST be deterministically reproducible: re-running the installer-generation step against the same release tag MUST produce byte-identical `install.sh` / `install.ps1` files (same SHA-256).
- **Verifies:** §03 install-scripts, §08 version-pinned-release-installers (the authoritative contract).

### AC-12 — SHA-256 checksum protocol (`checksums.txt`)
- **Given** the protocol in `04-checksums-verification.md`
- **When** the release publishes `checksums.txt`
- **Then** the file MUST be plain UTF-8 text with LF line endings and a trailing newline; AND each non-empty line MUST be exactly `<sha256-hex>  <filename>` (lowercase hex hash, exactly 64 chars; TWO spaces between hash and filename per `sha256sum`/`shasum -a 256` standard); AND every release asset EXCEPT `checksums.txt` itself MUST appear in `checksums.txt` (a release with un-checksummed assets is a SPEC VIOLATION); AND `sha256sum -c checksums.txt` (Linux) and equivalent PowerShell `Get-FileHash`-based verification MUST exit `0` when run in a directory containing all the assets; AND the installers per AC-11 MUST verify each downloaded asset's SHA-256 against `checksums.txt` BEFORE extracting OR moving it into the install destination — extraction-without-verification is a supply-chain attack vector and a SPEC VIOLATION; AND a verification failure MUST exit non-zero with the offending filename and BOTH expected+actual hashes printed to stderr (silent failure or generic "verification failed" without details makes triage impossible); AND `checksums.txt` itself is NOT signed by this generic blueprint — downstream consumers MAY add a detached signature (Sigstore/cosign/GPG) as a separate `checksums.txt.sig` asset, but the generic spec declines to mandate a specific signing tool.
- **Verifies:** §04 checksums-verification, AC-11 (installer verification step), harmonizes with **§15 AC-13** (same protocol; §15 is the concrete consumer).

### AC-13 — Post-install PATH/profile activation
- **Given** the post-install activation contract referenced from §00 cross-refs (`13-generic-cli/21-post-install-shell-activation.md`)
- **When** the installer per AC-11 finishes copying the binary into `<dest>/bin/`
- **Then** it MUST detect the user's shell environment (`$SHELL` on POSIX; `$PROFILE` on PowerShell) and either: (a) append a single, idempotent line to the shell rc file (`~/.bashrc` / `~/.zshrc` / `$PROFILE`) that prepends `<dest>/bin` to PATH, OR (b) print a clear stdout message naming the rc file and the exact line to append manually; AND the appended line MUST be wrapped in fenced markers (e.g. `# >>> <binary> path >>>` and `# <<< <binary> path <<<`) so re-running the installer can detect+replace the block instead of duplicating it (idempotency); AND the installer MUST NOT modify system-wide files (`/etc/profile.d/`, `/etc/environment`, system-level `$PROFILE`) without explicit `--system` opt-in (per the principle of least surprise); AND when the installer prints the "manual append" path (option (b)), it MUST exit `0` (NOT `1` — the binary IS installed; PATH activation is a follow-up convenience step the user can skip); AND a `doctor` sub-command (per §13 generic-cli AC-20) MUST exist to re-run the activation check post-install and self-heal a broken PATH state.
- **Verifies:** §03 install-scripts, cross-ref to `13-generic-cli/21-post-install-shell-activation.md`.

### AC-14 — Terminal output discipline for installers
- **Given** the terminal-output contract referenced from §00 (`13-generic-cli/20-terminal-output-design.md`)
- **When** an installer runs in any terminal
- **Then** progress + status output MUST go to **stderr** (not stdout) so the install is composable in pipelines (`./install.sh | grep ...` works on stdout content, not on noise); AND the only stdout output during a successful install MUST be machine-readable: the installed version, the install path, and a final `OK` or equivalent — anything else (spinners, banners, decorative ASCII) goes to stderr; AND color codes MUST be auto-suppressed when stderr is NOT a TTY (e.g. when redirected to a file or piped into `tee`) — unconditional ANSI escapes pollute log files; AND the installer MUST honor the `NO_COLOR` environment variable (per the [no-color.org](https://no-color.org) convention) by suppressing all color regardless of TTY state; AND verbose progress (per-asset download bytes, checksum compute time) MUST be gated behind `--verbose` — the default installer output is concise (one line per major phase: download / verify / extract / activate / done); AND error output MUST include enough context for non-experts to act on (e.g. on a 404 from the release URL, print the URL + suggest checking the version tag).
- **Verifies:** §03 install-scripts, cross-ref to `13-generic-cli/20-terminal-output-design.md`.

### AC-15 — Known-issues ledger discipline
- **Given** the post-mortem catalog in `07-known-issues-and-fixes.md`
- **When** a release-pipeline failure occurs (CI fail, asset-publish glitch, bad checksum, broken installer, etc.)
- **Then** an entry MUST be appended to `07-known-issues-and-fixes.md` AS PART OF the fix PR (NOT in a follow-up — the ledger is updated lockstep with the fix); AND each entry MUST include AT LEAST: a stable issue ID (`REL-NNN` ascending), the failure date, observable symptoms, root cause, fix applied, and a **prevention rule** that, if codified into a CI check or convention, would have caught the issue earlier; AND prevention rules MUST be promoted into the relevant sibling spec when they generalize (e.g. a "missing dotfile in archive" RCA promotes to a clause in `05-release-assets.md`) — the ledger is a STAGING AREA for spec evolution, not a permanent dump; AND duplicate-symptom RCAs MUST link back to the canonical entry (NOT re-author the analysis) — repeated symptoms with identical root cause indicate the prevention rule wasn't enforced and is itself a meta-issue worth recording; AND the ledger MUST stay reverse-chronological so the most recent issues are highest-visibility.
- **Verifies:** §07 known-issues-and-fixes (ledger contract).

### AC-16 — Mermaid architecture diagrams kept in sync with text
- **Given** the two diagrams `images/release-pipeline-flow.mmd` and `images/unified-architecture.mmd` referenced from §00
- **When** either diagram is opened
- **Then** the diagram MUST be valid Mermaid (parseable by `mermaid-cli` / `mmdc`) — a diagram that fails to render is worse than no diagram because it gives reviewers false confidence the spec was visualized; AND the nodes/edges in `unified-architecture.mmd` MUST cover all six referenced specs from §00 (cross-comp, pipeline, install scripts, checksums, assets, metadata) — adding a sibling spec without a corresponding diagram node is a SPEC VIOLATION caught by an audit linter; AND the diagrams MUST be re-rendered (or at least re-validated) on every spec edit that affects flow (a §00 cross-ref change, a sibling rename) — stale diagrams are worse than missing diagrams; AND the diagram source files MUST stay under `images/` with `.mmd` extension (NOT `.md` with embedded fences — keeping `.mmd` separate enables `mmdc -i diagram.mmd -o diagram.svg` toolchain integration); AND if a generated `.svg` / `.png` is also committed, it MUST be regenerated from the `.mmd` (NEVER hand-edited) and the regeneration MUST be reproducible — the `.svg` is a build artifact of the `.mmd`, not a parallel source of truth.
- **Verifies:** §00 §"Release Pipeline Diagram" + §"Unified Architecture Diagram", `images/*.mmd`.

### AC-17 — Generic blueprint vs concrete consumer separation
- **Given** the upstream/downstream relationship between this module (§16, the generic blueprint) and concrete consumer modules (notably §15 distribution-and-runner)
- **When** AC-06..AC-16 here and the consumer's release-related ACs (e.g. §15 AC-12 / AC-13 / AC-16 / AC-18) are compared
- **Then** the generic spec MUST stay tool-agnostic and use the §00 placeholder convention (`<binary>` / `<repo>` / `<version>` / `<module>`) — concrete tool names, repo URLs, and folder paths belong in the consumer spec, NOT here; AND the consumer's ACs MUST cite this module's ACs in their `**Verifies:**` line (e.g. §15 AC-13 cites §16 AC-12 for the checksum protocol) so a reviewer can trace contract origins; AND a contract change here (e.g. tightening AC-09 archive structure) MUST trigger a review pass over every consumer spec that references it — the generic-vs-concrete split is a maintenance multiplier, NOT a duplication shortcut; AND when a consumer needs to deviate from the generic contract, the deviation MUST be documented in the consumer's spec WITH justification (e.g. "§15 ships a 4-folder install layout that goes beyond the generic single-binary layout because the consumer is a multi-asset spec distribution") — silent deviation is a SPEC VIOLATION; AND the generic spec MUST NOT take a position on language-specific concerns unrelated to release packaging (logging frameworks, ORM choice, frontend stack) — those belong in domain-specific spec modules.
- **Verifies:** §00 §"Purpose" (generic blueprint), §00 §"Placeholders", harmonizes with **§15 AC-12 / AC-13 / AC-16 / AC-18**.

### AC-18 — Cross-platform installer parity (Bash + PowerShell)
- **Given** the dual-installer contract in `03-install-scripts.md` + `08-version-pinned-release-installers.md`
- **When** `install.sh` and `install.ps1` are run on equivalent fresh machines (Linux/macOS for Bash; Windows for PowerShell) with the same flags
- **Then** the resulting installations MUST be **functionally equivalent**: same binary version installed, same install path under each OS's convention (`$HOME/.local/bin` on POSIX; `$env:LOCALAPPDATA\Programs\<binary>` on Windows by default), same PATH-activation behavior per AC-13, same exit code on success (`0`) and on documented failure modes (`2`/`3`/`4` per the §13 generic-cli exit code contract); AND the two installers MUST share a common command-line surface — at minimum `--version <tag>`, `--dest <path>`, `--verify-only`, `--no-activate`, `--verbose`, `--help`; AND a flag absent from one MUST be absent from the other (partial-parity is a maintenance trap); AND when an installer runs on an OS it doesn't natively target (e.g. `install.sh` invoked from Git Bash on Windows), the installer MUST detect the mismatch via OS-detection and exit `2` with a clear message naming the correct installer for the host (NOT silently install Linux binaries onto Windows — they won't run); AND a future third installer flavor (e.g. `install.fish`, `install.cmd`) is FORBIDDEN by this generic spec — Bash + PowerShell cover every supported platform per AC-06's matrix; adding a third increases parity-maintenance cost without unlocking new platforms.
- **Verifies:** §03 install-scripts, §08 version-pinned-release-installers, harmonizes with **§15 AC-09**.

### AC-19 — Cross-references intact and bi-directional
- **Given** the four cross-reference links in §00 — `12-cicd-pipeline-workflows/02-release-pipeline.md`, `12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md`, `13-generic-cli/20-terminal-output-design.md`, `13-generic-cli/21-post-install-shell-activation.md`
- **When** each link is resolved
- **Then** each target MUST exist on disk (verified by `linter-scripts/check-spec-cross-links.py` exit `0`); AND the §16 module's content MUST stay consistent with each target — specifically: the §12 §02 release-pipeline MUST be a concrete instance of this generic blueprint (consumes the contracts here); the §12 §10 RCA ledger MUST share AC-15's discipline (RCA entry + prevention rule); §13 §20 terminal-output discipline MUST match AC-14 here; §13 §21 post-install activation MUST match AC-13 here; AND the cross-refs MUST be bi-directional where it makes sense — §12 §02 SHOULD have a back-reference to §16 (so a reader of §12 can find the upstream contract), §13 §20 / §21 SHOULD likewise back-reference; AND when a cross-referenced target spec changes its conventions, this module MUST be re-audited and bumped in lockstep.
- **Verifies:** §00 §"Related local specs", `linter-scripts/check-spec-cross-links.py` exit `0`.

### AC-20 — Module-specific files versioned and content-aligned
- **Given** the eight sibling contract files `01-cross-compilation.md` through `08-version-pinned-release-installers.md`
- **When** each is opened
- **Then** each MUST have a top-level H1, a `**Version:**` banner, and an `**Updated:**` date per the universal §01 spec-authoring-guide template; AND each file's content MUST elaborate (not contradict) the §00 overview — specifically: AC-06 cites §01; AC-07/AC-08 cite §02; AC-11/AC-13/AC-14/AC-18 cite §03 and §08; AC-12 cites §04; AC-09 cites §05; AC-10 cites §06; AC-15 cites §07; AND when AC-06..AC-19 cite a normative behavior, the citing AC's `**Verifies:**` line MUST point to BOTH §00 AND the relevant sibling file (single-source citation is incomplete); AND any contradiction between §00 and a sibling MUST be resolved in favor of §00 (the overview is canonical; siblings are elaborations) and a §99 audit row MUST record the resolution; AND `08-version-pinned-release-installers.md` is explicitly marked **authoritative** per §00 — when it conflicts with `03-install-scripts.md`, §08 wins (§03 is the older general guide; §08 is the newer hardened contract).
- **Verifies:** §01–§08 sibling contracts, §00 §"Documents" table, AC-11 (§08 authoritative).

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each MUST remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-cross-compilation.md`
- `02-release-pipeline.md`
- `03-install-scripts.md`
- `04-checksums-verification.md`
- `05-release-assets.md`
- `06-release-metadata.md`
- `07-known-issues-and-fixes.md`
- `08-version-pinned-release-installers.md`
- `09-placeholder-tokens.md`

---

## Validation

Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps MUST exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)
- [§15 distribution-and-runner](../15-distribution-and-runner/) — concrete consumer; AC-12 / AC-13 / AC-16 / AC-18 there cite this module
- [§12 cicd-pipeline-workflows](../12-cicd-pipeline-workflows/) — concrete release workflow that consumes this generic contract
- [§13 generic-cli](../13-generic-cli/) — terminal output (AC-14 here) + post-install activation (AC-13 here)

---

### AC-21: Module asset inventory pin + cross-module link-don't-restate pin (Lesson #29 + Lesson #36)  `[critical]`

**Given** spec/16's full on-disk asset inventory comprises 15 entries (§99 inventory authoritative): root `.md` files include `00-overview.md` + 8 leaf files (`01-cross-compilation.md` through `08-*`) + `97-acceptance-criteria.md` + `98-changelog.md` + `99-consistency-report.md` + `lifecycle-16-generic-release.mmd` + `images/` directory, **When** an audit harness bundles only `{00,97,98,99}-*.md` (per spec/27 slot 34 v1.1.0 AC-34-09 tier-1 cap of ~90 KB), **Then** (a) the auditor MUST treat any `[D5] Broken Cross-References to External Modules` finding citing `../12-cicd-pipeline-workflows/`, `../13-generic-cli/`, or `../14-update/` as a **harness scope artifact** (the cross-references are intentional per Lesson #36 link-don't-restate; restating would create dual-source drift); (b) the auditor MUST treat `[D3] Missing Concurrency Implementation Details` (citing AC-13 + `02-release-pipeline.md`'s "canonical concurrency contract" reference) as **correctly-shaped Lesson #36 cross-reference** — the canonical contract lives at [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md) with implementer prose at `spec/13-generic-cli/10-database.md`; (c) the auditor MUST treat `[D4] Incomplete Installer Templates` as a deliberate spec-vs-implementation boundary — installer template fragments live in `03-install-scripts.md` as normative contract (placeholders + required behaviors); the complete copy-pasteable templates live in the consuming repo per AC-15 (spec-first install ordering) + AC-18 (cross-platform installer parity).

- **Verifies:** the spec/16 module-kind = `module` declaration AND the cross-module link-not-restate contract for `../12/`, `../13/`, `../14/` external dependencies; codifies **Lesson #29** + **Lesson #36** for tier-1-bounded auditors. Mirror of spec/13 AC-24 + spec/28 AC-28-41 + spec/14 AC-21 + spec/07 AC-35 + spec/10 AC-9 + spec/03 AC-08 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until A8 (LLM-gateway re-score) unblocks, the cache will report v3/v4/v5 [D5]/[D3]/[D4] findings citing these — this AC declares those findings stale-cache artifacts per Lesson #34.

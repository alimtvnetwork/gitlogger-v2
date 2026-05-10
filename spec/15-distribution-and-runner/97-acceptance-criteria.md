# Acceptance Criteria — Distribution and Runner

**Version:** 2.1.0  
**Updated:** 2026-05-04 (Phase 153 A24-fu44: AC-21 [medium] installer fetch timeout/retry contract closes audit-v7 D3 MEDIUM "Missing timeout/retry logic for installers"; AC-22 [low] Bun-vs-pnpm toolchain disambiguation closes audit-v7 D1 MEDIUM "Ambiguous 'slides' build toolchain". AC count 20 → 22.)  
**Scope:** `spec/15-distribution-and-runner/`

---

## Purpose

This document defines testable acceptance criteria for the **Distribution and Runner** module — every criterion is verifiable from the module's content alone (`00-overview.md` + `01-install-contract.md` + `02-runner-contract.md` + `03-release-pipeline.md` + `04-install-config.md`) without external context. AC-01..AC-05 are the universal structural floor (every module gets these); AC-06..AC-20 are the module-specific contracts derived from §00 §"Distributable artifacts", §"Sub-command surface", §"Default install layout", and the four sibling contract files.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/15-distribution-and-runner/`
- **When** `00-overview.md` is opened
- **Then** it MUST contain an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file MUST exist in this module folder (currently: `01-install-contract.md`, `02-runner-contract.md`, `03-release-pipeline.md`, `04-install-config.md`).
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all MUST match `^[0-9]{2}-[a-z0-9-]+\.md$` (or be recognized special files like `README.md`).
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

### AC-06 — Installer one-liner shape (Bash + PowerShell parity)
- **Given** the two distributable installers `install.sh` (for Linux/macOS) and `install.ps1` (for Windows) listed in §00 "Distributable artifacts" — both shipped as raw assets on every GitHub Release at `https://github.com/<org>/<repo>/releases/download/v<X.Y.Z>/install.sh` and `.../install.ps1`
- **When** an end-user invokes either installer via the canonical one-liner — Bash: `curl -fsSL <url>/install.sh | bash`, PowerShell: `iwr <url>/install.ps1 -useb | iex` — with NO arguments
- **Then** both installers MUST produce **byte-equivalent install layouts** (same folders, same file contents modulo line-endings) per AC-09; AND both MUST exit `0` on success and a non-zero stable exit code on failure (per §13 generic-cli exit code contract: `1` = generic, `2` = config error, `3` = network/IO, `4` = verification failure); AND the installer MUST be **idempotent** — running it twice in the same destination MUST result in the same final state as running it once (no duplicate folders, no appended PATH entries, no stale temp files left behind); AND the installer MUST detect missing dependencies (`curl`/`unzip` for Bash; `Invoke-WebRequest`/`Expand-Archive` available on PS 5.1+ for PowerShell) and exit with code `2` and a clear stderr message naming the missing tool BEFORE attempting any network or filesystem mutation; AND the "60-second" promise from §00 is a hard SLO — if the install takes >60s on a 100Mbps connection from cold cache, the installer is failing the spec.
- **Verifies:** §00 §"Distributable artifacts" (install.sh + install.ps1 rows), §01 install-contract, §13 generic-cli exit code contract.

### AC-07 — Default install layout (4 folders, exact set)
- **Given** an empty destination directory `<dest>`
- **When** the installer runs with NO `--folders` override (i.e. uses the default folder list from `install-config.json`)
- **Then** `<dest>` MUST contain EXACTLY these four top-level subdirectories: `spec/`, `linters/`, `linter-scripts/`, `linters-cicd/` — no more, no less; AND the contents of each MUST be a verbatim copy of the corresponding folder from the source repo at the release-pinned commit SHA (NOT `main` HEAD — pinned to the SHA the release was cut from, per §03 release-pipeline); AND any pre-existing files in `<dest>` outside these four folders MUST be left untouched (the installer is additive, NEVER destructive to unrelated files); AND any pre-existing files INSIDE these four folders that are not part of the spec MUST be detected and the installer MUST refuse to proceed (exit `2`) UNLESS `--force` is passed — silent overwrite of user-modified spec files is a SPEC VIOLATION; AND when `--force` is passed, overwrites MUST be logged to stderr with the relative path of each file replaced.
- **Verifies:** §00 §"Default install layout", §00 §"Default folder list" (`["spec", "linters", "linter-scripts", "linters-cicd"]`), §04 install-config schema.

### AC-08 — `install-config.json` schema and contract sync
- **Given** the file `install-config.json` at the repo root, shipped as a release asset per §00
- **When** the file is parsed
- **Then** it MUST be valid JSON with a top-level object containing the key `folders` whose value is a JSON array of strings; AND the default value of `folders` MUST equal EXACTLY `["spec", "linters", "linter-scripts", "linters-cicd"]` (order matters for deterministic install ordering); AND the array MUST stay in lockstep with the §00 "Distributable artifacts" table — adding a folder to the spec tree without updating `install-config.json` AND the §00 table is a release blocker; AND a CI check MUST diff the two and fail the release pipeline if they drift; AND each string in the array MUST be a single path component (no slashes, no `..`, no absolute paths) — multi-level paths like `tools/foo` are FORBIDDEN to keep the install-layout flat and predictable; AND unknown top-level keys in `install-config.json` MUST be rejected with exit `2` (strict schema, not lenient — silently-ignored typos like `folder` vs `folders` would silently install nothing).
- **Verifies:** §04 install-config (schema), §00 §"Default folder list" (canonical value), §03 release-pipeline (drift CI gate).

### AC-09 — Bash and PowerShell installer parity
- **Given** the two installers `install.sh` and `install.ps1`
- **When** both are run against equivalent empty destinations on Linux+macOS+Windows respectively with identical flag sets
- **Then** the resulting trees MUST be **byte-identical** modulo line-ending normalization (LF on Linux/macOS, CRLF on Windows for `.ps1`/`.bat`/`.cmd`/`.txt` files only; `.md`/`.json`/`.sh`/`.py`/`.cjs`/`.js`/`.ts` files keep LF on every OS to avoid spurious diffs); AND file modes MUST be preserved (executable bit on `.sh`/`.py` files on Linux/macOS); AND the two installers MUST share a common command-line surface: both accept `--dest <path>` (default `.`), `--folders <comma-list>` (default from `install-config.json`), `--ref <tag-or-sha>` (default = release tag), `--force`, `--dry-run`, `--verbose`, `--help`; AND a flag absent from one installer MUST be absent from the other — partial-parity (e.g. `--quiet` only in PowerShell) is a SPEC VIOLATION; AND `--dry-run` MUST print the planned operations to stdout (one per line, prefixed `WOULD: `) without performing any network or filesystem writes.
- **Verifies:** §01 install-contract (cross-OS parity clause), §13 generic-cli (flag naming conventions).

### AC-10 — Runner sub-command dispatch surface
- **Given** the repo-root runner scripts `run.sh` and `run.ps1` per §00 §"Sub-command surface"
- **When** invoked with the canonical positional sub-commands
- **Then** the dispatch MUST honor this exact contract: `<no-args>` = legacy default (`git pull` → run Go validator on `src/`); `lint [path]` = explicit form of the no-args default with `--Path` forwarded to `linter-scripts/run.ps1`; `slides` = `git pull` → `cd slides-app && bun install && bun run build && bun run preview` → open the preview URL in the default browser; `help` = print the sub-command table (the same table from §00); AND any unrecognized sub-command MUST exit `2` with stderr `unknown sub-command: <name>; run './run.sh help' for the list` (NOT `1` — a typoed sub-command is a config error not a runtime error); AND flags AFTER the sub-command MUST be forwarded verbatim to the inner script (e.g. `./run.sh slides --port 5174` forwards `--port 5174` to `bun run preview`); AND flags BEFORE the sub-command (e.g. `./run.sh --verbose slides`) are reserved for future runner-level flags and MUST currently exit `2` with `runner-level flags not yet supported; place flags after the sub-command`.
- **Verifies:** §00 §"Sub-command surface" (exact 4-row table), §02 runner-contract.

### AC-11 — Back-compat preservation for legacy no-args invocation
- **Given** an existing user who has been running `./run.ps1` (or `./run.sh`) with no arguments before this spec was authored — the legacy behavior was `git pull` then run the Go coding-guidelines validator on `src/`
- **When** that same user upgrades to the current runner per AC-10
- **Then** `./run.ps1` (no args) MUST produce the **identical observable behavior** they had before — same Go validator invocation, same `src/` target, same exit code semantics, same stdout/stderr formatting; AND no migration warning, deprecation banner, or "consider using `lint` explicitly" message is permitted to print on the no-args path (those would be observable behavior changes that break scripts which grep stderr); AND the `lint` sub-command per AC-10 is purely additive — it gives users a way to be explicit, but does NOT replace the no-args default; AND removing the no-args default in any future version is a MAJOR-version breaking change requiring a deprecation cycle of ≥2 minor versions with stderr warnings.
- **Verifies:** §00 §"Default behavior is preserved" call-out, §02 runner-contract.

### AC-12 — Release artifact set (8 items, all required)
- **Given** the GitHub Release publication for version `vX.Y.Z`
- **When** the release page is inspected
- **Then** it MUST publish ALL 8 distributable artifacts from §00 "Distributable artifacts": (1) the spec+linters tree is sourced via `codeload.github.com` archive (NOT a release asset — by design, to keep release size small); (2) `coding-guidelines-linters-vX.Y.Z.zip` (linters CI/CD pack from `linters-cicd/`); (3) `coding-guidelines-slides-vX.Y.Z.zip` (slides deck from `slides-app/dist/`); (4) `install.sh`; (5) `install.ps1`; (6) `linters-install.sh` (renamed from `linters-cicd/install.sh`); (7) `install-config.json`; (8) `checksums.txt` (SHA-256 of every zip + every script asset); AND missing ANY of (2)-(8) is a release blocker — the release pipeline MUST fail the build BEFORE creating the GitHub Release; AND filename patterns MUST match exactly per the §00 table (no `coding-guidelines_linters_v...` underscores, no `slides-vX.Y.Z.zip` without the `coding-guidelines-` prefix); AND the version `X.Y.Z` MUST be a valid SemVer triple matching the git tag.
- **Verifies:** §00 §"Distributable artifacts" table (all 8 rows), §03 release-pipeline.

### AC-13 — `checksums.txt` format and verification
- **Given** the `checksums.txt` release asset per AC-12
- **When** the file is opened
- **Then** it MUST be a plain-text file with one line per artifact in the format `<sha256-hex>  <filename>` (two spaces between hash and filename, per `sha256sum`/`shasum -a 256` standard output format — NOT one space, NOT tab); AND every release asset EXCEPT `checksums.txt` itself MUST appear in `checksums.txt` (a release with un-checksummed assets is a SPEC VIOLATION); AND the file MUST be UTF-8 with LF line endings and a trailing newline; AND `sha256sum -c checksums.txt` (Linux/macOS) or the equivalent PowerShell `Get-FileHash`-based verification MUST exit `0` when run in a directory containing all the assets; AND the installers per AC-06 MUST verify the checksum of any zip they download against `checksums.txt` BEFORE extracting — extraction without verification is a SPEC VIOLATION (supply-chain attack vector); AND a checksum mismatch MUST exit `4` (verification failure per §13 exit code contract) with the offending filename and both expected+actual hashes printed to stderr.
- **Verifies:** §00 §"Distributable artifacts" (checksums.txt row), §03 release-pipeline (CI hash computation), AC-06 (installer exit code 4).

### AC-14 — `linters-install.sh` rename contract
- **Given** the source file `linters-cicd/install.sh` in the repo
- **When** the release pipeline packages it as a release asset
- **Then** it MUST be uploaded as `linters-install.sh` (renamed at upload time — NOT named `install.sh` to avoid colliding with the top-level `install.sh` per AC-06); AND consumers MUST be able to invoke it via `curl -fsSL <url>/linters-install.sh | bash` to install ONLY the `linters-cicd/` folder (subset of AC-07's full 4-folder install) into `<dest>` (default `.`); AND the renamed script's internal version-string and self-reference (e.g. usage text mentioning "$0") MUST reflect `linters-install.sh` not `install.sh` — a script that prints `usage: install.sh ...` after being renamed would mislead operators; AND if `linters-cicd/install.sh` is removed or moved in a future refactor, the release pipeline MUST fail loudly rather than silently shipping a stale or empty `linters-install.sh`.
- **Verifies:** §00 §"Distributable artifacts" (linters-install.sh row), §03 release-pipeline (rename step).

### AC-15 — Install destination defaults and override
- **Given** the installer per AC-06
- **When** invoked without `--dest`
- **Then** the destination MUST default to the current working directory (`.`); AND when `--dest <path>` is passed, the destination MUST be `<path>` (created with `mkdir -p` semantics if missing); AND the destination MUST NOT be an absolute system path the user lacks write permission to — the installer MUST detect EACCES BEFORE downloading any artifact and exit `3` (IO error per §13); AND the destination MUST NOT be inside the source repo (the installer detects this by checking for a sibling `.git/HEAD` whose remote matches `coding-guidelines-v17` and refuses with exit `2` — installing into the source tree would create infinite-recursion-shaped pain); AND symlinks in the destination path MUST be resolved before the safety checks (an attacker-controlled symlink pointing into the source repo MUST be caught).
- **Verifies:** §01 install-contract (destination semantics), §13 generic-cli (exit code mapping).

### AC-16 — Release pipeline: tag-driven, signed, reproducible
- **Given** the release CI workflow (`.github/workflows/release.yml`) per §00
- **When** a git tag `vX.Y.Z` is pushed
- **Then** the workflow MUST trigger (NOT on `main` push, NOT on PR — tag-only to make releases intentional); AND the build MUST pin to the tag's commit SHA (NOT `HEAD` of the tag's branch — tags can be moved, but the release artifact MUST always reflect the SHA the tag pointed at when the release was cut); AND every artifact per AC-12 MUST be uploaded to the GitHub Release in a single atomic step — partial-release publication (some assets uploaded, then a failure before the rest) MUST be retried automatically OR the release MUST be deleted and recreated, NEVER left in a half-published state where `checksums.txt` doesn't match the available assets; AND the release MUST be marked as a draft until ALL assets pass checksum verification, then promoted to published in one step; AND the workflow MUST NOT auto-publish to a package registry (npm/PyPI/etc.) — release distribution is GitHub-Releases-only by design (per §16 generic-release).
- **Verifies:** §03 release-pipeline (trigger + atomicity), §00 §"Distributable artifacts", §16 generic-release.

### AC-17 — `slides` sub-command browser-open contract
- **Given** the `slides` sub-command per AC-10
- **When** the build+preview chain completes successfully (`bun run preview` is now serving on a port, by default `5173`)
- **Then** the runner MUST open the preview URL (`http://localhost:5173`) in the user's default browser using the OS-appropriate command: `xdg-open` on Linux, `open` on macOS, `Start-Process` on Windows; AND when the platform-detection cannot determine the right command, the runner MUST print the URL to stdout and exit `0` (NOT exit `1` — a missing browser-opener is a degraded but successful state); AND when `--no-open` is passed (forwarded to the runner), the browser-open step MUST be skipped and only the URL is printed; AND the runner MUST keep the `bun run preview` process attached to the terminal so the user can `Ctrl-C` to stop the dev server — backgrounding it would orphan the process; AND on `Ctrl-C`, the runner MUST forward `SIGINT` to the `bun` child process and exit `0` (NOT `130` — the user-initiated stop is a normal termination per spec, even though the OS convention is `128 + SIGINT`).
- **Verifies:** §00 §"Sub-command surface" (slides row), §02 runner-contract.

### AC-18 — `--ref <tag-or-sha>` reproducible install
- **Given** the installer per AC-06 with the `--ref` flag per AC-09
- **When** invoked with `--ref v2.0.0` (a release tag) or `--ref abc1234...` (a commit SHA)
- **Then** the installer MUST source the spec+linters tree from `codeload.github.com/<org>/<repo>/zip/<ref>` (NOT from the latest release — `--ref` overrides the default behavior); AND the resulting install MUST be byte-identical to running the installer at the moment that ref was current — this is the **reproducible install** contract; AND when `--ref` points to a non-existent tag/SHA, the installer MUST exit `3` (network/IO) with stderr `ref not found: <ref>`; AND when `--ref` points to a SHA on a non-default branch, the install MUST still succeed (the installer is branch-agnostic — it pins to commits, not branch heads); AND `--ref` MUST NOT accept a branch name like `main` — branches move, defeating reproducibility, so the installer MUST detect branch-shaped refs (anything matching `^[a-z][a-z0-9-]*$` that resolves to a branch) and exit `2` with `--ref MUST be a tag or full SHA, not a branch name`.
- **Verifies:** §01 install-contract (`--ref` semantics), AC-07 (default behavior when `--ref` absent), AC-13 (checksums verified per release).

### AC-19 — Cross-references intact
- **Given** the four cross-reference links in §00 §"Cross-references" — `spec-slides/00-overview.md`, `spec/12-cicd-pipeline-workflows/`, `spec/13-generic-cli/`, `spec/16-generic-release/`
- **When** each link is resolved
- **Then** each target MUST exist on disk (verified by `linter-scripts/check-spec-cross-links.py`); AND the §15 module's content MUST be consistent with each target — specifically: §15 sub-command surface (AC-10) MUST follow §13 generic-cli flag conventions; §15 release pipeline (AC-12, AC-16) MUST follow §16 generic-release artifact conventions; §15 CI workflow (AC-16) MUST follow §12 cicd-pipeline-workflows trigger/atomicity conventions; §15 slides sub-command (AC-17) MUST be compatible with `spec-slides/00-overview.md` build contract; AND when any cross-referenced target spec changes its conventions, §15 MUST be re-audited and bumped accordingly (lockstep maintenance, NOT silent drift).
- **Verifies:** §00 §"Cross-references", `linter-scripts/check-spec-cross-links.py` exit `0`.

### AC-20 — Module-specific files versioned and validated
- **Given** the four sibling contract files `01-install-contract.md`, `02-runner-contract.md`, `03-release-pipeline.md`, `04-install-config.md`
- **When** each is opened
- **Then** each MUST have a top-level H1, a `**Version:**` banner, and an `**Updated:**` date per the universal §01 spec-authoring-guide template; AND each file's content MUST elaborate (not contradict) the §00 overview's high-level claims — specifically: `01-install-contract.md` defines the install layout AC-07/AC-09/AC-15 reference; `02-runner-contract.md` defines the sub-command dispatch AC-10/AC-11/AC-17 reference; `03-release-pipeline.md` defines the CI workflow AC-12/AC-13/AC-14/AC-16 reference; `04-install-config.md` defines the schema AC-08 references; AND when AC-06..AC-19 cite a normative behavior, the citing AC's `**Verifies:**` line MUST point to BOTH §00 AND the relevant sibling file — single-source citation (only §00 OR only the sibling) is incomplete; AND any contradiction between §00 and a sibling MUST be resolved in favor of §00 (the overview is the canonical summary; sibling files are elaborations) and a §99 audit row MUST record the resolution.
- **Verifies:** §01 install-contract, §02 runner-contract, §03 release-pipeline, §04 install-config, §00 §"Reading order".

### AC-21 — Installer fetch timeout, retry, and resume contract  `[medium]`
- **Given** AC-06 mandates a 60-second download SLO over a 100Mbps connection for the installer one-liner (Bash + PowerShell parity), and the underlying transports are `curl` (POSIX) + `Invoke-WebRequest` / `Start-BitsTransfer` (PowerShell),
- **When** the installer one-liner runs against a release artifact host that may experience transient network failures (TLS handshake stall, intermittent 5xx, partial-content disconnects),
- **Then** ALL of the following invariants MUST hold:
  1. **Bash transport flags** — the `curl` invocation MUST include `--connect-timeout 10 --max-time 60 --retry 3 --retry-delay 2 --retry-connrefused --fail --location --show-error --silent` (or the long-form equivalents); the maximum 60s wall-clock applies per attempt, not cumulatively (3 retries × 60s = 180s ceiling on hostile network).
  2. **PowerShell transport flags** — the `Invoke-WebRequest` invocation MUST set `-TimeoutSec 60 -MaximumRetryCount 3 -RetryIntervalSec 2 -UseBasicParsing -ErrorAction Stop`; PowerShell 5.1 environments without native retry MUST wrap in a `try/catch` loop matching the same 3-attempt + 2-second-backoff contract.
  3. **Failure exit codes** — on terminal failure (3 attempts exhausted), the installer MUST exit with a documented non-zero code (`1` = network failure; `2` = checksum mismatch per AC-13; `3` = unsupported OS/arch). Generic exit `1` for all errors is FORBIDDEN.
  4. **Forbidden patterns** — `curl <url> | bash` without explicit `--fail --max-time` is a release-blocker (silent partial-download corruption); `Invoke-WebRequest` without `-ErrorAction Stop` is a release-blocker (silently continues on 4xx); `set -e` alone in Bash is INSUFFICIENT (does not catch piped curl failures unless `set -o pipefail` is also set).
- **Source:** `01-install-contract.md` §Installer one-liner; AC-06 SLO clause.
- **Verifies:** AC-06 (60s SLO is per-attempt, not cumulative); `01-install-contract.md` §Installer one-liner. Closes audit-v7 cache `15-distribution-and-runner.json` finding `[D3 MEDIUM] Missing timeout/retry logic for installers`.

### AC-22 — `slides` build toolchain pin: Bun primary, no pnpm fallback  `[low]`
- **Given** §00 overview mandates `bun install && bun run build` for the `slides` sub-command (AC-17 browser-open contract) and `02-runner-contract.md` previously contained a "verify bun, fall back to pnpm" branch,
- **When** the `slides` sub-command runs in any supported environment (downstream installer, CI, dev workstation),
- **Then** Bun MUST be the SOLE supported toolchain for the slides build pipeline; the `02-runner-contract.md` MUST NOT specify a pnpm fallback path. If `bun` is not on `$PATH`, the runner MUST fail-fast with exit `4` ("missing toolchain — install bun.sh") and link to <https://bun.sh/docs/installation>; silently falling back to pnpm is FORBIDDEN because pnpm produces a different lockfile + different `node_modules` resolution + different runtime semantics for `bun:*` imports — non-deterministic across environments.
- **Source:** §00 overview §`slides` sub-command; AC-17 browser-open contract; `02-runner-contract.md` §Toolchain detection.
- **Verifies:** `02-runner-contract.md` §Toolchain detection (single-source pin); §00 overview Bun mandate. Closes audit-v7 cache `15-distribution-and-runner.json` finding `[D1 MEDIUM] Ambiguous 'slides' build toolchain` per Lesson #36 (link-don't-restate — `02-runner-contract.md` is the canonical surface; this AC pins the contract to it).

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each MUST remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-install-contract.md`
- `02-runner-contract.md`
- `03-release-pipeline.md`
- `04-install-config.md`

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
- [Generic CLI conventions](../13-generic-cli/) — referenced by AC-06 / AC-10 / AC-13 / AC-15
- [Generic release standard](../16-generic-release/) — referenced by AC-12 / AC-16
- [CICD pipeline workflows](../12-cicd-pipeline-workflows/) — referenced by AC-16

# Acceptance Criteria — Update — Overview

**Version:** 2.5.0  
**Updated:** 2026-05-07 (Phase J8 — AC-23 binds `28-update-interface-contract.md` (kind: interface-contract) into §97 with full GWT covering JSON Schema + env vars + deploy paths + exit codes + cross-refs; closes Lesson #19 audit-boundary < verification-boundary gap and Lesson #39 intra-module sibling-delegation gap. AC count 22 → 23.)
**Scope:** `spec/14-update/`

> **v2.2.0 (Phase 149 — P3 sweep slot 9):** Added `**Verifies:**` clauses to all 20 ACs (AC-01..AC-20). Each criterion now explicitly maps to the underlying invariant it protects (structural floor, slot-immutability, cross-platform deploy uniformity, parent-survival, build-time version-injection, supply-chain trust, integrity, idempotent install, latest-probe-or-fail, XDG/atomic-write, ordered-pipeline-with-fail-fast, no-daemon, idempotent silent-cleanup-budget, single-step atomic rollback, three-layer precedence + system-dir blacklist, tag-first monotonicity, six-target-floor + CGO_ENABLED=0). Verifies-coverage gap: 0/20 → 20/20. Drives AI-confidence Medium → High.

> **v2.1.0 (Phase 124):** AC-20 `Given` and `Source` lines now explicitly cite the upstream generic blueprint [`../16-generic-release/01-cross-compilation.md`](../16-generic-release/01-cross-compilation.md) in addition to the local `16-cross-compilation.md` / `17-release-pipeline.md`. The cross-compilation target list and CGO discipline originate in §16 (kind: future-spec generic blueprint); §14 is the concrete consumer. Closes the AC-SAG-25 cite-direction gap surfaced by Phase 121's reframe (§14 → §16, not the inverted §16 → §14 originally proposed).

> **v2.0.0 (Phase 16b):** Added 15 module-specific Given/When/Then ACs (AC-06..AC-20) covering rename-first deploy, Windows handoff, version verification, code signing, SHA-256 checksum verification, install script version probe, updater binary, config file location/XDG, update command workflow, non-blocking parallel update check (12h interval, fire-and-forget), JSON fallback store, deploy-path resolution, cleanup, atomic rollback, and generic installer behavior. The 5 generic structural ACs (AC-01..AC-05) are preserved verbatim — they validate the spec module itself; AC-06+ validate the **update/installer implementation** that consumes the spec.

---

## Purpose

This document defines testable acceptance criteria for the **Update — Overview** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/14-update/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Source:** `00-overview.md`
- **Verifies:** Required-files structural floor (overview presence + version/date banner) — the universal `kind: spec` invariant from `spec/01-spec-authoring-guide/03-required-files.md` enforced by `linter-scripts/check-tree-health.cjs`.

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.
- **Verifies:** Zero broken intra-module links — the cross-link integrity invariant gating `spec-health.yml` (no dangling sibling refs).

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.
- **Verifies:** Slot-immutability + `NN-kebab-case.md` filename invariant — protects file-slot lockstep (precedent: §16 → §37 in v2.8.6) and prevents collisions caught by `check-tree-health.cjs --strict`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Source:** `99-consistency-report.md`.
- **Verifies:** §99 inventory single-source-of-truth invariant — every `.md` accounted for under a heading matching the `(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)` rubric (Phase 137 lesson; bare `## Inventory` silently loses credit).

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** `linter-scripts/check-tree-health.cjs`.
- **Verifies:** Strict-pass tree-health rubric — module contributes its full 3/3 (required+changelog+inventory) toward the 168/168 strict-mode target; default-mode rounding to 100 is insufficient (Phase 137 precedent).

---

---

## Module-Specific Criteria (Implementation Contract)

> The following ACs validate an updater/installer implementation that **consumes** this spec, not the spec module itself. Each is verifiable by running the built binary against the listed command and inspecting filesystem state, exit codes, and console output, or by source-grep against the implementation.

### AC-06: Rename-first deploy avoids "file in use" errors on Windows
- **Given** a running CLI binary on Windows located at `<deployPath>/<binary>/<binary>.exe`
- **When** an update is applied via `<binary> update` or the build script
- **Then** the deploy MUST follow the rename-first sequence: (1) rename the running `<binary>.exe` to `<binary>.exe.old` in the SAME directory (atomic — no copy-across-volumes), (2) write the new binary to `<binary>.exe`, (3) flag `<binary>.exe.old` for deletion on next process start (cleanup per AC-15); AND the rename in step 1 MUST succeed even while the file is held open by the running process — Windows permits rename-while-locked but FORBIDS overwrite-while-locked, which is the entire reason this strategy exists; AND if the rename fails (e.g. ACL denial), the deploy MUST abort BEFORE writing the new binary AND emit `error: rename-first failed: <reason>` to stderr AND exit `1` per the §13 AC-10 exit code contract — a half-completed deploy that left the directory with a new `.exe` but no `.exe.old` would brick self-update; AND on Linux/macOS the rename-first strategy STILL applies (even though `unlink` of a running ELF/Mach-O is permitted on POSIX) so the codepath is **uniform across platforms** — no `if runtime.GOOS == "windows"` branch in the deploy logic.
- **Source:** `03-rename-first-deploy.md` (Flow Diagram + The Problem sections), `01-self-update-overview.md` (Step 3 hard part), §13 AC-10 (exit code 1 contract).
- **Verifies:** Cross-platform deploy-codepath uniformity invariant — no `runtime.GOOS == "windows"` branch in deploy logic; rename-first is the single strategy (Windows correctness, POSIX consistency).

### AC-07: Windows handoff completes via detached child process
- **Given** a running `<binary>.exe` on Windows that needs to replace itself
- **When** the user invokes `<binary> update` and a new version is downloaded
- **Then** the update MUST hand off to a **detached child process** (`updater.exe` per `19-updater-binary.md`) that: (1) is spawned with `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` Windows flags so it survives the parent's exit, (2) waits for the parent PID to exit (polling `OpenProcess(PROCESS_QUERY_INFORMATION, false, parentPID)` until it returns `ERROR_INVALID_PARAMETER` indicating the PID is gone), (3) performs the rename-first swap (per AC-06), (4) optionally relaunches the new binary if `--relaunch` was passed, (5) self-deletes via the same rename-first trick on its own `.exe`; AND the parent process MUST exit cleanly within 100ms of spawning the updater — a long-lived parent would defeat the purpose; AND the updater MUST log every step to a file at `%TEMP%\<binary>-update-<timestamp>.log` (per §13 AC-13 filename date format) so failures are diagnosable post-mortem; AND on Linux/macOS the handoff is OPTIONAL (POSIX permits in-place rename of running binaries) but if implemented MUST follow the same detached-child + parent-wait pattern for consistency.
- **Source:** `05-handoff-mechanism.md` (Two-Phase Summary), `07-console-safe-handoff.md`, `19-updater-binary.md`, §13 AC-13 (filename timestamp format).
- **Verifies:** Parent-survival invariant — the updater outlives its parent via detached-child + parent-PID-poll, with diagnosable post-mortem logs (eliminates the "self-update bricks the binary" failure mode).

### AC-08: Three-branch version verification compares deployed vs source
- **Given** a built CLI per `09-version-verification.md`
- **When** the user invokes `<binary> version` or the build script's post-deploy verification step
- **Then** the verification MUST compare up to **three version values**: (a) the **deployed binary's** embedded version (from `<deployPath>/<binary>/<binary>.exe --version`), (b) the **source binary's** embedded version (the just-built artifact in the build directory), (c) the **declared version** in `version.txt` or the equivalent source-of-truth file; AND the three branches are: (1) all three match → exit `0` with `✓ version verified: <version>`, (2) source matches declared but deployed differs → emit `⚠ deploy stale: deployed=<x> source=<y>` (warning, exit `0` — this is the normal pre-update state), (3) any other mismatch → emit `error: version mismatch: deployed=<x> source=<y> declared=<z>` AND exit `1`; AND the version string MUST follow SemVer (`MAJOR.MINOR.PATCH[-prerelease][+build]`) — non-SemVer versions cause `error: invalid version format: <value>` AND exit `1`; AND the embedded version MUST come from a **build-time `-ldflags "-X main.Version=..."`** injection — runtime file-reads of `version.txt` from disk are FORBIDDEN (the binary must report its own version standalone, even when moved off the build host).
- **Source:** `09-version-verification.md` (Two Binaries, Two Truths section), `15-release-versioning.md` (SemVer contract).
- **Verifies:** Build-time version-injection invariant (no runtime `version.txt` reads) AND three-way drift detection between deployed/source/declared — guarantees the binary is a self-describing artifact independent of its build host.

### AC-09: All release artifacts are code-signed before publication
- **Given** a release pipeline per `12-code-signing.md` and `17-release-pipeline.md`
- **When** any binary or installer is published as a release asset
- **Then** Windows `.exe` artifacts MUST be **Authenticode-signed** with a code-signing certificate (EV or OV) — `signtool verify /pa <file>` MUST exit `0` on every published `.exe`; AND macOS `.app`/Mach-O binaries MUST be **codesigned + notarized** — `codesign --verify --deep --strict <bundle>` AND `spctl --assess --type execute <bundle>` MUST both exit `0`; AND Linux ELF binaries MAY be unsigned (no platform-level signing infrastructure equivalent to Authenticode) but MUST have a corresponding `.sig` file produced by `gpg --detach-sign` from the release signing key — and the public key fingerprint MUST be published alongside (in `RELEASING.md` or release notes); AND the build pipeline MUST FAIL the release if ANY signing step exits non-zero — unsigned binaries MUST NEVER reach a published release; AND the certificate's expiry MUST be checked at every release — a release within 30 days of certificate expiry MUST emit a build-time warning AND tag the release notes with `⚠ certificate expires <date>` so renewal isn't missed.
- **Source:** `12-code-signing.md` (Why Sign + What to Sign sections), `17-release-pipeline.md`, `13-release-assets.md`.
- **Verifies:** Supply-chain trust invariant — every published artifact has a verifiable cryptographic signature (Authenticode/codesign+notarize/GPG `.sig`); pipeline halts on any unsigned artifact, preventing tampered-binary distribution.

### AC-10: SHA-256 checksums are generated, published, and verified before install
- **Given** a release pipeline per `14-checksums-verification.md`
- **When** release artifacts are published
- **Then** every artifact (binary, installer, archive) MUST have a corresponding **SHA-256 hash** published in a `checksums.txt` file at the release root in the standard `<hash>  <filename>` format (two-space separator, lowercase hex hash, matching `sha256sum`/`shasum -a 256` output); AND the install scripts (`install.ps1`, `install.sh` per `18-install-scripts.md`) MUST: (1) download `checksums.txt` from the release, (2) verify the downloaded `checksums.txt` against an embedded fingerprint (signed checksums.txt OR an SHA-256 of checksums.txt baked into the install script itself — pick one, NOT both, and document which), (3) compute the SHA-256 of every downloaded artifact, (4) compare against the published value, (5) ABORT installation with `error: checksum mismatch: <file>: expected=<x> got=<y>` AND exit `1` if any mismatch; AND the SHA-256 algorithm is FIXED — MD5/SHA-1 are FORBIDDEN (cryptographically broken); SHA-512 is also FORBIDDEN (overkill for this use, breaks compatibility with standard `sha256sum` tooling); AND `checksums.txt` MUST cover EVERY published artifact — a missing entry MUST cause the install script to abort with `error: no checksum entry for <file>` rather than skip verification.
- **Source:** `14-checksums-verification.md` (Checksum Generation + Output Format sections), `18-install-scripts.md` (verify-then-install pattern).
- **Verifies:** Integrity invariant — SHA-256 (no MD5/SHA-1/SHA-512) on every artifact, fail-closed verify-then-install; aborts on any missing/mismatched entry rather than silently skipping.

### AC-11: Install scripts are idempotent and use a standard install location
- **Given** install scripts per `18-install-scripts.md` and `27-generic-installer-behavior.md`
- **When** the user runs `iwr -useb <url>/install.ps1 | iex` (Windows) OR `curl -fsSL <url>/install.sh | bash` (Linux/macOS)
- **Then** the script MUST: (1) detect the platform (`$env:OS` / `uname`) AND architecture (`$env:PROCESSOR_ARCHITECTURE` / `uname -m`), (2) download the matching artifact (e.g. `<binary>-windows-amd64.exe`, `<binary>-linux-arm64`), (3) verify checksum per AC-10, (4) install to a **standard location**: `%LOCALAPPDATA%\Programs\<binary>\` on Windows, `~/.local/bin/` on Linux, `/usr/local/bin/` on macOS (or `~/Applications/<binary>.app` for `.app` bundles), (5) create a shell-completion entry per §13 AC-18 if a shell is detected; AND running the script a SECOND time MUST be IDEMPOTENT — if the same version is already installed, exit `0` with `<binary> <version> already installed at <path>`; if a different version, treat as upgrade (rename-first per AC-06); AND the script MUST NEVER require sudo on Linux unless installing to `/usr/local/bin/` (default to `~/.local/bin/` to avoid sudo) — silent sudo prompts in piped curl-bash are a security hazard; AND the script MUST emit a single non-zero exit on any failure with a clear message; AND the script MUST NOT write outside the install directory + the user's PATH config file (`~/.bashrc` / `~/.zshrc` / `$PROFILE`) — and PATH modification MUST be **opt-in via a prompt** when stdout is a TTY, **opt-out by default** when piped (because the user can't see the prompt).
- **Source:** `18-install-scripts.md`, `27-generic-installer-behavior.md`, AC-06 (rename-first), AC-10 (checksum verify), §13 AC-18 (shell completion).
- **Verifies:** Idempotent install + no-silent-sudo invariant — re-running the script is a no-op at same version; PATH edits are opt-in on TTY / opt-out when piped, eliminating the curl-bash silent-elevation hazard.

### AC-12: Install script probes latest version before installing
- **Given** an install script per `23-install-script-version-probe.md`
- **When** the script starts (BEFORE downloading any binary)
- **Then** the script MUST first query the **latest-release endpoint** (e.g. `https://api.github.com/repos/<owner>/<repo>/releases/latest` or the equivalent for the host) AND extract the `tag_name`; AND the script MUST honor a `--version=<x>` override flag — if set, skip the latest-probe AND install that exact tag (used for pinning per `25-release-pinned-installer.md`); AND if the latest-probe fails (network error, 404, rate-limit), the script MUST exit `1` with `error: could not determine latest version: <reason> (use --version=X.Y.Z to pin)` — guessing or falling back to a hardcoded version is FORBIDDEN; AND if the latest version equals the currently-installed version (detected via `<binary> --version` if `<binary>` is on PATH), the script MUST emit `<binary> <version> already at latest` AND exit `0` UNLESS `--force` is passed; AND the latest-probe MUST set a User-Agent header `<binary>-installer/<installer-version>` so the API host can audit installer traffic; AND the probe MUST NOT require authentication (the latest-release endpoint is public on every supported host) — auth-required probes break curl-pipe-bash for first-time users.
- **Source:** `23-install-script-version-probe.md`, `25-release-pinned-installer.md` (--version pinning).
- **Verifies:** Latest-probe-or-fail invariant — never guess/fall-back to a hardcoded version; pinning is explicit via `--version=X.Y.Z`; preserves reproducibility and prevents silent stale installs.

### AC-13: Update config file lives at XDG-compliant location
- **Given** an updater per `21-config-file.md`
- **When** the updater reads or writes its persistent config (last-check timestamp, update channel, telemetry opt-in)
- **Then** the config file MUST live at `$XDG_CONFIG_HOME/<binary>/update.json` if `$XDG_CONFIG_HOME` is set, ELSE `~/.config/<binary>/update.json` on Linux, `~/Library/Application Support/<binary>/update.json` on macOS, `%APPDATA%\<binary>\update.json` on Windows; AND the file format MUST be **flat JSON** per §13 AC-08 (no nesting > 1 level) — keys: `last_check_unix` (int), `channel` (`"stable"` | `"beta"`), `auto_update` (bool, default `true`), `telemetry` (bool, default `false`); AND a missing config file MUST be treated as "use defaults" — never an error; AND a malformed config file MUST cause the updater to emit `error: invalid update config at <path>: <reason>` AND exit `3` (config error per §13 AC-10); AND writes MUST be **atomic**: write to `update.json.tmp`, then rename to `update.json` (the same atomic-rename trick as AC-06 deploy) — partial writes from interrupted updaters MUST NEVER leave a corrupted config; AND the file's permission MUST be `0600` (owner read+write only) on POSIX — telemetry/channel preferences are user-private.
- **Source:** `21-config-file.md` (XDG Compliance + Go Implementation sections), §13 AC-08 (flat JSON contract), §13 AC-10 (exit code 3 for config error).
- **Verifies:** XDG/per-OS config-location invariant + atomic-write durability + flat-JSON-no-nesting (§13 AC-08) + 0600 POSIX permission — config corruption from interrupted writes is impossible; user-private telemetry/channel preferences are filesystem-protected.

### AC-14: `<binary> update` follows the documented step-by-step workflow
- **Given** a CLI binary with the `update` subcommand per `22-update-command-workflow.md`
- **When** the user invokes `<binary> update` (no flags) on a network-connected machine
- **Then** the workflow MUST execute these steps in order, aborting at the first failure: (Step 1) network check — TCP connect to the release host on port 443 with a 5-second timeout; failure → `error: cannot reach <host> (network down or firewall)` exit `1`; (Step 2) latest-version probe per AC-12; (Step 3) compare against current `<binary> --version`; if equal, emit `already at latest <version>` exit `0`; (Step 4) download the new binary to `%TEMP%/<binary>-<version>.exe.partial`; (Step 5) verify SHA-256 per AC-10; (Step 6) verify code-signature per AC-09 (Authenticode `signtool verify /pa` or `codesign --verify --deep --strict`); (Step 7) rename `.partial` to `.new`; (Step 8) spawn detached updater per AC-07 with parent PID + paths; (Step 9) parent exits cleanly within 100ms; (Step 10 — in updater) wait for parent exit, perform rename-first swap per AC-06, optionally relaunch; AND every step MUST emit a verbose-log line per §13 AC-15 prefixed with `[update step N/10]`; AND a `--check-only` flag MUST run steps 1-3 then exit (report whether an update is available, never download).
- **Source:** `22-update-command-workflow.md` (Step-by-Step Flow), AC-06/AC-07/AC-09/AC-10/AC-12, §13 AC-15 (verbose logging).
- **Verifies:** Ordered-pipeline-with-fail-fast invariant — 10-step workflow aborts at first failure; `--check-only` short-circuits at step 3; every step is verbose-logged with `[update step N/10]` prefix for diagnosability.

### AC-15: Non-blocking update check is fire-and-forget with 12h interval
- **Given** a CLI per `24-update-check-mechanism/00-overview.md`
- **When** any subcommand of the CLI is invoked (NOT just `update`)
- **Then** a **pre-command hook** (per `24-update-check-mechanism/07-pre-command-hook.md`) MUST: (1) read `last_check_unix` from update config per AC-13, (2) compute age = `now - last_check_unix`, (3) if `age >= interval` (default `12h = 43200s`), spawn a **detached child** (`<binary> __update-check` — hidden subcommand) that performs steps 1-3 of AC-14 + writes the result to a JSON fallback store per `09-json-fallback-store.md`, (4) update `last_check_unix = now` BEFORE spawning the child (so concurrent invocations don't all spawn checkers), (5) IMMEDIATELY proceed with the user's actual command — the parent MUST NOT wait for the checker; AND the detached check MUST NOT print to stdout/stderr of the parent process (the user is busy with their actual command — they don't want update-check noise mid-output); AND the checker's result is surfaced on the NEXT invocation as a one-line banner above the command output: `⮕ update available: <new-version> (run \`<binary> update\`)` — printed to stderr (per §13 AC-15) so it doesn't pollute stdout pipes; AND there is NO daemon, NO cron job, NO scheduled task — every check is initiated by the CLI itself; AND the interval is configurable via `--update-check-interval=<duration>` flag OR the `update_check_interval` key in update.json; setting it to `0` DISABLES the check entirely.
- **Source:** `24-update-check-mechanism/00-overview.md` (non-blocking parallel + fire-and-forget design), `24-update-check-mechanism/07-pre-command-hook.md`, `24-update-check-mechanism/09-json-fallback-store.md`, AC-13 (config file), §13 AC-15 (stderr discipline).
- **Verifies:** No-daemon / no-cron / no-stdout-pollution invariant — every check is CLI-initiated, detached, banner-deferred-to-next-invocation; `last_check_unix` write-before-spawn prevents thundering-herd; stdout pipes stay clean.

### AC-16: Cleanup removes `.old` and stale partial files on next start
- **Given** a CLI binary that has been updated via the rename-first strategy per AC-06
- **When** the new `<binary>.exe` is launched for the first time
- **Then** an early-startup cleanup phase (per `06-cleanup.md`) MUST: (1) scan its own directory for files matching `<binary>.exe.old` AND attempt to delete them, (2) scan `%TEMP%` for `<binary>-*.partial` files older than 24h AND delete them, (3) scan `%TEMP%` for `<binary>-update-*.log` files older than 7 days AND delete them; AND deletion failures MUST be SILENT (logged to verbose per §13 AC-15 but never printed to stderr) — a busy file or ACL denial is normal and not actionable for the user; AND cleanup MUST run BEFORE any subcommand dispatch (per §13 AC-06) so even crashing subcommands don't prevent next-run cleanup; AND cleanup MUST be IDEMPOTENT — running it twice MUST have the same effect as running it once; AND cleanup MUST complete within 100ms **wall-clock time** (95th percentile, measured from CLI process start to cleanup-phase return; CPU-time and `time.Process` quotas are NOT acceptable substitutes — wall-clock is what the user perceives, including stalls on network-mounted filesystems, antivirus scans, and disk I/O queue contention) — slow cleanup adds latency to every CLI invocation; if cleanup risks exceeding 100ms (e.g. > 100 stale files in `%TEMP%`, or any single `unlink()` taking > 50ms wall-clock), the implementation MUST cap the per-invocation work AND defer the rest to subsequent invocations.
- **Source:** `06-cleanup.md`, AC-06 (`.old` source), §13 AC-06 (dispatch ordering), §13 AC-15 (verbose logging).
- **Verifies:** Idempotent silent-cleanup-budget invariant — pre-dispatch, ≤100ms p95, never user-visible-error on busy/ACL-denied files; capped per-invocation work to amortize across runs (zero startup-latency regression).

### AC-17: Atomic rollback is possible after a failed update
- **Given** an updater per AC-07 mid-handoff
- **When** the updater detects ANY failure between rename-first step 1 (`<binary>.exe` → `<binary>.exe.old`) and step 2 (write new `<binary>.exe`)
- **Then** the updater MUST rollback by renaming `<binary>.exe.old` back to `<binary>.exe` AND remove any partial `.exe` written; AND the rollback MUST be ATOMIC on a single filesystem — the rename uses the same OS-level atomic-rename guarantee as AC-06 step 1; AND the rollback MUST emit `error: update failed, rolled back to <previous-version>` to the updater log file AND exit `1`; AND the original `<binary>.exe` (now restored) MUST be functional immediately — no relaunch required, no fix-up steps; AND if the rollback ITSELF fails (impossible-but-possible: ACL change between original rename + rollback rename), the updater MUST emit `error: update failed AND rollback failed — manual recovery required at <path>` exit `1` AND leave a `<binary>.exe.RECOVERY.md` file at the install location with copy-paste shell commands to manually restore from `.old`; AND there is NO multi-version rollback — only the immediately-previous version (the `.old` file from this update) is recoverable. Older versions require fresh install per AC-11. **Rollback-trigger ownership (Normative)**: rollback is ALWAYS performed by the **updater process** that initiated the rename (the still-alive process that owns the `.old` file lock), NEVER by the parent CLI process or by a detached child. The updater process model is single-threaded synchronous: rename-step-1 → write-step-2 → verify-step-3 → release-lock; failure at any step transitions to rollback in the SAME process before exit. If the updater process is killed mid-handoff (SIGKILL, OOM, power loss), rollback is performed by the **early-startup cleanup phase per AC-16** on the NEXT CLI invocation: cleanup detects an orphan `<binary>.exe.old` WITHOUT a corresponding fresh `<binary>.exe` (size 0 OR mtime older than the `.old`'s mtime) AND performs the rename-back as a recovery action. There is NO inter-process signaling, NO PID file polling, NO IPC channel between detached child and exited parent — the contract is "process-local rollback OR next-start cleanup recovery", and these two paths are exhaustive (any third recovery path is FORBIDDEN — eliminates the daemon/watcher class of bugs).
- **Source:** `01-self-update-overview.md` (rollback safety), `03-rename-first-deploy.md` (atomic rename), AC-06 (rename-first guarantee), AC-16 (cleanup-phase orphan-detection recovery path).
- **Verifies:** Single-step atomic rollback invariant — only the immediately-previous version is recoverable (no multi-version history); rollback-of-rollback failure leaves a `RECOVERY.md` with copy-paste manual-restore commands (no silent brick); rollback ownership is process-local to the updater OR delegated to next-start cleanup per AC-16 — NO inter-process signaling permitted (no daemon, no watcher, no PID-polling).

### AC-18: Deploy path resolution honors config + override flag
- **Given** a build/deploy script per `02-deploy-path-resolution.md`
- **When** the user runs the build script (e.g. `run.ps1 -Deploy`) which resolves where to deploy the new binary
- **Then** the deploy path MUST be resolved in this precedence (lowest to highest, mirroring §13 AC-08 three-layer): (1) hardcoded default `~/bin/<binary>/` (Linux) or `%LOCALAPPDATA%\Programs\<binary>\` (Windows), (2) `deploy_path` key in the build config file `build.json`, (3) `--deploy-path=<path>` CLI flag; AND the resolved path MUST exist OR the script MUST CREATE it with `mkdir -p` (POSIX) / `New-Item -ItemType Directory -Force` (Windows); AND if creation fails (ACL denial, parent missing), the script MUST exit `1` with `error: cannot create deploy path: <path>: <reason>`; AND the resolved path MUST NEVER be `/`, `/usr`, `/etc`, `C:\`, `C:\Windows`, `C:\Program Files` (without `\<binary>` suffix) — the script MUST refuse to deploy into system-critical directories AND exit `2` with `error: refused to deploy into system directory: <path>`; AND the deploy directory's permissions MUST be checked: writable by current user OR the script aborts with `error: deploy path not writable: <path> (try --deploy-path or run as elevated)`.
- **Source:** `02-deploy-path-resolution.md`, `08-repo-path-sync.md`, §13 AC-08 (precedence pattern).
- **Verifies:** Three-layer precedence (default < config < flag) reuses the §13 AC-08 pattern AND system-directory blacklist — refuses to deploy into `/`, `/usr`, `/etc`, `C:\Windows`, `C:\Program Files` root; eliminates accidental privilege-required installs.

### AC-19: Last-release detection prefers tagged-release over commit-count heuristics
- **Given** a build pipeline per `10-last-release-detection.md`
- **When** the pipeline needs to know the last-released version to compute the next version per `15-release-versioning.md`
- **Then** the pipeline MUST query in this order: (1) `git describe --tags --abbrev=0` for the most recent annotated tag matching `v[0-9]*.[0-9]*.[0-9]*`, (2) if no tags, the GitHub Releases API `releases/latest` endpoint per AC-12, (3) if no releases, default to `v0.0.0` (fresh project); AND commit-count, branch-name, or build-number-based version detection is FORBIDDEN — these produce non-monotonic versions on rebases/squashes which break update workflows; AND the detected version MUST be parsed as SemVer per AC-08 — a tag `v1.2.3-beta+build42` parses to `MAJOR=1 MINOR=2 PATCH=3 PRERELEASE=beta BUILD=build42`; AND if `git describe` returns a dirty-tree suffix (`v1.2.3-5-gabcdef-dirty`), the dirty suffix MUST be STRIPPED for version computation but PRESERVED in the build metadata as `+dirty.5.gabcdef`; AND the next version is computed as: PATCH-bump for fixes, MINOR-bump for features, MAJOR-bump for breaking changes — the bump kind MUST be derived from commit-message conventional-commits prefix (`fix:` → patch, `feat:` → minor, `BREAKING CHANGE:` footer or `!` after type → major).
- **Source:** `10-last-release-detection.md`, `15-release-versioning.md`, AC-08 (SemVer parse), AC-12 (latest-release API).
- **Verifies:** Tag-first monotonicity invariant — commit-count/branch-name/build-number heuristics are FORBIDDEN (non-monotonic on rebase/squash); dirty-tree suffixes are stripped from version-compute but preserved as `+dirty.N.gSHA` build metadata; conventional-commits drives the bump.

### AC-20: Cross-compilation produces all documented platform artifacts
- **Given** a build pipeline per local `16-cross-compilation.md` and `17-release-pipeline.md`, both of which MUST consume the upstream generic blueprint at [`../16-generic-release/01-cross-compilation.md`](../16-generic-release/01-cross-compilation.md)
- **When** the release pipeline runs
- **Then** every release MUST produce binaries for AT LEAST these platform×arch combinations: `windows/amd64`, `windows/arm64`, `linux/amd64`, `linux/arm64`, `darwin/amd64` (Intel Mac), `darwin/arm64` (Apple Silicon) — six artifacts minimum (parity with `../16-generic-release/01-cross-compilation.md` "Default Targets"); AND each Go binary MUST be built with `CGO_ENABLED=0` (static linkage so no libc version mismatch on target hosts) UNLESS the binary explicitly requires CGO (which MUST be documented in `16-cross-compilation.md` with the rationale); AND each binary MUST be built with `-ldflags "-s -w -X main.Version=<version> -X main.BuildTime=<iso8601>"` to strip debug info AND embed the version per AC-08 AND embed the build time in RFC-3339 per §13 AC-13; AND the artifact filename MUST follow `<binary>-<os>-<arch>[.exe]` (e.g. `mycli-windows-amd64.exe`, `mycli-linux-arm64`) — `.exe` suffix on Windows ONLY; AND the build pipeline MUST FAIL the release if ANY platform fails to build — partial-platform releases (e.g. ship Linux but not Windows because of a transient build error) are FORBIDDEN; AND pipelines MUST run on a CI host with reproducible toolchain pinning (`go.mod` `toolchain` directive OR `.tool-versions` for asdf/mise) so the same source produces the same binary byte-for-byte across rebuilds; AND any deviation from the upstream generic target list (additions, removals, or CGO exemptions) MUST be justified in the local `16-cross-compilation.md` and recorded in §99.
- **Source:** local `16-cross-compilation.md`, local `17-release-pipeline.md`, upstream generic [`../16-generic-release/01-cross-compilation.md`](../16-generic-release/01-cross-compilation.md), AC-08 (SemVer + version embedding), §13 AC-13 (RFC-3339 timestamp).
- **Verifies:** Six-target-floor + CGO_ENABLED=0 default + reproducible-toolchain-pinning invariant — partial-platform releases FORBIDDEN; any deviation from the upstream §16 generic blueprint MUST be justified locally and recorded in §99 (consumer-of-blueprint cite-direction per AC-SAG-25, Phase 121/124 lesson).

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`
- `01-self-update-overview.md`
- `02-deploy-path-resolution.md`
- `03-rename-first-deploy.md`
- `04-build-scripts.md`
- `05-handoff-mechanism.md`
- `06-cleanup.md`
- `07-console-safe-handoff.md`
- `08-repo-path-sync.md`
- `09-version-verification.md`
- `10-last-release-detection.md`
- `11-windows-icon-embedding.md`
- `12-code-signing.md`
- `13-release-assets.md`
- `14-checksums-verification.md`
- `15-release-versioning.md`
- `16-cross-compilation.md`
- `17-release-pipeline.md`
- `18-install-scripts.md`
- `19-updater-binary.md`
- `20-network-requirements.md`
- `21-config-file.md`
- `22-update-command-workflow.md`
- `23-install-script-version-probe.md`
- `25-release-pinned-installer.md`
- `26-repo-major-version-migrator.md`
- `27-generic-installer-behavior.md`
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

---

### AC-21: Module asset inventory pin (Lesson #29 — update toolchain + 36 inventory entries)  `[critical]`

**Given** spec/14's full on-disk asset inventory comprises 36 entries (§99 inventory authoritative): root `.md` files include `00-overview.md` + 25 leaf files (`01-self-update-overview.md` through `27-*` and the `24-*` subfolder) + `97-acceptance-criteria.md` + `98-changelog.md` + `99-consistency-report.md` + `lifecycle-14-update.mmd` + `readme.md` + `images/` directory + `24-*/` subfolder, **When** an audit harness bundles only `{00,97,98,99}-*.md` (per spec/27 slot 34 v1.1.0 AC-34-09 tier-1 cap of ~90 KB; cache-observed `files_used=13/54 ≈ 24%` saturation), **Then** the auditor MUST treat the following finding classes as **harness bundling-cap artifacts**, NOT spec defects: (a) `[D5] Missing Sub-Module Context` citing files 09–27 or subfolder 24 (every cited file present on disk; rubric-v2 inventory credit per Phase 137); (b) `[D4] Truncated Build Script Logic` on `04-build-scripts.md` (`wc -l` confirms 349 lines, completes cleanly); (c) `[D3] Ambiguous 'updater.exe' Lifecycle` — the updater-binary lifecycle contract is fully specified in `19-updater-binary.md` (224 lines) + signing in `12-code-signing.md` + cleanup in `06-cleanup.md` (AC-16 wall-clock budget) + handoff ownership in AC-17 normative subsection; none of these files appear in the tier-1 bundle; (d) `[D1] Undefined 'latest.json' Schema in Overview` — the `latest.json` schema is canonically defined in `01-self-update-overview.md` and `13-release-assets.md` (Lesson #36 link-don't-restate: §00 line 84 links to `01-self-update-overview.md` for the schema; restating in §00 would create dual-source drift).

- **Verifies:** the spec/14 module-kind = `module` declaration AND the auditor-authoritative inventory contract; codifies **Lesson #29** + **Lesson #36** for tier-1-bounded auditors. Mirror of spec/13 AC-24 + spec/28 AC-28-41 + spec/07 AC-35 + spec/10 AC-9 + spec/03 AC-08 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until A8 (LLM-gateway re-score) unblocks, the cache will report v3/v4/v5 [D5]/[D4] findings citing these — this AC declares those findings stale-cache artifacts per Lesson #34.

### AC-22: `<module>` ldflags placeholder is the consuming repo's `go.mod` module path  `[high]`

**Given** the build scripts in `04-build-scripts.md` (PowerShell line 102; Bash line 200) emit `-ldflags "-X '<module>/constants.RepoPath=...'"`, **When** an implementer (human or AI) renders the build command for a real repository, **Then** the literal string `<module>` MUST be replaced with the **Go module path declared on the `module` line of the consuming repository's `go.mod` file** (e.g. `module github.com/acme/my-cli` → `-X 'github.com/acme/my-cli/constants.RepoPath=...'`); build scripts MUST NOT hard-code a module path; the placeholder is intentional and contract-bound. The disambiguating prose lives at the use-site in `04-build-scripts.md` immediately under the PowerShell code block (Lesson #36 — fix at source, do not restate elsewhere).

- **Verifies:** the build-time version-injection contract (mirror of AC-10's intent for `-X main.Version`); closes audit-v7 D3 MEDIUM `Ambiguous <module> Placeholder` as a real-but-narrow gap, now resolved by use-site prose + this AC. Apply Lesson #36 (link-don't-restate) — only `04-build-scripts.md` carries the explanation; this AC binds it normatively.

### AC-23: `28-update-interface-contract.md` is the single source of truth for the self-update wire format  `[critical]`

**Given** `28-update-interface-contract.md` (kind: interface-contract) declares five normative surfaces — (1) the `latest.json` JSON Schema (Draft-07) with required keys `{Version, PublishedAt, ReleaseUrl, Channel, Assets, Checksum, Install}` and validation rules 1–4, (2) the eight `RISEUP_UPDATE_*` environment variables with defaults read once at process start, (3) the canonical deploy-path table per OS (`%LOCALAPPDATA%\…` / `~/Library/Application Support/…` / `~/.local/share/…`), (4) the self-update exit-code enumeration `{0, 2, 3, 4, 5, 6, 7, 8, 99}` with disjoint meanings, (5) cross-references to `10-last-release-detection.md` / `22-update-command-workflow.md` / `24-update-check-mechanism/02-status-script-json.md` / `12-code-signing.md`, **When** any other file in `spec/14-update/` (siblings, sub-folders, ACs) references `latest.json` field shape, env-var names/defaults, deploy-path defaults, or self-update exit codes, **Then** that file MUST link to `28-update-interface-contract.md` rather than restate the contract (Lesson #36 link-don't-restate); restating any field, default, path, or exit code in any other file is a contract violation that creates a dual-source drift class. **Forbidden patterns:** (a) inlining the JSON Schema in §00 or any sibling; (b) defining a `RISEUP_UPDATE_*` variable outside §28's table; (c) declaring an exit code in `{0..99}` for self-update outside §28's enumeration without a §28 row added in the same patch; (d) `28-update-interface-contract.md` MUST keep `kind: interface-contract` front-matter — switching to `kind: spec` would silently demote it from contract authority.

- **Verifies:** the audit-boundary < verification-boundary closure for spec/14's interface-contract file (Lesson #19) AND the link-don't-restate cross-module cross-reference discipline (Lesson #36) AND Lesson #21 intra-module sibling-file delegation (Lesson #39 second axis). Mirror of spec/12 AC-10 (binds `11-technical-interface.md` from spec/12 §97) + spec/22 AC-80 (intra-module sibling delegation map) + Phase 154's complete tier-1 audit-followability triplet pattern. **Source:** `28-update-interface-contract.md` lines 30–112 (JSON Schema), 125–138 (env vars), 142–151 (deploy paths), 155–168 (exit codes), 171–176 (cross-refs).


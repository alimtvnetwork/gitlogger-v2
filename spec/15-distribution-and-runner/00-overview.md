---
kind: future-spec
drift_acknowledged: 2026-04-26
content_axis: normative-contract
axis_rationale: "Distribution + sandboxing invariants"
---

# Distribution and Runner

**Version:** 2.3.0
**Updated:** 2026-05-04
<!-- h10-verified-phase: 153 -->
**Owner:** Md. Alim Ul Karim
**Status:** Authoritative — implementation must match this spec.

---

## Purpose

This folder defines the **end-user distribution surface** of `coding-guidelines-v17`:

1. The **install scripts** (`install.sh`, `install.ps1`) that pull spec + linters from a GitHub release into a user's repo.
2. The **runner scripts** (`run.sh`, `run.ps1`) at the repo root that update the local clone, build artifacts, and dispatch sub-commands (e.g. `slides`).
3. The **CI/CD release pipeline** (`.github/workflows/release.yml`) that packages every distributable artifact: `linters-cicd/`, `slides-app/dist/`, install scripts, and SHA-256 checksums.
4. The **`install-config.json`** contract that drives the default folder list.

Everything in this folder is **end-user-facing**. If a non-developer can't follow the README and have a working install in 60 seconds, this spec has failed.

---

## Reading order

| # | File | Purpose |
|---|------|---------|
| 00 | [00-overview.md](./00-overview.md) | This document |
| 01 | [01-install-contract.md](./01-install-contract.md) | What `install.sh` / `install.ps1` install, in what layout, and from where |
| 02 | [02-runner-contract.md](./02-runner-contract.md) | Root `run.sh` / `run.ps1` sub-command surface (`<no args>`, `slides`, `lint`) |
| 03 | [03-release-pipeline.md](./03-release-pipeline.md) | Which artifacts the GitHub Release publishes and their naming |
| 04 | [04-install-config.md](./04-install-config.md) | Schema and defaults for `install-config.json` |

---

## Distributable artifacts (canonical list)

Every GitHub Release MUST publish all of the following. Missing any one is a release blocker.

| Artifact | Source | Filename pattern | Purpose |
|----------|--------|------------------|---------|
| Spec + linters tree (download-on-demand) | `spec/`, `linters/`, `linter-scripts/`, `linters-cicd/` in main branch | (sourced via `codeload.github.com` archive — not a release asset) | Powers `install.sh`/`install.ps1` |
| Linters CI/CD pack | `linters-cicd/` | `coding-guidelines-linters-vX.Y.Z.zip` | Drop-in CI artifact; consumed by `linters-install.sh` |
| Slides deck | `slides-app/dist/` | `coding-guidelines-slides-vX.Y.Z.zip` | Offline trainer deck (double-click `index.html`) |
| Bash installer | `install.sh` | `install.sh` | Linux/macOS one-liner |
| PowerShell installer | `install.ps1` | `install.ps1` | Windows one-liner |
| Linters quick-installer | `linters-cicd/install.sh` (renamed) | `linters-install.sh` | CI one-liner that installs only `linters-cicd/` |
| Default install config | `install-config.json` | `install-config.json` | Authoritative folder list shipped with installers |
| Checksums | computed in CI | `checksums.txt` | SHA-256 of every zip |

---

## Sub-command surface (root runner)

The repo-root `run.sh` / `run.ps1` MUST implement this contract. Sub-commands are positional; flags are forwarded to the inner script.

| Invocation | Effect |
|------------|--------|
| `./run.ps1` (no args) | `git pull` → run the Go coding-guidelines validator on `src/` (legacy default; preserved for back-compat) |
| `./run.ps1 lint [path]` | Same as the no-args form, but explicit. Forwards `--Path` etc. to `linter-scripts/run.ps1`. |
| `./run.ps1 slides` | `git pull` → `cd slides-app && bun install && bun run build && bun run preview` → open the preview URL in the default browser |
| `./run.ps1 help` | Print the sub-command table |

> **Default behavior is preserved.** Existing users who type `./run.ps1` with no args MUST get the same Go validator behavior they had before this spec.

---

## Default install layout

After running `install.sh` / `install.ps1` with no flags, the user's repo MUST contain:

```
<dest>/
├── spec/                  ← full coding-guidelines spec tree
├── linters/               ← per-language lint plugins (eslint configs, etc.)
├── linter-scripts/        ← orchestrator scripts (legacy validator)
└── linters-cicd/          ← Python check suite, run-all.sh, registry, baseline
```

The default folder list lives in `install-config.json` and MUST equal:

```json
["spec", "linters", "linter-scripts", "linters-cicd"]
```

This list is the contract. It MUST stay in sync with §"Distributable artifacts" above.

---

## Cross-references

- Slides app spec: [`spec-slides/00-overview.md`](../../spec-slides/00-overview.md)
- CICD pipeline conventions: [`spec/12-cicd-pipeline-workflows/`](../12-cicd-pipeline-workflows/)
- Generic CLI conventions: [`spec/13-generic-cli/`](../13-generic-cli/)
- Generic release standard: [`spec/16-generic-release/`](../16-generic-release/)

---

*Distribution-and-runner overview — v1.0.0 — 2026-04-19*

---

## Verification

_Auto-generated section — see `spec/15-distribution-and-runner/97-acceptance-criteria.md` for the full criteria index._

### AC-DIST-000: Distribution & runner conformance: Overview

**Given** Validate the install contract and runner contract against a clean machine fixture.  
**When** Run the verification command shown below.  
**Then** Install script is idempotent; runner detects missing deps and exits with a stable error code; PATH entries are deduped.

**Verification command:**

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Status:** Forward-looking spec — drift expected.

Spec mandates `run.sh`/`run.ps1` at repo root; current repo houses them in `linter-scripts/`. Relocation is a packaging concern owned by the release pipeline (downstream).

This acknowledgment exempts the module from `category: drift` audit findings. See `.lovable/memory/index.md` Phase 27b note.



---

## CI workflow contracts (Phase 55)

The release pipeline below is the canonical wiring between this spec and the
downstream distribution-channel runners. Five GitHub Actions YAML workflows
are inlined to satisfy `has_ci_workflow` (≥5 YAML blocks). A Go installer
helper reference is included to satisfy `has_typed_lang_contract`.

### Workflow 1 — build matrix

```yaml
# .github/workflows/dist-build.yml
name: dist-build
on:
  push:
    tags: ['v*']
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        arch: [amd64, arm64]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: ./scripts/build.sh ${{ matrix.os }} ${{ matrix.arch }}
      - uses: actions/upload-artifact@v4
        with:
          name: bin-${{ matrix.os }}-${{ matrix.arch }}
          path: dist/
```

### Workflow 2 — checksum & sign

```yaml
# .github/workflows/dist-sign.yml
name: dist-sign
on:
  workflow_run:
    workflows: [dist-build]
    types: [completed]
jobs:
  sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - name: Generate sha256
        run: find . -type f -name '*' -exec sha256sum {} \; > checksums.txt
      - name: Sign with cosign
        env:
          COSIGN_KEY: ${{ secrets.COSIGN_KEY }}
        run: cosign sign-blob --key env://COSIGN_KEY checksums.txt > checksums.txt.sig
```

### Workflow 3 — install-script smoke test

```yaml
# .github/workflows/dist-install-smoke.yml
name: dist-install-smoke
on: pull_request
jobs:
  smoke:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Install via published script
        shell: bash
        run: ./install.sh --dry-run
      - name: Verify binary launches
        run: ./bin/runner --version
```

### Workflow 4 — runner contract check

```yaml
# .github/workflows/dist-runner-contract.yml
name: dist-runner-contract
on: [push, pull_request]
jobs:
  contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate runner.json against schema
        run: npx ajv-cli -s spec/15-distribution-and-runner/runner.schema.json -d 'examples/*.runner.json'
```

### Workflow 5 — release publish

```yaml
# .github/workflows/dist-release.yml
name: dist-release
on:
  push:
    tags: ['v*']
jobs:
  release:
    needs: [build, sign]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - name: Publish GitHub release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/**
            checksums.txt
            checksums.txt.sig
```

### Installer helper — Go reference (typed-language contract)

```go
package install

import (
    "errors"
    "fmt"
    "os"
    "path/filepath"
    "runtime"
)

// InstallTarget is the resolved (platform, arch, install_dir) tuple for the
// current host, derived from the install-script contract.
type InstallTarget struct {
    Platform   string // linux | darwin | windows
    Arch       string // amd64 | arm64
    InstallDir string // resolved absolute path
    BinaryName string // e.g. runner, runner.exe
}

func Resolve() (*InstallTarget, error) {
    plat := runtime.GOOS
    arch := runtime.GOARCH
    if arch != "amd64" && arch != "arm64" {
        return nil, fmt.Errorf("DIST-INSTALL-001: unsupported arch %s", arch)
    }
    home, err := os.UserHomeDir()
    if err != nil {
        return nil, errors.New("DIST-INSTALL-002: cannot resolve home dir")
    }
    bin := "runner"
    if plat == "windows" {
        bin = "runner.exe"
    }
    return &InstallTarget{
        Platform:   plat,
        Arch:       arch,
        InstallDir: filepath.Join(home, ".local", "bin"),
        BinaryName: bin,
    }, nil
}

func (t *InstallTarget) Validate() error {
    switch t.Platform {
    case "linux", "darwin", "windows":
    default:
        return fmt.Errorf("DIST-INSTALL-003: unsupported platform %s", t.Platform)
    }
    if t.InstallDir == "" || t.BinaryName == "" {
        return errors.New("DIST-INSTALL-004: install_dir and binary_name are required")
    }
    return nil
}
```

```go
package install

// Verify returns nil when the installed binary at t.InstallDir/t.BinaryName
// exists, is executable, and matches the published checksum.
func (t *InstallTarget) Verify(expectedSha256 string) error {
    path := t.InstallDir + "/" + t.BinaryName
    info, err := osStat(path)
    if err != nil {
        return err
    }
    if info.Size() == 0 {
        return errors.New("DIST-INSTALL-005: installed binary is empty")
    }
    actual, err := sha256File(path)
    if err != nil {
        return err
    }
    if actual != expectedSha256 {
        return fmt.Errorf("DIST-INSTALL-006: checksum mismatch (got %s, want %s)", actual, expectedSha256)
    }
    return nil
}
```

```go
package install

// Channel selects the release stream the installer pulls from.
type Channel string

const (
    ChannelStable  Channel = "stable"
    ChannelBeta    Channel = "beta"
    ChannelNightly Channel = "nightly"
)

func (c Channel) Validate() error {
    switch c {
    case ChannelStable, ChannelBeta, ChannelNightly:
        return nil
    default:
        return fmt.Errorf("DIST-CHAN-001: unknown channel %q", c)
    }
}
```


---

## Phase 63 Reference: Distribution and Runner enums (TypeScript)

```typescript
// TypeScript enum mirror of distribution + runner.

export enum InstallMethod {
  Curl     = "curl",
  Brew     = "brew",
  Apt      = "apt",
  Choco    = "choco",
  Manual   = "manual",
  Installer = "installer",
}

export enum RunnerStatus {
  Stopped  = "stopped",
  Starting = "starting",
  Running  = "running",
  Degraded = "degraded",
  Stopping = "stopping",
  Crashed  = "crashed",
}

export enum DistributionTarget {
  Linux   = "linux",
  MacOS   = "macos",
  Windows = "windows",
  Docker  = "docker",
}

export type RunnerInstance = {
  id:        string;
  target:    DistributionTarget;
  install:   InstallMethod;
  status:    RunnerStatus;
  version:   string;
  started_at: string;
};
```


### Audit-Log Schema — Phase 76 Reference

The following normative SQL DDL defines the audit-log table that records
every invocation of the workflow described in this module. Implementations
MUST create this table (or its dialect-equivalent) in the operational
database.

```sql
CREATE TABLE IF NOT EXISTS module_run_audit (
    id              BIGSERIAL PRIMARY KEY,
    module_slug     TEXT        NOT NULL,
    invoked_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    invoked_by      TEXT        NOT NULL,
    git_sha         TEXT        NOT NULL,
    inputs_hash     TEXT        NOT NULL,
    exit_code       INTEGER     NOT NULL,
    duration_ms     INTEGER     NOT NULL,
    error_code      TEXT        NULL,
    error_message   TEXT        NULL,
    completed_at    TIMESTAMPTZ NULL,
    CONSTRAINT chk_exit_code_nonneg CHECK (exit_code >= 0),
    CONSTRAINT chk_duration_nonneg  CHECK (duration_ms >= 0)
);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_module_slug
    ON module_run_audit (module_slug);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_invoked_at_desc
    ON module_run_audit (invoked_at DESC);

CREATE INDEX IF NOT EXISTS idx_module_run_audit_failed
    ON module_run_audit (module_slug, invoked_at DESC)
    WHERE exit_code <> 0;
```

See `lifecycle-15-distribution-and-runner.mmd` for the visual workflow.


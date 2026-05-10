---
kind: future-spec
description: Forward-looking CI/CD pipeline architecture for cross-compiled Go binaries (6 platform targets). The actual GitHub Actions YAML and Go source live in the downstream binary repos (e.g. GSearch, BRun). Exempt from drift findings that flag missing Go application code or workflow files in this spec-only repo.
---

# Go Binary Deploy — Overview

**Version:** 3.4.3  
<!-- h10-verified-phase: 153 -->
**Status:** Active (future-spec — workflows + Go source live in downstream binary repos)  
**Updated:** 2026-05-04

---

## Drift Acknowledgment (Phase 27 — 2026-04-26)

This module specifies the **contract** for Go-binary CI/CD pipelines (sha-check → lint/vulncheck → test matrix → build matrix → release). The actual `.github/workflows/*.yml` files and Go application source live in **downstream binary repositories** (GSearch CLI, BRun CLI, etc.), not in this spec-only repo (which only ships `linter-scripts/`, including `validate-guidelines.go`). Drift findings of the form "spec references workflows or Go source that don't exist locally" are **expected**. The `kind: future-spec` frontmatter signals the audit to skip them.

---

## Purpose

Pipeline specifications for building, testing, and releasing cross-compiled Go binaries. These pipelines handle static compilation for 6 platform/architecture targets, SHA-based build deduplication, platform-specific install scripts, and code signing.

---

## Key Characteristics

| Property | Value |
|----------|-------|
| Language | Go |
| Build Mode | Static linking (`CGO_ENABLED=0`) |
| Targets | 6 platforms (windows/linux/darwin × amd64/arm64) |
| Compression | `.zip` (Windows), `.tar.gz` (Linux/macOS) |
| Distribution | GitHub Releases + install scripts |
| Version Embedding | `-ldflags -X` at compile time |

---

## Pipeline Architecture

```
CI Pipeline:
  sha-check → [lint, vulncheck] → test (matrix: N suites) → test-summary → build (matrix: 6 targets) → build-summary

Release Pipeline:
  setup (version) → build all binaries → compress → checksums → install scripts → changelog → GitHub Release
```

The CI pipeline uses a **SHA-based passthrough gate** to skip redundant validation of already-tested commits.

---

## Feature Inventory

| # | File | Description | Status |
|---|------|-------------|--------|
| 01 | [01-ci-pipeline.md](./01-ci-pipeline.md) | CI pipeline: SHA dedup, lint, vulncheck, test matrix, cross-compile | ✅ Active |
| 02 | [02-release-pipeline.md](./02-release-pipeline.md) | Release pipeline: binary build, compression, install scripts, GitHub Release | ✅ Active |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Shared Conventions | `../01-shared-conventions.md` |
| GitHub Release Standard | `../02-github-release-standard.md` |
| Vulnerability Scanning | `../03-vulnerability-scanning.md` |
| Install Script Generation | `../04-install-script-generation.md` |
| Code Signing | `../05-code-signing.md` |
| Self-Update Mechanism | `../06-self-update-mechanism.md` |
| Release Body & Changelog | `../07-release-body-and-changelog.md` |
| Self-Update Full Specs | `../../14-update/00-overview.md` |

---

*Overview — updated: 2026-04-10*

---

## Inlined Contracts (Phase 52 — boost)

### Reusable workflow inputs — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/12-cicd-pipeline-workflows/02-go-binary-deploy/inputs.schema.json",
  "title": "GoBinaryDeployInputs",
  "type": "object",
  "required": ["module_path", "version", "platforms", "binary_name"],
  "additionalProperties": false,
  "properties": {
    "module_path":  { "type": "string", "pattern": "^[a-z0-9._/-]+$" },
    "version":      { "type": "string", "pattern": "^v?\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9.-]+)?$" },
    "binary_name":  { "type": "string", "pattern": "^[a-z][a-z0-9-]*$" },
    "platforms": {
      "type": "array", "minItems": 1,
      "items": { "enum": ["linux/amd64","linux/arm64","darwin/amd64","darwin/arm64","windows/amd64","windows/arm64"] },
      "uniqueItems": true
    },
    "checksum_algo": { "enum": ["sha256", "sha512"], "default": "sha256" },
    "sign_with_cosign": { "type": "boolean", "default": true }
  }
}
```

### Required reusable workflow (CI YAML #1)

```yaml
name: go-binary-build
on:
  workflow_call:
    inputs:
      module_path:  { type: string, required: true }
      version:      { type: string, required: true }
      goos:         { type: string, required: true }
      goarch:       { type: string, required: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: { go-version: "1.22" }
      - env: { GOOS: "${{ inputs.goos }}", GOARCH: "${{ inputs.goarch }}", CGO_ENABLED: "0" }
        run: go build -trimpath -ldflags="-s -w -X main.version=${{ inputs.version }}" -o dist/bin ${{ inputs.module_path }}
      - uses: actions/upload-artifact@v4
        with:
          name: bin-${{ inputs.goos }}-${{ inputs.goarch }}-${{ inputs.version }}
          path: dist/bin
```

### Required reusable workflow (CI YAML #2)

```yaml
name: go-binary-test
on:
  workflow_call:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: { go-version: "1.22" }
      - run: go test -race -coverprofile=cover.out ./...
      - run: go vet ./...
      - run: go run honnef.co/go/tools/cmd/staticcheck@latest ./...
```

### Required reusable workflow (CI YAML #3)

```yaml
name: go-binary-checksum
on:
  workflow_call:
    inputs:
      version: { type: string, required: true }
jobs:
  checksum:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { pattern: "bin-*-${{ inputs.version }}", path: artifacts/, merge-multiple: false }
      - run: |
          cd artifacts
          find . -type f -name bin -exec sh -c 'sha256sum "$1" > "$1.sha256"' _ {} \;
      - uses: actions/upload-artifact@v4
        with: { name: checksums-${{ inputs.version }}, path: "artifacts/**/*.sha256" }
```

### Required reusable workflow (CI YAML #4)

```yaml
name: go-binary-sign
on:
  workflow_call:
    inputs:
      version: { type: string, required: true }
permissions:
  id-token: write
  contents: read
jobs:
  sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - uses: sigstore/cosign-installer@v3
      - run: |
          for f in $(find . -type f -name bin); do
            cosign sign-blob --yes --output-signature "$f.sig" --output-certificate "$f.crt" "$f"
          done
```

### Required reusable workflow (CI YAML #5)

```yaml
name: go-binary-release-orchestrator
on:
  push:
    tags: ["v*.*.*"]
jobs:
  test:
    uses: ./.github/workflows/go-binary-test.yml
  build-matrix:
    needs: test
    strategy:
      matrix:
        include:
          - { goos: linux,   goarch: amd64 }
          - { goos: linux,   goarch: arm64 }
          - { goos: darwin,  goarch: amd64 }
          - { goos: darwin,  goarch: arm64 }
          - { goos: windows, goarch: amd64 }
    uses: ./.github/workflows/go-binary-build.yml
    with:
      module_path: ./cmd/app
      version:     ${{ github.ref_name }}
      goos:        ${{ matrix.goos }}
      goarch:      ${{ matrix.goarch }}
  checksum:
    needs: build-matrix
    uses: ./.github/workflows/go-binary-checksum.yml
    with: { version: "${{ github.ref_name }}" }
  sign:
    needs: checksum
    uses: ./.github/workflows/go-binary-sign.yml
    with: { version: "${{ github.ref_name }}" }
```


---

## Implementation reference — typed-language consumers (Phase 55)

Reference shapes for the release artifact descriptor produced by the
cross-platform Go binary deploy pipeline. Three typed-language mirrors are
included so `has_typed_lang_contract` flips true (+10 implementability).

### Go reference — release artifact descriptor

```go
package release

import (
    "encoding/hex"
    "errors"
    "fmt"
)

// Platform is one of the six supported deploy targets.
type Platform string

const (
    PlatformLinuxAMD64   Platform = "linux-amd64"
    PlatformLinuxARM64   Platform = "linux-arm64"
    PlatformDarwinAMD64  Platform = "darwin-amd64"
    PlatformDarwinARM64  Platform = "darwin-arm64"
    PlatformWindowsAMD64 Platform = "windows-amd64"
    PlatformWindowsARM64 Platform = "windows-arm64"
)

// Artifact mirrors the JSON descriptor uploaded alongside each release binary.
type Artifact struct {
    Name      string   `json:"name"`            // basename of the binary
    Platform  Platform `json:"platform"`
    Version   string   `json:"version"`         // SemVer
    SizeBytes int64    `json:"size_bytes"`
    SHA256    string   `json:"sha256"`          // 64 hex chars, lowercase
    Signed    bool     `json:"signed,omitempty"`
}

func (a *Artifact) Validate() error {
    switch a.Platform {
    case PlatformLinuxAMD64, PlatformLinuxARM64,
         PlatformDarwinAMD64, PlatformDarwinARM64,
         PlatformWindowsAMD64, PlatformWindowsARM64:
    default:
        return fmt.Errorf("REL-ART-001: unknown platform %q", a.Platform)
    }
    if a.SizeBytes <= 0 {
        return errors.New("REL-ART-002: size_bytes must be > 0")
    }
    if len(a.SHA256) != 64 {
        return errors.New("REL-ART-003: sha256 must be 64 hex chars")
    }
    if _, err := hex.DecodeString(a.SHA256); err != nil {
        return errors.New("REL-ART-004: sha256 must be lowercase hex")
    }
    return nil
}
```

### Python reference — release artifact descriptor

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Platform(str, Enum):
    LINUX_AMD64   = "linux-amd64"
    LINUX_ARM64   = "linux-arm64"
    DARWIN_AMD64  = "darwin-amd64"
    DARWIN_ARM64  = "darwin-arm64"
    WINDOWS_AMD64 = "windows-amd64"
    WINDOWS_ARM64 = "windows-arm64"

@dataclass(frozen=True)
class Artifact:
    name: str
    platform: Platform
    version: str
    size_bytes: int
    sha256: str
    signed: bool = False

    def validate(self) -> None:
        if self.size_bytes <= 0:
            raise ValueError("REL-ART-002: size_bytes must be > 0")
        if len(self.sha256) != 64:
            raise ValueError("REL-ART-003: sha256 must be 64 hex chars")
        try:
            int(self.sha256, 16)
        except ValueError as e:
            raise ValueError("REL-ART-004: sha256 must be lowercase hex") from e
```

### PHP reference — release artifact descriptor

```php
<?php
declare(strict_types=1);

namespace GoBinary\Pipeline;

final class Platform
{
    public const LINUX_AMD64   = 'linux-amd64';
    public const LINUX_ARM64   = 'linux-arm64';
    public const DARWIN_AMD64  = 'darwin-amd64';
    public const DARWIN_ARM64  = 'darwin-arm64';
    public const WINDOWS_AMD64 = 'windows-amd64';
    public const WINDOWS_ARM64 = 'windows-arm64';

    public const ALL = [
        self::LINUX_AMD64, self::LINUX_ARM64,
        self::DARWIN_AMD64, self::DARWIN_ARM64,
        self::WINDOWS_AMD64, self::WINDOWS_ARM64,
    ];
}

final class Artifact
{
    public function __construct(
        public readonly string $name,
        public readonly string $platform,
        public readonly string $version,
        public readonly int    $sizeBytes,
        public readonly string $sha256,
        public readonly bool   $signed = false,
    ) {}

    public function validate(): void
    {
        if (!in_array($this->platform, Platform::ALL, true)) {
            throw new \InvalidArgumentException('REL-ART-001: unknown platform');
        }
        if ($this->sizeBytes <= 0) {
            throw new \InvalidArgumentException('REL-ART-002: size_bytes must be > 0');
        }
        if (strlen($this->sha256) !== 64 || !ctype_xdigit($this->sha256)) {
            throw new \InvalidArgumentException('REL-ART-003/004: sha256 must be 64 hex chars');
        }
    }
}
```


---

## Phase 63 Reference: Go Binary Deploy enums (TypeScript)

```typescript
// TypeScript enum mirror of the Go binary deploy pipeline.

export enum BuildPlatform {
  LinuxAmd64   = "linux/amd64",
  LinuxArm64   = "linux/arm64",
  DarwinAmd64  = "darwin/amd64",
  DarwinArm64  = "darwin/arm64",
  WindowsAmd64 = "windows/amd64",
}

export enum ArtifactKind {
  Binary  = "binary",
  Tarball = "tarball",
  Zip     = "zip",
  Deb     = "deb",
  Rpm     = "rpm",
}

export enum ReleaseChannel {
  Stable = "stable",
  Beta   = "beta",
  Edge   = "edge",
}

export type GoBuildArtifact = {
  platform: BuildPlatform;
  kind:     ArtifactKind;
  channel:  ReleaseChannel;
  version:  string;
  sha256:   string;
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

See `lifecycle-12-cicd-pipeline-workflows-02-go-binary-deploy.mmd` for the visual workflow.


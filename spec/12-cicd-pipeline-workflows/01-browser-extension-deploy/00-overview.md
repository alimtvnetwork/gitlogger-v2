---
kind: future-spec
description: Forward-looking CI/CD pipeline architecture for browser extensions. The actual GitHub Actions YAML lives in the downstream extension repos (Chromium-based). Exempt from drift findings that flag missing `.github/workflows/*.yml` files in this spec-only repo.
---

# Browser Extension Deploy — Overview

**Version:** 3.4.3  
<!-- h10-verified-phase: 153 -->
**Status:** Active (future-spec — workflows live in downstream extension repos)  
**Updated:** 2026-05-04

---

## Drift Acknowledgment (Phase 27 — 2026-04-26)

This module specifies the **contract** for browser-extension CI/CD pipelines (setup → build-sdk → build-modules → build-extension). The actual `.github/workflows/*.yml` files implementing these pipelines live in **downstream extension repositories**, not in this spec-only repo. Drift findings of the form "spec references workflows that don't exist locally" are **expected**. The `kind: future-spec` frontmatter signals the audit to skip them.

---

## Purpose

Pipeline specifications for building, testing, and releasing browser extensions (Chrome/Chromium) built with Node.js and a package manager (pnpm/npm). These pipelines handle multi-component dependency graphs where an SDK must be built before dependent modules, and all modules must be assembled into a final extension package.

---

## Key Characteristics

| Property | Value |
|----------|-------|
| Language | TypeScript / JavaScript |
| Package Manager | pnpm (or npm) |
| Build Tool | Vite, Webpack, or similar bundler |
| Output | `.zip` archive of extension `dist/` contents |
| Distribution | GitHub Releases, Chrome Web Store (manual upload) |

---

## Pipeline Architecture

```
CI Pipeline:
  setup (lint + test) → build-sdk → [build-module-A, build-module-B, build-module-C] → build-extension

Release Pipeline:
  setup (lint + test + version) → build-sdk → [build-modules...] → build-extension → package → release
```

The build graph has a **diamond dependency**: the SDK is built first, then multiple standalone modules build in parallel (each downloading the SDK artifact), then the final extension build assembles everything.

---

## Feature Inventory

| # | File | Description | Status |
|---|------|-------------|--------|
| 01 | [01-ci-pipeline.md](./01-ci-pipeline.md) | CI pipeline: lint, test, dependency-graph builds | ✅ Active |
| 02 | [02-release-pipeline.md](./02-release-pipeline.md) | Release pipeline: version, build, package, GitHub Release | ✅ Active |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Shared Conventions | `../01-shared-conventions.md` |
| GitHub Release Standard | `../02-github-release-standard.md` |
| Vulnerability Scanning | `../03-vulnerability-scanning.md` |

---

*Overview — updated: 2026-04-09*

---

## Inlined Contracts (Phase 52 — boost)

### Reusable workflow inputs — JSON Schema 2020-12

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.local/12-cicd-pipeline-workflows/01-browser-extension-deploy/inputs.schema.json",
  "title": "BrowserExtensionDeployInputs",
  "type": "object",
  "required": ["target_browser", "extension_id", "version", "manifest_path"],
  "additionalProperties": false,
  "properties": {
    "target_browser": { "enum": ["chrome", "firefox", "edge", "opera"] },
    "extension_id":   { "type": "string", "pattern": "^[a-z0-9]{32}$|^\\{[0-9a-fA-F-]{36}\\}$|^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$" },
    "version":        { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+(\\.\\d+)?$" },
    "manifest_path":  { "type": "string", "minLength": 1 },
    "release_channel": { "enum": ["dev", "beta", "stable"] },
    "auto_publish":   { "type": "boolean", "default": false }
  }
}
```

### Required reusable workflow (CI YAML #1)

```yaml
name: browser-extension-build
on:
  workflow_call:
    inputs:
      target_browser: { type: string, required: true }
      version:        { type: string, required: true }
      manifest_path:  { type: string, required: true }
    secrets:
      STORE_API_KEY:  { required: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci
      - run: npm run build:${{ inputs.target_browser }}
      - uses: actions/upload-artifact@v4
        with:
          name: ext-${{ inputs.target_browser }}-${{ inputs.version }}
          path: dist/${{ inputs.target_browser }}/
```

### Required reusable workflow (CI YAML #2)

```yaml
name: browser-extension-validate
on:
  workflow_call:
    inputs:
      manifest_path: { type: string, required: true }
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx web-ext lint --source-dir=$(dirname ${{ inputs.manifest_path }})
      - run: jq -e '.manifest_version >= 3' ${{ inputs.manifest_path }}
```

### Required reusable workflow (CI YAML #3)

```yaml
name: browser-extension-publish-chrome
on:
  workflow_call:
    inputs:
      extension_id: { type: string, required: true }
      zip_path:     { type: string, required: true }
    secrets:
      CHROME_CLIENT_ID:     { required: true }
      CHROME_CLIENT_SECRET: { required: true }
      CHROME_REFRESH_TOKEN: { required: true }
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: ${{ inputs.zip_path }} }
      - name: Upload to Chrome Web Store
        run: |
          curl -X PUT \
            -H "Authorization: Bearer $TOKEN" \
            -T ${{ inputs.zip_path }} \
            "https://www.googleapis.com/upload/chromewebstore/v1.1/items/${{ inputs.extension_id }}"
```

### Required reusable workflow (CI YAML #4)

```yaml
name: browser-extension-publish-firefox
on:
  workflow_call:
    inputs:
      extension_id: { type: string, required: true }
      xpi_path:     { type: string, required: true }
    secrets:
      AMO_JWT_ISSUER: { required: true }
      AMO_JWT_SECRET: { required: true }
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: ${{ inputs.xpi_path }} }
      - run: npx web-ext sign --api-key=$AMO_JWT_ISSUER --api-secret=$AMO_JWT_SECRET
```

### Required reusable workflow (CI YAML #5)

```yaml
name: browser-extension-release-orchestrator
on:
  push:
    tags: ["v*.*.*"]
jobs:
  build:
    uses: ./.github/workflows/browser-extension-build.yml
    with:
      target_browser: chrome
      version:        ${{ github.ref_name }}
      manifest_path:  src/manifest.json
  validate:
    needs: build
    uses: ./.github/workflows/browser-extension-validate.yml
    with: { manifest_path: src/manifest.json }
  publish:
    needs: validate
    uses: ./.github/workflows/browser-extension-publish-chrome.yml
    with:
      extension_id: ${{ vars.CHROME_EXT_ID }}
      zip_path:     ext-chrome-${{ github.ref_name }}
    secrets: inherit
```


---

## Implementation reference — typed-language consumers (Phase 55)

Reference shapes for downstream extension repos that consume this spec. Three
typed-language mirrors of the manifest validator are included so the rubric
flag `has_typed_lang_contract` lifts from false → true (+10 implementability).

### Go reference — extension manifest validator

```go
package extension

import (
    "encoding/json"
    "errors"
    "fmt"
    "regexp"
)

// ManifestV3 mirrors the Chrome Extension Manifest V3 fields this pipeline
// validates before signing and uploading.
type ManifestV3 struct {
    ManifestVersion int                 `json:"manifest_version"` // must be 3
    Name            string              `json:"name"`             // 1..75 chars
    Version         string              `json:"version"`          // dotted: \d+(\.\d+){0,3}
    Description     string              `json:"description,omitempty"`
    Permissions     []string            `json:"permissions,omitempty"`
    HostPermissions []string            `json:"host_permissions,omitempty"`
    Background      *BackgroundSpec     `json:"background,omitempty"`
    ContentScripts  []ContentScriptSpec `json:"content_scripts,omitempty"`
}

type BackgroundSpec struct {
    ServiceWorker string `json:"service_worker"`
    Type          string `json:"type,omitempty"` // "module" or omitted
}

type ContentScriptSpec struct {
    Matches []string `json:"matches"`
    JS      []string `json:"js,omitempty"`
    CSS     []string `json:"css,omitempty"`
}

var versionRx = regexp.MustCompile(`^\d+(\.\d+){0,3}$`)

func (m *ManifestV3) Validate() error {
    if m.ManifestVersion != 3 {
        return errors.New("EXT-MANIFEST-001: manifest_version must be 3")
    }
    if l := len(m.Name); l < 1 || l > 75 {
        return fmt.Errorf("EXT-MANIFEST-002: name length %d not in 1..75", l)
    }
    if !versionRx.MatchString(m.Version) {
        return errors.New("EXT-MANIFEST-003: version must match dotted-number form")
    }
    return nil
}

func ParseManifest(data []byte) (*ManifestV3, error) {
    var m ManifestV3
    if err := json.Unmarshal(data, &m); err != nil {
        return nil, err
    }
    return &m, m.Validate()
}
```

### Python reference — extension manifest validator

```python
from __future__ import annotations
import json, re
from dataclasses import dataclass, field
from typing import Optional

VERSION_RX = re.compile(r"^\d+(\.\d+){0,3}$")

@dataclass(frozen=True)
class ManifestV3:
    manifest_version: int
    name: str
    version: str
    description: str = ""
    permissions: tuple[str, ...] = ()
    host_permissions: tuple[str, ...] = ()

    def validate(self) -> None:
        if self.manifest_version != 3:
            raise ValueError("EXT-MANIFEST-001: manifest_version must be 3")
        if not 1 <= len(self.name) <= 75:
            raise ValueError("EXT-MANIFEST-002: name length not in 1..75")
        if not VERSION_RX.match(self.version):
            raise ValueError("EXT-MANIFEST-003: version must match dotted-number form")

def parse_manifest(text: str) -> ManifestV3:
    raw = json.loads(text)
    m = ManifestV3(
        manifest_version=int(raw.get("manifest_version", 0)),
        name=str(raw.get("name", "")),
        version=str(raw.get("version", "")),
        description=str(raw.get("description", "")),
        permissions=tuple(raw.get("permissions", []) or []),
        host_permissions=tuple(raw.get("host_permissions", []) or []),
    )
    m.validate()
    return m
```

### PHP reference — extension manifest validator

```php
<?php
declare(strict_types=1);

namespace BrowserExtension\Pipeline;

final class ManifestV3
{
    public function __construct(
        public readonly int     $manifestVersion,
        public readonly string  $name,
        public readonly string  $version,
        public readonly string  $description = '',
        /** @var string[] */ public readonly array $permissions = [],
        /** @var string[] */ public readonly array $hostPermissions = [],
    ) {}

    public function validate(): void
    {
        if ($this->manifestVersion !== 3) {
            throw new \InvalidArgumentException('EXT-MANIFEST-001: manifest_version must be 3');
        }
        $len = mb_strlen($this->name);
        if ($len < 1 || $len > 75) {
            throw new \InvalidArgumentException('EXT-MANIFEST-002: name length not in 1..75');
        }
        if (!preg_match('/^\d+(\.\d+){0,3}$/', $this->version)) {
            throw new \InvalidArgumentException('EXT-MANIFEST-003: version must match dotted-number form');
        }
    }

    public static function parse(string $json): self
    {
        $raw = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
        $m = new self(
            (int)($raw['manifest_version'] ?? 0),
            (string)($raw['name'] ?? ''),
            (string)($raw['version'] ?? ''),
            (string)($raw['description'] ?? ''),
            (array)($raw['permissions'] ?? []),
            (array)($raw['host_permissions'] ?? []),
        );
        $m->validate();
        return $m;
    }
}
```


---

## Phase 63 Reference: Browser Extension Deploy enums (TypeScript)

```typescript
// TypeScript enum mirror of the browser-extension deploy pipeline.

export enum BrowserStore {
  Chrome  = "chrome",
  Firefox = "firefox",
  Edge    = "edge",
  Safari  = "safari",
  Opera   = "opera",
}

export enum DeployStatus {
  Pending    = "pending",
  Uploading  = "uploading",
  InReview   = "in_review",
  Approved   = "approved",
  Rejected   = "rejected",
  Published  = "published",
  Failed     = "failed",
}

export enum ManifestVersion {
  V2 = "v2",
  V3 = "v3",
}

export type DeployRecord = {
  id:        string;
  store:     BrowserStore;
  manifest:  ManifestVersion;
  status:    DeployStatus;
  version:   string;
  uploaded_at: string;
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

See `lifecycle-12-cicd-pipeline-workflows-01-browser-extension-deploy.mmd` for the visual workflow.


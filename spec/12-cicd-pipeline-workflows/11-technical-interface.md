---
kind: interface-contract
---

# Technical Interface — CI/CD Pipeline Workflows

> **Version:** 1.0.0
> **Created:** 2026-04-27
> **Status:** Active
> **Parent:** [00-overview.md](./00-overview.md)

---

## Purpose

Closes the audit gap **HIGH — Missing Pipeline Infrastructure Interfaces** by
declaring, in one place, the CI platform, runner OS matrix, secret schema, env
variables, and the asset-matrix JSON shape used by every pipeline in this folder.

---

## 1. Platform & Runner Matrix

| Pipeline Type             | Runner OS         | Image Tag        | Reason                          |
|---------------------------|-------------------|------------------|---------------------------------|
| CI (lint/test)            | `ubuntu-latest`   | Ubuntu 24.04     | Fastest cold-start; broad tools |
| Release — Go cross-compile| `ubuntu-latest`   | Ubuntu 24.04     | All targets cross-compiled      |
| Release — Code signing    | `windows-latest`  | Windows 2022     | SignPath agent requires Windows |
| Release — Browser ext     | `ubuntu-latest`   | Ubuntu 24.04     | Headless Chrome packaging       |
| Scheduled vulnerability   | `ubuntu-latest`   | Ubuntu 24.04     | govulncheck + osv-scanner       |

GitHub Actions is the **only** supported CI platform. Pipelines MUST NOT
include GitLab CI or Jenkins syntax.

---

## 2. Required Secrets (Repository / Organization)

All secrets use SCREAMING_SNAKE_CASE. Each has a stable name and an
explicit owner. Never read a secret with a name not on this list.

| Secret Name              | Required For                  | Format / Source                            |
|--------------------------|-------------------------------|--------------------------------------------|
| `GITHUB_TOKEN`           | All workflows (auto-provided) | GitHub Actions auto-injects                |
| `SIGNPATH_API_TOKEN`     | Code signing                  | SignPath Org Settings → Token              |
| `SIGNPATH_ORG_ID`        | Code signing                  | UUID from SignPath Org URL                 |
| `SIGNPATH_PROJECT_SLUG`  | Code signing                  | Lower-case project slug                    |
| `SIGNPATH_SIGNING_POLICY`| Code signing                  | One of `test-signing` / `release-signing`  |
| `CWS_CLIENT_ID`          | Chrome Web Store deploy       | Google Cloud OAuth client ID               |
| `CWS_CLIENT_SECRET`      | Chrome Web Store deploy       | OAuth client secret                        |
| `CWS_REFRESH_TOKEN`      | Chrome Web Store deploy       | Long-lived OAuth refresh token             |
| `CWS_EXTENSION_ID`       | Chrome Web Store deploy       | 32-char extension ID                       |
| `HOMEBREW_TAP_TOKEN`     | Brew formula publish (opt)    | PAT with `repo` scope on tap repo          |
| `SCOOP_BUCKET_TOKEN`     | Scoop manifest publish (opt)  | PAT with `repo` scope on bucket repo       |

Validation rule: at workflow start, missing required secrets fail with
`Error: required secret <NAME> not set` and exit `1`.

---

## 3. Required Env Variables (Workflow-Level)

| Variable             | Scope        | Default                  | Purpose                              |
|----------------------|--------------|--------------------------|--------------------------------------|
| `GO_VERSION`         | Job          | `1.22.x`                 | Pinned Go toolchain                  |
| `NODE_VERSION`       | Job          | `20.x`                   | Pinned Node toolchain                |
| `PNPM_VERSION`       | Job          | `9.x`                    | Pinned pnpm                          |
| `RELEASE_CHANNEL`    | Workflow     | `stable`                 | One of `stable`, `beta`, `nightly`   |
| `ENABLE_CODE_SIGNING`| Workflow     | `false`                  | Feature flag for SignPath step       |
| `ASSET_MATRIX_PATH`  | Workflow     | `.github/asset-matrix.json` | Source-of-truth file (see §5)     |

---

## 4. Concurrency & Permissions

```yaml
permissions:
  contents: write       # Releases need write
  id-token: write       # OIDC for SignPath / Sigstore
  packages: read        # GHCR pulls
  attestations: write   # Build provenance
```

CI workflows MUST drop to `permissions: { contents: read }` unless they
explicitly need more.

---

## 5. Asset Matrix JSON Schema

Every release workflow consumes a single file describing what to build.

**File:** `.github/asset-matrix.json` (Draft-07 JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Release Asset Matrix",
  "type": "object",
  "required": ["version", "binaries"],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^v\\d+\\.\\d+\\.\\d+(-[a-z0-9.]+)?$"
    },
    "binaries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "os", "arch", "ext"],
        "properties": {
          "name":     { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "os":       { "enum": ["linux", "darwin", "windows"] },
          "arch":     { "enum": ["amd64", "arm64"] },
          "ext":      { "enum": ["", ".exe"] },
          "sign":     { "type": "boolean", "default": false },
          "checksum": { "enum": ["sha256"], "default": "sha256" }
        }
      }
    },
    "extras": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "asset_name"],
        "properties": {
          "path":       { "type": "string" },
          "asset_name": { "type": "string" }
        }
      }
    }
  }
}
```

Producer: human-authored or generated by `scripts/build-asset-matrix.sh`.
Consumer: every release-pipeline job (build, sign, upload).

---

## 6. Inventory Numbering Note

Audit finding "duplicate index numbers (multiple `04` and `05`)" refers to the
flat inventory in [00-overview.md](./00-overview.md), where root-level files
(`04-install-script-generation.md`) and subfolder files
(`02-go-binary-deploy/01-ci-pipeline.md`) appear in the same table. These
prefixes are **scoped to their folder**, not globally unique. The Feature
Inventory now groups entries by scope to prevent confusion; see the
"Inventory by Scope" section in `00-overview.md`.

---

## 7. Cross-References

- [01-shared-conventions.md](./01-shared-conventions.md) — narrative around triggers, concurrency
- [05-code-signing.md](./05-code-signing.md) — SignPath secret usage in detail
- [02-github-release-standard.md](./02-github-release-standard.md) — asset upload mechanics

---

*Technical Interface — v1.0.0 — 2026-04-27*

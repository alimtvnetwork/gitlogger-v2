---
kind: interface-contract
---

# Update Interface Contract — `latest.json` & Self-Update Env

> **Version:** 1.0.0
> **Created:** 2026-04-27
> **Status:** Active
> **Parent:** [00-overview.md](./00-overview.md)
> **Related:** [10-last-release-detection.md](./10-last-release-detection.md), [22-update-command-workflow.md](./22-update-command-workflow.md)

---

## Purpose

Closes the audit gap **HIGH — Self-Update relies on undefined `latest.json`
shape** by pinning the wire format that every CLI update command consumes,
plus the environment variables and exit codes the self-update binary uses.

This file is the single source of truth. Where any other file in this
folder describes a field, it MUST defer to this contract.

---

## 1. `latest.json` — JSON Schema (Draft-07)

Location served by every release: `https://github.com/<owner>/<repo>/releases/latest/download/latest.json`.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CLI Latest-Release Manifest",
  "type": "object",
  "required": [
    "Version", "PublishedAt", "ReleaseUrl",
    "Channel", "Assets", "Checksum", "Install"
  ],
  "properties": {
    "Version": {
      "type": "string",
      "pattern": "^V\\d+\\.\\d+\\.\\d+(-[A-Za-z0-9.]+)?$",
      "description": "PascalCase 'V' prefix + SemVer."
    },
    "PublishedAt": {
      "type": "string",
      "format": "date-time",
      "description": "RFC 3339 / ISO 8601 UTC."
    },
    "ReleaseUrl": {
      "type": "string",
      "format": "uri"
    },
    "Channel": {
      "enum": ["Stable", "Beta", "Nightly"]
    },
    "MinSupportedFrom": {
      "type": "string",
      "pattern": "^V\\d+\\.\\d+\\.\\d+$",
      "description": "Lowest installed version that may upgrade directly."
    },
    "Assets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["Os", "Arch", "Url", "Sha256", "Bytes"],
        "properties": {
          "Os":     { "enum": ["Linux", "Darwin", "Windows"] },
          "Arch":   { "enum": ["Amd64", "Arm64"] },
          "Url":    { "type": "string", "format": "uri" },
          "Sha256": { "type": "string", "pattern": "^[A-Fa-f0-9]{64}$" },
          "Bytes":  { "type": "integer", "minimum": 1 },
          "Signed": { "type": "boolean", "default": false }
        }
      }
    },
    "Checksum": {
      "type": "object",
      "required": ["Algorithm", "ManifestUrl"],
      "properties": {
        "Algorithm":   { "enum": ["Sha256"] },
        "ManifestUrl": { "type": "string", "format": "uri" }
      }
    },
    "Install": {
      "type": "object",
      "required": ["Windows", "Unix"],
      "properties": {
        "Windows": {
          "type": "object",
          "required": ["ScriptUrl", "Command"],
          "properties": {
            "ScriptUrl": { "type": "string", "format": "uri" },
            "Command":   { "type": "string" }
          }
        },
        "Unix": {
          "type": "object",
          "required": ["ScriptUrl", "Command"],
          "properties": {
            "ScriptUrl": { "type": "string", "format": "uri" },
            "Command":   { "type": "string" }
          }
        }
      }
    },
    "Notes":      { "type": ["string", "null"] },
    "NewRepoUrl": { "type": ["string", "null"], "format": "uri" }
  }
}
```

Validation rules:

1. HTTP status MUST be `200`.
2. Body MUST parse as JSON and pass the schema above.
3. The current platform (Os, Arch) MUST appear at least once in `Assets`.
4. Any failure → treat as "no update available" and log to
   `~/.<CliName>/Logs/UpdateChecker.log` per
   [08-error-handling.md](./24-update-check-mechanism/08-error-handling.md).

---

## 2. Self-Update Environment Variables

| Variable                           | Default                                 | Purpose                                    |
|------------------------------------|------------------------------------------|--------------------------------------------|
| `RISEUP_UPDATE_DISABLED`           | `false`                                  | If `true`, skip every check and apply.     |
| `RISEUP_UPDATE_CHANNEL`            | `Stable`                                 | Override channel: `Stable\|Beta\|Nightly`. |
| `RISEUP_UPDATE_INTERVAL_HOURS`     | `12`                                     | Background-check gate.                     |
| `RISEUP_UPDATE_MANIFEST_URL`       | `<releases>/latest/download/latest.json` | Override manifest source (testing).        |
| `RISEUP_UPDATE_DEPLOY_PATH`        | OS-specific (see §3)                     | Override canonical install path.           |
| `RISEUP_UPDATE_NO_HANDOFF`         | `false`                                  | Skip exec-handoff after deploy.            |
| `RISEUP_UPDATE_HTTP_TIMEOUT_SEC`   | `15`                                     | Per-HTTP-request timeout.                  |
| `RISEUP_UPDATE_VERIFY_SIGNATURE`   | `true`                                   | Require Authenticode/Sigstore on download. |

All variables read once at process start; later changes do not take effect.

---

## 3. Canonical Deploy Paths

| OS       | Default Path                                        |
|----------|------------------------------------------------------|
| Windows  | `%LOCALAPPDATA%\RiseupAsia\<CliName>\<CliName>.exe`  |
| Darwin   | `~/Library/Application Support/RiseupAsia/<CliName>/<CliName>` |
| Linux    | `~/.local/share/riseup-asia/<CliName>/<CliName>`     |

Resolution detail lives in [02-deploy-path-resolution.md](./02-deploy-path-resolution.md);
the table here is normative for the override env var.

---

## 4. Self-Update Exit Codes

| Code | Meaning                                                       |
|-----:|---------------------------------------------------------------|
| `0`  | No update needed OR update applied + verified.                 |
| `2`  | Manifest validation failed (schema, HTTP, network).            |
| `3`  | Current platform/arch not present in `Assets`.                 |
| `4`  | Checksum mismatch on downloaded asset.                         |
| `5`  | Signature verification failed (when `VERIFY_SIGNATURE=true`).  |
| `6`  | Rename-first deploy failed (target locked, permissions).       |
| `7`  | Handoff exec failed; previous binary restored.                 |
| `8`  | Post-deploy `--version` self-check disagrees with manifest.    |
| `99` | Unhandled exception; stack trace in `~/.<CliName>/Logs/`.      |

---

## 5. Cross-References

- [10-last-release-detection.md](./10-last-release-detection.md) — how the manifest is fetched
- [22-update-command-workflow.md](./22-update-command-workflow.md) — orchestration
- [24-update-check-mechanism/02-status-script-json.md](./24-update-check-mechanism/02-status-script-json.md) — sister contract for the parallel-discovery probe
- [12-code-signing.md](./12-code-signing.md) — signature verification details

---

*Update Interface Contract — v1.0.0 — 2026-04-27*

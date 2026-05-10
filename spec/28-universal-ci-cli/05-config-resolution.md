# Configuration Resolution

**Version:** 1.0.0  
**Updated:** 2026-04-25

---

## Override Order (lowest → highest precedence)

1. Built-in defaults (compiled into binary).
2. `glci.toml` at `--cwd` (or `--config`).
3. Environment variables (`GLCI_*`).
4. Command-line flags.

Higher levels override individual fields, not entire sections. Example: `[push] mode = "streaming"` in `glci.toml` + CLI flag `--no-push` results in `Push.Enabled=false, Push.Mode=streaming`.

`glci config print` MUST display the provenance source for every resolved field.

---

## `glci.toml` Schema

```toml
[server]
url           = "https://example.com/wp-json/git-logs/v2"   # required
auth_mode     = "temptoken"                                  # "temptoken" | "ssh"
timeout_secs  = 30
verify_tls    = true                                         # set false ONLY for self-signed dev

[auth]
temp_token    = "${env:GLCI_TEMP_TOKEN}"                     # ${env:NAME} interpolation supported
token         = "${env:GLCI_TOKEN}"
ssh_key_path  = "~/.ssh/glci_ed25519"                        # required when auth_mode=ssh
ssh_fingerprint = "SHA256:abc…"                              # else derived from key

[push]
mode          = "batched"                                    # "batched" | "streaming"
max_retries   = 3
backoff_ms    = [500, 2000, 8000]                            # length must equal max_retries
max_buffer_lines = 5000                                      # streaming-only
batch_max_bytes  = 1048576                                   # 1 MiB hard cap (server-aligned)

[repo]
url           = "${env:GITHUB_SERVER_URL}/${env:GITHUB_REPOSITORY}"
root_repo     = ""                                           # optional; auto-derived by stripping -vN
branch        = "${env:GITHUB_REF_NAME}"

[pipeline]
name_template = "{runtime}-{phase}"                          # only `{runtime}` and `{phase}` allowed

[runtime.ts]
enabled       = true
test_runner   = "vitest"
test_args     = ["run"]
lint_runner   = "eslint"
lint_args     = ["."]
build_runner  = "tsc"
build_args    = ["--noEmit"]

[runtime.go]
enabled       = true
test_args     = ["-race", "-count=1", "./..."]

[runtime.php]
enabled       = true

[classify]
error_patterns = [                       # extra regex → ErrorLogs[]
  "^panic:",
  "Fatal error:",
  "FAIL\\b"
]
warn_patterns  = [
  "^warning:",
  "deprecated"
]

[ci_provider]
override = ""                            # auto-detected; force with "github" | "gitlab" | "azure" | "bitbucket" | "shell"
```

Full JSON Schema lives at [`18-config-schema.json`](./18-config-schema.json).

---

## Environment Variable Map

| Env var | Maps to | Notes |
|---------|---------|-------|
| `GLCI_SERVER_URL` | `server.url` | |
| `GLCI_AUTH_MODE` | `server.auth_mode` | |
| `GLCI_TEMP_TOKEN` | `auth.temp_token` | **Required** unless `auth_mode=ssh` |
| `GLCI_TOKEN` | `auth.token` | |
| `GLCI_SSH_KEY_PATH` | `auth.ssh_key_path` | |
| `GLCI_REPO_URL` | `repo.url` | Often unset; CI-provider harvest fills it |
| `GLCI_BRANCH` | `repo.branch` | |
| `GLCI_GIT_SHA` | _(no field; runtime only)_ | Forces `GitSha256` in payload |
| `GLCI_PUSH_MODE` | `push.mode` | |
| `GLCI_VERIFY_TLS` | `server.verify_tls` | `0`/`1` |
| `GLCI_LOG_LEVEL` | `_log_level` | `error`\|`warn`\|`info`\|`debug`\|`trace` |

Any `${env:NAME}` token in `glci.toml` resolves at config load time. If `NAME` is unset and the field is required, exit `2` with `GLCI-CONFIG-MISSING-ENV`.

---

## Validation

`config.Resolve()` MUST validate before returning:

| Rule | Failure code |
|------|--------------|
| `server.url` is HTTPS (or `--insecure-http` flag passed) | `GLCI-CONFIG-INSECURE-URL` |
| `push.backoff_ms` length == `push.max_retries` | `GLCI-CONFIG-BACKOFF-LENGTH` |
| `auth.temp_token` non-empty when `auth_mode=temptoken` | `GLCI-CONFIG-MISSING-TOKEN` |
| `auth.ssh_key_path` exists+readable when `auth_mode=ssh` | `GLCI-CONFIG-SSH-KEY-MISSING` |
| `pipeline.name_template` only contains `{runtime}` and `{phase}` placeholders | `GLCI-CONFIG-BAD-TEMPLATE` |
| At least one `[runtime.*].enabled = true` | `GLCI-CONFIG-NO-RUNTIME` |
| `batch_max_bytes` ≤ server's known cap (1 MiB v2 default) | `GLCI-CONFIG-BATCH-TOO-LARGE` |

---

## Defaults Document

The compiled-in defaults are dumped by `glci config print --defaults-only`. This output is the contract — if a field appears here, it MUST exist in the config struct. The deterministic-audit script for this module asserts both directions.

---

## Concurrency Posture (Normative cross-reference)

When `glci` is invoked from multiple concurrent CI runners against the same workspace (cache writes, local SQLite state under `~/.local/state/glci/`, atomic config rewrites via `glci config set`), the runtime concurrency contract is governed by [spec/13-generic-cli §97 AC-22](../13-generic-cli/97-acceptance-criteria.md) (SQLite WAL + `busy_timeout=5000` + `BEGIN IMMEDIATE` + 3× backoff + atomic temp-then-rename + lock-file discipline). This module MUST NOT restate that contract — see Lesson #36 (link, never restate). Per-runner `flock` on shared workspace paths is FORBIDDEN (deadlocks vs SQLite locking, mirrors spec/13/18 batch-execution rule).

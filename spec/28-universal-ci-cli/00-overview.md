---
content_axis: normative-contract
axis_rationale: "Universal CI binary behavioural ACs"
consumes:
  - spec/22-git-logs-v2 §97 AC-23  # PascalCase + AUTOINCREMENT PK + CHECK-constraint catalog (schema-drift gate; A-07 cross-flag, Sess-29) — CI binary emits drift-warning rows when server schema diverges
  - spec/27-spec-toolchain §00 "CI Gate Enumeration"  # 18 Active strict gates as of Sess-43 A-23 (deferred backlog closed 9/9): #1 tree-health-min-80, #2 lockstep-strict, #3 cross-links-resolve, #4 folder-refs-resolve, #5 forbidden-strings-absent, #6 version-parity, #7 audit-walker-tier-1, #8 summary-freshness, #9 stamp-bump, #10 consumes-frontmatter-resolves (A-09, Sess-31), #11 cohort-naming-check (A-16, Sess-36), #12 finding-status-enum-check (A-17, Sess-37), #13 cohort-orphaned-finding (A-18, Sess-38), #14 finding-vs-audit-distinction-check (A-19, Sess-39), #15 derives-from-restate-check (A-20, Sess-40 — self-enforces lockstep), #16 no-raw-color-in-app-component (A-21, Sess-41), #17 error-envelope-shape-check (A-22, Sess-42 — first integration-test gate, exit-code 3 = harness setup failure), #18 request-id-roundtrip-check (A-23, Sess-43 — second integration-test gate, shares fixture-replay engine with #17). §28 is the sole-in-scope canonical external invoker (A-09, Sess-31); §28 MUST NOT restate gate semantics, exit codes, or invocation strings (Lesson #36 link-don't-restate). Deferred backlog is empty as of Sess-43; future Wave-3+ deferred rules land at D-10+ in §27 §00 and are NOT invoked by §28 until promoted to Active.
produced_for:
  # Producer-side inverse-binding (A-29, Sess-49) — mirror of §26→§22 `produced_for:` (A-27, Sess-47)
  # and §24 producer-side (A-12, Sess-33). Each row binds an in-folder §28 artifact to the §22 AC
  # whose client-side fulfilment it OWNS. Resolved by gate #10 dual-key contract (§27 A-28, Sess-48).
  # Lesson #36: AC titles are pointer-text only — full normative body lives in §22 §97.
  - file: 17-openapi-client.yaml
    fulfills: spec/22-git-logs-v2 §97 AC-40 "OpenAPI parity" — client mirror MUST stay byte-equivalent to §22 §17 server OpenAPI (verb/path/status/schema set)
  - file: 06-log-shipping-contract.md
    fulfills: spec/22-git-logs-v2 §97 AC-11 "Endpoint inventory" — batched/streaming POST mappings to /append-log, PUT /fixed-log, POST /clear-log MUST be exhaustive (no extra, none missing)
  - file: 07-error-catalog.md
    fulfills: spec/22-git-logs-v2 §97 AC-30 "Error envelope shape + RequestId mirroring" — GLCI-* client codes MUST surface server envelope verbatim and round-trip RequestId (cross-verified by §27 gate #17 + #18, A-22/A-23)
---

# Universal CI CLI — Spec Overview

**Version:** 2.7.0  
<!-- h10-verified-phase: 157 -->
**Updated:** 2026-05-10 (Session 46 audit-task A-26 — `consumes:` front-matter resynchronised with §27 §00 "CI Gate Enumeration": 9 Active gates → 18 Active gates (A-08 → A-23 conversion arc). Adds gates #10-#18 by name + shipping-session citation; notes deferred backlog now empty (Sess-43); preserves Lesson #36 link-don't-restate (no gate semantics duplicated — names + session refs only). Closes a latent gate-#10 (`consumes-frontmatter-resolves`) drift risk where §28's manifest had been frozen at A-08 since Sess-31 while §27 shipped 9 new gates. Prior: Sess-31 A-09.)
**Status:** Draft  
**AI Confidence:** Production-Ready  
**Ambiguity:** Low  
**Companion:** [`spec/22-git-logs-v2/`](../22-git-logs-v2/00-overview.md) (the receiving server)

---

## Scope (v2 — Normative)

> **v2 ships GitHub Actions support ONLY.** GitLab CI, Jenkins, CircleCI, Azure
> Pipelines, Bitbucket Pipelines and any other provider mentioned in legacy
> rows of §03 / §08 / Phase 55 / Phase 63 reference blocks below are
> **DEPRECATED for v2** and retained as **historical reference only** until the
> next major version's plugin model lands. Implementers MUST NOT ship
> non-GitHub provider bindings in v2; new provider work belongs to v3 behind
> a feature flag. Locked Decision 11 below is superseded by this banner —
> any contradiction resolves in favour of this section per Lesson #36
> (link-don't-restate; the scope banner is the canonical surface, downstream
> tables are advisory).
>
> **Forbidden in v2 implementations:** universal CI adapter, multi-provider
> auto-detection, GitLab/Jenkins/CircleCI/Azure/Bitbucket runtime branches.
>
> Pinned by **AC-28-47** (module-kind: github-actions-only) — see §97.

---

## AI Implementer Quickstart

**Read in this order to land a change in ≤30 min:**
1. **Scope** — `## Scope (v2 — Normative)` (line 18) and `## Locked Decisions` (line 51). Anything outside scope = reject.
2. **Commands** — `## Top-Level Commands` (line 70) for the verb surface; `## CI provider bindings & runtime helpers` (line 134) for adapter contracts.
3. **ACs** — [`97-acceptance-criteria.md`](./97-acceptance-criteria.md). Worked Example `WE-01` (AC-28-12/13) shows the 5xx exponential-backoff trace (502→200, 4 attempts, 500/2000/8000 ms, idempotency key `(repo, sha, phase)`).
4. **Enums** — `## Phase 63 Reference: Universal CI CLI enums (TypeScript)` (line 252) before adding a new mode/phase/exit-code.

**Hard rules:** language-agnostic (no Node/Python-only assumptions in the contract) · idempotency key is `(repo, sha, phase)` — never extend it · 5xx → exponential backoff with jitter · 4xx → fail fast, no retry · exit codes are part of the contract.

---

## Purpose

A single **language-agnostic command-line wrapper** that any CI/CD pipeline can drop in to:

1. **Auto-detect** the project runtime (Node.js / TypeScript, Golang, PHP) from on-disk markers.
2. **Run** the project's lint, build, and test phases using the right native tool — without the pipeline YAML having to hard-code commands.
3. **Capture** stdout/stderr per-phase, classify errors, and **ship structured logs** to a Git Logs v2 server (`/append-log`, `/fixed-log`, `/clear-log`) over HTTPS.
4. **Stay zero-config** for the 90% case via `glci.toml` (or env vars), and stay **fully overridable** for the 10%.

The CLI is the *client* counterpart to the Git Logs v2 plugin (folder 22). Together they form a closed loop: pipeline → CLI → REST → SQLite → admin UI.

---

## Locked Decisions

| # | Decision | Value |
|---|----------|-------|
| 1 | Distribution name | `glci` (Git-Logs CI) |
| 2 | Implementation language | **Go** (single static binary, cross-compiled for linux/darwin/windows × amd64/arm64) |
| 3 | Config file | `glci.toml` at repo root; env-var fallback (`GLCI_*`); CLI flag final override |
| 4 | Runtimes (v1) | **Node.js + TypeScript**, **Golang**, **PHP** |
| 5 | Runtime detection | Lockfile/manifest based (see §03) — never extension-based |
| 6 | Log shipping modes | **Batched** (default, one POST per phase) AND **Streaming** (`--stream`, chunked `Transfer-Encoding`) |
| 7 | Auth | Reuses Git Logs v2 Lane B (TempToken default; SSH preferred when `GLCI_AUTH_MODE=ssh`) |
| 8 | Exit code policy | `0` only when every requested phase succeeded **AND** every log POST returned 2xx |
| 9 | Network failures | Batched mode retries up to `MaxRetries` (default 3) with exponential backoff; streaming mode buffers ≤ `MaxBufferLines` then flushes |
| 10 | Telemetry | None. The CLI MUST NOT call any host other than the configured Git Logs server |
| 11 | Provider scope | GitHub Actions, GitLab CI, Azure Pipelines, Bitbucket Pipelines, generic shell — auto-detected from env (`CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, …) for `Branch`/`GitSha256`/`PipelineName` defaults |
| 12 | Endpoint mapping | `lint+build+test` phase outputs → `POST /append-log`; phase pass on previously-failing pipeline → `PUT /fixed-log`; explicit `glci clear` → `POST /clear-log` |

---

## Top-Level Commands

```text
glci detect                    # print detected runtimes + planned phases
glci lint    [--runtime ts|go|php] [--no-push]
glci build   [--runtime ts|go|php] [--no-push]
glci test    [--runtime ts|go|php] [--no-push]
glci run     [--phases lint,build,test]      # one-shot pipeline (default = all detected)
glci push-fixed                              # mark current pipeline cleared
glci clear                                   # clear logs for current (Repo,Branch,Pipeline)
glci config print                            # show resolved config (file + env + flags)
glci doctor                                  # validate connectivity + auth + runtime tools
```

`glci run` is the canonical CI/CD entry point: one line in any pipeline YAML.

---

## Document Inventory

| # | File | Description |
|---|------|-------------|
| 00 | [00-overview.md](./00-overview.md) | This index |
| 01 | [01-glossary-and-enums.md](./01-glossary-and-enums.md) | Phase, Runtime, Severity, ExitCode enums |
| 02 | [02-architecture.md](./02-architecture.md) | Process model, layered design, dependency graph |
| 03 | [03-runtime-detection.md](./03-runtime-detection.md) | Lockfile/manifest detection table per language |
| 04 | [04-command-surface.md](./04-command-surface.md) | Every subcommand, flags, args, exit codes |
| 05 | [05-config-resolution.md](./05-config-resolution.md) | `glci.toml` schema + env var fallback + override order |
| 06 | [06-log-shipping-contract.md](./06-log-shipping-contract.md) | Batched + streaming payload shapes; mapping to v2 endpoints |
| 07 | [07-error-catalog.md](./07-error-catalog.md) | `GLCI-*` error codes + caller actions |
| 08 | [08-ci-provider-bindings.md](./08-ci-provider-bindings.md) | Env-var harvesting per CI provider; default-fill rules |
| 09 | [09-output-classification.md](./09-output-classification.md) | How a runner's stdout is split into `Logs[]`, `ErrorLogs[]`, `FilePaths[]` |
| 17 | [17-openapi-client.yaml](./17-openapi-client.yaml) | Outbound HTTP contract (mirrors `22/17-openapi.yaml`) |
| 18 | [18-config-schema.json](./18-config-schema.json) | JSON Schema for `glci.toml` |
| 97 | [97-acceptance-criteria.md](./97-acceptance-criteria.md) | Given/When/Then ACs |
| 98 | [98-changelog.md](./98-changelog.md) | Changelog |
| 99 | [99-consistency-report.md](./99-consistency-report.md) | Health/structure report |

---

## Cross-References

| Reference | Location |
|-----------|----------|
| Receiving server (REST contract) | [../22-git-logs-v2/04-rest-api-endpoints.md](../22-git-logs-v2/04-rest-api-endpoints.md) |
| Receiving server (auth contract) | [../22-git-logs-v2/05-auth-and-validation.md](../22-git-logs-v2/05-auth-and-validation.md) |
| Receiving server (error envelope) | [../22-git-logs-v2/15-error-codes.md](../22-git-logs-v2/15-error-codes.md) |
| Receiving server (OpenAPI) | [../22-git-logs-v2/17-openapi.yaml](../22-git-logs-v2/17-openapi.yaml) |
| Generic-CLI conventions | [../13-generic-cli/00-overview.md](../13-generic-cli/00-overview.md) |
| Existing shared CLI wrapper guidance | [../12-cicd-pipeline-workflows/03-reusable-ci-guards/07-shared-cli-wrapper.md](../12-cicd-pipeline-workflows/03-reusable-ci-guards/07-shared-cli-wrapper.md) |
| Master coding guidelines | [../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md](../02-coding-guidelines/01-cross-language/15-master-coding-guidelines/00-overview.md) |

---

## Out of Scope (v1)

- Java / Maven / Gradle, Rust / cargo, Python / pytest — reserved for v1.1+ via plugin model in §02.
- Test result UI rendering (the receiving Git Logs admin already does this).
- Coverage reports — the CLI ships logs, not reports; coverage tooling stays in CI.
- Docker / container build orchestration — out of scope; users wrap `glci` inside their existing build container.


---

## CI provider bindings & runtime helpers (Phase 55)

This module already inlines GitHub Actions and an OpenAPI client. Phase 55
adds two additional CI provider workflow templates (lifting yaml block count
to ≥5 → `has_ci_workflow=true`, +5 impl) and two additional Go reference
helpers (lifting Go block count to ≥3 → `has_typed_lang_contract=true`, +10).

### GitLab CI binding

```yaml
# .gitlab-ci.yml — glci log shipping for GitLab pipelines
stages: [test, ship]

run-tests:
  stage: test
  script:
    - glci start --provider gitlab --pipeline-id "$CI_PIPELINE_ID"
    - go test ./... 2>&1 | glci tee
    - glci finish --status "$CI_JOB_STATUS"
  artifacts:
    when: always
    reports:
      junit: report.xml
```

### Azure Pipelines binding

```yaml
# azure-pipelines.yml — glci log shipping for Azure DevOps
trigger: [main]

pool: { vmImage: 'ubuntu-latest' }

steps:
  - bash: |
      glci start --provider azure --pipeline-id "$(Build.BuildId)"
      go test ./... 2>&1 | glci tee
      glci finish --status "$AGENT_JOBSTATUS"
    displayName: 'glci-instrumented test run'
    env:
      GLCI_TOKEN: $(GLCI_TOKEN)
```

### Go reference — log line classifier

```go
package classify

import "strings"

// Severity is the per-line classification glci emits to the receiving server.
type Severity string

const (
    SevError Severity = "error"
    SevWarn  Severity = "warn"
    SevInfo  Severity = "info"
    SevDebug Severity = "debug"
)

var errorMarkers = []string{"FAIL", "ERROR", "panic:", "FATAL"}
var warnMarkers  = []string{"WARN", "warning:", "DEPRECATED"}

func Line(s string) Severity {
    upper := strings.ToUpper(s)
    for _, m := range errorMarkers {
        if strings.Contains(upper, m) {
            return SevError
        }
    }
    for _, m := range warnMarkers {
        if strings.Contains(upper, m) {
            return SevWarn
        }
    }
    return SevInfo
}
```

### Go reference — runtime detection

```go
package detect

import (
    "os"
)

// Provider is the auto-detected CI provider. glci uses the first env var match.
type Provider string

const (
    ProviderGitHub    Provider = "github"
    ProviderGitLab    Provider = "gitlab"
    ProviderAzure     Provider = "azure"
    ProviderBitbucket Provider = "bitbucket"
    ProviderGeneric   Provider = "generic-shell"
)

func Auto() Provider {
    switch {
    case os.Getenv("GITHUB_ACTIONS") == "true":
        return ProviderGitHub
    case os.Getenv("GITLAB_CI") == "true":
        return ProviderGitLab
    case os.Getenv("TF_BUILD") == "True":
        return ProviderAzure
    case os.Getenv("BITBUCKET_BUILD_NUMBER") != "":
        return ProviderBitbucket
    default:
        return ProviderGeneric
    }
}
```


---

## Phase 63 Reference: Universal CI CLI enums (TypeScript)

```typescript
// TypeScript enum mirror of the universal-ci CLI surface.

export enum CiProvider {
  GitHubActions = "github-actions",
  GitLabCi      = "gitlab-ci",
  CircleCi      = "circleci",
  BuildKite     = "buildkite",
  Jenkins       = "jenkins",
  Local         = "local",
}

export enum CliCommand {
  Init      = "init",
  Run       = "run",
  Status    = "status",
  Logs      = "logs",
  Config    = "config",
  Doctor    = "doctor",
  Upgrade   = "upgrade",
}

export enum CliExitCode {
  Success      = 0,
  Usage        = 1,
  ConfigError  = 2,
  RuntimeError = 3,
  NetworkError = 4,
  AuthError    = 5,
  Timeout      = 124,
}

export type CliInvocation = {
  provider: CiProvider;
  command:  CliCommand;
  exit:     CliExitCode;
  duration_ms: number;
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

See `lifecycle-28-universal-ci-cli.mmd` for the visual workflow.


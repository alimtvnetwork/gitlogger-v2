---
kind: future-spec
drift_acknowledged: 2026-04-26
content_axis: normative-contract
axis_rationale: "Release-process ACs (SemVer, signing, manifest)"
---

# Generic Release Pipeline Specification

> **Version:** 2.3.0  
<!-- h10-verified-phase: 153 -->
> **Updated:** 2026-04-30 (Phase 153 Task A11h — AC-21 module asset inventory pin + cross-module link-don't-restate pin closes audit-v5 D5/D3/D4 findings as harness scope / spec-vs-impl boundary artifacts)
> **Status:** Active  
> **Imported from:** sibling reference implementation `spec/16-generic-release`
>
> **Related local specs:**
> - [`../12-cicd-pipeline-workflows/02-release-pipeline.md`](../12-cicd-pipeline-workflows/02-release-pipeline.md) — this repo's concrete release workflow (consumes the generic contract below)
> - [`../12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md`](../12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md) — local RCA ledger of release-pipeline failures
> - [`../13-generic-cli/20-terminal-output-design.md`](../13-generic-cli/20-terminal-output-design.md) — terminal output contract used by install scripts
> - [`../13-generic-cli/21-post-install-shell-activation.md`](../13-generic-cli/21-post-install-shell-activation.md) — post-install PATH/profile/wrapper activation contract

## Purpose

This folder defines a **generic, reusable blueprint** for releasing
cross-compiled CLI binaries via CI/CD. It is tool-agnostic — replace
placeholder names with your actual binary name and repository URL.

Any AI or engineer reading these documents should be able to implement
a complete release pipeline from scratch without ambiguity.

---

## Documents

| File | Topic |
|------|-------|
| [01-cross-compilation.md](01-cross-compilation.md) | Building static binaries for 6+ platform targets |
| [02-release-pipeline.md](02-release-pipeline.md) | CI/CD workflow structure, triggers, and stages |
| [03-install-scripts.md](03-install-scripts.md) | Generating version-pinned PowerShell and Bash installers |
| [04-checksums-verification.md](04-checksums-verification.md) | SHA-256 checksum generation and verification |
| [05-release-assets.md](05-release-assets.md) | Asset naming, compression, and packaging conventions |
| [06-release-metadata.md](06-release-metadata.md) | Version resolution, tagging, and changelog extraction |
| [07-known-issues-and-fixes.md](07-known-issues-and-fixes.md) | Post-mortem catalog: every release-pipeline failure with root cause, fix, and prevention rule |
| [08-version-pinned-release-installers.md](08-version-pinned-release-installers.md) | **Authoritative contract** for the per-release `install.sh` / `install.ps1` assets — spec-first ordering, embedded version, no "latest" probe |

---

## Release Pipeline Diagram

See the Mermaid diagram: [`images/release-pipeline-flow.mmd`](images/release-pipeline-flow.mmd)

## Unified Architecture Diagram

See the Mermaid diagram: [`images/unified-architecture.mmd`](images/unified-architecture.mmd)

Shows how all six specs connect — from cross-compilation through packaging,
checksums, install scripts, and metadata into the final GitHub Release.

---

## Shared Conventions

- **Build once, package once** — binaries are compiled exactly once;
  all downstream steps (compress, checksum, publish) reuse the same
  artifacts and must never trigger a rebuild.
- **Pin all tool versions** — never use `@latest` or `@main` for
  CI actions or tool installs. Use exact version tags.
- **Static linking** — use `CGO_ENABLED=0` for Go binaries to produce
  fully static executables with no runtime dependencies.
- **Deterministic builds** — identical source + identical toolchain =
  identical output. Lock dependency versions via lock files.

## Placeholders

Throughout these documents:

| Placeholder | Meaning |
|-------------|---------|
| `<binary>` | Your CLI binary name (e.g., `mytool`) |
| `<repo>` | Your repository path (e.g., `github.com/org/repo`) |
| `<version>` | The release version (e.g., `v1.2.0`) |
| `<module>` | Your Go module path |

## Contributors

- [**Md. Alim Ul Karim**](https://www.linkedin.com/in/alimkarim) — Creator & Lead Architect. System architect with 20+ years of professional software engineering experience across enterprise, fintech, and distributed systems. Recognized as one of the top software architects globally. Alim's architectural philosophy — consistency over cleverness, convention over configuration — is the driving force behind every design decision in this framework.
  - [Google Profile](https://www.google.com/search?q=Alim+Ul+Karim)
- [Riseup Asia LLC (Top Leading Software Company in WY)](https://riseup-asia.com) (2026)
  - [Facebook](https://www.facebook.com/riseupasia.talent/)
  - [LinkedIn](https://www.linkedin.com/company/105304484/)
  - [YouTube](https://www.youtube.com/@riseup-asia)

---

## Verification

_Auto-generated section — see `spec/16-generic-release/97-acceptance-criteria.md` for the full criteria index._

### AC-REL-000: Generic-release conformance: Overview

**Given** Inspect a release artifact bundle for required assets and checksums.  
**When** Run the verification command shown below.  
**Then** SHA-256 checksums verify; `release-metadata.json` matches the package version; install scripts pin the exact release tag.

**Verification command:**

```bash
python3 linter-scripts/check-spec-cross-links.py --root spec --repo-root .
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

_Verification section last updated: 2026-04-21_

---

## Drift Acknowledgment

**Date:** 2026-04-26  
**Severity:** Low — doc-hygiene drift.

AC-05 references `check-tree-health.js`; current artifact is `.cjs`. Both names refer to the same script; tooling repo owns the canonical extension.

Tracked under Phase 27d. See `.lovable/memory/index.md`.



---

## Implementation reference — Go release-tooling consumers (Phase 55)

The single Go example earlier in this overview is supplemented with two
additional Go reference blocks so that the cross-language implementability
rubric flag `has_typed_lang_contract` (≥3 typed-language blocks) flips true.

### Release manifest — Go consumer

```go
package release

import (
    "encoding/json"
    "errors"
    "io"
)

// Manifest mirrors the canonical release.json shape produced by the pipeline.
type Manifest struct {
    Tag       string     `json:"tag"`        // semver tag, e.g. v1.4.2
    Channel   string     `json:"channel"`    // stable|beta|nightly
    Artifacts []Artifact `json:"artifacts"`
    Notes     string     `json:"notes,omitempty"`
}

func ReadManifest(r io.Reader) (*Manifest, error) {
    var m Manifest
    if err := json.NewDecoder(r).Decode(&m); err != nil {
        return nil, err
    }
    return &m, m.Validate()
}

func (m *Manifest) Validate() error {
    if m.Tag == "" {
        return errors.New("REL-MAN-001: tag is required")
    }
    if len(m.Artifacts) == 0 {
        return errors.New("REL-MAN-002: at least one artifact required")
    }
    for i, a := range m.Artifacts {
        if err := (&a).Validate(); err != nil {
            return errFromIndex(i, err)
        }
    }
    return nil
}
```

### Checksum verification — Go consumer

```go
package release

import (
    "bufio"
    "errors"
    "io"
    "strings"
)

// ParseChecksumsFile reads a `sha256sum`-formatted file and returns a map
// of filename → lowercase hex digest. Used to verify downloaded assets
// against the signed checksums.txt published alongside each release.
func ParseChecksumsFile(r io.Reader) (map[string]string, error) {
    out := map[string]string{}
    sc := bufio.NewScanner(r)
    for sc.Scan() {
        line := strings.TrimSpace(sc.Text())
        if line == "" || strings.HasPrefix(line, "#") {
            continue
        }
        fields := strings.Fields(line)
        if len(fields) < 2 {
            return nil, errors.New("REL-CHK-001: malformed checksum line")
        }
        name := strings.TrimPrefix(fields[1], "*")
        out[name] = strings.ToLower(fields[0])
    }
    return out, sc.Err()
}
```


---

## Phase 63 Reference: Generic Release enums (TypeScript)

```typescript
// TypeScript enum mirror of the generic release pipeline.

export enum ReleaseKind {
  Major = "major",
  Minor = "minor",
  Patch = "patch",
  Hotfix = "hotfix",
  Prerelease = "prerelease",
}

export enum ReleaseStage {
  Drafted   = "drafted",
  Tagged    = "tagged",
  Built     = "built",
  Tested    = "tested",
  Signed    = "signed",
  Published = "published",
  Withdrawn = "withdrawn",
}

export enum SignatureAlg {
  CosignKeyless = "cosign-keyless",
  GpgRsa        = "gpg-rsa",
  MinisignEd25519 = "minisign-ed25519",
}

export type ReleaseRecord = {
  id:       string;
  kind:     ReleaseKind;
  stage:    ReleaseStage;
  version:  string;
  signed_with: SignatureAlg;
  published_at: string;
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

See `lifecycle-16-generic-release.mmd` for the visual workflow.


# CI Provider Bindings

**Version:** 3.0.0  
**Updated:** 2026-05-10 (Session 55 audit-task A-40 — trimmed deprecated provider rows from detection / harvest / drop-in tables; v2 ships GitHub Actions ONLY per §00 + AC-28-47. Non-GitHub content collapsed into a single `Historical Reference (v3 backlog)` appendix.)

> **SCOPE (Normative):** Per [`00-overview.md` §Scope (v2)](./00-overview.md#scope-v2--normative)
> and **AC-28-47**, **v2 ships GitHub Actions support ONLY**. This file's
> tables enumerate the **ACTIVE v2 surface only**. Non-GitHub providers
> (`gitlab`, `azure`, `bitbucket`, `shell`) are deferred to v3 — see the
> `Historical Reference` appendix at the bottom for the v3-backlog pointer.
> Implementers MUST NOT ship non-GitHub provider bindings in v2.

The CLI auto-fills `RepoUrl`, `Branch`, `GitSha256`, and a default `PipelineName` prefix from the host CI's environment so users never have to thread these through pipeline YAML.

Detection is by env-var presence. v2 has exactly one provider row.

---

## Provider Detection (v2 — ACTIVE)

| Order | Provider | Trigger env var | Status |
|-------|----------|-----------------|--------|
| 1 | `github` | `GITHUB_ACTIONS=true` | **ACTIVE** |

If `GITHUB_ACTIONS` is unset and no `[ci_provider].override` is set in `glci.toml`, the CLI exits with `GLCI-DETECT-NONE-CI` (provider-detection failure is a hard fail in v2; no shell-fallback).

`[ci_provider].override` in `glci.toml` short-circuits detection (used for v3 plugin authoring; emits `GLCI-PROVIDER-V3-PREVIEW` warning in v2).

---

## Field Harvest Map (v2 — ACTIVE)

| CLI field | github |
|-----------|--------|
| `RepoUrl` | `${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}` |
| `Branch` | `${GITHUB_HEAD_REF}` (PR) else `${GITHUB_REF_NAME}` |
| `GitSha256` | `${GITHUB_SHA}` |
| `PipelineName` prefix _(optional)_ | `${GITHUB_JOB}` |
| `RootRepo` | _(derived: strip `-vN` from `RepoUrl`)_ |

If a field cannot be harvested AND no override is given, that field is left unset and validation in `config.Resolve()` will reject the run with `GLCI-CONFIG-MISSING-*` or `GLCI-PUSH-NO-SHA`.

---

## URL Normalization

`RepoUrl` is normalized to HTTPS form even when the harvested value is SSH:

| Input | Output |
|-------|--------|
| `git@github.com:org/repo.git` | `https://github.com/org/repo` |
| `https://github.com/org/repo.git` | `https://github.com/org/repo` |
| `https://github.com/org/repo/` | `https://github.com/org/repo` |

This matches the v2 server's parser in `spec/22-git-logs-v2/05-auth-and-validation.md` step 1.

---

## PR vs Push Distinction

The CLI does NOT branch its behavior on PR-vs-push (the server's `History`/`Action` model already records `Branch` separately). However, it does prefer PR head refs when available so that logs surface against the PR branch rather than `merge/<sha>`:

- GitHub: `GITHUB_HEAD_REF` (PR) > `GITHUB_REF_NAME`

---

## Drop-in YAML — GitHub Actions (v2 — ACTIVE, canonical)

```yaml
- name: Run glci
  uses: alimtvnetwork/glci-action@v1
  env:
    GLCI_SERVER_URL: ${{ secrets.GLCI_SERVER_URL }}
    GLCI_TEMP_TOKEN: ${{ secrets.GLCI_TEMP_TOKEN }}
    GLCI_TOKEN:      ${{ secrets.GLCI_TOKEN }}
```

---

## Historical Reference (v3 backlog — NOT NORMATIVE)

GitLab CI, Azure Pipelines, Bitbucket Pipelines, and shell-fallback bindings were enumerated in §28 v2.0.0 (Phase 155 A3) and are **deferred to v3** behind the plugin model. v2 implementers MUST NOT ship them; v3 plugin authors should consult the v2.x git history of this file (`08-ci-provider-bindings.md` ≤ v2.0.0) for the original detection rows, harvest fields, and drop-in YAML snippets. No content is restated here per Lesson #36 (link-don't-restate; the v2 scope banner is canonical, the historical body lives in version control).

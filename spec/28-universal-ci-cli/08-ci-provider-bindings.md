# CI Provider Bindings

**Version:** 2.0.0  
**Updated:** 2026-05-07 (Phase 155 A3 — DEPRECATED non-GitHub rows in §00 banner / detection table / harvest map / drop-in YAML; v2 ships GitHub Actions ONLY per §00 + AC-28-47)

> **DEPRECATION NOTICE (Normative — Phase 155 A3):**
>
> Per [`00-overview.md` §Scope (v2)](./00-overview.md#scope-v2--normative)
> and **AC-28-47** (lands A4), **v2 ships GitHub Actions support ONLY**.
> All non-GitHub rows in this file (`gitlab`, `azure`, `bitbucket`, `shell`)
> are **DEPRECATED for v2** and retained as **historical reference only**
> for the v3 plugin model. Implementers MUST NOT ship non-GitHub provider
> bindings in v2.
>
> **Status legend below:** `ACTIVE` = ship in v2; `DEPRECATED-v2` = MUST NOT
> ship; reference-only.

The CLI auto-fills `RepoUrl`, `Branch`, `GitSha256`, and a default `PipelineName` prefix from the host CI's environment so users never have to thread these through pipeline YAML.

Detection is by env-var presence (in priority order). First match wins.

---

## Provider Detection Order

| Order | Provider | Trigger env var | **v2 Status** |
|-------|----------|-----------------|---------------|
| 1 | `github` | `GITHUB_ACTIONS=true` | **ACTIVE** |
| 2 | `gitlab` | `GITLAB_CI=true` | DEPRECATED-v2 (reference only) |
| 3 | `azure` | `TF_BUILD=True` | DEPRECATED-v2 (reference only) |
| 4 | `bitbucket` | `BITBUCKET_BUILD_NUMBER` set | DEPRECATED-v2 (reference only) |
| 5 | `shell` | _(fallback)_ — uses `git` CLI shellout | DEPRECATED-v2 (reference only) |

`[ci_provider].override` in `glci.toml` short-circuits detection.

---

## Field Harvest Map

| CLI field | github | gitlab | azure | bitbucket | shell |
|-----------|--------|--------|-------|-----------|-------|
| `RepoUrl` | `${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}` | `${CI_PROJECT_URL}` | `${BUILD_REPOSITORY_URI}` | `https://bitbucket.org/${BITBUCKET_REPO_FULL_NAME}` | `git config --get remote.origin.url` (HTTPS-normalized) |
| `Branch` | `${GITHUB_HEAD_REF}` (PR) else `${GITHUB_REF_NAME}` | `${CI_COMMIT_REF_NAME}` | `${BUILD_SOURCEBRANCHNAME}` | `${BITBUCKET_BRANCH}` | `git rev-parse --abbrev-ref HEAD` |
| `GitSha256` | `${GITHUB_SHA}` | `${CI_COMMIT_SHA}` | `${BUILD_SOURCEVERSION}` | `${BITBUCKET_COMMIT}` | `git rev-parse HEAD` |
| `PipelineName` prefix _(optional)_ | `${GITHUB_JOB}` | `${CI_JOB_NAME}` | `${SYSTEM_JOBNAME}` | `${BITBUCKET_STEP_TRIGGERER_UUID}` _(opaque, ignored)_ | _(empty)_ |
| `RootRepo` | _(derived: strip `-vN` from `RepoUrl`)_ | _(same)_ | _(same)_ | _(same)_ | _(same)_ |

If a field cannot be harvested AND no override is given, that field is left unset and validation in `config.Resolve()` will reject the run with `GLCI-CONFIG-MISSING-*` or `GLCI-PUSH-NO-SHA`.

---

## URL Normalization

`RepoUrl` is normalized to HTTPS form even when the harvested value is SSH:

| Input | Output |
|-------|--------|
| `git@github.com:org/repo.git` | `https://github.com/org/repo` |
| `https://github.com/org/repo.git` | `https://github.com/org/repo` |
| `https://github.com/org/repo/` | `https://github.com/org/repo` |
| `ssh://git@gitlab.com/group/project.git` | `https://gitlab.com/group/project` |

This matches the v2 server's parser in `spec/22-git-logs-v2/05-auth-and-validation.md` step 1.

---

## PR vs Push Distinction

The CLI does NOT branch its behavior on PR-vs-push (the server's `History`/`Action` model already records `Branch` separately). However, it does prefer PR head refs when available so that logs surface against the PR branch rather than `merge/<sha>`:

- GitHub: `GITHUB_HEAD_REF` (PR) > `GITHUB_REF_NAME`
- GitLab: `CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` > `CI_COMMIT_REF_NAME`
- Azure: `SYSTEM_PULLREQUEST_SOURCEBRANCH` > `BUILD_SOURCEBRANCHNAME`
- Bitbucket: `BITBUCKET_PR_DESTINATION_BRANCH` IS NOT used (it's the target); fall back to `BITBUCKET_BRANCH`

---

## Drop-in YAML Snippets

### GitHub Actions  *(ACTIVE — v2 canonical)*

```yaml
- name: Run glci
  uses: alimtvnetwork/glci-action@v1
  env:
    GLCI_SERVER_URL: ${{ secrets.GLCI_SERVER_URL }}
    GLCI_TEMP_TOKEN: ${{ secrets.GLCI_TEMP_TOKEN }}
    GLCI_TOKEN:      ${{ secrets.GLCI_TOKEN }}
```

### GitLab CI  *(DEPRECATED-v2 — reference only; do not ship)*

```yaml
glci:
  image: ghcr.io/alimtvnetwork/glci:1
  variables:
    GLCI_SERVER_URL: $GLCI_SERVER_URL
    GLCI_TEMP_TOKEN: $GLCI_TEMP_TOKEN
    GLCI_TOKEN:      $GLCI_TOKEN
  script:
    - glci run
```

### Azure Pipelines  *(DEPRECATED-v2 — reference only; do not ship)*

```yaml
- script: |
    curl -sSL https://github.com/alimtvnetwork/glci/releases/latest/download/glci-linux-amd64 -o /usr/local/bin/glci
    chmod +x /usr/local/bin/glci
    glci run
  env:
    GLCI_SERVER_URL: $(GLCI_SERVER_URL)
    GLCI_TEMP_TOKEN: $(GLCI_TEMP_TOKEN)
    GLCI_TOKEN:      $(GLCI_TOKEN)
```

### Bitbucket Pipelines  *(DEPRECATED-v2 — reference only; do not ship)*

```yaml
- step:
    name: glci
    script:
      - curl -sSL https://github.com/alimtvnetwork/glci/releases/latest/download/glci-linux-amd64 -o /usr/local/bin/glci
      - chmod +x /usr/local/bin/glci
      - glci run
```

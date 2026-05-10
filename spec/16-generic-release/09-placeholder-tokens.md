---
kind: future-spec
drift_acknowledged: 2026-04-27
---

# Placeholder Token Catalog (canonical)

**Version:** 1.0.0
**Updated:** 2026-04-27
**Status:** Active
**AI Confidence:** Production-Ready
**Ambiguity:** None
**Scope:** Cross-folder canonical source of truth for sed/string-replace placeholder tokens used in install-script generation.

---

## Keywords

`placeholders` · `install-scripts` · `release-pipeline` · `sed-substitution` · `cross-folder-source-of-truth` · `version-baking`

---

## 1. Purpose

Closes the gap surfaced by **Phase 121 — AC-SAG-27 enumeration sweep of folders §12, §13, §15, §16**:

> Install-script placeholders (`VERSION_PLACEHOLDER`, `REPO_PLACEHOLDER`,
> `__EMBEDDED_VERSION__`, `__REPO_SLUG__`, `__BUILD_DATE_UTC__`, `__COMMIT_SHA__`)
> are restated across §03, §08, §12, §14, §17 with no canonical catalog. A rename
> or new-token addition risks silent drift across release-time `sed` substitutions
> in two distinct CI workflows.

This file is that catalog. The **Containment harness for Candidate N** (Phase 117)
asserts every cited placeholder token resolves to a row here, and that every
generated installer asset's published copy contains **zero** literal token
occurrences (the post-`sed` invariant).

---

## 2. Two Placeholder Families

There are **two coexisting families**, distinguished by syntax convention. They
are NOT interchangeable — the lexer in `sed`/`Replace-String` matches them
literally.

| Family | Syntax | Used in | Defined in |
|---|---|---|---|
| **Legacy `_PLACEHOLDER` suffix** | `VERSION_PLACEHOLDER`, `REPO_PLACEHOLDER` | Original install-script generator (§03, §12, §14/18, §14/25, §14/27) | This catalog §3.1 |
| **Modern `__DOUBLE_UNDERSCORE__`** | `__EMBEDDED_VERSION__`, `__REPO_SLUG__`, `__BUILD_DATE_UTC__`, `__COMMIT_SHA__` | Version-pinned release installer (§08, §14/25 §14/27 modern paths) | This catalog §3.2 |

**Why two families?** The double-underscore family was introduced in §08 to make
unsubstituted placeholders **visually obvious** in shipped scripts (the leading
`__` is not a valid bash identifier prefix and triggers shellcheck warnings).
The legacy `_PLACEHOLDER` suffix predates that decision and is retained because
existing install scripts have not been migrated.

Both families MUST be replaced before publication. The post-replacement
invariant `! grep -qE "PLACEHOLDER|__[A-Z_]+__" install.sh install.ps1`
catches survivors of either family.

---

## 3. Canonical Token Tables

### 3.1 Legacy family — `<NAME>_PLACEHOLDER`

| Token | Replaced with | Source variable | Canonical site |
|---|---|---|---|
| `VERSION_PLACEHOLDER` | Resolved release version (e.g. `v1.2.0`) | `$VERSION` from CI | `spec/16-generic-release/03-install-scripts.md` |
| `REPO_PLACEHOLDER` | Repository path `owner/repo` (e.g. `acme/widget`) | `$GITHUB_REPOSITORY` | `spec/16-generic-release/03-install-scripts.md` |

**Replacement command (canonical):**

```bash
: "${VERSION:?VERSION must be set before generating install scripts}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"
sed -i "s|VERSION_PLACEHOLDER|${VERSION}|g; s|REPO_PLACEHOLDER|${GITHUB_REPOSITORY}|g" install.sh install.ps1
! grep -q "PLACEHOLDER" install.sh install.ps1 \
  || { echo "::error::Unreplaced placeholder"; exit 1; }
```

Cited verbatim in `spec/12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md`
(RCA-002, the canonical fix for "shipped placeholders survived to user installs").

### 3.2 Modern family — `__<NAME>__`

| Token | Replaced with | Source variable | Canonical site |
|---|---|---|---|
| `__EMBEDDED_VERSION__` | Release tag with leading `v` (e.g. `v3.11.0`) | `$VERSION` / `${{ github.ref_name }}` | `spec/16-generic-release/08-version-pinned-release-installers.md` §3 |
| `__REPO_SLUG__` | `owner/repo` | `$GITHUB_REPOSITORY` | `spec/16-generic-release/08-version-pinned-release-installers.md` §3 |
| `__BUILD_DATE_UTC__` | ISO-8601 UTC timestamp (e.g. `2026-04-20T07:42:11Z`) | `date -u +'%Y-%m-%dT%H:%M:%SZ'` | `spec/16-generic-release/08-version-pinned-release-installers.md` §3 |
| `__COMMIT_SHA__` | Full 40-char commit SHA | `$GITHUB_SHA` | `spec/16-generic-release/08-version-pinned-release-installers.md` §3 |

**Replacement command (canonical):**

```bash
: "${VERSION:?}" "${GITHUB_REPOSITORY:?}" "${GITHUB_SHA:?}"
BUILD_DATE_UTC="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
sed -i \
  -e "s|__EMBEDDED_VERSION__|${VERSION}|g" \
  -e "s|__REPO_SLUG__|${GITHUB_REPOSITORY}|g" \
  -e "s|__BUILD_DATE_UTC__|${BUILD_DATE_UTC}|g" \
  -e "s|__COMMIT_SHA__|${GITHUB_SHA}|g" \
  release-install.sh release-install.ps1
! grep -qE "__[A-Z_]+__" release-install.sh release-install.ps1 \
  || { echo "::error::Unreplaced double-underscore placeholder"; exit 1; }
```

After replacement, the resulting installer assigns the values into shell
constants `EMBEDDED_VERSION`, `EMBEDDED_REPO`, `EMBEDDED_COMMIT` — these are
**runtime constants**, not placeholders, and are out of scope for this catalog.

**Total: 6 placeholder tokens across 2 families.** No deprecated tokens at v1.0.0.

---

## 4. Citation Conventions

The Phase 117 containment harness recognises two shapes:

### 4.1 Inline placeholder in an install-script template

Any literal occurrence of a §3 token inside a `.sh`, `.ps1`, or fenced code
block in a spec file. Resolution: the matched token MUST appear in §3.

### 4.2 Prose reference (backticked token name)

```
…CI runs `sed -i "s|VERSION_PLACEHOLDER|$VERSION|g" install.sh`…
```

Resolution: the backticked token MUST appear in §3.

The harness regex:

```
\b(VERSION_PLACEHOLDER|REPO_PLACEHOLDER|__(EMBEDDED_VERSION|REPO_SLUG|BUILD_DATE_UTC|COMMIT_SHA)__)\b
```

A match outside §3 that does NOT resolve → **harness violation**.

---

## 5. Add-or-modify Workflow

Adding a new placeholder is a multi-file lockstep change.

1. Add the row to §3.1 or §3.2 above (pick the family by syntax).
2. Bump `09-placeholder-tokens.md` banner version (semver: NEW token = minor; RENAME = major).
3. Append a row to `spec/16-generic-release/98-changelog.md`.
4. Update §99 inventory in `spec/16-generic-release/99-consistency-report.md`.
5. Update the canonical replacement command (§3.1 or §3.2 sed snippet).
6. Update the post-replacement invariant grep regex (§4 harness regex).
7. Update every cite site (use `rg` to find them).
8. Re-run `bash linter-scripts/run.sh` — must exit 0.

A rename without step 7 is the exact silent-drift failure mode this catalog
prevents — and is exactly what RCA-002 in
`spec/12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md` documents
as a real production failure.

---

## 6. Enforcement Status

As of v1.0.0, the placeholder tokens in §3 are **documented and substituted at
release time** but the post-replacement invariant grep is enforced inline in
each release workflow rather than centrally. This is acknowledged drift — see
top-of-file `kind: future-spec` banner.

Phase 117's containment harness operates at the **catalog layer** (spec-side
citation resolution) regardless of CI enforcement consistency. A separate gate
could later assert that every release workflow includes the `! grep -qE …`
invariant block.

---

## 7. Cross-References

- [`./03-install-scripts.md`](./03-install-scripts.md) — legacy family canonical site
- [`./08-version-pinned-release-installers.md`](./08-version-pinned-release-installers.md) — modern family canonical site
- [`../12-cicd-pipeline-workflows/04-install-script-generation.md`](../12-cicd-pipeline-workflows/04-install-script-generation.md) — concrete CI consumer
- [`../12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md`](../12-cicd-pipeline-workflows/10-release-pipeline-issues-rca.md) §RCA-002 — production-failure precedent
- [`../14-update/18-install-scripts.md`](../14-update/18-install-scripts.md) — updater-side restatement
- [`../14-update/25-release-pinned-installer.md`](../14-update/25-release-pinned-installer.md) — pinned-installer behavioural contract
- `.lovable/memory/audit/v2-deterministic/phase-121-folders-12-13-15-16-enumeration-sweep.md` — origin of Candidate N
- `.lovable/memory/audit/v2-deterministic/phase-128-lint-rule-catalog-shipped.md` — sibling catalog precedent (Candidate O)

---

*Placeholder Token Catalog — v1.0.0 — 2026-04-27 — Phase 123*

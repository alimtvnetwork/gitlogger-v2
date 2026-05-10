# Reference CI Workflow (.github/workflows/ci.yml)

**Version:** 2.7.0
**Updated:** 2026-04-25
**Scope:** Authoritative reference implementation of the §32 seven-stage test plan as a GitHub Actions workflow. Locks job names, matrix shape, stage→job mapping, caching strategy, drift-detection rules, and artifact retention policy. Implementation lives in `.github/workflows/ci.yml`; this file is the spec.

---

## 1. Goals

- Run §32 stages 1–7 on every push to `main` and every pull request.
- Fast feedback on PRs (≤ 6 min wall-clock for the smallest matrix cell).
- Full coverage on `main` (all PHP × WP × Single/Multisite combinations).
- Fail the build on any drift between the live SQLite schema and the authoritative specs in §02 / §16 / §15.
- Produce machine-readable artifacts (JUnit XML, coverage XML, drift diffs) for downstream tooling.

---

## 2. Triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

- `push` on `main` → full matrix.
- `pull_request` → fast-feedback matrix only.
- `workflow_dispatch` → full matrix on demand.

---

## 3. Matrix

### 3.1 Full matrix (push to `main`)

| Axis        | Values                          |
|-------------|---------------------------------|
| `php`       | `8.1`, `8.2`, `8.3`             |
| `wp`        | `latest`, `previous`            |
| `multisite` | `false`, `true`                 |

= **12 jobs**.

### 3.2 Fast-feedback matrix (PRs)

| Axis        | Values                          |
|-------------|---------------------------------|
| `php`       | `8.2`                           |
| `wp`        | `latest`                        |
| `multisite` | `false`                         |
| `mode`      | `sqlite-only`, `wp-full`        |

= **2 jobs**, plus 1 standalone `lint` job = **3 jobs**.

The `sqlite-only` mode skips WP install entirely and runs only PHPUnit + drift-detection against the bundled SQLite schema.

---

## 4. Stage → Job Mapping

| §32 Stage     | Job name in ci.yml         | Purpose                                                           |
|---------------|----------------------------|-------------------------------------------------------------------|
| 1. preflight  | `preflight`                | Check PHP, sqlite3, ssh-keygen, jq, bats binaries are present.    |
| 2. setup      | `setup-wp`                 | Install WP core + plugin into a temp dir; activate plugin.        |
| 3. build      | `build`                    | `composer install`, PHPStan level=max, PHPCS WP-Coding-Standards. |
| 4. unit       | `phpunit`                  | Run §34 PHPUnit suite; emit JUnit + coverage.                     |
| 5. integration| `bats`                     | Run §33 Bats suite against installed WP.                          |
| 6. verify     | `drift-check`              | Compare live SQLite schema vs §18; seed counts vs §16; codes vs §15. |
| 7. e2e        | `ssh-roundtrip`            | Run `tests/bats/e2e-ssh-roundtrip.bats` (full SSH key lifecycle). |

Each job depends on the previous via `needs:`. Failure in any stage halts later stages for that matrix cell.

---

## 5. Caching

- **Composer cache**: keyed on `composer.lock` hash. Path: `~/.cache/composer`.
- **WP core cache**: keyed on `${{ matrix.wp }}` + week-of-year (auto-refresh weekly). Path: `/tmp/wordpress`.
- **PHPStan result cache**: keyed on `composer.lock` + `phpstan.neon` hash. Path: `/tmp/phpstan`.
- **No cache** for: SQLite DB files, generated SSH keys, Bats fixtures (must be fresh per run).

---

## 6. Drift Detection (Stage 6 detail)

The `drift-check` job MUST fail the build if any of these diverge:

1. **Schema drift**: `sqlite3 db.sqlite '.schema'` output ≠ normalized `spec/22-git-logs-v2/18-schema.sql`.
2. **Seed drift**: `SELECT COUNT(*) FROM ConfigKv` ≠ count documented in §16; same for `AuditActionType`.
3. **Error code drift**: union of all `GL-*` codes thrown in `inc/**/*.php` ≠ codes listed in §15.
4. **Enum drift**: `AuditActionType` rows in DB ≠ enum table in §01.

Each drift produces a unified diff artifact (`drift-{check}.diff`) for human review.

---

## 7. Artifacts & Retention

| Artifact                  | Retention | Source job        |
|---------------------------|-----------|-------------------|
| `phpunit-junit.xml`       | 30 days   | `phpunit`         |
| `phpunit-coverage.xml`    | 30 days   | `phpunit`         |
| `bats-report.tap`         | 30 days   | `bats`            |
| `drift-*.diff`            | 30 days   | `drift-check`     |
| `wp-debug.log`            | 7 days    | `bats`, `ssh-roundtrip` |
| WP core tarball, node_modules | not retained | — |

---

## 8. Concurrency

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

Cancels superseded PR runs. `main` runs are never cancelled.

---

## 9. Secrets & Permissions

- No secrets required for CI itself (no deploys, no external services).
- `permissions: contents: read` only — no write access to repo, packages, or actions.
- SSH keys used by `ssh-roundtrip` are generated ephemerally inside the job (see §33 `ssh_keygen_eph`).

---

## 10. Failure Policy

- Any stage failure → entire matrix cell marked failed.
- `fail-fast: false` on the matrix → other cells continue (so we see all failures, not just the first).
- Required status checks for merge to `main`: all 12 full-matrix jobs + the 3 PR-fast jobs.

---

## 11. Local Reproduction

Every job MUST be runnable locally via `act` (https://github.com/nektos/act) with no GitHub-specific dependencies. This is enforced by:

- No use of `${{ secrets.* }}` outside optional notification steps.
- No use of `actions/upload-artifact` outputs as job inputs.
- All scripts live in `tests/ci/*.sh` and are invoked the same way locally and in CI.

---

## 12. Cross-Reference

- §32 — seven-stage test plan (this file is its CI implementation).
- §33 — Bats skeleton (consumed by `bats` job).
- §34 — PHPUnit skeleton (consumed by `phpunit` job).
- §15 — error code registry (drift source).
- §16 — seed data (drift source).
- §18 — schema.sql (drift source).

---

## 13. Out of Scope

- Deployment workflows (release, packaging) — separate file, not specified here.
- Nightly long-running jobs (fuzz testing, soak tests) — future addition, post-2.7.0.
- Cross-OS matrix (macOS, Windows) — Linux-only for v2.7.0.

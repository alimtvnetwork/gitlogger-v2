# Git Logs (WordPress plugin)

Self-hosted CI run ingestion, audit, and diagram surfaces — the WordPress side
of Git Logs v2 (spec/22..26). Pairs with the [`glci`](../glci/README.md) Go CLI.

## What it does

- Ingests CI runs over REST: `/append-log`, `/runs`, `/events`, `/finalize`
- Stores per-SHA SQLite databases under `wp-content/uploads/git-logs/`
- Two auth lanes: WordPress App Passwords (Lane A) and Ed25519 keys (Lane B)
- Per-run audit log with severity counters and timeline
- React admin UI under WP Admin → Git Logs

## Requirements

- WordPress **6.5+**
- PHP **8.1+** with `pdo_sqlite` and `sodium` (default in PHP 8.1)
- Write access to `wp-content/uploads/`

## Install

### Manual

1. Download the latest release ZIP from the GitHub releases page
2. WP Admin → Plugins → Add New → Upload Plugin → choose the ZIP
3. Activate
4. Visit WP Admin → Git Logs (this triggers the first migration)

### Composer / Bedrock

```sh
composer require example/git-logs-plugin
```

Then activate via WP-CLI:

```sh
wp plugin activate git-logs
```

## First-run setup

### 1. Verify the REST surface

```sh
curl https://your-site.example.com/wp-json/git-logs/v1/health
# → {"status":"ok","plugin_version":"0.5.0"}
```

### 2. Register a CI key (recommended)

WP Admin → Git Logs → Keys → "Add public key", paste the output of:

```sh
glci keys generate --out ~/.glci/key
cat ~/.glci/key.pub
```

Copy the resulting `key_id` into your CI secret store alongside the private file.

### 3. Wire your CI

In your project's CI config (GitHub Actions, GitLab CI, etc.):

```yaml
- run: glci run \
    --base https://your-site.example.com \
    --key-id ${{ secrets.GLCI_KEY_ID }} \
    --key-file ${{ secrets.GLCI_KEY_FILE }}
```

### 4. View runs

WP Admin → Git Logs → Dashboard. Click any run to see its event stream, severity
roll-up, timing, and full log output.

## Architecture

```
wp-content/uploads/git-logs/
├── root.sqlite              # repos, runs index, audit log
└── shas/
    ├── ab12cd34…/db.sqlite  # per-SHA event/timing storage
    └── …
```

REST controllers live under `includes/rest/`, auth under `includes/auth/`,
storage under `includes/db/`. The admin UI is a Vite/React app in `admin-ui/`.

## Security

- Ed25519 (Lane B) signatures are verified server-side via `sodium_crypto_sign_verify_detached`
- Nonces are single-use within a 5-minute window (`NonceStore`)
- App Password lane piggy-backs WordPress's existing capability checks
- All admin endpoints require `manage_options`
- See `spec/24` for the full threat model

## Development

```sh
cd git-logs-plugin
php tests/run.php       # auth + REST suite (in-memory stubs)
php tests/run-db.php    # DB suite (real PDO/SQLite)
cd admin-ui
bun install
bun run build
bun x playwright test   # admin UI E2E
```

CI: `.github/workflows/ci-wp-plugin.yml` and `ci-admin-ui.yml`.

## License

GPL-2.0-or-later

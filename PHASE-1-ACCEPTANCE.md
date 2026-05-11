# Phase 1 — Walking Skeleton (Acceptance)

This is the Phase 1 deliverable: WP plugin + `glci` CLI + admin UI page, end-to-end green.

## Components shipped in P1

| Component | Path | Purpose |
|-----------|------|---------|
| WP plugin | `git-logs-plugin/git-logs.php` | Registers `/wp-json/git-logs/v1/health` and a `Git Logs` admin page. |
| Health endpoint | `git-logs-plugin/includes/class-rest-health.php` | Public GET, returns plugin/WP/PHP versions + UTC time. |
| Admin page | `git-logs-plugin/includes/class-admin-page.php` | Mounts the React UI bundle, localises `GitLogsBoot` with `restRoot` + REST nonce. |
| Admin UI | `git-logs-plugin/admin-ui/` | React 19 + TS + Vite. One page that calls `/health` and renders the response. |
| `glci` CLI | `glci/` | Go 1.22+. `glci ping --base <url>` calls `/health` and pretty-prints JSON. |

## Acceptance checklist

Run all four — all four must pass for P1 to be considered green.

### 1. Build the admin UI bundle
```bash
cd git-logs-plugin/admin-ui
npm install
npm run build
# expect: dist/index.js + dist/index.css
```

### 2. Activate the plugin in a WordPress 6.5+ / PHP 8.1+ site
- Symlink or copy `git-logs-plugin/` into `wp-content/plugins/git-logs/`.
- Activate "Git Logs" from the WP admin Plugins screen.
- Expect: no fatal errors, "Git Logs" appears in the admin sidebar.

### 3. Probe the health endpoint
```bash
curl -s https://your-site.test/wp-json/git-logs/v1/health | jq
# expect: { "status": "ok", "plugin": "git-logs", "plugin_version": "0.1.0", ... }
```

### 4. Build and run `glci ping`
```bash
cd glci
go build -o glci .
./glci ping --base https://your-site.test
# expect: same JSON body as step 3, pretty-printed
```

### 5. Load the admin page
- Navigate to `wp-admin/admin.php?page=git-logs`.
- Expect: heading "Git Logs", card "Backend health", dl with status `ok`, plugin version, WP version, PHP version, REST namespace, server time.

## What is intentionally NOT in P1

- Auth (App Password / SSH-key signed requests) → P2
- SQLite schema, repos/branches/runs/sha_index/users/audit tables → P3
- The other 9 REST endpoints (POST /runs, /events, /finalize, etc.) → P4
- Runtime detection, `init` / `run` / `submit` / `status` / `diagram` / `config` commands → P5
- Generic CLI runtime (V→V+5, pinned-installer self-update, Status.ps1/sh) → P6
- Full design system, dashboard, run detail, diagram viewer, audit log → P7
- E2E tests, release pipeline (WP.org SVN, GoReleaser, Homebrew, Scoop), security → P8

## Decisions locked at the start of P1

- **CLI binary name**: `glci`
- **Go module path**: `github.com/example/glci` (placeholder — swap when GitHub handle is provided)
- **Plugin slug**: `git-logs` (REST namespace `git-logs/v1`, text-domain `git-logs`)
- **Plugin minimum**: WordPress 6.5, PHP 8.1
- **CI auth lane (future P2)**: WP App Password (HTTP Basic) for `glci` in CI; SSH-key lane reserved for human/dev use
- **Admin UI stack**: React 19 + TypeScript + Vite, bundled into `admin-ui/dist/`, enqueued by PHP
- **Repo layout**: hybrid — plugin (incl. its admin UI) is one unit under `git-logs-plugin/`; CLI + future runtime under `glci/`

# WP.org Readme + Screenshots (v2)

**Version:** 2.5.0  
**Updated:** 2026-04-25

Specifies the public `readme.txt` (WordPress.org plugin directory format) and the screenshot inventory shipped with the plugin.

---

## readme.txt

Lives at plugin root. Format reference: <https://wordpress.org/plugins/developers/#readme>.

### Required sections + content

```
=== Git Logs ===
Contributors: <wp.org-handles>
Tags: ci, cd, logs, github, gitlab, devops, audit, sqlite
Requires at least: 6.2
Tested up to: 6.5
Requires PHP: 8.1
Stable tag: 2.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Centralized CI/CD log + audit store for WordPress, backed by a single SQLite file. Per-Profile credentials, per-branch acceptance rules, full audit trail.

== Description ==

Git Logs gives every WordPress site an embedded CI/CD telemetry hub. Workflows push log lines via four lightweight REST endpoints; admins review them through a clean WP-admin UI with role-gated screens.

**Why Git Logs?**

* No external service required — one SQLite file in `uploads/`.
* Per-Profile credentials with TempToken + Token, scoped by GitHub URL + branch + Acceptance rule.
* Three-tier audit model (History → Action → AuditTrail) — every change is explainable.
* Role × Permission matrix decoupled from WP roles; Editor and Admin presets out of the box.
* Prometheus-format `/metrics` endpoint for ops.
* WP-CLI commands for backup, restore, prune, verify.

**For CI/CD pipelines**

Four endpoints to wire into your workflow:

* `POST /wp-json/git-logs/v2/append-log` — push a batch of log + error lines.
* `POST /wp-json/git-logs/v2/fixed-log` — flip a Pipeline back to healthy.
* `POST /wp-json/git-logs/v2/clear-log` — truncate one Pipeline.
* `POST /wp-json/git-logs/v2/clear-log-all` — truncate every Pipeline under a RepoVersion.

Reads use WP Application Passwords or your existing JWT/OAuth setup.

== Installation ==

1. Upload the `git-logs/` folder to `/wp-content/plugins/`, OR install via Plugins → Add New.
2. Activate.
3. On first admin pageload, the bootstrap form generates the first Admin Profile.
4. Save the displayed `TempToken` + `Token` securely — they are shown only once.
5. Add a GitProfile pointing at your GitHub org/user and configure Acceptance.
6. Wire your CI/CD workflow to `POST /wp-json/git-logs/v2/append-log` with the credentials.

== Frequently Asked Questions ==

= Does this require a separate database server? =

No. Everything is one SQLite file in `wp-content/uploads/git-logs/`.

= Is it multisite-compatible? =

Yes — each site gets an isolated DB. Network admins see aggregated stats; reads stay site-scoped.

= Can I prune old logs? =

Yes, via `wp git-logs prune --older-than=30d`. There is no automatic prune; operators choose retention.

= How do I back up the data? =

`wp git-logs backup --to=/path/file.sqlite --checkpoint`. Restore with `wp git-logs restore --from=...`.

= Does it support encryption at rest? =

Plain TEXT in v2. AES-256-GCM with HKDF-derived lookup keys is planned for v3.

= How do I integrate with GitHub Actions? =

See the docs page or the `examples/` folder for a ready-to-paste workflow snippet.

== Screenshots ==

1. Profile screen — list of plugin Profiles with status pill and last-active timestamp.
2. First-run bootstrap — one-time credential reveal panel.
3. GitProfile screen — Acceptance rule selector and branch restriction toggle.
4. History timeline — chronological audit feed with severity badges.
5. App detail — polymorphic AppLink picker showing GitProfile + Repo links side by side.
6. AccessToRoles matrix — Permission × Role grid with admin-only checkboxes.
7. Site Health card — three plugin tests with pass/fail icons.
8. Prometheus /metrics endpoint — raw text exposition example.

== Changelog ==

= 2.0.0 =
* Initial public release. Full v2 architecture: SQLite root DB, polymorphic AppLink, three-table audit, 10 REST endpoints, role × permission matrix, Site Health + metrics, WP-CLI suite.

== Upgrade Notice ==

= 2.0.0 =
First public release. No upgrade path from internal pre-releases.
```

---

## Screenshot inventory

WP.org expects PNGs at the plugin root, named `screenshot-N.png`. Captions come from the `== Screenshots ==` section in order.

| # | File | Min size | Caption (must match readme.txt) |
|---|------|----------|----------------------------------|
| 1 | `screenshot-1.png` | 1280×800 | Profile screen — list of plugin Profiles with status pill and last-active timestamp. |
| 2 | `screenshot-2.png` | 1280×800 | First-run bootstrap — one-time credential reveal panel. |
| 3 | `screenshot-3.png` | 1280×800 | GitProfile screen — Acceptance rule selector and branch restriction toggle. |
| 4 | `screenshot-4.png` | 1280×800 | History timeline — chronological audit feed with severity badges. |
| 5 | `screenshot-5.png` | 1280×800 | App detail — polymorphic AppLink picker showing GitProfile + Repo links side by side. |
| 6 | `screenshot-6.png` | 1280×800 | AccessToRoles matrix — Permission × Role grid with admin-only checkboxes. |
| 7 | `screenshot-7.png` | 1280×800 | Site Health card — three plugin tests with pass/fail icons. |
| 8 | `screenshot-8.png` | 1280×800 | Prometheus /metrics endpoint — raw text exposition example. |

### Style rules

- 2× DPI export so retina viewers stay crisp.
- WP admin chrome (sidebar + top bar) always included for context — never crop to the panel only.
- Use a clean WP install with the default Twenty Twenty-Four theme; no third-party admin themes.
- Sample data: at least 3 Profiles, 2 GitProfiles, 4 Apps, 6 Pipelines spanning 2 RepoVersions, 50+ LogEntries with mixed severities. Anonymize emails (`alice@example.com`, etc.).
- Annotations (red arrows / callouts) only on screenshots 2 and 6 where UX is non-obvious; everything else is plain.

---

## Banner + icon

WP.org supports plugin banners (1544×500 + 772×250) and icons (256×256 + 128×128). Stored in `assets/` of the SVN repo (NOT plugin root).

| File | Purpose |
|------|---------|
| `assets/banner-1544x500.png` | Hero banner on plugin page |
| `assets/banner-772x250.png` | Mobile banner |
| `assets/icon-256x256.png` | High-res icon |
| `assets/icon-128x128.png` | Standard icon |
| `assets/icon.svg` | Optional vector source |

Brand: monospaced `git-logs` wordmark on dark slate, with a subtle terminal-prompt glyph. Avoid generic GitHub octocat or WordPress logo to prevent trademark issues.

---

## Build pipeline

The release ZIP must include readme.txt + screenshot-*.png; the SVN `assets/` folder is separate.

```
make release
  → build/git-logs/
      git-logs.php
      readme.txt
      screenshot-1.png … screenshot-8.png
      languages/git-logs.pot
      inc/...
  → git-logs-2.0.0.zip
```

CI gate: `wp plugin check` (WordPress.org plugin checker) must pass before tagging.

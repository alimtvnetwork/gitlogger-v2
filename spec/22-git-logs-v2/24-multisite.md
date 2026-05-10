# Multisite Behavior (v2)

**Version:** 2.5.0  
**Updated:** 2026-04-25

How the plugin behaves on a WordPress Multisite (network) install.

---

## Default mode: per-site

When activated **per-site** (not network-activated), each site gets its own isolated DB:

```
wp-content/uploads/sites/<blogId>/git-logs/git-logs.sqlite
```

Single-site installs keep `wp-content/uploads/git-logs/git-logs.sqlite` (no `sites/<blogId>` prefix). The path resolver uses `wp_upload_dir()['basedir']` which already incorporates the multisite prefix.

Properties:

- Profiles, GitProfiles, Apps, Pipelines, Logs are all site-local.
- Network admins see nothing aggregated — they must visit each site.
- Activation/deactivation/uninstall hooks run per-site.
- Migrations run when each site's admin first loads the plugin page after upgrade.

This is the **recommended** mode for tenant isolation.

---

## Network-activated mode

When network-activated via `wp plugin activate git-logs --network`:

- Per-site DB layout is **unchanged** — still one SQLite file per site.
- A network admin screen appears at **Network Admin → Git Logs → Sites**, listing every site with: DB size, Profile count, Pipeline count, last push.
- Network admins do not get cross-site read endpoints. Each site's `/wp-json/git-logs/v2/get-logs` is still scoped to that site's DB.
- Plugin updates trigger migrations on every site lazily (first admin pageload per site), never in a single network-wide transaction.

Rationale: SQLite does not support cross-database joins safely under WP Multisite plugin lifecycles. Per-site files keep activation/deactivation atomic.

---

## What is NOT supported

| Feature | Status | Why |
|---------|--------|-----|
| Single shared DB across all sites | ❌ | Tenant bleed risk; SQLite locking would serialize all sites. |
| Cross-site log queries from one endpoint | ❌ | Would require a new aggregation layer; out of v2 scope. |
| Network-level Profiles | ❌ | Profile = credential boundary; must stay site-scoped. |
| Per-site override of `ConfigKv` from network admin | ❌ | Each site owns its config. |

---

## Subdomain vs subdirectory installs

No behavioral difference. The plugin only cares about `get_current_blog_id()` and `wp_upload_dir()`.

---

## Uninstall semantics

Uninstall via `register_uninstall_hook` only runs for the site being uninstalled. To wipe the network's DBs in one shot, an operator must run:

```
wp site list --field=url | xargs -I{} wp --url={} plugin uninstall git-logs --deactivate
```

The plugin **never** deletes other sites' files during a per-site uninstall.

---

## CLI scoping

All `wp git-logs *` commands accept the standard `--url=<site>` flag. Without it, WP-CLI uses the main site (blog 1).

```
wp --url=https://tenant-a.example.com git-logs prune --older-than=30d
```

---

## Site Health (§20) under multisite

Each site's Site Health page shows that site's plugin tests. Network Admin Site Health shows aggregated pass/fail counts only — no per-site detail (WP core limitation).

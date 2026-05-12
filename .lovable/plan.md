# "Visit plugin site" — Landing Page Plan

When a WordPress admin clicks **Visit plugin site** on the Plugins screen, they should land on a marketing/info page that explains what Git Logs is, what it does, how to install it, and where to get help. Today it points to `https://example.com/git-logs` (a placeholder), which is why nothing useful loads.

The landing page will live at the root of this Lovable project (`/`) and the three plugin headers (`Plugin URI` in `git-logs.php`, plus `readme.txt` and `git-logs-plugin/README.md`) will be updated to point to the published URL.

---

## What the page must communicate

1. **What Git Logs is** — a self-hosted, WordPress-based CI/CD dashboard
2. **Who it's for** — dev teams running builds across multiple repos
3. **How it works** — `glci` CLI → signed REST → WP plugin → React admin
4. **What you see** — Dashboard, Run detail (live stream), Repos, Diagrams, Audit log
5. **Why choose it** — self-hosted, Ed25519 signed, multi-repo, uses existing WP users
6. **How to install** — WP plugin ZIP + `glci` install + minimal CI snippet
7. **Requirements** — WP 6.5+, PHP 8.1+, `pdo_sqlite`, `sodium`
8. **Where to get help** — GitHub repo, issues, docs

---

## Phased build


| #   | Phase                        | Deliverable                                                                                                                                                                               |
| --- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Hero + value proposition** | Headline, sub-headline, primary/secondary CTAs (Download / View on GitHub), version badge, hero screenshot of the WP admin Dashboard                                                      |
| 2   | **Feature grid**             | 4–6 cards: Multi-repo dashboard, Live log streaming, Ed25519 signed ingestion, Self-hosted, Uses WP users/roles, Audit log                                                                |
| 3   | **How it works**             | 3-step flow diagram (`glci` → signed REST → WP plugin) + concrete "push commit → see it live" example                                                                                     |
| 4   | **Screenshots gallery**      | Dashboard, Run detail (live stream), Repos list, Diagrams viewer, Audit log                                                                                                               |
| 5   | **Quick-start / install**    | Tabbed code blocks: WP plugin (ZIP upload), `glci` install (brew / go install / binary), CI snippet (GitHub Actions YAML)                                                                 |
| 6   | **Requirements + FAQ**       | Requirements table + accordion FAQ (Why WordPress? Is it secure? Does it work with GitLab? Can I self-host the CLI? etc.)                                                                 |
| 7   | **Footer + SEO polish**      | Footer with links (GitHub, Issues, Docs, License), `<head>` SEO tags, JSON-LD `SoftwareApplication`, then patch `Plugin URI` in `git-logs.php`, `readme.txt`, `git-logs-plugin/README.md` |
| 8   | **Polish + responsive QA**   | Mobile/tablet/desktop QA, dark-mode pass, animations, accessibility checks                                                                                                                |


---

## Technical notes

- **Stack:** TanStack Start (already set up). Single landing page in `src/routes/index.tsx`, broken into section components under `src/components/landing/`.
- **Design tokens:** All colors/typography via `src/styles.css` semantic tokens (no hard-coded colors in components).
- **Hero & screenshot assets:** Generated via `imagegen` and stored in `src/assets/`.
- **No backend needed** — fully static marketing page.
- **Final wiring (Phase 7):** Update `Plugin URI: https://example.com/git-logs` to the published Lovable URL (or custom domain if you provide one) in all three plugin files.

---

## One open question before Phase 1

What URL should the "Visit plugin site" link point to?

1. **Lovable preview/published URL** (e.g. `15bba2cc-….lovable.app`) for now — easy to swap to a custom domain later
2. **Custom domain** you already own (e.g. `gitlogs.dev`) — bake it in now
3. **GitHub repo URL** — skip the landing page, just patch the three plugin files

Say `next` to start Phase 1 (and tell me which URL option you want, otherwise I'll default to option 1).
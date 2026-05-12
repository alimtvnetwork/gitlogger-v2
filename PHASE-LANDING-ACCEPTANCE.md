# Landing Page — Acceptance (Phases 1–8)

Date: 2026-05-12
Route: `/` (src/routes/index.tsx)

## Sections shipped
1. Hero — headline, sub, dual CTAs, status badges, faux WP-Admin run-detail visual
2. Features — 6-card grid (live streaming, multi-repo, Ed25519, audit log, WP auth, self-hosted)
3. How it works — 3-step flow + copy-pasteable `.github/workflows/ci.yml`
4. Screenshots — tabbed gallery: Dashboard, Run detail, Repos, Diagrams, Audit log
5. Install — 3-tab quick-start (WP plugin ZIP, glci CLI, CI workflow with `GLCI_TOKEN`)
6. Requirements + FAQ — 6 reqs, 8 FAQs incl. trust trio (streaming mechanics, WP-down resilience, who-can-see)
7. Footer + SEO — 3-column footer, JSON-LD `SoftwareApplication`, canonical, OG/Twitter meta; `Plugin URI` in `git-logs-plugin/git-logs.php` updated to `https://github.com/git-logs/wp-plugin`
8. Polish — `scroll-smooth` on `<html>`; QA at 375px and 1366px

## QA notes
- Mobile (375×812): hero stacks correctly, badges wrap on 2 rows, no horizontal overflow
- Desktop (1366×864): hero centered, header nav visible, hero preview readable
- Code blocks use `overflow-x-auto` so long YAML lines scroll within the block
- All anchor links (`#features`, `#how`, `#install`, `#faq`) resolve to in-page sections

## Open follow-ups (not blocking)
- `SITE_URL` constant placeholder = `https://gitlogs.dev` — swap when real domain is chosen
- Replace mocked screenshots with real WP-Admin captures once plugin is deployed somewhere public
- Add `og:image` once a hero image exists (currently omitted — better than generic)

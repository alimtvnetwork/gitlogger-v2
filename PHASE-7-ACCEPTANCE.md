# Phase 7 — Acceptance Notes

> Status: **DONE** (2026-05-11). Closes the Admin UI full surface
> commitment from spec/24 (design system + UI conventions) and provides
> the in-WordPress consumer for the Phase-4 REST endpoints + the
> spec/26 diagram catalog.

## Scope

Phase 7 turns the Phase-1 walking-skeleton admin page into a real
three-view single-page app: **Dashboard**, **Run detail** (with live
event polling + filtering), and **Diagram viewer** (lists shipped
spec/26 SVGs). All UI uses semantic design tokens scoped under
`.gl-admin` so styles never leak into the WP admin chrome.

## Components Shipped

| File | Purpose |
|------|---------|
| `git-logs-plugin/admin-ui/src/App.tsx` | Hash-based router (`#/`, `#/runs/:id`, `#/diagrams`); header + nav; mounts the three views; surfaces a typed "boot data missing" fallback when `GitLogsBoot` is absent. |
| `git-logs-plugin/admin-ui/src/api/client.ts` | `useApi(boot)` — minimal fetch wrapper that injects `X-WP-Nonce`, parses JSON safely, throws a typed `ApiError` exposing the server's `code` (`ErrorCode`) verbatim per spec/22 R3 contract. |
| `src/views/Dashboard.tsx` | Two cards: **Recent runs** table (status/pipeline/branch/SHA-7/started/errors + open link) and **Repositories** list. Skeleton-loader placeholders, empty states. |
| `src/views/RunDetail.tsx` | Run summary card + **Event stream** card. Polls `/runs/:id/events?since=N` every 2 s when "Live follow" is on; cursor stored in a ref so re-renders don't reset position. Tabs filter `all` \| `warn` \| `error`. |
| `src/views/DiagramViewer.tsx` | Two-pane layout: list of shipped diagrams + `<object type="image/svg+xml">` stage with a "view source" link to the `.mmd`. |
| `src/components/StatusBadge.tsx` | Tone-mapped pill: `passed+!hasError` → ok, `failed/errored/hasError` → err, `running` → info, else muted. |
| `src/components/ErrorBanner.tsx` | `role="alert"` red banner. |
| `src/components/TimeAgo.tsx` | Relative time with absolute ISO in `title`. Resilient to null / invalid dates. |
| `src/styles.css` | Design tokens in `oklch` per spec/24 (Surface, Border, Primary/OK/Warn/Err/Info, radii, shadow, mono stack). All colors via tokens — no hard-coded hex. Includes responsive breakpoint at 720 px and event-stream monospace block with sticky header semantics. |
| `git-logs-plugin/includes/rest/class-rest-admin-diagrams.php` | `GET /git-logs/v1/admin/diagrams` — admin-only, scans `spec/26-gitlogs-diagrams/*.svg`, pairs with sibling `.mmd` source when present; returns `{ items: [{ slug, title, href, source? }] }`; humanises slugs by stripping leading numeric prefix. |
| `git-logs-plugin/git-logs.php` | Wires `Rest\Admin_Diagrams::register` into `rest_api_init`. |

## Acceptance Checklist

- [x] `bun run build` (in `git-logs-plugin/admin-ui/`) compiles clean
      with **34 modules** → `dist/index.css 6.13 kB` + `dist/index.js
      203.97 kB`. Zero TS errors.
- [x] Hash-based routing: `#/` → Dashboard, `#/runs/<id>` → Run detail,
      `#/diagrams` → Diagram viewer. No external router dependency.
- [x] Every fetch carries `X-WP-Nonce`; failed responses surface the
      server's `ErrorCode` verbatim (R3 contract mirror).
- [x] Live follow on Run detail uses a `since` cursor; toggling off the
      checkbox cancels the poll loop and aborts pending timeouts.
- [x] Event filter is purely client-side (no extra round trips).
- [x] Skeleton loaders prevent layout shift while fetches are in flight.
- [x] All colors use tokens (`--gl-primary`, `--gl-err`, etc.) defined
      in `oklch` under the `.gl-admin` scope. No raw hex values in
      components.
- [x] `<object type="image/svg+xml">` keeps SVG accessibility (a11y tree
      preserved) and the `aria-label` carries the diagram title.
- [x] Diagram REST endpoint requires `manage_options` and returns an
      empty `items[]` (not 500) when `spec/26-gitlogs-diagrams/` is
      missing.
- [x] Mobile breakpoint at 720 px collapses the diagram split into a
      single column and reflows the event grid.

## Out of Scope (deferred)

- Server-Sent Events / WebSocket push for the event stream (currently
  2 s polling). Tracked alongside streaming-mode shipping in P8.
- Repo / run mutation UI (create repo, finalize run manually,
  GC controls). All Phase-4 mutation endpoints exist; only read views
  are wired in P7.
- Inline Mermaid render fallback when only `.mmd` is shipped (current
  viewer requires the pre-built `.svg`).
- Theme switcher / dark mode. Tokens are dark-mode-ready (oklch
  lightness pivot) but no toggle is wired.
- Audit-log viewer. Endpoint exists since P4; UI lands in a follow-up.

## Remaining Tasks (project-level)

| Phase | Title | Status |
|-------|-------|--------|
| ~~P1~~ | Walking skeleton | done |
| ~~P2~~ | Dual auth lanes | done |
| ~~P3~~ | SQLite schema + repository layer | done |
| ~~P4~~ | Public REST surface + OpenAPI | done |
| ~~P5~~ | glci command surface + runtime detection + CI bindings | done |
| ~~P6~~ | Shipping client + self-test harness + doctor reach | done |
| ~~P7~~ | Admin UI full surface (Dashboard, Run detail, Diagram viewer) | **done** |
| **P8** | **Streaming + Lane B SSH + self-update + E2E + GoReleaser/SVN release pipeline** | **next (final phase)** |

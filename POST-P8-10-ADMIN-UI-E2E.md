# Post-P8 #10 — Admin UI E2E (Playwright)

**Status:** ✅ scaffolded; runs in CI (sandbox lacks browser deps for local exec)

## Scope
End-to-end coverage of the React admin UI (`git-logs-plugin/admin-ui/`) —
Dashboard, RunDetail, boot validation, and StatusBadge tone mapping —
without requiring a real WordPress install.

## Approach
- `e2e/fixtures/admin.html` — static harness mirroring the markup that
  `class-admin-page.php` injects into wp-admin (`#git-logs-admin-root`,
  boot blob, module entry). Loads `/src/main.tsx` via Vite dev so HMR
  transforms fire normally.
- A pre-bundle `<script>` installs a `window.fetch` interceptor that
  reads canned responses from `window.__GL_FIXTURES__` (preloaded per
  spec via `page.addInitScript`). Anything unmocked returns 404 with a
  recognisable JSON envelope so missing fixtures surface clearly. A
  `__GL_PASSTHROUGH__` escape hatch hands control back to Playwright's
  own `page.route()` for tests that need server-side stubs.
- `playwright.config.ts` boots Vite (`vite --port 5733 --strictPort`)
  via `webServer`, single Chromium project, `retain-on-failure` traces.

## Specs (9 tests across 3 files)
- `e2e/dashboard.spec.ts`
  - renders header, recent runs table, status badges (`ok`/`err`/`info`),
    "Open →" links, and the repos list
  - empty-state copy when both endpoints return `{ items: [] }`
  - graceful fallback when every endpoint 404s (Dashboard's `.catch()` →
    same empty state)
  - hash navigation toggles `is-active` and switches to the diagrams view
- `e2e/run-detail.spec.ts`
  - summary card + dl + 3-row event stream; level filter narrows to the
    error row and back
  - unchecking "Live follow" stops further `/runs/:id/events` polls
    (asserted by counting `page.route` hits)
  - 500 from `/runs/:id` surfaces in the `.gl-banner-err` banner
- `e2e/boot.spec.ts`
  - "Boot data missing" card when `window.GitLogsBoot` is undefined
  - StatusBadge tone matrix: passed→ok, failed/errored→err, running→info,
    queued→muted

## Verification
- `bun x tsc --noEmit` — clean (specs + fixtures fully typed)
- `bun run build` — production bundle still builds (203.97 kB / 6.13 kB CSS)
- Local Playwright run BLOCKED in this sandbox: chrome-headless-shell needs
  `libglib-2.0.so.0` + the usual nss/atk/cairo/pango/dbus/libxkbcommon
  family. `nix-shell` can fetch them but `LD_LIBRARY_PATH` plumbing into
  Playwright's spawned subprocess wasn't reliable. Resolved by running
  the suite inside `mcr.microsoft.com/playwright:v1.59.1-jammy` in CI
  (every browser dep preinstalled).

## CI
`.github/workflows/ci-admin-ui.yml`
- triggers on changes under `git-logs-plugin/admin-ui/**`
- runs in the official Playwright container
- steps: `bun install --frozen-lockfile` → `tsc --noEmit` → `bun run build`
  → `bun x playwright test`
- uploads `playwright-report/` artifact on failure (7-day retention)

## Files changed
- new: `git-logs-plugin/admin-ui/e2e/fixtures/admin.html`
- new: `git-logs-plugin/admin-ui/e2e/fixtures/mocks.ts`
- new: `git-logs-plugin/admin-ui/e2e/dashboard.spec.ts`
- new: `git-logs-plugin/admin-ui/e2e/run-detail.spec.ts`
- new: `git-logs-plugin/admin-ui/e2e/boot.spec.ts`
- new: `git-logs-plugin/admin-ui/playwright.config.ts`
- new: `.github/workflows/ci-admin-ui.yml`
- edited: `git-logs-plugin/admin-ui/package.json` (added `@playwright/test`
  devDep + `test:e2e` script)

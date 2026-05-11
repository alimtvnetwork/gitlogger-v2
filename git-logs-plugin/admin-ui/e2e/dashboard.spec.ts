import { test, expect } from "@playwright/test";
import { setupAdmin, defaultFixtures, baseRuns, baseRepos } from "./fixtures/mocks";

test.describe("Dashboard", () => {
  test("renders header, recent runs, and repositories from API", async ({ page }) => {
    await setupAdmin(page, defaultFixtures);

    await expect(page.getByRole("heading", { name: "Git Logs" })).toBeVisible();
    await expect(page.locator(".gl-tag")).toHaveText("v0.1.0-e2e");

    // Runs table renders one row per fixture run.
    const runRows = page.locator(".gl-table tbody tr");
    await expect(runRows).toHaveCount(baseRuns.items.length);

    // Status badges: 'passed' (ok), 'failed' (err), 'running' (info)
    await expect(page.locator(".gl-badge-ok")).toHaveText("passed");
    await expect(page.locator(".gl-badge-err")).toContainText("failed");
    await expect(page.locator(".gl-badge-info")).toHaveText("running");

    // Each row exposes a link to its run detail view.
    await expect(page.getByRole("link", { name: /Open/ })).toHaveCount(baseRuns.items.length);

    // Repos list renders one li per fixture repo.
    const repoRows = page.locator(".gl-list-row");
    await expect(repoRows).toHaveCount(baseRepos.items.length);
    await expect(repoRows.first()).toContainText("git@github.com:acme/api.git");
  });

  test("shows empty state when API returns no runs and no repos", async ({ page }) => {
    await setupAdmin(page, {
      "/repos?limit=50": { items: [] },
      "/runs?limit=25":  { items: [] },
    });
    await expect(page.locator(".gl-empty")).toHaveCount(2);
    await expect(page.locator(".gl-empty").first()).toContainText("No runs yet");
  });

  test("falls back to skeleton then empty when API errors out", async ({ page }) => {
    // No fixtures registered → harness returns 404 for every call. The
    // Dashboard's catch() turns each failure into an empty list.
    await setupAdmin(page, {});
    await expect(page.locator(".gl-empty").first()).toContainText("No runs yet");
  });

  test("hash navigation switches to the diagrams view", async ({ page }) => {
    await setupAdmin(page, {
      ...defaultFixtures,
      "/diagrams": { items: [] },
    });
    await page.getByRole("link", { name: "Diagrams" }).click();
    await expect(page).toHaveURL(/#\/diagrams$/);
    // Active nav state mirrors the route.
    await expect(page.locator("a.is-active")).toHaveText("Diagrams");
  });
});

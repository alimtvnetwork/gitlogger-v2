import { test, expect } from "@playwright/test";
import { setupAdmin, baseRuns, passedRunDetail, passedRunEvents } from "./fixtures/mocks";

const RUN = baseRuns.items[0];

test.describe("RunDetail", () => {
  test("renders run summary, all events, and supports level filter", async ({ page }) => {
    await setupAdmin(page, {
      "/repos?limit=50": { items: [] },
      "/runs?limit=25":  baseRuns,
      [`/runs/${encodeURIComponent(RUN.id)}`]: passedRunDetail,
      [`/runs/${encodeURIComponent(RUN.id)}/events?since=0&limit=500`]: passedRunEvents,
      // suppress polling
      [`/runs/${encodeURIComponent(RUN.id)}/events`]: { items: [] },
    });

    await page.goto(`/e2e/fixtures/admin.html#/runs/${encodeURIComponent(RUN.id)}`);

    // Summary card
    await expect(page.getByRole("heading", { level: 2 }).first()).toContainText(RUN.id.slice(0, 8));
    await expect(page.locator(".gl-card-head .gl-badge-ok")).toHaveText("passed");
    await expect(page.locator(".gl-dl")).toContainText(["Started", "Ended", "Errors", "Warnings"]);

    // Event stream — all 3 fixture events visible.
    const events = page.locator(".gl-events .gl-event");
    await expect(events).toHaveCount(passedRunEvents.items.length);
    await expect(events.nth(0)).toHaveClass(/gl-event-info/);
    await expect(events.nth(1)).toHaveClass(/gl-event-warn/);
    await expect(events.nth(2)).toHaveClass(/gl-event-error/);

    // Filter to "error" → only the error row remains.
    await page.getByRole("tab", { name: "error" }).click();
    await expect(events).toHaveCount(1);
    await expect(events.first()).toContainText("TypeError in module foo");
    await expect(events.first()).toContainText("src/foo.ts");

    // Switch back to "all".
    await page.getByRole("tab", { name: "all" }).click();
    await expect(events).toHaveCount(3);
  });

  test("toggling Live follow off stops further polling", async ({ page }) => {
    let pollCount = 0;
    await page.addInitScript(() => {
      (window as any).__GL_FIXTURES__ = {};
    });
    await page.route("**/api/git-logs/v1/**", async (route) => {
      const url = new URL(route.request().url());
      const path = url.pathname.replace(/^\/api\/git-logs\/v1/, "") + url.search;
      let body: unknown = { items: [] };
      if (path === `/runs/${encodeURIComponent(RUN.id)}`) body = passedRunDetail;
      else if (path === `/runs/${encodeURIComponent(RUN.id)}/events?since=0&limit=500`) {
        pollCount++;
        body = passedRunEvents;
      } else if (path.startsWith(`/runs/${encodeURIComponent(RUN.id)}/events`)) {
        pollCount++;
      }
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(body) });
    });
    await page.addInitScript(() => { (window as any).__GL_PASSTHROUGH__ = true; });
    await page.goto(`/e2e/fixtures/admin.html#/runs/${encodeURIComponent(RUN.id)}`);

    await expect(page.locator(".gl-events .gl-event")).toHaveCount(3);

    await page.getByLabel("Live follow").uncheck();
    const before = pollCount;
    await page.waitForTimeout(2500);
    expect(pollCount - before).toBeLessThanOrEqual(1);
  });

  test("surfaces an error banner when the run detail API fails", async ({ page }) => {
    await page.route("**/api/git-logs/v1/runs/**", (route) => {
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ code: "internal_error", message: "boom" }),
      });
    });
    await page.addInitScript(() => { (window as any).__GL_PASSTHROUGH__ = true; });
    await page.goto(`/e2e/fixtures/admin.html#/runs/${encodeURIComponent(RUN.id)}`);
    await expect(page.locator(".gl-banner-err")).toContainText("boom");
  });
});

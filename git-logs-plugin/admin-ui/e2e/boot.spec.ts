import { test, expect } from "@playwright/test";

test.describe("Boot validation", () => {
  test("renders 'Boot data missing' when GitLogsBoot is absent", async ({ page }) => {
    await page.addInitScript(() => {
      // Override the boot blob to undefined BEFORE the bundle module runs.
      Object.defineProperty(window, "GitLogsBoot", { value: undefined, configurable: true });
    });
    await page.goto("/e2e/fixtures/admin.html");
    await expect(page.locator(".gl-err-card")).toContainText("Boot data missing");
  });

  test("StatusBadge tones map correctly across statuses", async ({ page }) => {
    const items = [
      { id: "a".repeat(36), repo_id: 1, branch: "main", pipeline_name: "p", git_sha: "0".repeat(40), status: "passed",  has_error: 0, started_at: new Date().toISOString() },
      { id: "b".repeat(36), repo_id: 1, branch: "main", pipeline_name: "p", git_sha: "1".repeat(40), status: "failed",  has_error: 1, started_at: new Date().toISOString() },
      { id: "c".repeat(36), repo_id: 1, branch: "main", pipeline_name: "p", git_sha: "2".repeat(40), status: "errored", has_error: 1, started_at: new Date().toISOString() },
      { id: "d".repeat(36), repo_id: 1, branch: "main", pipeline_name: "p", git_sha: "3".repeat(40), status: "running", has_error: 0, started_at: new Date().toISOString() },
      { id: "e".repeat(36), repo_id: 1, branch: "main", pipeline_name: "p", git_sha: "4".repeat(40), status: "queued",  has_error: 0, started_at: new Date().toISOString() },
    ];
    await page.addInitScript((runs) => {
      (window as any).__GL_FIXTURES__ = {
        "/repos?limit=50": { items: [] },
        "/runs?limit=25":  { items: runs },
      };
    }, items);
    await page.goto("/e2e/fixtures/admin.html");

    await expect(page.locator(".gl-badge-ok")).toHaveCount(1);
    await expect(page.locator(".gl-badge-err")).toHaveCount(2); // failed + errored
    await expect(page.locator(".gl-badge-info")).toHaveCount(1); // running
    await expect(page.locator(".gl-badge-muted")).toHaveCount(1); // queued
  });
});

/**
 * Canned API responses shared across specs. Each spec is free to override
 * a subset by passing its own fixture object to setupAdmin().
 */

import type { Page } from "@playwright/test";

export const baseRepos = {
  items: [
    { id: 1, url: "git@github.com:acme/api.git",  created_at: "2025-04-01T10:00:00Z", last_run_at: "2025-05-10T09:00:00Z" },
    { id: 2, url: "git@github.com:acme/site.git", created_at: "2025-03-15T10:00:00Z", last_run_at: null },
  ],
};

export const baseRuns = {
  items: [
    {
      id: "11111111-1111-4111-8111-111111111111",
      repo_id: 1, branch: "main", pipeline_name: "build-and-test",
      git_sha: "abcdef0123456789abcdef0123456789abcdef01",
      status: "passed", has_error: 0, error_count: 0, warn_count: 2,
      started_at: new Date(Date.now() - 6 * 60_000).toISOString(),
      ended_at:   new Date(Date.now() - 5 * 60_000).toISOString(),
    },
    {
      id: "22222222-2222-4222-8222-222222222222",
      repo_id: 1, branch: "feature/x", pipeline_name: "lint",
      git_sha: "fedcba9876543210fedcba9876543210fedcba98",
      status: "failed", has_error: 1, error_count: 4, warn_count: 1,
      started_at: new Date(Date.now() - 30 * 60_000).toISOString(),
      ended_at:   new Date(Date.now() - 29 * 60_000).toISOString(),
    },
    {
      id: "33333333-3333-4333-8333-333333333333",
      repo_id: 2, branch: "main", pipeline_name: "deploy",
      git_sha: "1111111111111111111111111111111111111111",
      status: "running", has_error: 0, error_count: 0, warn_count: 0,
      started_at: new Date(Date.now() - 15_000).toISOString(),
      ended_at: null,
    },
  ],
};

export const passedRunDetail = {
  item: baseRuns.items[0],
};

export const passedRunEvents = {
  items: [
    { id: 1, ts: "2025-05-10T09:00:00.123Z", level: "info",  line: "starting build" },
    { id: 2, ts: "2025-05-10T09:00:01.456Z", level: "warn",  line: "deprecated flag --legacy" },
    { id: 3, ts: "2025-05-10T09:00:02.789Z", level: "error", line: "TypeError in module foo", file_path: "src/foo.ts" },
  ],
};

/**
 * Install fixtures + mocked window.fetch and navigate to the admin page.
 */
export async function setupAdmin(page: Page, fixtures: Record<string, unknown>) {
  await page.addInitScript((f) => { (window as any).__GL_FIXTURES__ = f; }, fixtures);
  await page.goto("/e2e/fixtures/admin.html");
}

export const defaultFixtures = {
  "/repos?limit=50": baseRepos,
  "/runs?limit=25":  baseRuns,
  [`/runs/${encodeURIComponent(baseRuns.items[0].id)}`]: passedRunDetail,
  [`/runs/${encodeURIComponent(baseRuns.items[0].id)}/events?since=0&limit=500`]: passedRunEvents,
  // Subsequent polling calls (since=last id) return empty so the test loop
  // does not accumulate forever.
  [`/runs/${encodeURIComponent(baseRuns.items[0].id)}/events`]: { items: [] },
};

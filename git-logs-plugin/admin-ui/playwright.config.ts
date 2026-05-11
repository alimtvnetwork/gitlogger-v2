import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright spawns Vite in preview mode rooted at the admin-ui package so
 * that /dist/* and /e2e/fixtures/* resolve from the same origin.
 */
export default defineConfig({
  testDir: "./e2e",
  testMatch: /.*\.spec\.ts/,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "list" : [ ["list"] ],
  use: {
    baseURL: "http://127.0.0.1:5733",
    actionTimeout: 5000,
    navigationTimeout: 10_000,
    trace: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: {
    command: "bun x vite --port 5733 --strictPort",
    url: "http://127.0.0.1:5733/e2e/fixtures/admin.html",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
    stdout: "pipe",
    stderr: "pipe",
  },
});

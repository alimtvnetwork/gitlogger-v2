/**
 * Project-wide site config for the Git Logs landing page.
 * Update these in one place when the real repo / domain are ready.
 */
export const SITE_URL = "https://15bba2cc-3c74-4134-aa1e-6340608435e8.lovable.app";

// GitHub org/repo for the WP plugin
export const GITHUB_ORG = "git-logs";
export const GITHUB_REPO = "git-logs";
export const GITHUB_BASE = `https://github.com/${GITHUB_ORG}/${GITHUB_REPO}`;

export const LINKS = {
  github: GITHUB_BASE,
  issues: `${GITHUB_BASE}/issues`,
  releases: `${GITHUB_BASE}/releases`,
  pluginZip: `${GITHUB_BASE}/releases/latest/download/git-logs.zip`,
  glciRepo: "https://github.com/git-logs/glci",
  glciTap: "git-logs/tap/glci",
  glciGo: "github.com/git-logs/glci@latest",
  glciTarball:
    "https://github.com/git-logs/glci/releases/latest/download/glci_linux_amd64.tar.gz",
  setupGlciAction: "git-logs/setup-glci@v1",
} as const;

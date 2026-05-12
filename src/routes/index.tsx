import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Git Logs — Self-hosted CI/CD dashboard for WordPress" },
      {
        name: "description",
        content:
          "Stream every CI build, test, and deploy from your repos into a private WordPress dashboard. Live logs, audit trail, Ed25519-signed, self-hosted.",
      },
      { property: "og:title", content: "Git Logs — Self-hosted CI/CD dashboard for WordPress" },
      {
        property: "og:description",
        content:
          "Push a commit, watch it run live in WP Admin. Multi-repo dashboard with full audit log. Self-hosted, Ed25519-signed.",
      },
      { property: "og:type", content: "website" },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <Hero />
      <Features />
      <HowItWorks />
      <Screenshots />
      <Install />
    </div>
  );
}

function Install() {
  const tabs = [
    { id: "wp", label: "1. WordPress plugin" },
    { id: "cli", label: "2. glci CLI" },
    { id: "ci", label: "3. Wire up CI" },
  ] as const;
  type T = (typeof tabs)[number]["id"];
  const [tab, setTab] = useState<T>("wp");

  return (
    <section id="install" className="border-t border-border bg-muted/30">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">Install in 2 minutes</h2>
          <p className="mt-4 text-pretty text-muted-foreground md:text-lg">
            Three steps. Each one stands alone — finish it, verify, move on.
          </p>
        </div>

        <div className="mx-auto mt-10 max-w-3xl">
          <div className="flex flex-wrap items-center justify-center gap-2">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`inline-flex h-9 items-center justify-center rounded-full border px-4 text-sm transition-colors ${
                  tab === t.id
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border bg-card text-muted-foreground hover:text-foreground"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          <div className="mt-8">
            {tab === "wp" && <InstallWP />}
            {tab === "cli" && <InstallCli />}
            {tab === "ci" && <InstallCi />}
          </div>
        </div>
      </div>
    </section>
  );
}

function InstallWP() {
  return (
    <div className="space-y-4">
      <Step n={1} title="Download the plugin ZIP">
        <CodeBlock>{`curl -LO https://github.com/git-logs/wp-plugin/releases/latest/download/git-logs.zip`}</CodeBlock>
      </Step>
      <Step n={2} title="Upload via WP-Admin">
        Go to <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">Plugins › Add New › Upload</code>,
        pick the ZIP, click Install Now, then Activate.
      </Step>
      <Step n={3} title="Generate an Ed25519 keypair">
        Open <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">Settings › Git Logs › Keys</code>{" "}
        and click <strong>Generate</strong>. Copy the private key — you'll paste it into your CI secrets next.
      </Step>
    </div>
  );
}

function InstallCli() {
  return (
    <div className="space-y-4">
      <Step n={1} title="Install glci">
        <div className="space-y-2">
          <div className="text-xs text-muted-foreground">macOS / Linux (Homebrew):</div>
          <CodeBlock>{`brew install git-logs/tap/glci`}</CodeBlock>
          <div className="pt-2 text-xs text-muted-foreground">Or with Go ≥ 1.22:</div>
          <CodeBlock>{`go install github.com/git-logs/glci@latest`}</CodeBlock>
          <div className="pt-2 text-xs text-muted-foreground">Or download a binary from GitHub Releases.</div>
        </div>
      </Step>
      <Step n={2} title="Verify it runs">
        <CodeBlock>{`glci version
glci doctor`}</CodeBlock>
      </Step>
      <Step n={3} title="Smoke-test against your site">
        <CodeBlock>{`glci ping --server-url=https://yoursite.com/wp-json/git-logs/v1
# expects: { "ok": true, "version": "0.4.0" }`}</CodeBlock>
      </Step>
    </div>
  );
}

function InstallCi() {
  const yaml = `# .github/workflows/ci.yml
name: ci
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci

      # Install glci once per job
      - uses: git-logs/setup-glci@v1
        with: { version: latest }

      # Stream lint + test + build to your WordPress dashboard
      - run: glci run --stream \\
          --server-url=https://yoursite.com/wp-json/git-logs/v1 \\
          -- npm test
        env:
          GLCI_TOKEN: \${{ secrets.GLCI_TOKEN }}`;

  return (
    <div className="space-y-4">
      <Step n={1} title="Add the private key to repo secrets">
        <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">Settings › Secrets and variables › Actions</code>,
        new secret <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">GLCI_TOKEN</code>.
      </Step>
      <Step n={2} title="Drop this workflow into your repo">
        <CodeBlock filename=".github/workflows/ci.yml">{yaml}</CodeBlock>
      </Step>
      <Step n={3} title="Push a commit">
        Watch it appear at <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">/wp-admin/admin.php?page=git-logs</code>{" "}
        within ~3 seconds.
      </Step>
    </div>
  );
}

function Step({ n, title, children }: { n: number; title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <div className="mb-3 flex items-center gap-3">
        <span className="inline-flex h-7 w-7 items-center justify-center rounded-full bg-primary/10 font-mono text-xs text-primary">
          {n}
        </span>
        <h3 className="text-sm font-semibold">{title}</h3>
      </div>
      <div className="pl-10 text-sm text-muted-foreground">{children}</div>
    </div>
  );
}

function CodeBlock({ children, filename }: { children: string; filename?: string }) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-background">
      {filename && (
        <div className="border-b border-border bg-muted/40 px-3 py-1.5 font-mono text-[11px] text-muted-foreground">
          {filename}
        </div>
      )}
      <pre className="overflow-x-auto p-3 font-mono text-[12px] leading-relaxed text-foreground">
        <code>{children}</code>
      </pre>
    </div>
  );
}

function Screenshots() {
  const tabs = [
    { id: "dashboard", label: "Dashboard" },
    { id: "run", label: "Run detail" },
    { id: "repos", label: "Repos" },
    { id: "diagrams", label: "Diagrams" },
    { id: "audit", label: "Audit log" },
  ] as const;
  type TabId = (typeof tabs)[number]["id"];
  const [active, setActive] = useState<TabId>("dashboard");

  return (
    <section id="screenshots" className="border-t border-border">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
            Built into the WordPress you already use
          </h2>
          <p className="mt-4 text-pretty text-muted-foreground md:text-lg">
            Five focused views. No new tab to keep open, no new login to remember.
          </p>
        </div>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-2">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setActive(t.id)}
              className={`inline-flex h-9 items-center justify-center rounded-full border px-4 text-sm transition-colors ${
                active === t.id
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-border bg-card text-muted-foreground hover:text-foreground"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className="mx-auto mt-10 max-w-5xl">
          <div className="overflow-hidden rounded-xl border border-border bg-card shadow-2xl">
            <div className="flex items-center gap-2 border-b border-border bg-muted/50 px-4 py-2.5">
              <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
              <span className="ml-3 truncate text-xs text-muted-foreground">
                yoursite.com/wp-admin/admin.php?page=git-logs
                {active !== "dashboard" && ` › ${tabs.find((t) => t.id === active)?.label.toLowerCase()}`}
              </span>
            </div>
            <div className="min-h-[420px]">
              {active === "dashboard" && <ShotDashboard />}
              {active === "run" && <ShotRun />}
              {active === "repos" && <ShotRepos />}
              {active === "diagrams" && <ShotDiagrams />}
              {active === "audit" && <ShotAudit />}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ShotDashboard() {
  const rows = [
    { repo: "acme/api", branch: "main", sha: "9f3a21e", status: "running", time: "12s ago" },
    { repo: "acme/web", branch: "feat/checkout", sha: "1b8c402", status: "passed", time: "3m" },
    { repo: "acme/infra", branch: "main", sha: "7d11ff9", status: "failed", time: "11m" },
    { repo: "acme/api", branch: "main", sha: "84a90bd", status: "passed", time: "22m" },
    { repo: "acme/docs", branch: "main", sha: "30ea7c2", status: "passed", time: "1h" },
  ] as const;
  return (
    <div className="p-5">
      <div className="mb-4 flex items-center justify-between">
        <h4 className="text-sm font-semibold">Recent runs</h4>
        <div className="flex gap-2">
          <FakeChip>All repos</FakeChip>
          <FakeChip>Last 24h</FakeChip>
        </div>
      </div>
      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-left text-xs">
          <thead className="bg-muted/50 text-muted-foreground">
            <tr>
              <th className="px-3 py-2 font-medium">Repo</th>
              <th className="px-3 py-2 font-medium">Branch</th>
              <th className="px-3 py-2 font-medium">SHA</th>
              <th className="px-3 py-2 font-medium">Status</th>
              <th className="px-3 py-2 font-medium text-right">When</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="border-t border-border">
                <td className="px-3 py-2 font-mono">{r.repo}</td>
                <td className="px-3 py-2 font-mono text-muted-foreground">{r.branch}</td>
                <td className="px-3 py-2 font-mono text-muted-foreground">{r.sha}</td>
                <td className="px-3 py-2"><StatusPill status={r.status} /></td>
                <td className="px-3 py-2 text-right text-muted-foreground">{r.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ShotRun() {
  const lines = [
    { lvl: "info", t: "› npm ci" },
    { lvl: "info", t: "added 421 packages in 6.2s" },
    { lvl: "info", t: "› npm run lint" },
    { lvl: "info", t: "✓ no problems" },
    { lvl: "info", t: "› npm test" },
    { lvl: "warn", t: "WARN  deprecated lifecycle hook in user.test.ts" },
    { lvl: "info", t: "PASS  src/auth.test.ts (12 tests)" },
    { lvl: "info", t: "PASS  src/api.test.ts (25 tests)" },
    { lvl: "info", t: "Tests:  37 passed, 37 total" },
    { lvl: "info", t: "› glci ship" },
    { lvl: "info", t: "✓ uploaded 1.2k log lines to git-logs" },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-[220px_1fr]">
      <aside className="border-b border-border bg-muted/30 p-4 text-xs md:border-b-0 md:border-r">
        <div className="mb-1 font-mono text-muted-foreground">acme/api</div>
        <div className="mb-3 font-mono text-[11px] text-muted-foreground">main · 9f3a21e</div>
        <StatusPill status="running" />
        <dl className="mt-4 space-y-2 text-[11px]">
          <div className="flex justify-between"><dt className="text-muted-foreground">Triggered</dt><dd>jane@acme</dd></div>
          <div className="flex justify-between"><dt className="text-muted-foreground">Duration</dt><dd>00:42</dd></div>
          <div className="flex justify-between"><dt className="text-muted-foreground">Lines</dt><dd>1,204</dd></div>
          <div className="flex justify-between"><dt className="text-muted-foreground">Warnings</dt><dd>1</dd></div>
        </dl>
      </aside>
      <div className="p-4 font-mono text-[11px] leading-relaxed">
        {lines.map((l, i) => (
          <div key={i} className="flex gap-3">
            <span className="w-8 shrink-0 text-right text-muted-foreground/60">{i + 1}</span>
            <span className={l.lvl === "warn" ? "text-amber-500" : "text-foreground"}>{l.t}</span>
          </div>
        ))}
        <div className="mt-2 inline-flex items-center gap-2 text-[11px] text-emerald-600">
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500" />
          streaming…
        </div>
      </div>
    </div>
  );
}

function ShotRepos() {
  const repos = [
    { name: "acme/api", runs: 412, last: "12s ago", health: "ok" },
    { name: "acme/web", runs: 386, last: "3m ago", health: "ok" },
    { name: "acme/infra", runs: 98, last: "11m ago", health: "fail" },
    { name: "acme/docs", runs: 54, last: "1h ago", health: "ok" },
  ] as const;
  return (
    <div className="p-5">
      <div className="grid gap-4 sm:grid-cols-2">
        {repos.map((r) => (
          <div key={r.name} className="rounded-lg border border-border p-4">
            <div className="flex items-center justify-between">
              <div className="font-mono text-sm">{r.name}</div>
              <span className={`h-2 w-2 rounded-full ${r.health === "ok" ? "bg-emerald-500" : "bg-destructive"}`} />
            </div>
            <div className="mt-3 flex justify-between text-xs text-muted-foreground">
              <span>{r.runs} runs</span>
              <span>last {r.last}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ShotDiagrams() {
  return (
    <div className="p-5">
      <div className="mb-4 text-xs text-muted-foreground">
        Auto-rendered Mermaid pipeline diagrams shipped with each repo
      </div>
      <div className="rounded-lg border border-border bg-muted/20 p-8">
        <svg viewBox="0 0 600 220" className="mx-auto block w-full max-w-2xl">
          {[
            { x: 30, label: "push" },
            { x: 165, label: "lint" },
            { x: 300, label: "build" },
            { x: 435, label: "test" },
          ].map((n, i, arr) => (
            <g key={n.label}>
              <rect x={n.x} y={90} width={100} height={40} rx={8} className="fill-card stroke-border" strokeWidth={1.5} />
              <text x={n.x + 50} y={115} textAnchor="middle" className="fill-foreground font-mono text-[12px]">{n.label}</text>
              {i < arr.length - 1 && (
                <path d={`M${n.x + 100} 110 L${arr[i + 1].x} 110`} className="stroke-muted-foreground" strokeWidth={1.5} markerEnd="url(#arr)" />
              )}
            </g>
          ))}
          <g>
            <rect x={300} y={170} width={100} height={40} rx={8} className="fill-card stroke-border" strokeWidth={1.5} />
            <text x={350} y={195} textAnchor="middle" className="fill-foreground font-mono text-[12px]">deploy</text>
            <path d="M350 130 L350 170" className="stroke-muted-foreground" strokeWidth={1.5} markerEnd="url(#arr)" />
          </g>
          <defs>
            <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M0 0 L10 5 L0 10 z" className="fill-muted-foreground" />
            </marker>
          </defs>
        </svg>
      </div>
    </div>
  );
}

function ShotAudit() {
  const events = [
    { t: "2026-05-12 14:22:01", actor: "jane@acme", action: "run.created", target: "acme/api @ 9f3a21e" },
    { t: "2026-05-12 14:18:44", actor: "system", action: "key.rotated", target: "ed25519 #4" },
    { t: "2026-05-12 13:02:11", actor: "tom@acme", action: "run.failed", target: "acme/infra @ 7d11ff9" },
    { t: "2026-05-12 11:41:09", actor: "jane@acme", action: "repo.added", target: "acme/docs" },
    { t: "2026-05-11 22:10:55", actor: "ci-bot", action: "run.passed", target: "acme/web @ 1b8c402" },
  ];
  return (
    <div className="p-5">
      <div className="overflow-hidden rounded-lg border border-border">
        <table className="w-full text-left font-mono text-[11px]">
          <thead className="bg-muted/50 text-muted-foreground">
            <tr>
              <th className="px-3 py-2 font-medium">Timestamp</th>
              <th className="px-3 py-2 font-medium">Actor</th>
              <th className="px-3 py-2 font-medium">Action</th>
              <th className="px-3 py-2 font-medium">Target</th>
            </tr>
          </thead>
          <tbody>
            {events.map((e, i) => (
              <tr key={i} className="border-t border-border">
                <td className="px-3 py-2 text-muted-foreground">{e.t}</td>
                <td className="px-3 py-2">{e.actor}</td>
                <td className="px-3 py-2 text-primary">{e.action}</td>
                <td className="px-3 py-2 text-muted-foreground">{e.target}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function FakeChip({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex h-7 items-center rounded-full border border-border bg-card px-3 text-[11px] text-muted-foreground">
      {children}
    </span>
  );
}

function StatusPill({ status }: { status: "running" | "passed" | "failed" }) {
  const map = {
    running: { c: "bg-emerald-500/10 text-emerald-600", dot: "bg-emerald-500 animate-pulse", label: "running" },
    passed: { c: "bg-emerald-500/10 text-emerald-600", dot: "bg-emerald-500", label: "passed" },
    failed: { c: "bg-destructive/10 text-destructive", dot: "bg-destructive", label: "failed" },
  } as const;
  const s = map[status];
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-[10px] font-medium ${s.c}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${s.dot}`} />
      {s.label}
    </span>
  );
}

function HowItWorks() {
  const steps = [
    {
      n: "01",
      title: "Push a commit",
      body:
        "Your normal git push triggers GitHub Actions (or any CI runner). Nothing about your existing workflow changes.",
    },
    {
      n: "02",
      title: "glci streams the run",
      body:
        "The glci CLI runs your build, captures every stdout/stderr line, signs the batch with Ed25519, and POSTs incrementally to your WP site.",
    },
    {
      n: "03",
      title: "Your team watches in WP-Admin",
      body:
        "Open /wp-admin/admin.php?page=git-logs. The run appears within ~3 seconds, logs stream live, and the result is permanent in the audit log.",
    },
  ];

  const yaml = `# .github/workflows/ci.yml
name: ci
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci

      # The one line that wires CI \u2192 your WordPress dashboard
      - run: glci run --stream \\
          --server-url=https://yoursite.com/wp-json/git-logs/v1
        env:
          GLCI_TOKEN: \${{ secrets.GLCI_TOKEN }}`;

  return (
    <section id="how" className="border-t border-border bg-muted/30">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">How it works</h2>
          <p className="mt-4 text-pretty text-muted-foreground md:text-lg">
            Three moving pieces. One line of CI config. No new dashboards to learn.
          </p>
        </div>

        <ol className="mt-14 grid gap-6 md:grid-cols-3">
          {steps.map((s, i) => (
            <li
              key={s.n}
              className="relative rounded-xl border border-border bg-card p-6"
            >
              <div className="mb-4 flex items-center gap-3">
                <span className="font-mono text-xs text-muted-foreground">{s.n}</span>
                <span className="h-px flex-1 bg-border" />
                {i < steps.length - 1 && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden className="text-muted-foreground">
                    <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
              </div>
              <h3 className="text-base font-semibold">{s.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.body}</p>
            </li>
          ))}
        </ol>

        <div className="mx-auto mt-12 max-w-3xl">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-semibold">Concrete example — drop this into your repo</h3>
            <span className="font-mono text-xs text-muted-foreground">.github/workflows/ci.yml</span>
          </div>
          <div className="overflow-hidden rounded-xl border border-border bg-card shadow-sm">
            <div className="flex items-center gap-2 border-b border-border bg-muted/50 px-4 py-2">
              <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
            </div>
            <pre className="overflow-x-auto p-5 font-mono text-[12px] leading-relaxed text-foreground">
              <code>{yaml}</code>
            </pre>
          </div>
          <p className="mt-3 text-center text-xs text-muted-foreground">
            That single <code className="rounded bg-muted px-1 py-0.5 font-mono">glci run --stream</code> line is the entire integration.
          </p>
        </div>
      </div>
    </section>
  );
}

function Features() {
  const items = [
    {
      title: "Live log streaming",
      body:
        "glci streams stdout/stderr line-by-line over HTTPS while the job runs. Your team watches builds finish in real time — no refresh, no polling.",
      icon: (
        <path d="M4 7h16M4 12h10M4 17h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      ),
    },
    {
      title: "Multi-repo dashboard",
      body:
        "One WP-Admin page shows every repo, every branch, every run. Filter by status, drill into any commit SHA, compare runs side-by-side.",
      icon: (
        <path d="M4 6h7v6H4zM13 6h7v6h-7zM4 14h7v6H4zM13 14h7v6h-7z" stroke="currentColor" strokeWidth="2" />
      ),
    },
    {
      title: "Ed25519-signed ingest",
      body:
        "Every batch is signed with libsodium Ed25519. The plugin verifies signatures before writing to the DB — no shared secrets in CI variables.",
      icon: (
        <path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      ),
    },
    {
      title: "Permanent audit log",
      body:
        "Every run, every key rotation, every config change is recorded with actor + timestamp. When something breaks next week, the trail is already there.",
      icon: (
        <path d="M9 5h6l4 4v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2zM9 13h6M9 17h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      ),
    },
    {
      title: "WordPress auth, reused",
      body:
        "Permissions piggyback on WP roles you already manage. No new user system, no second SSO to wire up. Editors read, admins manage keys.",
      icon: (
        <path d="M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      ),
    },
    {
      title: "100% self-hosted",
      body:
        "Runs on the WordPress you already pay for. SQLite-backed, zero external services, your logs never leave your server. GPL-2.0, no SaaS lock-in.",
      icon: (
        <path d="M4 7l8-4 8 4-8 4-8-4zM4 12l8 4 8-4M4 17l8 4 8-4" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      ),
    },
  ];

  return (
    <section id="features" className="border-t border-border">
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
            Everything you need to trust your pipeline
          </h2>
          <p className="mt-4 text-pretty text-muted-foreground md:text-lg">
            A focused dashboard for teams that want CI visibility without handing logs to a third party.
          </p>
        </div>

        <div className="mt-14 grid gap-px overflow-hidden rounded-xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3">
          {items.map((it) => (
            <div key={it.title} className="bg-card p-6 transition-colors hover:bg-accent/40">
              <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
                  {it.icon}
                </svg>
              </div>
              <h3 className="text-base font-semibold">{it.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{it.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Header() {
  return (
    <header className="border-b border-border">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2 font-semibold tracking-tight">
          <span className="inline-block h-6 w-6 rounded-md bg-primary" aria-hidden />
          Git Logs
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
          <a href="#features" className="hover:text-foreground">Features</a>
          <a href="#how" className="hover:text-foreground">How it works</a>
          <a href="#install" className="hover:text-foreground">Install</a>
          <a href="#faq" className="hover:text-foreground">FAQ</a>
        </nav>
        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center justify-center rounded-md border border-input bg-background px-3 py-1.5 text-sm font-medium hover:bg-accent"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 opacity-60"
        style={{
          backgroundImage:
            "radial-gradient(60rem 30rem at 50% -10%, color-mix(in oklab, var(--primary) 18%, transparent), transparent 60%)",
        }}
      />
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs text-muted-foreground">
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500" aria-hidden />
            v0.4 — WordPress 6.5+ · PHP 8.1+ · Self-hosted
          </div>

          <h1 className="text-balance text-4xl font-bold tracking-tight md:text-6xl">
            Watch your CI runs live, inside WordPress.
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-muted-foreground md:text-lg">
            Git Logs streams every build, test, and deploy from your repos into a private WP-Admin
            dashboard. Push a commit — your team watches it pass or fail in real time, with the
            full log line-by-line and a permanent audit trail.
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <a
              href="#install"
              className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary/90"
            >
              Install in 2 minutes
            </a>
            <a
              href="#how"
              className="inline-flex h-11 items-center justify-center rounded-md border border-input bg-background px-6 text-sm font-medium hover:bg-accent"
            >
              See how it works
            </a>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-muted-foreground">
            <Badge label="Live log streaming" />
            <Badge label="Ed25519-signed" />
            <Badge label="Multi-repo" />
            <Badge label="Audit log" />
            <Badge label="100% self-hosted" />
          </div>
        </div>

        <HeroPreview />
      </div>
    </section>
  );
}

function Badge({ label }: { label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <svg width="12" height="12" viewBox="0 0 20 20" fill="none" aria-hidden>
        <path
          d="M5 10.5l3 3 7-7"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-emerald-500"
        />
      </svg>
      {label}
    </span>
  );
}

function HeroPreview() {
  return (
    <div className="mx-auto mt-16 max-w-4xl">
      <div className="overflow-hidden rounded-xl border border-border bg-card shadow-2xl">
        <div className="flex items-center gap-2 border-b border-border bg-muted/50 px-4 py-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-destructive/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
          <span className="ml-3 truncate text-xs text-muted-foreground">
            yoursite.com/wp-admin/admin.php?page=git-logs
          </span>
        </div>
        <div className="grid gap-0 md:grid-cols-[180px_1fr]">
          <aside className="border-b border-border bg-muted/30 p-4 text-xs md:border-b-0 md:border-r">
            <div className="mb-2 font-medium text-foreground">Repos</div>
            <ul className="space-y-1.5 text-muted-foreground">
              <li className="text-foreground">acme/api</li>
              <li>acme/web</li>
              <li>acme/infra</li>
            </ul>
          </aside>
          <div className="p-4 font-mono text-[11px] leading-relaxed">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-foreground">acme/api · main · 9f3a21e</span>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-600">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500" />
                running
              </span>
            </div>
            <pre className="overflow-hidden whitespace-pre-wrap text-muted-foreground">
{`› npm ci
added 421 packages in 6.2s
› npm run lint
✓ no problems
› npm test
PASS  src/auth.test.ts
PASS  src/api.test.ts
Tests:  37 passed, 37 total
› glci ship
✓ uploaded 1.2k log lines to git-logs`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}

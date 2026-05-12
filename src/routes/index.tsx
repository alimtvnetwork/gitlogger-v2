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
    </div>
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

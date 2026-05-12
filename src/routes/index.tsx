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
    </div>
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

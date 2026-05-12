import { Terminal, ShieldCheck, LayoutDashboard, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: Terminal,
    label: "Step 1",
    title: "glci runs in CI",
    body: "The glci Go CLI runs on your dev machine or inside GitHub Actions / GitLab. It captures repo, branch, commit SHA, status, timing, and the full event stream.",
  },
  {
    icon: ShieldCheck,
    label: "Step 2",
    title: "Signed REST ingest",
    body: "Each payload is signed with an Ed25519 key registered to your WordPress site. No passwords, no shared secrets — verification is cryptographic.",
  },
  {
    icon: LayoutDashboard,
    label: "Step 3",
    title: "WP admin dashboard",
    body: "The plugin stores everything (repos, branches, runs, events, audit log) and renders it in a React admin UI at WP Admin → Git Logs.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="border-b border-border bg-secondary/30">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            How it works
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            A small CLI, a signed REST call, and a WordPress dashboard. That's it.
          </p>
        </div>

        <div className="mt-14 grid gap-6 lg:grid-cols-3">
          {steps.map(({ icon: Icon, label, title, body }, i) => (
            <div key={title} className="relative">
              <div className="h-full rounded-xl border border-border bg-card p-6">
                <div className="flex items-center gap-3">
                  <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-accent text-accent-foreground">
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    {label}
                  </span>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-card-foreground">
                  {title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {body}
                </p>
              </div>
              {i < steps.length - 1 && (
                <div
                  aria-hidden
                  className="absolute -right-3 top-1/2 hidden -translate-y-1/2 lg:block"
                >
                  <ArrowRight className="h-5 w-5 text-muted-foreground" />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Concrete example */}
        <div className="mt-12 rounded-xl border border-border bg-card p-6 sm:p-8">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-chart-2" />
            In practice
          </div>
          <p className="mt-3 text-base leading-relaxed text-card-foreground sm:text-lg">
            You push a commit. GitHub Actions runs your tests and calls{" "}
            <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">
              glci run
            </code>
            . Three seconds later your team opens{" "}
            <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">
              /wp-admin/admin.php?page=git-logs
            </code>{" "}
            and watches the run stream live. If it fails next week, the failure is
            already in the audit log alongside who deployed it.
          </p>
        </div>
      </div>
    </section>
  );
}

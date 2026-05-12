import {
  GitBranch,
  Radio,
  ShieldCheck,
  Server,
  Users,
  ScrollText,
} from "lucide-react";

const features = [
  {
    icon: GitBranch,
    title: "Multi-repo dashboard",
    body: "See every build, test, and deploy across all your repositories on one screen — no more jumping between Actions tabs.",
  },
  {
    icon: Radio,
    title: "Live log streaming",
    body: "Follow runs as they execute. Filter by log level, jump to errors, and replay the full event stream after the fact.",
  },
  {
    icon: ShieldCheck,
    title: "Ed25519-signed ingestion",
    body: "Every CI payload is cryptographically signed. No shared secrets to leak, no API tokens to rotate.",
  },
  {
    icon: Server,
    title: "Self-hosted",
    body: "Your build data stays on your infrastructure. Runs anywhere WordPress runs — including the host you already pay for.",
  },
  {
    icon: Users,
    title: "Uses WP users & roles",
    body: "Permissions inherit from WordPress. The team you've already onboarded gets access — no new identity provider.",
  },
  {
    icon: ScrollText,
    title: "Built-in audit log",
    body: "Key registrations, GC runs, and admin actions are recorded automatically. Know who did what, when.",
  },
];

export function Features() {
  return (
    <section id="features" className="border-b border-border bg-background">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything your team needs to ship with confidence
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            A focused toolkit for developer teams who want CI visibility without
            handing their data to another SaaS.
          </p>
        </div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(({ icon: Icon, title, body }) => (
            <div
              key={title}
              className="group relative rounded-xl border border-border bg-card p-6 transition-shadow hover:shadow-lg"
            >
              <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-accent text-accent-foreground">
                <Icon className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-lg font-semibold text-card-foreground">
                {title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

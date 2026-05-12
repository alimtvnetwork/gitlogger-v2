import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const requirements = [
  { label: "WordPress", value: "6.5 or newer" },
  { label: "PHP", value: "8.1 or newer" },
  { label: "PHP extensions", value: "pdo_sqlite, sodium" },
  { label: "Database", value: "SQLite (bundled) — no MySQL config needed" },
  { label: "glci CLI", value: "Linux / macOS / Windows (amd64, arm64)" },
];

const faqs = [
  {
    q: "Why WordPress, of all things?",
    a: "Because most teams already run one. You get authentication, user management, roles, hosting, and an admin shell for free — instead of standing up another service with its own login system.",
  },
  {
    q: "Is it secure? No shared secrets?",
    a: "Every payload is signed with an Ed25519 key. The private key lives only on the machine that runs glci; the public key is registered in WP Admin. There is no bearer token or API password to leak.",
  },
  {
    q: "Does it work with GitLab / Bitbucket / Jenkins?",
    a: "Yes — glci is a generic CLI. Anywhere you can run a binary, you can ship runs to Git Logs. We provide a ready-made GitHub Actions setup; the same pattern works on GitLab CI, CircleCI, Jenkins, or your laptop.",
  },
  {
    q: "Where does the data live?",
    a: "On your WordPress host, in a SQLite database inside wp-content/uploads. Nothing leaves your infrastructure. Back it up with the rest of your wp-content directory.",
  },
  {
    q: "Can multiple repos report to one site?",
    a: "Yes — that is the whole point. Repos, branches, and runs are first-class entities. The dashboard unifies every repo your team has registered.",
  },
  {
    q: "Is it free?",
    a: "Yes. Git Logs is open source, GPL-2.0-or-later for the WP plugin and Apache-2.0 for the glci CLI. No paid tier, no vendor account.",
  },
];

export function Requirements() {
  return (
    <section id="requirements" className="border-b border-border bg-background">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="grid gap-12 lg:grid-cols-2">
          {/* Requirements */}
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Requirements
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              If you can run modern WordPress, you can run Git Logs.
            </p>

            <dl className="mt-8 divide-y divide-border rounded-xl border border-border bg-card">
              {requirements.map((r) => (
                <div
                  key={r.label}
                  className="flex flex-col gap-1 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
                >
                  <dt className="text-sm font-semibold text-card-foreground">
                    {r.label}
                  </dt>
                  <dd className="text-sm text-muted-foreground">{r.value}</dd>
                </div>
              ))}
            </dl>
          </div>

          {/* FAQ */}
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Frequently asked
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              The questions every team asks before they install.
            </p>

            <Accordion type="single" collapsible className="mt-8">
              {faqs.map((f, i) => (
                <AccordionItem key={f.q} value={`item-${i}`}>
                  <AccordionTrigger className="text-left text-base font-semibold">
                    {f.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm leading-relaxed text-muted-foreground">
                    {f.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </div>
    </section>
  );
}

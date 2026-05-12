import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowLeft } from "lucide-react";
import { Footer } from "@/components/landing/Footer";
import { SITE_URL, LINKS } from "@/config/site";

export const Route = createFileRoute("/docs")({
  component: DocsPage,
  head: () => ({
    meta: [
      { title: "Docs — Git Logs" },
      {
        name: "description",
        content:
          "Install, configure, and operate Git Logs. Plugin install, glci CLI setup, key registration, CI integration, and troubleshooting.",
      },
      { property: "og:title", content: "Docs — Git Logs" },
      {
        property: "og:description",
        content:
          "Install, configure, and operate Git Logs — WordPress plugin + glci CLI.",
      },
      { property: "og:url", content: `${SITE_URL}/docs` },
    ],
    links: [{ rel: "canonical", href: `${SITE_URL}/docs` }],
  }),
});

const sections = [
  { id: "install-plugin", label: "Install the plugin" },
  { id: "install-glci", label: "Install glci CLI" },
  { id: "register-key", label: "Register an Ed25519 key" },
  { id: "ci-integration", label: "Wire it into CI" },
  { id: "config", label: "Configuration reference" },
  { id: "troubleshooting", label: "Troubleshooting" },
  { id: "uninstall", label: "Uninstall" },
];

function DocsPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="border-b border-border bg-secondary/30">
        <div className="mx-auto max-w-6xl px-6 py-12">
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" /> Back to overview
          </Link>
          <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">
            Git Logs documentation
          </h1>
          <p className="mt-3 max-w-2xl text-lg text-muted-foreground">
            Everything you need to install Git Logs, register your first key, and
            ship CI runs to your WordPress site.
          </p>
        </div>
      </div>

      <div className="mx-auto grid max-w-6xl gap-12 px-6 py-16 lg:grid-cols-[220px_1fr]">
        {/* TOC */}
        <nav className="lg:sticky lg:top-8 lg:self-start">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            On this page
          </p>
          <ul className="mt-3 space-y-2 text-sm">
            {sections.map((s) => (
              <li key={s.id}>
                <a
                  href={`#${s.id}`}
                  className="text-muted-foreground hover:text-foreground"
                >
                  {s.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Body */}
        <article className="prose-docs space-y-12">
          <Section id="install-plugin" title="Install the plugin">
            <ol className="list-decimal space-y-2 pl-5 text-muted-foreground">
              <li>
                Download the latest release ZIP from{" "}
                <a className="underline" href={LINKS.releases}>
                  GitHub releases
                </a>
                .
              </li>
              <li>
                In WP Admin, go to <strong>Plugins → Add New → Upload Plugin</strong>
                .
              </li>
              <li>Select the ZIP, install, then activate.</li>
              <li>
                Visit <strong>WP Admin → Git Logs</strong>. The first activation
                runs the database migrations automatically.
              </li>
            </ol>
            <Callout title="Requirements">
              WordPress 6.5+, PHP 8.1+, with <code>pdo_sqlite</code> and{" "}
              <code>sodium</code> extensions enabled.
            </Callout>
          </Section>

          <Section id="install-glci" title="Install the glci CLI">
            <p className="text-muted-foreground">
              The CLI is a single Go binary. Install it on each machine that runs
              tests or builds (your laptop, CI runners, deploy bots).
            </p>
            <CodeBlock
              code={`# Homebrew
brew install ${LINKS.glciTap}

# Or with Go
go install ${LINKS.glciGo}

# Or download a prebuilt binary
curl -L ${LINKS.glciTarball} | tar xz`}
            />
            <p className="text-muted-foreground">
              Verify with <code>glci --version</code>.
            </p>
          </Section>

          <Section id="register-key" title="Register an Ed25519 key">
            <ol className="list-decimal space-y-2 pl-5 text-muted-foreground">
              <li>
                On the machine that will run <code>glci</code>, generate a key:
              </li>
            </ol>
            <CodeBlock code={`glci keys generate --out ~/.config/glci/key`} />
            <ol className="list-decimal space-y-2 pl-5 text-muted-foreground" start={2}>
              <li>
                Copy the public key (printed to stdout).
              </li>
              <li>
                In WP Admin → Git Logs → Keys, paste the public key and give it a
                label (e.g. <em>github-actions-frontend</em>).
              </li>
              <li>
                Save. The key is now authorized to ingest runs.
              </li>
            </ol>
          </Section>

          <Section id="ci-integration" title="Wire it into CI">
            <p className="text-muted-foreground">
              Set two secrets in your CI provider, then call <code>glci run</code>{" "}
              from a workflow step.
            </p>
            <CodeBlock
              code={`# .github/workflows/ci.yml
- uses: ${LINKS.setupGlciAction}
- run: glci run -- npm test
  env:
    GLCI_ENDPOINT: \${{ secrets.GLCI_ENDPOINT }}
    GLCI_KEY:      \${{ secrets.GLCI_KEY }}`}
            />
            <ul className="list-disc space-y-2 pl-5 text-muted-foreground">
              <li>
                <code>GLCI_ENDPOINT</code> — your WP site URL (e.g.
                <code>https://example.com</code>).
              </li>
              <li>
                <code>GLCI_KEY</code> — the contents of{" "}
                <code>~/.config/glci/key</code>, stored as a CI secret.
              </li>
            </ul>
          </Section>

          <Section id="config" title="Configuration reference">
            <div className="overflow-x-auto rounded-lg border border-border">
              <table className="w-full text-sm">
                <thead className="bg-muted text-muted-foreground">
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold">
                      Variable
                    </th>
                    <th className="px-4 py-2 text-left font-semibold">
                      Required
                    </th>
                    <th className="px-4 py-2 text-left font-semibold">Purpose</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {[
                    ["GLCI_ENDPOINT", "yes", "Base URL of your WordPress site"],
                    ["GLCI_KEY", "yes", "Ed25519 private key (CI secret)"],
                    ["GLCI_REPO", "no", "Override repo slug detection"],
                    ["GLCI_BRANCH", "no", "Override branch detection"],
                    ["GLCI_TIMEOUT", "no", "HTTP timeout (default 30s)"],
                  ].map(([k, req, purpose]) => (
                    <tr key={k}>
                      <td className="px-4 py-2 font-mono text-xs">{k}</td>
                      <td className="px-4 py-2 text-muted-foreground">{req}</td>
                      <td className="px-4 py-2 text-muted-foreground">
                        {purpose}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>

          <Section id="troubleshooting" title="Troubleshooting">
            <Faq
              q="401 Unauthorized when ingesting"
              a="Your public key is not registered in WP Admin → Git Logs → Keys, or the wrong private key is loaded. Confirm the public key matches what's stored in WP."
            />
            <Faq
              q="Plugin shows a database error on activation"
              a="The pdo_sqlite extension is missing. Install php-sqlite3 (Debian/Ubuntu) or enable it in your php.ini, then reactivate the plugin."
            />
            <Faq
              q="Runs appear but logs are empty"
              a="glci streams events as the wrapped command produces them. Make sure stdout/stderr are not buffered (e.g. use unbuffered Python: python -u, or stdbuf -oL)."
            />
            <Faq
              q="I get 413 Payload Too Large"
              a="Your web server's upload limit is below the configured chunk size. Raise client_max_body_size (nginx) or LimitRequestBody (Apache), or lower GLCI_CHUNK_SIZE."
            />
          </Section>

          <Section id="uninstall" title="Uninstall">
            <p className="text-muted-foreground">
              Deactivate and delete the plugin from WP Admin → Plugins. The
              SQLite database is preserved by default. To wipe data, delete{" "}
              <code>wp-content/uploads/git-logs/</code> after uninstall.
            </p>
          </Section>
        </article>
      </div>

      <Footer />
    </main>
  );
}

function Section({
  id,
  title,
  children,
}: {
  id: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-8">
      <h2 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
        {title}
      </h2>
      <div className="mt-4 space-y-4 text-base leading-relaxed">{children}</div>
    </section>
  );
}

function CodeBlock({ code }: { code: string }) {
  return (
    <pre className="overflow-x-auto rounded-lg border border-border bg-card p-4 font-mono text-sm leading-relaxed text-card-foreground">
      <code>{code}</code>
    </pre>
  );
}

function Callout({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-border bg-accent/40 p-4">
      <p className="text-sm font-semibold text-foreground">{title}</p>
      <p className="mt-1 text-sm text-muted-foreground">{children}</p>
    </div>
  );
}

function Faq({ q, a }: { q: string; a: string }) {
  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <p className="font-semibold text-card-foreground">{q}</p>
      <p className="mt-1 text-sm text-muted-foreground">{a}</p>
    </div>
  );
}

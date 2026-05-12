import { useState } from "react";
import { cn } from "@/lib/utils";
import { Check, Copy } from "lucide-react";
import { LINKS } from "@/config/site";

type Tab = { id: string; label: string; code: string; intro: string };

const tabs: Tab[] = [
  {
    id: "plugin",
    label: "WordPress plugin",
    intro: "Upload the ZIP from your WP admin → Plugins → Add New → Upload Plugin.",
    code: `# 1. Download the latest release
curl -LO ${LINKS.pluginZip}

# 2. In WP Admin → Plugins → Add New → Upload Plugin
# 3. Activate "Git Logs"
# 4. Visit WP Admin → Git Logs → register your first Ed25519 key`,
  },
  {
    id: "glci",
    label: "glci CLI",
    intro: "Install the Go CLI on your dev machine or CI runner.",
    code: `# Homebrew (macOS / Linux)
brew install ${LINKS.glciTap}

# Or with Go
go install ${LINKS.glciGo}

# Or download a prebuilt binary
curl -L ${LINKS.glciTarball} | tar xz`,
  },
  {
    id: "ci",
    label: "GitHub Actions",
    intro: "Drop this into .github/workflows/ci.yml to ship runs to your WordPress site.",
    code: `name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ${LINKS.setupGlciAction}
      - run: glci run -- npm test
        env:
          GLCI_ENDPOINT: \${{ secrets.GLCI_ENDPOINT }}
          GLCI_KEY:      \${{ secrets.GLCI_KEY }}`,
  },
];

export function QuickStart() {
  const [active, setActive] = useState(tabs[0].id);
  const [copied, setCopied] = useState(false);
  const current = tabs.find((t) => t.id === active) ?? tabs[0];

  const copy = async () => {
    await navigator.clipboard.writeText(current.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <section id="install" className="border-b border-border bg-secondary/30">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Quick start
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Three pieces — install the plugin, install the CLI, wire it into CI.
          </p>
        </div>

        <div className="mx-auto mt-10 max-w-3xl">
          <div className="flex flex-wrap gap-2 border-b border-border">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setActive(t.id)}
                className={cn(
                  "-mb-px border-b-2 px-4 py-2 text-sm font-medium transition-colors",
                  active === t.id
                    ? "border-foreground text-foreground"
                    : "border-transparent text-muted-foreground hover:text-foreground",
                )}
              >
                {t.label}
              </button>
            ))}
          </div>

          <p className="mt-6 text-sm text-muted-foreground">{current.intro}</p>

          <div className="relative mt-3 overflow-hidden rounded-xl border border-border bg-card">
            <button
              onClick={copy}
              className="absolute right-3 top-3 inline-flex items-center gap-1.5 rounded-md border border-border bg-background px-2.5 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground"
              aria-label="Copy"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5" /> Copied
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" /> Copy
                </>
              )}
            </button>
            <pre className="overflow-x-auto p-5 pr-20 font-mono text-sm leading-relaxed text-card-foreground">
              <code>{current.code}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}

import { createFileRoute } from "@tanstack/react-router";
import heroDashboard from "@/assets/hero-dashboard.jpg";
import { Button } from "@/components/ui/button";
import { Github, Download, GitBranch, Activity } from "lucide-react";
import { Features } from "@/components/landing/Features";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Screenshots } from "@/components/landing/Screenshots";
import { QuickStart } from "@/components/landing/QuickStart";
import { Requirements } from "@/components/landing/Requirements";
import { Footer } from "@/components/landing/Footer";

const SITE_URL = "https://15bba2cc-3c74-4134-aa1e-6340608435e8.lovable.app";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => ({
    meta: [
      { title: "Git Logs — Self-hosted CI/CD dashboard for WordPress" },
      {
        name: "description",
        content:
          "Git Logs turns your WordPress site into a unified CI/CD dashboard. Multi-repo runs, live log streaming, Ed25519-signed ingestion, self-hosted on infra you already own.",
      },
      { property: "og:title", content: "Git Logs — Self-hosted CI/CD dashboard for WordPress" },
      {
        property: "og:description",
        content:
          "One dashboard for every repo's builds, tests, and deploys — hosted on your own WordPress.",
      },
      { property: "og:type", content: "website" },
      { property: "og:url", content: SITE_URL },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: "Git Logs — Self-hosted CI/CD dashboard for WordPress" },
      {
        name: "twitter:description",
        content:
          "One dashboard for every repo's builds, tests, and deploys — hosted on your own WordPress.",
      },
    ],
    links: [{ rel: "canonical", href: SITE_URL }],
    scripts: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "SoftwareApplication",
          name: "Git Logs",
          description:
            "Self-hosted CI/CD dashboard for WordPress. Multi-repo runs, live log streaming, Ed25519-signed ingestion.",
          applicationCategory: "DeveloperApplication",
          operatingSystem: "WordPress 6.5+, PHP 8.1+",
          softwareVersion: "0.4.0",
          url: SITE_URL,
          offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
          license: "https://www.gnu.org/licenses/gpl-2.0.html",
        }),
      },
    ],
  }),
});

function Index() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <Hero />
      <Features />
      <HowItWorks />
      <Screenshots />
      <QuickStart />
      <Requirements />
      <Footer />
    </main>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-border">
      {/* subtle background accents */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_80%_50%_at_50%_-10%,var(--color-accent),transparent)]"
      />

      <div className="mx-auto max-w-6xl px-6 pt-16 pb-12 sm:pt-24 sm:pb-20">
        {/* status / version chip */}
        <div className="mb-6 flex justify-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-chart-2" />
            v0.4.0 · WordPress 6.5+ · PHP 8.1+
          </span>
        </div>

        <h1 className="text-center text-4xl font-bold tracking-tight text-foreground sm:text-5xl md:text-6xl">
          Your CI/CD pipeline,
          <br className="hidden sm:block" />{" "}
          <span className="bg-gradient-to-r from-chart-1 to-chart-4 bg-clip-text text-transparent">
            inside WordPress.
          </span>
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-center text-lg text-muted-foreground sm:text-xl">
          Git Logs is a self-hosted dashboard for every build, test, and deploy across your
          repositories. Live log streaming, Ed25519-signed ingestion, and the WordPress users
          you already trust — all in one place.
        </p>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button size="lg" className="gap-2">
            <Download className="h-4 w-4" />
            Download plugin
          </Button>
          <Button size="lg" variant="outline" className="gap-2">
            <Github className="h-4 w-4" />
            View on GitHub
          </Button>
        </div>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-muted-foreground">
          <span className="inline-flex items-center gap-1.5">
            <GitBranch className="h-4 w-4" />
            Multi-repo
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Activity className="h-4 w-4" />
            Live streaming
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="font-mono text-xs">Ed25519</span>
            signed
          </span>
        </div>

        {/* hero screenshot */}
        <div className="mt-14 sm:mt-20">
          <div className="relative mx-auto max-w-5xl">
            <div
              aria-hidden
              className="absolute -inset-4 -z-10 rounded-2xl bg-gradient-to-tr from-chart-1/20 to-chart-4/20 blur-2xl"
            />
            <div className="overflow-hidden rounded-xl border border-border bg-card shadow-2xl">
              <img
                src={heroDashboard}
                alt="Git Logs admin dashboard inside WordPress showing CI runs across multiple repositories"
                width={1920}
                height={1080}
                className="h-auto w-full"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

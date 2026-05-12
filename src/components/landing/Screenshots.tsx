import { useState } from "react";
import dashboard from "@/assets/hero-dashboard.jpg";
import runDetail from "@/assets/screenshot-run-detail.jpg";
import repos from "@/assets/screenshot-repos.jpg";
import diagrams from "@/assets/screenshot-diagrams.jpg";
import audit from "@/assets/screenshot-audit.jpg";
import { cn } from "@/lib/utils";

const shots = [
  { id: "dashboard", label: "Dashboard", src: dashboard, caption: "Recent runs across every repo, color-coded by status." },
  { id: "run", label: "Run detail", src: runDetail, caption: "Live event stream with log-level filters." },
  { id: "repos", label: "Repos", src: repos, caption: "Every repository that has reported in, at a glance." },
  { id: "diagrams", label: "Diagrams", src: diagrams, caption: "Architecture and flow diagrams from your spec folder." },
  { id: "audit", label: "Audit log", src: audit, caption: "Who did what, when — automatically recorded." },
];

export function Screenshots() {
  const [active, setActive] = useState(shots[0].id);
  const current = shots.find((s) => s.id === active) ?? shots[0];

  return (
    <section id="screenshots" className="border-b border-border bg-background">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            See it in action
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Five surfaces inside WP Admin → Git Logs.
          </p>
        </div>

        <div className="mt-10 flex flex-wrap justify-center gap-2">
          {shots.map((s) => (
            <button
              key={s.id}
              onClick={() => setActive(s.id)}
              className={cn(
                "rounded-full border px-4 py-2 text-sm font-medium transition-colors",
                active === s.id
                  ? "border-foreground bg-foreground text-background"
                  : "border-border bg-card text-muted-foreground hover:text-foreground",
              )}
            >
              {s.label}
            </button>
          ))}
        </div>

        <div className="mt-8">
          <div className="relative mx-auto max-w-5xl">
            <div
              aria-hidden
              className="absolute -inset-4 -z-10 rounded-2xl bg-gradient-to-tr from-chart-1/10 to-chart-4/10 blur-2xl"
            />
            <div className="overflow-hidden rounded-xl border border-border bg-card shadow-xl">
              <img
                key={current.id}
                src={current.src}
                alt={`${current.label} — ${current.caption}`}
                width={1280}
                height={800}
                loading="lazy"
                className="h-auto w-full"
              />
            </div>
          </div>
          <p className="mt-4 text-center text-sm text-muted-foreground">
            {current.caption}
          </p>
        </div>
      </div>
    </section>
  );
}

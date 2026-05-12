import { Github, BookOpen, Bug, Scale } from "lucide-react";
import { LINKS } from "@/config/site";

export function Footer() {
  return (
    <footer className="bg-background">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="text-lg font-bold text-foreground">Git Logs</div>
            <p className="mt-2 text-sm text-muted-foreground">
              Self-hosted CI/CD dashboard for WordPress.
            </p>
            <p className="mt-4 text-xs text-muted-foreground">
              v0.4.0 · GPL-2.0-or-later
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-foreground">Project</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li>
                <a
                  href={LINKS.github}
                  className="inline-flex items-center gap-1.5 hover:text-foreground"
                >
                  <Github className="h-4 w-4" /> GitHub
                </a>
              </li>
              <li>
                <a
                  href={LINKS.issues}
                  className="inline-flex items-center gap-1.5 hover:text-foreground"
                >
                  <Bug className="h-4 w-4" /> Issues
                </a>
              </li>
              <li>
                <a
                  href={LINKS.releases}
                  className="inline-flex items-center gap-1.5 hover:text-foreground"
                >
                  <BookOpen className="h-4 w-4" /> Releases
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-foreground">Learn</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li>
                <a href="#how-it-works" className="hover:text-foreground">
                  How it works
                </a>
              </li>
              <li>
                <a href="#install" className="hover:text-foreground">
                  Quick start
                </a>
              </li>
              <li>
                <a href="#requirements" className="hover:text-foreground">
                  Requirements
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-foreground">Legal</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li className="inline-flex items-center gap-1.5">
                <Scale className="h-4 w-4" /> WP Plugin: GPL-2.0
              </li>
              <li className="inline-flex items-center gap-1.5">
                <Scale className="h-4 w-4" /> glci CLI: Apache-2.0
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-3 border-t border-border pt-6 text-xs text-muted-foreground sm:flex-row">
          <p>© {new Date().getFullYear()} Git Logs Contributors</p>
          <p>Built with WordPress, Go, and React.</p>
        </div>
      </div>
    </footer>
  );
}

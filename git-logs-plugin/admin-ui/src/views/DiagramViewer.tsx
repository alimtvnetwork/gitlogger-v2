import { useEffect, useState } from "react";
import type { ApiClient, DiagramRow } from "../api/client";
import { ErrorBanner } from "../components/ErrorBanner";

export function DiagramViewer({ api }: { api: ApiClient }) {
  const [items, setItems] = useState<DiagramRow[] | null>(null);
  const [active, setActive] = useState<DiagramRow | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api.get<{ items: DiagramRow[] }>("/admin/diagrams")
      .then((j) => {
        if (cancelled) return;
        const list = j.items ?? [];
        setItems(list);
        setActive(list[0] ?? null);
      })
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => { cancelled = true; };
  }, [api]);

  return (
    <div className="gl-stack">
      {error && <ErrorBanner message={error} />}
      <section className="gl-card">
        <header className="gl-card-head">
          <h2>Diagrams</h2>
          <span className="gl-muted">{items?.length ?? 0} shipped</span>
        </header>
        {items == null ? (
          <p className="gl-empty">Loading…</p>
        ) : items.length === 0 ? (
          <p className="gl-empty">
            No diagrams found. Plugin scans <code>spec/26-gitlogs-diagrams/*.svg</code>.
          </p>
        ) : (
          <div className="gl-diagram-grid">
            <nav aria-label="Diagrams">
              <ul className="gl-list">
                {items.map((d) => (
                  <li key={d.slug}>
                    <button
                      className={`gl-link gl-list-btn ${active?.slug === d.slug ? "is-active" : ""}`}
                      onClick={() => setActive(d)}
                    >
                      {d.title}
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
            <figure className="gl-diagram-stage">
              {active ? (
                <>
                  <object
                    data={active.href}
                    type="image/svg+xml"
                    aria-label={active.title}
                    className="gl-diagram-svg"
                  >
                    <a href={active.href}>{active.title}</a>
                  </object>
                  <figcaption>
                    {active.title}
                    {active.source && (
                      <> · <a className="gl-link" href={active.source}>view source</a></>
                    )}
                  </figcaption>
                </>
              ) : (
                <p className="gl-empty">Select a diagram.</p>
              )}
            </figure>
          </div>
        )}
      </section>
    </div>
  );
}

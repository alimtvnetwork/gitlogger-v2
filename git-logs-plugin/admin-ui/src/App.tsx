import { useEffect, useMemo, useState } from "react";
import { Dashboard } from "./views/Dashboard";
import { RunDetail } from "./views/RunDetail";
import { DiagramViewer } from "./views/DiagramViewer";
import { useApi } from "./api/client";

type Boot = { restRoot: string; nonce: string; version: string };

type Route =
  | { name: "dashboard" }
  | { name: "run"; id: string }
  | { name: "diagrams" };

function parseHash(): Route {
  const h = (typeof window !== "undefined" ? window.location.hash : "").replace(/^#\/?/, "");
  if (h.startsWith("runs/")) return { name: "run", id: decodeURIComponent(h.slice("runs/".length)) };
  if (h === "diagrams") return { name: "diagrams" };
  return { name: "dashboard" };
}

export function App({ boot }: { boot?: Boot }) {
  const [route, setRoute] = useState<Route>(parseHash());

  useEffect(() => {
    const onHash = () => setRoute(parseHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const api = useApi(boot);

  const view = useMemo(() => {
    if (!boot) {
      return (
        <div className="gl-card gl-err-card">
          <h2>Boot data missing</h2>
          <p>The plugin did not localize <code>GitLogsBoot</code>. Refresh the WordPress admin page.</p>
        </div>
      );
    }
    switch (route.name) {
      case "run":
        return <RunDetail api={api} runId={route.id} />;
      case "diagrams":
        return <DiagramViewer api={api} />;
      default:
        return <Dashboard api={api} />;
    }
  }, [route, boot, api]);

  return (
    <div className="gl-admin">
      <header className="gl-header">
        <div className="gl-header-brand">
          <h1>Git Logs</h1>
          <span className="gl-tag">v{boot?.version ?? "?"}</span>
        </div>
        <nav className="gl-nav" aria-label="Primary">
          <a href="#/" className={route.name === "dashboard" ? "is-active" : ""}>Dashboard</a>
          <a href="#/diagrams" className={route.name === "diagrams" ? "is-active" : ""}>Diagrams</a>
        </nav>
      </header>
      <main>{view}</main>
    </div>
  );
}

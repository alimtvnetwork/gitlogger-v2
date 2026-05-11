import { useEffect, useState } from "react";

type Boot = { restRoot: string; nonce: string; version: string };
type HealthResponse = {
  status: string;
  plugin: string;
  plugin_version: string;
  wp_version: string;
  php_version: string;
  rest_namespace: string;
  server_time_utc: string;
};

export function App({ boot }: { boot?: Boot }) {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!boot) {
      setError("GitLogsBoot is not present — plugin did not localize the script.");
      setLoading(false);
      return;
    }
    fetch(`${boot.restRoot}/health`, { headers: { "X-WP-Nonce": boot.nonce } })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((j: HealthResponse) => setData(j))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [boot]);

  return (
    <div className="gl-admin">
      <h1>Git Logs</h1>
      <p className="gl-tag">Phase 1 walking skeleton — plugin v{boot?.version ?? "?"}</p>

      <section className="gl-card">
        <h2>Backend health</h2>
        {loading && <p>Probing /wp-json/git-logs/v1/health…</p>}
        {error && <p className="gl-err">Failed: {error}</p>}
        {data && (
          <dl className="gl-dl">
            <dt>Status</dt><dd>{data.status}</dd>
            <dt>Plugin version</dt><dd>{data.plugin_version}</dd>
            <dt>WordPress</dt><dd>{data.wp_version}</dd>
            <dt>PHP</dt><dd>{data.php_version}</dd>
            <dt>REST namespace</dt><dd><code>{data.rest_namespace}</code></dd>
            <dt>Server time (UTC)</dt><dd>{data.server_time_utc}</dd>
          </dl>
        )}
      </section>
    </div>
  );
}

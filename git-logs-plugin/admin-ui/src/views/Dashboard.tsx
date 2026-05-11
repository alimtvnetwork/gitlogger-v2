import { useEffect, useState } from "react";
import type { ApiClient, RepoRow, RunRow } from "../api/client";
import { StatusBadge } from "../components/StatusBadge";
import { ErrorBanner } from "../components/ErrorBanner";
import { TimeAgo } from "../components/TimeAgo";

export function Dashboard({ api }: { api: ApiClient }) {
  const [repos, setRepos] = useState<RepoRow[] | null>(null);
  const [runs, setRuns] = useState<RunRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      api.get<{ items: RepoRow[] }>("/repos?limit=50").catch(() => ({ items: [] })),
      api.get<{ items: RunRow[] }>("/runs?limit=25").catch(() => ({ items: [] })),
    ])
      .then(([r, ru]) => {
        if (cancelled) return;
        setRepos(r.items ?? []);
        setRuns(ru.items ?? []);
      })
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => { cancelled = true; };
  }, [api]);

  return (
    <div className="gl-stack">
      {error && <ErrorBanner message={error} />}

      <section className="gl-card">
        <header className="gl-card-head">
          <h2>Recent runs</h2>
          <span className="gl-muted">{runs?.length ?? 0} shown</span>
        </header>
        {runs == null ? (
          <SkeletonRows n={5} />
        ) : runs.length === 0 ? (
          <EmptyState>No runs yet. Submit one with <code>glci run</code>.</EmptyState>
        ) : (
          <table className="gl-table">
            <thead>
              <tr>
                <th>Status</th>
                <th>Pipeline</th>
                <th>Branch</th>
                <th>SHA</th>
                <th>Started</th>
                <th>Errors</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {runs.map((r) => (
                <tr key={r.id}>
                  <td><StatusBadge status={r.status} hasError={!!r.has_error} /></td>
                  <td className="gl-mono">{r.pipeline_name}</td>
                  <td>{r.branch}</td>
                  <td className="gl-mono" title={r.git_sha}>{r.git_sha?.slice(0, 7) ?? "—"}</td>
                  <td><TimeAgo iso={r.started_at} /></td>
                  <td>{r.error_count ?? 0}</td>
                  <td><a className="gl-link" href={`#/runs/${encodeURIComponent(r.id)}`}>Open →</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className="gl-card">
        <header className="gl-card-head">
          <h2>Repositories</h2>
          <span className="gl-muted">{repos?.length ?? 0}</span>
        </header>
        {repos == null ? (
          <SkeletonRows n={3} />
        ) : repos.length === 0 ? (
          <EmptyState>No repositories registered yet.</EmptyState>
        ) : (
          <ul className="gl-list">
            {repos.map((r) => (
              <li key={r.id} className="gl-list-row">
                <div>
                  <div className="gl-mono">{r.url}</div>
                  {r.root_repo && r.root_repo !== r.url && (
                    <div className="gl-muted">root: {r.root_repo}</div>
                  )}
                </div>
                <div className="gl-muted"><TimeAgo iso={r.last_run_at ?? r.created_at} /></div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function SkeletonRows({ n }: { n: number }) {
  return (
    <div className="gl-skeleton-stack" aria-busy="true">
      {Array.from({ length: n }).map((_, i) => (
        <div key={i} className="gl-skeleton-row" />
      ))}
    </div>
  );
}

function EmptyState({ children }: { children: React.ReactNode }) {
  return <p className="gl-empty">{children}</p>;
}

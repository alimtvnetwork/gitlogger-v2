import { useEffect, useRef, useState } from "react";
import type { ApiClient, RunEvent, RunRow } from "../api/client";
import { StatusBadge } from "../components/StatusBadge";
import { ErrorBanner } from "../components/ErrorBanner";
import { TimeAgo } from "../components/TimeAgo";

export function RunDetail({ api, runId }: { api: ApiClient; runId: string }) {
  const [run, setRun] = useState<RunRow | null>(null);
  const [events, setEvents] = useState<RunEvent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [follow, setFollow] = useState(true);
  const [filter, setFilter] = useState<"all" | "warn" | "error">("all");
  const sinceRef = useRef<number>(0);

  useEffect(() => {
    let cancelled = false;
    api.get<{ item: RunRow }>(`/runs/${encodeURIComponent(runId)}`)
      .then((j) => !cancelled && setRun(j.item ?? (j as any)))
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => { cancelled = true; };
  }, [api, runId]);

  useEffect(() => {
    let cancelled = false;
    let timer: number | undefined;

    const tick = async () => {
      try {
        const j = await api.get<{ items: RunEvent[] }>(
          `/runs/${encodeURIComponent(runId)}/events?since=${sinceRef.current}&limit=500`
        );
        const items = j.items ?? [];
        if (items.length > 0 && !cancelled) {
          sinceRef.current = items[items.length - 1].id;
          setEvents((prev) => [...prev, ...items]);
        }
      } catch (e) {
        if (!cancelled) setError((e as Error).message);
      }
      if (!cancelled && follow) {
        timer = window.setTimeout(tick, 2000);
      }
    };

    tick();
    return () => {
      cancelled = true;
      if (timer) window.clearTimeout(timer);
    };
  }, [api, runId, follow]);

  const visible = events.filter((e) => filter === "all" || e.level === filter);

  return (
    <div className="gl-stack">
      <a className="gl-link" href="#/">← Dashboard</a>
      {error && <ErrorBanner message={error} />}

      <section className="gl-card">
        <header className="gl-card-head">
          <div>
            <h2>Run <span className="gl-mono">{runId.slice(0, 8)}</span></h2>
            {run && (
              <p className="gl-muted">
                {run.pipeline_name} · {run.branch} · <span className="gl-mono">{run.git_sha?.slice(0, 7)}</span>
              </p>
            )}
          </div>
          {run && <StatusBadge status={run.status} hasError={!!run.has_error} />}
        </header>
        {run && (
          <dl className="gl-dl">
            <dt>Started</dt><dd><TimeAgo iso={run.started_at} /></dd>
            <dt>Ended</dt><dd><TimeAgo iso={run.ended_at} /></dd>
            <dt>Errors</dt><dd>{run.error_count ?? 0}</dd>
            <dt>Warnings</dt><dd>{run.warn_count ?? 0}</dd>
          </dl>
        )}
      </section>

      <section className="gl-card">
        <header className="gl-card-head">
          <h2>Event stream</h2>
          <div className="gl-toolbar">
            <label className="gl-checkbox">
              <input type="checkbox" checked={follow} onChange={(e) => setFollow(e.target.checked)} />
              Live follow
            </label>
            <div role="tablist" className="gl-tabs">
              {(["all", "warn", "error"] as const).map((k) => (
                <button
                  key={k}
                  role="tab"
                  aria-selected={filter === k}
                  className={filter === k ? "is-active" : ""}
                  onClick={() => setFilter(k)}
                >
                  {k}
                </button>
              ))}
            </div>
          </div>
        </header>
        {visible.length === 0 ? (
          <p className="gl-empty">No events yet.</p>
        ) : (
          <ol className="gl-events">
            {visible.map((e) => (
              <li key={e.id} className={`gl-event gl-event-${e.level}`}>
                <span className="gl-event-ts gl-mono">{shortTs(e.ts)}</span>
                <span className="gl-event-level">{e.level}</span>
                <span className="gl-event-line">{e.line}</span>
                {e.file_path && <span className="gl-event-path">{e.file_path}</span>}
              </li>
            ))}
          </ol>
        )}
      </section>
    </div>
  );
}

function shortTs(iso: string): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toISOString().slice(11, 23);
}

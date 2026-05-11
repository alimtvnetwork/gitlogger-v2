export function TimeAgo({ iso }: { iso?: string | null }) {
  if (!iso) return <span className="gl-muted">—</span>;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return <span className="gl-muted">{iso}</span>;
  const diff = Date.now() - d.getTime();
  const abs = Math.abs(diff);
  const min = 60_000, hr = 60 * min, day = 24 * hr;
  let txt: string;
  if (abs < min) txt = "just now";
  else if (abs < hr) txt = `${Math.round(abs / min)}m ago`;
  else if (abs < day) txt = `${Math.round(abs / hr)}h ago`;
  else txt = `${Math.round(abs / day)}d ago`;
  return <time dateTime={iso} title={d.toISOString()}>{txt}</time>;
}

import type { RunRow } from "../api/client";

export function StatusBadge({
  status,
  hasError,
}: {
  status: RunRow["status"];
  hasError?: boolean;
}) {
  const tone =
    status === "passed" && !hasError ? "ok"
    : status === "failed" || status === "errored" || hasError ? "err"
    : status === "running" ? "info"
    : "muted";
  return <span className={`gl-badge gl-badge-${tone}`}>{status}</span>;
}

import { useMemo } from "react";

export type Boot = { restRoot: string; nonce: string; version: string };

export type ApiClient = {
  get: <T>(path: string) => Promise<T>;
  post: <T>(path: string, body: unknown) => Promise<T>;
};

export type RepoRow = {
  id: number;
  url: string;
  root_repo?: string;
  created_at?: string;
  last_run_at?: string | null;
};

export type RunRow = {
  id: string;
  repo_id: number;
  repo_url?: string;
  branch: string;
  pipeline_name: string;
  git_sha: string;
  status: "queued" | "running" | "passed" | "failed" | "errored";
  has_error: 0 | 1;
  error_count?: number;
  warn_count?: number;
  started_at?: string | null;
  ended_at?: string | null;
};

export type RunEvent = {
  id: number;
  ts: string;
  level: "info" | "warn" | "error";
  line: string;
  file_path?: string | null;
};

export type DiagramRow = {
  slug: string;
  title: string;
  href: string;     // SVG URL relative to restRoot
  source?: string;  // .mmd source URL (optional)
};

class ApiError extends Error {
  status: number;
  code?: string;
  constructor(status: number, msg: string, code?: string) {
    super(msg);
    this.status = status;
    this.code = code;
  }
}

export function useApi(boot?: Boot): ApiClient {
  return useMemo<ApiClient>(() => {
    const root = boot?.restRoot ?? "";
    const headers: HeadersInit = boot?.nonce ? { "X-WP-Nonce": boot.nonce } : {};
    const handle = async (r: Response) => {
      const text = await r.text();
      const json = text ? safeJSON(text) : null;
      if (!r.ok) {
        const code = (json && (json.code || json.ErrorCode)) || undefined;
        const msg = (json && (json.message || json.Message)) || `HTTP ${r.status}`;
        throw new ApiError(r.status, msg, code);
      }
      return json;
    };
    return {
      get: async <T,>(path: string) => {
        const r = await fetch(`${root}${path}`, { headers });
        return (await handle(r)) as T;
      },
      post: async <T,>(path: string, body: unknown) => {
        const r = await fetch(`${root}${path}`, {
          method: "POST",
          headers: { ...headers, "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        return (await handle(r)) as T;
      },
    };
  }, [boot]);
}

function safeJSON(text: string): any | null {
  try { return JSON.parse(text); } catch { return null; }
}

export { ApiError };

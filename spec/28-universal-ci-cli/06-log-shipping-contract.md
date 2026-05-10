# Log Shipping Contract

**Version:** 1.1.1  
**Updated:** 2026-05-10  
**Server contract:** [`spec/22-git-logs-v2/04-rest-api-endpoints.md`](../22-git-logs-v2/04-rest-api-endpoints.md)

The CLI is a *client* of Git Logs v2. Wire shapes here MUST stay byte-compatible with the server spec — when they conflict, the server wins and this file is patched.

---

## Endpoint Mapping

| CLI event | HTTP | v2 endpoint | Trigger |
|-----------|------|-------------|---------|
| Phase finished, logs to deliver | `POST` | `/append-log` | Always (unless `--no-push`) |
| Phase passed AND server says previous run had `HasError=1` | `PUT`  | `/fixed-log` | Automatic post-success check |
| `glci clear --pipeline X` | `POST` | `/clear-log` | Manual |
| `glci clear --all` | `POST` | `/clear-log-all` | Manual |
| `glci doctor` reachability ping | `GET`  | `/get-logs?q=<repo>&limit=0` | Pre-flight only |

`/get-pipeline-logs`, `/get-error-logs`, `/get-pipeline-error-logs` are read endpoints owned by humans/admin UI; the CLI does NOT call them in any phase.

---

## Batched Mode (default)

One POST per `(Runtime, Phase)`. Body = full payload from §22 `/append-log`:

```json
{
  "RepoUrl":      "https://github.com/org/repo",
  "RootRepo":     "https://github.com/org/repo",
  "Branch":       "main",
  "TempToken":    "…",
  "Token":        "…",
  "PipelineName": "ts-test",
  "GitSha256":    "abc123…",
  "Logs":         ["line 1", "line 2", "..."],
  "ErrorLogs":    ["FAIL test/foo.spec.ts > should compile"],
  "FilePaths":    ["test/foo.spec.ts"],
  "HasError":     true
}
```

Field rules:

- `Logs[]` cap: `batch_max_bytes` (default 1 MiB) total UTF-8. Lines beyond cap are dropped and `ErrorLogs[]` gains a synthetic `"GLCI: log truncated, N lines dropped"`.
- `ErrorLogs[]` cap: same; dropped lines counted in same synthetic line.
- `FilePaths[]` derived from §09 classifier; deduplicated; max 100 entries.
- `HasError` is **true iff** `ErrorLogs[]` is non-empty OR runner exit code ≠ 0.
- `GitSha256` must be a real commit SHA — when unset, exit `2` with `GLCI-PUSH-NO-SHA`.

Retry on `5xx`/network: exponential backoff per `push.backoff_ms`. After `max_retries`, exit `4` with `GLCI-PUSH-RETRIES-EXHAUSTED`.

Retry on `4xx`: **never**. Surface server's `ErrorCode` directly and exit `3`.

---

## Request Timeout & Retry Discipline (Normative)

**Verifying AC:** [§97 AC-28-48](./97-acceptance-criteria.md#ac-28-48--log-shipping-per-request-timeout--max-wall-clock-cap-normative).

Every HTTP request to `/append-log`, `/fixed-log`, `/get-logs`, `/profile/me` MUST be bounded by **two independent timeouts**:

| Bound | Constant | Default | Configurable via | Forbidden value |
|---|---|---:|---|---|
| Per-attempt wall-clock | `PUSH_REQUEST_TIMEOUT_MS` | `30000` (30 s) | `glci.toml` `push.request_timeout_ms` | `0`, negative, `>120000` |
| Total ship-cycle wall-clock (all retries combined) | `PUSH_TOTAL_DEADLINE_MS` | `180000` (3 min) | `glci.toml` `push.total_deadline_ms` | `0`, negative, `<= request_timeout_ms` |

**Retry envelope:** retries on `5xx`/network errors use exponential backoff seeded by `push.backoff_ms` (default `1000`) with **±25% jitter** — `delay_n = backoff_ms * 2^n * (0.75 + rand()*0.5)` — capped at `max_retries` (default `5`). The retry loop discipline mirrors **[`spec/27-spec-toolchain` §97 AC-T-28 R3](../27-spec-toolchain/97-acceptance-criteria.md)** (link, do not restate per Lesson #36).

**Termination triggers** (closed enumeration; first match wins):

1. Server returned `2xx` → success (clean exit `0`).
2. Server returned `4xx` → exit `3` with server's `ErrorCode` verbatim (no retry).
3. `max_retries` exhausted → exit `4` with `GLCI-PUSH-RETRIES-EXHAUSTED`.
4. `PUSH_TOTAL_DEADLINE_MS` reached mid-retry → exit `4` with `GLCI-PUSH-DEADLINE-EXCEEDED` (NEW — distinct from retries-exhausted because the budget, not the count, was the limit).
5. Per-attempt `PUSH_REQUEST_TIMEOUT_MS` reached → request cancelled, counted as one network failure (feeds rule 3 or 4).

**FORBIDDEN patterns:**

- Unbounded `http.Client` (Go) / `axios.create()` without `timeout` (TS) / Guzzle without `connect_timeout`+`timeout` (PHP) / `reqwest::Client::builder()` without `.timeout()` (Rust) / `HttpClient` without `Timeout` (C#) — every runtime stub MUST set BOTH per-attempt AND total deadline.
- Treating timeout as a `4xx`-class error (skips retry).
- Retrying after `PUSH_TOTAL_DEADLINE_MS` is exceeded (the deadline is hard).
- Streaming-mode (`--stream`) requests skipping the deadline (the chunked transfer MUST also honour `PUSH_TOTAL_DEADLINE_MS`; stream-aborts mid-chunk surface as `GLCI-PUSH-DEADLINE-EXCEEDED`).

---

## Streaming Mode (`--stream`)

```http
POST /append-log HTTP/1.1
Transfer-Encoding: chunked
Content-Type: application/x-ndjson
X-GL-Stream: 1

{"RepoUrl":"…","Branch":"…","TempToken":"…","Token":"…","PipelineName":"ts-test","GitSha256":"…","StreamHeader":true}
{"Line":"line 1"}
{"Line":"line 2"}
{"Line":"FAIL test/foo.spec.ts","IsError":true,"FilePath":"test/foo.spec.ts"}
{"StreamFooter":true,"HasError":true}
```

- First chunk MUST carry `StreamHeader=true` plus identity fields.
- Each subsequent chunk MUST be one valid JSON object terminated by `\n`.
- Final chunk MUST carry `StreamFooter=true` plus the resolved `HasError`.
- Server returns standard ack envelope after the final chunk; CLI parses and treats it identically to batched mode.
- Buffer cap: `max_buffer_lines` lines kept in memory; if the channel blocks (slow server), oldest non-error lines are dropped first and a `"GLCI: stream backpressure dropped N lines"` synthetic line is inserted before the next sent chunk.

Streaming and batched modes are mutually exclusive per invocation. Mixing per-phase is not supported in v1.

---

## `/fixed-log` Auto-Detection

After a phase passes, the orchestrator MAY emit `PUT /fixed-log` iff:

1. The previous run for `(RepoUrl, Branch, PipelineName)` had `HasError=1`, AND
2. The current run had zero `ErrorLogs[]`, AND
3. The runner exit code is 0.

Discovery of "previous run had `HasError=1`" uses the **server response** to the most recent `/append-log` POST — the v2 server's ack envelope SHOULD include `PreviousHasError` per `spec/22-git-logs-v2/04-rest-api-endpoints.md`. If the server omits this field, the CLI does NOT call `/fixed-log` (no local cache).

> **Open server-side dependency:** v2 ack envelope currently lacks `PreviousHasError`. Tracked as gap **GAP-22-04** in [`spec/22-git-logs-v2/99-consistency-report.md`](../22-git-logs-v2/99-consistency-report.md).

---

## Auth Lane Selection

Maps directly to v2 `X-GL-Auth-Mode`:

| `auth_mode` | Headers | Body fields | v2 lane |
|-------------|---------|-------------|---------|
| `temptoken` | _(none added)_ | `TempToken`, `Token` | Lane B / TempToken sub-mode |
| `ssh` | `X-GL-Auth-Mode: ssh`, `X-GL-Fingerprint`, `X-GL-Timestamp`, `X-GL-Nonce`, `X-GL-Signature` | `TempToken`/`Token` MUST NOT appear (else server returns `GL-SSH-LANE-CONFLICT`) | Lane B / SSH sub-mode |

Signing string for SSH mode is `GL-SSHSIG-V1` per `spec/22-git-logs-v2/05-auth-and-validation.md` step 8 — the CLI shells out to `ssh-keygen -Y sign -n git-logs@v2` for portability.

### Worked Example — SSH-mode signed request (Normative reference)

End-to-end transcript a contributor can replay locally. All values are deterministic given the inputs; only `X-GL-Nonce` and `X-GL-Timestamp` are environment-dependent.

**Inputs:**

- Private key: `~/.ssh/id_ed25519` (Ed25519, fingerprint `SHA256:abc123…XYZ`)
- Endpoint: `POST https://logs.example.test/api/v2/runs`
- Canonical body (after AC-28-08 sort/dedup, before signing — see AC-28-23):

```json
{"Branch":"main","CommitSha":"a1b2c3","ErrorLogs":[],"FilePaths":["app.go","main.go"],"GitSha256":"deadbeef","Logs":[{"Phase":"go.test","Line":"PASS","Ts":"2026-05-10T12:00:00.001Z"}],"PipelineName":"glci","RepoUrl":"https://github.com/acme/repo"}
```

**Step 1 — Compute headers (CLI):**

```text
X-GL-Auth-Mode: ssh
X-GL-Fingerprint: SHA256:abc123…XYZ
X-GL-Timestamp:   2026-05-10T12:00:00Z      # RFC3339 UTC, second precision
X-GL-Nonce:       7f3a9c1e2b8d4f60          # 16 hex chars, crypto/rand
```

**Step 2 — Build signing string `GL-SSHSIG-V1` (per spec/22 §05 step 8):**

```text
GL-SSHSIG-V1\n
POST\n
/api/v2/runs\n
2026-05-10T12:00:00Z\n
7f3a9c1e2b8d4f60\n
sha256:<hex(sha256(canonical_body))>\n
```

**Step 3 — Sign via `ssh-keygen` (portable, no Go/Rust crypto deps):**

```bash
printf '%s' "$SIGNING_STRING" \
  | ssh-keygen -Y sign -n git-logs@v2 -f ~/.ssh/id_ed25519 \
  | base64 -w0
# => SSHSIG_BASE64 (single line, ~600 chars)
```

The CLI MUST invoke `ssh-keygen` as a subprocess (not link `libssh`) — see AC-28-09 `**Verifies:**` clause and the SSH-key Lane B contract in `mem://specs/git-logs`.

**Step 4 — Attach signature header & POST:**

```text
X-GL-Signature: <SSHSIG_BASE64>
Content-Type: application/json
…canonical body from Step 1…
```

**Step 5 — Server response (success):**

```text
HTTP/1.1 201 Created
{"RunId":"01HXYZ…","Accepted":true}
```

**Forbidden (each violates AC-28-09 / spec/22 §05):**

- `TempToken` field present in body alongside SSH headers → server returns `GL-SSH-LANE-CONFLICT` (HTTP 409).
- Re-signing a *modified* body (e.g. retry mutates `Logs[]`) → server returns `GL-SSH-SIG-INVALID` (HTTP 401); CLI MUST re-canonicalize and re-sign on every retry.
- Reusing a `(Fingerprint, Nonce)` pair within the server's replay window → server returns `GL-SSH-NONCE-REUSED` (HTTP 401).
- Clock skew > 300 s vs server `Date:` header → server returns `GL-SSH-TIMESTAMP-WINDOW`; `glci doctor` MUST flag this pre-run per AC-28-16.

This block is illustrative (kind: example). The normative contract lives in AC-28-09 (this module) and `spec/22-git-logs-v2/05-auth-and-validation.md` step 8 (cross-module — Lesson #36: link, never restate).

---

## Determinism

Two consecutive `glci run` invocations on the same commit, same env, same source MUST emit byte-identical request bodies (modulo `GitSha256` if HEAD changed). Specifically:

- `Logs[]` order reflects exec capture order, not goroutine scheduling.
- `FilePaths[]` is sorted lexicographically.
- JSON key order is insertion order from the typed struct (Go default with `encoding/json`).

Tests for this contract live in `spec/22-git-logs-v2/32-cli-test-plan.md` and the BATS skeleton at `spec/22-git-logs-v2/33-bats-test-skeleton.md` (the old §22 `16-test-plan.md` was relocated to `38-test-plan-superseded.md` in Phase P5; do not link to the legacy slot).

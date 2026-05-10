# Error Code Catalog (v2)

**Version:** 2.9.4  
**Updated:** 2026-04-28 (Phase P16: §15/§17/§97 lockstep for the 4 `GL-STREAM-*` ingest-streaming codes deferred from Phase P2 — codes promoted from §04 §1.2 prose into this catalog so `ErrorResponder.php` and the `ErrorCode` enum have a single canonical source.)

All `GL-*` codes returned by the plugin. Codes are stable strings (constants in `inc/Support/ErrorCodes.php`). Adding a new code requires a row here.

---

## Authentication (Lane A — admin/read)

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-AUTH-WP-MISSING | 401 | No WP App Password / cookie present. | Authenticate via Application Password. |
| GL-AUTH-WP-INVALID | 401 | App Password rejected by WP. | Regenerate App Password in WP admin. |
| GL-AUTH-NOT-LOGGED-IN | 401 | `wp_get_current_user()` returned 0 (no resolved user). | Authenticate first. |
| GL-AUTH-PROFILE-NOT-LINKED | 403 | WP user has no matching `Profile.UserName`. | Admin must create the Profile in plugin UI. |
| GL-AUTH-NO-PROFILE-LINK | 403 | No `Profile.Email` matches `wp_user.user_email`. | Provision a Git Logs Profile with the same email. |
| GL-AUTH-PROFILE-SUSPENDED | 403 | Lane A: matched Profile has `UserStatusId != Active`. | Re-activate Profile in admin. |
| GL-AUTH-WRONG-LANE | 400 | Lane B credential (TempToken in body) sent to a Lane A read endpoint, or vice versa. | Use the correct lane per `25-headless-auth-notes.md`. |
| GL-AUTHZ-PERMISSION-DENIED | 403 | Profile's `RolePermission` union lacks the required Permission. | Grant via AccessToRoles screen. |

## Authentication (Lane B — CI/CD writes)

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-AUTH-TEMPTOKEN-INVALID | 401 | `TempToken` matches no Profile. | Rotate TempToken in Profile UI; re-issue to CI. |
| GL-AUTH-TOKEN-MISMATCH | 401 | `Token` doesn't match the same Profile that owns the matched `TempToken`. | Update CI secrets. |
| GL-AUTH-PROFILE-INACTIVE | 403 | Profile `UserStatus` ∈ {Suspended, Revoked}. | Re-activate Profile in admin. |
| GL-APP-NOT-ACTIVE | 403 | Linked `App.AppStatus` ∈ {Disabled, Archived}. | Set App back to Active or unlink. |

## Authentication (Lane B — SSH sub-mode, preferred from v2.7.0)

Validation order fixed by §31 (steps 1–10). See [`31-ssh-key-auth.md`](./31-ssh-key-auth.md) for canonical signing string and payload shape.

| Code | HTTP | Step | Cause | Caller action |
|------|------|------|-------|---------------|
| GL-SSH-HEADER-MISSING | 400 | 2 | One of `X-GL-Fingerprint`, `X-GL-Timestamp`, `X-GL-Nonce`, `X-GL-Signature` absent. | Re-run signer; ensure all four headers set. |
| GL-SSH-TIMESTAMP-SKEW | 401 | 3 | `\|now − X-GL-Timestamp\| > ReplayWindowSeconds`. | Sync runner clock (NTP). |
| GL-SSH-KEY-UNKNOWN | 401 | 4 | No `SshKey` row matches `Fingerprint`. | Register the public key on the target Repo. |
| GL-SSH-KEY-INACTIVE | 403 | 4 | `SshKey.IsActive=0`. | Re-activate or rotate to a new key. |
| GL-SSH-REPO-MISMATCH | 403 | 5 | Parsed `RepoId` ≠ `SshKey.RepoId` (deploy-key binding). | Use a key registered on this Repo. |
| GL-SSH-NONCE-REUSED | 401 | 7 | `(SshKeyId, Nonce)` already seen within `ReplayWindowSeconds`. | Generate a fresh ≥16-byte nonce per request. |
| GL-SSH-SIGNATURE-INVALID | 401 | 8 | `ssh-keygen -Y verify` failed against canonical `GL-SSHSIG-V1` string. | Confirm namespace `git-logs@v2`, body hash, header values match signed payload. |
| GL-SSH-LANE-CONFLICT | 400 | mode parse | `X-GL-Auth-Mode: ssh` AND body `TempToken` both present. | Pick one lane. |
| GL-AUTH-LANE-DISABLED | 403 | mode parse | TempToken submitted while `ConfigKv.SshAuthMode = required`. | Switch CI to SSH lane. |

## Validation (Lane B body inputs)

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-VALIDATION-PROFILE-NOT-FOUND | 404 | No `GitProfile` row for `(Provider, OwnerName)` parsed from `RepoUrl`. | Add the GitProfile in admin. |
| GL-VALIDATION-REPO-NOT-ALLOWED | 403 | `Acceptance` rule rejected the repo (`AcceptSelectedRepoOnly` mismatch or version mismatch). | Adjust GitProfile Acceptance or push from the allowed repo. |
| GL-VALIDATION-BRANCH-RESTRICTED | 403 | `IsRestrictInBranch=1` and inbound `Branch` ≠ `StrictBranch`. | Push from allowed branch or relax restriction. |
| GL-VALIDATION-REPOURL-MALFORMED | 400 | `RepoUrl` failed parser (no provider/owner/repo). | Fix CI variable. |
| GL-VALIDATION-MISSING-FIELD | 400 | Required body field absent (e.g., `RepoUrl`, `Branch`). | Add field. |
| GL-VALIDATION-FIELD-TYPE | 400 | Field present but wrong type (e.g., `HasError` not bool). | Fix payload. |

## Rate limiting + payload (Lane B)

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-PAYLOAD-TOO-LARGE | 413 | `Content-Length` > `MaxPushPayloadBytes` (default 1 MiB). | Split push or increase config. |
| GL-LINES-TOO-MANY | 413 | `len(Logs) + len(ErrorLogs)` > `MaxLinesPerPush` (default 10000). | Split push. |
| GL-RATE-LIMIT-EXCEEDED | 429 | Per-Profile token bucket empty. Response includes `Retry-After`. | Wait per `Retry-After` then retry. |

> Per-line oversize is **not** an error: the server truncates and tags the line with `LogSeverity=Warn`. No GL- code returned.

## Read endpoints (Lane A)

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-READ-CURSOR-INVALID | 400 | `Cursor` opaque string failed decode. | Drop cursor and start fresh. |
| GL-READ-PIPELINE-NOT-FOUND | 404 | `PipelineId` not in DB. | Verify ID. |
| GL-READ-LIMIT-OUT-OF-RANGE | 400 | `Limit` < 1 or > 1000. | Use 1–1000. |

## Operational

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-DB-UNAVAILABLE | 503 | SQLite open failed (file lock, FS error). | Retry; check WP error log. |
| GL-MIGRATION-PENDING | 503 | Plugin booting; migration not yet applied. | Retry after a few seconds. |
| GL-CONFIG-MISSING | 500 | Required `ConfigKv` key absent (corrupted DB). | Re-run activator. |
| GL-INTERNAL | 500 | Unhandled exception. `RequestId` correlates with WP error log. | Report to maintainer with `RequestId`. |

## Per-SHA log storage (split-DB — see §39)

Codes raised by the per-SHA SQLite handle pool when reading/writing `<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db`. Path resolved from `ShaRegistry.DbFilePath`.

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-SHA-DB-OPEN-FAILED | 503 | Per-SHA `.db` file exists in `ShaRegistry` but cannot be opened (FS error, permissions, locked by another process). | Retry; check FS perms on `<ShaLogsRoot>` tree. |
| GL-SHA-DB-CREATE-FAILED | 500 | First-write to a new SHA: cannot create the `.db` file or its `<Sha[0:2]>` shard folder (disk full, EROFS, EACCES). | Free disk; verify the data dir is writable. |
| GL-SHA-DB-CHECKSUM-MISMATCH | 500 | At backup/restore or scheduled audit: stored `Sha256` in `ShaRegistry` does not match recomputed file hash. | Restore from backup; quarantine the file; do not return partial logs. |
| GL-SHA-DB-QUOTA-EXCEEDED | 507 | Open-handle pool already at `MaxOpenShaDbHandles` and no idle handle is older than `ShaDbIdleCloseSec`; pool refused a new open. | Retry; tune `MaxOpenShaDbHandles` / `ShaDbIdleCloseSec` in `ConfigKv`. |

---

## NDJSON streaming retrieval (see §04 §11)

Codes specific to the `Accept: application/x-ndjson` opt-in streaming mode for read endpoints #5/#6/#7/#8/#9/#10. Both codes can appear either as a mid-stream `Error` frame (when the connection is still open and at least the `Header` frame has flushed) or as a conventional JSON envelope (when the failure happens before any frame is emitted).

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-NDJSON-CLIENT-DISCONNECT | 499 | **Informational, server-only audit.** Mid-stream the client closed the TCP connection (EPIPE/ECONNRESET detected within 1 flush cycle per §04 §11.4 step 4). The server returns the per-SHA handle to the AC-52 LRU pool, abandons the cursor, and writes one `AuditTrail` row with this code. **No `Error` frame is sent** — the socket is gone. The 499 status is recorded in access logs only; clients never observe it. | None — this is an audit-side code. To resume from the last successfully delivered row, re-issue the request with `?after-seq=<Seq of last received Log/ErrorLog frame>` per §04 §11.6. |
| GL-NDJSON-CURSOR-LOST | 500 | A `?after-seq=N` resume request (or a fresh stream that internally crossed a SHA boundary) found that the per-SHA `.db` file referenced by the original cursor has been pruned (AC-53) or the `ShaRegistry` row is gone. The server cannot satisfy the requested `Seq` range. Wire shape per §04 §11.6: `Header` → `Error{Code:"GL-NDJSON-CURSOR-LOST"}` → `End{Status:"Error"}`. | Discard the cursor and re-issue without `?after-seq=`; accept that rows in the lost SHA window are unrecoverable from logs alone (per §22 retention contract — pruning is expected). |

## Streaming ingest (Lane B — see §04 §1.2)

Codes specific to the opt-in NDJSON ingest mode on `POST /append-log` activated by request header `X-GL-Stream: 1` + `Content-Type: application/x-ndjson; charset=utf-8` + `Transfer-Encoding: chunked`. All four are buffered JSON envelope rejects (NOT mid-stream `Error` frames) — ingest streaming response is buffered per §04 §1.2; clients always observe the standard `ErrorEnvelope` shape. Frame contract: exactly-one `StreamHeader` (first), zero-or-more `Line`, exactly-one `StreamFooter` (last). Cap `NdjsonMaxRowsPerStream` is shared with retrieval streaming (§11.4) — same backpressure ceiling for ingest and read.

| Code | HTTP | Cause | Caller action |
|------|------|-------|---------------|
| GL-STREAM-NO-HEADER | 400 | `StreamHeader` frame missing, malformed, or arrived after a `Line` frame. Server validates `StreamHeader` BEFORE processing any `Line` frames (§04 §1.2 step 1). All buffered inserts (none yet at this point) MUST be rolled back. | Re-issue the request with a well-formed `StreamHeader` as the first NDJSON line. Do not interleave `Line` frames before the header. |
| GL-STREAM-NO-FOOTER | 400 | EOF arrived before a `StreamFooter` frame (client closed body or network truncation). Server MUST roll back any partial inserts made from `Line` frames already consumed in the same request. | Re-issue the request and ensure the client flushes the closing `{"StreamFooter":true,"HasError":<bool>}` frame before closing the body. |
| GL-STREAM-TOO-MANY-LINES | 413 | Line count in the active stream exceeded `NdjsonMaxRowsPerStream` (§11.4 retrieval cap, intentionally reused for ingest backpressure). Server stops reading and rolls back. | Split the run into multiple `/append-log` requests, OR raise `NdjsonMaxRowsPerStream` in `ConfigKv` if the deployment can sustain the higher buffer. |
| GL-STREAM-UNKNOWN-FRAME | 400 | An NDJSON frame's leading discriminator key was none of `StreamHeader` / `Line` / `StreamFooter`. Forward-compat rule: server MUST ignore *unknown keys* inside a recognized frame, but MUST reject frames whose *discriminator* itself is unrecognized (e.g. `{"Foo":true,…}`). | Bring the client up to a frame schema the server understands, OR remove the unrecognized frame. The discriminator MUST be a literal boolean `true` value of one of the three recognized keys. |

## Envelope (recap)

Every reject returns:

```json
{
  "Status": "Error",
  "Code": "GL-…",
  "Message": "human-readable",
  "RequestId": "req_…",
  "HttpStatus": <int>
}
```

`RequestId` is also written to `AuditTrail.RequestId` for any reject — operators can grep both sides.

---

## Adding a new code

1. Append a row to the relevant section above.
2. Add a constant in `inc/Support/ErrorCodes.php`.
3. Wire `inc/Rest/ErrorResponder.php` to map it to the listed HTTP status.
4. Bump `98-changelog.md`.

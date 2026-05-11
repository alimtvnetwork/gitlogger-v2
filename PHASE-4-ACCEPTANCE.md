# Phase 4 — Public REST Surface + OpenAPI (Acceptance)

Adds the full read/write REST API for repos, runs, events, audit, and admin.

## Endpoint matrix

| Method | Path | Auth | Phase |
|--------|------|------|-------|
| GET    | `/health`                       | public | P1 |
| GET    | `/whoami`                       | user   | P2 |
| GET    | `/keys`                         | user   | P2 |
| POST   | `/keys`                         | user   | P2 |
| DELETE | `/keys/{id}`                    | user   | P2 |
| GET    | `/repos`                        | user   | **P4** |
| POST   | `/repos`                        | user   | **P4** |
| GET    | `/runs`                         | user   | **P4** |
| POST   | `/runs`                         | user   | **P4** |
| GET    | `/runs/{id}`                    | user   | **P4** |
| POST   | `/runs/{id}/events`             | user   | **P4** |
| GET    | `/runs/{id}/events`             | user   | **P4** |
| POST   | `/runs/{id}/finalize`           | user   | **P4** |
| GET    | `/audit`                        | admin  | **P4** |
| GET    | `/admin/migrate`                | admin  | P3 |
| POST   | `/admin/migrate`                | admin  | P3 |
| POST   | `/admin/gc`                     | admin  | **P4** |

**14 endpoints total**, all defined in `git-logs-plugin/openapi.yaml` (mirrored to `glci/internal/api/openapi.yaml`).

## Components shipped in P4

| File | Purpose |
|------|---------|
| `includes/rest/class-rest-repos.php` | GET list / POST upsert |
| `includes/rest/class-rest-runs.php` | create + fetch + list + events POST/GET + finalize |
| `includes/rest/class-rest-audit.php` | admin-only audit reader |
| `includes/rest/class-rest-admin-gc.php` | per-SHA SQLite GC with `dry_run` |
| `openapi.yaml` | OpenAPI 3.0 contract for all 14 routes |
| `glci/internal/api/openapi.yaml` | 1:1 mirror for client codegen |
| `glci/internal/api/README.md` | mirror policy |

## Idempotency contracts

- `POST /repos` — idempotent on `slug` (upsert).
- `POST /runs/{id}/events` — `INSERT OR IGNORE (run_id, seq)` makes batch retries safe.
- `POST /admin/migrate` — already-applied migrations are skipped.
- `POST /admin/gc` — defaults to `dry_run=true`; pass `{"dry_run":false}` to actually delete.

## Acceptance checklist

### 1. End-to-end happy path
```bash
BASE=https://your-site.test/wp-json/git-logs/v1
AUTH='-u alice:XXXX YYYY ZZZZ AAAA'

# Upsert repo
curl -s $AUTH -X POST $BASE/repos -H 'Content-Type: application/json' \
  -d '{"slug":"acme/web","display_name":"Acme Web"}'
# expect: {"id":1,"slug":"acme/web"}

# Create run
RUN=$(curl -s $AUTH -X POST $BASE/runs -H 'Content-Type: application/json' \
  -d '{"repo_slug":"acme/web","branch":"main","sha":"'"$(printf 'a%.0s' {1..40})"'","ci_provider":"local"}' | jq -r .id)
echo "run=$RUN"

# Append events
curl -s $AUTH -X POST "$BASE/runs/$RUN/events" -H 'Content-Type: application/json' \
  -d '{"events":[
    {"seq":1,"ts_utc":"2026-05-11T00:00:00Z","stream":"stdout","phase":"build","severity":"info","message":"hello"},
    {"seq":2,"ts_utc":"2026-05-11T00:00:01Z","stream":"stderr","phase":"build","severity":"error","message":"boom"}
  ]}'
# expect: {"appended":2,"errors":1,"warns":0}

# Read events
curl -s $AUTH "$BASE/runs/$RUN/events?after_seq=0&limit=10"

# Finalize
curl -s $AUTH -X POST "$BASE/runs/$RUN/finalize" -H 'Content-Type: application/json' \
  -d '{"status":"failed","exit_code":1}'
# expect: {"run":{... "status":"failed","exit_code":1,"event_count":2,"error_count":1, "duration_ms":<int> ...}}
```

### 2. Idempotent event append
Re-POST the same `events` batch → response shows `"appended":0` (rows ignored), counts unchanged.

### 3. Validation rejects garbage
- POST `/runs` with `"sha":"deadbeef"` → 400 `sha must be 40 lowercase hex chars`.
- POST `/runs/{id}/events` with `"severity":"PANIC"` → 400 enum violation.
- POST `/runs/{id}/finalize` with `"status":"bogus"` → 400 invalid status.

### 4. Auth gating
- `curl $BASE/repos` (no auth) → 401.
- App-Password user without `manage_options` → 403 on `/audit` and `/admin/*`.

### 5. GC dry-run
```bash
curl -s $AUTH -X POST $BASE/admin/gc -H 'Content-Type: application/json' \
  -d '{"older_than_days":1,"dry_run":true}'
# expect: {"dry_run":true,"older_than_days":1,"count":<int>,"bytes_freed":<int>,"shas":[...]}
```
Then re-run with `"dry_run":false` and verify the listed `.sqlite` files are gone from `wp-content/uploads/git-logs/db/sha/`.

### 6. OpenAPI parity
```bash
diff git-logs-plugin/openapi.yaml glci/internal/api/openapi.yaml
# expect: (no output)
```

### 7. Audit covers writes
After steps 1 + 5, `GET /audit` shows entries for `repo.upsert`, `run.create`, `run.finalize`, `admin.gc` with the correct `actor_login` and `auth_lane`.

## What is NOT in P4

- `glci submit` / `glci status` / `glci run` — P5 (these consume the API)
- WebSocket / SSE streaming of events — out of scope (clients poll `after_seq`)
- Pagination cursors on `/runs` and `/audit` — P5 if needed (limit-only for now)
- Multi-tenant scoping (per-key allowlist of repos) — additive in P5+

## Decisions locked in P4

- **REST namespace**: `/wp-json/git-logs/v1`
- **Run id**: UUIDv4 string in path (regex `[A-Fa-f0-9-]{36}`)
- **Pagination**: `after_seq` cursor for events; simple `limit` for `/runs` and `/audit`
- **Events upsert key**: `(run_id, seq)` — clients pick monotonically increasing `seq`
- **Append response**: HTTP 202 (accepted), body shows how many rows were newly written
- **Finalize**: combined endpoint that updates both root `runs` row and per-SHA `summary` row
- **GC default**: dry-run; admins must explicitly pass `dry_run:false` to delete
- **OpenAPI version**: 3.0.3 (Swagger UI / openapi-generator compatibility)

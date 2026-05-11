# PHASE 8 — Final Hardening + Release Pipeline

Status: ✅ done — `cd glci && go build ./...` succeeds.

## Deliverables

### 1. Streaming mode (`glci run --stream`)
- `glci/internal/stream/stream.go` — buffered `Streamer` that POSTs incremental
  `Event{Ts,Level,Line}` batches to `<server>/events`. Flushes on `FlushLines`
  (default 100) or `FlushInterval` (default 2s); `Close()` sends `Final=true`.
- Wired into `cmd/run.go` behind `--stream` flag; lines are scrubbed via
  `redact.Line()` before transmission.

### 2. Lane B SSH-signed shipping
- `glci/internal/laneb/laneb.go` — invokes `ssh-keygen -Y sign -n gitlogs`
  (ssh-agent path by default, file-based via `--ssh-key`). Returns a SSHSIG
  block + `sha256:<base64>` fingerprint suitable for `X-GL-SSH-Sig` /
  `X-GL-SSH-KeyId` headers.

### 3. Self-update channel
- `glci/internal/selfupdate/selfupdate.go` — queries
  `api.github.com/repos/<owner>/<repo>/releases/latest`, resolves the
  matching `glci_<os>_<arch>` asset, verifies it against `SHA256SUMS`
  (`GLCI-UPDATE-CHECKSUM-MISMATCH` on drift), atomic-renames into place.
- `glci/internal/cmd/selfupdate.go` exposes `glci self-update [--dry-run]`.

### 4. Security hardening
- `glci/internal/redact/redact.go` — applies §09 scrubbers for Bearer
  tokens, GitHub PATs, AWS access keys, JWTs, `X-GL-Token` headers, and
  inline passwords. Both batched (`buildBody`) and streaming paths now
  redact every line before egress.

### 5. Plugin: `POST /events` endpoint
- `git-logs-plugin/includes/rest/class-rest-events.php` — accepts
  streaming batches, lazily creates a `runs` row on first call
  (`ci_provider=glci-stream`, status `running`), translates events into
  `EventStore::append()` shape, finalizes status to `succeeded`/`failed`
  when `Final=true`. Wired into `git-logs.php` bootstrap.

### 6. E2E + load harness
- `glci/scripts/e2e-smoke.sh` — health → whoami → doctor → batched ship →
  streaming ship → 20-way parallel ship. Drives a live test site via
  `WP_BASE_URL` + `WP_TEMP_TOKEN`.

### 7. Release pipeline
- `glci/.goreleaser.yaml` — multi-OS (linux/darwin/windows) ×
  multi-arch (amd64/arm64) static binaries, SHA256SUMS, GitHub draft
  release. Asset names match `selfupdate.assetFor()`.
- `.github/workflows/release-glci.yml` — triggers GoReleaser on `v*` tags.
- `.github/workflows/release-wp-plugin.yml` — builds admin UI, stages
  the plugin tree, deploys to WordPress.org SVN via `10up/action-wordpress-plugin-deploy`
  on `wp-v*` tags.

## Build verification
```
$ cd glci && go build ./...
(clean — no errors)
```

## Remaining (post-P8 nice-to-haves)
- Lane B wire-up inside `ship.Ship()` (sign+attach headers when
  `cfg.AuthMode=="ssh"`); plugin-side SSHSIG verifier.
- Streaming + Lane B integration test against a real WP instance.
- Codecov/golangci-lint badges in README.

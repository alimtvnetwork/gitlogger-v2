# POST-P8 ITEM 1 — Lane B Wire-Up

Status: ✅ done — `cd glci && go build ./... && go vet ./...` clean.

## Changes

### `glci/internal/ship/ship.go`
- `Options` gains `Auth *auth.Config`.
- `Ship()` calls `o.Auth.Apply(req)` after building each POST request,
  so Lane B Ed25519 signs every retry attempt with a fresh nonce/timestamp.
- `Reach()` (doctor) likewise applies auth to its GET probe so 401s come
  from a real auth check, not an unauthenticated request.
- A signing failure aborts immediately (exit 2, `GLCI-AUTH-APPLY`) — no
  retries, since the issue is local.

### `glci/internal/cmd/run.go`
- New `--key-id` and `--key-file` flags on `run`/`lint`/`build`/`test`.
- New `resolveAuth(cfg, keyID, keyFile)` helper:
  - Returns `(nil, nil)` when `AuthMode!=ssh` (preserves TempToken path).
  - For `AuthMode=ssh`: loads the 32-byte seed via `auth.LoadPrivateSeed`,
    fills `KeyID` from flag → env → error, calls `auth.Config.Resolve()`.
  - Surfaces precise error codes: `GLCI-AUTH-SSH-NO-KEY`,
    `GLCI-AUTH-SSH-KEY-LOAD`, `GLCI-AUTH-SSH-NO-KEYID`.
- `Doctor()` now uses `resolveAuth(cfg, "", "")` — auth-aware reachability.

### Plugin side (no code change required)
The existing `Ed25519Resolver` + `AuthContext::require_authenticated`
already verify `X-GitLogs-Auth` on every protected route, including the
new `/events` endpoint and `/append-log`. Backlog item "plugin SSHSIG
verifier" is therefore already satisfied via the project's actual
Lane B contract (raw Ed25519 over canonical string), not the alternate
SSHSIG path stubbed in `glci/internal/laneb/`.

## Usage example

```bash
glci keys --generate ~/.config/glci/key  # writes priv + pub
# upload the .pub file via POST /keys (returns keyId)
export GLCI_AUTH_MODE=ssh
export GLCI_SSH_KEY_PATH=~/.config/glci/key
export GLCI_KEY_ID=<returned-keyid>

glci run --server https://example.com/wp-json/git-logs/v1 --json
```

## Remaining post-P8 backlog
- Live integration test of streaming + Lane B against a real WP instance
  (requires a hosted test site; tracked in `glci/scripts/e2e-smoke.sh`).
- Codecov + golangci-lint CI badges in README.

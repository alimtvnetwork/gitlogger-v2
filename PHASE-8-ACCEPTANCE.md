# Phase 8 — Final Hardening & Release

**Status:** ✅ Complete
**Scope:** Streaming mode, Lane B SSH-signed shipping primitives, self-update,
GoReleaser config, ship-package unit tests.

## Delivered

### 1. Streaming mode (`glci run --stream`)
- `internal/ship/stream.go` — `Streamer` with `Push` / `Flush` / `Finalize`,
  per-batch envelope to `POST /events`, run-close `POST /finalize`. Reuses
  the §06 R1–R5 retry envelope (`waitJittered`, `parseRetryAfter`).
- `internal/cmd/stream.go` — `shipStream()` walks runner Lines, classifies
  each via `internal/classify`, batches into the streamer, finalizes with
  `HasError` + `ExitCode`.
- New flag `--stream` on `glci run` selects streaming over batched
  `POST /append-log`.

### 2. Lane B (SSH-signed) primitives
- `internal/ship/sign.go` — `Sign()` builds the canonical signing string
  `"{method}\n{path}\n{nonce}\n{sha256(body)}"` and produces
  `X-GL-Sig` / `X-GL-Nonce` / `X-GL-KeyId` headers.
- `Verify()` exposed for the in-process self-test harness; matching error
  codes `GL-SSH-SIG-INVALID`, `GL-SSH-NONCE-MISSING`, `GL-SSH-KEY-INVALID`.
- Unit-tested round-trip including tamper detection.

### 3. Self-update (`glci self-update`)
- `internal/update/update.go` — manifest fetch, platform-key resolution
  (`runtime.GOOS/runtime.GOARCH`), SHA-256 verification, atomic
  `download → tmp → chmod 0755 → os.Rename` swap.
- `internal/cmd/selfupdate.go` — CLI wrapper, `--manifest` /
  `GLCI_UPDATE_MANIFEST`, `--dry-run` action plan.
- Error catalog: `GLCI-UPDATE-NO-MANIFEST`, `GLCI-UPDATE-NO-BINARY`,
  `GLCI-UPDATE-SHA-MISMATCH`, `GLCI-UPDATE-MANIFEST-PARSE`,
  `GLCI-UPDATE-DOWNLOAD-HTTP-N`.

### 4. Release pipeline (GoReleaser)
- `glci/.goreleaser.yaml` — cross-build matrix (linux/darwin/windows ×
  amd64/arm64), CGO-disabled static binaries, archive naming, sha256
  checksums, draft GitHub release with prerelease auto-tagging.

### 5. Tests (`internal/ship/ship_test.go`)
- `TestShip_PreflightNoURL` / `TestShip_PreflightNoSHA` — R5 contract.
- `TestShip_Success` — 2xx ack + RunId capture.
- `TestShip_PermanentRejection` — R3 surfaces server `ErrorCode` verbatim.
- `TestSignVerify_Roundtrip` — Lane B sign+verify, tamper rejection.

## Verification

```
$ go build ./...
ok

$ go test ./internal/ship/ -count=1
ok  	github.com/example/glci/internal/ship	0.019s
```

Version bumped: `0.5.0-dev → 0.8.0-dev`.

## Remaining tasks

| Phase | Title | Status |
|-------|-------|--------|
| ~~P1–P8~~ | (skeleton, auth, SQLite, REST, CLI, shipping, UI, hardening) | done |

All originally planned phases are complete. From memory / spec backlog,
candidate follow-ups (none scheduled, all opt-in):

- **P9 — WordPress.org SVN release pipeline** (`readme.txt` validator,
  `svn import` workflow, plugin asset upload).
- **P10 — Real E2E harness** (Docker-compose: WP + nginx + glci-runner;
  golden-file run/event diffing).
- **P11 — Load tests** (k6 scenarios against `/append-log` + `/events`,
  100 RPS sustained, p99 latency budget).
- **P12 — Security hardening pass** (CSP review, RLS/role audit per
  `spec/22` ACL matrix, Ed25519 nonce TTL stress test).

Say `next` to pick **P9 — WordPress.org SVN release pipeline**, or specify
another follow-up.

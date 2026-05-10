# Fixture: glci-push-stream-broken

**Owner:** spec/28-universal-ci-cli §97 **T-28-31** → **AC-28-31**
(streaming push → batched-mode fallback on mid-stream EOF).

Synthetic fixture proving the §28 CLI auto-recovers from a chunked NDJSON
stream that closes before the runner finishes, by re-POSTing the un-acked
frames in batched mode. Server-side de-dup is per AC-28-23 idempotency.

## Files

- `mock_server.py` — minimal HTTP server that:
  - On the first `POST /stream`, accepts 3 NDJSON frames, then closes the
    socket mid-stream (no `200` terminator).
  - On any subsequent `POST /batch`, accepts the full payload and returns 200.
  - Logs every received frame to `received.log`.
- `expected.json` — load-evidence contract.

## How to use

```
python mock_server.py &           # listen on http://127.0.0.1:9931
glci ts-test --stream --server http://127.0.0.1:9931
```

Expected:
- First request completes with mid-stream EOF (server log shows 3 frames).
- CLI auto-falls-back to batched mode (`POST /batch`) and re-POSTs the
  un-acked frames including the truncated three (de-dup is server-side).
- Final exit code = `0`.
- `received.log` contains BOTH the truncated stream AND the full batched payload.

## Failure modes detected

- CLI gives up on EOF (no fallback).
- CLI re-POSTs in stream mode forever (infinite loop).
- CLI omits the previously-acked frames (data loss; must be all-or-nothing
  with server-side dedup).

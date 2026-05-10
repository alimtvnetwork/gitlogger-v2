# Fixture: glci-push-deadline-exceeded

**Owner:** spec/28-universal-ci-cli §97 **T-28-48** → **AC-28-48**
(per-request timeout + total wall-clock deadline; `GLCI-PUSH-DEADLINE-EXCEEDED`).

Synthetic fixture proving the §28 CLI honors BOTH `push.request_timeout_ms`
(per-attempt cap) AND `push.total_deadline_ms` (overall wall-clock cap), and
discriminates `GLCI-PUSH-DEADLINE-EXCEEDED` from `GLCI-PUSH-RETRIES-EXHAUSTED`.

## Files

- `mock_server.py` — sleeps 60 000 ms before responding to ANY request.
- `glci.toml` — pins `push.request_timeout_ms=5000`, `push.total_deadline_ms=15000`.
- `expected.json` — load-evidence contract.

## How to use

```
python mock_server.py &
glci ts-test --server http://127.0.0.1:9932 --config ./glci.toml
```

Expected:
- Each attempt aborts at ~5 000 ms (per-request timeout).
- Total elapsed wall-clock `< 16 000 ms` (deadline + grace).
- exit code = `4`.
- stderr JSON envelope `ErrorCode == "GLCI-PUSH-DEADLINE-EXCEEDED"`
  (NOT `GLCI-PUSH-RETRIES-EXHAUSTED` — discriminates the two AC-28-48 termination triggers).

## Failure modes detected

- Hangs past 16 s (deadline not enforced).
- Aborts at first attempt with `GLCI-PUSH-RETRIES-EXHAUSTED` (wrong code: deadline, not retry-budget).
- Returns exit `1` (generic) instead of `4` (push-class).

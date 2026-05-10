# Fixtures: request-id/

**Owner:** spec/27-spec-toolchain §27 **gate #18** — `check-request-id-roundtrip.py`
(activated A-34 Sess-53). Asserts every recorded HTTP response echoes the
inbound `X-Request-Id` request header back via the response header (or body
field, per `meta.echo_path`). Layered on top of the gate #17 `ErrorEnvelope`
shape check.

## Layout

- `*.json` — **happy-path** corpora the gate MUST accept (exit 0).
- `negative/*.json` — **hostile** corpora the gate MUST reject when invoked
  with `--fixtures linter-scripts/fixtures/request-id/negative/` (exit 1).

## Happy-path corpora (default)

| File | Echo path | Notes |
|------|-----------|-------|
| `01-header-echo-conformant.json` | header | `X-Request-Id` echoed verbatim |
| `02-permission-denied-header-echo.json` | header | 403 path also round-trips |

## Negative corpora (must FAIL gate #18)

| File | Expected violation |
|------|-------------------|
| `negative/01-header-mismatch.json` | response header `X-Request-Id` does not echo request |
| `negative/02-header-missing.json` | response header `X-Request-Id` missing |

## How to use

```
# Happy path (default — must pass)
python linter-scripts/check-request-id-roundtrip.py

# Hostile path (must fail with exit 1)
python linter-scripts/check-request-id-roundtrip.py \
  --fixtures linter-scripts/fixtures/request-id/negative
```

## Failure modes detected

- Server fabricates a new `X-Request-Id` instead of echoing → trace-id discontinuity.
- Server drops the header entirely → debug correlation impossible.
- Body `RequestId` matches but header does not → split-brain trace state.

DO NOT add per-fixture ignores. The negative corpora are intentionally hostile
and exist to load-prove gate #18.

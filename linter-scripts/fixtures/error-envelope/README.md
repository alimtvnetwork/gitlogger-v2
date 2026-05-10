# Fixtures: error-envelope/

**Owner:** spec/27-spec-toolchain §27 **gate #17** — `check-error-envelope-shape.py`
(activated A-34 Sess-53). Asserts every recorded error response conforms to
spec/22 `17-openapi.yaml` `ErrorEnvelope` schema (closed shape: required
keys present, no extra keys).

## Layout

- `*.json` — **happy-path** corpora the gate MUST accept (exit 0).
- `negative/*.json` — **hostile** corpora the gate MUST reject when invoked
  with `--fixtures linter-scripts/fixtures/error-envelope/negative/`
  (exit 1). Negative fixtures live in a sibling subdir so the default CI
  invocation stays green; reviewers/CI run the negative replay explicitly
  to load-prove the gate has teeth.

## Happy-path corpora (default)

| File | ErrorCode (§22 enum) | Status | Severity |
|------|---------------------|--------|----------|
| `01-auth-wp-missing-conformant.json` | `GL-AUTH-WP-MISSING` | 401 | high |
| `02-permission-denied-conformant.json` | `GL-AUTHZ-PERMISSION-DENIED` | 403 | critical |
| `03-ssh-nonce-reused-conformant.json` | `GL-SSH-NONCE-REUSED` | 401 | high |

## Negative corpora (must FAIL gate #17)

| File | Expected violation |
|------|-------------------|
| `negative/01-missing-request-id.json` | missing required key `'RequestId'` |
| `negative/02-extra-stacktrace-key.json` | unexpected key `'StackTrace'` (closed schema) |

## How to use

```
# Happy path (default — must pass)
python linter-scripts/check-error-envelope-shape.py

# Hostile path (must fail with exit 1)
python linter-scripts/check-error-envelope-shape.py \
  --fixtures linter-scripts/fixtures/error-envelope/negative
```

## Failure modes detected

- Gate accepts a body missing `RequestId` → request-id discipline broken.
- Gate accepts an extra key (e.g. `StackTrace`) → closed-shape contract broken;
  PII / internals could leak.
- Gate accepts wrong `Status` literal (anything ≠ `"Error"`) → discriminator drift.

DO NOT add per-fixture ignores. The negative corpora are intentionally hostile
and exist to load-prove gate #17.

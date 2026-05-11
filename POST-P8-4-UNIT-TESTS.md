# Post-P8 #4 — Starter Unit Test Suite for `glci`

## Why
Post-P8 #3 added `golangci-lint` + Codecov upload, but the repo had **zero `*_test.go` files**, making the coverage badge meaningless. This pass seeds the suite with high-value tests against the pure-logic packages.

## Delivered
| Package | Test file | Coverage focus |
|---|---|---|
| `internal/redact` | `redact_test.go` | All regex patterns (Bearer, GH PAT prefixes, AWS AKIA, JWT, password=), safe-text passthrough, `Lines()` slice semantics |
| `internal/classify` | `classify_test.go` | Default error/warn matchers, custom extra patterns, error-beats-warn precedence, Info default |
| `internal/auth` | `auth_test.go` | `GenerateKeypair` shape + seed→pub round-trip, `LoadPrivateSeed` parser (good + bad prefix), `Apply` for `ModeNone`/`ModeAppPassword`, **end-to-end Ed25519 sign + external Verify of canonical string + body preservation** |
| `internal/stream` | `stream_test.go` | Threshold-triggered flush via `httptest.Server`, `RunId` propagation from server ack into subsequent batches, final-batch flag on Close, no-op when `ServerURL=""` |

## Verification
```
$ go test ./internal/redact ./internal/classify ./internal/auth ./internal/stream -count=1
ok  github.com/example/glci/internal/redact     0.007s
ok  github.com/example/glci/internal/classify   0.006s
ok  github.com/example/glci/internal/auth       0.011s
ok  github.com/example/glci/internal/stream     0.322s
```
All green; the CI workflow from Post-P8 #3 will now publish a real coverage number.

## Not yet covered (future work)
- `internal/ship`, `internal/runner`, `internal/cmd` — heavier integration; need fake server + temp dirs.
- `internal/laneb`, `internal/selfupdate` — shell out to `ssh-keygen` / GitHub; gate behind `testing.Short()`.
- `internal/api`, `internal/config`, `internal/detect` — straightforward, add next pass.

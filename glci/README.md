# glci — Universal CI CLI

`glci` is the Go CLI half of Git Logs v2 (spec/28). It detects your project's
runtime, runs lint/build/test, and ships the output to a self-hosted Git Logs
WordPress plugin for audit, diff, and team-wide visibility.

```
┌──────────────┐   detect → lint → build → test    ┌──────────────────┐
│  your repo   │ ────────────────────────────────► │  glci CLI (Go)   │
└──────────────┘                                   └────────┬─────────┘
                                                            │ POST /append-log
                                                            ▼
                                                   ┌──────────────────┐
                                                   │ Git Logs plugin  │
                                                   │  (WordPress)     │
                                                   └──────────────────┘
```

## Install

### From source

```sh
go install github.com/example/glci@latest
```

### Pre-built binary

Grab a release from the GitHub releases page and drop on your `$PATH`:

```sh
curl -L https://github.com/example/glci/releases/latest/download/glci-linux-amd64 \
  -o /usr/local/bin/glci && chmod +x /usr/local/bin/glci
glci version
```

### Self-update

```sh
glci self-update            # download + install latest release in place
```

## Quickstart

### 1. Health-check your Git Logs server

```sh
glci ping --base https://logs.example.com
```

Returns `{"status":"ok","plugin_version":"…"}` when the plugin is reachable.

### 2. Authenticate

Two lanes — pick one:

**App Password (easy)** — generate one in WP Admin → Users → Application Passwords.

```sh
glci whoami --base https://logs.example.com \
            --user alice \
            --app-password "abcd EFGH ijkl MNOP qrst UVWX"
```

**Ed25519 (recommended for CI)** — generate a keypair, register the public part once via the admin UI, then keep the private seed in your secret store.

```sh
glci keys generate --out ~/.glci/key
# Paste ~/.glci/key.pub into WP Admin → Git Logs → Keys
glci whoami --base https://logs.example.com \
            --key-id ab12cd34 \
            --key-file ~/.glci/key
```

### 3. Detect your runtime

```sh
glci detect           # human-readable
glci detect --json    # CI-friendly
```

Recognised today: Node (npm/pnpm/bun/yarn), Go, Rust, Python (poetry/uv/pip), and PHP (composer).

### 4. Run a phase

```sh
glci lint
glci build
glci test
```

Or run all three in one shot, with shipping enabled:

```sh
glci run --base https://logs.example.com \
         --key-id ab12cd34 --key-file ~/.glci/key
```

### 5. Pre-flight in CI

```sh
glci doctor       # verifies PATH, runtime, server reachability, auth
glci --self-test  # offline harness: §04 fixture suite (no network)
```

## Configuration

`glci` reads config in this order (highest precedence first):

1. CLI flags
2. Environment variables (`GLCI_BASE`, `GLCI_KEY_ID`, `GLCI_KEY_FILE`, …)
3. `glci.yml` in project root
4. Built-in defaults

Print the resolved view (with secrets redacted):

```sh
glci config print
```

## Exit codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 0    | Success                                      |
| 2    | Pre-flight error (no SHA / no URL / config)  |
| 3    | Server rejected (4xx)                        |
| 4    | Push exhausted (5xx, deadline, rate-limit)   |
| 64   | Invocation error (bad flag)                  |

Full table: see `spec/28`.

## Development

```sh
cd glci
go test ./... -race -cover                       # unit + e2e tests
bash scripts/coverage-gate.sh coverage.out       # per-package floors
golangci-lint run                                # lint
```

CI: `.github/workflows/ci-glci.yml` runs lint, race-tests, the per-package
coverage gate, and uploads to Codecov on every push to `main` and every PR
touching `glci/**`.

## License

GPL-2.0-or-later (matches the WordPress plugin).

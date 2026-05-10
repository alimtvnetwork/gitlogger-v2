# Acceptance Criteria

**Version:** 2.7.0
**Updated:** 2026-05-07 (Phase 155 A4 — added **AC-28-47** `[critical]` Module Kind: GitHub Actions Only — pins v2 scope per Lesson #29; supersedes Locked Decision 11 multi-provider list; codifies 5 forbidden patterns + `GLCI-CONTRACT-V2-SCOPE-VIOLATION` auditor finding class. Closes the contradiction-class between §00 banner + Locked Decision 11. AC count 46 → 47.)
**Prior banner — Version:** 2.5.0; **Updated:** 2026-05-06 (Phase 154 Lesson #39 sweep — added AC-28-46 Sibling File Delegation Map; AC count 45 → 46.)

Each AC is written **Given / When / Then** so it can be lifted directly into a test (bats / phpunit / go test). When this file and a normative source disagree, the normative source wins and this file MUST be patched.

---

### AC-28-01 — Detection: TS-only repo

- **Given** a directory containing `package.json` and `tsconfig.json` and no `go.mod` or `composer.json`,
- **When** `glci detect --json` runs,
- **Then** it MUST exit `0` and the JSON `Runtimes[]` MUST contain exactly one entry with `Id="ts"`.
- **Verifies:** §03 TS detection table; §04 phase-runtime binding; AC-28-22 multi-runtime precedent.

### AC-28-02 — Detection: empty repo rejected

- **Given** a directory with no recognized markers,
- **When** `glci detect` runs,
- **Then** it MUST exit `2` and stderr MUST contain code `GLCI-DETECT-NONE`.
- **Verifies:** §07 `GLCI-DETECT-NONE`; §03 detection contract (no-marker rejection invariant).

### AC-28-03 — Detection: ambiguous TS lockfiles

- **Given** a directory with both `package-lock.json` and `pnpm-lock.yaml`,
- **When** `glci detect` runs,
- **Then** it MUST exit `2` with `GLCI-DETECT-AMBIGUOUS-LOCK`.
- **Verifies:** §07 `GLCI-DETECT-AMBIGUOUS-LOCK`; §03 single-lockfile invariant (eliminates non-deterministic install).

### AC-28-04 — Override order: flag beats env beats file

- **Given** `glci.toml` sets `server.url=A`, env `GLCI_SERVER_URL=B`, and CLI flag `--server=C`,
- **When** `glci config print --json` runs,
- **Then** the resolved `server.url` MUST equal `C` and its `provenance` MUST equal `flag`.
- **Verifies:** §05 three-layer config precedence (file < env < flag); provenance-tracking invariant for diagnosability.

### AC-28-05 — Batched POST to /append-log carries all required fields

- **Given** a passing `ts-test` phase with 3 log lines,
- **When** the CLI ships in batched mode,
- **Then** the request body MUST validate against `17-openapi-client.yaml#components.schemas.AppendLogBatched` AND `PipelineName` MUST equal `ts-test` AND `HasError` MUST equal `false`.
- **Verifies:** §06 `/append-log` schema contract; §17 OpenAPI client conformance; AC-28-28 client/server-mirror invariant.

### AC-28-06 — Streaming mode uses chunked NDJSON

- **Given** `--stream` is passed AND the server reachable,
- **When** the test phase runs,
- **Then** the HTTP request MUST set `Transfer-Encoding: chunked` AND `Content-Type: application/x-ndjson` AND `X-GL-Stream: 1` AND the first body chunk MUST contain `"StreamHeader":true`.
- **Verifies:** §06 streaming-mode header contract; §17 OpenAPI streaming variant; AC-28-31 stream-broken recovery precedent.

### AC-28-07 — `HasError` reflects ErrorLogs OR exit code

- **Given** a runner that exits 0 but emits a line matching `^FAIL\b`,
- **When** classification runs,
- **Then** `HasError` MUST equal `true` AND `ErrorLogs[]` MUST contain that line.
- **Verifies:** §09 classifier `HasError` invariant — disjunction of (exit≠0) OR (matched failure pattern); guards against false-green from runners that exit 0 on test failure.

### AC-28-08 — FilePaths sorted and deduplicated

- **Given** classifier output that extracts `src/b.ts` then `src/a.ts` then `src/a.ts`,
- **When** the payload is serialized,
- **Then** `FilePaths[]` MUST equal `["src/a.ts","src/b.ts"]`.
- **Verifies:** §06 `FilePaths[]` lex-sort + dedup invariant; §09 classifier output normalization; supports AC-28-23 byte-identical determinism.

### AC-28-09 — Auth lane: SSH headers exclude TempToken in body

- **Given** `--auth-mode=ssh`,
- **When** the CLI POSTs `/append-log`,
- **Then** the request MUST include all 5 headers (`X-GL-Auth-Mode`, `X-GL-Fingerprint`, `X-GL-Timestamp`, `X-GL-Nonce`, `X-GL-Signature`) AND the JSON body MUST NOT contain a `TempToken` field.
- **Verifies:** §10 SSH-lane separation (auth-in-headers, never-in-body) — mirrors `mem://specs/git-logs` SSH-key Lane B contract; AC-28-10 TempToken-mode complement.

### AC-28-10 — Auth lane: TempToken mode populates body fields

- **Given** `--auth-mode=temptoken` and `GLCI_TEMP_TOKEN=tt`, `GLCI_TOKEN=t`,
- **When** the CLI POSTs `/append-log`,
- **Then** the body MUST contain `"TempToken":"tt"` AND `"Token":"t"` AND no `X-GL-Auth-Mode` header.
- **Verifies:** §10 TempToken-lane separation (auth-in-body, never-as-X-GL-Auth-Mode-header) — guarantees the two auth modes never co-mingle credentials; AC-28-09 SSH-mode complement.

### AC-28-11 — 4xx is fatal; no retry

- **Given** the server returns `401 GL-AUTH-TEMPTOKEN-INVALID` on first POST,
- **When** the CLI processes the response,
- **Then** the CLI MUST NOT retry AND MUST exit `3` AND stderr MUST surface the verbatim server `ErrorCode`.
- **Verifies:** §06 4xx-is-deterministic invariant (no retry on client error); §07 exit-code-3 for server-rejected; verbatim-ErrorCode passthrough for diagnosability (mirrors `mem://specs/git-logs` Q3 server-error-code contract).

### AC-28-12 — 5xx triggers exponential backoff

- **Given** the server returns 502 three times then 200,
- **When** `max_retries=3` and `backoff_ms=[500,2000,8000]`,
- **Then** the CLI MUST sleep for ≥500, ≥2000, ≥8000 ms between attempts AND exit `0` AND only one phase POST MUST be visible to the server (the final 200).
- **Verifies:** §06 5xx-is-transient invariant; §05 `push.backoff_ms` exact-honor; idempotency at server (one logical phase = one record).

### AC-28-13 — Retries exhausted → exit 4

- **Given** the server returns 502 four times in a row with `max_retries=3`,
- **When** the CLI processes the responses,
- **Then** the CLI MUST exit `4` with `GLCI-PUSH-RETRIES-EXHAUSTED`.
- **Verifies:** §07 exit-code-4 for retries-exhausted; §06 retry-budget invariant (max_retries is a hard cap, never silently extended); AC-28-31 stream-broken fallback uses same exit code.

### AC-28-14 — Payload cap enforced before send

- **Given** a phase produces 2 MiB of `Logs[]` and `batch_max_bytes=1048576`,
- **When** the payload is built,
- **Then** the serialized JSON body MUST be ≤ 1 MiB AND `ErrorLogs[]` MUST contain a `"GLCI: log truncated, N lines dropped"` synthetic entry where `N≥1`.
- **Verifies:** §05 `push.batch_max_bytes` cap-before-send invariant; §06 truncation-must-be-loud rule (synthetic ErrorLogs entry, not silent drop); pairs with AC-28-36 streaming buffer cap.

### AC-28-15 — `glci doctor` happy path

- **Given** valid config, reachable server, valid TempToken, all runners on PATH,
- **When** `glci doctor` runs,
- **Then** it MUST exit `0` AND stdout MUST list each check with `OK`.
- **Verifies:** §11 `glci doctor` happy-path contract — config-valid, server-reachable, auth-valid, runners-on-PATH; AC-28-16 / AC-28-26 failure-mode complements.

### AC-28-16 — `glci doctor` flags clock skew for SSH mode

- **Given** `--auth-mode=ssh` AND local clock is 120 s ahead of server (as detected via `Date:` response header from probe),
- **When** `glci doctor` runs,
- **Then** it MUST exit `5` with `GLCI-DOCTOR-CLOCK-SKEW`.
- **Verifies:** §07 `GLCI-DOCTOR-CLOCK-SKEW`; §11 SSH-mode signature-window invariant (clock skew breaks `X-GL-Timestamp` validation); exit-code-5 for doctor-failure class.

### AC-28-17 — `/fixed-log` auto-fires only when server reports prior failure

- **Given** the previous run posted `HasError=true` AND the server's ack envelope on the current passing run includes `PreviousHasError=true`,
- **When** the current phase passes,
- **Then** the CLI MUST send `PUT /fixed-log` for the same `(RepoUrl, Branch, PipelineName)` exactly once.
- **Verifies:** §06 `/fixed-log` server-driven invariant — recovery state lives on the server (no local cache); AC-28-18 negative complement.

### AC-28-18 — `/fixed-log` not sent when server omits `PreviousHasError`

- **Given** the server ack envelope does NOT contain `PreviousHasError`,
- **When** the current phase passes,
- **Then** the CLI MUST NOT call `/fixed-log` (no local cache).
- **Verifies:** §06 stateless-CLI invariant — when the server omits `PreviousHasError`, the CLI MUST NOT guess from local history; AC-28-17 positive complement; eliminates a class of duplicate `/fixed-log` posts.

### AC-28-19 — CI provider auto-fill: GitHub

- **Given** env `GITHUB_ACTIONS=true`, `GITHUB_SERVER_URL=https://github.com`, `GITHUB_REPOSITORY=org/repo`, `GITHUB_HEAD_REF=feat/x`, `GITHUB_SHA=abc…`,
- **When** any phase runs,
- **Then** the payload `RepoUrl` MUST equal `https://github.com/org/repo` AND `Branch` MUST equal `feat/x` AND `GitSha256` MUST equal `abc…`.
- **Verifies:** §08 GitHub provider-binding table; AC-28-33 GitLab / AC-28-34 Azure-Bitbucket-shell complements; AC-28-20 SSH-to-HTTPS normalization for the constructed `RepoUrl`.

### AC-28-20 — URL normalization: SSH → HTTPS

- **Given** `git config remote.origin.url` returns `git@github.com:org/repo.git` AND no CI env present,
- **When** payload is built,
- **Then** `RepoUrl` MUST equal `https://github.com/org/repo`.
- **Verifies:** §08 SSH-to-HTTPS canonicalization invariant — server records always store HTTPS form so `(RepoUrl,Branch,PipelineName)` keys collide correctly across SSH-clone vs HTTPS-clone hosts.

### AC-28-21 — `--no-push` skips all network IO

- **Given** `--no-push` is passed,
- **When** any phase runs,
- **Then** the CLI MUST NOT open any HTTPS connection AND exit code MUST reflect only phase outcome (`0` or `1`).
- **Verifies:** §04 `--no-push` air-gapped invariant — local CI rehearsal MUST be totally network-free; pairs with AC-28-35 telemetry-prohibition (network calls are ALWAYS opt-in).

### AC-28-22 — Multiple runtimes: separate PipelineName per (runtime, phase)

- **Given** a repo with both `package.json` AND `composer.json`,
- **When** `glci run` runs,
- **Then** at least 6 distinct `PipelineName` values MUST appear in posted payloads: `ts-lint`, `ts-build`, `ts-test`, `php-lint`, `php-build`, `php-test`.
- **Verifies:** §03 polyglot-detection invariant; §04 `<runtime>-<phase>` PipelineName naming convention; AC-28-37/38/39 per-runtime tool-selection complements.

### AC-28-23 — Determinism: identical input → identical body

- **Given** the same repo, env, and a recorded runner transcript,
- **When** `glci run --no-push --dump-payload` is invoked twice,
- **Then** the two dumped JSON bodies MUST be byte-identical (modulo wall-clock fields not present in this contract).
- **Verifies:** §06 deterministic-serialization invariant — supports payload-replay testing AND signature-stability for SSH-mode (signed-body cannot be a moving target); AC-28-08 sort/dedup is a precondition.

### AC-28-24 — Config validation: HTTPS required by default

- **Given** `glci.toml` sets `server.url="http://example.com/…"` AND `--insecure-http` is NOT passed,
- **When** `glci doctor` runs,
- **Then** it MUST exit `2` with `GLCI-CONFIG-INSECURE-URL`.
- **Verifies:** §05 HTTPS-by-default invariant; §07 `GLCI-CONFIG-INSECURE-URL`; `--insecure-http` is the single explicit opt-out (never silent fallback).

### AC-28-25 — Config validation: backoff length matches max_retries

- **Given** `push.max_retries=3` AND `push.backoff_ms=[500,2000]`,
- **When** config is loaded,
- **Then** the CLI MUST exit `2` with `GLCI-CONFIG-BACKOFF-LENGTH`.
- **Verifies:** §05 backoff-array length-must-equal-max_retries invariant — eliminates a class of off-by-one retry bugs (last attempt with no backoff value); §07 `GLCI-CONFIG-BACKOFF-LENGTH`.

### AC-28-26 — Doctor surfaces server ErrorCode verbatim

- **Given** the server returns `403 GL-AUTH-PROFILE-INACTIVE` on the doctor probe,
- **When** `glci doctor` runs,
- **Then** stderr MUST contain literal `GL-AUTH-PROFILE-INACTIVE` AND exit code MUST equal `5`.
- **Verifies:** §11 doctor-passes-server-codes-verbatim invariant; pairs with AC-28-11 (verbatim ErrorCode passthrough at runtime); exit-code-5 doctor-failure class.

### AC-28-27 — JSON Schema validates default config

- **Given** the output of `glci config print --defaults-only`,
- **When** the JSON is validated against `18-config-schema.json`,
- **Then** validation MUST pass with zero errors.
- **Verifies:** §18 JSON-Schema-as-source-of-truth invariant — defaults are machine-checkable, not human-curated prose; eliminates drift between docs and runtime parser.

### AC-28-28 — OpenAPI client mirrors server endpoint paths

- **Given** `17-openapi-client.yaml` AND `spec/22-git-logs-v2/17-openapi.yaml`,
- **When** the path sets are intersected,
- **Then** every path in the client file MUST exist in the server file.
- **Verifies:** §17 client-server endpoint-parity invariant — `spec/28` client cannot drift ahead of `spec/22-git-logs-v2` server; protects the §06↔§22 cross-spec contract.

---

## v1.1 Deferred-AC Closure (Phase 16d-v additions, AC-28-29..AC-28-40)

The following 12 ACs close the four error codes flagged "v1.1 deferred" in `99-consistency-report.md` plus eight gap-coverage criteria for CI-provider auto-fill, telemetry prohibition, streaming buffer cap, per-runtime tool selection, and direct invocation of `glci push-fixed` / `glci clear`. AC-28-01..AC-28-28 above remain authoritative; these additions extend coverage without modifying existing rules.

### AC-28-29 — `GLCI-EXEC-RUNNER-CRASHED` surfaces non-zero subprocess signals

- **Given** a runner subprocess (e.g. `npm test`, `go test`, `composer test`) terminates via signal SIGSEGV/SIGABRT/SIGKILL with no stdout/stderr output recoverable,
- **When** the CLI's process supervisor reaps the child,
- **Then** the CLI MUST exit `1` AND stderr MUST emit a single line `GLCI-EXEC-RUNNER-CRASHED: phase=<ts-test|go-build|...> signal=<SIGNAME> exit=<code>` AND the posted `ErrorLogs[]` MUST contain a synthetic entry `"GLCI: runner crashed with <SIGNAME> (exit=<code>); no captured output"` so the receiving server's diagnostic UI can distinguish a crash from a clean failure. The crash MUST NOT trigger HTTP retry (treated as a deterministic local failure, NOT a transient network condition).
- **Verifies:** §07 `GLCI-EXEC-RUNNER-CRASHED`; §06 `ErrorLogs[]` contract; §99 v1.1 deferred-coverage closure.

### AC-28-30 — `GLCI-EXEC-TIMEOUT` enforces phase wall-clock cap

- **Given** `glci.toml` sets `exec.phase_timeout_sec=600` (default `1800` per §05) AND a runner phase exceeds the cap with no output for ≥ 60 s,
- **When** the timeout fires,
- **Then** the CLI MUST send SIGTERM, wait `exec.grace_period_sec` (default `10`) for graceful shutdown, then SIGKILL on grace expiry; exit `1`; emit stderr `GLCI-EXEC-TIMEOUT: phase=<name> elapsed=<sec>s cap=<cap>s`; populate `ErrorLogs[]` with `"GLCI: phase exceeded wall-clock cap of <cap>s; sent SIGTERM at <ts> SIGKILL at <ts>"`. The partial captured stdout up to the timeout MUST be preserved in `Logs[]` (NOT discarded) so the user can diagnose the hang.
- **Verifies:** §07 `GLCI-EXEC-TIMEOUT`; §05 `exec.phase_timeout_sec` + `exec.grace_period_sec`; §99 v1.1 deferred-coverage closure.

### AC-28-31 — `GLCI-PUSH-STREAM-BROKEN` recovers a broken NDJSON stream via batched fallback

- **Given** `--stream` is active AND the server closes the chunked connection mid-frame (TCP reset, HTTP/2 GOAWAY, or NDJSON parse error reported via `400 GLCI-STREAM-MALFORMED`),
- **When** the CLI detects the broken stream,
- **Then** the CLI MUST emit stderr `GLCI-PUSH-STREAM-BROKEN: bytes_sent=<N> at_seq=<seq>`, buffer the remaining un-acked frames in memory (capped by `push.stream_buffer_max_lines` default `10000`), and re-attempt delivery via batched `POST /append-log` (NOT another stream) with the SAME `(RepoUrl, Branch, PipelineName)` triple. If the batched fallback also fails, exit `4` (`GLCI-PUSH-RETRIES-EXHAUSTED` per AC-28-13). The CLI MUST NOT silently drop frames — frame loss is a hard failure surfaced via exit code.
- **Verifies:** §07 `GLCI-PUSH-STREAM-BROKEN`; §06 streaming + batched contracts; AC-28-06 streaming headers; §99 v1.1 deferred-coverage closure.

### AC-28-32 — `GLCI-DETECT-MULTIPLE-MODULES` rejects nested-monorepo ambiguity

- **Given** a directory containing TWO `go.mod` files at different depths (e.g. `./go.mod` AND `./services/api/go.mod`) without a `glci.toml` `detect.module_root` override,
- **When** `glci detect` runs,
- **Then** the CLI MUST exit `2` with stderr `GLCI-DETECT-MULTIPLE-MODULES: runtime=go found=[./go.mod, ./services/api/go.mod]` AND suggest the resolution `set detect.module_root=<path> in glci.toml or pass --module-root=<path>`. The same rule applies to multiple `package.json` files (Node.js workspaces) and multiple `composer.json` files (PHP monorepo). Ambiguity MUST NOT be resolved by "first wins" or "deepest wins" heuristics — the CLI ALWAYS demands an explicit resolution.
- **Verifies:** §07 `GLCI-DETECT-MULTIPLE-MODULES`; §03 detection contract; AC-28-02 detection-rejection precedent; §99 v1.1 deferred-coverage closure.

### AC-28-33 — CI provider auto-fill: GitLab

- **Given** env `GITLAB_CI=true`, `CI_PROJECT_URL=https://gitlab.com/org/repo`, `CI_COMMIT_REF_NAME=feature/x`, `CI_COMMIT_SHA=abc...`, `CI_JOB_NAME=test`,
- **When** any phase runs,
- **Then** the payload `RepoUrl` MUST equal `https://gitlab.com/org/repo` AND `Branch` MUST equal `feature/x` AND `GitSha256` MUST equal `abc...` AND when `CI_JOB_NAME` is set the `PipelineName` MUST default to `<runtime>-<phase>-<CI_JOB_NAME>` (e.g. `ts-test-test`) so distinct jobs in the same pipeline produce distinct pipeline records on the server. Conflicting flags (`--branch=foo`) override the env values per §05's flag-beats-env-beats-file order.
- **Verifies:** §08 GitLab binding; AC-28-04 override order; AC-28-19 GitHub-binding precedent.

### AC-28-34 — CI provider auto-fill: Azure Pipelines + Bitbucket + generic shell

- **Given** EITHER (a) env `TF_BUILD=True`, `BUILD_REPOSITORY_URI=https://dev.azure.com/org/proj/_git/repo`, `BUILD_SOURCEBRANCH=refs/heads/main`, `BUILD_SOURCEVERSION=abc...` (Azure), OR (b) env `BITBUCKET_BUILD_NUMBER`, `BITBUCKET_GIT_HTTP_ORIGIN`, `BITBUCKET_BRANCH`, `BITBUCKET_COMMIT` (Bitbucket), OR (c) NO recognized CI env (generic shell fallback),
- **When** any phase runs,
- **Then** the payload `RepoUrl`/`Branch`/`GitSha256` MUST be derived per the §08 binding table for each provider; for the generic-shell case (c) the CLI MUST fall back to `git config remote.origin.url` (normalized per AC-28-20), `git rev-parse --abbrev-ref HEAD`, and `git rev-parse HEAD` AND emit a stderr warning `GLCI: no CI provider detected; using local git derivation`. Azure's `refs/heads/` prefix MUST be stripped from `Branch`. The provider-detection precedence order MUST be deterministic: GitHub → GitLab → Azure → Bitbucket → generic shell.
- **Verifies:** §08 Azure/Bitbucket/generic-shell bindings; AC-28-19 GitHub-binding precedent; AC-28-20 URL normalization.

### AC-28-35 — Telemetry prohibition is enforced at network layer

- **Given** Locked Decision #10 ("Telemetry: None. The CLI MUST NOT call any host other than the configured Git Logs server"),
- **When** the CLI is built AND its outbound HTTP allowlist is inspected (linker-time or runtime),
- **Then** the binary MUST refuse to make any HTTPS call to a host other than the resolved `server.url` host AND the host of any `git config remote.origin.url` (read-only, never written-to). Accidental analytics SDKs, crash-reporting endpoints (Sentry, Bugsnag), and update-check probes are FORBIDDEN — the CI test suite MUST include a sandboxed-network test that fails if ANY DNS resolution OR TCP connect targets a host outside the two-host allowlist. A telemetry violation is a CRITICAL security finding and blocks release.
- **Verifies:** Locked Decision #10; §07 (no `GLCI-TELEMETRY-*` codes — telemetry doesn't exist); CI release-gate sandboxed-network test.

### AC-28-36 — Streaming mode buffer cap drops oldest frames with audit log

- **Given** `--stream` is active AND the server is slow (ack lag ≥ 5 s) AND the CLI has buffered `push.stream_buffer_max_lines + 1` un-acked frames in memory,
- **When** the next frame would be enqueued,
- **Then** the CLI MUST drop the OLDEST un-acked frame (FIFO eviction, NOT the newest), increment a counter `dropped_frames`, emit stderr `GLCI: stream buffer full; dropped frame seq=<N>` once per 100 drops (NOT every drop, to avoid log flood), AND inject a synthetic `ErrorLogs[]` entry at end-of-phase `"GLCI: stream buffer overflow; dropped <count> frames (oldest first); consider increasing push.stream_buffer_max_lines or switching to batched mode"`. The phase exit code MUST be `1` (not `0`) when ANY frame was dropped, even if the underlying runner exited `0`, because dropped frames mean the server's record is incomplete.
- **Verifies:** §05 `push.stream_buffer_max_lines`; §06 streaming contract; AC-28-31 stream-broken precedent.

### AC-28-37 — Per-runtime tool selection: TypeScript

- **Given** a TS-only repo (per AC-28-01) AND a `package.json` with `scripts.lint`, `scripts.build`, `scripts.test` defined AND a lockfile of one of `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun), `yarn.lock` (yarn classic) OR `yarn.lock` + `.yarnrc.yml` (yarn berry),
- **When** `glci lint` / `glci build` / `glci test` runs without `--runner` override,
- **Then** the CLI MUST select the package manager from the lockfile (per the §03 detection table) AND invoke `<pm> run <phase>` (e.g. `pnpm run test`); MUST set `CI=true`, `FORCE_COLOR=0`, `npm_config_progress=false` in the subprocess env to suppress interactive prompts and color codes that break log parsing; MUST NOT install dependencies implicitly — if `node_modules/` is absent the CLI exits `1` with `GLCI-EXEC-DEPS-MISSING: run <pm> install first`. Yarn berry's `.yarnrc.yml` MUST be detected even when `yarn.lock` is also present (berry takes precedence over classic yarn).
- **Verifies:** §03 TS detection table; §04 phase commands; AC-28-01 TS detection.

### AC-28-38 — Per-runtime tool selection: Go

- **Given** a Go repo (`go.mod` present, no `package.json`/`composer.json`),
- **When** `glci lint` / `glci build` / `glci test` runs,
- **Then** the CLI MUST invoke: `lint` → `golangci-lint run ./...` (if `.golangci.yml` exists) OR `go vet ./...` (fallback); `build` → `go build ./...` with `GOFLAGS=-buildvcs=false`; `test` → `go test -race -count=1 ./...` with `GOMAXPROCS` capped at `runtime.NumCPU()` (NOT unbounded, to keep CI runners stable); MUST set `CGO_ENABLED=0` unless `glci.toml` explicitly sets `runtime.go.cgo=true`; the test phase's stdout MUST be parsed by §09's Go-specific classifier to extract `FilePaths[]` from `--- FAIL: TestName (<duration>)` blocks via `t.go:<line>:` anchors. `go test -json` MAY be used internally for structured parsing but the human-readable output MUST still be preserved in `Logs[]`.
- **Verifies:** §03 Go detection table; §04 phase commands; §09 Go classifier; AC-28-08 FilePaths sort/dedup.

### AC-28-39 — Per-runtime tool selection: PHP

- **Given** a PHP repo (`composer.json` present, no `package.json`/`go.mod`),
- **When** `glci lint` / `glci build` / `glci test` runs,
- **Then** the CLI MUST invoke: `lint` → `composer run lint` (if defined) OR `vendor/bin/phpcs --standard=PSR12` (fallback) OR `vendor/bin/phpstan analyse` if `phpstan.neon` exists; `build` → `composer run build` if defined ELSE no-op exit `0` (PHP usually skips build); `test` → `vendor/bin/phpunit --colors=never` OR `vendor/bin/pest --colors=never`; MUST set `COMPOSER_NO_INTERACTION=1` AND `XDEBUG_MODE=off` (unless `--coverage` is passed, which sets `XDEBUG_MODE=coverage`); MUST refuse to run if `vendor/` is absent with `GLCI-EXEC-DEPS-MISSING: run composer install first`. The test classifier MUST extract `FilePaths[]` from PHPUnit's `<file>:<line>` anchors.
- **Verifies:** §03 PHP detection table; §04 phase commands; §09 PHP classifier; AC-28-08 FilePaths sort/dedup.

### AC-28-40 — `glci push-fixed` and `glci clear` invoke their endpoints directly without phase execution

- **Given** the user runs `glci push-fixed` OR `glci clear` (NOT `glci run`),
- **When** the command executes,
- **Then** `glci push-fixed` MUST send a single `PUT /fixed-log` for the current `(RepoUrl, Branch, PipelineName)` triple WITHOUT running any lint/build/test phase — the command exists to manually mark a green pipeline when the server didn't get the auto-fired `/fixed-log` (per AC-28-17); `glci clear` MUST send `POST /clear-log` for the same triple, AND with `--all` it MUST send `POST /clear-log-all` for `(RepoUrl, Branch)` — affecting ALL pipelines on the branch. Both commands MUST honor `--no-push` (in which case they print the would-be request body to stdout and exit `0`); both MUST surface server `ErrorCode` verbatim per AC-28-26; both MUST NOT auto-trigger `/fixed-log` (no recursive auto-fire). Exit codes match the table in AC-28-11/12/13.
- **Verifies:** §04 `push-fixed` / `clear` / `clear --all` subcommands; §06 endpoint mapping; AC-28-17 auto-fired `/fixed-log`; AC-28-21 `--no-push` precedent.

---

## v5 audit-finding closure (Phase 153 Task A11g additions, AC-28-41..AC-28-43)

### AC-28-41 — Module cross-reference pin for spec/13 + spec/05 + spec/27 external dependencies (Lesson #29 + Lesson #36)  `[critical]`

- **Given** `spec/28-universal-ci-cli/05-config-resolution.md` `## Concurrency Posture (Normative cross-reference)` links to [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md) (DB+file concurrency) which in turn cites `spec/05-split-db-architecture/97-acceptance-criteria.md` AC-SD-22 (PRAGMA + retry) and `spec/27-spec-toolchain/97-acceptance-criteria.md` AC-T-28 (atomic-write resilience), AND files `08-ci-provider-bindings.md`, `09-output-classification.md`, `17-openapi-client.yaml`, `18-config-schema.json` are present on disk in this module's directory,
- **When** an audit harness scoped to spec/28's bundle reports `[D4] Truncated Error Catalog and missing sections` (citing files 08/09/17/18 as "subsequent files missing") OR `[D5] Broken External References` (citing AC-22/AC-SD-22/AC-T-28 as unresolved),
- **Then** the auditor MUST treat both findings as **harness scope artifacts**, NOT spec defects — every cited file is present at its documented path (verifiable via `ls spec/28-universal-ci-cli/` against §99 inventory) AND every cited cross-module AC is present in its owning module per Lesson #36 (link-don't-restate). Restating AC-22 / AC-SD-22 / AC-T-28 inside spec/28 would create a dual-source drift class explicitly forbidden by spec/04 §4.3 (Phase 153 P3 precedent). The canonical inventory is §99 `## Module Inventory`; if the auditor's bundle truncated mid-`07-error-catalog.md` (line 107 closing `}` + ` ``` ` confirms file is complete), the harness 90 KB cap was hit — see `spec/17-consolidated-guidelines/34-full-tree-ai-audit-v6.md` § "Tier-1 walker" (Lesson #16).
- **Verifies:** the spec/28 module-kind = `module` declaration AND the cross-module link-not-restate contract; codifies **Lesson #29** + **Lesson #36** for tier-1-bounded auditors operating on per-module bundles. Mirror of spec/13 AC-24 + spec/03 AC-08 + spec/07 AC-35 + spec/10 AC-09 + spec/11 AC-10 + spec/12 AC-09 + spec/17 AC-10 + spec/18 AC-09 + spec/25 AC-AI-09..11. Until A8 (LLM-gateway re-score) unblocks, the cache will report v5 [D4] + [D5] findings citing these — this AC declares them stale-cache artifacts per Lesson #34.

### AC-28-42 — Stdout/stderr interleaving uses kernel pipe-merge, NOT pseudo-terminal  `[high]`

- **Given** §04 `## glci lint / build / test` step 3 specifies "Capture stdout + stderr **interleaved** with timestamps to preserve ordering",
- **When** a runner subprocess is spawned for any phase (lint/build/test/run),
- **Then** the CLI MUST merge stdout + stderr at the **OS pipe level** (`exec.Cmd.Stderr = exec.Cmd.Stdout` in Go; equivalent constructions in TS/PHP/Rust/C# runtimes) so the kernel's pipe FIFO discipline preserves byte-level ordering. The CLI MUST NOT allocate a pseudo-terminal (PTY) for the runner — runners detect TTY via `isatty(fd)` and emit ANSI escapes / progress bars / pager invocations that corrupt log parsing (the §04 env vars `CI=true`, `FORCE_COLOR=0`, `npm_config_progress=false` per AC-28-37 suppress most TTY-conditional output, but PTY allocation defeats those signals because `isatty` returns true). The CLI MUST NOT use two independent pipes round-robined in user space (separate `Stdout` + `Stderr` then multiplex via `select` / goroutines) because interleaving order then becomes user-space-scheduling-dependent and non-reproducible across runs (breaks AC-28-23 determinism). Each captured byte MUST be timestamped at read time with monotonic-clock millisecond resolution.
- **Verifies:** §04 interleaved-capture clause; AC-28-23 determinism (identical input → identical body); AC-28-37 TS env-var TTY suppression; AC-28-38 Go `CGO_ENABLED=0`; closes audit-v5 D3 MED ambiguity (PTY vs pipe).

### AC-28-43 — `GLCI-DOCTOR-PROFILE-NOT-FOUND` server-side resolves `RepoUrl` → `GitProfile`; CLI is passive  `[low]`

- **Given** §04 `glci doctor` step 4 maps server `404` → `GLCI-DOCTOR-PROFILE-NOT-FOUND` AND §07 catalog row "Code GLCI-DOCTOR-PROFILE-NOT-FOUND" cites server `GL-VALIDATION-PROFILE-NOT-FOUND` with caller action "Add the GitProfile in admin UI",
- **When** the doctor probe `GET /get-logs?q=<repo>&limit=0` returns `404 GL-VALIDATION-PROFILE-NOT-FOUND`,
- **Then** the CLI MUST surface the server's `ErrorCode` verbatim per AC-28-26 — it MUST NOT attempt any local `GitProfile` lookup, MUST NOT cache profile state, MUST NOT prompt the user to "select a profile" (the runner has no profile concept — only a `RepoUrl` from `glci.toml` or auto-detection per §03). The `GitProfile` entity is a server-side admin-database row that maps `RepoUrl` → auth credentials + branch policies; the server performs the resolution and returns 404 if no match. The CLI's role is binary: forward the `RepoUrl`, surface the response. The caller-action prompt "Add the GitProfile in admin UI for this `RepoUrl`" (§07 row 41 prose) instructs the operator to navigate to the admin UI and create the missing profile keyed by `RepoUrl`.
- **Verifies:** §04 doctor 404 mapping; §07 GLCI-DOCTOR-PROFILE-NOT-FOUND row; AC-28-26 server `ErrorCode` verbatim surface; closes audit-v5 D1 LOW ambiguity (GitProfile undefined in CLI surface).

### AC-28-44 — `--parallel` failure isolation: per-runtime scope, aggregated worst-exit, opt-in `--fail-fast` (Task S28-01) `[medium]`

- **Given** §02 `## Concurrency Model` declares "runtimes run in parallel goroutines, separate ship queues" under `--parallel` AND §02 `## Failure Semantics` table defines per-phase outcomes for sequential runs,
- **When** `glci --parallel ts,php` executes and `ts.lint` exits non-zero while `php.build` is mid-flight,
- **Then** the `ts` runtime MUST skip its own `ts.build` + `ts.test` per the §02 Failure Semantics table, AND the `php` runtime MUST run to completion (success OR failure) without receiving any `SIGTERM`/`SIGINT` from `glci` originating in the `ts` failure — failure scope is **per-runtime goroutine**, never cross-runtime. Sibling cancellation is opt-in via `--fail-fast` (which propagates `SIGTERM` to ALL runtimes on first phase failure). Without `--fail-fast`, `glci` MUST wait for all runtimes to terminate, then exit with the **highest** observed exit code per precedence `4` (transport) > `2` (config) > `1` (phase) > `0` (success). External signals (`SIGINT` / `SIGTERM` to the `glci` parent) MUST propagate to ALL runtime subtrees and exit `130` / `143` respectively. Codified in §02 `### --parallel failure isolation (Normative)` subsection (4-row event table + aggregated-exit-code rule + 4-pattern forbidden list).
- **AND** per-runtime ship queues remain sealed per AC-28-22 — a failed runtime's ship queue MUST NOT be drained "first" to prioritize its diagnostic logs over a sibling's ongoing queue (cross-runtime queue reordering is forbidden).
- **Verifies:** §02 `## Concurrency Model` table (per-runtime goroutine declaration); §02 `### --parallel failure isolation (Normative)` (event table + forbidden patterns); §02 `## Failure Semantics` table (per-phase exit codes feeding the aggregated rule); AC-28-22 (per-runtime PipelineName separation, sealed ship queues); closes audit-v6 MEDIUM/D3 finding "Ambiguous behavior for parallel runtime failures — unclear if a failure in 'ts' should abort an ongoing 'php' runtime or just prevent its next phase".

---

### AC-28-45 — Cross-Module Externalized Citation Map (Lesson #36 + Lesson #37 — link-don't-restate anchor table)  `[critical]`

**Given** spec/28-universal-ci-cli is an integration-axis module (a CLI binary that orchestrates lints/builds/tests across multiple language runtimes AND ships logs to a server defined by spec/22) whose normative content references contract surfaces owned by other top-level spec modules — concretely (a) AC-28-41 already pins the spec/13 + spec/05 + spec/27 citation triad as a Lesson #29 + #36 anchor, (b) `00-overview.md` line 14 + AC-28-31 cite `spec/22-git-logs-v2/17-openapi.yaml` as the OpenAPI source-of-truth for `/append-log` + `/fixed-log` + `/get-logs`, (c) `05-config-resolution.md` cites spec/13 §97 AC-22 for runtime concurrency, (d) `07-error-catalog.md` ErrorCode taxonomy mirrors spec/03 + spec/22 §15 envelope shape, (e) `08-ci-provider-bindings.md` references spec/04 DDL conventions for the local cache schema, (f) `00-overview.md` lines 573+ cite 5 linter-scripts (the standard 5 — detect-changed-modules, validate-contracts, audit-spec-vs-code-v2, promote-artifact, update-consistency-report);

**When** an AI auditor walks spec/28 §97 (the tier-1 contract surface) and encounters any of these externalized citations OR a downstream contributor needs to follow the dependency chain to verify a normative claim,

**Then** the auditor MUST find the canonical anchor for each external citation in the table below — every row is a Lesson-#36 link-don't-restate boundary (the citation lives ONCE in its owning module's §97; spec/28 cites it but never restates it):

| External cite | Owning module + AC | Cited from spec/28 file | Citation purpose | Restate-in-28 forbidden? |
|---|---|---|---|---|
| spec/22-git-logs-v2/17-openapi.yaml | spec/22 §97 AC-44..AC-58 (REST endpoint contract) + spec/22/17-openapi.yaml (the schema itself) | `00-overview.md` L14 + AC-28-31 (OpenAPI parity) + `06-log-shipping-contract.md` | Server-side OpenAPI specification for `/append-log`, `/fixed-log`, `/get-logs`, `/profile/me` — the wire contract spec/28 client implements | **YES** — endpoint paths + request/response schemas + error envelopes live in spec/22 OpenAPI; spec/28 generates client stubs from it, NEVER duplicates the schema (would diverge silently) |
| spec/13-generic-cli §97 AC-22 | spec/13 §97 AC-22 + spec/13/10-database.md (implementer mirror, Phase 153 P3) | AC-28-41 (already pinned) + `05-config-resolution.md` `## Concurrency Posture` cross-ref | SQLite locking strategy for local cache: `journal_mode=WAL`, `busy_timeout=5000`, retry+jitter | **YES** — full PRAGMA + retry contract lives in spec/13 §97 AC-22; spec/28 cites the AC, never restates the PRAGMA table |
| spec/05-split-db-architecture | spec/05 §97 AC-SD-21..23 | AC-28-41 (already pinned) + L301 (cited in §97 cross-refs) | Split-DB pattern: SQL identifier double-quoting + Go struct tags + busy_timeout retry | **YES** — pattern + identifier conventions live in spec/05 §97; spec/28 inherits, never re-derives |
| spec/04-database-conventions | spec/04 §00 + §02-schema-design.md AC-09 (boolean storage) | `08-ci-provider-bindings.md` (local cache schema) + AC-28-32 (provider-binding DDL) | Cross-language boolean storage convention (P48-2): SQLite `INTEGER 0/1`, MySQL `TINYINT(1)`, Postgres `BOOLEAN` | **YES** — boolean storage table + per-engine DDL live in spec/04 §02 v3.4.1; spec/28 local cache inherits, never restates |
| spec/03-error-manage | spec/03 §97 (ErrorCode envelope contract) | `07-error-catalog.md` (GLCI-* error code family) | Error envelope shape inherited and extended with `GLCI-*` prefix; CLI exit-code mapping | **YES** — envelope shape + classification rules live in spec/03 §97; spec/28's `GLCI-*` codes extend the contract per AC-28-26 (server `ErrorCode` verbatim surface) |
| spec/27-spec-toolchain (script anchors) | spec/27 §97 (slot 02/03/14/18/24 — standard 5-script set) | `00-overview.md` L573/585/597/611/625 + AC-28-41 (already pinned) | Mechanical PR-time gates: changed-module detection, contract validation, deterministic spec-vs-code audit, artifact promotion, consistency-report regen | **YES** — script CLI surfaces + exit-code contracts live in spec/27 §97 per-slot ACs; spec/28 cites script paths, never replicates CLI logic |

**AND** any future contributor authoring new normative content in spec/28 that references a contract surface owned by another top-level module MUST add a row to the table above (citation + owning module/AC + spec/28 file + purpose + restate-forbidden flag) before the new content ships — the table IS the audit-followable dependency chain. **This AC supersedes-and-extends AC-28-41**: AC-28-41 covers the spec/13 + spec/05 + spec/27 triad as a stale-cache rebuttal; AC-28-45 broadens the surface to all 6 externalized citation classes with the same link-don't-restate contract. AC-28-41 remains the canonical stale-cache rebuttal AC; AC-28-45 is the canonical citation-map AC. Both are normative — AC-28-45 does NOT obsolete AC-28-41;

**AND** any auditor finding citing "external dependency unresolved" or "dangling cross-module reference" against the 6 rows above MUST be classified as a stale-cache artifact (the anchor exists in the cited owning module's §97 — verify with `rg -n "AC-XX" spec/NN-*/97-acceptance-criteria.md` before flagging);

**AND** the table is **append-only** within a phase (rows MAY be added, never reworded);

**AND** restating any of the linked contracts inline within spec/28 is **FORBIDDEN** (Lesson #36 dual-source drift class) — every row's "Restate-in-28 forbidden?" cell is `YES` by construction. The CLI/server boundary is the architectural manifestation of this rule: spec/28 implements a *client* for spec/22's wire contract — replicating the schema or error catalog would create a dual-source drift class that silently diverges as spec/22 evolves.

- **Verifies:** the cross-module externalized citation contract for spec/28 — every external dependency (spec/22 OpenAPI + spec/13 concurrency + spec/05 split-DB + spec/04 DDL + spec/03 error envelope + spec/27 CI gates) has an explicit normative anchor in the table above. Codifies **Lesson #36** (link-don't-restate cross-module boundary) + **Lesson #37** (integration-axis module co-needs Lesson #19 + Lesson #36). Mirror of spec/22 AC-79 + spec/23 AC-ADB-17 + spec/24 AC-ADS-14 + spec/26 AC-25 (Phase 154 C-Sweep batch). Supersedes-and-extends AC-28-41 (which remains the canonical stale-cache rebuttal AC for the spec/13 + spec/05 + spec/27 subset).

---

### AC-28-46 — Sibling File Delegation Map (Lesson #21 + Lesson #39 — intra-module audit-followability)  `[critical]`

**Given** spec/28-universal-ci-cli is a top-level module with **9 normative sibling files** (`01-glossary-and-enums.md` through `09-output-classification.md`) plus the tier-1 contract trio (`00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`), and an AI auditor walking only §97 (per the tier-1 walker contract codified in spec/27 slot 34 AC-34-09) MUST be able to follow every normative claim in any sibling file back to a governing AC family in this §97;

**When** an auditor encounters a normative subsection in any sibling file (e.g. the runtime-detection table in `03-runtime-detection.md`, the `glci` subcommand surface in `04-command-surface.md`, the CI ENV variable matrix in `08-ci-provider-bindings.md`),

**Then** the auditor MUST find the file's governing AC family in the table below — every row binds one sibling file to (a) the AC family that audits it, (b) the tier-visibility class (tier-1 contract, normative implementer, informative-exempt), (c) the **restate-forbidden** flag indicating whether content in the row's file may be restated elsewhere in spec/28:

| Sibling file | Content kind | Governing §97 AC family | Tier visibility | Restate-forbidden? |
|---|---|---|---|---|
| `01-glossary-and-enums.md` | Glossary + ErrorCode enum + Phase enum + Runtime enum | AC-28-07 (canonical phase enum) + AC-28-26 (server ErrorCode verbatim) + AC-28-41 (cross-module ErrorCode citation) | normative implementer | **YES** — enum values ship from spec/03 + spec/22; spec/28 names them, never re-derives |
| `02-architecture.md` | Component diagram + client/server boundary + concurrency model | AC-28-22 (per-runtime PipelineName) + AC-28-44 (`--parallel` failure isolation) + AC-28-45 row 1 (spec/22 OpenAPI client/server boundary) | normative implementer | **YES** — wire contract lives in spec/22; spec/28 implements client only |
| `03-runtime-detection.md` | Per-runtime marker tables (TS / Go / PHP / Rust / C# / Python) + ambiguity rules | AC-28-01..AC-28-06 (detection contract) + AC-28-32 (nested-monorepo rejection) + AC-28-37..AC-28-39 (per-runtime tool selection) | normative implementer | **YES** — detection invariants live in §97 ACs; this file is the lookup table they reference |
| `04-command-surface.md` | `glci` subcommand list + flag matrix + exit-code table | AC-28-07 (canonical phase enum) + AC-28-21 (`--no-push`) + AC-28-29..AC-28-31 (exec error family) + AC-28-40 (`push-fixed`/`clear` direct invocation) + AC-28-44 (`--parallel`) | normative implementer | **YES** — subcommand contracts owned by §97 ACs; this file enumerates them |
| `05-config-resolution.md` | Config file precedence + JSON Schema + concurrency posture cross-ref | AC-28-24 (HTTPS required) + AC-28-25 (backoff length) + AC-28-27 (JSON Schema validation) + AC-28-45 row 2 (spec/13 §97 AC-22 concurrency cross-ref) | normative implementer | **YES** — concurrency owned by spec/13 §97 AC-22 (Lesson #36 cross-ref); validation rules owned by AC-28-24..27 |
| `06-log-shipping-contract.md` | NDJSON envelope + retry/backoff + `/append-log` + `/fixed-log` semantics | AC-28-08..AC-28-18 (log shipping family) + AC-28-23 (determinism) + AC-28-31 (stream recovery) + AC-28-36 (buffer cap) + AC-28-45 row 1 (OpenAPI source-of-truth) | normative implementer | **YES** — wire schema lives in spec/22 OpenAPI; this file is the client-side behavior contract |
| `07-error-catalog.md` | `GLCI-*` ErrorCode catalog + exit-code mapping + classification rules | AC-28-26 (server ErrorCode verbatim) + AC-28-41..AC-28-43 (extended catalog) + AC-28-45 row 5 (spec/03 envelope inheritance) | normative implementer | **YES** — envelope shape lives in spec/03 §97; spec/28 extends with `GLCI-*` prefix only |
| `08-ci-provider-bindings.md` | Per-provider ENV detection matrix (GitHub / GitLab / Azure / Bitbucket / generic) + local cache DDL | AC-28-19..AC-28-20 (GitHub + URL normalization) + AC-28-33..AC-28-34 (GitLab + others) + AC-28-45 row 4 (spec/04 DDL conventions) | normative implementer | **YES** — boolean storage lives in spec/04 §02 v3.4.1; provider auto-fill rules in §97 ACs |
| `09-output-classification.md` | Stdout/stderr interleaving + ANSI stripping + line classification | AC-28-09 (output classification) + AC-28-42 (kernel pipe-merge, NOT pseudo-terminal) + AC-28-35 (telemetry prohibition at network layer) | normative implementer | **YES** — interleaving contract owned by AC-28-42; this file is the implementation surface |
| `00-overview.md` | Tier-1 module entry-point + table of contents + cross-module dependency narrative | AC-28-41 + AC-28-45 (cross-module citation map — both rooted here) | tier-1 contract (auto-bound) | N/A (tier-1 is the audit entry point, not a sibling) |
| `97-acceptance-criteria.md` | This file (normative AC catalog) | self | tier-1 contract (auto-bound) | N/A |
| `98-changelog.md` | Version history + per-phase AC additions | self (AC-31-31 lockstep ledger) | tier-1 contract (auto-bound) | N/A |
| `99-consistency-report.md` | Inventory + Validation History + Summary | self (slot 26 freshness gate) | tier-1 contract (auto-bound) | N/A |

**AND** any future contributor adding a new sibling file (`10-*.md` or higher) MUST add a row to the table above before the file ships — the row MUST cite (a) the governing AC family in this §97, (b) the tier visibility, (c) the restate-forbidden flag. **No new sibling file may be merged unbound.**

**AND** any auditor finding citing "normative content in `NN-*.md` not bound from §97" against the 9 normative siblings above MUST be classified as a stale-cache or stale-walker artifact (the binding lives in the table above — verify with `rg -n "AC-28-NN" spec/28-*/97-acceptance-criteria.md` before flagging);

**AND** the table is **append-only within a phase** (rows MAY be added when new files ship; existing rows MAY be extended with additional governing-AC citations, but the (file, content kind) pair is immutable);

**AND** restating a sibling file's normative content in a different sibling file is **FORBIDDEN** (Lesson #25 dual-source drift class) — every row's "Restate-forbidden?" cell is `YES` for normative siblings by construction. Cross-references between siblings MUST link, not restate (Lesson #36 cross-module rule applied to the intra-module axis per Lesson #39).

- **Verifies:** the intra-module sibling-file delegation contract for spec/28 — every one of the 9 normative sibling files has an explicit governing-AC binding visible from this tier-1 §97 file. Codifies **Lesson #21** (audit-boundary < verification-boundary closure pattern) on its **second axis** (intra-module sibling files, per **Lesson #39**) — the first axis (cross-language sub-folders, e.g. spec/02 AC-CG-21) and the cross-module axis (e.g. spec/22 AC-79, spec/28 AC-28-45) leave intra-module sibling-file binding as a third orthogonal surface this AC closes for spec/28. Mirror of spec/22 AC-80 (33-row delegation map for spec/22's sibling files, Phase 154). Companion to AC-28-45 (cross-module citation map) — together AC-28-45 + AC-28-46 form the **complete tier-1 audit-followability triplet** for spec/28 per Lesson #37 (integration-axis modules need both Lesson #19/#21 closure AND Lesson #36 closure). Closes the Lesson #39 spec/28 sweep candidate identified in Phase 154 closing memo (4 of 9 normative siblings were unbound pre-AC-28-46: `01-glossary-and-enums`, `02-architecture`, `03-runtime-detection`, `04-command-surface`).

---

## v2 scope narrowing (Phase 155 — AC-28-47)

### AC-28-47 — Module Kind: GitHub Actions Only (v2 scope pin — Lesson #29)  `[critical]`

- **Given** the spec/28 module front-matter declares `axis: normative-contract`
  AND [`00-overview.md` §Scope (v2 — Normative)`](./00-overview.md#scope-v2--normative) declares **v2 ships GitHub Actions support ONLY**
  AND [`08-ci-provider-bindings.md`](./08-ci-provider-bindings.md) `## Provider Detection Order` table marks `gitlab`/`azure`/`bitbucket`/`shell` rows as **DEPRECATED-v2 (reference only)**
  AND [`03-runtime-detection.md`](./03-runtime-detection.md) `> Scope inheritance` callout points to the §00 banner;
- **When** an implementer reads any sibling file, reference YAML block, or `Locked Decision 11` table row that mentions a non-GitHub provider (`GitLab CI`, `Jenkins`, `CircleCI`, `Azure Pipelines`, `Bitbucket Pipelines`, `generic shell`, `universal CI adapter`, `multi-provider auto-detection`);
- **Then** that mention MUST be treated as **historical reference for the v3 plugin model** and the implementer MUST NOT ship a v2 binary that auto-detects, branches on, or harvests env vars for any provider other than `github` (`GITHUB_ACTIONS=true`).
- **AND** any future v2 patch that re-introduces a non-GitHub runtime branch MUST be rejected at review with a citation to this AC;
- **AND** Locked Decision 11 of `00-overview.md` (which still lists GitLab/Azure/Bitbucket for legacy continuity) is **superseded by the §00 Scope banner** per Lesson #36 (link-don't-restate; the banner is the canonical surface);
- **AND** the `Phase 55` GitLab/Azure YAML blocks and the `Phase 63` `CiProvider` enum (lines 121-156 + 237-244 of `00-overview.md`) are retained for v3 continuity but MUST NOT be cited as v2 implementation requirements;
- **AND** any auditor finding of the form "spec/28 contradicts itself: GitHub-only banner + multi-provider table" MUST be classified as a **stale-cache or pre-Phase-155 audit artifact** — the contradiction-resolution rule is pinned in this AC + the §00 banner;
- **AND** the `## Out of Scope (v1)` section of `00-overview.md` (Java/Maven/Rust/Python) is orthogonal to this AC and remains in force unchanged.

**Forbidden patterns in v2 implementations** (auditor MUST flag any of these as `GLCI-CONTRACT-V2-SCOPE-VIOLATION`):

| # | Pattern | Why forbidden |
|---|---------|---------------|
| 1 | Switch/match arm dispatching on `GITLAB_CI`, `TF_BUILD`, `BITBUCKET_BUILD_NUMBER` env vars | Multi-provider auto-detection — v3 only |
| 2 | Helper function named `detectProvider()` returning a multi-valued enum (anything beyond `{github, none}`) | Universal CI adapter pattern — v3 only |
| 3 | Config key `[ci_provider].override` accepting non-`github` value | DEPRECATED-v2 in §08; supersedes per AC-28-47 |
| 4 | YAML drop-in template under `.gitlab-ci.yml`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, or `Jenkinsfile` shipped as a v2 release artifact | Reference YAML blocks in §00/§08 are documentation-only |
| 5 | README/docs claiming v2 supports any provider beyond GitHub Actions | Marketing/scope contradiction |

**v3 unblock trigger:** When a v3 plugin model lands (separate spec module, e.g. `spec/30-ci-provider-plugins/`), this AC's GH-only constraint relaxes for v3 binaries only; v2 LTS branch retains AC-28-47 in force until end-of-life.

- **Source:** Phase 155 A1 (§00 scope banner) + A2 (§03 inheritance pointer) + A3 (§08 DEPRECATED-v2 labels) + A4 (this AC).
- **Verifies:** §00 `## Scope (v2 — Normative)` banner + §03 `> Scope inheritance` callout + §08 `## Provider Detection Order` `**v2 Status**` column + §08 per-provider YAML heading labels (`(ACTIVE — v2 canonical)` / `(DEPRECATED-v2 — reference only)`). Codifies **Lesson #29** (Module-kind pin in §97 is the canonical fix for scope-narrowing — explicit "this module is X kind, NOT Y kind" AC with line-anchored citations to the misreadable content; mirror of AC-AI-09/10/11 in spec/25 for the audit-corpus axis, applied here to the scope-narrowing axis). Closes the contradiction-class between Locked Decision 11's multi-provider list and the §00 v2-scope banner — auditor stale-cache findings of "spec/28 contradicts itself" MUST cite this AC for resolution.

---

## Phase 156 — Log-shipping timeout discipline (audit-v6 D3 closure)

### AC-28-48 — Log-shipping per-request timeout + max wall-clock cap (Normative)  `[medium]`

- **Given** the spec/28 CLI is a HTTP client of `spec/22-git-logs-v2` endpoints (`/append-log`, `/fixed-log`, `/get-logs`, `/profile/me`)
  AND every network call MUST be bounded so that a hung server cannot wedge the runner indefinitely
  AND audit-v6 D3 finding "Missing timeout for log shipping" identifies that pre-Phase-156 prose only specified retry/backoff but no per-request or total wall-clock bound;
- **When** the CLI issues any HTTP request to a server endpoint;
- **Then** the request MUST be bounded by `PUSH_REQUEST_TIMEOUT_MS` (default `30000`, configurable via `glci.toml` `push.request_timeout_ms`, range `1..120000`)
  AND the entire ship-cycle (initial attempt + all retries + jitter delays) MUST be bounded by `PUSH_TOTAL_DEADLINE_MS` (default `180000`, configurable via `push.total_deadline_ms`, range `request_timeout_ms+1..600000`)
  AND retries on `5xx`/network MUST use exponential backoff with **±25% jitter** (`delay_n = backoff_ms * 2^n * (0.75 + rand()*0.5)`) mirroring [`spec/27-spec-toolchain` §97 AC-T-28 R3](../27-spec-toolchain/97-acceptance-criteria.md) (link-don't-restate per Lesson #36).
- **AND** termination triggers form a closed enumeration `{SUCCESS_2XX, EXIT_3_4XX, EXIT_4_RETRIES_EXHAUSTED, EXIT_4_DEADLINE_EXCEEDED, ATTEMPT_TIMEOUT_RETRY}` (first match wins; `EXIT_4_DEADLINE_EXCEEDED` is distinct from `EXIT_4_RETRIES_EXHAUSTED` because the budget, not the count, was the limit) — surfaced as `GLCI-PUSH-DEADLINE-EXCEEDED` (NEW error code) and `GLCI-PUSH-RETRIES-EXHAUSTED` (existing) respectively;
- **AND** Streaming Mode (`--stream`, chunked transfer) MUST also honour `PUSH_TOTAL_DEADLINE_MS` — stream-aborts mid-chunk surface as `GLCI-PUSH-DEADLINE-EXCEEDED`, NOT as a successful partial ship.

**Forbidden patterns** (auditor MUST flag any as `GLCI-CONTRACT-TIMEOUT-VIOLATION`):

| # | Pattern | Why forbidden |
|---|---------|---------------|
| 1 | Go `&http.Client{}` literal without `Timeout` field | Unbounded request — kernel-level only, can hang indefinitely |
| 2 | TS `axios.create({})` without `timeout` option | Unbounded XHR — Node default is ∞ |
| 3 | PHP `new GuzzleClient([])` without `connect_timeout` AND `timeout` | Both bounds required (connect + read) |
| 4 | Rust `reqwest::Client::new()` without `.timeout()` builder call | Unbounded request |
| 5 | C# `new HttpClient()` with default `Timeout = TimeSpan.FromSeconds(100)` left untouched | 100 s default exceeds `PUSH_REQUEST_TIMEOUT_MS` ceiling |
| 6 | Treating timeout as `4xx`-class error | Skips retry — timeout is network-class, MUST feed retry loop |
| 7 | Retrying after `PUSH_TOTAL_DEADLINE_MS` is reached | Hard deadline; retry loop MUST honour it |

- **Source:** audit-v6 cache `.lovable/cache/audit-ai/28-universal-ci-cli.json` D3 finding "Missing timeout for log shipping"; Phase 156 (this AC + `06-log-shipping-contract.md` `## Request Timeout & Retry Discipline (Normative)` section).
- **Verifies:** `06-log-shipping-contract.md` `## Request Timeout & Retry Discipline (Normative)` section (timeout table + retry envelope + termination triggers + 7 forbidden patterns). Codifies **Lesson #22** (closed Exception Ledger replaces open "etc." phrases — termination triggers are a 5-state closed enum, forbidden patterns are a 7-row closed table) + **Lesson #36** (jitter formula links to spec/27 AC-T-28 R3, never restated). Closes audit-v6 D3 MEDIUM finding.

---

## Worked Examples

> Non-normative `kind: example` — illustrative implementations of opaque ACs. If example and AC ever diverge, the AC wins.

### WE-01 — AC-28-12 / AC-28-13 retry envelope walked

**Setup:** `max_retries=3`, `backoff_ms=[500, 2000, 8000]`, server scripted to return `502, 502, 502, 200`.

**Wall-clock trace (T=0 at first POST):**
| T (ms) | Event | Notes |
|---:|---|---|
| 0 | POST /append-log → 502 | attempt 1 of 4 (initial + 3 retries) |
| ~5 | sleep 500 ms | `backoff_ms[0]` |
| 505 | POST /append-log → 502 | attempt 2 |
| ~510 | sleep 2000 ms | `backoff_ms[1]` |
| 2510 | POST /append-log → 502 | attempt 3 |
| ~2515 | sleep 8000 ms | `backoff_ms[2]` |
| 10515 | POST /append-log → 200 | attempt 4 succeeds |
| 10520 | exit 0 | one logical phase recorded server-side (idempotency) |

**Negative path (AC-28-13):** if attempt 4 also returns 502, the CLI MUST exit `4` with `GLCI-PUSH-RETRIES-EXHAUSTED`. No 5th attempt — `max_retries` is a hard cap.

**Forbidden behaviours (would break AC-28-12):**
- Sleeping less than the `backoff_ms[i]` floor (e.g. 400 ms instead of 500 ms).
- Treating 502 as 4xx-class and aborting on attempt 1 (violates §06 5xx-is-transient).
- Issuing a 5th retry beyond `max_retries`.
- Producing two logical phase records server-side because of the prior 502s (idempotency violation — server keys on `(repo, sha, phase)` not on attempt count).

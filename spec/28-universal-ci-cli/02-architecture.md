# Architecture

**Version:** 1.1.0  
**Updated:** 2026-05-03

---

## Process Model

`glci` is a single static binary. One invocation = one process = one set of phases for one commit. No daemons, no background workers, no shared state across invocations.

```
┌─────────────────────────────────────────────────────────────┐
│  glci run --phases lint,build,test                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1. config.Resolve()       (file → env → flag)       │   │
│  │ 2. ci.Harvest()           (CI env vars → defaults)  │   │
│  │ 3. detect.Plan()          (lockfiles → phase plan)  │   │
│  │ 4. doctor.Preflight()     (auth ping, binaries)     │   │
│  │ 5. for phase in plan:                                │   │
│  │      a. exec.Run(runner, args, captureOut)           │   │
│  │      b. classify.Lines(out)  → Logs / ErrorLogs      │   │
│  │      c. ship.Push(payload, mode)                     │   │
│  │      d. record(exitCode, errorCount)                 │   │
│  │ 6. ship.MaybeFixed()      (if previous run failed)  │   │
│  │ 7. exitCode.Compute()                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Layered Design

```
┌─────────────────────────────────────────────────┐
│  cmd/         (cobra commands; thin wiring)     │
├─────────────────────────────────────────────────┤
│  internal/orchestrator   (phase loop, ordering) │
├─────────────────────────────────────────────────┤
│  internal/detect   internal/exec   internal/ship│
│  internal/config   internal/ci     internal/auth│
│  internal/classify internal/doctor              │
├─────────────────────────────────────────────────┤
│  pkg/api    (typed structs for v2 endpoints)    │
│  pkg/errors (GLCI-* taxonomy, see §07)          │
└─────────────────────────────────────────────────┘
```

**Rules of the layering:**

1. `cmd/` MUST NOT touch `pkg/api` directly — it goes through `internal/orchestrator`.
2. `internal/*` packages MUST NOT import each other in a cycle. Allowed direction is downward only (orchestrator → detect/exec/ship → api).
3. `pkg/*` is the only externally importable surface; everything else stays `internal/`.
4. No package may import `net/http` directly except `internal/ship` and `internal/auth`.

---

## Plugin Model (forward-looking)

A new runtime is added by implementing this interface in `internal/detect`:

```go
type RuntimePlugin interface {
    ID() Runtime                              // "ts" | "go" | "php" | …
    Detect(repoRoot string) (bool, error)     // marker presence
    Phases() []PhaseDef                       // (Phase, Runner, DefaultArgs)
    EnvCheck() []DoctorCheck                  // binary versions, etc.
}
```

v1 ships three plugins (`ts.go`, `go.go`, `php.go`). v1.1 adds `python.go`, `rust.go`, `java.go` without touching the orchestrator.

A runtime plugin MUST be deterministic — given the same `repoRoot`, `Detect()` and `Phases()` MUST always return the same result.

---

## Concurrency Model

| Phase | Default | `--parallel` |
|-------|---------|--------------|
| Within one runtime | sequential `lint → build → test` | sequential (parallelism inside runners only) |
| Across runtimes (e.g. ts+php) | sequential by runtime | runtimes run in parallel goroutines, separate ship queues |

`--parallel` is opt-in only. Default sequential ordering keeps log streams readable in the admin UI.

---

## Failure Semantics

| Phase outcome | Continue subsequent phases? | Ship logs? | Exit code |
|---------------|-----------------------------|------------|-----------|
| `lint` fails | NO (default) — `--keep-going` overrides | YES | `1` |
| `build` fails | NO | YES | `1` |
| `test` fails | N/A (last phase) | YES | `1` |
| `ship` fails after retries | (does not affect phase decision) | YES if streaming partial | `4` (overrides phase exit code) |

A ship failure NEVER hides a phase failure: if both happen, exit code is `4` (transport) but `ErrorCount` from the phase is preserved in any logs that did make it through.

### `--parallel` failure isolation (Normative)

Under `--parallel`, runtimes execute in **independent goroutines with disjoint failure scopes**. A phase failure in runtime *R₁* (e.g. `ts.lint` exits non-zero) MUST NOT abort, signal, or cancel an in-flight phase in any sibling runtime *R₂* (e.g. an ongoing `php.build`). Only *R₁*'s own subsequent phases are skipped per the table above.

| Event | Sibling runtime impact | Process-tree impact | Exit code |
|---|---|---|---|
| Single-runtime phase failure | NONE — siblings run to completion | sibling subprocesses receive NO `SIGTERM`/`SIGINT` from `glci` | aggregated per "Aggregated exit code" rule below |
| `glci` receives `SIGINT` (Ctrl-C) | ALL runtimes propagate `SIGTERM` to their child subprocess tree | full tree shutdown | `130` |
| `glci` receives `SIGTERM` | ALL runtimes propagate `SIGTERM` to their child subprocess tree | full tree shutdown | `143` |
| `--fail-fast` flag set | First failure cancels ALL siblings via `SIGTERM` | full tree shutdown | first non-zero phase exit code |

**Aggregated exit code (without `--fail-fast`):** `glci` waits for ALL parallel runtimes to terminate (success or failure), then exits with the **highest** observed exit code (precedence: `4` transport > `2` config > `1` phase > `0`). A runtime that completed successfully does NOT lower the aggregated exit code. Ship-queue failures are accumulated per-runtime and surface independently in the aggregated code per the existing precedence rule.

**Forbidden patterns:**
- ❌ Cross-runtime cancellation on first phase failure WITHOUT `--fail-fast` (silent loss of sibling diagnostic logs).
- ❌ Inheriting `SIGTERM` from a sibling runtime's failed subprocess (each runtime owns its own process group).
- ❌ Lowering the aggregated exit code because a later sibling succeeded (last-writer-wins is a regression class — exit code reflects the worst outcome).
- ❌ Reordering ship queues across runtime boundaries to "drain" a failed runtime's logs first (per-runtime ship queues are sealed by AC-28-22).

---

## State

The CLI is **stateless across invocations**. The only persistent state is what the receiving Git Logs v2 server records (per AC-13: `Pipeline.HasError` survives until `/fixed-log` clears it). This means a PR pipeline that previously failed and now passes will automatically POST `/fixed-log` *because the server told us `HasError=1` from the previous run* — never because the CLI cached anything locally.

`glci doctor` is the only command that reads server state (`GET /get-pipeline-error-logs?…`); all other commands are write-only against the server.

# Runtime Detection

**Version:** 1.1.0  
**Updated:** 2026-05-07 (Phase 155 A2 — added Scope Inheritance pointer to §00 GitHub-Actions-only banner; this file is provider-agnostic by axis but shipping is GH-Actions-only)

> **Scope inheritance (Normative):** This file describes **language-runtime
> detection only** (ts / go / php). It contains no CI-provider rows, but
> implementers MUST treat the v2 shipping target as **GitHub Actions ONLY**
> per [§00 `## Scope (v2 — Normative)`](./00-overview.md#scope-v2--normative)
> and AC-28-47 (lands A4). Any provider examples elsewhere in this module
> (Phase 55 / 63 reference blocks, §08 binding tables) are advisory until v3
> per Lesson #36 (link-don't-restate; the §00 banner is canonical).

Detection is **lockfile- and manifest-based** — never extension-based. A repo with a stray `.ts` file but no `package.json` is NOT a TS project.

---

## Detection Order

```
for each runtime in [ts, go, php]:
    if any(marker exists for runtime in repoRoot):
        detected += runtime
return detected   // empty list → exit 2 with GLCI-DETECT-NONE
```

Order is fixed (`ts → go → php`) only for deterministic output of `glci detect`. All detected runtimes run; one cannot suppress another.

---

## Markers

### Runtime: `ts` (Node.js + TypeScript)

| Required | Optional bonus | Notes |
|----------|----------------|-------|
| `package.json` exists at `--cwd` | `tsconfig.json` (enables `tsc` build phase) | Without `tsconfig.json`, build phase falls back to `node --check` on entrypoint |

Lockfile picks the package manager:

| Lockfile present | Selected manager | Lint runner | Build runner | Test runner |
|------------------|------------------|-------------|--------------|-------------|
| `bun.lockb` or `bun.lock` | `bun` | `bun x eslint .` | `bun run build` (else `bun x tsc --noEmit`) | `bun test` (else `bun x vitest run`) |
| `pnpm-lock.yaml` | `pnpm` | `pnpm exec eslint .` | `pnpm run build` (else `pnpm exec tsc --noEmit`) | `pnpm test` (else `pnpm exec vitest run`) |
| `yarn.lock` | `yarn` | `yarn eslint .` | `yarn build` (else `yarn tsc --noEmit`) | `yarn test` |
| `package-lock.json` | `npm` | `npm exec eslint --` | `npm run build --if-present` (else `npm exec tsc -- --noEmit`) | `npm test` |
| _(none)_ | `npm` | same as above | same | same |

Multiple lockfiles → reject with `GLCI-DETECT-AMBIGUOUS-LOCK` (forces user to pick one in `glci.toml`).

### Runtime: `go` (Golang)

| Required | Notes |
|----------|-------|
| `go.mod` at `--cwd` | `go.work` honored when present (multi-module) |

Phase plan:

| Phase | Default runner |
|-------|----------------|
| lint  | `golangci-lint run ./...` (falls back to `go vet ./...` if golangci-lint absent — emits `GLCI-DOCTOR-LINTER-MISSING` warning) |
| build | `go build ./...` |
| test  | `go test -race -count=1 ./...` |

### Runtime: `php`

| Required | Notes |
|----------|-------|
| `composer.json` at `--cwd` | `vendor/` populated only required for test phase |

Phase plan, resolved with `vendor/bin` first, then `$PATH`:

| Phase | Default runner |
|-------|----------------|
| lint  | `phpcs` if `phpcs.xml(.dist)` present, else `phpstan analyse` if `phpstan.neon(.dist)` present, else `php -l` over `src/` |
| build | `composer dump-autoload --strict-psr` |
| test  | `phpunit` (looks for `phpunit.xml(.dist)` then `tests/` directory) |

---

## Override

`glci.toml` may pin runners explicitly:

```toml
[runtime.ts]
test_runner = "vitest"
test_args   = ["run", "--reporter=verbose"]

[runtime.php]
lint_runner = "phpstan"
lint_args   = ["analyse", "--level=9", "src"]
```

When overridden, detection still runs (for the `Detect()` boolean) but `Phases()` is replaced.

---

## Detection Output

`glci detect` prints (and exits 0) a stable JSON document:

```json
{
  "Cwd": "/path/to/repo",
  "Runtimes": [
    {
      "Id": "ts",
      "Manager": "bun",
      "Phases": [
        { "Phase": "lint",  "Runner": "bun",  "Args": ["x", "eslint", "."] },
        { "Phase": "build", "Runner": "bun",  "Args": ["x", "tsc", "--noEmit"] },
        { "Phase": "test",  "Runner": "bun",  "Args": ["test"] }
      ]
    }
  ],
  "Skipped": [
    { "Id": "go", "Reason": "no go.mod" }
  ]
}
```

Field names use PascalCase to match Git Logs v2 server conventions. Output is deterministic — same repo state → byte-identical JSON.

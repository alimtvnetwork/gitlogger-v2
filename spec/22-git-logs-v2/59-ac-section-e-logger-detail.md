# AC-04 — Logger Level Gating (Section E Detail)

**Status:** active · **Phase:** E-2 (logger-pipeline tier-1 binding) · **Bound from:** `97-acceptance-criteria.md` §AC-04
**Mirror class:** AC-05 (§53) · AC-12 (§55) · AC-23 (§56) · AC-11 (§57) · AC-34 (§58) — Phase D/E normative-surface promotions
**Generated:** 2026-05-10 (Lesson #19 audit-boundary pin; Lesson #36 link-don't-restate)

---

## Why this file exists

Pre-promotion AC-04 in §97 was a single dense paragraph (~3.2 KB) packing the level integer mapping, gating-at-call-boundary rule, forbidden-work enumeration, "filter-at-sink" anti-pattern, cached-integer rule, request-scoped cache semantics, fixed-six-levels rule, and AC-05 ordering — all without test enumeration. The audit walker chunk merge averaged d2 (testability) low. This file is the tier-1 binding surface with a 9-row T-LG-* matrix.

## Canonical level integer mapping (FIXED)

| Level | Integer | Use case |
|---|---:|---|
| `Trace` | 0 | Per-statement trace; very high volume |
| `Debug` | 1 | Developer debugging; off in production |
| `Info` | 2 | **Default** — lifecycle events |
| `Warn` | 3 | Recoverable anomalies |
| `Error` | 4 | Operation failed; user impact |
| `Fatal` | 5 | Plugin-stopping condition; near-silence emergency mode |

**Lower number = more verbose.** Storage in `ConfigKv.LogLevelMin` is the case-sensitive PascalCase string (per §23 convention); the cached integer is derived once at request bootstrap. Default `Info` if the row is missing or NULL.

The six levels are **FIXED**. Adding `Verbose`, `Critical`, or `Notice` requires a spec amendment + AC-04 update + DB migration. Implementations that silently extend the enum are SPEC VIOLATIONS.

## Normative invariants

1. **Gate at call boundary.** Every logger method (`Logger::debug`, `::info`, etc.) MUST compare `call_level` to the cached `min_level` integer FIRST.
2. **Constant-time early return.** If `call_level < min_level`: `return` immediately. No sink invocation. No `sprintf` / template interpolation. No context-array serialization. No JSON-encode of `$ctx`. No timestamp computation. No stack-frame inspection. No source-location lookup.
3. **No filter-at-sink.** Building the message and handing it to a sink that drops it is FORBIDDEN. Rationale: (i) wastes CPU on thrown-away strings, (ii) allocates intermediate strings/arrays pressuring the PHP allocator, (iii) defeats `LogLevelMin` as a performance valve operators turn down under load.
4. **Cached integer.** The `min_level` integer is read ONCE at request start (or autoloader bootstrap) and stored in a static / process-singleton. Re-reading `ConfigKv.LogLevelMin` from the DB on every log call is a SPEC VIOLATION (one DB query per dropped debug line would amplify load 10–100×).
5. **Request-scoped cache.** Operator UI updates to `LogLevelMin` take effect on the **next** request, not the current. The cache is request-scoped, NOT process-scoped.
6. **`Fatal` mode = near-silence.** When `LogLevelMin = Fatal` (5), only `Fatal` lines emit; `Error` (4) lines ARE dropped. This is the emergency throttle when the plugin is causing observable system stress.
7. **AC-05 dedup ordering.** Dedup (per AC-05) applies AFTER level gating. A line that fails AC-04 never reaches AC-05's dedup window — order matters for performance.

## Test invariants (T-LG-01..T-LG-09)

| T-ID | Invariant | Assertion |
|---|---|---|
| T-LG-01 | `LogLevelMin=Info` (2) → `Logger::debug(...)` returns immediately, sink uninvoked | `assertSame(0, $sink->callCount)` after 1000 debug calls |
| T-LG-02 | Constant-time gate: dropped call performs zero `sprintf` | `assertSame(0, $spy->sprintfCount)` under `Info` with debug calls |
| T-LG-03 | Dropped call performs zero `json_encode($ctx)` | `assertSame(0, $spy->jsonEncodeCount)` |
| T-LG-04 | Dropped call performs zero `debug_backtrace()` | `assertSame(0, $spy->backtraceCount)` |
| T-LG-05 | Cached integer: 1000 dropped debug calls perform ZERO DB queries | `assertSame(0, $db->queryCount)` after warm-up |
| T-LG-06 | Filter-at-sink anti-pattern detected: builder invoked for dropped line → fail | `assertSame(0, $messageBuilder->callCount)` for `Logger::trace` under `Info` |
| T-LG-07 | `LogLevelMin=Fatal` drops `Error` (4) lines | `assertSame(0, $sink->errorCount)` after `Logger::error(...)` calls |
| T-LG-08 | Operator update to `LogLevelMin` takes effect next request, NOT current | within request: `assertSame($prevMin, $logger->cachedMin)` after KV write |
| T-LG-09 | AC-05 dedup never sees lines that failed AC-04 gate | `assertSame(0, $dedupWindow->fingerprintCount)` for under-gated levels |

Test files: `test/AcLoggerLevelGatingTest.php` (PHPUnit) + `test/ac-logger-level-gating.bats` (bats CLI smoke for `wp git-logs log-level` admin command). Each test method MUST embed its T-ID; absence triggers `GL-TEST-COVERAGE-GAP` per AC-80. Deterministic monotonic-clock injection per AC-29 §5 for any test asserting timestamp absence.

## Worked example (T-LG-05 — cached integer / zero DB queries)

```php
// Bootstrap: cache once
$min = LogLevelType::fromString(ConfigKv::get('LogLevelMin', 'Info'))->toInt(); // 1 query
Logger::setCachedMin($min);

// Hot path: 1000 debug calls under Info
$dbQueryCountBefore = $db->queryCount;
for ($i = 0; $i < 1000; $i++) {
    Logger::debug("ingest row {$i}", ['row_id' => $i]);   // gated, zero work
}
$dbQueryCountAfter = $db->queryCount;

assert($dbQueryCountAfter === $dbQueryCountBefore);        // T-LG-05
assert($sink->callCount === 0);                            // T-LG-01
```

A naïve "filter-at-sink" implementation (where `Logger::debug` always builds the message + hands it to a sink that drops it) would: (a) call `sprintf` 1000× (T-LG-02 fail), (b) allocate 1000 context arrays (T-LG-03 fail), (c) measurably increase request latency on busy ingestion endpoints. The constant-time gate is the structural defense.

## Cross-references

- **§97 §AC-04** — slim binding stub (this file is the full body)
- **§06 `06-migrations-and-logger.md`** — logger subsystem prose contract
- **§03 `03-admin-ui.md`** — `ConfigKv` admin UI for `LogLevelMin` updates
- **§23 (`23-app-database` PascalCase convention)** — enum-string storage rule
- **AC-05** (§53) — dedup window applies AFTER gating; ordering invariant
- **AC-12** (§55) — streaming ingest logger respects the same gate
- **AC-29 §5** — deterministic monotonic-clock injection for tests
- **AC-80** — sibling test-file delegation + `GL-TEST-COVERAGE-GAP`

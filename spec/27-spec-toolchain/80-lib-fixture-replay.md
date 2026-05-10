# 80 — _lib/fixture_replay/ (shared harness library)

**Version:** 1.0.0  
**Updated:** 2026-05-10 (Session 52 audit-task A-32 — initial skeleton landing per the §27 §00 "Shared harness library contract", A-31 Sess-51)  
**Source:** [`linter-scripts/_lib/fixture_replay/`](../../linter-scripts/_lib/fixture_replay/)  
**Category:** Shared library (NOT a gate — imported by gates #17 + #18 + future integration-test gates)

---

## Purpose

Sole canonical home for the HTTP fixture-replay engine shared by gate #17 (`error-envelope-shape-check`, A-22 Sess-42) and gate #18 (`request-id-roundtrip-check`, A-23 Sess-43). Per the §27 §00 normative paragraph **"Shared harness library contract (A-31, Session 51)"**, re-defining `load_fixtures`, `replay`, or any of the exit-code constants outside this package is a gate #15 (`derives-from-restate-check`) violation at meta-level.

---

## Public API

| Symbol | Kind | Purpose |
|---|---|---|
| `load_fixtures(dir: Path) -> Iterator[Fixture]` | function | Yield every `*.json` fixture in deterministic order. Raises `HarnessSetupError` on unreadable input. |
| `replay(fixture, schema) -> ReplayResult` | function | Compare `fixture.response['body']` against the named OpenAPI schema component (closed shape: required-keys + no-extras). |
| `load_schema(path, component_name) -> dict` | function | Load one named component from `spec/22-git-logs-v2/17-openapi.yaml` (or sibling). Raises `HarnessSetupError` on missing file/component. |
| `Fixture` | dataclass | `(name, request, response, meta)` record. Frozen. |
| `ReplayResult` | dataclass | `(fixture_name, passed, violations: list[str])` record. Callers extend `violations` for per-gate assertions. |
| `HarnessSetupError` | exception | Raise → caller translates to exit-code 3. Distinct from invocation errors (exit 2) and contract violations (exit 1). |
| `EXIT_PASS = 0` | constant | Standard pass. |
| `EXIT_VIOLATION = 1` | constant | Contract drift detected. |
| `EXIT_INVOCATION = 2` | constant | Bad CLI args / unrecoverable wrapper failure. |
| `EXIT_HARNESS_SETUP = 3` | constant | **Sole sanctioned source of exit-code 3 across the entire toolchain.** |

---

## Usage (per-gate script template)

```python
import sys
from pathlib import Path
from _lib.fixture_replay import (
    EXIT_HARNESS_SETUP, EXIT_INVOCATION, EXIT_PASS, EXIT_VIOLATION,
    HarnessSetupError, load_fixtures, load_schema, replay,
)

def main() -> int:
    try:
        schema = load_schema(Path("spec/22-git-logs-v2/17-openapi.yaml"), "ErrorEnvelope")
        fixtures = list(load_fixtures(Path("linter-scripts/fixtures/error-envelope")))
    except HarnessSetupError as e:
        print(f"harness setup failure: {e}", file=sys.stderr)
        return EXIT_HARNESS_SETUP

    failed: list[str] = []
    for fx in fixtures:
        result = replay(fx, schema)
        # ... per-gate assertions extend result.violations here ...
        if not result.passed:
            failed.extend(result.violations)

    if failed:
        for v in failed:
            print(v, file=sys.stderr)
        return EXIT_VIOLATION
    return EXIT_PASS

if __name__ == "__main__":
    sys.exit(main())
```

---

## Constraints (normative)

- **No network**: `replay()` is in-process. Fixtures carry both the recorded request envelope and the recorded response envelope; the engine asserts shape/schema conformance, never live HTTP.
- **No PyYAML dependency at install time**: `schema_loader` defers the import to runtime and falls back to JSON parsing when PyYAML is unavailable.
- **Closed schema comparison**: `replay()` flags both missing-required-keys AND unexpected keys (closed shape).
- **`_lib/` reservation**: Only cross-gate shared code lives here. Per-gate logic stays in top-level `linter-scripts/check-*.py`. Future Wave-3+ integration-test gates MUST import from `_lib/fixture_replay/` or declare a §27 §00 normative exception.
- **Exit-code 3 monopoly**: No script in the toolchain may emit exit-code 3 outside `EXIT_HARNESS_SETUP`. Any other source is a §27 §00 violation.

---

## Cross-references

- §27 §00 normative contract: **"Shared harness library contract (A-31, Session 51)"** — the binding paragraph.
- Gate #17 — [`spec/27-spec-toolchain/00-overview.md` row 354](./00-overview.md) (`error-envelope-shape-check`).
- Gate #18 — [`spec/27-spec-toolchain/00-overview.md` row 355](./00-overview.md) (`request-id-roundtrip-check`).
- Gate #15 self-enforcement extension (A-31): scans `linter-scripts/check-*.py` for re-definition of `load_fixtures` / `replay` / `EXIT_HARNESS_SETUP`.

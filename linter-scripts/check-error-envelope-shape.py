#!/usr/bin/env python3
"""Gate #17 — error-envelope-shape-check (A-22 Sess-42 · activated A-34 Sess-53).

Asserts that every recorded HTTP error fixture conforms to the spec/22
`17-openapi.yaml` `ErrorEnvelope` schema (closed shape: required keys
present, no extra keys). Per-gate layer on top of the shared
`_lib/fixture_replay/` engine, per the §27 §00 "Shared harness library
contract" (A-31 Sess-51).

Exit codes (per §27 §00 A-31, mirrored from `_lib/fixture_replay/exit_codes.py`):
    0 — all fixtures conform
    1 — one or more shape violations
    2 — bad CLI invocation
    3 — harness setup error (missing fixtures, unreadable schema, …)

Re-defining `load_fixtures`, `replay`, or `EXIT_HARNESS_SETUP` here would
trip gate #15 (`derives-from-restate-check`) at meta-level — instead we
import them from `_lib/fixture_replay/`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure `_lib` is importable when run from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _lib.fixture_replay import (  # noqa: E402
    EXIT_HARNESS_SETUP,
    EXIT_INVOCATION,
    EXIT_PASS,
    EXIT_VIOLATION,
    HarnessSetupError,
    load_fixtures,
    load_schema,
    replay,
)

# Per-gate constants — narrow scope: only fixtures tagged as error responses.
SCHEMA_COMPONENT = "ErrorEnvelope"
DEFAULT_FIXTURES = Path("linter-scripts/fixtures/error-envelope")
DEFAULT_SCHEMA = Path("spec/22-git-logs-v2/17-openapi.yaml")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return EXIT_INVOCATION

    try:
        schema = load_schema(args.schema, SCHEMA_COMPONENT)
        fixtures = list(load_fixtures(args.fixtures))
    except HarnessSetupError as exc:
        print(f"[gate-17] harness setup error: {exc}", file=sys.stderr)
        return EXIT_HARNESS_SETUP

    failed = 0
    for fixture in fixtures:
        # Gate #17 only scopes fixtures whose meta tags them as error responses.
        if fixture.meta.get("kind") not in (None, "error"):
            continue
        result = replay(fixture, schema)
        if not result.passed:
            failed += 1
            for v in result.violations:
                print(f"[gate-17] {v}", file=sys.stderr)

    if failed:
        print(
            f"[gate-17] FAIL: {failed}/{len(fixtures)} fixtures violate "
            f"ErrorEnvelope shape",
            file=sys.stderr,
        )
        return EXIT_VIOLATION

    print(f"[gate-17] PASS: {len(fixtures)} fixtures conform to ErrorEnvelope")
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())

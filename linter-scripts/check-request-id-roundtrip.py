#!/usr/bin/env python3
"""Gate #18 — request-id-roundtrip-check (A-23 Sess-43 · activated A-34 Sess-53).

Asserts that every recorded HTTP fixture echoes the inbound
`X-Request-Id` request header back in the response (header or body
field, per fixture `meta.echo_path`). Per-gate layer on top of the
shared `_lib/fixture_replay/` engine, per the §27 §00 "Shared harness
library contract" (A-31 Sess-51).

Exit codes (mirrored from `_lib/fixture_replay/exit_codes.py`):
    0 — every fixture round-trips its request-id
    1 — one or more echo violations
    2 — bad CLI invocation
    3 — harness setup error

Re-defining `load_fixtures`, `replay`, or `EXIT_HARNESS_SETUP` here
would trip gate #15 — they are imported from `_lib/fixture_replay/`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _lib.fixture_replay import (  # noqa: E402
    EXIT_HARNESS_SETUP,
    EXIT_INVOCATION,
    EXIT_PASS,
    EXIT_VIOLATION,
    Fixture,
    HarnessSetupError,
    ReplayResult,
    load_fixtures,
    load_schema,
    replay,
)

# Gate #18 reuses ErrorEnvelope shape as a baseline (every response,
# error or not, carries the standard envelope) and adds the echo check.
SCHEMA_COMPONENT = "ErrorEnvelope"
DEFAULT_FIXTURES = Path("linter-scripts/fixtures/request-id")
DEFAULT_SCHEMA = Path("spec/22-git-logs-v2/17-openapi.yaml")
REQUEST_HEADER = "X-Request-Id"


def _check_echo(fixture: Fixture, base: ReplayResult) -> ReplayResult:
    """Layer the request-id echo assertion on top of the shape result."""
    req_headers = {k.lower(): v for k, v in (fixture.request.get("headers") or {}).items()}
    expected = req_headers.get(REQUEST_HEADER.lower())
    if not expected:
        return ReplayResult(
            fixture.name,
            False,
            base.violations + [f"{fixture.name}: request missing {REQUEST_HEADER}"],
        )

    echo_path = (fixture.meta or {}).get("echo_path", "header")
    violations = list(base.violations)

    if echo_path == "header":
        resp_headers = {k.lower(): v for k, v in (fixture.response.get("headers") or {}).items()}
        actual = resp_headers.get(REQUEST_HEADER.lower())
        if actual != expected:
            violations.append(
                f"{fixture.name}: response header {REQUEST_HEADER}={actual!r} "
                f"does not echo request {expected!r}"
            )
    elif echo_path == "body":
        body = fixture.response.get("body") or {}
        actual = body.get("requestId") if isinstance(body, dict) else None
        if actual != expected:
            violations.append(
                f"{fixture.name}: response.body.requestId={actual!r} does not "
                f"echo request {REQUEST_HEADER}={expected!r}"
            )
    else:
        violations.append(f"{fixture.name}: unknown meta.echo_path={echo_path!r}")

    return ReplayResult(fixture.name, not violations, violations)


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
        print(f"[gate-18] harness setup error: {exc}", file=sys.stderr)
        return EXIT_HARNESS_SETUP

    failed = 0
    for fixture in fixtures:
        base = replay(fixture, schema)
        result = _check_echo(fixture, base)
        if not result.passed:
            failed += 1
            for v in result.violations:
                print(f"[gate-18] {v}", file=sys.stderr)

    if failed:
        print(
            f"[gate-18] FAIL: {failed}/{len(fixtures)} fixtures fail "
            f"request-id round-trip",
            file=sys.stderr,
        )
        return EXIT_VIOLATION

    print(f"[gate-18] PASS: {len(fixtures)} fixtures round-trip {REQUEST_HEADER}")
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())

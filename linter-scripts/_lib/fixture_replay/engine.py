"""HTTP fixture-replay engine — shared core of gates #17 + #18.

Public API (per §27 §00 "Shared harness library contract", A-31 Sess-51):

* ``load_fixtures(dir) -> Iterator[Fixture]`` — yields fixture records,
  raises ``HarnessSetupError`` on unreadable input.
* ``replay(fixture, schema) -> ReplayResult`` — performs the in-process
  round-trip and shape comparison (no real network — fixtures carry both
  the request payload and the expected/observed response shape).

Per-gate logic (which §22 ACs to assert, which severities to scope, which
header echoes to verify) lives in the top-level ``check-*.py`` script.
This module is INTENTIONALLY minimal — it is the harness, not the gate.

Re-defining ``load_fixtures``, ``replay``, or any of the exit-code
constants outside ``linter-scripts/_lib/fixture_replay/`` is a gate #15
violation at meta-level.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List

from .schema_loader import HarnessSetupError


@dataclass(frozen=True)
class Fixture:
    """A single request/response fixture replayed against a schema.

    Attributes:
        name: Fixture id (filename stem, used in violation messages).
        request: Recorded request envelope (method, path, headers, body).
        response: Recorded response envelope (status, headers, body).
        meta: Free-form per-gate metadata (e.g. expected `requestId`
            echo path for gate #18, severity tag for gate #17).
    """

    name: str
    request: Dict[str, Any]
    response: Dict[str, Any]
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReplayResult:
    """Outcome of replaying one fixture against one schema.

    Attributes:
        fixture_name: Mirrors ``Fixture.name`` for log correlation.
        passed: True iff the response shape matched the schema and any
            per-gate assertions in ``meta`` were satisfied.
        violations: Human-readable violation strings (empty when passed).
    """

    fixture_name: str
    passed: bool
    violations: List[str] = field(default_factory=list)


def load_fixtures(fixtures_dir: Path) -> Iterator[Fixture]:
    """Yield every fixture in the directory, sorted by filename.

    Each fixture is a single ``*.json`` file with three top-level keys:
    ``request``, ``response``, and (optional) ``meta``.

    Args:
        fixtures_dir: e.g. ``linter-scripts/fixtures/error-envelope/``
            or ``linter-scripts/fixtures/request-id/``.

    Yields:
        ``Fixture`` records in deterministic (filename) order.

    Raises:
        HarnessSetupError: directory missing, no fixtures, or any
            fixture is unreadable / malformed JSON / missing required keys.
    """
    if not fixtures_dir.exists() or not fixtures_dir.is_dir():
        raise HarnessSetupError(f"fixtures directory not found: {fixtures_dir}")

    files = sorted(fixtures_dir.glob("*.json"))
    if not files:
        raise HarnessSetupError(f"no *.json fixtures in {fixtures_dir}")

    for path in files:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise HarnessSetupError(f"malformed fixture {path}: {exc}") from exc

        if not isinstance(raw, dict) or "request" not in raw or "response" not in raw:
            raise HarnessSetupError(
                f"fixture {path} missing required keys 'request' and/or 'response'"
            )

        yield Fixture(
            name=path.stem,
            request=raw["request"],
            response=raw["response"],
            meta=raw.get("meta", {}) or {},
        )


def replay(fixture: Fixture, schema: Dict[str, Any]) -> ReplayResult:
    """Replay one fixture against one schema component.

    v1 contract: assert that every key declared ``required`` in the
    schema is present in ``fixture.response['body']`` and that no
    response body key is absent from ``schema['properties']`` (closed
    shape). Per-gate assertions (header echo for gate #18, severity
    filter for gate #17) are layered by the calling script via the
    ``ReplayResult.violations`` list, which the script may extend
    before deciding pass/fail.

    Args:
        fixture: A record yielded by ``load_fixtures``.
        schema: A schema dict from ``schema_loader.load_schema``.

    Returns:
        A ``ReplayResult`` with ``passed`` reflecting shape conformance
        only. Callers extend ``violations`` for gate-specific checks.
    """
    violations: List[str] = []
    body = fixture.response.get("body", {}) or {}
    if not isinstance(body, dict):
        violations.append(
            f"{fixture.name}: response.body is not an object (shape gate requires JSON object)"
        )
        return ReplayResult(fixture.name, False, violations)

    required = set(schema.get("required", []) or [])
    properties = set((schema.get("properties", {}) or {}).keys())

    missing = sorted(required - body.keys())
    for key in missing:
        violations.append(f"{fixture.name}: missing required key {key!r}")

    extra = sorted(set(body.keys()) - properties) if properties else []
    for key in extra:
        violations.append(f"{fixture.name}: unexpected key {key!r} (closed schema)")

    return ReplayResult(fixture.name, not violations, violations)

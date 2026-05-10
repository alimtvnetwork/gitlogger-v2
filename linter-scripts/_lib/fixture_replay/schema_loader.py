"""OpenAPI schema loader for the shared fixture-replay engine.

Reads the §22 `17-openapi.yaml` `ErrorEnvelope` schema (and any sibling
schema named by integration-test gates) into a plain-dict representation
that `engine.replay()` can compare fixture responses against.

`HarnessSetupError` MUST be raised on any unreadable input — the caller
script translates this to `EXIT_HARNESS_SETUP` (= 3) per §27 §00 A-31.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class HarnessSetupError(RuntimeError):
    """Raised when the harness cannot read fixtures or schema.

    Caller MUST translate to `EXIT_HARNESS_SETUP = 3`. Distinct from
    invocation errors (bad CLI args → exit 2) and contract violations
    (drift detected → exit 1).
    """


def load_schema(schema_path: Path, component_name: str) -> Dict[str, Any]:
    """Load a single named schema component from an OpenAPI document.

    Args:
        schema_path: Path to `spec/22-git-logs-v2/17-openapi.yaml` (or sibling).
        component_name: Schema name under `components.schemas`
            (e.g. ``"ErrorEnvelope"``).

    Returns:
        The resolved schema dict (no `$ref` traversal — gates assert on the
        named top-level component only; deep refs are out of scope for v1).

    Raises:
        HarnessSetupError: schema file unreadable, malformed YAML/JSON, or
            named component missing.
    """
    if not schema_path.exists():
        raise HarnessSetupError(f"schema file not found: {schema_path}")

    raw = schema_path.read_text(encoding="utf-8")
    try:
        # YAML is a JSON superset for the subset OpenAPI uses; defer the
        # PyYAML import to runtime so the contract has no install-time dep.
        import yaml  # type: ignore[import-not-found]

        doc = yaml.safe_load(raw)
    except ImportError:
        # Fallback: assume `.json` form when PyYAML unavailable.
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise HarnessSetupError(
                f"PyYAML missing and {schema_path} is not valid JSON: {exc}"
            ) from exc
    except Exception as exc:  # pragma: no cover - yaml.YAMLError surface
        raise HarnessSetupError(f"malformed schema {schema_path}: {exc}") from exc

    components = (doc or {}).get("components", {}).get("schemas", {})
    if component_name not in components:
        raise HarnessSetupError(
            f"schema component {component_name!r} not found in {schema_path}"
        )
    return components[component_name]

"""Shared HTTP fixture-replay engine for §27 integration-test gates.

Sole canonical home for the harness shared by gate #17
(`error-envelope-shape-check`, A-22 Sess-42) and gate #18
(`request-id-roundtrip-check`, A-23 Sess-43), per the §27 §00
"Shared harness library contract" (A-31, Session 51 — normative).

Re-defining `load_fixtures`, `replay`, or `EXIT_HARNESS_SETUP` outside this
package is a gate #15 (`derives-from-restate-check`) violation at meta-level.
"""

from .engine import Fixture, ReplayResult, load_fixtures, replay
from .exit_codes import EXIT_HARNESS_SETUP, EXIT_INVOCATION, EXIT_PASS, EXIT_VIOLATION
from .schema_loader import HarnessSetupError, load_schema

__all__ = [
    "EXIT_HARNESS_SETUP",
    "EXIT_INVOCATION",
    "EXIT_PASS",
    "EXIT_VIOLATION",
    "Fixture",
    "HarnessSetupError",
    "ReplayResult",
    "load_fixtures",
    "load_schema",
    "replay",
]

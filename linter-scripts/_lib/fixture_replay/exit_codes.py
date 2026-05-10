"""Sanctioned exit codes for §27 integration-test gates.

`EXIT_HARNESS_SETUP = 3` is the ONLY sanctioned source of exit-code 3
across the entire toolchain (§27 §00 A-31, Sess-51 — normative). Gates
emitting `exit 3` from any other constant trip a §27 §00 violation.
"""

EXIT_PASS: int = 0
EXIT_VIOLATION: int = 1
EXIT_INVOCATION: int = 2
EXIT_HARNESS_SETUP: int = 3

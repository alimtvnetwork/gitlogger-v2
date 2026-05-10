#!/usr/bin/env python3
"""check-verification-ledger-cadence.py — §27 slot 38 (Sess-63 A-53).

Enforces the §25 invariant 5 verification-cadence rule (A-46 Sess-56):
every spec-improvement session that does NOT materially edit a
`Carried-open` row in `spec/25-app-issues/02-consolidated-audit-findings/00-overview.md`
MUST append a row to the **Verification cadence ledger** with a sweep
session id (`Sess-NN`) that is at most 1 session behind the current
session. Otherwise the cohort drifts and §27 gate #13 D5 fires for all
8 Carried-open rows.

This gate parses the ledger directly and asserts:

  latest_ledger_sweep_session >= current_session - tolerance   (default tolerance = 1)

Per §25 v1.6.0 changelog:
  > Shipping a §27 gate `verification-ledger-cadence-check` that
  > mechanically rejects sessions missing a ledger row when no material
  > Carried-open edit occurred → C4 R 19→20.

Usage:
    python3 linter-scripts/check-verification-ledger-cadence.py \\
        --current-session 63
    python3 linter-scripts/check-verification-ledger-cadence.py --self-test

Exit codes (mirrored from `_lib/fixture_replay/exit_codes.py` per §27 §00 A-31):
    0 — ledger cadence honored (latest sweep within tolerance window)
    1 — cadence violation (ledger stale)
    2 — bad CLI invocation
    3 — harness setup error (file unreadable, ledger section missing)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER_FILE = (
    REPO_ROOT
    / "spec"
    / "25-app-issues"
    / "02-consolidated-audit-findings"
    / "00-overview.md"
)
LEDGER_SECTION_HEADER = "**Verification cadence ledger.**"
SESS_RE = re.compile(r"Sess-(\d+)")

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_INVOCATION = 2
EXIT_HARNESS_SETUP = 3


def _extract_sweep_sessions(text: str) -> List[int]:
    """Return all Sess-NN ids appearing in the ledger table block.

    Strategy: locate the ledger header sentinel; scan forward until the
    next blank-line-then-non-table boundary; collect every Sess-NN match
    inside the table region (first column).
    """
    idx = text.find(LEDGER_SECTION_HEADER)
    if idx < 0:
        raise FileNotFoundError(
            f"ledger section sentinel {LEDGER_SECTION_HEADER!r} not found"
        )
    # Walk lines until we leave the ledger region (next bold paragraph).
    lines = text[idx:].splitlines()
    sessions: List[int] = []
    seen_table_header = False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("**") and stripped != LEDGER_SECTION_HEADER:
            break
        if stripped.startswith("|") and "Sweep session" in stripped:
            seen_table_header = True
            continue
        if seen_table_header and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not cells or set(cells[0]) <= {"-", ":", " "}:
                continue
            m = SESS_RE.search(cells[0])
            if m:
                sessions.append(int(m.group(1)))
    return sessions


def check_cadence(
    ledger_path: Path, current_session: int, tolerance: int
) -> Tuple[int, List[str]]:
    """Return (exit_code, messages)."""
    if not ledger_path.exists():
        return EXIT_HARNESS_SETUP, [f"ledger file not found: {ledger_path}"]
    try:
        text = ledger_path.read_text(encoding="utf-8")
    except OSError as exc:
        return EXIT_HARNESS_SETUP, [f"ledger file unreadable: {exc}"]
    try:
        sweeps = _extract_sweep_sessions(text)
    except FileNotFoundError as exc:
        return EXIT_HARNESS_SETUP, [str(exc)]
    if not sweeps:
        return EXIT_HARNESS_SETUP, [
            "ledger table parsed but no Sess-NN sweep rows found "
            "(invariant 5 cadence rule cannot be evaluated)"
        ]
    latest = max(sweeps)
    drift = current_session - latest
    if drift <= tolerance:
        return EXIT_PASS, [
            f"PASS: latest sweep Sess-{latest} is {drift} session(s) behind "
            f"current Sess-{current_session} (tolerance={tolerance})"
        ]
    return EXIT_VIOLATION, [
        f"FAIL: latest sweep Sess-{latest} is {drift} session(s) behind "
        f"current Sess-{current_session} (tolerance={tolerance}); "
        f"§25 invariant 5 requires a freshness sweep this session OR a "
        f"material Carried-open edit (which this gate cannot verify — "
        f"append a ledger row to acknowledge the sweep was performed)."
    ]


def run_self_test() -> int:
    """In-memory fixtures covering pass / fail / setup-error paths."""
    import tempfile

    failures = 0

    def synth(rows: list[str]) -> str:
        body = "\n".join(rows)
        return (
            "preamble\n\n"
            f"{LEDGER_SECTION_HEADER} text\n\n"
            "| Sweep session | Rows verified | Result | Next due |\n"
            "|---|---|---|---|\n"
            f"{body}\n\n"
            "**Disposition rollup.**\n"
        )

    cases = [
        # (label, file_text, current_sess, tolerance, expected_exit)
        ("pass-same-session", synth(["| Sess-63 (A-53) | 8 | ok | Sess-64 |"]), 63, 1, EXIT_PASS),
        ("pass-1-behind", synth(["| Sess-62 (A-52) | 8 | ok | Sess-63 |"]), 63, 1, EXIT_PASS),
        ("fail-2-behind", synth(["| Sess-61 (A-51) | 8 | ok | Sess-62 |"]), 63, 1, EXIT_VIOLATION),
        (
            "pass-multi-rows-takes-latest",
            synth(
                [
                    "| Sess-56 (A-46) | 8 | ok | Sess-57 |",
                    "| Sess-63 (A-53) | 8 | ok | Sess-64 |",
                ]
            ),
            63,
            1,
            EXIT_PASS,
        ),
        ("setup-error-missing-sentinel", "no ledger here\n", 63, 1, EXIT_HARNESS_SETUP),
    ]

    for label, content, sess, tol, want in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(content)
            path = Path(f.name)
        got, msgs = check_cadence(path, sess, tol)
        path.unlink()
        if got == want:
            print(f"SELF-TEST PASS [{label}] exit={got}")
        else:
            print(f"SELF-TEST FAIL [{label}] expected={want} got={got} msgs={msgs}")
            failures += 1
    return EXIT_VIOLATION if failures else EXIT_PASS


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_FILE)
    ap.add_argument(
        "--current-session",
        type=int,
        help="Current spec-improvement session number (Sess-NN).",
    )
    ap.add_argument(
        "--tolerance",
        type=int,
        default=1,
        help="Max allowed drift between latest sweep and current session (default 1).",
    )
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        rc = run_self_test()
        print(f"\nSelf-test {'PASSED' if rc == EXIT_PASS else 'FAILED'}")
        return rc

    if args.current_session is None:
        print(
            "error: --current-session N is required (or pass --self-test)",
            file=sys.stderr,
        )
        return EXIT_INVOCATION

    rc, msgs = check_cadence(args.ledger, args.current_session, args.tolerance)
    stream = sys.stdout if rc == EXIT_PASS else sys.stderr
    for m in msgs:
        print(f"[gate-21] {m}", file=stream)
    return rc


if __name__ == "__main__":
    sys.exit(main())

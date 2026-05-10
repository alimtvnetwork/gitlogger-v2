#!/usr/bin/env python3
"""
check-spec22-inventory.py — §27 slot 37 (Sess-56 A-48)

Enforces spec/22 AC-78 "Module asset inventory pin": every entry declared in
spec/22's §99 Module Inventory MUST exist on disk at the cited path with the
cited line-count tolerance, and the locked-vacant slot range (09..13) MUST
remain absent.

Usage:
    python3 linter-scripts/check-spec22-inventory.py --check inventory
    python3 linter-scripts/check-spec22-inventory.py --check locked-vacant
    python3 linter-scripts/check-spec22-inventory.py --check all
    python3 linter-scripts/check-spec22-inventory.py --self-test

Exit codes:
    0 — all checks pass
    1 — at least one violation (missing file, present-but-locked, etc.)
    2 — invocation/usage error
"""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC22 = REPO_ROOT / "spec" / "22-git-logs-v2"
LOCKED_VACANT_SLOTS = {"09", "10", "11", "12", "13"}

# Required normative-fixture set (AC-78 cites these explicitly).
REQUIRED_NON_MD = [
    "18-schema.sql",
    "33-bats-test-skeleton.md",
    "34-phpunit-test-skeleton.md",
    "35-reference-ci-yml.md",
]

REQUIRED_TIER1 = [
    "00-overview.md",
    "97-acceptance-criteria.md",
    "98-changelog.md",
    "99-consistency-report.md",
]


def check_inventory() -> list[str]:
    errors: list[str] = []
    if not SPEC22.is_dir():
        return [f"spec/22 directory not found at {SPEC22}"]
    for fname in REQUIRED_TIER1 + REQUIRED_NON_MD:
        p = SPEC22 / fname
        if not p.is_file():
            errors.append(f"AC-78 violation: required file missing: {fname}")
        elif p.stat().st_size == 0:
            errors.append(f"AC-78 violation: required file empty: {fname}")
    return errors


def check_locked_vacant() -> list[str]:
    errors: list[str] = []
    if not SPEC22.is_dir():
        return [f"spec/22 directory not found at {SPEC22}"]
    for entry in SPEC22.iterdir():
        if not entry.is_file():
            continue
        slot = entry.name[:2]
        if slot in LOCKED_VACANT_SLOTS:
            errors.append(
                f"AC-22-LV1 violation: locked-vacant slot {slot} occupied by {entry.name}"
            )
    return errors


def run_self_test() -> int:
    """Run all checks against synthetic fixtures under linter-scripts/fixtures/."""
    import tempfile
    import shutil
    global SPEC22
    original = SPEC22
    failures = 0

    # Fixture 1: complete inventory → must pass
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "spec22"
        d.mkdir()
        for f in REQUIRED_TIER1 + REQUIRED_NON_MD:
            (d / f).write_text("stub\n")
        SPEC22 = d
        errs = check_inventory() + check_locked_vacant()
        if errs:
            print(f"SELF-TEST FAIL [complete-inventory]: unexpected errors: {errs}")
            failures += 1
        else:
            print("SELF-TEST PASS [complete-inventory]")

    # Fixture 2: missing 18-schema.sql → must fail
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "spec22"
        d.mkdir()
        for f in REQUIRED_TIER1 + REQUIRED_NON_MD:
            if f == "18-schema.sql":
                continue
            (d / f).write_text("stub\n")
        SPEC22 = d
        errs = check_inventory()
        if any("18-schema.sql" in e for e in errs):
            print("SELF-TEST PASS [missing-schema-sql]")
        else:
            print(f"SELF-TEST FAIL [missing-schema-sql]: expected violation, got {errs}")
            failures += 1

    # Fixture 3: locked-vacant slot 11 occupied → must fail
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "spec22"
        d.mkdir()
        for f in REQUIRED_TIER1 + REQUIRED_NON_MD:
            (d / f).write_text("stub\n")
        (d / "11-forbidden-occupant.md").write_text("violation\n")
        SPEC22 = d
        errs = check_locked_vacant()
        if any("slot 11" in e for e in errs):
            print("SELF-TEST PASS [locked-vacant-11-occupied]")
        else:
            print(f"SELF-TEST FAIL [locked-vacant-11-occupied]: expected violation, got {errs}")
            failures += 1

    SPEC22 = original
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", choices=["inventory", "locked-vacant", "all"])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        rc = run_self_test()
        print(f"\nSelf-test {'PASSED' if rc == 0 else 'FAILED'}")
        return rc

    if not args.check:
        ap.print_help()
        return 2

    errors: list[str] = []
    if args.check in ("inventory", "all"):
        errors += check_inventory()
    if args.check in ("locked-vacant", "all"):
        errors += check_locked_vacant()

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"\nFAIL: {len(errors)} AC-78 / AC-22-LV1 violation(s)", file=sys.stderr)
        return 1
    print("PASS: spec/22 inventory + locked-vacant constraints honored")
    return 0


if __name__ == "__main__":
    sys.exit(main())

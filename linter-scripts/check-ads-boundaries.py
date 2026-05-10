#!/usr/bin/env python3
"""check-ads-boundaries.py — §24 AC-ADS-06/09/10 boundary scanner.

Implements the three Test invariant blocks added by Sess-55 A-41:

  ac-ads-06: marketing routes MUST NOT import src/components/app/AppShell
  ac-ads-09: src/components/ui/** ∩ src/components/app/** basenames MUST be empty
  ac-ads-10: var(--app-status-*) MUST NOT appear under src/components/ui/**

Invocation:
  check-ads-boundaries.py --check {ac-ads-06|ac-ads-09|ac-ads-10|all}
                          [--root <project-or-fixture-root>]

Exit codes:
  0 = pass (no violations found)
  1 = at least one violation (per-AC message printed to stderr)
  2 = harness/usage error (bad flag, missing root)

Fixture self-test:
  Each AC's negative fixture under linter-scripts/fixtures/<name>/ MUST cause
  exit-code 1. The harness tester `--self-test` runs the scanner against each
  fixture and asserts non-zero exit — proving the scanner has teeth.

This script is fixture-shipped (Sess-55 A-42) but NOT yet promoted to a §27
gate; promotion to §27 slot 36 (`check-ads-boundaries`) is queued behind the
next §27 §97 AC-T-NN bump per scope-lock discipline.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

APPSHELL_IMPORT_RX = re.compile(
    r"""from\s+["']([^"']*?components/app/AppShell[^"']*)["']"""
)
APP_STATUS_TOKEN_RX = re.compile(r"--app-status-[a-z0-9-]+")

MARKETING_GLOBS = ("pages/(marketing)/**/*.tsx", "pages/(marketing)/**/*.ts")
UI_DIR = "src/components/ui"
APP_DIR = "src/components/app"


def _iter(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    out: list[Path] = []
    for pat in patterns:
        out.extend(root.glob(pat))
    return [p for p in out if p.is_file()]


def check_ac_ads_06(root: Path) -> list[str]:
    """Marketing routes MUST NOT import AppShell."""
    violations: list[str] = []
    for f in _iter(root, MARKETING_GLOBS):
        text = f.read_text(encoding="utf-8", errors="replace")
        if APPSHELL_IMPORT_RX.search(text):
            violations.append(f"ADS-06-VIOLATION: marketing route imports AppShell: {f}")
    return violations


def check_ac_ads_09(root: Path) -> list[str]:
    """src/components/ui/** ∩ src/components/app/** basenames MUST be empty."""
    ui_root = root / UI_DIR
    app_root = root / APP_DIR
    if not ui_root.exists() or not app_root.exists():
        return []
    skip_suffixes = (".test.tsx", ".stories.tsx", ".test.ts", ".stories.ts")

    def names(p: Path) -> set[str]:
        return {
            f.stem.lower()
            for f in p.rglob("*.tsx")
            if not f.name.endswith(skip_suffixes)
        }

    overlap = sorted(names(ui_root) & names(app_root))
    return [f"ADS-09-VIOLATION: name collision: {n}" for n in overlap]


def check_ac_ads_10(root: Path) -> list[str]:
    """var(--app-status-*) MUST NOT appear under src/components/ui/**."""
    ui_root = root / UI_DIR
    if not ui_root.exists():
        return []
    violations: list[str] = []
    for f in ui_root.rglob("*"):
        if not f.is_file() or f.suffix not in (".tsx", ".ts", ".css", ".scss"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if APP_STATUS_TOKEN_RX.search(text):
            violations.append(
                f"ADS-10-VIOLATION: --app-status-* used outside src/components/app/: {f}"
            )
    return violations


CHECKS = {
    "ac-ads-06": check_ac_ads_06,
    "ac-ads-09": check_ac_ads_09,
    "ac-ads-10": check_ac_ads_10,
}


def run_self_test() -> int:
    """Each negative fixture MUST cause non-zero exit."""
    cases = [
        ("ac-ads-06", "linter-scripts/fixtures/marketing-appshell-violation"),
        ("ac-ads-09", "linter-scripts/fixtures/ownership-matrix-collision"),
        ("ac-ads-10", "linter-scripts/fixtures/status-token-leak"),
    ]
    failures: list[str] = []
    for check, fixture in cases:
        rc = subprocess.run(
            [sys.executable, str(Path(__file__)), "--check", check, "--root", str(REPO_ROOT / fixture)],
            capture_output=True,
        ).returncode
        if rc == 0:
            failures.append(f"SELF-TEST FAIL: {check} accepted hostile fixture {fixture} (expected exit 1)")
        else:
            print(f"self-test ok: {check} rejected {fixture} (rc={rc})", file=sys.stderr)
    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", choices=[*CHECKS, "all"], required=False)
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return run_self_test()
    if not args.check:
        print("error: --check is required (or pass --self-test)", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"error: root does not exist: {root}", file=sys.stderr)
        return 2

    targets = list(CHECKS) if args.check == "all" else [args.check]
    violations: list[str] = []
    for t in targets:
        violations.extend(CHECKS[t](root))

    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

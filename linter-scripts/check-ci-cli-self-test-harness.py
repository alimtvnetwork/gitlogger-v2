#!/usr/bin/env python3
"""Gate #40 — check-ci-cli-self-test-harness.

Asserts §28 (Universal CI CLI) declares a built-in `--self-test`
harness mirroring the §27 self-test cohort discipline.

Six clauses (slot-62 contract):
  1. §04 declares `--self-test` (or canonical equivalent) with the
     four semantic markers `built-in`, `no network`,
     `no real CI provider`, `no real git repo`.
  2. §28 §00 OR §97 carries the literal `vacuously-passing`
     (R5 inheritance) AND the canonical R5 marker
     `vacuous-pass` (allows either `exit \`1\` with \`vacuous-pass:`
     or the canonical equivalent `auto-fail`).
  3. §97 carries ≥6 fixture rows in the canonical shape
     `**Fixture F-N (<mode>):** <description>` AND every
     `--check <mode>` enumerated in §04 (or in §97 fixture rows
     when §04 declares no per-mode flag) has at least one
     fixture row.
  4. §07 declares a 4-row exit-code table mapping
     `0` → pass · `1` → violation · `2` → invocation error ·
     `3` → fixture-rot.
  5. §28 §00 carries the literal harness declaration
     `glci ships a built-in \`--self-test\` harness` (or
     canonical equivalent `built-in self-test harness is
     load-bearing for shippability`) AND the Lesson-#15
     self-citation `Self-enforcing via §27 backlog gate
     \`ci-cli-self-test-harness-check\``.
  6. R5 vacuously-passing scanner: at least one anchor located
     in EACH of §00, §04, §07, §97; otherwise auto-fail with
     `vacuous-pass:` line.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3
fixture-rot.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = REPO_ROOT / "spec" / "28-universal-ci-cli"

SEMANTIC_MARKERS = (
    "built-in",
    "no network",
    "no real CI provider",
    "no real git repo",
)

HARNESS_DECL_LITERALS = (
    "ships a built-in `--self-test` harness",
    "built-in self-test harness is load-bearing for shippability",
)

LESSON15_CITATION = (
    "Self-enforcing via §27 backlog gate `ci-cli-self-test-harness-check`"
)

EXIT_TABLE_ROWS = (
    re.compile(r"`0`\s*[→\-]\s*pass", re.IGNORECASE),
    re.compile(r"`1`\s*[→\-]\s*violation", re.IGNORECASE),
    re.compile(r"`2`\s*[→\-]\s*invocation\s*error", re.IGNORECASE),
    re.compile(r"`3`\s*[→\-]\s*fixture-rot", re.IGNORECASE),
)

FIXTURE_ROW_RE = re.compile(
    r"\*\*Fixture\s+F-\d+\s*\(([^)]+)\)\:\*\*",
)

CHECK_MODE_RE = re.compile(r"`--check\s+([A-Za-z0-9\-]+)`")
SELF_TEST_FLAG_RE = re.compile(r"`--(?:self-test|harness|selftest)`|`selftest`\s+sub")


@dataclass
class FileSet:
    overview: str
    cmd_surface: str
    error_catalog: str
    ac: str

    @classmethod
    def from_dir(cls, base: Path) -> "FileSet":
        return cls(
            overview=(base / "00-overview.md").read_text(encoding="utf-8"),
            cmd_surface=(base / "04-command-surface.md").read_text(encoding="utf-8"),
            error_catalog=(base / "07-error-catalog.md").read_text(encoding="utf-8"),
            ac=(base / "97-acceptance-criteria.md").read_text(encoding="utf-8"),
        )


# ---------- Clause checks ----------

def clause_self_test_flag(fs: FileSet) -> list[str]:
    errs: list[str] = []
    if not SELF_TEST_FLAG_RE.search(fs.cmd_surface):
        errs.append(
            "clause-1: §04 missing `--self-test` flag (or canonical "
            "equivalent `--harness` / `selftest` subcommand)"
        )
    missing_markers = [m for m in SEMANTIC_MARKERS if m not in fs.cmd_surface]
    if missing_markers:
        errs.append(
            "clause-1: §04 missing semantic markers: "
            + ", ".join(f"`{m}`" for m in missing_markers)
        )
    return errs


def clause_r5_inheritance(fs: FileSet) -> list[str]:
    blob = fs.overview + "\n" + fs.ac
    errs: list[str] = []
    if "vacuously-passing" not in blob:
        errs.append(
            "clause-2: §28 §00 OR §97 missing `vacuously-passing` literal"
        )
    # canonical equivalents accepted: `vacuous-pass`, `auto-fail per R5`,
    # `R5 vacuous-pass clause`
    if not (
        "vacuous-pass" in blob
        or "auto-fail per R5" in blob
        or "R5 vacuous-pass" in blob
    ):
        errs.append(
            "clause-2: §28 §00 OR §97 missing R5 marker "
            "(`vacuous-pass` / `auto-fail per R5` / `R5 vacuous-pass`)"
        )
    return errs


def clause_fixture_coverage(fs: FileSet) -> list[str]:
    errs: list[str] = []
    fixtures = FIXTURE_ROW_RE.findall(fs.ac)
    if len(fixtures) < 6:
        errs.append(
            f"clause-3: §97 has only {len(fixtures)} fixture rows "
            "(canonical shape `**Fixture F-N (<mode>):** <description>`); "
            "minimum 6 (F-1 unique-passing + ≥5 failure variants)"
        )
    modes = set(CHECK_MODE_RE.findall(fs.cmd_surface))
    if modes:
        fixture_modes = {f.strip() for f in fixtures}
        uncovered = sorted(modes - fixture_modes)
        if uncovered:
            errs.append(
                "clause-3: `--check` modes without §97 fixture rows: "
                + ", ".join(f"`{m}`" for m in uncovered)
            )
    return errs


def clause_exit_code_table(fs: FileSet) -> list[str]:
    errs: list[str] = []
    blob = fs.error_catalog + "\n" + fs.cmd_surface
    missing = []
    for label, rx in zip(("0→pass", "1→violation", "2→invocation-error", "3→fixture-rot"), EXIT_TABLE_ROWS):
        if not rx.search(blob):
            missing.append(label)
    if missing:
        errs.append(
            "clause-4: §07 (or §04) exit-code table missing rows: "
            + ", ".join(missing)
        )
    return errs


def clause_harness_declaration(fs: FileSet) -> list[str]:
    errs: list[str] = []
    if not any(lit in fs.overview for lit in HARNESS_DECL_LITERALS):
        errs.append(
            "clause-5: §28 §00 missing harness declaration literal "
            "(`glci ships a built-in --self-test harness` or canonical "
            "equivalent `built-in self-test harness is load-bearing for shippability`)"
        )
    if LESSON15_CITATION not in fs.overview:
        errs.append(
            "clause-5: §28 §00 missing Lesson #15 self-citation literal "
            f"(`{LESSON15_CITATION}`)"
        )
    return errs


def clause_r5_vacuous_pass(fs: FileSet) -> list[str]:
    errs: list[str] = []
    if not fs.overview.strip():
        errs.append("vacuous-pass: §28 §00 not scanned (empty)")
    if not SELF_TEST_FLAG_RE.search(fs.cmd_surface) and "--check" not in fs.cmd_surface:
        errs.append("vacuous-pass: §28 §04 has zero --check modes / harness flag")
    if not any(rx.search(fs.error_catalog) for rx in EXIT_TABLE_ROWS):
        errs.append("vacuous-pass: §28 §07 exit-code table absent")
    if not FIXTURE_ROW_RE.search(fs.ac):
        errs.append("vacuous-pass: §28 §97 has zero AC-28-* fixture row")
    return errs


CHECKS: dict[str, Callable[[FileSet], list[str]]] = {
    "self-test-flag-declared": clause_self_test_flag,
    "r5-vacuous-pass-carried": clause_r5_inheritance,
    "per-mode-fixture-coverage": clause_fixture_coverage,
    "exit-code-contract": clause_exit_code_table,
    "harness-declaration": clause_harness_declaration,
    "vacuous-pass": clause_r5_vacuous_pass,
}


def run_checks(fs: FileSet, mode: str) -> list[str]:
    if mode == "all":
        errs: list[str] = []
        # vacuous-pass first — short-circuit if scan surface empty
        v = clause_r5_vacuous_pass(fs)
        if v:
            return v
        for name, fn in CHECKS.items():
            if name == "vacuous-pass":
                continue
            errs.extend(fn(fs))
        return errs
    if mode not in CHECKS:
        print(f"error: unknown --check mode `{mode}`", file=sys.stderr)
        sys.exit(2)
    return CHECKS[mode](fs)


# ---------- Self-test fixtures ----------

F1_OVERVIEW = """# §28 Overview

> **`glci` ships a built-in `--self-test` harness** — load-bearing.
> R5 vacuously-passing scanner is auto-fail (vacuous-pass marker).
> **Self-enforcing via §27 backlog gate `ci-cli-self-test-harness-check`**.
"""

F1_CMD = """# Command Surface

| Flag | Description |
|------|-------------|
| `--self-test` | built-in harness; no network; no real CI provider; no real git repo |
| `--check <mode>` | run a single check |

`--check all` `--check self-test-flag-declared` `--check r5-vacuous-pass-carried`
`--check per-mode-fixture-coverage` `--check exit-code-contract`
`--check harness-declaration`
"""

F1_ERR = """# Error Catalog

| Exit | Meaning |
|-----:|---------|
| `0` → pass | clean run |
| `1` → violation | gate violation |
| `2` → invocation error | bad CLI usage |
| `3` → fixture-rot | self-test broken |
"""

F1_AC = """# AC

vacuously-passing scanner is auto-fail per R5.

- **Fixture F-1 (all):** complete-clean; passes.
- **Fixture F-2 (self-test-flag-declared):** strip flag; fails.
- **Fixture F-3 (r5-vacuous-pass-carried):** strip literal; fails.
- **Fixture F-4 (per-mode-fixture-coverage):** drop row; fails.
- **Fixture F-5 (exit-code-contract):** strip exit row; fails.
- **Fixture F-6 (harness-declaration):** strip cite; fails.
"""


def make_fixture(overview=F1_OVERVIEW, cmd=F1_CMD, err=F1_ERR, ac=F1_AC) -> FileSet:
    return FileSet(overview=overview, cmd_surface=cmd, error_catalog=err, ac=ac)


def self_test() -> int:
    failures: list[str] = []

    # F-1 complete-clean: all clauses pass
    fs = make_fixture()
    errs = run_checks(fs, "all")
    if errs:
        failures.append(f"F-1 should pass; got: {errs}")

    # F-2 strip --self-test flag
    bad_cmd = F1_CMD.replace("`--self-test`", "`--something-else`").replace("built-in harness; no network; no real CI provider; no real git repo", "built-in harness")
    fs = make_fixture(cmd=bad_cmd)
    if not clause_self_test_flag(fs):
        failures.append("F-2 should fail clause-1")

    # F-3 strip R5 literal
    bad_ov = F1_OVERVIEW.replace("vacuously-passing", "X").replace("vacuous-pass", "X")
    bad_ac = F1_AC.replace("vacuously-passing", "X").replace("R5", "X")
    fs = make_fixture(overview=bad_ov, ac=bad_ac)
    if not clause_r5_inheritance(fs):
        failures.append("F-3 should fail clause-2")

    # F-4 only 5 fixtures
    bad_ac4 = F1_AC.replace("- **Fixture F-6 (harness-declaration):** strip cite; fails.\n", "")
    fs = make_fixture(ac=bad_ac4)
    if not clause_fixture_coverage(fs):
        failures.append("F-4 should fail clause-3")

    # F-5 strip exit `3` row
    bad_err = F1_ERR.replace("| `3` → fixture-rot | self-test broken |", "")
    fs = make_fixture(err=bad_err)
    if not clause_exit_code_table(fs):
        failures.append("F-5 should fail clause-4")

    # F-6 strip Lesson #15 cite
    bad_ov6 = F1_OVERVIEW.replace(LESSON15_CITATION, "X")
    fs = make_fixture(overview=bad_ov6)
    if not clause_harness_declaration(fs):
        failures.append("F-6 should fail clause-5")

    if failures:
        for f in failures:
            print(f"  ✘ {f}", file=sys.stderr)
        print(f"--self-test: {len(failures)} fixture(s) failed", file=sys.stderr)
        return 3
    print("--self-test: 6/6 fixtures passed (F-1 unique-passing + 5 failure variants)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", default="all",
                        help="all | " + " | ".join(CHECKS.keys()))
    parser.add_argument("--self-test", action="store_true",
                        help="run built-in fixture suite (no I/O, no network)")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    try:
        fs = FileSet.from_dir(SPEC_DIR)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errs = run_checks(fs, args.check)
    if errs:
        for e in errs:
            print(f"  ✘ {e}", file=sys.stderr)
        print(f"check-ci-cli-self-test-harness: {len(errs)} violation(s) "
              f"(mode={args.check})", file=sys.stderr)
        return 1
    print(f"check-ci-cli-self-test-harness: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

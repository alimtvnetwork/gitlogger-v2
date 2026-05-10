#!/usr/bin/env python3
"""Slot 60 — check-no-toolchain-enum-in-issues-folder.py (gate #38 / Phase-5 T-31).

Asserts §25 folder owns ZERO toolchain-enumeration surface. Single source of
truth for the gate roster, slot-range table, and `linter-scripts/` directory
listing is §27. Single-gate / single-slot citations in prose remain permitted.
See spec/27-spec-toolchain/60-check-no-toolchain-enum-in-issues-folder.md.

Bindings: mem://constraints/spec-scope (locked-7 scope-lock) — boundary-quartet 3/4.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ISSUES_DIR = REPO / "spec" / "25-app-issues"
OVERVIEW = ISSUES_DIR / "00-overview.md"

FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}```")
TABLE_ROW_RE = re.compile(r"^\s*\|.+\|\s*$")
HEADER_AC_RE = re.compile(r"^###\s+AC-AI-\w+", re.IGNORECASE)
HEADER_RE = re.compile(r"^#{1,6}\s+")
BACKTICK_SPAN_RE = re.compile(r"`+[^`\n]+`+")
SCRIPT_PATH_RE = re.compile(r"linter-scripts/[a-z][a-z0-9-]*\.py")
SLOT_RANGE_BULLET_RE = re.compile(r"^\s*[-*]\s+`?\d{2}-\d{2}`?\s*[:—–-]")
GATE_NAME_RE = re.compile(r"`check-[a-z][a-z0-9-]+`")
SLOT_TOKEN_RE = re.compile(r"`slot\s+\d+`", re.IGNORECASE)

BOUNDARY_LITERALS = (
    "Toolchain enumeration is owned exclusively by §27",
    "Self-enforcing via §27 backlog gate `no-toolchain-enum-in-issues-folder-check`",
)


def md_files(root: Path):
    return sorted(p for p in root.rglob("*.md"))


def scan(paths):
    return {p: p.read_text(encoding="utf-8").splitlines() for p in paths}


def split_ac_sections(lines: list[str]):
    """Yield (start, end) line indices (0-based) for each ### AC-AI-* section."""
    sections = []
    cur_start = None
    for i, ln in enumerate(lines):
        if HEADER_AC_RE.match(ln):
            if cur_start is not None:
                sections.append((cur_start, i))
            cur_start = i
        elif cur_start is not None and HEADER_RE.match(ln) and not HEADER_AC_RE.match(ln):
            sections.append((cur_start, i))
            cur_start = None
    if cur_start is not None:
        sections.append((cur_start, len(lines)))
    return sections


def in_ac_section(lineno_0: int, ac_sections) -> bool:
    return any(s <= lineno_0 < e for s, e in ac_sections)


def find_tables(lines: list[str]):
    """Return list of (header_idx, body_rows) for each contiguous markdown table.

    Header is detected by row + separator (next row containing only |, -, :, spaces).
    """
    tables = []
    i = 0
    n = len(lines)
    in_fence = False
    while i < n:
        if FENCE_OPEN_RE.match(lines[i]):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        if TABLE_ROW_RE.match(lines[i]) and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = i
            body = []
            j = i + 2
            while j < n and TABLE_ROW_RE.match(lines[j]):
                body.append((j, lines[j]))
                j += 1
            tables.append((header, lines[header], body))
            i = j
            continue
        i += 1
    return tables


# ---- Clause 1: gate-enumeration tables --------------------------------------

def check_no_gate_enum_table(files, ac_sections_by_file):
    errs = []
    for p, lines in files.items():
        ac_sections = ac_sections_by_file[p]
        for header_idx, header, body in find_tables(lines):
            hl = header.lower()
            cols = [c.strip() for c in header.strip().strip("|").split("|")]
            ncols = len(cols)
            has_gate = ("gate" in hl) or ("gate #" in hl)
            has_slot = "slot" in hl
            has_extra = any(tok in hl for tok in ("workflow step", "status", "check"))
            row_count = len(body)
            # Header-shape detector
            if has_gate and has_slot and has_extra and row_count >= 2:
                # Exempt single-gate finding-evidence rows (only one row referencing one gate)
                if row_count == 1:
                    continue
                if in_ac_section(header_idx, ac_sections) and row_count <= 2:
                    continue
                errs.append(
                    f"clause-1: gate-enumeration table in {p}:{header_idx+1} "
                    f"(cols={cols}, rows={row_count})"
                )
                continue
            # Body-shape detector: ≥3 rows starting `| #NN |` with `gate #` token
            numbered = sum(
                1 for _, row in body
                if re.match(r"^\s*\|\s*#?\d{1,3}\s*\|", row) and "gate #" in row.lower()
            )
            if numbered >= 3:
                errs.append(
                    f"clause-1: gate-enumeration table (numbered rows) in {p}:{header_idx+1} "
                    f"(numbered_rows={numbered})"
                )
    return errs


# ---- Clause 2: linter-scripts directory listings ----------------------------

def check_no_script_roster(files, ac_sections_by_file):
    errs = []
    for p, lines in files.items():
        ac_sections = ac_sections_by_file[p]
        # (a) fenced blocks containing ≥4 script paths
        i = 0
        n = len(lines)
        while i < n:
            if FENCE_OPEN_RE.match(lines[i]):
                start = i + 1
                j = start
                while j < n and not FENCE_OPEN_RE.match(lines[j]):
                    j += 1
                body = "\n".join(lines[start:j])
                hits = SCRIPT_PATH_RE.findall(body)
                if len(hits) >= 4:
                    errs.append(
                        f"clause-2: linter-scripts roster fence in {p}:{i+1} "
                        f"(script_path_count={len(hits)})"
                    )
                i = j + 1
                continue
            i += 1
        # (b) ≥4 consecutive bullets each citing a linter-scripts path
        run = 0
        run_start = -1
        for idx, ln in enumerate(lines):
            stripped = ln.lstrip()
            is_bullet = stripped.startswith(("- ", "* ", "+ "))
            if is_bullet and SCRIPT_PATH_RE.search(ln):
                if run == 0:
                    run_start = idx
                run += 1
            else:
                if run >= 4 and not in_ac_section(run_start, ac_sections):
                    errs.append(
                        f"clause-2: linter-scripts bullet roster in {p}:{run_start+1} "
                        f"(consecutive_bullets={run})"
                    )
                run = 0
        if run >= 4 and not in_ac_section(run_start, ac_sections):
            errs.append(
                f"clause-2: linter-scripts bullet roster in {p}:{run_start+1} "
                f"(consecutive_bullets={run})"
            )
    return errs


# ---- Clause 3: slot-number range table --------------------------------------

RANGE_PATTERNS = ("01-09", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "90-99")


def check_no_slot_range_table(files, ac_sections_by_file):
    errs = []
    for p, lines in files.items():
        ac_sections = ac_sections_by_file[p]
        for header_idx, header, body in find_tables(lines):
            hl = header.lower()
            if "range" in hl and "purpose" in hl:
                body_text = "\n".join(r for _, r in body)
                if sum(1 for pat in RANGE_PATTERNS if pat in body_text) >= 3:
                    errs.append(
                        f"clause-3: slot-range table in {p}:{header_idx+1}"
                    )
        # Bullet-list shape: ≥3 consecutive `NN-NN` bullets with separator
        run = 0
        run_start = -1
        for idx, ln in enumerate(lines):
            if SLOT_RANGE_BULLET_RE.match(ln):
                if run == 0:
                    run_start = idx
                run += 1
            else:
                if run >= 3 and not in_ac_section(run_start, ac_sections):
                    errs.append(
                        f"clause-3: slot-range bullet list in {p}:{run_start+1} "
                        f"(consecutive_bullets={run})"
                    )
                run = 0
        if run >= 3 and not in_ac_section(run_start, ac_sections):
            errs.append(
                f"clause-3: slot-range bullet list in {p}:{run_start+1} "
                f"(consecutive_bullets={run})"
            )
    return errs


# ---- Clause 4: AC-finding exemption — positive R5 anchor ---------------------

def count_ac_exemption_anchors(files, ac_sections_by_file) -> int:
    n = 0
    for p, lines in files.items():
        for s, e in ac_sections_by_file[p]:
            block = "\n".join(lines[s:e])
            if GATE_NAME_RE.search(block) or SLOT_TOKEN_RE.search(block):
                n += 1
    return n


# ---- Clause 5: boundary declaration -----------------------------------------

def check_boundary_declaration():
    errs = []
    if not OVERVIEW.exists():
        return [f"clause-5: §25 §00 overview missing at {OVERVIEW}"]
    txt = OVERVIEW.read_text(encoding="utf-8")
    for lit in BOUNDARY_LITERALS:
        if lit not in txt:
            errs.append(f"clause-5: missing literal in §25 §00: {lit!r}")
    return errs


# ---- Self-test --------------------------------------------------------------

FIXTURES = {
    "F-1-clean": {
        "files": {
            "00-overview.md": (
                "# X\n\n"
                + BOUNDARY_LITERALS[0] + " — narrative.\n\n"
                + BOUNDARY_LITERALS[1] + " (slot 60).\n"
            ),
            "97-acceptance-criteria.md": (
                "### AC-AI-99: Cite gate `check-error-envelope-uniformity` and `slot 60`.\n"
                "Body cites `check-no-sql-ddl-in-ui-folder`.\n"
            ),
        },
        "expect_pass": True,
    },
    "F-2-gate-enum-table": {
        "files": {
            "00-overview.md": "# X\n\n"
                + BOUNDARY_LITERALS[0] + "\n\n" + BOUNDARY_LITERALS[1] + "\n",
            "97-acceptance-criteria.md": (
                "### AC-AI-99: cite `check-x` `slot 1`.\n"
            ),
            "extra.md": (
                "| Gate | Slot | Workflow step |\n"
                "|------|------|---------------|\n"
                "| #1   | 01   | step-a        |\n"
                "| #2   | 02   | step-b        |\n"
                "| #3   | 03   | step-c        |\n"
            ),
        },
        "expect_pass": False,
        "expect_clause": "clause-1",
    },
    "F-3-script-roster-fence": {
        "files": {
            "00-overview.md": "# X\n\n"
                + BOUNDARY_LITERALS[0] + "\n\n" + BOUNDARY_LITERALS[1] + "\n",
            "97-acceptance-criteria.md": (
                "### AC-AI-99: cite `check-x` `slot 1`.\n"
            ),
            "extra.md": (
                "```text\n"
                "linter-scripts/check-a.py\n"
                "linter-scripts/check-b.py\n"
                "linter-scripts/check-c.py\n"
                "linter-scripts/check-d.py\n"
                "```\n"
            ),
        },
        "expect_pass": False,
        "expect_clause": "clause-2",
    },
    "F-4-slot-range-table": {
        "files": {
            "00-overview.md": "# X\n\n"
                + BOUNDARY_LITERALS[0] + "\n\n" + BOUNDARY_LITERALS[1] + "\n",
            "97-acceptance-criteria.md": (
                "### AC-AI-99: cite `check-x` `slot 1`.\n"
            ),
            "extra.md": (
                "| Range | Purpose |\n"
                "|-------|---------|\n"
                "| 01-09 | A |\n"
                "| 10-19 | B |\n"
                "| 20-29 | C |\n"
            ),
        },
        "expect_pass": False,
        "expect_clause": "clause-3",
    },
    "F-5-ac-exemption-broken": {
        # Boundary present; AC sections exist but none cite a gate-name/slot.
        "files": {
            "00-overview.md": "# X\n\n"
                + BOUNDARY_LITERALS[0] + "\n\n" + BOUNDARY_LITERALS[1] + "\n",
            "97-acceptance-criteria.md": (
                "### AC-AI-99: no gate citations here.\n"
                "Plain prose only.\n"
            ),
        },
        "expect_pass": False,
        "expect_clause": "vacuous-pass",
    },
    "F-6-boundary-stripped": {
        "files": {
            "00-overview.md": "# X\n\nNo boundary literal present.\n",
            "97-acceptance-criteria.md": (
                "### AC-AI-99: cite `check-x` `slot 1`.\n"
            ),
        },
        "expect_pass": False,
        "expect_clause": "clause-5",
    },
}


def run_against(files_dict: dict[str, str]):
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        issues = td_path / "spec" / "25-app-issues"
        issues.mkdir(parents=True)
        for name, body in files_dict.items():
            (issues / name).write_text(body, encoding="utf-8")
        # Patch globals
        global ISSUES_DIR, OVERVIEW
        old_issues, old_over = ISSUES_DIR, OVERVIEW
        ISSUES_DIR = issues
        OVERVIEW = issues / "00-overview.md"
        try:
            errs = run_all_checks()
        finally:
            ISSUES_DIR, OVERVIEW = old_issues, old_over
        return errs


def run_all_checks():
    paths = md_files(ISSUES_DIR)
    if not paths:
        return ["vacuous-pass: §25 has zero .md files"]
    files = scan(paths)
    ac_sections_by_file = {p: split_ac_sections(lines) for p, lines in files.items()}
    errs = []
    errs += check_no_gate_enum_table(files, ac_sections_by_file)
    errs += check_no_script_roster(files, ac_sections_by_file)
    errs += check_no_slot_range_table(files, ac_sections_by_file)
    errs += check_boundary_declaration()
    anchors = count_ac_exemption_anchors(files, ac_sections_by_file)
    if anchors == 0:
        errs.append(
            "vacuous-pass: no ### AC-AI-* section references a §27 gate name or slot number "
            "in a backtick span (clause-4 exemption never exercised)"
        )
    return errs


def self_test() -> int:
    failed = 0
    for name, fx in FIXTURES.items():
        errs = run_against(fx["files"])
        passed = len(errs) == 0
        if fx["expect_pass"] and not passed:
            print(f"[FAIL] {name}: expected pass, got errs:\n  " + "\n  ".join(errs))
            failed += 1
        elif not fx["expect_pass"]:
            if passed:
                print(f"[FAIL] {name}: expected failure, got pass")
                failed += 1
            else:
                want = fx.get("expect_clause", "")
                if want and not any(want in e for e in errs):
                    print(f"[FAIL] {name}: expected clause {want!r}, got:\n  " + "\n  ".join(errs))
                    failed += 1
                else:
                    print(f"[ok]   {name}: {len(errs)} err(s) (expected {want or 'any'})")
        else:
            print(f"[ok]   {name}: pass")
    print(f"\nself-test: {len(FIXTURES) - failed}/{len(FIXTURES)} fixtures passed")
    return 0 if failed == 0 else 3


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    errs = run_all_checks()
    if errs:
        for e in errs:
            print(e)
        return 1
    print(f"OK: {len(md_files(ISSUES_DIR))} §25 .md files clean (gate #38)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

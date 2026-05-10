#!/usr/bin/env python3
"""Slot 58 — check-no-sql-ddl-in-ui-folder.py (gate #36 / Phase-5 T-29).

Asserts §24 folder owns ZERO executable DDL surface. Single source of truth
for App-side DDL is §23. See spec/27-spec-toolchain/58-check-no-sql-ddl-in-ui-folder.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UI_DIR = REPO / "spec" / "24-app-design-system-and-ui"
OVERVIEW = UI_DIR / "00-overview.md"

FORBIDDEN_LANGS = ("sql", "sqlite", "postgres", "pg", "mysql", "mariadb", "ddl", "plpgsql")
FENCE_RE = re.compile(r"^[ ]{0,3}```\s*([A-Za-z]+)", re.IGNORECASE)
BARE_DDL = ("CREATE TABLE ", "ALTER TABLE ", "DROP TABLE ", "CREATE INDEX ", "ALTER COLUMN ")
MIGRATION_PATH_RE = re.compile(
    r"spec/24-[A-Za-z0-9_-]+/(migrations|schema|ddl)/[A-Za-z0-9_./-]+\.sql",
    re.IGNORECASE,
)
BOUNDARY_LITERALS = (
    "App-side DDL is owned exclusively by §23",
    "Self-enforcing via §27 backlog gate `no-sql-ddl-in-ui-folder-check`",
)
DDL_COL_NAMES = ("IsActive", "AppId", "AppLinkType", "AppStatusId")
INLINE_BACKTICKS = re.compile(r"`+[^`\n]*`+")


def strip_inline_backticks(s: str) -> str:
    return INLINE_BACKTICKS.sub(" ", s)


def scan_files(paths):
    """Returns dict: path -> list[lines] (without modifying)."""
    out = {}
    for p in paths:
        try:
            out[p] = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            pass
    return out


def check_no_sql_fences(files):
    errs = []
    for p, lines in files.items():
        for i, ln in enumerate(lines, 1):
            m = FENCE_RE.match(ln)
            if m and m.group(1).lower() in FORBIDDEN_LANGS:
                errs.append(f"clause-1: SQL fence in {p}:{i} (lang={m.group(1)})")
    return errs


def check_no_bare_ddl(files):
    errs = []
    for p, lines in files.items():
        in_fence = False
        for i, ln in enumerate(lines, 1):
            if FENCE_RE.match(ln):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            stripped = strip_inline_backticks(ln)
            for kw in BARE_DDL:
                if kw in stripped:
                    errs.append(f"clause-2: bare DDL keyword {kw!r} in {p}:{i}")
                    break
    return errs


def check_no_migration_paths(files):
    errs = []
    for p, lines in files.items():
        for i, ln in enumerate(lines, 1):
            stripped = strip_inline_backticks(ln)
            if MIGRATION_PATH_RE.search(stripped):
                errs.append(f"clause-3: migration path reference in {p}:{i}")
    return errs


def check_binding_table_exemption(files):
    """R5 anchor: ≥1 U-1/U-3 row mentions a DDL column name (gate's own clause-4 wired)."""
    for p, lines in files.items():
        for ln in lines:
            if ln.lstrip().startswith("|") and any(c in ln for c in DDL_COL_NAMES):
                return []
    return ["clause-4: no U-1/U-3 row references a DDL column name (clause-4 exemption never exercised)"]


def check_boundary_declaration(files):
    if OVERVIEW not in files:
        return ["clause-5: §24 §00 not found"]
    text = "\n".join(files[OVERVIEW])
    errs = []
    for lit in BOUNDARY_LITERALS:
        if lit not in text:
            errs.append(f"clause-5: missing boundary literal: {lit!r}")
    return errs


CHECKS = {
    "no-sql-fences": check_no_sql_fences,
    "no-bare-ddl-keywords": check_no_bare_ddl,
    "no-migration-paths": check_no_migration_paths,
    "binding-table-exemption": check_binding_table_exemption,
    "boundary-declaration": check_boundary_declaration,
}


# ---------------- Self-test ----------------

def write_fixture(root: Path, files: dict[str, str]):
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


def fixture_complete_clean() -> dict[str, str]:
    overview = (
        "# §24\n\n"
        "> **No-DDL boundary:** **App-side DDL is owned exclusively by §23.** "
        "**Self-enforcing via §27 backlog gate `no-sql-ddl-in-ui-folder-check`**.\n\n"
        "## U-1\n\n"
        "| ID | Component | Bound to |\n|---|---|---|\n"
        "| U-01 | AppCard | `IsActive` column |\n"
        "## U-3\n\n"
        "| Token | Bound to |\n|---|---|\n"
        "| --app-status-active | `AppId` |\n"
    )
    return {"00-overview.md": overview, "02-child.md": "Plain prose, no DDL.\n"}


def run_self_test_against(files_map) -> list[str]:
    files = {Path(k): v.splitlines() for k, v in files_map.items()}
    # Adjust BOUNDARY_LITERALS check to use the synthetic overview path
    overview_path = next((p for p in files if p.name == "00-overview.md"), None)
    errs = []
    errs.extend(check_no_sql_fences(files))
    errs.extend(check_no_bare_ddl(files))
    errs.extend(check_no_migration_paths(files))
    errs.extend(check_binding_table_exemption(files))
    if overview_path:
        text = "\n".join(files[overview_path])
        for lit in BOUNDARY_LITERALS:
            if lit not in text:
                errs.append(f"clause-5: missing boundary literal: {lit!r}")
    else:
        errs.append("clause-5: §24 §00 not found")
    return errs


SELF_TESTS = []


def self_test() -> int:
    fails = 0
    cases = []

    # F-1 happy
    cases.append(("F-1 complete-clean", True, None, fixture_complete_clean()))

    # F-2 sql fence
    f2 = fixture_complete_clean()
    f2["04-render-spec.md"] = "Render spec.\n\n```sql\nSELECT * FROM App;\n```\n"
    cases.append(("F-2 sql-fence", False, "clause-1", f2))

    # F-3 bare DDL
    f3 = fixture_complete_clean()
    f3["05.md"] = "Run CREATE TABLE App (id INT) on first boot.\n"
    cases.append(("F-3 bare-ddl", False, "clause-2", f3))

    # F-4 migration path
    f4 = fixture_complete_clean()
    f4["06.md"] = "See spec/24-app-design-system-and-ui/migrations/001.sql for schema.\n"
    cases.append(("F-4 migration-path", False, "clause-3", f4))

    # F-5 binding-table exemption broken (no U-1/U-3 column rows)
    f5 = fixture_complete_clean()
    f5["00-overview.md"] = (
        "# §24\n\n"
        "> **App-side DDL is owned exclusively by §23.** "
        "**Self-enforcing via §27 backlog gate `no-sql-ddl-in-ui-folder-check`**.\n"
    )
    cases.append(("F-5 binding-table-exemption-broken", False, "clause-4", f5))

    # F-6 boundary literal stripped
    f6 = fixture_complete_clean()
    f6["00-overview.md"] = f6["00-overview.md"].replace(
        "**Self-enforcing via §27 backlog gate `no-sql-ddl-in-ui-folder-check`**.", ""
    )
    cases.append(("F-6 boundary-stripped", False, "clause-5", f6))

    for name, should_pass, expect, files in cases:
        errs = run_self_test_against(files)
        if should_pass and errs:
            print(f"FAIL {name}: expected pass, got: {errs}")
            fails += 1
        elif not should_pass:
            if not errs:
                print(f"FAIL {name}: expected failure ({expect}), got pass")
                fails += 1
            elif not any(expect in e for e in errs):
                print(f"FAIL {name}: expected {expect}, got: {errs}")
                fails += 1
            else:
                print(f"ok  {name} ({expect})")
        else:
            print(f"ok  {name}")

    if fails:
        print(f"\n{fails} self-test failure(s)")
        return 1
    print(f"\nAll {len(cases)} self-test fixtures passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all", choices=["all", *CHECKS.keys()])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if not UI_DIR.exists():
        print(f"FAIL: {UI_DIR} not found")
        return 1
    paths = sorted(UI_DIR.rglob("*.md"))
    if not paths:
        print("FAIL: vacuous-pass: §24 has zero .md files")
        return 1
    files = scan_files(paths)

    names = list(CHECKS.keys()) if args.check == "all" else [args.check]
    errs = []
    for n in names:
        errs.extend(CHECKS[n](files))
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: {len(names)} clause(s) passed across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

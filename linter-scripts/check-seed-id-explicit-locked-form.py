#!/usr/bin/env python3
"""Slot 54 — check-seed-id-explicit-locked-form.py (gate #32 / Phase-5 T-25).

Enforces the §23 §00 seed-data locked-ID parity contract (AC-ADB-13,
T-10 remediation). See spec/27-spec-toolchain/54-check-seed-id-explicit-locked-form.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent
SEED_FILE = REPO / "spec" / "23-app-database" / "00-overview.md"
SEED_HEADING = "### Seed data (lookup tables) — locked-ID parity"

PRIMARY_FENCE_HEADING = "**PRIMARY lane (SQLite — MATERIALISE):**"
REFERENCE_FENCE_HEADING = (
    "**REFERENCE lane (PostgreSQL — DO NOT MATERIALISE; shown for parity audit only):**"
)
MATRIX_HEADING = "**Seed-ID parity matrix (binding):**"
FORBIDDEN_HEADING = "**Forbidden seed shapes (binding"

PRIMARY_LITERALS = [
    "INSERT OR IGNORE INTO AppStatus (AppStatusId, Name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived')",
    "INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo')",
]
REFERENCE_LITERALS = [
    ("INSERT INTO app_status (app_status_id, name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived')",
     "ON CONFLICT (app_status_id) DO NOTHING"),
    ("INSERT INTO app_link_type(app_link_type_id, name) VALUES (1,'GitProfile'),(2,'Repo')",
     "ON CONFLICT (app_link_type_id) DO NOTHING"),
]
MATRIX_ROWS_EXPECTED = [
    ("AppLinkType", "1", "GitProfile"),
    ("AppLinkType", "2", "Repo"),
    ("AppStatus", "1", "Active"),
    ("AppStatus", "2", "Disabled"),
    ("AppStatus", "3", "Archived"),
]
FORBIDDEN_LITERALS = [
    "INSERT OR IGNORE INTO AppLinkType(Name) VALUES ('GitProfile'),('Repo')",
    "silently de-anchors",
    "IDs are the contract",
]
CITE_CHAIN = [
    "AC-ADB-13", "AC-ADB-11", "T-10 remediation", "MATERIALISE",
    "DO NOT MATERIALISE", "XOR target invariant", "Discriminator", "Q1",
]
RESTATE_RE = re.compile(r"INSERT[^;]*VALUES\s*\(\s*1\s*,\s*'GitProfile'\s*\)", re.IGNORECASE)
RESTATE_DIRS = [
    REPO / "spec" / "22-git-logs-v2",
    REPO / "spec" / "24-app-design-system-and-ui",
    REPO / "spec" / "25-app-issues",
]

WS = re.compile(r"\s+")


def normalise(s: str) -> str:
    return WS.sub(" ", s).strip()


def extract_section(text: str) -> tuple[list[str], int]:
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(SEED_HEADING):
            start = i
            break
    if start is None:
        return [], -1
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("### ") or lines[j].strip() == "---":
            end = j
            break
    return lines[start:end], start


def find_fence_after(lines: list[str], heading_substr: str) -> tuple[list[str], int]:
    for i, ln in enumerate(lines):
        if heading_substr in ln:
            for j in range(i + 1, len(lines)):
                if lines[j].lstrip().startswith("```"):
                    end = j + 1
                    while end < len(lines) and not lines[end].lstrip().startswith("```"):
                        end += 1
                    return lines[j + 1:end], j + 1
    return [], -1


def check_primary(section: list[str]) -> list[str]:
    fence, _ = find_fence_after(section, PRIMARY_FENCE_HEADING)
    if not fence:
        return ["clause-1: PRIMARY lane fence not found"]
    body = normalise(" ".join(fence))
    errs = []
    for lit in PRIMARY_LITERALS:
        if normalise(lit) not in body:
            errs.append(f"clause-1: missing PRIMARY literal: {lit!r}")
    return errs


def check_reference(section: list[str]) -> list[str]:
    fence, _ = find_fence_after(section, REFERENCE_FENCE_HEADING)
    if not fence:
        return ["clause-2: REFERENCE lane fence not found"]
    errs = []
    for insert_lit, conflict_lit in REFERENCE_LITERALS:
        joined = "\n".join(fence)
        norm_joined = normalise(joined)
        if normalise(insert_lit) not in norm_joined:
            errs.append(f"clause-2: missing REFERENCE INSERT: {insert_lit!r}")
            continue
        # Conflict target must follow within 2 lines
        for idx, ln in enumerate(fence):
            if normalise(insert_lit) in normalise(ln) or normalise(insert_lit).split(" VALUES")[0] in normalise(ln):
                window = " ".join(fence[idx:idx + 3])
                if normalise(conflict_lit) not in normalise(window):
                    errs.append(f"clause-2: missing conflict target near {insert_lit!r}: expected {conflict_lit!r}")
                break
    return errs


def check_matrix(section: list[str]) -> list[str]:
    start = None
    for i, ln in enumerate(section):
        if MATRIX_HEADING in ln:
            start = i
            break
    if start is None:
        return ["clause-3: parity matrix heading not found"]
    rows = []
    for ln in section[start:]:
        s = ln.strip()
        if s.startswith("|") and "---" not in s and "Lookup table" not in s:
            cells = [c.strip().strip("`") for c in s.strip("|").split("|")]
            if len(cells) >= 3:
                rows.append((cells[0], cells[1], cells[2]))
        elif rows and not s.startswith("|"):
            break
    if rows != MATRIX_ROWS_EXPECTED:
        return [f"clause-3: matrix rows mismatch: got {rows!r} expected {MATRIX_ROWS_EXPECTED!r}"]
    return []


def check_forbidden(section: list[str]) -> list[str]:
    start = None
    for i, ln in enumerate(section):
        if FORBIDDEN_HEADING in ln:
            start = i
            break
    if start is None:
        return ["clause-4: forbidden-shape block not found"]
    body = "\n".join(section[start:])
    errs = []
    for lit in FORBIDDEN_LITERALS:
        if normalise(lit) not in normalise(body):
            errs.append(f"clause-4: missing forbidden literal: {lit!r}")
    # Numbered items
    if not re.search(r"^\s*1\.", body, re.M) or not re.search(r"^\s*2\.", body, re.M) or not re.search(r"^\s*3\.", body, re.M):
        errs.append("clause-4: missing 1./2./3. numbered items")
    icons = re.findall(r"[❌⚠]", body)
    if icons[:3] != ["❌", "⚠", "❌"]:
        errs.append(f"clause-4: status icons must be ❌/⚠/❌ (got {icons[:3]!r})")
    return errs


def check_cite_chain(section: list[str]) -> list[str]:
    body = "\n".join(section)
    errs = []
    for anchor in CITE_CHAIN:
        if anchor not in body:
            errs.append(f"clause-5: missing cite-chain anchor: {anchor!r}")
    return errs


def check_no_restate() -> list[str]:
    errs = []
    for d in RESTATE_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*.md"):
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            in_sql_fence = False
            for i, ln in enumerate(lines, 1):
                stripped = ln.lstrip()
                if stripped.startswith("```"):
                    lang = stripped[3:].strip().lower()
                    if not in_sql_fence and lang.startswith("sql"):
                        in_sql_fence = True
                    elif in_sql_fence:
                        in_sql_fence = False
                    continue
                if in_sql_fence and RESTATE_RE.search(ln):
                    rel = p.relative_to(REPO)
                    errs.append(f"clause-6: restated seed in {rel}:{i}")
    return errs


CHECKS = {
    "primary-lane-explicit-pk": ("section", check_primary),
    "reference-lane-parity": ("section", check_reference),
    "parity-matrix-coverage": ("section", check_matrix),
    "forbidden-block-literals": ("section", check_forbidden),
    "locked-id-cite-chain": ("section", check_cite_chain),
    "no-restate": ("none", check_no_restate),
}


def run_checks(names: Iterable[str], section: list[str]) -> list[str]:
    errs = []
    for name in names:
        kind, fn = CHECKS[name]
        if kind == "section":
            errs.extend(fn(section))
        else:
            errs.extend(fn())
    return errs


SELF_TEST_FIXTURES = [
    ("happy-path", True, None),
    ("primary-omits-AppStatusId", False, "clause-1"),
    ("reference-bare-do-nothing", False, "clause-2"),
    ("matrix-missing-row", False, "clause-3"),
    ("forbidden-block-removed", False, "clause-4"),
    ("cite-chain-broken", False, "clause-5"),
]


def build_fixture_section(variant: str) -> list[str]:
    primary_app_status = "INSERT OR IGNORE INTO AppStatus  (AppStatusId, Name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived');"
    if variant == "primary-omits-AppStatusId":
        primary_app_status = "INSERT OR IGNORE INTO AppStatus(Name) VALUES ('Active'),('Disabled'),('Archived');"
    ref_app_status_conflict = "  ON CONFLICT (app_status_id) DO NOTHING;"
    if variant == "reference-bare-do-nothing":
        ref_app_status_conflict = "  ON CONFLICT DO NOTHING;"
    matrix_rows = [
        "| `AppLinkType`  | `1`       | `GitProfile` | x | y | z |",
        "| `AppLinkType`  | `2`       | `Repo`       | x | y | z |",
        "| `AppStatus`    | `1`       | `Active`     | x | y | z |",
        "| `AppStatus`    | `2`       | `Disabled`   | x | y | z |",
        "| `AppStatus`    | `3`       | `Archived`   | x | y | z |",
    ]
    if variant == "matrix-missing-row":
        matrix_rows = matrix_rows[:-1]
    forbidden_block = [
        FORBIDDEN_HEADING + " — emit any of these and the CHECK constraint silently de-anchors):**",
        "",
        "1. `INSERT OR IGNORE INTO AppLinkType(Name) VALUES ('GitProfile'),('Repo');` IDs are the contract. ❌",
        "2. Reordering the VALUES tuples — order is documentation. ⚠",
        "3. Mixing the two lane shapes within the same migration file. ❌",
    ]
    if variant == "forbidden-block-removed":
        forbidden_block = []
    cite_extras = "AC-ADB-11 XOR target invariant"
    if variant == "cite-chain-broken":
        cite_extras = ""
    section = [
        SEED_HEADING + " (AC-ADB-13, T-10 remediation)",
        "",
        f"prose Discriminator Q1 {cite_extras}",
        "",
        PRIMARY_FENCE_HEADING,
        "",
        "```sql",
        primary_app_status,
        "INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo');",
        "```",
        "",
        REFERENCE_FENCE_HEADING,
        "",
        "```sql",
        "INSERT INTO app_status   (app_status_id, name) VALUES (1,'Active'),(2,'Disabled'),(3,'Archived')",
        ref_app_status_conflict,
        "INSERT INTO app_link_type(app_link_type_id, name) VALUES (1,'GitProfile'),(2,'Repo')",
        "  ON CONFLICT (app_link_type_id) DO NOTHING;",
        "```",
        "",
        MATRIX_HEADING,
        "",
        "| Lookup table | Locked ID | Locked Name | a | b | c |",
        "|---|---|---|---|---|---|",
        *matrix_rows,
        "",
        *forbidden_block,
    ]
    return section


def self_test() -> int:
    fails = 0
    for name, should_pass, expect in SELF_TEST_FIXTURES:
        section = build_fixture_section(name)
        errs = []
        for cn in ["primary-lane-explicit-pk", "reference-lane-parity",
                   "parity-matrix-coverage", "forbidden-block-literals",
                   "locked-id-cite-chain"]:
            kind, fn = CHECKS[cn]
            errs.extend(fn(section))
        if should_pass and errs:
            print(f"FAIL self-test {name}: expected pass, got: {errs}")
            fails += 1
        elif not should_pass:
            if not errs:
                print(f"FAIL self-test {name}: expected failure ({expect}), got pass")
                fails += 1
            elif not any(expect in e for e in errs):
                print(f"FAIL self-test {name}: expected {expect}, got: {errs}")
                fails += 1
            else:
                print(f"ok  self-test {name} ({expect})")
        else:
            print(f"ok  self-test {name}")
    if fails:
        print(f"\n{fails} self-test failure(s)")
        return 1
    print(f"\nAll {len(SELF_TEST_FIXTURES)} self-test fixtures passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all", choices=["all", *CHECKS.keys()])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if not SEED_FILE.exists():
        print(f"FAIL: {SEED_FILE} not found")
        return 1
    text = SEED_FILE.read_text(encoding="utf-8")
    section, _ = extract_section(text)
    if not section:
        print("FAIL: seed-data section not found in §23 §00")
        return 1

    names = list(CHECKS.keys()) if args.check == "all" else [args.check]
    errs = run_checks(names, section)
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: {len(names)} clause(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

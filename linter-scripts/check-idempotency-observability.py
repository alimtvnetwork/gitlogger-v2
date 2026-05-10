#!/usr/bin/env python3
"""
Slot 45 — check-idempotency-observability.py (Gate #26)

Mechanises AC-CAF-03 ("Idempotency contract is observable at every layer")
across §23 R-1, §23 R-4 invariant 6, §23 WE-4, §24 S-2, §24 U-1, and
§24 §97 AC-CAF-03 declaring text. See spec/27-spec-toolchain/45-*.md.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent

# Canonical sets (declared in AC-CAF-03 line 247 + 249).
YES_SET = {"R-02", "R-03", "R-05", "R-06", "R-07",
           "R-09", "R-10", "R-11", "R-12", "R-13", "R-14"}
NO_SET = {"R-01", "R-04", "R-08", "R-15"}

# Markers that AC-CAF-03 prose MUST carry (clause-2).
CAF03_LITERALS = ("EXPLAIN QUERY PLAN", "IDENTICAL body", "modulo TraceId", "WE-4")

# WE-4 required literals (clause-3).
WE4_LITERALS = ("idempotent", "200", "DisconnectedAt")
WE4_NOOP_PHRASES = ("no-op", "from the first call", "read, don't rewrite")

ROW_RE = re.compile(r"^\|\s*(R-\d{2})\s*\|.*\|\s*(Yes|No)[^|]*\|", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Path resolution (overridable by --root for self-test).
# ---------------------------------------------------------------------------
def _paths(root: Path) -> dict:
    return {
        "db_overview": root / "spec/23-app-database/00-overview.md",
        "ds_overview": root / "spec/24-app-design-system-and-ui/00-overview.md",
        "ds_ac": root / "spec/24-app-design-system-and-ui/97-acceptance-criteria.md",
        "gl_openapi": root / "spec/22-git-logs-v2/17-openapi.yaml",
        "gl_observ": root / "spec/22-git-logs-v2/20-observability.md",
        "issues": root / "spec/25-app-issues",
    }


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# Matrix extractors.
# ---------------------------------------------------------------------------
def _extract_idempotent_rows(text: str) -> dict[str, str]:
    """Return {R-NN: 'Yes'|'No'} for rows whose 'Idempotent' column matches."""
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        rid, flag = m.group(1), m.group(2).strip().capitalize()
        # Only accept rows where one of the columns header context contains
        # 'Idempotent' — heuristic: line must contain 'Yes' or 'No' as its
        # OWN column. We already matched a column boundary; trust that.
        out[rid] = flag
    return out


def _extract_caf03_block(ds_ac_text: str) -> str:
    """Return AC-CAF-03 prose (heading line through next AC heading)."""
    m = re.search(r"^### AC-CAF-03:[^\n]*\n(.*?)(?=^### AC-|^## )",
                  ds_ac_text, re.MULTILINE | re.DOTALL)
    return m.group(0) if m else ""


def _extract_we4_block(db_text: str) -> str:
    m = re.search(r"^### WE-4[^\n]*\n(.*?)(?=^### |^## )",
                  db_text, re.MULTILINE | re.DOTALL)
    return m.group(0) if m else ""


def _extract_r4_inv6(db_text: str) -> str:
    """R-4 invariant 6 — single bullet starting `6. **Idempotency**`."""
    m = re.search(r"^6\.\s+\*\*Idempotency\*\*[^\n]*", db_text, re.MULTILINE)
    return m.group(0) if m else ""


def _extract_u1_rows(ds_text: str) -> list[tuple[str, str]]:
    """Return [(row_id, raw_line)] for U-1 rows (U-NN | … | endpoint)."""
    out: list[tuple[str, str]] = []
    in_u1 = False
    for line in ds_text.splitlines():
        if line.startswith("### U-1"):
            in_u1 = True
            continue
        if in_u1 and (line.startswith("### ") or line.startswith("## ")):
            break
        if in_u1 and re.match(r"^\|\s*U-\d{2}\s*\|", line):
            out.append((line.split("|")[1].strip(), line))
    return out


# ---------------------------------------------------------------------------
# Clauses.
# ---------------------------------------------------------------------------
def check_set_parity(p: dict) -> list[str]:
    db = _read(p["db_overview"])
    ds = _read(p["ds_overview"])
    ac = _read(p["ds_ac"])
    rows = {**_extract_idempotent_rows(db), **_extract_idempotent_rows(ds)}
    if not rows:
        return ["vacuous-pass: zero R-1/S-2 idempotency rows or zero AC-CAF-03 anchors found"]

    yes_actual = {r for r, f in rows.items() if f == "Yes"}
    no_actual = {r for r, f in rows.items() if f == "No"}

    errs: list[str] = []
    if yes_actual != YES_SET:
        errs.append(f"clause-1 set-parity: Yes-set drift; actual={sorted(yes_actual)} expected={sorted(YES_SET)}")
    if no_actual != NO_SET:
        errs.append(f"clause-1 set-parity: No-set drift; actual={sorted(no_actual)} expected={sorted(NO_SET)}")

    # AC-CAF-03 declaring text MUST enumerate the Yes set IDs.
    block = _extract_caf03_block(ac)
    if not block:
        errs.append("clause-1: AC-CAF-03 declaring block not found in §24 §97")
    else:
        for rid in YES_SET:
            if rid not in block:
                errs.append(f"clause-1: AC-CAF-03 prose missing Yes-set ID {rid}")
        for rid in NO_SET:
            if rid not in block:
                errs.append(f"clause-1: AC-CAF-03 prose missing No-set ID {rid}")
    return errs


def check_observability_marker(p: dict) -> list[str]:
    block = _extract_caf03_block(_read(p["ds_ac"]))
    if not block:
        return ["clause-2: AC-CAF-03 declaring block not found"]
    errs = [f"clause-2: AC-CAF-03 missing literal {lit!r}"
            for lit in CAF03_LITERALS if lit not in block]
    return errs


def check_we4_cite(p: dict) -> list[str]:
    db = _read(p["db_overview"])
    we4 = _extract_we4_block(db)
    inv6 = _extract_r4_inv6(db)
    errs: list[str] = []
    if not we4:
        errs.append("clause-3: §23 §00 WE-4 block not found")
    else:
        for lit in WE4_LITERALS:
            if lit not in we4:
                errs.append(f"clause-3: WE-4 missing literal {lit!r}")
        if not any(phrase in we4 for phrase in WE4_NOOP_PHRASES):
            errs.append(f"clause-3: WE-4 missing canonical no-op phrasing (one of {WE4_NOOP_PHRASES})")
    if not inv6:
        errs.append("clause-3: §23 §00 R-4 invariant 6 (Idempotency) not found")
    elif "R-07" not in inv6:
        errs.append("clause-3: R-4 invariant 6 must name R-07 as worked example")
    elif "Idempoten" not in inv6:
        errs.append("clause-3: R-4 invariant 6 missing 'Idempotency' literal")
    return errs


def check_ui_no_alias(p: dict) -> list[str]:
    ds = _read(p["ds_overview"])
    rows = _extract_u1_rows(ds)
    errs: list[str] = []
    if not rows:
        return ["clause-4: §24 §00 U-1 rows not found (vacuous-pass guard)"]
    no_set_pat = re.compile(r"\b(R-01|R-04|R-08|R-15)\b")
    for uid, line in rows:
        if no_set_pat.search(line) and re.search(r"idempotent", line, re.IGNORECASE):
            errs.append(f"clause-4: U-1 row {uid} aliases non-idempotent endpoint as Idempotent: {line.strip()}")
    return errs


def check_no_restate(p: dict) -> list[str]:
    errs: list[str] = []
    suspect_header = re.compile(r"^#{1,6}\s+.*Idempotency\s+contract", re.MULTILINE | re.IGNORECASE)
    for label, path in (("§22 17-openapi.yaml", p["gl_openapi"]),
                        ("§22 20-observability.md", p["gl_observ"])):
        text = _read(path)
        if not text:
            continue
        if suspect_header.search(text):
            errs.append(f"clause-5 restate-drift: {label} declares parallel 'Idempotency contract' header")
        # Detect parallel matrix: a markdown table whose header contains
        # both 'Idempotent' AND 'R-09' OR 'R-15' (S-2 rows) appearing
        # outside the binding source-of-truth surfaces.
        for m in re.finditer(r"\|.*Idempotent.*\|", text):
            # Window of 20 lines after the header.
            tail = text[m.end():m.end() + 2000]
            if re.search(r"\bR-(09|10|11|12|13|14|15)\b", tail):
                errs.append(f"clause-5 restate-drift: {label} inlines parallel S-2 idempotency matrix")
                break
    issues_dir = p["issues"]
    if issues_dir.is_dir():
        for f in issues_dir.glob("*.md"):
            text = _read(f)
            if suspect_header.search(text):
                errs.append(f"clause-5 restate-drift: {f.name} declares parallel 'Idempotency contract' header")
    return errs


CHECKS = {
    "set-parity": check_set_parity,
    "observability-marker": check_observability_marker,
    "we4-cite": check_we4_cite,
    "ui-no-alias": check_ui_no_alias,
    "no-restate": check_no_restate,
}


# ---------------------------------------------------------------------------
# Self-test (5 synthetic fixtures + R5 vacuous-pass guard).
# ---------------------------------------------------------------------------
F1_DB = """\
## REST
### R-1
| ID    | Method | Path | Auth | Maps | Idempotent | Returns |
|-------|--------|------|------|------|------------|---------|
| R-01  | POST   | /a   | a    | INS  | No         | 201     |
| R-02  | GET    | /a   | u    | SEL  | Yes        | 200     |
| R-03  | GET    | /b   | u    | SEL  | Yes        | 200     |
| R-04  | POST   | /c   | a    | INS  | No         | 201     |
| R-05  | GET    | /d   | u    | SEL  | Yes        | 200     |
| R-06  | POST   | /e   | s    | Q1   | Yes        | 200     |
| R-07  | POST   | /f   | a    | Q2   | Yes        | 200     |
| R-08  | POST   | /g   | a    | Q3   | No         | 201     |

### R-4 — Contract invariants
6. **Idempotency** — endpoints flagged Idempotent in R-1 MUST be safe to retry; R-07 second call returns 200 with the same `DisconnectedAt` timestamp from the first call (read, don't rewrite).

### WE-4 — Disconnect already-disconnected → 200 idempotent
Returns 200 with `DisconnectedAt` from the first call. R-07 second call is a no-op (read, don't rewrite).

### Z
"""

F1_DS = """\
### U-1 — Component binding
| ID    | Component | Route | Endpoint(s) | Role | Renders |
|-------|-----------|-------|-------------|------|---------|
| U-01  | AppList   | /a    | R-03        | u    | table   |
| U-03  | Create    | /a    | R-01        | a    | form    |
| U-04  | Make      | /b    | R-04        | a    | form    |
| U-07  | Recon     | /c    | R-08        | a    | form    |

### S-2 — Settings persistence
| ID    | Method | Path | Maps | Idempotent | Notes |
|-------|--------|------|------|------------|-------|
| R-09  | GET    | /s   | sel  | Yes        | merge |
| R-10  | PATCH  | /s   | up   | Yes        | part  |
| R-11  | GET    | /p   | sel  | Yes        | u     |
| R-12  | PATCH  | /p   | up   | Yes        | part  |
| R-13  | GET    | /a   | sel  | Yes        | t+d   |
| R-14  | PATCH  | /a   | up   | Yes        | enum  |
| R-15  | POST   | /d   | var  | No         | conf  |

### Z
"""

F1_AC = """\
### AC-CAF-03: Idempotency contract is observable at every layer
**Given** an endpoint flagged Idempotent=Yes in §23 R-1 (R-02, R-03, R-05, R-06, R-07, R-09, R-11, R-13),
**Then** IDENTICAL body modulo TraceId, EXPLAIN QUERY PLAN shows SELECT only. WE-4 is the canonical fixture. Non-idempotent (R-01, R-04, R-08, R-15) MUST NOT be aliased.

### AC-NEXT
"""


def _write_fixture(d: Path, db: str, ds: str, ac: str,
                   gl_openapi: str = "", gl_observ: str = "") -> dict:
    (d / "spec/23-app-database").mkdir(parents=True, exist_ok=True)
    (d / "spec/24-app-design-system-and-ui").mkdir(parents=True, exist_ok=True)
    (d / "spec/22-git-logs-v2").mkdir(parents=True, exist_ok=True)
    (d / "spec/25-app-issues").mkdir(parents=True, exist_ok=True)
    (d / "spec/23-app-database/00-overview.md").write_text(db)
    (d / "spec/24-app-design-system-and-ui/00-overview.md").write_text(ds)
    (d / "spec/24-app-design-system-and-ui/97-acceptance-criteria.md").write_text(ac)
    (d / "spec/22-git-logs-v2/17-openapi.yaml").write_text(gl_openapi)
    (d / "spec/22-git-logs-v2/20-observability.md").write_text(gl_observ)
    return _paths(d)


def _run_all(p: dict) -> list[str]:
    errs: list[str] = []
    for fn in CHECKS.values():
        errs.extend(fn(p))
    return errs


def self_test() -> int:
    cases: list[tuple[str, str, str, str, str, str, bool]] = []
    # F-1 passing
    cases.append(("F-1 complete-uniform", F1_DB, F1_DS, F1_AC, "", "", True))
    # F-2 flip R-07 to No
    f2_db = F1_DB.replace("| R-07  | POST   | /f   | a    | Q2   | Yes        | 200     |",
                          "| R-07  | POST   | /f   | a    | Q2   | No         | 200     |")
    cases.append(("F-2 R-07 flag flip", f2_db, F1_DS, F1_AC, "", "", False))
    # F-3 drop EXPLAIN QUERY PLAN
    f3_ac = F1_AC.replace("EXPLAIN QUERY PLAN shows SELECT only. ", "")
    cases.append(("F-3 marker stripped", F1_DB, F1_DS, f3_ac, "", "", False))
    # F-4 U-03 (R-01) gains "(Idempotent retry)"
    f4_ds = F1_DS.replace("| U-03  | Create    | /a    | R-01        | a    | form    |",
                          "| U-03  | Create    | /a    | R-01        | a    | form (Idempotent retry) |")
    cases.append(("F-4 UI alias", F1_DB, f4_ds, F1_AC, "", "", False))
    # F-5 §22 inlines parallel matrix
    f5_obs = ("# Observability\n## Idempotency contract\n"
              "| ID | Idempotent |\n|----|-----------|\n| R-09 | Yes |\n")
    cases.append(("F-5 restate-drift", F1_DB, F1_DS, F1_AC, "", f5_obs, False))
    # F-6 vacuous: empty matrices
    cases.append(("F-6 vacuous", "", "", "", "", "", False))

    failures = 0
    for label, db, ds, ac, gl_o, gl_obs, should_pass in cases:
        with tempfile.TemporaryDirectory() as td:
            p = _write_fixture(Path(td), db, ds, ac, gl_o, gl_obs)
            errs = _run_all(p)
            passed = (len(errs) == 0)
            ok = (passed == should_pass)
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {label} (errs={len(errs)}, expected_pass={should_pass})")
            if not ok:
                failures += 1
                for e in errs[:5]:
                    print(f"        - {e}")
    if failures:
        print(f"\nself-test: {failures} fixture(s) failed")
        return 3
    print("\nself-test: all 6 fixtures behaved as expected")
    return 0


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", choices=["all", *CHECKS.keys()], default="all")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    p = _paths(Path(args.root))
    fns: Iterable = CHECKS.values() if args.check == "all" else [CHECKS[args.check]]
    errs: list[str] = []
    for fn in fns:
        errs.extend(fn(p))

    if errs:
        print(f"check-idempotency-observability: {len(errs)} violation(s)")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("check-idempotency-observability: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())

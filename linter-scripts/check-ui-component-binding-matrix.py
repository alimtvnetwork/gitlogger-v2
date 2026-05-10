#!/usr/bin/env python3
"""Slot 49 / Gate #30 — UI component binding matrix check.

Enforces the §24 §00 U-1/U-2/U-3 contract against the §23 §00 R-1
endpoint matrix. See spec/27-spec-toolchain/49-check-ui-component-binding-matrix.md
for the full contract (6 clauses + R5 vacuous-pass guard).
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

ADS_DIR_DEFAULT = REPO / "spec" / "24-app-design-system-and-ui"
ADB_OVERVIEW_DEFAULT = REPO / "spec" / "23-app-database" / "00-overview.md"

ROLE_ENUM = {"user", "admin", "svc", "svc/admin", "admin/svc"}

U2_TABLE_LITERALS = (
    "<AppSkeleton/>",
    "<AppEmptyState/>",
    "<AppErrorState/>",
    "(the component body)",
)
U2_PROSE_LITERALS = ("data-error-code", "Error.TraceId", "copy-to-clipboard")
U3_LITERALS = (
    "IsActive: true",
    "IsActive: false",
    "--app-status-active",
    "--app-status-inactive",
    "MUST NOT render raw `0`/`1`",
    "MUST NOT invert",
    "MUST NOT introduce a third",
    "Mirrors §23 R-4 invariant 2",
)

R_TOKEN_RE = re.compile(r"\bR-\d{2}\b")
U_ROW_RE = re.compile(r"^\|\s*(U-\d{2})\s*\|")
R_ROW_RE = re.compile(r"^\|\s*(R-\d{2})\s*\|")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _section_lines(text: str, header_re: str) -> list[str]:
    """Return the lines under a `### <header>` block until the next `### ` or `## `."""
    lines = text.splitlines()
    out: list[str] = []
    in_block = False
    pat = re.compile(header_re)
    for ln in lines:
        if in_block:
            if ln.startswith("### ") or ln.startswith("## "):
                break
            out.append(ln)
        elif pat.match(ln):
            in_block = True
    return out


def _parse_u1(text: str) -> list[dict]:
    """Parse the U-1 table rows. Returns list of {id, role, endpoints:set[str], raw}."""
    block = _section_lines(text, r"^### U-1\b")
    rows: list[dict] = []
    for ln in block:
        m = U_ROW_RE.match(ln)
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        # cells: ID, Component, Route, Endpoint(s), Role gate, Renders
        endpoints = set(R_TOKEN_RE.findall(cells[3]))
        rows.append({
            "id": cells[0],
            "component": cells[1],
            "endpoints": endpoints,
            "role": cells[4],
        })
    return rows


def _parse_r1(text: str) -> list[dict]:
    """Parse §23 R-1 table. Returns list of {id, role}."""
    block = _section_lines(text, r"^### R-1\b")
    rows: list[dict] = []
    for ln in block:
        m = R_ROW_RE.match(ln)
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        # cells: ID, Method, Path, Role, ...
        rows.append({"id": cells[0], "role": cells[3], "raw": ln})
    return rows


def _u2_block(text: str) -> str:
    return "\n".join(_section_lines(text, r"^### U-2\b"))


def _u3_block(text: str) -> str:
    return "\n".join(_section_lines(text, r"^### U-3\b"))


def check_all(ads_dir: Path, adb_overview: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    overview = ads_dir / "00-overview.md"
    if not overview.exists():
        return 1, [f"missing §24 overview: {overview}"]
    if not adb_overview.exists():
        return 1, [f"missing §23 overview: {adb_overview}"]

    ads_text = _read(overview)
    adb_text = _read(adb_overview)

    u1 = _parse_u1(ads_text)
    r1 = _parse_r1(adb_text)
    u2 = _u2_block(ads_text)
    u3 = _u3_block(ads_text)

    # R5 vacuous-pass guard
    u2_lit_seen = sum(1 for s in U2_TABLE_LITERALS + U2_PROSE_LITERALS if s in u2)
    u3_lit_seen = sum(1 for s in U3_LITERALS if s in u3)
    if not u1 or not r1 or u2_lit_seen == 0 or u3_lit_seen == 0:
        return 1, [
            "vacuous-pass: zero U-1 / R-1 rows or zero U-2 / U-3 literals parsed "
            f"(u1={len(u1)} r1={len(r1)} u2_lit={u2_lit_seen} u3_lit={u3_lit_seen})"
        ]

    r1_ids = {r["id"] for r in r1}

    # Clause 1: U-1 R-NN tokens resolve in §23 R-1
    for row in u1:
        for ep in sorted(row["endpoints"]):
            if ep not in r1_ids:
                errors.append(
                    f"clause-1: U-1 row {row['id']} references {ep} not in §23 R-1"
                )

    # Clause 2: every UI-consumable R-NN (role user|admin) referenced in U-1
    referenced = set().union(*(r["endpoints"] for r in u1)) if u1 else set()
    for r in r1:
        role = r["role"].lower()
        if role in ("user", "admin") and r["id"] not in referenced:
            errors.append(
                f"clause-2: §23 R-1 row {r['id']} (role={r['role']}) is unbound — no U-1 row references it"
            )

    # Clause 3: U-2 four-state literal presence (in table rows) + prose literals
    u2_table_lines = "\n".join(ln for ln in u2.splitlines() if ln.lstrip().startswith("|"))
    u2_prose_lines = "\n".join(ln for ln in u2.splitlines() if not ln.lstrip().startswith("|"))
    for lit in U2_TABLE_LITERALS:
        if lit not in u2_table_lines:
            errors.append(f"clause-3: U-2 table missing slot literal `{lit}`")
    for lit in U2_PROSE_LITERALS:
        if lit not in u2_prose_lines:
            errors.append(f"clause-3: U-2 prose missing literal `{lit}`")

    # Clause 4: role-gate enum discipline
    for row in u1:
        if row["role"] not in ROLE_ENUM:
            errors.append(
                f"clause-4: U-1 row {row['id']} role gate `{row['role']}` not in enum {sorted(ROLE_ENUM)}"
            )

    # Clause 5: U-3 boolean parity literals
    for lit in U3_LITERALS:
        if lit not in u3:
            errors.append(f"clause-5: U-3 missing literal `{lit}`")

    # Clause 6: no restate of §23 R-1 matrix shape in §24
    forbidden_header_re = re.compile(
        r"^\|\s*ID\s*\|\s*Endpoint\s*\|\s*Method\s*\|\s*Path\s*\|", re.IGNORECASE
    )
    for md in sorted(ads_dir.rglob("*.md")):
        for i, ln in enumerate(_read(md).splitlines(), start=1):
            if forbidden_header_re.match(ln):
                errors.append(
                    f"clause-6: {md.relative_to(REPO)}:{i} declares §23 R-1 shape "
                    "`| ID | Endpoint | Method | Path |` (Lesson #36 link-don't-restate)"
                )

    return (1 if errors else 0), errors


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------

_F_R1 = """\
## R API
### R-1 — Endpoint matrix
| ID    | Method | Path                         | Role  | Op            |
|-------|--------|------------------------------|-------|---------------|
| R-01  | POST   | `/api/v1/apps`               | admin | INSERT        |
| R-02  | GET    | `/api/v1/apps/{AppId}`       | user  | SELECT        |
| R-03  | GET    | `/api/v1/apps`               | user  | SELECT        |
"""

_F_U_HEADER = """\
## UI Contract

### U-1 — Component → Endpoint binding matrix

| ID    | Component   | Route   | Endpoint(s) | Role gate | Renders |
|-------|-------------|---------|-------------|-----------|---------|
"""

_U2_GOOD = """\
### U-2 — Async-state contract

| State    | Slot component       | Visible when | Required content |
|----------|----------------------|--------------|------------------|
| loading  | `<AppSkeleton/>`     | x            | y                |
| empty    | `<AppEmptyState/>`   | x            | y                |
| error    | `<AppErrorState/>`   | x            | y                |
| ready    | (the component body) | x            | y                |

The `<AppErrorState/>` slot exposes `Error.Code` as `data-error-code`,
and `Error.TraceId` is visible copy-to-clipboard text.
"""

_U3_GOOD = """\
### U-3 — Boolean rendering parity

Wire `IsActive: true` → `--app-status-active`. Wire `IsActive: false` →
`--app-status-inactive`. MUST NOT render raw `0`/`1` integers,
MUST NOT invert, MUST NOT introduce a third state. Mirrors §23 R-4 invariant 2.
"""


def _write_fixture(tmp: Path, u1_rows: str, *, u2: str = _U2_GOOD, u3: str = _U3_GOOD,
                   extra_md: dict[str, str] | None = None,
                   r1: str = _F_R1) -> tuple[Path, Path]:
    ads = tmp / "spec" / "24-app-design-system-and-ui"
    adb = tmp / "spec" / "23-app-database"
    ads.mkdir(parents=True)
    adb.mkdir(parents=True)
    (ads / "00-overview.md").write_text(_F_U_HEADER + u1_rows + "\n" + u2 + "\n" + u3, encoding="utf-8")
    (adb / "00-overview.md").write_text(r1, encoding="utf-8")
    if extra_md:
        for name, body in extra_md.items():
            (ads / name).write_text(body, encoding="utf-8")
    return ads, adb / "00-overview.md"


_U1_GOOD = """\
| U-01  | `AppList`         | `/apps`        | R-03        | user      | table    |
| U-02  | `AppDetail`       | `/apps/$Id`    | R-02        | user      | detail   |
| U-03  | `AppCreateDialog` | (modal)        | R-01        | admin     | form     |
"""


def _self_test() -> int:
    failures = 0

    def run(label: str, ads_dir: Path, adb_path: Path, expect_pass: bool, expect_clause: str | None = None):
        nonlocal failures
        rc, errs = check_all(ads_dir, adb_path)
        ok_pass = (rc == 0) if expect_pass else (rc != 0)
        ok_clause = True
        if expect_clause and not expect_pass:
            ok_clause = any(expect_clause in e for e in errs)
        status = "PASS" if (ok_pass and ok_clause) else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"  [{status}] {label}: rc={rc} errs={len(errs)} expect_pass={expect_pass} expect={expect_clause}")
        if status == "FAIL":
            for e in errs:
                print(f"        · {e}")

    with tempfile.TemporaryDirectory() as td:
        # F-1 complete-uniform → passes
        ads, adb = _write_fixture(Path(td) / "f1", _U1_GOOD)
        run("F-1 complete-uniform", ads, adb, expect_pass=True)

        # F-2 U-01 binds R-99 → clause-1
        bad = _U1_GOOD.replace("R-03", "R-99", 1)
        ads, adb = _write_fixture(Path(td) / "f2", bad)
        run("F-2 U-01 binds R-99", ads, adb, expect_pass=False, expect_clause="clause-1")

        # F-3 R-12 user but no U-1 row references it
        r1_with_orphan = _F_R1 + "| R-12  | GET    | `/api/v1/foo`                | user  | SELECT        |\n"
        ads, adb = _write_fixture(Path(td) / "f3", _U1_GOOD, r1=r1_with_orphan)
        run("F-3 orphan R-12 user", ads, adb, expect_pass=False, expect_clause="clause-2")

        # F-4 U-2 missing AppErrorState row
        u2_bad = _U2_GOOD.replace("| error    | `<AppErrorState/>`   | x            | y                |\n", "")
        ads, adb = _write_fixture(Path(td) / "f4", _U1_GOOD, u2=u2_bad)
        run("F-4 U-2 omits AppErrorState", ads, adb, expect_pass=False, expect_clause="clause-3")

        # F-5 U-04 role=editor → clause-4
        u1_editor = _U1_GOOD + "| U-04  | `Foo`             | `/foo`         | R-02        | editor    | x        |\n"
        ads, adb = _write_fixture(Path(td) / "f5", u1_editor)
        run("F-5 U-04 role=editor", ads, adb, expect_pass=False, expect_clause="clause-4")

        # F-6 child file with restate of R-1 shape
        extra = {"02-routes.md": "# Routes\n\n| ID | Endpoint | Method | Path |\n|----|----------|--------|------|\n| 1 | a | GET | /x |\n"}
        ads, adb = _write_fixture(Path(td) / "f6", _U1_GOOD, extra_md=extra)
        run("F-6 child restates R-1 shape", ads, adb, expect_pass=False, expect_clause="clause-6")

    if failures:
        print(f"self-test: {failures} fixture(s) failed", file=sys.stderr)
        return 3
    print("self-test: 6/6 fixtures OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", default="all", choices=[
        "all", "u1-endpoints-resolve", "no-orphan-r-endpoints",
        "u2-four-state-literals", "u1-role-enum", "u3-boolean-literals",
        "no-restate-r1",
    ])
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--ads-dir", default=str(ADS_DIR_DEFAULT))
    p.add_argument("--adb-overview", default=str(ADB_OVERVIEW_DEFAULT))
    args = p.parse_args()

    if args.self_test:
        return _self_test()

    rc, errs = check_all(Path(args.ads_dir), Path(args.adb_overview))
    if args.check != "all":
        prefix_map = {
            "u1-endpoints-resolve": "clause-1",
            "no-orphan-r-endpoints": "clause-2",
            "u2-four-state-literals": "clause-3",
            "u1-role-enum": "clause-4",
            "u3-boolean-literals": "clause-5",
            "no-restate-r1": "clause-6",
        }
        prefix = prefix_map[args.check]
        errs = [e for e in errs if e.startswith(prefix) or e.startswith("vacuous-pass")]
        rc = 1 if errs else 0

    for e in errs:
        print(e, file=sys.stderr)
    if rc == 0:
        print(f"check-ui-component-binding-matrix: OK ({args.check})")
    return rc


if __name__ == "__main__":
    sys.exit(main())

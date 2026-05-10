#!/usr/bin/env python3
"""Slot 53 / Gate #31 — AppShell route matrix check.

Enforces the §24 §00 AppShell Route Matrix (AS-NN rows), the
variant→behaviour binding table, the four normative invariants, and
the §24 §97 AC-ADS-UI-04 surface. See
spec/27-spec-toolchain/53-check-appshell-route-matrix.md for the
full 6-clause contract + R5 vacuous-pass guard.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADS_OVERVIEW_DEFAULT = REPO / "spec" / "24-app-design-system-and-ui" / "00-overview.md"
ADS_AC_DEFAULT = REPO / "spec" / "24-app-design-system-and-ui" / "97-acceptance-criteria.md"

VARIANT_ENUM = {"Marketing", "Console", "Settings", "Modal"}
VARIANT_SENTINEL = "(none — no shell)"

AS_HEADER_RE = re.compile(
    r"^\|\s*ID\s*\|\s*Route prefix\s*\|\s*AppShellVariant\s*\|\s*Auth-gated\?\s*\|\s*Notes\s*\|"
)
BIND_HEADER_RE = re.compile(
    r"^\|\s*Variant\s*\|\s*AppToolbar\s*\|\s*AppSidebar\s*\|\s*AppCanvas padding\s*\|\s*Used by\s*\|"
)
AS_ROW_RE = re.compile(r"^\|\s*(AS-\d{2})\s*\|")
AS_TOKEN_RE = re.compile(r"\bAS-\d{2}\b")

INVARIANT_LITERALS = (
    "single source of truth",
    "appshell-route-matrix-check",
    "MUST NOT import from `src/components/app/**`",
    "--app-toolbar-height",
    "5th variant",
)
AC_LITERALS = (
    "AppShell route matrix",
    "8-row AS-NN matrix",
    "4-row variant→behaviour binding table",
    "parity-locked",
)


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _parse_as_matrix(text: str) -> tuple[list[dict], int | None]:
    lines = text.splitlines()
    header_idx = next((i for i, ln in enumerate(lines) if AS_HEADER_RE.match(ln)), None)
    if header_idx is None:
        return [], None
    rows: list[dict] = []
    for ln in lines[header_idx + 2:]:
        if not ln.lstrip().startswith("|"):
            break
        m = AS_ROW_RE.match(ln)
        if not m:
            break
        cells = _split_cells(ln)
        if len(cells) < 5:
            break
        rows.append({
            "id": cells[0],
            "route": cells[1],
            "variant_raw": cells[2],
            "auth": cells[3],
            "notes": cells[4],
        })
    return rows, header_idx


def _parse_binding_table(text: str) -> list[dict]:
    lines = text.splitlines()
    header_idx = next((i for i, ln in enumerate(lines) if BIND_HEADER_RE.match(ln)), None)
    if header_idx is None:
        return []
    rows: list[dict] = []
    for ln in lines[header_idx + 2:]:
        if not ln.lstrip().startswith("|"):
            break
        cells = _split_cells(ln)
        if len(cells) < 5:
            break
        rows.append({
            "variant_raw": cells[0],
            "toolbar": cells[1],
            "sidebar": cells[2],
            "padding": cells[3],
            "used_by": cells[4],
        })
    return rows


def _strip_backticks(s: str) -> str:
    return s.replace("`", "").strip()


def _ac_block(text: str, ac_id: str = "AC-ADS-UI-04") -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_block = False
    pat = re.compile(r"^###\s+" + re.escape(ac_id) + r"\b")
    for ln in lines:
        if in_block:
            if ln.startswith("### ") or ln.startswith("## "):
                break
            out.append(ln)
        elif pat.match(ln):
            in_block = True
            out.append(ln)
    return "\n".join(out)


def check_all(overview: Path, ac_file: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    if not overview.exists():
        return 1, [f"missing §24 overview: {overview}"]
    if not ac_file.exists():
        return 1, [f"missing §24 §97: {ac_file}"]

    text = _read(overview)
    ac_text = _read(ac_file)

    as_rows, _ = _parse_as_matrix(text)
    bind_rows = _parse_binding_table(text)
    ac_block = _ac_block(ac_text, "AC-ADS-UI-04")

    # R5 vacuous-pass guard
    if len(as_rows) < 8 or len(bind_rows) < 4 or not ac_block:
        return 1, [
            f"vacuous-pass: AS-NN matrix < 8 rows / binding table < 4 rows / "
            f"AC-ADS-UI-04 surface absent (as={len(as_rows)} bind={len(bind_rows)} ac={'yes' if ac_block else 'no'})"
        ]

    # Clause 1: matrix presence + shape + AS-IDs unique + contiguous from AS-01
    seen: set[str] = set()
    for row in as_rows:
        if row["id"] in seen:
            errors.append(f"clause-1: AS-NN matrix duplicate ID {row['id']}")
        seen.add(row["id"])
    for i, row in enumerate(as_rows, start=1):
        expected = f"AS-{i:02d}"
        if row["id"] != expected:
            errors.append(
                f"clause-1: AS-NN matrix gap or out-of-order at row {i}: expected {expected}, got {row['id']}"
            )
            break

    # Clause 2: variant enum closed-set
    observed_variants: set[str] = set()
    for row in as_rows:
        v_clean = _strip_backticks(row["variant_raw"])
        if v_clean == VARIANT_SENTINEL:
            continue
        if v_clean not in VARIANT_ENUM:
            errors.append(
                f"clause-2: AS-NN row {row['id']} variant `{row['variant_raw']}` not in enum {sorted(VARIANT_ENUM)} (or sentinel)"
            )
        else:
            observed_variants.add(v_clean)

    # Clause 3: variant↔binding parity (bidirectional)
    bind_variants: dict[str, dict] = {}
    for r in bind_rows:
        v_clean = _strip_backticks(r["variant_raw"])
        if v_clean in VARIANT_ENUM:
            bind_variants[v_clean] = r

    for v in observed_variants:
        if v not in bind_variants:
            errors.append(
                f"clause-3: variant `{v}` present in AS-NN matrix but missing from variant→behaviour binding table"
            )
        else:
            cited = set(AS_TOKEN_RE.findall(bind_variants[v]["used_by"]))
            if not cited:
                errors.append(
                    f"clause-3: binding row for `{v}` has empty `Used by` (no AS-NN citations)"
                )
    for v in bind_variants:
        if v not in observed_variants:
            errors.append(
                f"clause-3: binding row for `{v}` is orphan — no AS-NN row uses this variant"
            )

    # Clause 4: Marketing rows MUST cite "MUST NOT import" + AC-ADS-06
    for row in as_rows:
        if _strip_backticks(row["variant_raw"]) != "Marketing":
            continue
        if "MUST NOT import" not in row["notes"]:
            errors.append(
                f"clause-4: Marketing AS-NN row {row['id']} notes missing literal `MUST NOT import`"
            )
        if "AC-ADS-06" not in row["notes"]:
            errors.append(
                f"clause-4: Marketing AS-NN row {row['id']} notes missing AC-ADS-06 cite"
            )

    # Clause 5: invariant block literal presence
    for lit in INVARIANT_LITERALS:
        if lit not in text:
            errors.append(f"clause-5: §24 §00 missing invariant literal `{lit}`")

    # Clause 6: AC-ADS-UI-04 surface literals
    for lit in AC_LITERALS:
        if lit not in ac_block:
            # Also accept the §00 surface (AC-ADS-UI-04 is declared there in current spec)
            if lit not in text:
                errors.append(f"clause-6: AC-ADS-UI-04 body missing literal `{lit}`")

    return (1 if errors else 0), errors


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------

_AS_GOOD = """\
| ID    | Route prefix | AppShellVariant | Auth-gated? | Notes |
|-------|--------------|-----------------|-------------|-------|
| AS-01 | `/`          | `Marketing`     | No          | MUST NOT import `AppShell` (AC-ADS-06). |
| AS-02 | `/login`     | `Marketing`     | No          | MUST NOT import `AppShell` (AC-ADS-06). |
| AS-03 | `/apps`      | `Console`       | Yes         | full shell |
| AS-04 | `/x`         | `Console`       | Yes         | x |
| AS-05 | `/r`         | `Console`       | Yes         | r |
| AS-06 | `/settings`  | `Settings`      | Yes         | settings |
| AS-07 | `/api/*`     | (none — no shell) | varies    | server only |
| AS-08 | `*`          | `Modal`         | No          | 404 |
"""

_BIND_GOOD = """\
| Variant     | AppToolbar | AppSidebar | AppCanvas padding | Used by      |
|-------------|------------|------------|-------------------|--------------|
| `Marketing` | (none)     | (none)     | full-bleed        | AS-01, AS-02 |
| `Console`   | full       | primary    | `--space-4`       | AS-03, AS-04, AS-05 |
| `Settings`  | full       | settings   | `--space-6`       | AS-06        |
| `Modal`     | minimal    | (none)     | `--space-8`       | AS-08        |
"""

_INV_GOOD = """\
**Invariants (binding):**

1. The matrix is the single source of truth — `appshell-route-matrix-check` enforces it.
2. Marketing routes MUST NOT import from `src/components/app/**`.
3. Variants share the `--app-toolbar-height` token.
4. Adding a 5th variant requires a paired binding row.
"""

_AC_GOOD = """\
### AC-ADS-UI-04 — AppShell route matrix present and parity-locked

The 8-row AS-NN matrix and the 4-row variant→behaviour binding table MUST be
present in `00-overview.md`. AppShell route matrix is parity-locked.
"""


def _write_fixture(tmp: Path, *, as_table: str = _AS_GOOD, bind: str = _BIND_GOOD,
                   inv: str = _INV_GOOD, ac: str = _AC_GOOD) -> tuple[Path, Path]:
    ads = tmp / "spec" / "24-app-design-system-and-ui"
    ads.mkdir(parents=True)
    (ads / "00-overview.md").write_text(
        "## AppShell Route Matrix\n\n" + as_table + "\n" + bind + "\n" + inv,
        encoding="utf-8",
    )
    (ads / "97-acceptance-criteria.md").write_text(ac, encoding="utf-8")
    return ads / "00-overview.md", ads / "97-acceptance-criteria.md"


def _self_test() -> int:
    failures = 0

    def run(label: str, overview: Path, ac: Path, expect_pass: bool, expect_clause: str | None = None):
        nonlocal failures
        rc, errs = check_all(overview, ac)
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
        # F-1
        ov, ac = _write_fixture(Path(td) / "f1")
        run("F-1 complete-uniform", ov, ac, expect_pass=True)

        # F-2 gap AS-03
        as_gap = _AS_GOOD.replace(
            "| AS-03 | `/apps`      | `Console`       | Yes         | full shell |\n", ""
        )
        ov, ac = _write_fixture(Path(td) / "f2", as_table=as_gap)
        run("F-2 AS-NN gap AS-03", ov, ac, expect_pass=False, expect_clause="clause-1")

        # F-3 AS-04 variant Dashboard (free-form)
        as_bad = _AS_GOOD.replace("| AS-04 | `/x`         | `Console`", "| AS-04 | `/x`         | `Dashboard`")
        ov, ac = _write_fixture(Path(td) / "f3", as_table=as_bad)
        run("F-3 AS-04 variant Dashboard", ov, ac, expect_pass=False, expect_clause="clause-2")

        # F-4 binding table omits Settings
        bind_bad = _BIND_GOOD.replace(
            "| `Settings`  | full       | settings   | `--space-6`       | AS-06        |\n", ""
        )
        ov, ac = _write_fixture(Path(td) / "f4", bind=bind_bad)
        run("F-4 binding omits Settings", ov, ac, expect_pass=False, expect_clause="clause-3")

        # F-5 AS-01 Marketing notes drops MUST NOT import
        as_bad = _AS_GOOD.replace(
            "| AS-01 | `/`          | `Marketing`     | No          | MUST NOT import `AppShell` (AC-ADS-06). |",
            "| AS-01 | `/`          | `Marketing`     | No          | landing page. |",
        )
        ov, ac = _write_fixture(Path(td) / "f5", as_table=as_bad)
        run("F-5 AS-01 drops MUST NOT import", ov, ac, expect_pass=False, expect_clause="clause-4")

        # F-6 AC-ADS-UI-04 drops parity-locked
        ac_bad = _AC_GOOD.replace("parity-locked", "PARITYLOCK").replace("parity-locked", "PARITYLOCK")
        ov, ac = _write_fixture(Path(td) / "f6", ac=ac_bad)
        run("F-6 AC-ADS-UI-04 drops parity-locked", ov, ac, expect_pass=False, expect_clause="clause-6")

    if failures:
        print(f"self-test: {failures} fixture(s) failed", file=sys.stderr)
        return 3
    print("self-test: 6/6 fixtures OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", default="all", choices=[
        "all", "matrix-shape", "variant-enum", "binding-parity",
        "marketing-boundary", "invariant-literals", "ac-ads-ui-04-surface",
    ])
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--overview", default=str(ADS_OVERVIEW_DEFAULT))
    p.add_argument("--ac-file", default=str(ADS_AC_DEFAULT))
    args = p.parse_args()

    if args.self_test:
        return _self_test()

    rc, errs = check_all(Path(args.overview), Path(args.ac_file))
    if args.check != "all":
        prefix_map = {
            "matrix-shape": "clause-1",
            "variant-enum": "clause-2",
            "binding-parity": "clause-3",
            "marketing-boundary": "clause-4",
            "invariant-literals": "clause-5",
            "ac-ads-ui-04-surface": "clause-6",
        }
        prefix = prefix_map[args.check]
        errs = [e for e in errs if e.startswith(prefix) or e.startswith("vacuous-pass")]
        rc = 1 if errs else 0

    for e in errs:
        print(e, file=sys.stderr)
    if rc == 0:
        print(f"check-appshell-route-matrix: OK ({args.check})")
    return rc


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
r"""Gate #33 — check-dialect-precedence-banner-present.

Mechanises §23 §00 dialect precedence banner + §22 §00 single-dialect
declaration. Six clauses (slot-55 contract):

  1. §23 §00 precedence heading present and BEFORE first SQL fence.
  2. Lane table closed-set discipline (PRIMARY + REFERENCE rows + literals).
  3. Cross-cuts pin block carries all 6 required literals.
  4. AI-walker contract paragraph literals present.
  5. Every SQL fence in §23 walked is preceded within 30 lines by a
     lane marker (4-form whitelist). _archive/ exempt.
  6. §22 §00 declares `Database engine` → `SQLite` within 5 lines.
  R5. Vacuous-pass guard.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_ROOT = REPO_ROOT / "spec"
APP_DB_DIR = SPEC_ROOT / "23-app-database"
APP_DB_OVERVIEW = APP_DB_DIR / "00-overview.md"
GIT_LOGS_OVERVIEW = SPEC_ROOT / "22-git-logs-v2" / "00-overview.md"

PRECEDENCE_HEADING = "## Implementation Target Precedence (Normative — read before any DDL block)"

LANE_TABLE_PRIMARY_LITERALS = ("**PRIMARY**", "SQLite", "PascalCase", "INTEGER",
                                "ACTIVE", "✅ YES")
LANE_TABLE_REFERENCE_LITERALS = ("**REFERENCE**", "PostgreSQL", "snake_case", "boolean",
                                  "REFERENCE ONLY", "❌ NO",
                                  "silent dialect-flip is FORBIDDEN")

CROSS_CUTS_LITERALS = (
    "Boolean policy (AC-ADB-11",
    "Timestamp parity (AC-ADB-16)",
    "Seed ID parity (AC-ADB-13)",
    "Any code emitting `boolean` on the App database is a violation",
    "EXTRACT(EPOCH FROM",
    "INSERT … VALUES (1,'GitProfile'),(2,'Repo')",
)

AI_WALKER_LITERALS = (
    "partial-context violation",
    "re-anchor",
    "§00 Quick-Nav guarantees this pin is reached on a TOC walk",
)

LANE_MARKERS = (
    "**PRIMARY lane (SQLite — MATERIALISE):**",
    "**REFERENCE lane (PostgreSQL — DO NOT MATERIALISE; shown for parity audit only):**",
    "### 🚫 REFERENCE-ONLY",
    "> **⚠️ Reference / Secondary dialect (per AC-ADB-11).**",
)

SQL_FENCE_RE = re.compile(r"^```sql(?:ite)?\s*$")


# ---------- Surface ----------

@dataclass
class Surface:
    app_db_overview: str = ""
    git_logs_overview: str = ""
    app_db_files: list[tuple[Path, str]] = field(default_factory=list)

    @classmethod
    def from_disk(cls) -> "Surface":
        s = cls(
            app_db_overview=_safe_read(APP_DB_OVERVIEW),
            git_logs_overview=_safe_read(GIT_LOGS_OVERVIEW),
        )
        if APP_DB_DIR.exists():
            for p in sorted(APP_DB_DIR.rglob("*.md")):
                if "_archive" in p.parts:
                    continue
                s.app_db_files.append((p, p.read_text(encoding="utf-8")))
        return s


def _safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---------- Clauses ----------

def clause_banner_position(surf: Surface) -> list[str]:
    errs: list[str] = []
    text = surf.app_db_overview
    if PRECEDENCE_HEADING not in text:
        errs.append("clause-1: §23 §00 precedence heading absent")
        return errs
    lines = text.splitlines()
    heading_idx = next(i for i, ln in enumerate(lines) if ln.strip() == PRECEDENCE_HEADING)
    first_fence = next((i for i, ln in enumerate(lines) if SQL_FENCE_RE.match(ln.strip())), None)
    if first_fence is not None and first_fence < heading_idx:
        errs.append(f"clause-1: precedence heading at line {heading_idx + 1} appears AFTER first SQL fence at line {first_fence + 1}")
    return errs


def clause_lane_table_literals(surf: Surface) -> list[str]:
    errs: list[str] = []
    text = surf.app_db_overview
    if PRECEDENCE_HEADING not in text:
        return ["clause-2: precedence heading missing — cannot locate lane table"]
    # Slice from heading to next "##" heading
    idx = text.find(PRECEDENCE_HEADING)
    nxt = text.find("\n## ", idx + len(PRECEDENCE_HEADING))
    section = text[idx:nxt] if nxt > 0 else text[idx:]
    # Lane table rows: lines starting with "> | **PRIMARY**" etc.
    primary_rows = [ln for ln in section.splitlines() if "**PRIMARY**" in ln and "|" in ln]
    reference_rows = [ln for ln in section.splitlines() if "**REFERENCE**" in ln and "|" in ln]
    if len(primary_rows) != 1:
        errs.append(f"clause-2: expected exactly 1 PRIMARY data row, got {len(primary_rows)}")
    if len(reference_rows) != 1:
        errs.append(f"clause-2: expected exactly 1 REFERENCE data row, got {len(reference_rows)}")
    if primary_rows:
        for lit in LANE_TABLE_PRIMARY_LITERALS:
            if lit not in primary_rows[0]:
                errs.append(f"clause-2: PRIMARY row missing literal `{lit}`")
    if reference_rows:
        for lit in LANE_TABLE_REFERENCE_LITERALS:
            if lit not in reference_rows[0]:
                errs.append(f"clause-2: REFERENCE row missing literal `{lit}`")
    # ordering: PRIMARY before REFERENCE
    if primary_rows and reference_rows:
        if section.find(primary_rows[0]) > section.find(reference_rows[0]):
            errs.append("clause-2: PRIMARY row appears after REFERENCE row (order violation)")
    return errs


def clause_cross_cuts_literals(surf: Surface) -> list[str]:
    errs: list[str] = []
    text = surf.app_db_overview
    if PRECEDENCE_HEADING not in text:
        return ["clause-3: precedence heading missing"]
    idx = text.find(PRECEDENCE_HEADING)
    nxt = text.find("\n## ", idx + len(PRECEDENCE_HEADING))
    section = text[idx:nxt] if nxt > 0 else text[idx:]
    for lit in CROSS_CUTS_LITERALS:
        if lit not in section:
            errs.append(f"clause-3: cross-cuts block missing literal `{lit}`")
    return errs


def clause_ai_walker_contract(surf: Surface) -> list[str]:
    errs: list[str] = []
    text = surf.app_db_overview
    if PRECEDENCE_HEADING not in text:
        return ["clause-4: precedence heading missing"]
    idx = text.find(PRECEDENCE_HEADING)
    nxt = text.find("\n## ", idx + len(PRECEDENCE_HEADING))
    section = text[idx:nxt] if nxt > 0 else text[idx:]
    for lit in AI_WALKER_LITERALS:
        if lit not in section:
            errs.append(f"clause-4: AI-walker contract missing literal `{lit}`")
    return errs


def _line_has_lane_marker(line: str) -> bool:
    s = line.strip()
    for m in LANE_MARKERS:
        if s == m or s.startswith(m):
            return True
    return False


def clause_fence_restate_markers(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.app_db_files:
        lines = text.splitlines()
        for i, ln in enumerate(lines):
            if not SQL_FENCE_RE.match(ln.strip()):
                continue
            window = lines[max(0, i - 30):i]
            if any(_line_has_lane_marker(w) for w in window):
                continue
            rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
            errs.append(f"clause-5: {rel}:{i + 1}: SQL fence with no lane marker in prior 30 lines")
    return errs


def clause_spec22_single_dialect(surf: Surface) -> list[str]:
    errs: list[str] = []
    text = surf.git_logs_overview
    if not text:
        errs.append("clause-6: §22 §00 absent")
        return errs
    lines = text.splitlines()
    found = False
    for i, ln in enumerate(lines):
        if "Database engine" in ln:
            window = "\n".join(lines[i:i + 6])
            if "SQLite" in window:
                found = True
                break
    if not found:
        errs.append("clause-6: §22 §00 missing `Database engine` row paired with `SQLite` within 5 lines")
    return errs


def clause_vacuous(surf: Surface) -> list[str]:
    errs: list[str] = []
    if PRECEDENCE_HEADING not in surf.app_db_overview:
        errs.append("vacuous-pass: §23 §00 precedence section absent")
    fence_count = sum(
        1 for _, t in surf.app_db_files
        for ln in t.splitlines() if SQL_FENCE_RE.match(ln.strip())
    )
    if fence_count == 0:
        errs.append("vacuous-pass: zero SQL fences scanned in §23")
    if "Database engine" not in surf.git_logs_overview:
        errs.append("vacuous-pass: §22 §00 Database-engine row absent")
    return errs


CHECKS = {
    "banner-position": clause_banner_position,
    "lane-table-literals": clause_lane_table_literals,
    "cross-cuts-literals": clause_cross_cuts_literals,
    "ai-walker-contract": clause_ai_walker_contract,
    "fence-restate-markers": clause_fence_restate_markers,
    "spec22-single-dialect": clause_spec22_single_dialect,
}


def run_all(surf: Surface) -> list[str]:
    v = clause_vacuous(surf)
    if v:
        return v
    out: list[str] = []
    for fn in (
        clause_banner_position,
        clause_lane_table_literals,
        clause_cross_cuts_literals,
        clause_ai_walker_contract,
        clause_fence_restate_markers,
        clause_spec22_single_dialect,
    ):
        out.extend(fn(surf))
    return out


# ---------- Self-test ----------

GOOD_PRECEDENCE = f"""# §23 §00

## Document Inventory

| # | File | Purpose |
|---|------|---------|
| 00 | `00-overview.md` | x |

{PRECEDENCE_HEADING}

> **🚦 Single source:** pin
>
> | Lane | Dialect | Naming | Boolean | PK | Status | Canonical surface | Materialise? |
> |------|---------|--------|---------|----|--------|-------------------|--------------|
> | **PRIMARY** | SQLite (3.40+) | PascalCase | `INTEGER` 0/1 + `Is` prefix | `INTEGER PRIMARY KEY AUTOINCREMENT` | **ACTIVE — every consuming binary MUST use this lane** | `## Inlined Contracts` § "DDL" | ✅ YES |
> | **REFERENCE** | PostgreSQL 15+ | snake_case | `boolean` | `uuid DEFAULT gen_random_uuid()` | **REFERENCE ONLY — preserved for snake_case** | `## Inlined Contracts` § "REFERENCE ONLY" | ❌ NO — silent dialect-flip is FORBIDDEN per AC-ADB-11 |
>
> **Cross-cuts pinned here so a 1-section read cannot miss them:**
> - **Boolean policy (AC-ADB-11 + Convention recap below):** Any code emitting `boolean` on the App database is a violation regardless.
> - **Timestamp parity (AC-ADB-16):** wrap (`EXTRACT(EPOCH FROM …)::bigint` on read) — never surfaced as ISO-8601.
> - **Seed ID parity (AC-ADB-13):** explicit `INSERT … VALUES (1,'GitProfile'),(2,'Repo')` is the only conformant seed shape.
>
> **AI-walker contract:** if a reader reaches any DDL fence without passing this precedence pin, treat the read as a **partial-context violation** and re-anchor. The §00 Quick-Nav guarantees this pin is reached on a TOC walk.

## DDL

**PRIMARY lane (SQLite — MATERIALISE):**

```sql
CREATE TABLE App ( AppId INTEGER PRIMARY KEY );
```
"""

GOOD_GIT_LOGS = """# §22 §00

## Decisions Matrix

| # | Decision | Value |
|---|----------|-------|
| 1 | Database engine | SQLite (Gitlogs root DB), single file |
"""


def _surf(app_db=GOOD_PRECEDENCE, git_logs=GOOD_GIT_LOGS,
          extra_files: list[tuple[str, str]] | None = None) -> Surface:
    files = [(Path("spec/23-app-database/00-overview.md"), app_db)]
    for name, body in extra_files or []:
        files.append((Path(f"spec/23-app-database/{name}"), body))
    return Surface(app_db_overview=app_db, git_logs_overview=git_logs, app_db_files=files)


def self_test() -> int:
    fails: list[str] = []

    # F-1 complete-uniform → passes
    errs = run_all(_surf())
    if errs:
        fails.append(f"F-1 should pass; got: {errs[:5]}")

    # F-2 precedence heading appears AFTER first SQL fence
    bad = (
        "# §23 §00\n\n## DDL\n\n```sql\nCREATE TABLE X (X INTEGER);\n```\n\n"
        + PRECEDENCE_HEADING + "\n\n> pin\n"
    )
    if not any("AFTER first SQL fence" in e for e in clause_banner_position(_surf(app_db=bad))):
        fails.append("F-2 should fail clause-1 (positional reorder)")

    # F-3 REFERENCE row drops `silent dialect-flip is FORBIDDEN`
    bad = GOOD_PRECEDENCE.replace("silent dialect-flip is FORBIDDEN per AC-ADB-11", "neutral note")
    if not any("silent dialect-flip is FORBIDDEN" in e for e in clause_lane_table_literals(_surf(app_db=bad))):
        fails.append("F-3 should fail clause-2 (REFERENCE literal stripped)")

    # F-4 cross-cuts omit EXTRACT literal
    bad = GOOD_PRECEDENCE.replace("EXTRACT(EPOCH FROM …)::bigint", "wrap-on-read")
    if not any("EXTRACT(EPOCH FROM" in e for e in clause_cross_cuts_literals(_surf(app_db=bad))):
        fails.append("F-4 should fail clause-3 (timestamp literal stripped)")

    # F-5 child file with bare ```sql fence and no marker in prior 30 lines
    child_body = "# 02 queries\n\nNo marker here.\n\n```sql\nSELECT 1;\n```\n"
    surf = _surf(extra_files=[("02-queries.md", child_body)])
    if not any("no lane marker" in e for e in clause_fence_restate_markers(surf)):
        fails.append("F-5 should fail clause-5 (unlabelled child SQL fence)")

    # F-6 §22 §00 sets Database engine → MariaDB (no SQLite within 5 lines)
    bad_gl = "# §22\n\n| 1 | Database engine | MariaDB |\n"
    if not any("§22 §00" in e for e in clause_spec22_single_dialect(_surf(git_logs=bad_gl))):
        fails.append("F-6 should fail clause-6 (§22 single-dialect violated)")

    if fails:
        for f in fails:
            print(f"  ✘ {f}", file=sys.stderr)
        print(f"--self-test: {len(fails)} fixture(s) failed", file=sys.stderr)
        return 3
    print("--self-test: 6/6 fixtures passed (F-1 unique-passing + 5 failure variants)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", default="all", help="all | " + " | ".join(CHECKS.keys()))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    surf = Surface.from_disk()

    if args.check == "all":
        errs = run_all(surf)
    elif args.check in CHECKS:
        errs = CHECKS[args.check](surf)
    else:
        print(f"error: unknown --check mode `{args.check}`", file=sys.stderr)
        return 2

    if errs:
        for e in errs[:80]:
            print(f"  ✘ {e}", file=sys.stderr)
        if len(errs) > 80:
            print(f"  … and {len(errs) - 80} more", file=sys.stderr)
        print(f"check-dialect-precedence-banner-present: {len(errs)} violation(s) (mode={args.check})",
              file=sys.stderr)
        return 1
    print(f"check-dialect-precedence-banner-present: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

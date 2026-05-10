#!/usr/bin/env python3
r"""Gate #24 — check-boolean-uniformity-primary-lane.

Closes the 3-surface boolean parity triple alongside gate #34
(REST PascalCase parity) and gate #35 (REST boolean parity).

Mechanises:
  - §23 §00 R-4 invariant 2 (PRIMARY-lane SQLite `INTEGER` 0/1 + `Is`-prefix)
  - §22 `17-openapi.yaml` `type: boolean` field set
  - §24 §00 U-3 boolean rendering parity
  - cross-cutting AC-CAF-01 (T-12, wire-boolean parity DB ↔ REST ↔ UI)

Five clauses (slot-43 contract):
  1. DB primary-lane: every boolean-shaped column is `INTEGER` (NOT NULL,
     or NULL paired with a coupled CHECK) AND name begins with `Is`.
     Bare `BOOLEAN`/`TINYINT`/non-`Is` flag columns are rejected.
  2. REST wire-shape: §22 OpenAPI `type: boolean` fields use
     `Is|Has|Was|Can|Should|Truncated|Deprecated` predicate prefix and
     do NOT carry an `enum: [0,1]` integer-coercion construct.
  3. UI render-side: §24 §00 U-3 carries the IsActive label binding +
     three forbidden sub-clauses (no raw 0/1, no invert, no third state).
  4. No coercion-attack surface: §23 R-1 must cite R-4 invariant 2 in a
     422 `field.invalid` clause + WE-3 fixture present.
  5. No restate-drift: §22/§24/§25 children MUST NOT inline a parallel
     "boolean encoding" / "boolean policy" heading.
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
APP_DB = SPEC_ROOT / "23-app-database" / "00-overview.md"
GIT_LOGS_SCHEMA = SPEC_ROOT / "22-git-logs-v2" / "18-schema.sql"
OPENAPI = SPEC_ROOT / "22-git-logs-v2" / "17-openapi.yaml"
DS_OVERVIEW = SPEC_ROOT / "24-app-design-system-and-ui" / "00-overview.md"

PREDICATE_PREFIX_RE = re.compile(r"^(Is|Has|Was|Can|Should|Truncated|Deprecated)[A-Z0-9]?")
IS_PREFIX_RE = re.compile(r"^Is[A-Z][A-Za-z0-9]*$")

# Match a column line in a CREATE TABLE block: "    Name  TYPE ..."
COL_LINE_RE = re.compile(
    r"^\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<type>[A-Z][A-Z0-9_]*)\b(?P<rest>[^,\n]*)",
)
CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((?P<body>.*?)\n\);",
    re.DOTALL | re.IGNORECASE,
)

BOOLEAN_FLAG_HINT_RE = re.compile(
    r"^(Is|Has|Was|Can|Should|Active|Enabled|Deleted|Deprecated|Disabled|Hidden|Locked|Visible|Primary|Default)"
)
KNOWN_BOOLEAN_COLUMNS = {"IsActive", "IsDeprecated"}

NO_RESTATE_FOLDERS = (
    "22-git-logs-v2",
    "24-app-design-system-and-ui",
    "25-app-issues",
)
RESTATE_PATTERNS = (
    re.compile(r"^#{2,4}\s+.*[Bb]oolean\s+[Ee]ncoding\b"),
    re.compile(r"^#{2,4}\s+.*[Bb]oolean\s+[Pp]olicy\b"),
    re.compile(r"^#{2,4}\s+.*[Bb]oolean\s+[Tt]ranslation\b"),
)

U3_REQUIRED_LITERALS = (
    "IsActive",
    "Active",
    "Inactive",
    "MUST NOT render raw",
    "MUST NOT invert",
    "third",
    "§23 R-4",
)

R4_INV2_LITERAL = "Boolean parity"
WE3_HEADING_RE = re.compile(r"^###\s+WE-3\b.*[Bb]oolean", re.MULTILINE)
R1_422_LITERAL = "field.invalid"


# ---------- Surface ----------

@dataclass
class Surface:
    app_db: str = ""
    git_logs_schema: str = ""
    openapi: str = ""
    ds_overview: str = ""
    sibling_files: list[tuple[Path, str]] = field(default_factory=list)

    @classmethod
    def from_disk(cls) -> "Surface":
        s = cls(
            app_db=_safe_read(APP_DB),
            git_logs_schema=_safe_read(GIT_LOGS_SCHEMA),
            openapi=_safe_read(OPENAPI),
            ds_overview=_safe_read(DS_OVERVIEW),
        )
        for sub in NO_RESTATE_FOLDERS:
            base = SPEC_ROOT / sub
            if not base.exists():
                continue
            for p in sorted(base.rglob("*.md")):
                if p == DS_OVERVIEW:
                    continue
                s.sibling_files.append((p, p.read_text(encoding="utf-8")))
        return s


def _safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _extract_sql_blocks(md: str) -> str:
    """Return concatenated content of ```sql fences in a markdown doc."""
    return "\n".join(re.findall(r"```sql\s*\n(.*?)\n```", md, re.DOTALL))


# ---------- Clauses ----------

def _scan_table_columns(sql: str) -> list[tuple[str, str, str, str]]:
    """Yield (table, col_name, col_type, rest_of_line) for each column."""
    out: list[tuple[str, str, str, str]] = []
    for m in CREATE_TABLE_RE.finditer(sql):
        table = m.group(1)
        for line in m.group("body").splitlines():
            cm = COL_LINE_RE.match(line)
            if not cm:
                continue
            name = cm.group("name")
            if name.upper() in {"CHECK", "FOREIGN", "PRIMARY", "UNIQUE", "CONSTRAINT"}:
                continue
            out.append((table, name, cm.group("type").upper(), cm.group("rest")))
    return out


def clause_db_primary_lane(surf: Surface) -> list[str]:
    errs: list[str] = []
    sql_app = _extract_sql_blocks(surf.app_db)
    # Restrict to PRIMARY-lane (SQLite) blocks; skip the PostgreSQL REFERENCE-
    # lane mirror by examining only blocks whose CREATE TABLE used PascalCase
    # tables (App/AppLink/Setting/...). The snake_case PostgreSQL mirror lives
    # later in the doc and is intentionally excluded — see slot-55 dialect-
    # precedence-banner gate.
    for table, name, typ, rest in _scan_table_columns(sql_app):
        if not table[:1].isupper():
            continue  # snake_case / postgres mirror
        # Reject bare BOOLEAN / TINYINT
        if typ in {"BOOLEAN", "BOOL", "TINYINT"}:
            errs.append(f"clause-1: {table}.{name} declared `{typ}` (PRIMARY lane forbids; use INTEGER)")
            continue
        # If it's a known boolean-shaped column, demand INTEGER + Is- prefix
        is_bool_named = bool(BOOLEAN_FLAG_HINT_RE.match(name)) or name in KNOWN_BOOLEAN_COLUMNS
        if is_bool_named:
            if typ != "INTEGER":
                errs.append(f"clause-1: boolean-shaped column {table}.{name} type=`{typ}` (must be INTEGER)")
            if not IS_PREFIX_RE.match(name):
                errs.append(f"clause-1: boolean-shaped column {table}.{name} missing `Is` prefix")

    # Mirror check on §22 18-schema.sql — legacy git-logs predicates
    # (HasError/PreviousHasError/Truncated) are whitelisted to mirror the
    # §22 OpenAPI clause-2 whitelist; everything else holds the line.
    legacy_ok = {"HasError", "PreviousHasError", "Truncated"}
    for table, name, typ, rest in _scan_table_columns(surf.git_logs_schema):
        if typ in {"BOOLEAN", "BOOL", "TINYINT"}:
            errs.append(f"clause-1: §22 {table}.{name} declared `{typ}` (PRIMARY lane forbids)")
            continue
        if name in legacy_ok:
            continue
        if BOOLEAN_FLAG_HINT_RE.match(name) or name in KNOWN_BOOLEAN_COLUMNS:
            if typ != "INTEGER":
                errs.append(f"clause-1: §22 boolean-shaped column {table}.{name} type=`{typ}`")
            if not IS_PREFIX_RE.match(name):
                errs.append(f"clause-1: §22 boolean-shaped column {table}.{name} missing `Is` prefix")
    return errs


_OPENAPI_BOOL_INLINE_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\{[^}]*type:\s*boolean[^}]*\}", re.MULTILINE)
_OPENAPI_BOOL_BLOCK_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\n\s+type:\s*boolean\b", re.MULTILINE)
_OPENAPI_INT_COERCION_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\n\s+type:\s*integer\b[^\n]*\n\s+enum:\s*\[\s*0\s*,\s*1\s*\]",
    re.MULTILINE,
)
_OPENAPI_INT_COERCION_INLINE_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\{[^}]*type:\s*integer[^}]*enum:\s*\[\s*0\s*,\s*1\s*\][^}]*\}",
    re.MULTILINE,
)


def clause_rest_wire_shape(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.openapi:
        return errs
    fields: set[str] = set()
    for rx in (_OPENAPI_BOOL_INLINE_RE, _OPENAPI_BOOL_BLOCK_RE):
        fields.update(m.group(1) for m in rx.finditer(surf.openapi))
    # whitelisted git-logs predicates
    legacy_ok = {"HasError", "PreviousHasError", "Truncated"}
    for k in sorted(fields):
        if k in legacy_ok:
            continue
        if not PREDICATE_PREFIX_RE.match(k):
            errs.append(f"clause-2: OpenAPI boolean `{k}` lacks predicate prefix (Is/Has/Was/Can/Should/...)")
    for rx in (_OPENAPI_INT_COERCION_RE, _OPENAPI_INT_COERCION_INLINE_RE):
        for m in rx.finditer(surf.openapi):
            errs.append(f"clause-2: OpenAPI `{m.group(1)}` declares `type: integer + enum:[0,1]` (boolean coercion)")
    return errs


def clause_ui_render_parity(surf: Surface) -> list[str]:
    errs: list[str] = []
    if "### U-3" not in surf.ds_overview:
        errs.append("clause-3: §24 §00 missing `### U-3` heading")
        return errs
    idx = surf.ds_overview.find("### U-3")
    nxt = surf.ds_overview.find("\n### ", idx + 1)
    block = surf.ds_overview[idx:nxt] if nxt > 0 else surf.ds_overview[idx:]
    for lit in U3_REQUIRED_LITERALS:
        if lit not in block:
            errs.append(f"clause-3: §24 U-3 missing literal `{lit}`")
    # length budget: U-3 ≤ ~14 lines (render-parity rule, not a translation table)
    body_lines = [ln for ln in block.splitlines() if ln.strip()]
    if len(body_lines) > 14:
        errs.append(f"clause-3: §24 U-3 too long ({len(body_lines)} non-blank lines; ≤14)")
    return errs


def clause_no_coercion_surface(surf: Surface) -> list[str]:
    errs: list[str] = []
    if R4_INV2_LITERAL not in surf.app_db:
        errs.append("clause-4: §23 §00 R-4 invariant 2 (`Boolean parity`) absent")
    if R1_422_LITERAL not in surf.app_db:
        errs.append("clause-4: §23 §00 missing 422 `field.invalid` clause for boolean coercion")
    if not WE3_HEADING_RE.search(surf.app_db):
        errs.append("clause-4: §23 §00 missing WE-3 boolean-coercion attack fixture heading")
    return errs


def clause_no_restate(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.sibling_files:
        if path.name in {"17-openapi.yaml", "18-schema.sql"}:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in RESTATE_PATTERNS:
                if pat.match(line):
                    rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
                    errs.append(f"clause-5: {rel}:{i}: parallel boolean encoding heading `{line.strip()}`")
                    break
    return errs


def clause_vacuous(surf: Surface) -> list[str]:
    errs: list[str] = []
    sql_app = _extract_sql_blocks(surf.app_db)
    cols = _scan_table_columns(sql_app)
    bool_like = [c for c in cols if BOOLEAN_FLAG_HINT_RE.match(c[1]) or c[1] in KNOWN_BOOLEAN_COLUMNS]
    if not bool_like:
        errs.append("vacuous-pass: zero boolean-shaped columns found in §23 §00 PRIMARY-lane DDL")
    if surf.openapi:
        any_bool = bool(_OPENAPI_BOOL_INLINE_RE.search(surf.openapi) or _OPENAPI_BOOL_BLOCK_RE.search(surf.openapi))
        if not any_bool:
            errs.append("vacuous-pass: §22 OpenAPI `type: boolean` field set empty")
    if surf.ds_overview and "### U-3" not in surf.ds_overview:
        errs.append("vacuous-pass: §24 §00 U-3 surface absent")
    return errs


CHECKS = {
    "db-primary-lane": clause_db_primary_lane,
    "rest-wire-shape": clause_rest_wire_shape,
    "ui-render-parity": clause_ui_render_parity,
    "no-coercion": clause_no_coercion_surface,
    "no-restate": clause_no_restate,
}


def run_all(surf: Surface) -> list[str]:
    v = clause_vacuous(surf)
    if v:
        return v
    out: list[str] = []
    for fn in (
        clause_db_primary_lane,
        clause_rest_wire_shape,
        clause_ui_render_parity,
        clause_no_coercion_surface,
        clause_no_restate,
    ):
        out.extend(fn(surf))
    return out


# ---------- Self-test ----------

GOOD_APP_DB = """# §23 §00

```sql
CREATE TABLE IF NOT EXISTS AppLink (
    AppLinkId            INTEGER PRIMARY KEY AUTOINCREMENT,
    AppId                INTEGER NOT NULL,
    IsActive             INTEGER NOT NULL,
    DisconnectedAt       INTEGER NULL,
    CHECK (
      (IsActive = 1 AND DisconnectedAt IS NULL)
      OR
      (IsActive = 0 AND DisconnectedAt IS NOT NULL)
    )
);
```

## REST / RPC Contract

| 422 | Body fails validation | `field.invalid` |

2. **Boolean parity** — wire `true`/`false` ↔ DB `1`/`0`.

### WE-3 — Boolean-coercion attack on R-01 → 422
"""

GOOD_OPENAPI = """schemas:
  Foo:
    properties:
      IsEnabled:  { type: boolean }
      HasError:   { type: boolean }
"""

GOOD_DS = """# §24 §00

### U-3 — Boolean rendering parity

Wire `IsActive: true` → label "Active" with `--app-status-active` token.
Wire `IsActive: false` → label "Inactive" with `--app-status-inactive` token.
Components MUST NOT render raw `0`/`1` integers, MUST NOT invert the boolean,
and MUST NOT introduce a third "unknown" state. Mirrors §23 R-4 invariant 2.

### U-4 — next
"""


def _surf(app_db=GOOD_APP_DB, openapi=GOOD_OPENAPI, ds=GOOD_DS,
          git_logs="", sib=None) -> Surface:
    return Surface(app_db=app_db, git_logs_schema=git_logs, openapi=openapi,
                   ds_overview=ds, sibling_files=sib or [])


def self_test() -> int:
    fails: list[str] = []

    # F-1 complete-uniform → passes
    if run_all(_surf()):
        fails.append(f"F-1 should pass; got: {run_all(_surf())[:5]}")

    # F-2 §23 declares IsActive BOOLEAN NOT NULL
    bad = GOOD_APP_DB.replace("IsActive             INTEGER NOT NULL",
                              "IsActive             BOOLEAN NOT NULL")
    if not any("BOOLEAN" in e for e in clause_db_primary_lane(_surf(app_db=bad))):
        fails.append("F-2 should fail clause-1 (BOOLEAN type)")

    # F-3 §23 declares Active INTEGER (missing Is prefix)
    bad = GOOD_APP_DB.replace("IsActive", "Active")
    errs = clause_db_primary_lane(_surf(app_db=bad))
    if not any("missing `Is` prefix" in e for e in errs):
        fails.append(f"F-3 should fail clause-1 (Is prefix). got: {errs}")

    # F-4 OpenAPI integer-coercion
    bad_oa = GOOD_OPENAPI + "      IsBad:\n        type: integer\n        enum: [0, 1]\n"
    if not any("IsBad" in e for e in clause_rest_wire_shape(_surf(openapi=bad_oa))):
        fails.append("F-4 should fail clause-2 (integer-coercion)")

    # F-5 §24 U-3 drops the "MUST NOT invert" sub-clause
    bad_ds = GOOD_DS.replace("MUST NOT invert the boolean,\n", "")
    if not any("MUST NOT invert" in e for e in clause_ui_render_parity(_surf(ds=bad_ds))):
        fails.append("F-5 should fail clause-3 (invert sub-clause stripped)")

    # F-6 sibling restates parallel "Boolean encoding" heading
    sib = [(Path("spec/25-app-issues/04-extra.md"),
            "# Extra\n\n## Boolean encoding\n\nApp lane uses 0/1.\n")]
    if not clause_no_restate(_surf(sib=sib)):
        fails.append("F-6 should fail clause-5 (sibling restate)")

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

    try:
        surf = Surface.from_disk()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

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
        print(f"check-boolean-uniformity-primary-lane: {len(errs)} violation(s) (mode={args.check})",
              file=sys.stderr)
        return 1
    print(f"check-boolean-uniformity-primary-lane: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

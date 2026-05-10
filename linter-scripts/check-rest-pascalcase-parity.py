#!/usr/bin/env python3
r"""Gate #34 — check-rest-pascalcase-parity.

Mechanises §23 §00 `## REST / RPC Contract` R-1/R-2/R-4 + §23 §97
AC-ADB-REST-01. Six clauses (slot-56 contract):

  1. PascalCase shape on every wire key (R-2 jsonc fences).
  2. Wire ↔ DDL bijection for App / AppLink (modulo whitelists).
  3. Boolean key `Is`-prefix discipline.
  4. R-4 invariant 1 literal preservation (incl. self-citation).
  5. AC-ADB-REST-01 surface presence + status tag.
  6. No-restate of `## REST / RPC Contract` in §22/§24/§25.
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
APP_DB_AC = SPEC_ROOT / "23-app-database" / "97-acceptance-criteria.md"

REST_HEADING = "## REST / RPC Contract"
INLINED_HEADING = "## Inlined Contracts"

# Top-level wrapper keys (transport envelope, not data fields)
WRAPPER_WHITELIST = {"Error", "items"}
# Request-only fields that have no DDL backing column
REQUEST_ONLY_WHITELIST = {"RepoUrl", "ResolutionState"}
# Error-envelope keys (R-3) — not part of R-2 wire/DDL bijection
ERROR_ENVELOPE_KEYS = {"Code", "Message", "Field", "TraceId"}

PASCAL_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
JSON_KEY_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:')
DDL_COLUMN_RE = re.compile(r"^\s*([A-Z][A-Za-z0-9]*)\s+(INTEGER|TEXT|REAL|BLOB|NUMERIC)", re.MULTILINE)
JSON_BOOL_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:\s*(true|false)\b')

R4_LITERALS = (
    "PascalCase parity",
    "1:1",
    "No camelCase",
    "no snake_case on the wire",
    "Self-enforcing via §27 backlog gate `rest-pascalcase-parity-check`",
)

AC_REST_01_HEADINGS = (
    "### AC-ADB-REST-01 — REST/RPC contract present and parity-pinned",
)
AC_REST_01_BODY_LITERALS = (
    "8-row R-1 endpoint matrix",
    "R-4 invariants 1",  # accept "1–7" or "1, 2"
)
STATUS_TAG_RE = re.compile(r"\[(active|deferred|archived)\]")

NO_RESTATE_FOLDERS = (
    "22-git-logs-v2",
    "24-app-design-system-and-ui",
    "25-app-issues",
)


# ---------- Surface ----------

@dataclass
class Surface:
    overview: str = ""
    overview_path: Path = APP_DB
    ac: str = ""
    rest_section: str = ""
    app_ddl: str = ""
    applink_ddl: str = ""
    sibling_files: list[tuple[Path, str]] = field(default_factory=list)
    rest_section_found: bool = False

    @classmethod
    def from_disk(cls) -> "Surface":
        overview = APP_DB.read_text(encoding="utf-8")
        ac = APP_DB_AC.read_text(encoding="utf-8") if APP_DB_AC.exists() else ""
        sib: list[tuple[Path, str]] = []
        for sub in NO_RESTATE_FOLDERS:
            base = SPEC_ROOT / sub
            if not base.exists():
                continue
            for p in sorted(base.rglob("*.md")):
                # exempt §22 OpenAPI surface (owns git-logs REST, not App REST)
                if p.name == "17-openapi.yaml":
                    continue
                sib.append((p, p.read_text(encoding="utf-8")))
        return cls.build(overview, ac, sib)

    @classmethod
    def build(cls, overview: str, ac: str, sib: list[tuple[Path, str]]) -> "Surface":
        rest = _slice_section(overview, REST_HEADING)
        app_ddl = _slice_named_ddl(overview, "App")
        applink_ddl = _slice_named_ddl(overview, "AppLink")
        return cls(
            overview=overview,
            ac=ac,
            rest_section=rest,
            app_ddl=app_ddl,
            applink_ddl=applink_ddl,
            sibling_files=sib,
            rest_section_found=bool(rest),
        )


def _slice_section(text: str, heading: str) -> str:
    """Return text from `heading` up to the next top-level `## ` heading."""
    lines = text.splitlines()
    out: list[str] = []
    in_sec = False
    for line in lines:
        if line.startswith(heading):
            in_sec = True
            out.append(line)
            continue
        if in_sec:
            if line.startswith("## ") and not line.startswith(heading):
                break
            out.append(line)
    return "\n".join(out)


def _slice_named_ddl(text: str, table: str) -> str:
    """Extract the first ```sql ... CREATE TABLE [IF NOT EXISTS] {table} (...) ``` block."""
    pat = re.compile(
        r"```sql\s*\n(.*?CREATE TABLE(?:\s+IF NOT EXISTS)?\s+" + re.escape(table)
        + r"\s*\(.*?)\n```",
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        return ""
    block = m.group(1)
    # narrow to the App / AppLink CREATE TABLE statement only (stop at next CREATE)
    ct_pat = re.compile(
        r"CREATE TABLE(?:\s+IF NOT EXISTS)?\s+" + re.escape(table)
        + r"\s*\((.*?)\n\);", re.DOTALL,
    )
    m2 = ct_pat.search(block)
    return m2.group(1) if m2 else ""


def _extract_jsonc_fences(section: str) -> list[str]:
    return re.findall(r"```jsonc?\s*\n(.*?)\n```", section, re.DOTALL)


def _wire_keys_for(table: str, section: str) -> set[str]:
    """Extract JSON keys appearing inside a fence whose comment names {table} (response)."""
    keys: set[str] = set()
    for fence in _extract_jsonc_fences(section):
        # Only consider response shapes for the table
        head = fence.splitlines()[0] if fence.splitlines() else ""
        if f"// {table} (response)" not in head and not head.startswith(f"// {table}\n"):
            # Be permissive: also accept any fence whose first comment line mentions "{table} (response)"
            if f"{table} (response)" not in head:
                continue
        for k in JSON_KEY_RE.findall(fence):
            keys.add(k)
    return keys


def _ddl_columns(ddl_block: str) -> set[str]:
    cols: set[str] = set()
    for m in DDL_COLUMN_RE.finditer(ddl_block):
        cols.add(m.group(1))
    return cols


# ---------- Clauses ----------

def clause_pascalcase_shape(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section:
        return errs
    for fence in _extract_jsonc_fences(surf.rest_section):
        for k in JSON_KEY_RE.findall(fence):
            if k in WRAPPER_WHITELIST:
                continue
            if not PASCAL_RE.match(k):
                errs.append(f"clause-1: non-PascalCase wire key `{k}` in REST fence")
    return errs


def clause_wire_ddl_bijection(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section:
        return errs
    app_wire = _wire_keys_for("App", surf.rest_section)
    link_wire = _wire_keys_for("AppLink", surf.rest_section)
    app_cols = _ddl_columns(surf.app_ddl)
    link_cols = _ddl_columns(surf.applink_ddl)
    # Strip wrapper + error-envelope + request-only keys
    wire = (app_wire | link_wire) - WRAPPER_WHITELIST - ERROR_ENVELOPE_KEYS - REQUEST_ONLY_WHITELIST
    ddl = app_cols | link_cols
    wire_only = wire - ddl
    ddl_only = ddl - wire
    for k in sorted(wire_only):
        errs.append(f"clause-2: wire key `{k}` has no PRIMARY-lane DDL backing column")
    for k in sorted(ddl_only):
        errs.append(f"clause-2: DDL column `{k}` is not surfaced on the wire")
    return errs


def clause_boolean_is_prefix(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section:
        return errs
    for fence in _extract_jsonc_fences(surf.rest_section):
        for m in JSON_BOOL_RE.finditer(fence):
            key = m.group(1)
            if key in WRAPPER_WHITELIST:
                continue
            if not key.startswith("Is"):
                errs.append(
                    f"clause-3: boolean wire key `{key}` lacks `Is` prefix "
                    f"(value={m.group(2)})"
                )
    return errs


def clause_r4_literals(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section:
        return errs
    for lit in R4_LITERALS:
        if lit not in surf.rest_section:
            errs.append(f"clause-4: R-4 block missing literal `{lit}`")
    return errs


def clause_ac_rest_01(surf: Surface) -> list[str]:
    errs: list[str] = []
    # Accept the heading in EITHER §97 or §00 (per slot-56 contract line 454)
    haystacks = []
    if surf.ac:
        haystacks.append(("§97", surf.ac))
    if surf.overview:
        haystacks.append(("§00", surf.overview))
    found_heading = False
    found_body = False
    found_status = False
    for label, text in haystacks:
        if any(h in text for h in AC_REST_01_HEADINGS):
            found_heading = True
            # find body window — next 1500 chars after heading
            for h in AC_REST_01_HEADINGS:
                idx = text.find(h)
                if idx >= 0:
                    window = text[idx:idx + 2000]
                    if all(b in window for b in AC_REST_01_BODY_LITERALS):
                        found_body = True
                    if STATUS_TAG_RE.search(window):
                        found_status = True
    if not found_heading:
        errs.append("clause-5: AC-ADB-REST-01 heading missing from §23 §97 and §00")
    else:
        if not found_body:
            errs.append("clause-5: AC-ADB-REST-01 body missing literals "
                        "(`8-row R-1 endpoint matrix` AND `R-4 invariants 1…`)")
        if not found_status:
            errs.append("clause-5: AC-ADB-REST-01 missing `[active]`/`[deferred]`/`[archived]` status tag")
    return errs


def clause_no_restate(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.sibling_files:
        for line in text.splitlines():
            if line.startswith(REST_HEADING):
                errs.append(
                    f"clause-6: {path.relative_to(REPO_ROOT) if path.is_absolute() else path}: "
                    f"parallel `{REST_HEADING}` heading restates §23 §00 surface"
                )
                break
    return errs


def clause_vacuous(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section_found:
        errs.append("vacuous-pass: §23 §00 REST section absent")
        return errs
    fences = _extract_jsonc_fences(surf.rest_section)
    if not fences:
        errs.append("vacuous-pass: R-2 JSON fence absent")
    total_keys = sum(len(JSON_KEY_RE.findall(f)) for f in fences)
    if total_keys < 6:
        errs.append(f"vacuous-pass: wire-key set < 6 (got {total_keys})")
    if not surf.app_ddl and not surf.applink_ddl:
        errs.append("vacuous-pass: PRIMARY-lane DDL fence absent")
    if "### R-4" not in surf.rest_section and "R-4 — Contract invariants" not in surf.rest_section:
        errs.append("vacuous-pass: R-4 block absent")
    if surf.ac and not any(h in surf.ac for h in AC_REST_01_HEADINGS) \
       and not any(h in surf.overview for h in AC_REST_01_HEADINGS):
        errs.append("vacuous-pass: AC-ADB-REST-01 surface absent")
    return errs


CHECKS = {
    "pascalcase-shape": clause_pascalcase_shape,
    "wire-ddl-bijection": clause_wire_ddl_bijection,
    "boolean-is-prefix": clause_boolean_is_prefix,
    "r4-invariant-literals": clause_r4_literals,
    "ac-rest-01-surface": clause_ac_rest_01,
    "no-restate": clause_no_restate,
}


def run_all(surf: Surface) -> list[str]:
    out: list[str] = []
    v = clause_vacuous(surf)
    if v:
        return v
    for fn in (
        clause_pascalcase_shape,
        clause_wire_ddl_bijection,
        clause_boolean_is_prefix,
        clause_r4_literals,
        clause_ac_rest_01,
        clause_no_restate,
    ):
        out.extend(fn(surf))
    return out


# ---------- Self-test ----------

REST_SECTION_TEMPLATE = """## REST / RPC Contract (Normative — Phase-5 T-06)

### R-1 — Endpoint matrix
| ID | Method | Path | Returns |
|----|--------|------|---------|

### R-2 — Request / response schemas (JSON)

```jsonc
// App (response)
{APP_BODY}
```

```jsonc
// AppLink (response)
{LINK_BODY}
```

### R-4 — Contract invariants (binding)

1. **PascalCase parity** — every JSON key matches its PRIMARY-lane DDL column 1:1. No camelCase, no snake_case on the wire. Self-enforcing via §27 backlog gate `rest-pascalcase-parity-check`.

### AC-ADB-REST-01 — REST/RPC contract present and parity-pinned
The 8-row R-1 endpoint matrix and R-4 invariants 1–7 MUST be present. [active]
"""

DDL_TEMPLATE = """## Inlined Contracts

```sql
CREATE TABLE IF NOT EXISTS App (
    AppId        INTEGER PRIMARY KEY AUTOINCREMENT,
    Name         TEXT    NOT NULL,
    IsActive     INTEGER NOT NULL,
    CreatedAt    INTEGER NOT NULL,
    UpdatedAt    INTEGER NOT NULL
);
```

```sql
CREATE TABLE IF NOT EXISTS AppLink (
    AppLinkId      INTEGER PRIMARY KEY AUTOINCREMENT,
    AppId          INTEGER NOT NULL,
    IsActive       INTEGER NOT NULL,
    CreatedAt      INTEGER NOT NULL,
    DisconnectedAt INTEGER NULL
);
```
"""

GOOD_APP_BODY = (
    '{\n'
    '  "AppId": 1,\n'
    '  "Name": "demo",\n'
    '  "IsActive": true,\n'
    '  "CreatedAt": "2026-01-01T00:00:00Z",\n'
    '  "UpdatedAt": "2026-01-01T00:00:00Z"\n'
    '}'
)
GOOD_LINK_BODY = (
    '{\n'
    '  "AppLinkId": 1,\n'
    '  "AppId": 1,\n'
    '  "IsActive": true,\n'
    '  "CreatedAt": "2026-01-01T00:00:00Z",\n'
    '  "DisconnectedAt": null\n'
    '}'
)


def _mk_overview(app_body: str = GOOD_APP_BODY,
                 link_body: str = GOOD_LINK_BODY,
                 r4_block: str | None = None,
                 ddl: str = DDL_TEMPLATE) -> str:
    rest = REST_SECTION_TEMPLATE.replace("{APP_BODY}", app_body).replace("{LINK_BODY}", link_body)
    if r4_block is not None:
        rest = re.sub(r"### R-4.*?(?=### AC-ADB-REST-01)", r4_block + "\n\n", rest, count=1, flags=re.DOTALL)
    return f"# §23 §00\n\n{ddl}\n\n{rest}\n\n## Trailing section\n"


def self_test() -> int:
    fails: list[str] = []

    # F-1 complete-uniform → passes
    surf = Surface.build(_mk_overview(), "", [])
    errs = run_all(surf)
    if errs:
        fails.append(f"F-1 should pass; got: {errs[:5]}")

    # F-2 camelCase wire key → fails clause-1
    bad_app = GOOD_APP_BODY.replace('"AppId"', '"appId"')
    surf = Surface.build(_mk_overview(app_body=bad_app), "", [])
    if not clause_pascalcase_shape(surf):
        fails.append("F-2 should fail clause-1 (camelCase)")

    # F-3 wire-only key with no DDL → fails clause-2
    bad_link = GOOD_LINK_BODY.replace(
        '"DisconnectedAt": null',
        '"DisconnectedAt": null,\n  "LinkLabel": "x"',
    )
    surf = Surface.build(_mk_overview(link_body=bad_link), "", [])
    if not any("LinkLabel" in e for e in clause_wire_ddl_bijection(surf)):
        fails.append("F-3 should fail clause-2 (wire-only key)")

    # F-4 boolean on non-Is key → fails clause-3
    bad_app = GOOD_APP_BODY.replace('"IsActive": true', '"Active": true')
    surf = Surface.build(_mk_overview(app_body=bad_app), "", [])
    if not clause_boolean_is_prefix(surf):
        fails.append("F-4 should fail clause-3 (boolean non-Is)")

    # F-5 R-4 self-citation stripped → fails clause-4
    r4_stripped = (
        "### R-4 — Contract invariants (binding)\n\n"
        "1. **PascalCase parity** — every JSON key matches its PRIMARY-lane "
        "DDL column 1:1. No camelCase, no snake_case on the wire."
    )
    surf = Surface.build(_mk_overview(r4_block=r4_stripped), "", [])
    if not any("Self-enforcing" in e for e in clause_r4_literals(surf)):
        fails.append("F-5 should fail clause-4 (self-citation stripped)")

    # F-6 §24 child restates REST heading → fails clause-6
    sib = [(Path("spec/24-app-design-system-and-ui/04-rest-mirror.md"),
            "# Mirror\n\n## REST / RPC Contract\n\nrestated.\n")]
    surf = Surface.build(_mk_overview(), "", sib)
    if not clause_no_restate(surf):
        fails.append("F-6 should fail clause-6 (sibling restate)")

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
        print(f"check-rest-pascalcase-parity: {len(errs)} violation(s) (mode={args.check})",
              file=sys.stderr)
        return 1
    print(f"check-rest-pascalcase-parity: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

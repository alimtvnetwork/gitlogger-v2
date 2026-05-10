#!/usr/bin/env python3
"""Slot 42 / Gate #23 — check-error-envelope-uniformity.

Promotes AC-CAF-02 from contract-proven (paper-only) to load-proven by walking
the three error-envelope anchors (§22 OpenAPI schema, §23 R-3 cite + WE-*
JSON, §24 AC-ADS-15 row + <AppErrorState/> contract) and rejecting any
uniformity drift.

Five clauses (matched to on-disk reality, not the slot doc's pre-Sess-43
field set):

  clause-1 schema-pin: §22 17-openapi.yaml declares EXACTLY ONE top-level
           `ErrorEnvelope:` block under components.schemas.
  clause-2 db-mirror: §23 §00 carries the literal "### R-3 — Error envelope"
           heading; every WE-* response that emits a non-2xx HTTP status MUST
           carry an `Error` JSON object with `Code`, `Message`, AND `TraceId`
           keys. The R-3 reference jsonc block IS the canonical positive.
  clause-3 ui-mirror: §24 §00 has the AC-ADS-15 row binding ADS-* codes to
           §22 ErrorEnvelope, AND the `<AppErrorState/>` row in the
           component-state matrix cites BOTH `Error.Message` AND `TraceId`.
  clause-4 code-prefix: every Error.Code literal in the three folders matches
           its lane vocabulary — §22 OpenAPI ErrorCode enum entries match
           `^GL-[A-Z0-9-]+$`; §24 AC-ADS-15 row codes match
           `^ADS-[A-Z0-9-]+$`; §23 R-3 code enumeration uses dotted
           lowercase `^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)+$`. Cross-lane
           bleed (e.g. §23 inventing `DB-FOREIGN-XYZ`) is rejected.
  clause-5 no-restate: §23 / §24 markdown bodies MUST NOT inline a YAML
           block redefining `ErrorEnvelope:` field set; `Error` JSON
           illustrations (jsonc, http, json fences) are exempt.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot
(R5 vacuous-pass; no ErrorEnvelope schema found in §22 corpus).
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GIT_LOGS = REPO_ROOT / "spec" / "22-git-logs-v2"
APP_DB = REPO_ROOT / "spec" / "23-app-database"
APP_UI = REPO_ROOT / "spec" / "24-app-design-system-and-ui"

OPENAPI_PATH = GIT_LOGS / "17-openapi.yaml"
APP_DB_OVERVIEW = APP_DB / "00-overview.md"
APP_UI_OVERVIEW = APP_UI / "00-overview.md"

GL_CODE_RE = re.compile(r"^GL-[A-Z0-9-]+$")
ADS_CODE_RE = re.compile(r"^ADS-[A-Z0-9-]+$")
DB_CODE_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
SCHEMA_HEADER_RE = re.compile(r"^[ \t]+ErrorEnvelope:\s*$")


@dataclass
class Surface:
    openapi: str = ""
    db_overview: str = ""
    ui_overview: str = ""

    @classmethod
    def from_disk(cls) -> "Surface":
        return cls(
            openapi=_read(OPENAPI_PATH),
            db_overview=_read(APP_DB_OVERVIEW),
            ui_overview=_read(APP_UI_OVERVIEW),
        )

    @classmethod
    def from_strings(cls, *, openapi: str, db: str, ui: str) -> "Surface":
        return cls(openapi=openapi, db_overview=db, ui_overview=ui)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# ---------- Clauses ----------


def clause_schema_pin(s: Surface) -> list[str]:
    errs: list[str] = []
    if not s.openapi:
        return ["clause-1: §22 17-openapi.yaml absent"]
    matches = [i for i, ln in enumerate(s.openapi.splitlines())
               if SCHEMA_HEADER_RE.match(ln)]
    if len(matches) == 0:
        # R5 vacuous-pass — surface separately so caller can exit 3.
        errs.append("R5-vacuous-pass: zero ErrorEnvelope schema blocks "
                    "found in §22 17-openapi.yaml")
    elif len(matches) > 1:
        errs.append(f"clause-1: §22 17-openapi.yaml declares "
                    f"{len(matches)} ErrorEnvelope schema blocks "
                    f"(expected 1) at lines {[m+1 for m in matches]}")
    return errs


HTTP_RESP_RE = re.compile(r"```http\s*\nHTTP/1\.1\s+(\d{3})", re.MULTILINE)
WE_BLOCK_RE = re.compile(
    r"### WE-\d+[^\n]*\n.*?(?=\n### |\n## |\Z)", re.DOTALL)


def clause_db_mirror(s: Surface) -> list[str]:
    errs: list[str] = []
    if not s.db_overview:
        return ["clause-2: §23 §00 absent"]
    if "### R-3 — Error envelope" not in s.db_overview:
        errs.append("clause-2: §23 §00 missing literal "
                    "`### R-3 — Error envelope` heading")
    # Walk WE-* blocks
    for block in WE_BLOCK_RE.finditer(s.db_overview):
        body = block.group(0)
        title = body.splitlines()[0]
        # only fail if a non-2xx HTTP response is asserted
        statuses = HTTP_RESP_RE.findall(body)
        non2xx = [c for c in statuses if not c.startswith("2")]
        if not non2xx:
            continue
        if '"Error":' not in body and '"Error" :' not in body:
            errs.append(f"clause-2: §23 §00 {title.strip()} declares "
                        f"non-2xx response {non2xx} but body has no "
                        f"`\"Error\":` JSON envelope")
            continue
        for key in ('"Code"', '"Message"', '"TraceId"'):
            if key not in body:
                errs.append(f"clause-2: §23 §00 {title.strip()} "
                            f"non-2xx response missing required "
                            f"envelope key {key}")
    return errs


ADS_ROW_RE = re.compile(r"AC-ADS-15.*ErrorEnvelope.*ADS-[A-Z0-9-]+",
                        re.DOTALL)
APPERROR_ROW_RE = re.compile(
    r"\|\s*error\s*\|[^\n]*<AppErrorState/>[^\n]*\|[^\n]*\|[^\n]*\|")


def clause_ui_mirror(s: Surface) -> list[str]:
    errs: list[str] = []
    if not s.ui_overview:
        return ["clause-3: §24 §00 absent"]
    if not ADS_ROW_RE.search(s.ui_overview):
        errs.append("clause-3: §24 §00 missing AC-ADS-15 row binding "
                    "ADS-* codes to §22 ErrorEnvelope")
    m = APPERROR_ROW_RE.search(s.ui_overview)
    if not m:
        errs.append("clause-3: §24 §00 missing `<AppErrorState/>` row "
                    "in component-state matrix")
    else:
        row = m.group(0)
        if "Error.Message" not in row:
            errs.append("clause-3: §24 §00 `<AppErrorState/>` row "
                        "missing `Error.Message` requirement")
        if "TraceId" not in row and "RequestId" not in row:
            errs.append("clause-3: §24 §00 `<AppErrorState/>` row "
                        "missing `TraceId` (or `RequestId`) requirement")
    return errs


# §22 OpenAPI ErrorCode enum walk: collect lines matching `        - GL-...`
ENUM_ENTRY_RE = re.compile(r"^[ \t]+-\s+([A-Z][A-Z0-9-]+)\s*$")
JSON_CODE_RE = re.compile(r'"Code"\s*:\s*"([^"]+)"')
ADS_LITERAL_RE = re.compile(r"`(ADS-[A-Z0-9-]+)`")


def _enum_codes(openapi: str) -> list[tuple[int, str]]:
    out = []
    in_enum = False
    for i, ln in enumerate(openapi.splitlines()):
        if "ErrorCode:" in ln:
            in_enum = True
            continue
        if in_enum:
            m = ENUM_ENTRY_RE.match(ln)
            if m:
                out.append((i + 1, m.group(1)))
            elif ln.strip() and not ln.startswith(" "):
                in_enum = False
            elif re.match(r"^[ \t]+[A-Za-z][A-Za-z0-9]*:\s*$", ln):
                in_enum = False
    return out


def clause_code_prefix(s: Surface) -> list[str]:
    errs: list[str] = []
    # §22 ErrorCode enum entries MUST be GL-*
    for lineno, code in _enum_codes(s.openapi):
        if not GL_CODE_RE.match(code):
            errs.append(f"clause-4: §22 17-openapi.yaml:{lineno} "
                        f"ErrorCode enum entry `{code}` violates "
                        f"`^GL-[A-Z0-9-]+$`")
    # §24 ADS-15 row codes MUST be ADS-*
    for code in ADS_LITERAL_RE.findall(s.ui_overview):
        if not ADS_CODE_RE.match(code):
            errs.append(f"clause-4: §24 §00 ADS literal `{code}` "
                        f"violates `^ADS-[A-Z0-9-]+$`")
    # §23 R-3 + WE-* code literals MUST be dotted lowercase
    for m in JSON_CODE_RE.finditer(s.db_overview):
        code = m.group(1)
        if not DB_CODE_RE.match(code):
            errs.append(f"clause-4: §23 §00 JSON `Code` literal "
                        f"`{code}` violates dotted lowercase shape "
                        f"`^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$`")
    # Also walk inline backtick tokens for foreign envelope-code prefixes.
    for tbl_match in re.finditer(r"`([A-Za-z][A-Za-z0-9_.\-]*)`",
                                 s.db_overview):
        token = tbl_match.group(1)
        if token.startswith(("DB-", "GL-", "ADS-", "CAF-")):
            errs.append(f"clause-4: §23 §00 inline-code `{token}` uses "
                        f"foreign envelope-code prefix (DB/GL/ADS/CAF)")
    return errs


RESTATE_RE = re.compile(
    r"```ya?ml\s*\n(?:[^`]*\n)*?\s*ErrorEnvelope:\s*\n",
    re.MULTILINE)


def clause_no_restate(s: Surface) -> list[str]:
    errs: list[str] = []
    for label, text in (("§23", s.db_overview), ("§24", s.ui_overview)):
        if RESTATE_RE.search(text):
            errs.append(f"clause-5: {label} §00 inlines a YAML "
                        f"`ErrorEnvelope:` block restating §22 "
                        f"17-openapi.yaml schema (Lesson #36 violation)")
    return errs


CLAUSES = {
    "schema-pin": clause_schema_pin,
    "db-mirror": clause_db_mirror,
    "ui-mirror": clause_ui_mirror,
    "code-prefix": clause_code_prefix,
    "no-restate": clause_no_restate,
}


def run_check(s: Surface, which: str) -> tuple[list[str], bool]:
    """Return (errors, vacuous_flag)."""
    if which == "all":
        out: list[str] = []
        vacuous = False
        for name, fn in CLAUSES.items():
            es = fn(s)
            for e in es:
                if e.startswith("R5-vacuous-pass"):
                    vacuous = True
                else:
                    out.append(e)
        return out, vacuous
    fn = CLAUSES[which]
    es = fn(s)
    out = [e for e in es if not e.startswith("R5-vacuous-pass")]
    vacuous = any(e.startswith("R5-vacuous-pass") for e in es)
    return out, vacuous


# ---------- Self-test ----------

F1_OPENAPI = """\
components:
  schemas:
    ErrorCode:
      type: string
      enum:
        - GL-NOT-FOUND
        - GL-INVALID-INPUT
    ErrorEnvelope:
      type: object
      required: [Status, Code, Message, RequestId, HttpStatus]
      properties:
        Status:    { type: string, enum: [Error] }
        Code:      { $ref: '#/components/schemas/ErrorCode' }
        Message:   { type: string }
        RequestId: { type: string }
        HttpStatus: { type: integer }
"""

F1_DB = """\
### R-3 — Error envelope (uniform across all 8 endpoints)

```jsonc
{
  "Error": {
    "Code": "applink.unresolved",
    "Message": "x",
    "TraceId": "01HXYZ"
  }
}
```

### WE-1 — Resolve unknown RepoUrl → 404 `applink.unresolved`

**Expected response:**
```http
HTTP/1.1 404 Not Found

{
  "Error": {
    "Code": "applink.unresolved",
    "Message": "x",
    "TraceId": "01HXYZ"
  }
}
```
"""

F1_UI = """\
| **AC-ADS-15** | critical | §22 inheritance — ErrorEnvelope shape; codes ADS-TOKEN-LOADER-FAIL, ADS-SHELL-GEOMETRY-DRIFT | §97 |

| error    | `<AppErrorState/>`   | non-2xx response with R-3 envelope      | `Error.Message` + `TraceId` + Retry   |
"""


def _tmp_surface(openapi: str, db: str, ui: str) -> Surface:
    return Surface.from_strings(openapi=openapi, db=db, ui=ui)


def self_test() -> int:
    fails: list[str] = []

    # F-1: complete-uniform → passes
    s = _tmp_surface(F1_OPENAPI, F1_DB, F1_UI)
    errs, vac = run_check(s, "all")
    if errs or vac:
        fails.append(f"F-1 should pass; got vacuous={vac} errs={errs}")

    # F-2: §23 WE-1 missing RequestId-equivalent (here: TraceId) → fails clause-2
    db_f2 = F1_DB.replace('"TraceId": "01HXYZ"', '"X": "01HXYZ"')
    # Remove also the canonical R-3 jsonc TraceId so only WE-1 is the diff
    # but keep R-3 heading present
    s2 = _tmp_surface(F1_OPENAPI, db_f2, F1_UI)
    errs2, _ = run_check(s2, "db-mirror")
    if not any("TraceId" in e for e in errs2):
        fails.append(f"F-2 should fail clause-2 on missing TraceId; got {errs2}")

    # F-3: §24 AppErrorState row drops TraceId → fails clause-3
    ui_f3 = F1_UI.replace("`Error.Message` + `TraceId` + Retry",
                          "`Error.Message` + Retry")
    s3 = _tmp_surface(F1_OPENAPI, F1_DB, ui_f3)
    errs3, _ = run_check(s3, "ui-mirror")
    if not any("TraceId" in e for e in errs3):
        fails.append(f"F-3 should fail clause-3 on missing TraceId; got {errs3}")

    # F-4: §23 invents foreign-prefixed code → fails clause-4
    db_f4 = F1_DB + "\n`DB-FOREIGN-XYZ.bad`\n"
    s4 = _tmp_surface(F1_OPENAPI, db_f4, F1_UI)
    errs4, _ = run_check(s4, "code-prefix")
    if not any("DB-FOREIGN" in e for e in errs4):
        fails.append(f"F-4 should fail clause-4 on foreign prefix; got {errs4}")

    # F-5: §23 inlines YAML ErrorEnvelope: → fails clause-5
    db_f5 = F1_DB + "\n```yaml\nErrorEnvelope:\n  type: object\n```\n"
    s5 = _tmp_surface(F1_OPENAPI, db_f5, F1_UI)
    errs5, _ = run_check(s5, "no-restate")
    if not any("Lesson #36" in e for e in errs5):
        fails.append(f"F-5 should fail clause-5 on YAML restate; got {errs5}")

    # F-6: R5 vacuous-pass — zero schema blocks
    openapi_f6 = "components:\n  schemas:\n    Other:\n      type: object\n"
    s6 = _tmp_surface(openapi_f6, F1_DB, F1_UI)
    errs6, vac6 = run_check(s6, "schema-pin")
    if not vac6:
        fails.append(f"F-6 should flag vacuous-pass; got vac={vac6} errs={errs6}")

    if fails:
        print("--self-test FAILED:")
        for f in fails:
            print("  ✘", f)
        return 1
    print("--self-test: 6/6 fixtures passed "
          "(F-1 unique-passing + 5 failure variants)")
    return 0


# ---------- Main ----------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all",
                    choices=["all", *CLAUSES.keys()])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    s = Surface.from_disk()
    errs, vacuous = run_check(s, args.check)

    if vacuous:
        print(f"check-error-envelope-uniformity: vacuous-pass — empty walk "
              f"→ exit 3 fixture-rot (mode={args.check})")
        return 3

    if errs:
        for e in errs:
            print(f"  ✘ {e}")
        print(f"check-error-envelope-uniformity: {len(errs)} violation(s) "
              f"(mode={args.check})")
        return 1

    print(f"check-error-envelope-uniformity: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

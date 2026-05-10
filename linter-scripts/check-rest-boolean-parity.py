#!/usr/bin/env python3
r"""Gate #35 — check-rest-boolean-parity.

Mechanises §23 §00 R-2 + R-4 invariant 2 (wire boolean lane) +
§22 `17-openapi.yaml` (`type: boolean` field set) + §24 §00 U-3
(UI boolean render parity). Final REST-side §27 backlog ticket.

Six clauses (slot-57 contract):
  1. Wire boolean sample value discipline (`Is`-prefix only).
  2. R-4 invariant 2 literal preservation (incl. self-citation).
  3. OpenAPI ↔ wire bijection (`Is`-prefix or §22 whitelist).
  4. No integer-coercion attack surface.
  5. §24 U-3 surface presence.
  6. No-restate of App-surface boolean encoding in §22/§24/§25.
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
OPENAPI = SPEC_ROOT / "22-git-logs-v2" / "17-openapi.yaml"
DS_OVERVIEW = SPEC_ROOT / "24-app-design-system-and-ui" / "00-overview.md"

REST_HEADING = "## REST / RPC Contract"
IS_KEY_RE = re.compile(r"^Is[A-Z][A-Za-z0-9]*$")
JSON_KEY_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:')
JSON_BOOL_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:\s*(true|false)\b')
JSON_NONBOOL_VAL_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:\s*([^,\n}]+)')

# §22 git-logs OpenAPI whitelist — legacy git-logs surface, not App.
GIT_LOGS_BOOL_WHITELIST = {"HasError", "Truncated"}

R4_BOOL_LITERALS = (
    "wire `true`/`false` ↔ DB `1`/`0`",
    "Never accept `0`/`1` integers in request bodies",
    "reject with 422 `field.invalid`",
    "Self-enforcing via §27 backlog gate `rest-boolean-parity-check`",
)

U3_REQUIRED_LITERALS = ("boolean", "true", "false", "IsActive")
U3_BACKREF_LITERALS = ("AC-ADB-11", "AC-CAF-01", "§23 R-4 invariant 2")

NO_RESTATE_FOLDERS = (
    "22-git-logs-v2",
    "24-app-design-system-and-ui",
    "25-app-issues",
)
RESTATE_PATTERNS = (
    re.compile(r"^#{2,4}\s+.*[Bb]oolean.*[Ee]ncoding"),
    re.compile(r"^#{2,4}\s+.*[Bb]oolean.*[Pp]olicy"),
)


@dataclass
class Surface:
    overview: str = ""
    rest_section: str = ""
    openapi: str = ""
    ds_overview: str = ""
    sibling_files: list[tuple[Path, str]] = field(default_factory=list)

    @classmethod
    def from_disk(cls) -> "Surface":
        overview = APP_DB.read_text(encoding="utf-8")
        openapi = OPENAPI.read_text(encoding="utf-8") if OPENAPI.exists() else ""
        ds = DS_OVERVIEW.read_text(encoding="utf-8") if DS_OVERVIEW.exists() else ""
        sib: list[tuple[Path, str]] = []
        for sub in NO_RESTATE_FOLDERS:
            base = SPEC_ROOT / sub
            if not base.exists():
                continue
            for p in sorted(base.rglob("*.md")):
                # exempt §24 U-3 binding row in overview itself + §22 OpenAPI source
                if p == DS_OVERVIEW:
                    continue
                sib.append((p, p.read_text(encoding="utf-8")))
        return cls.build(overview, openapi, ds, sib)

    @classmethod
    def build(cls, overview: str, openapi: str, ds: str,
              sib: list[tuple[Path, str]]) -> "Surface":
        return cls(
            overview=overview,
            rest_section=_slice_section(overview, REST_HEADING),
            openapi=openapi,
            ds_overview=ds,
            sibling_files=sib,
        )


def _slice_section(text: str, heading: str) -> str:
    out, in_sec = [], False
    for line in text.splitlines():
        if line.startswith(heading):
            in_sec = True
            out.append(line)
            continue
        if in_sec:
            if line.startswith("## ") and not line.startswith(heading):
                break
            out.append(line)
    return "\n".join(out)


def _extract_jsonc_fences(section: str) -> list[str]:
    return re.findall(r"```jsonc?\s*\n(.*?)\n```", section, re.DOTALL)


def _r4_inv2_block(section: str) -> str:
    """Extract the R-4 invariant 2 line(s)."""
    m = re.search(r"\n2\.\s+\*\*Boolean parity\*\*[^\n]*\n", section)
    return m.group(0) if m else ""


# ---------- Clauses ----------

def clause_wire_sample_shape(surf: Surface) -> list[str]:
    errs: list[str] = []
    for fence in _extract_jsonc_fences(surf.rest_section):
        # boolean values on non-Is keys
        for m in JSON_BOOL_RE.finditer(fence):
            k = m.group(1)
            if k in {"Error", "items"}:
                continue
            if not IS_KEY_RE.match(k):
                errs.append(f"clause-1: boolean sample on non-`Is`-prefixed key `{k}` (={m.group(2)})")
        # Is-prefixed keys with non-boolean sample values
        for m in JSON_NONBOOL_VAL_RE.finditer(fence):
            k, v = m.group(1), m.group(2).strip().rstrip(",").strip()
            if not IS_KEY_RE.match(k):
                continue
            # accept only literal true/false (with optional inline-comment)
            if not re.match(r"^(true|false)\b", v):
                errs.append(f"clause-1: `Is`-prefixed key `{k}` carries non-boolean sample `{v[:40]}`")
    return errs


def clause_r4_literals(surf: Surface) -> list[str]:
    errs: list[str] = []
    block = _r4_inv2_block(surf.rest_section)
    if not block:
        errs.append("clause-2: R-4 invariant 2 line not located")
        return errs
    for lit in R4_BOOL_LITERALS:
        if lit not in block:
            errs.append(f"clause-2: R-4 invariant 2 missing literal `{lit}`")
    return errs


_OPENAPI_BOOL_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\{[^}]*type:\s*boolean[^}]*\}", re.MULTILINE)
_OPENAPI_BOOL_BLOCK_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\n\s+type:\s*boolean\b", re.MULTILINE)


def _openapi_bool_fields(text: str) -> set[str]:
    out: set[str] = set()
    for m in _OPENAPI_BOOL_RE.finditer(text):
        out.add(m.group(1))
    for m in _OPENAPI_BOOL_BLOCK_RE.finditer(text):
        out.add(m.group(1))
    return out


def clause_openapi_bijection(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.openapi:
        return errs
    for k in sorted(_openapi_bool_fields(surf.openapi)):
        if IS_KEY_RE.match(k):
            continue
        if k in GIT_LOGS_BOOL_WHITELIST:
            continue
        errs.append(
            f"clause-3: OpenAPI `type: boolean` field `{k}` lacks `Is` prefix "
            f"and is not in §22 git-logs whitelist {sorted(GIT_LOGS_BOOL_WHITELIST)}"
        )
    return errs


_INT_COERCION_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\n\s+type:\s*integer\b[^\n]*\n\s+enum:\s*\[\s*0\s*,\s*1\s*\]",
    re.MULTILINE,
)
_INT_COERCION_INLINE_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\{[^}]*type:\s*integer[^}]*enum:\s*\[\s*0\s*,\s*1\s*\][^}]*\}",
    re.MULTILINE,
)
_R2_BOOL_INTSAMPLE_RE = re.compile(r'"(Is[A-Z][A-Za-z0-9]*)"\s*:\s*([01])\b')


def clause_no_integer_coercion(surf: Surface) -> list[str]:
    errs: list[str] = []
    for fence in _extract_jsonc_fences(surf.rest_section):
        for m in _R2_BOOL_INTSAMPLE_RE.finditer(fence):
            errs.append(f"clause-4: R-2 fence ships boolean key `{m.group(1)}` with integer sample `{m.group(2)}`")
    if surf.openapi:
        for m in _INT_COERCION_RE.finditer(surf.openapi):
            errs.append(f"clause-4: OpenAPI field `{m.group(1)}` declares `type: integer + enum: [0,1]` (boolean-coercion)")
        for m in _INT_COERCION_INLINE_RE.finditer(surf.openapi):
            errs.append(f"clause-4: OpenAPI inline field `{m.group(1)}` declares `type: integer + enum: [0,1]` (boolean-coercion)")
    return errs


def clause_u3_surface(surf: Surface) -> list[str]:
    errs: list[str] = []
    if "### U-3" not in surf.ds_overview:
        errs.append("clause-5: §24 §00 missing `### U-3` heading")
        return errs
    # locate U-3 block: from `### U-3` to next `### `
    idx = surf.ds_overview.find("### U-3")
    nxt = surf.ds_overview.find("\n### ", idx + 1)
    block = surf.ds_overview[idx:nxt] if nxt > 0 else surf.ds_overview[idx:]
    for lit in U3_REQUIRED_LITERALS:
        if lit not in block:
            errs.append(f"clause-5: §24 U-3 block missing literal `{lit}`")
    if not any(b in block for b in U3_BACKREF_LITERALS):
        errs.append(
            f"clause-5: §24 U-3 block missing back-reference (one of {list(U3_BACKREF_LITERALS)})"
        )
    return errs


def clause_no_restate(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.sibling_files:
        # exempt §22 OpenAPI source itself (it IS the git-logs surface)
        if path.name == "17-openapi.yaml":
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in RESTATE_PATTERNS:
                if pat.match(line):
                    errs.append(
                        f"clause-6: {path.relative_to(REPO_ROOT) if path.is_absolute() else path}"
                        f":{i}: parallel App-surface boolean encoding heading `{line.strip()}`"
                    )
                    break
    return errs


def clause_vacuous(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not surf.rest_section:
        errs.append("vacuous-pass: §23 §00 REST section absent")
        return errs
    fences = _extract_jsonc_fences(surf.rest_section)
    if not fences:
        errs.append("vacuous-pass: R-2 JSON fence absent")
    bool_count = sum(len(JSON_BOOL_RE.findall(f)) for f in fences)
    if bool_count < 1:
        errs.append("vacuous-pass: zero boolean sample values observed in R-2 fences")
    if not _r4_inv2_block(surf.rest_section):
        errs.append("vacuous-pass: R-4 invariant 2 absent")
    if surf.openapi and not _openapi_bool_fields(surf.openapi):
        errs.append("vacuous-pass: OpenAPI `type: boolean` field set empty")
    if surf.ds_overview and "### U-3" not in surf.ds_overview:
        errs.append("vacuous-pass: §24 §00 U-3 surface absent")
    return errs


CHECKS = {
    "wire-sample-shape": clause_wire_sample_shape,
    "r4-invariant-literals": clause_r4_literals,
    "openapi-bijection": clause_openapi_bijection,
    "no-integer-coercion": clause_no_integer_coercion,
    "u3-surface-presence": clause_u3_surface,
    "no-restate": clause_no_restate,
}


def run_all(surf: Surface) -> list[str]:
    v = clause_vacuous(surf)
    if v:
        return v
    out: list[str] = []
    for fn in (
        clause_wire_sample_shape,
        clause_r4_literals,
        clause_openapi_bijection,
        clause_no_integer_coercion,
        clause_u3_surface,
        clause_no_restate,
    ):
        out.extend(fn(surf))
    return out


# ---------- Self-test ----------

GOOD_R2 = """```jsonc
// App (response)
{
  "AppId": 1,
  "IsActive": true,
  "CreatedAt": "2026-01-01T00:00:00Z"
}
```"""

GOOD_R4 = (
    "\n2. **Boolean parity** — wire `true`/`false` ↔ DB `1`/`0`. "
    "Never accept `0`/`1` integers in request bodies; reject with 422 "
    "`field.invalid`. Self-enforcing via §27 backlog gate "
    "`rest-boolean-parity-check`.\n"
)

GOOD_OPENAPI = """schemas:
  Foo:
    properties:
      IsEnabled:  { type: boolean }
      HasError:   { type: boolean }
"""

GOOD_DS = """# §24 §00

### U-3 — Boolean rendering parity

Wire `IsActive: true` → label "Active". Wire `IsActive: false` → label "Inactive".
boolean values mirror §23 R-4 invariant 2.

### U-4 — next
"""


def _mk_overview(r2: str = GOOD_R2, r4: str = GOOD_R4) -> str:
    return (
        "# §23 §00\n\n"
        "## REST / RPC Contract\n\n"
        "### R-2 — schemas\n\n" + r2 + "\n\n"
        "### R-4 — invariants\n" + r4 + "\n"
        "## Trailing\n"
    )


def self_test() -> int:
    fails: list[str] = []

    # F-1 complete-uniform → passes
    surf = Surface.build(_mk_overview(), GOOD_OPENAPI, GOOD_DS, [])
    errs = run_all(surf)
    if errs:
        fails.append(f"F-1 should pass; got: {errs[:5]}")

    # F-2 boolean on non-Is key
    bad_r2 = GOOD_R2.replace('"IsActive": true', '"Active": true')
    surf = Surface.build(_mk_overview(r2=bad_r2), GOOD_OPENAPI, GOOD_DS, [])
    if not clause_wire_sample_shape(surf):
        fails.append("F-2 should fail clause-1 (boolean on non-Is)")

    # F-3 R-4 self-citation stripped
    bad_r4 = GOOD_R4.replace(" Self-enforcing via §27 backlog gate `rest-boolean-parity-check`.", "")
    surf = Surface.build(_mk_overview(r4=bad_r4), GOOD_OPENAPI, GOOD_DS, [])
    if not any("Self-enforcing" in e for e in clause_r4_literals(surf)):
        fails.append("F-3 should fail clause-2 (self-citation stripped)")

    # F-4 OpenAPI integer-coercion stand-in for boolean
    bad_oa = GOOD_OPENAPI + "      IsBad:\n        type: integer\n        enum: [0, 1]\n"
    surf = Surface.build(_mk_overview(), bad_oa, GOOD_DS, [])
    if not any("IsBad" in e for e in clause_no_integer_coercion(surf)):
        fails.append("F-4 should fail clause-4 (integer-coercion)")

    # F-5 §24 U-3 missing IsActive literal
    bad_ds = GOOD_DS.replace("IsActive", "Foo")
    surf = Surface.build(_mk_overview(), GOOD_OPENAPI, bad_ds, [])
    if not any("IsActive" in e for e in clause_u3_surface(surf)):
        fails.append("F-5 should fail clause-5 (U-3 missing IsActive)")

    # F-6 §25 child restates App-surface boolean encoding
    sib = [(Path("spec/25-app-issues/04-extra.md"),
            "# Extra\n\n## Boolean encoding\n\nApp lane uses 0/1.\n")]
    surf = Surface.build(_mk_overview(), GOOD_OPENAPI, GOOD_DS, sib)
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
        print(f"check-rest-boolean-parity: {len(errs)} violation(s) (mode={args.check})",
              file=sys.stderr)
        return 1
    print(f"check-rest-boolean-parity: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

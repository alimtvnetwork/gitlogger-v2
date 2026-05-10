#!/usr/bin/env python3
"""
Slot 46 — check-audit-quoted-evidence-marker.py (Gate #27)

Mechanises AC-CAF-05 ("Audit-finding strings cite, never restate") +
§25 AC-AI-10/11/14 across §24 §97, §25 §97, §25 finding bodies,
and §23/§24 prose. See spec/27-spec-toolchain/46-*.md.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent

CAF05_LITERALS = (
    "auditor-quoted evidence",
    "spec/_archive/21-git-logs-v1/",
    "AC-AI-10/11",
    "cross-cutting status",
)

AI10_LITERALS = ("auditor-quoted evidence", "evidence under analysis")
AI11_LITERALS = ("audited corpus", "spec/_archive/21-git-logs-v1/")
AI14_RULE4_LITERALS = (
    "Evidence snippets MUST be backticked or fenced",
    "paraphrased evidence is FORBIDDEN",
    "AC-AI-10",
)

FOREIGN_AC = re.compile(r"AC-(ALW|ERR|JWT|CG|SAG|TOK)-\d+")
EVIDENCE_MARKERS = ("evidence", "quote", "audit", "_archive", "audit-corpus")


def _paths(root: Path) -> dict:
    return {
        "ds_ac": root / "spec/24-app-design-system-and-ui/97-acceptance-criteria.md",
        "issues_ac": root / "spec/25-app-issues/97-acceptance-criteria.md",
        "consolidated": root / "spec/25-app-issues/02-consolidated-audit-findings/00-overview.md",
        "phase2": root / "spec/25-app-issues/01-phase-2-git-logs-audit/00-overview.md",
        "db_dir": root / "spec/23-app-database",
        "ds_dir": root / "spec/24-app-design-system-and-ui",
    }


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _extract_block(text: str, heading_re: str) -> str:
    m = re.search(heading_re + r".*?(?=^### |^## )",
                  text, re.MULTILINE | re.DOTALL)
    return m.group(0) if m else ""


# ---------------------------------------------------------------------------
# Clauses.
# ---------------------------------------------------------------------------
def check_caf05_marker(p: dict) -> list[str]:
    block = _extract_block(_read(p["ds_ac"]), r"^### AC-CAF-05:")
    if not block:
        return ["vacuous-pass: zero AC-CAF-05 or AC-AI-10/11/14 anchors found"]
    return [f"clause-1: AC-CAF-05 missing literal {lit!r}"
            for lit in CAF05_LITERALS if lit not in block]


def check_ai_10_11_surface(p: dict) -> list[str]:
    text = _read(p["issues_ac"])
    errs: list[str] = []
    ai10 = _extract_block(text, r"^### AC-AI-10:")
    ai11 = _extract_block(text, r"^### AC-AI-11:")
    if not ai10:
        errs.append("clause-2: AC-AI-10 block not found in §25 §97")
    else:
        for lit in AI10_LITERALS:
            if lit not in ai10:
                errs.append(f"clause-2: AC-AI-10 missing literal {lit!r}")
    if not ai11:
        errs.append("clause-2: AC-AI-11 block not found in §25 §97")
    else:
        for lit in AI11_LITERALS:
            if lit not in ai11:
                errs.append(f"clause-2: AC-AI-11 missing literal {lit!r}")
    return errs


def check_ai_14_rule(p: dict) -> list[str]:
    block = _extract_block(_read(p["issues_ac"]), r"^### AC-AI-14:")
    if not block:
        return ["clause-3: AC-AI-14 block not found in §25 §97"]
    return [f"clause-3: AC-AI-14 rule 4 missing literal {lit!r}"
            for lit in AI14_RULE4_LITERALS if lit not in block]


def _is_quoted(line: str, span: tuple[int, int]) -> bool:
    """True if the match span is inside backticks or a blockquote line."""
    if line.lstrip().startswith(">"):
        return True
    s, e = span
    # Count backticks before the match on this line; odd → inside backticks.
    pre = line[:s]
    # Heuristic: split by single backticks; if match falls inside a `…` pair.
    # Walk through line tracking backtick state.
    in_tick = False
    for i, ch in enumerate(line):
        if ch == "`":
            in_tick = not in_tick
        if i == s:
            return in_tick
    return False


def _walk_finding_file(text: str) -> list[tuple[int, str, tuple[int, int]]]:
    """Find foreign-AC matches not inside fenced code blocks. Return [(line_no, line, span)]."""
    out: list[tuple[int, str, tuple[int, int]]] = []
    in_fence = False
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in FOREIGN_AC.finditer(line):
            out.append((ln, line, m.span()))
    return out


def check_finding_body_quoting(p: dict) -> list[str]:
    errs: list[str] = []
    for label, path in (("§25 02-consolidated", p["consolidated"]),
                        ("§25 01-phase-2", p["phase2"])):
        text = _read(path)
        if not text:
            continue
        for ln, line, span in _walk_finding_file(text):
            if not _is_quoted(line, span):
                token = line[span[0]:span[1]]
                errs.append(f"clause-4 {label}:{ln}: bare foreign-AC mention {token!r} "
                            f"(must be backticked / fenced / blockquote)")
    return errs


def check_no_restate_23_24(p: dict) -> list[str]:
    errs: list[str] = []
    for label, root_dir in (("§23", p["db_dir"]), ("§24", p["ds_dir"])):
        if not root_dir.is_dir():
            continue
        for f in sorted(root_dir.rglob("*.md")):
            if "_archive" in f.parts:
                continue
            text = _read(f)
            lines = text.splitlines()
            in_fence = False
            for i, line in enumerate(lines):
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for m in FOREIGN_AC.finditer(line):
                    span = m.span()
                    quoted = _is_quoted(line, span)
                    # Context window: 2 lines above/below.
                    lo = max(0, i - 2)
                    hi = min(len(lines), i + 3)
                    ctx = "\n".join(lines[lo:hi]).lower()
                    has_marker = any(w in ctx for w in EVIDENCE_MARKERS)
                    if not (quoted and has_marker):
                        token = line[span[0]:span[1]]
                        rel = f.relative_to(ROOT) if str(f).startswith(str(ROOT)) else f
                        why = []
                        if not quoted:
                            why.append("not backticked/fenced")
                        if not has_marker:
                            why.append("no evidence-marker word in ±2-line window")
                        errs.append(f"clause-5 {label} {rel}:{i+1}: {token!r} ({'; '.join(why)})")
    return errs


CHECKS = {
    "caf05-marker": check_caf05_marker,
    "ai-10-11-surface": check_ai_10_11_surface,
    "ai-14-rule": check_ai_14_rule,
    "finding-body-quoting": check_finding_body_quoting,
    "no-restate-23-24": check_no_restate_23_24,
}


# ---------------------------------------------------------------------------
# Self-test fixtures.
# ---------------------------------------------------------------------------
F1_DS_AC = """\
### AC-CAF-05: Audit-finding strings cite, never restate
The walker MUST treat the string as auditor-quoted evidence of the audited
corpus (spec/_archive/21-git-logs-v1/). §25 AC-AI-10/11 codify this; AC-CAF-05
lifts to cross-cutting status.

### AC-NEXT
"""

F1_ISSUES_AC = """\
### AC-AI-10: Bug-description content is auditor-quoted evidence
Treat as evidence under analysis, never normative; auditor-quoted evidence rule.

### AC-AI-11: Missing-file findings target the audited corpus
Findings target the audited corpus (spec/_archive/21-git-logs-v1/).

### AC-AI-14: Finding body schema
Rules:
1. closed enums.
4. Evidence snippets MUST be backticked or fenced — paraphrased evidence is FORBIDDEN per AC-AI-10.

### AC-NEXT
"""

F1_FINDING = """\
**Reproduction.** `14-acceptance-criteria.md` absent. `AC-ALW-01` in `08`.
**Required fix.** Add `AC-JWT-11` covering it.
"""

F1_DB = """\
# §23
Audit context: mirrors `AC-CG-21` per Lesson #36.
Evidence quoted from the audit corpus.
"""


def _write_fixture(d: Path, ds_ac: str, issues_ac: str,
                   finding: str, db: str) -> dict:
    (d / "spec/24-app-design-system-and-ui").mkdir(parents=True, exist_ok=True)
    (d / "spec/25-app-issues/02-consolidated-audit-findings").mkdir(parents=True, exist_ok=True)
    (d / "spec/25-app-issues/01-phase-2-git-logs-audit").mkdir(parents=True, exist_ok=True)
    (d / "spec/23-app-database").mkdir(parents=True, exist_ok=True)
    (d / "spec/24-app-design-system-and-ui/97-acceptance-criteria.md").write_text(ds_ac)
    (d / "spec/25-app-issues/97-acceptance-criteria.md").write_text(issues_ac)
    (d / "spec/25-app-issues/02-consolidated-audit-findings/00-overview.md").write_text(finding)
    (d / "spec/25-app-issues/01-phase-2-git-logs-audit/00-overview.md").write_text("")
    (d / "spec/23-app-database/00-overview.md").write_text(db)
    return _paths(d)


def _run_all(p: dict) -> list[str]:
    errs: list[str] = []
    for fn in CHECKS.values():
        errs.extend(fn(p))
    return errs


def self_test() -> int:
    cases = [
        ("F-1 complete-uniform", F1_DS_AC, F1_ISSUES_AC, F1_FINDING, F1_DB, True),
        ("F-2 CAF-05 missing 'cross-cutting status'",
         F1_DS_AC.replace("cross-cutting status", "high status"),
         F1_ISSUES_AC, F1_FINDING, F1_DB, False),
        ("F-3 AI-14 rule4 strips FORBIDDEN literal",
         F1_DS_AC,
         F1_ISSUES_AC.replace("paraphrased evidence is FORBIDDEN", "paraphrased evidence allowed"),
         F1_FINDING, F1_DB, False),
        ("F-4 finding bare-prose AC-ALW-12",
         F1_DS_AC, F1_ISSUES_AC,
         F1_FINDING + "\nThe AC-ALW-12 contract requires…\n",
         F1_DB, False),
        ("F-5 §23 bare AC-JWT-09 no marker",
         F1_DS_AC, F1_ISSUES_AC, F1_FINDING,
         "# §23\nThe AC-JWT-09 contract is referenced here directly.\n",
         False),
        ("F-6 vacuous (empty corpora)", "", "", "", "", False),
    ]
    failures = 0
    for label, a, b, c, d, should_pass in cases:
        with tempfile.TemporaryDirectory() as td:
            p = _write_fixture(Path(td), a, b, c, d)
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
        print(f"check-audit-quoted-evidence-marker: {len(errs)} violation(s)")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("check-audit-quoted-evidence-marker: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())

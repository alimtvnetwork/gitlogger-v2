#!/usr/bin/env python3
"""
check-truncated-prose.py — Phase P47-followup-1 (Task #12)

Flags spec markdown files that appear to end mid-sentence or with an
unbalanced code fence. Mechanically prevents the truncation class of
AI-implementability blockers surfaced in the Phase P47 audit
(`/mnt/documents/audit-phase-p47.md`).

Detection rules (a file FAILS if):
  1. The number of ```-fences is odd (unclosed fenced block).
  2. The last non-blank, non-HTML-comment, non-structural line does not end
     with a sentence terminator (. ! ? : ; ) ] } > " ` * _).

A line is "structural" (always considered a clean ending) when it is:
  - a heading (#, ##, ...)
  - a horizontal rule (---)
  - a list item (-, *, 1.)
  - a table row (| ... |)
  - a blockquote (>)
  - a closing fence (```)
  - a link-only line ([text](url))

Scope: spec/**/*.md (skips _archive/).

Exit codes:
  0  clean
  1  one or more truncated files
  2  usage error
"""
from __future__ import annotations
import re, sys, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"

FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"^\s*<!--")
STRUCTURAL_RE = re.compile(r"^\s*(#{1,6}\s|---+\s*$|\*\s|-\s|\d+\.\s|\||>|\[.*\]\(.*\)\s*$|```)")
TERMINATOR_RE = re.compile(r"""[.!?:;)\]\}>"`*_]\s*$""")


def classify(path: pathlib.Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    raw_lines = text.splitlines()
    fences = sum(1 for l in raw_lines if FENCE_RE.match(l))
    if fences % 2 == 1:
        return False, f"unclosed code fence (odd fence count={fences})"
    # last meaningful line
    meaningful = [l.rstrip() for l in raw_lines if l.strip() and not COMMENT_RE.match(l)]
    if not meaningful:
        return True, "empty"
    last = meaningful[-1]
    if STRUCTURAL_RE.match(last):
        return True, "structural-ending"
    if TERMINATOR_RE.search(last):
        return True, "terminator-ending"
    return False, f"mid-sentence (last: {last[:80]!r})"


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect truncated spec prose.")
    ap.add_argument("--root", default=str(SPEC), help="spec root (default: spec/)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"ERROR: spec root not found: {root}", file=sys.stderr)
        return 2
    failures: list[tuple[pathlib.Path, str]] = []
    checked = 0
    for p in sorted(root.rglob("*.md")):
        if "_archive" in p.parts:
            continue
        checked += 1
        ok, why = classify(p)
        try:
            display = p.relative_to(ROOT)
        except ValueError:
            display = p
        if not ok:
            failures.append((p, why))
            if args.verbose:
                print(f"FAIL {display}  -- {why}", file=sys.stderr)
        elif args.verbose:
            print(f"OK   {display}  [{why}]")
    if failures:
        print(f"check-truncated-prose: {len(failures)} truncated file(s) of {checked} checked", file=sys.stderr)
        for p, why in failures:
            try:
                display = p.relative_to(ROOT)
            except ValueError:
                display = p
            print(f"  FAIL  {display}  -- {why}", file=sys.stderr)
        return 1
    print(f"check-truncated-prose: OK ({checked} files clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

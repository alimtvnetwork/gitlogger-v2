#!/usr/bin/env python3
"""
check-99-summary-freshness.py — flag stale §99 Summary narrative claims.

Phase H1 (2026-04-28): codifies the Phase 136/139 lesson — §99 ## Summary
sections accumulated stale narrative claims (counts, versions, status flags)
that diverged from §97/§00/source-of-truth. Manual sweeps caught them late
(Phase 136 over-counted 20 modules; Phase 139 found real count was 1).

This gate detects §99 modules whose ## Summary block carries a
`<!-- verified-phase: NNN -->` stamp older than --max-age phases.

Stamp format (recommended, opt-in per file):

    ## Summary
    <!-- verified-phase: 147 -->

    ...narrative claims...

If a §99 has NO stamp, this gate emits a per-file `info` line and does not fail
(advisory until project-wide stamp adoption is decided in a future phase / R1).
If a §99 has a stamp older than the current phase by more than --max-age, the
gate fails (strict mode) or warns (--report-only).

Current phase is read from `mem://index.md` via the `Phase NNN` token nearest
the top, falling back to the latest `Phase NNN` in `spec/27-spec-toolchain/98-changelog.md`.

CLI:
    python3 linter-scripts/check-99-summary-freshness.py [--report-only] [--max-age N]

Exit codes:
    0 = all stamped §99 files within budget (or --report-only)
    1 = at least one stamped §99 file is stale beyond --max-age (strict mode)
    2 = structural error (cannot determine current phase, etc.)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = REPO / "spec"
MEM_INDEX = REPO / ".lovable" / "memory" / "index.md"
CHANGELOG_27 = SPEC / "27-spec-toolchain" / "98-changelog.md"

PHASE_RE = re.compile(r"\bPhase\s+(\d{1,4})\b")
STAMP_RE = re.compile(r"<!--\s*verified-phase:\s*(\d{1,4})\s*-->")
# Phase H7 (2026-04-28): codifies the "audit-log-only §99" exemption.
# Some §99 files carry only date-stamped audit-log headings (no narrative
# Summary, no inventory rubric) and have no claims to verify. Files marking
# `<!-- freshness-exempt: <reason> -->` anywhere in the file are counted
# separately and excluded from the unstamped advisory tally.
EXEMPT_RE = re.compile(r"<!--\s*freshness-exempt:\s*([a-z0-9_\-]+)\s*-->")
# Phase H2 (2026-04-28): widened from `## Summary` only to also cover
# inventory-rubric blocks (the 43 §99 files that ship inventory tables instead
# of a narrative Summary). The stamp may live under any of these headings.
TRACKED_HEADING_RE = re.compile(
    r"^##+\s+(Summary|Module Health|File Inventory|Module Inventory|"
    r"Top-Level Modules|Document Inventory|Modules)\b",
    re.MULTILINE,
)


def detect_current_phase() -> int | None:
    """Return the highest Phase number visible in mem index or §27 changelog."""
    candidates: list[int] = []
    for src in (MEM_INDEX, CHANGELOG_27):
        if not src.exists():
            continue
        for m in PHASE_RE.finditer(src.read_text(encoding="utf-8", errors="ignore")):
            try:
                candidates.append(int(m.group(1)))
            except ValueError:
                continue
    return max(candidates) if candidates else None


def find_99_files() -> list[Path]:
    """All §99 files anywhere under spec/, excluding _archive/."""
    return sorted(p for p in SPEC.rglob("99-consistency-report.md")
                  if "_archive" not in p.parts)


def find_summary_stamp(text: str) -> int | None:
    """Return the highest phase number stamped under ANY tracked heading
    (## Summary OR an inventory-rubric heading), or None if no tracked heading
    has a stamp. Phase H2 widened the scope from Summary-only to also accept
    inventory-rubric blocks; multi-block scan ensures a stamp under Summary
    is still found even if an inventory heading appears first."""
    matches = list(TRACKED_HEADING_RE.finditer(text))
    if not matches:
        return None
    best: int | None = None
    for i, m in enumerate(matches):
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # Also stop at any other ## heading inside the slice (defensive).
        body = text[body_start:body_end]
        next_h = re.search(r"^##+\s+\S", body, re.MULTILINE)
        if next_h:
            body = body[:next_h.start()]
        stamp = STAMP_RE.search(body)
        if not stamp:
            continue
        try:
            n = int(stamp.group(1))
        except ValueError:
            continue
        if best is None or n > best:
            best = n
    return best


def find_misplaced_stamps(text: str) -> list[tuple[int, str]]:
    """Phase H9 (2026-04-28): detect stamps placed immediately BEFORE a tracked
    heading rather than under it. Codifies the H8 stamp-position precedent —
    5 files in H8 had `<!-- verified-phase: NNN -->` on a blank line above
    `## Summary` and the heading-body scanner correctly rejected them.

    Returns a list of (line_number, snippet) for each stamp that:
      - Appears OUTSIDE any tracked-heading body, AND
      - Is followed (within the next 3 non-empty lines) by a tracked heading
        (suggesting authorial intent was "stamp this heading").

    Stamps that appear inside blockquoted narrative (e.g. §27's Validation
    History referencing past phases) are NOT flagged — they aren't adjacent
    to a tracked heading and represent legitimate documentation.
    """
    findings: list[tuple[int, str]] = []
    headings = list(TRACKED_HEADING_RE.finditer(text))
    # Build set of (start, end) tracked-body slices for in-body check.
    bodies: list[tuple[int, int]] = []
    for i, h in enumerate(headings):
        body_start = h.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[body_start:body_end]
        nh = re.search(r"^##+\s+\S", body, re.MULTILINE)
        if nh:
            body_end = body_start + nh.start()
        bodies.append((body_start, body_end))

    def in_any_body(pos: int) -> bool:
        return any(s <= pos < e for s, e in bodies)

    lines = text.split("\n")
    for s in STAMP_RE.finditer(text):
        if in_any_body(s.start()):
            continue
        # Find line number of stamp.
        line_no = text[:s.start()].count("\n") + 1
        # Look at next 3 non-empty lines: is one of them a tracked heading?
        for j in range(line_no, min(line_no + 3, len(lines))):
            ln = lines[j].strip()
            if not ln:
                continue
            if TRACKED_HEADING_RE.match(lines[j]):
                findings.append((line_no, lines[line_no - 1].strip()))
                break
            # First non-empty non-heading line — not adjacent to tracked heading.
            break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-only", action="store_true",
                        help="Never exit 1; print findings and exit 0.")
    parser.add_argument("--max-age", type=int, default=20,
                        help="Max phase delta before a stamp is stale (default: 20).")
    parser.add_argument("--strict-position", action="store_true",
                        help="Phase H9: also fail if any stamp appears immediately "
                             "BEFORE a tracked heading rather than under it.")
    args = parser.parse_args()

    current = detect_current_phase()
    if current is None:
        print("ERROR: cannot determine current phase from mem://index.md or §27 changelog.",
              file=sys.stderr)
        return 2
    print(f"Current phase: {current}; max stale delta: {args.max_age}")

    files = find_99_files()
    if not files:
        print("WARNING: no §99 files found under spec/.", file=sys.stderr)
        return 0

    stamped = 0
    unstamped = 0
    exempt = 0
    stale: list[tuple[Path, int, int]] = []
    misplaced: list[tuple[Path, int, str]] = []

    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if EXEMPT_RE.search(text):
            exempt += 1
            continue
        stamp = find_summary_stamp(text)
        if stamp is None:
            unstamped += 1
        else:
            stamped += 1
            delta = current - stamp
            if delta > args.max_age:
                stale.append((f, stamp, delta))
        # H9: position check runs on every non-exempt file (including stamped
        # ones — a misplaced ghost stamp can hide near a tracked heading even
        # when a correctly-placed stamp also exists in another body).
        for line_no, snippet in find_misplaced_stamps(text):
            misplaced.append((f, line_no, snippet))

    print(f"§99 files scanned: {len(files)}; stamped: {stamped}; exempt: {exempt}; unstamped: {unstamped}")
    if unstamped:
        print(f"  (info) {unstamped} §99 files have no `<!-- verified-phase: NNN -->` stamp — advisory only.")
    if exempt:
        print(f"  (info) {exempt} §99 files carry `<!-- freshness-exempt: ... -->` and are skipped.")

    failed = False

    if stale:
        print()
        print(f"❌ {len(stale)} §99 file(s) carry a stale Summary stamp (>{args.max_age} phases behind):")
        for f, stamp, delta in stale:
            rel = f.relative_to(REPO)
            print(f"  - {rel}  [stamp: Phase {stamp}, delta: {delta}]")
        failed = True

    if misplaced:
        print()
        label = "❌" if args.strict_position else "⚠️ "
        mode = "strict-position" if args.strict_position else "advisory"
        print(f"{label} {len(misplaced)} stamp(s) placed immediately BEFORE a tracked heading "
              f"rather than under it ({mode}):")
        for f, line_no, snippet in misplaced:
            rel = f.relative_to(REPO)
            print(f"  - {rel}:{line_no}  {snippet}")
        print(f"  (Phase H8 precedent: stamps MUST live INSIDE a tracked-heading body. "
              f"Move the stamp to the line immediately AFTER the heading.)")
        if args.strict_position:
            failed = True

    if failed:
        if args.report_only:
            print()
            print("  --report-only: not failing.")
            return 0
        return 1

    print("✅ All stamped §99 Summary blocks are within freshness budget.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())

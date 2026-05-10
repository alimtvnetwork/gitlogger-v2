#!/usr/bin/env python3
"""
check-memo-retrospective-headings.py — Phase 104 meta-linter.

Scans phase memos under `.lovable/memory/audit/v2-deterministic/phase-NNN-*.md`
and FAILS if any memo at or above the cutoff phase contains a forward-looking
H2/H3 section heading (e.g., "Next phases", "Next iteration", "Remaining
Tasks", "Future work", "TODO", "Upcoming", "Roadmap").

Why this matters
----------------
Phase 100 retired the freshness-sweep + "Next phases" cadence after empirical
evidence that recent memos (Phase 90+) were already self-contained
retrospectives that did not drift. Forward-looking sections in a memo create
two problems:

  1. **Drift**: a "Next phases" list inside a memo for Phase N becomes stale
     the moment Phase N+1 lands. The memo then misrepresents the actual path
     taken.
  2. **Authority confusion**: there is exactly ONE place where pending work
     belongs — the chat reply's "Remaining Tasks" table. A second list inside
     a memo competes with that single source of truth.

A memo's purpose is to record what happened in that phase, why, and what it
mechanically locked. Predictions about future phases belong in chat (and in
the AC's `Verifies` clause if they were locked in by code), not in the memo.

Cutoff
------
Phase 100 retired the cadence; Phases 100, 101, 102, 103 deliberately ship
with retrospective sections only ("Closing the freshness-sweep cadence",
"What this enables", "Why Phase N's prediction was correct"). Memos with
phase number < CUTOFF_PHASE are historical record and are NOT modified —
the linter only enforces the rule on new memos.

Forbidden heading patterns (matched case-insensitively at H2/H3 only):
  - "Next phases", "Next phase", "Next iteration", "Next iterations"
  - "Next Recommended ..." (e.g., "Next Recommended Phase", "Next Recommended Work")
  - "Remaining work", "Remaining Tasks", "Remaining Backlog", "Remaining backlog"
  - "Future work", "Future iteration"
  - "TODO", "Upcoming", "Roadmap"

Allowed retrospective alternatives (suggested in error output):
  - "What this enables" — what the locked contract makes possible going forward
  - "Why Phase N's prediction was correct" — citing the prior memo verbatim
  - "Closing the X cadence" — explicitly retiring a previous pattern
  - "Why this matters" — the rationale section
  - "Verification" — what was checked
  - "Files touched" — concrete record
  - "Score impact" — measured effect

Exit codes:
  0  All in-scope memos are retrospective-only.
  1  One or more memos contain forbidden forward-looking headings.
  2  Structural error (memo directory missing).

Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-29)
Memo: .lovable/memory/audit/v2-deterministic/phase-104-memo-retrospective-headings.md
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

MEMO_DIR = Path(".lovable/memory/audit/v2-deterministic")
PHASE_RX = re.compile(r"^phase-(\d+)-", re.IGNORECASE)
HEADING_RX = re.compile(r"^(#{2,3})\s+(.+?)\s*$")

# Phase 100 retired the freshness-sweep cadence and explicitly
# established the retrospective-only convention. Memos at or above
# this cutoff MUST be retrospective. Older memos are historical record.
CUTOFF_PHASE = 100

# Forbidden heading patterns (case-insensitive substring match against the
# heading text — the part after the leading `##`/`###` markers).
FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Next phases / Next phase",           re.compile(r"^next\s+phases?\b", re.IGNORECASE)),
    ("Next iteration / Next iterations",   re.compile(r"^next\s+iterations?\b", re.IGNORECASE)),
    ("Next Recommended …",                 re.compile(r"^next\s+recommended\b", re.IGNORECASE)),
    ("Remaining work / tasks / backlog",   re.compile(r"^remaining\s+(work|tasks?|backlog)\b", re.IGNORECASE)),
    ("Future work / iteration",            re.compile(r"^future\s+(work|iterations?|phases?)\b", re.IGNORECASE)),
    ("TODO heading",                       re.compile(r"^todo\b", re.IGNORECASE)),
    ("Upcoming",                           re.compile(r"^upcoming\b", re.IGNORECASE)),
    ("Roadmap",                            re.compile(r"^roadmap\b", re.IGNORECASE)),
]

SUGGESTED_REPLACEMENTS = [
    "## What this enables",
    "## Why Phase <N>'s prediction was correct",
    "## Closing the <X> cadence",
    "## Why this matters",
    "## Verification",
    "## Files touched",
    "## Score impact",
]


def phase_number(filename: str) -> int | None:
    m = PHASE_RX.match(filename)
    return int(m.group(1)) if m else None


def scan_memo(path: Path) -> list[tuple[int, str, str]]:
    """Return list of (line_no, heading_text, matched_pattern_label)."""
    findings: list[tuple[int, str, str]] = []
    for ln, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        m = HEADING_RX.match(raw)
        if not m:
            continue
        heading_text = m.group(2)
        for label, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(heading_text):
                findings.append((ln, raw, label))
                break
    return findings


def main() -> int:
    if not MEMO_DIR.is_dir():
        print(f"❌ Memo directory not found: {MEMO_DIR}", file=sys.stderr)
        return 2

    in_scope: list[Path] = []
    for p in sorted(MEMO_DIR.glob("phase-*.md")):
        n = phase_number(p.name)
        if n is None:
            continue
        if n >= CUTOFF_PHASE:
            in_scope.append(p)

    if not in_scope:
        print(f"⚠ No memos at or above phase {CUTOFF_PHASE} found.", file=sys.stderr)
        return 0

    total_findings = 0
    failed_memos: list[Path] = []
    for memo in in_scope:
        findings = scan_memo(memo)
        if findings:
            failed_memos.append(memo)
            total_findings += len(findings)
            print(f"\n❌ {memo}")
            for ln, raw, label in findings:
                print(f"   line {ln}: {raw}")
                print(f"            → forbidden pattern: {label}")

    print()
    print(f"Memos scanned (phase ≥ {CUTOFF_PHASE}): {len(in_scope)}")
    print(f"Memos with forbidden headings        : {len(failed_memos)}")
    print(f"Total forbidden headings             : {total_findings}")

    if total_findings == 0:
        print("\n✅ All in-scope memos are retrospective-only (no forward-looking headings).")
        return 0

    print()
    print("Phase 100 retired the forward-looking 'Next phases' / 'Remaining' /")
    print("'Next iteration' cadence inside memos. Pending work belongs in the")
    print("chat reply's 'Remaining Tasks' table — the single source of truth.")
    print()
    print("Suggested retrospective replacements:")
    for s in SUGGESTED_REPLACEMENTS:
        print(f"  • {s}")
    print()
    print("Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-29)")
    return 1


if __name__ == "__main__":
    sys.exit(main())

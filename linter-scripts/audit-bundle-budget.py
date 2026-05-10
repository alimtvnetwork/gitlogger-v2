#!/usr/bin/env python3
# audit-bundle-budget.py — Walker bundle budget audit (deterministic, no gateway)
#
# Phase 153 Task A24-fu32 — productionised from /tmp/a24-fu27-bundle-budget.py
# (the ephemeral script used in Phase 153 fu27 to enumerate the OVER class
# and drive the fu28-fu31 sweep). The fu27 audit shipped Lesson #65
# (structural surgery > pure-promotion); this script makes the gate permanent
# so future regressions are caught the next CI run, not the next quarterly
# rebaseline.
#
# Reads MAX_BYTES directly from audit-ai-implementability.py to avoid drift.
#
# Per-module classification:
#   CLEAR       — siblings fit under (cap - §00 - §97); full bundle visible
#   AT_CEILING  — siblings exceed headroom but tier1 itself fits cap
#   OVER        — tier1 (§00+§97+§98+§99) alone exceeds cap; STRUCTURAL EMERGENCY
#
# Default mode: advisory (exit 0; print report to stdout).
# --strict: exit 1 if any module is OVER (use as CI gate after fu28-fu31 sweep).

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_ROOT = REPO_ROOT / "spec"
AUDITOR_PATH = REPO_ROOT / "linter-scripts" / "audit-ai-implementability.py"

TIER1_PATTERN = re.compile(r"^(00|97|98|99)-.*\.md$")
SIBLING_PATTERN = re.compile(r"^(0[1-9]|[1-8][0-9]|9[0-6])-.*\.md$")  # 01..96
MODULE_PATTERN = re.compile(r"^\d{2}-")


def read_max_bytes() -> int:
    """Pull MAX_BYTES from audit-ai-implementability.py to avoid drift."""
    if not AUDITOR_PATH.exists():
        return 120_000
    text = AUDITOR_PATH.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^MAX_BYTES\s*=\s*([\d_]+)", text, re.MULTILINE)
    if not m:
        return 120_000
    return int(m.group(1).replace("_", ""))


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def analyse_module(module_dir: Path, cap: int) -> dict:
    tier1_bytes = 0
    sibling_bytes = 0
    sibling_count = 0
    s00 = s97 = s98 = s99 = 0

    for entry in sorted(module_dir.iterdir()):
        if not entry.is_file() or not entry.name.endswith(".md"):
            continue
        size = file_size(entry)
        if TIER1_PATTERN.match(entry.name):
            tier1_bytes += size
            if entry.name.startswith("00-"):
                s00 += size
            elif entry.name.startswith("97-"):
                s97 += size
            elif entry.name.startswith("98-"):
                s98 += size
            elif entry.name.startswith("99-"):
                s99 += size
        elif SIBLING_PATTERN.match(entry.name):
            sibling_bytes += size
            sibling_count += 1

    headroom = max(0, cap - s00 - s97)
    if tier1_bytes > cap:
        status = "OVER"
        deficit = tier1_bytes - cap
    elif sibling_bytes > headroom:
        status = "AT_CEILING"
        deficit = sibling_bytes - headroom
    else:
        status = "CLEAR"
        deficit = 0

    return {
        "module": module_dir.name,
        "s00": s00,
        "s97": s97,
        "s98": s98,
        "s99": s99,
        "tier1": tier1_bytes,
        "siblings": sibling_bytes,
        "sibling_count": sibling_count,
        "headroom": headroom,
        "deficit": deficit,
        "status": status,
    }


def collect() -> list[dict]:
    cap = read_max_bytes()
    modules = []
    for entry in sorted(SPEC_ROOT.iterdir()):
        if not entry.is_dir() or not MODULE_PATTERN.match(entry.name):
            continue
        if entry.name.startswith("_"):
            continue
        modules.append(analyse_module(entry, cap))
    return modules


def fmt_kb(n: int) -> str:
    return f"{n/1024:.1f}"


def render_report(modules: list[dict], cap: int) -> str:
    rank = {"OVER": 0, "AT_CEILING": 1, "CLEAR": 2}
    modules_sorted = sorted(modules, key=lambda m: (rank[m["status"]], -m["deficit"]))
    counts = {"OVER": 0, "AT_CEILING": 0, "CLEAR": 0}
    for m in modules:
        counts[m["status"]] += 1

    lines = [
        f"# Walker Bundle Budget Audit",
        "",
        f"**Walker cap (MAX_BYTES):** {cap:,} bytes (~{cap/1024:.0f} KB)",
        f"**Source:** `linter-scripts/audit-ai-implementability.py`",
        f"**Modules scanned:** {len(modules)}",
        f"**Status counts:** OVER={counts['OVER']} · AT_CEILING={counts['AT_CEILING']} · CLEAR={counts['CLEAR']}",
        "",
        "| Module | §00 | §97 | §98 | §99 | tier1 | siblings | #sib | deficit | status |",
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|---|",
    ]
    for m in modules_sorted:
        lines.append(
            f"| {m['module']} | {fmt_kb(m['s00'])} | {fmt_kb(m['s97'])} | {fmt_kb(m['s98'])} | {fmt_kb(m['s99'])} "
            f"| {fmt_kb(m['tier1'])} | {fmt_kb(m['siblings'])} | {m['sibling_count']} "
            f"| {fmt_kb(m['deficit'])} | **{m['status']}** |"
        )
    lines.append("")
    lines.append("(All sizes KB.)")
    lines.append("")
    lines.append("## Classification")
    lines.append("")
    lines.append("- **CLEAR** — siblings fit in headroom (cap − §00 − §97); auditor sees full bundle.")
    lines.append("- **AT_CEILING** — siblings exceed headroom but tier1 itself fits cap; pure-promotion teasers ineffective (Lesson #64). Sibling extraction is the only lever.")
    lines.append("- **OVER** — tier1 alone exceeds cap; STRUCTURAL EMERGENCY (Lesson #65). Apply §98 archive split or §97 sub-folder extraction.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Walker bundle budget audit (deterministic).")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON to stdout.")
    parser.add_argument("--report", type=Path, help="Write markdown report to PATH.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any module is OVER.")
    args = parser.parse_args()

    cap = read_max_bytes()
    modules = collect()
    counts = {"OVER": 0, "AT_CEILING": 0, "CLEAR": 0}
    for m in modules:
        counts[m["status"]] += 1

    if args.json:
        print(json.dumps({"cap": cap, "counts": counts, "modules": modules}, indent=2))
    else:
        report = render_report(modules, cap)
        print(report)
        if args.report:
            args.report.write_text(report, encoding="utf-8")
            print(f"\nReport: {args.report}", file=sys.stderr)

    if args.strict and counts["OVER"] > 0:
        print(f"\nFAIL: {counts['OVER']} module(s) OVER walker cap ({cap:,} bytes).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

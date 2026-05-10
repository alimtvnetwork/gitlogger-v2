#!/usr/bin/env python3
"""
check-ai-confidence.py — P48-1-fu1 AC-09 mechanization gate.

Phase P48-1-fu1 (2026-04-29). Advisory-by-default per H1 / P20 pattern.

Mechanizes the four-gate AI Confidence rubric defined in
`spec/17-consolidated-guidelines/01-spec-authoring.md` § *AI Confidence
Rubric (normative)* and bound by AC-09 in §17 §97.

For each `spec/<module>/00-overview.md` carrying a `**AI Confidence:**`
banner, the script:

  1) Evaluates the four gates against deterministic on-disk signals:
       P1 — §00 exists, lists every sibling .md in inventory, Updated
            date is within the current calendar year.
       P2 — P1 holds AND §97 contains ≥1 GWT-shaped AC (`**Given**` /
            `**When**` / `**Then**`) AND no spec file under the module
            ends with a truncation marker (trailing `…`, mid-sentence
            cut, or a bare TODO/TBD/FIXME line).
       P3 — P2 holds AND every AC in §97 has a `**Verifies:**` clause.
       P4 — P3 holds AND module path is referenced in
            `.github/workflows/spec-health.yml` AND §99 carries a
            `<!-- verified-phase: NNN -->` stamp ≤ 30 phases stale
            (relative to the highest stamp anywhere in the tree).

  2) Maps the highest-passing gate to a tier:
       P4 → "Production-Ready"
       P3 → "High"
       P2 → "Medium"
       P1 → "Low"
       (none) → unset

  3) Compares the *derived* tier to the *declared* banner value and
     emits drift findings.

This is intentionally a CHEAP linter — it does NOT re-run the four
underlying gate scripts. It re-implements the cheapest version of each
signal inline so the linter is fast (<2s tree-wide) and stable across
machines that may not have node/python deps for the heavier gates.
For authoritative gate verdicts, run the underlying scripts directly.

Modes (mirrors check-version-parity.py P20/P31 pattern exactly):
  default        : advisory; exit 0; emit one info line per drift.
                   Drifts on STAMPED §00 files still fail in default
                   mode (per-file strict promotion path).
  --strict       : exit 1 on ANY drift (tree-wide CI gate once
                   adoption matures).
  --report-only  : never fails (overrides --strict AND per-file
                   stamps); useful for dashboards.
  --json         : machine-readable output.

Per-file opt-in stamp:
  Authors who have verified their §00 banner matches the rubric-derived
  tier can add inside the first 40 lines of `00-overview.md`:

      <!-- ai-confidence-verified-phase: NNN -->

  Once stamped, ANY future drift on that file fails the gate even in
  default (advisory-tree) mode. Stamp name deliberately distinct from
  `verified-phase` (H1 §99 freshness) and `h10-verified-phase` (P20
  version parity) so the three opt-in gates remain independently
  trackable per file.

Skip rules:
  - Files under `spec/_archive/**` (frozen by design).
  - Modules whose `00-overview.md` has no `**AI Confidence:**` banner
    (opt-in — the field is not required by tree-health).
  - Tier value `unset` / blank (matches the rubric's "omit rather than
    guess" rule — no drift can be computed).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
SPEC_ROOT = ROOT / "spec"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "spec-health.yml"

TIER_VALUES = ("Production-Ready", "High", "Medium", "Low")
TIER_RANK = {t: i for i, t in enumerate(TIER_VALUES)}  # 0 = best, 3 = worst

# Strip CR + nbsp + trailing whitespace from a banner value.
def _norm(v: str) -> str:
    return v.replace("\u00a0", " ").strip().rstrip(",;:.").strip()

BANNER_AI = re.compile(r"^\*\*AI Confidence:\*\*\s*(?:`)?([A-Za-z\-]+)(?:`)?", re.M)
BANNER_UPDATED = re.compile(r"^\*\*Updated:\*\*\s*(\d{4})-(\d{2})-(\d{2})", re.M)
STAMP_RE = re.compile(r"<!--\s*ai-confidence-verified-phase:\s*(\d+)\s*-->")
H1_STAMP_RE = re.compile(r"<!--\s*verified-phase:\s*(\d+)\s*-->")
TRUNC_TAIL = re.compile(r"(\.{3,}|…|TODO|TBD|FIXME)\s*$", re.I)

GWT_RE = re.compile(r"\*\*(Given|When|Then)\*\*", re.M)
VERIFIES_RE = re.compile(r"\*\*Verifies:\*\*", re.M)
AC_RE = re.compile(r"^### AC[-_][A-Za-z0-9\-]+", re.M)
INVENTORY_LINK_RE = re.compile(r"\]\(\.\/([A-Za-z0-9_][A-Za-z0-9_\-\.]*\.md)\)")
# Phase 153 Task #29d (2026-04-29): bare-filename inventory matches inside table
# rows or list items. Restricts to inventory-shaped lines (starting with `|`,
# `-`, or `*`, optionally with leading whitespace) to avoid matching arbitrary
# `.md` words in prose. Backtick-wrapped filenames are also accepted. Mirrors
# the AC-33-07 broadening precedent (numeric-prefix → any-prefix) — same shape,
# different surface form (markdown link vs. table cell).
INVENTORY_BARE_RE = re.compile(
    r"^[ \t]*[|\-*][^\n]*?`?([A-Za-z0-9_][A-Za-z0-9_\-/\.]*\.md)`?",
    re.M,
)


def list_modules() -> list[Path]:
    """Every directory under spec/ (recursively) that contains a 00-overview.md.

    Phase 153 Task #29b (2026-04-29) widened from top-level-only to recursive:
    nested sub-modules (e.g. spec/03-error-manage/02-error-architecture/.../01-copy-formats/)
    routinely carry their own `**AI Confidence:**` banners and were silently
    skipped by the v1 walker, masking ~40 modules' worth of drift signal.
    """
    out = []
    for ov in sorted(SPEC_ROOT.rglob("00-overview.md")):
        # Skip _archive/** (frozen by design) and any hidden-prefixed parent.
        if any(part.startswith("_") for part in ov.relative_to(SPEC_ROOT).parts):
            continue
        out.append(ov.parent)
    return out


def parse_banner(text: str) -> Optional[str]:
    m = BANNER_AI.search(text)
    if not m:
        return None
    val = _norm(m.group(1))
    return val if val in TIER_VALUES else None


def gate_p1(mod: Path, ov_text: str) -> tuple[bool, str]:
    # Inventory completeness: every sibling .md (excluding 00 itself, and the
    # standard meta-slots 97/98/99 which are conventionally omitted from
    # inventory tables — they are guaranteed to exist by tree-health and have
    # their own dedicated linters).
    META = {"00-overview.md", "97-acceptance-criteria.md", "98-changelog.md", "99-consistency-report.md"}
    siblings = {p.name for p in mod.iterdir() if p.is_file() and p.name.endswith(".md") and p.name not in META}
    if not siblings:
        listed = set()
    else:
        # Markdown-link form `](./file.md)` is unambiguous — scan the whole
        # document (these are explicit cross-refs anywhere in §00).
        listed = set(INVENTORY_LINK_RE.findall(ov_text))
        # Bare-filename form (table cells, list items) is ambiguous — restrict
        # to the section under a `## ... Inventory` heading to avoid matching
        # `.md` words in arbitrary prose. Falls back to no bare-scan if no
        # such heading exists (the link-form scan above still applies).
        # Scan EVERY inventory-titled section (a §00 may carry both a "Full
        # Document Inventory" with subfolder paths AND a "Document Inventory"
        # with bare filenames — both are legitimate listings).
        inv_heading_re = re.compile(r"^##[^\n]*(Inventory|Index|Modules|Files|Contents)[^\n]*\n", re.M | re.I)
        next_h2_re = re.compile(r"^## ", re.M)
        for m_inv in inv_heading_re.finditer(ov_text):
            after = ov_text[m_inv.end():]
            m_next = next_h2_re.search(after)
            inv_section = after[: m_next.start()] if m_next else after
            for raw in INVENTORY_BARE_RE.findall(inv_section):
                listed.add(raw.rsplit("/", 1)[-1])
    missing = siblings - listed
    if missing:
        return False, f"P1: {len(missing)} sibling(s) not in inventory ({sorted(missing)[:3]}…)"
    m = BANNER_UPDATED.search(ov_text)
    if not m:
        return False, "P1: no `**Updated:** YYYY-MM-DD` banner"
    yr = int(m.group(1))
    if yr != date.today().year:
        return False, f"P1: Updated year {yr} ≠ current year {date.today().year}"
    return True, "P1 ok"


def gate_p2(mod: Path) -> tuple[bool, str]:
    ac = mod / "97-acceptance-criteria.md"
    if not ac.is_file():
        return False, "P2: §97 missing"
    ac_text = ac.read_text(encoding="utf-8", errors="replace")
    if not GWT_RE.search(ac_text):
        return False, "P2: §97 has zero GWT (`**Given**`/`**When**`/`**Then**`) markers"
    # Truncation: scan all .md in module for trailing-marker last non-empty line.
    for f in sorted(mod.glob("*.md")):
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Strip trailing whitespace/newlines, then take last non-empty line.
        lines = [ln for ln in txt.rstrip().splitlines() if ln.strip()]
        if not lines:
            return False, f"P2: {f.name} is empty"
        last = lines[-1].rstrip()
        if TRUNC_TAIL.search(last):
            return False, f"P2: {f.name} ends in truncation marker (`{last[-20:]}`)"
    return True, "P2 ok"


def gate_p3(mod: Path) -> tuple[bool, str]:
    ac = mod / "97-acceptance-criteria.md"
    if not ac.is_file():
        return False, "P3: §97 missing"
    ac_text = ac.read_text(encoding="utf-8", errors="replace")
    ac_count = len(AC_RE.findall(ac_text))
    if ac_count == 0:
        return False, "P3: §97 has zero `### AC-…` headings"
    verifies_count = len(VERIFIES_RE.findall(ac_text))
    if verifies_count < ac_count:
        return False, f"P3: §97 has {ac_count} ACs but only {verifies_count} `**Verifies:**` clauses"
    return True, "P3 ok"


def _max_h1_stamp_in_tree() -> int:
    """Highest `<!-- verified-phase: NNN -->` stamp anywhere in spec/, used as 'now' for staleness."""
    high = 0
    for f in SPEC_ROOT.rglob("*.md"):
        if "_archive" in f.parts:
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in H1_STAMP_RE.finditer(txt):
            n = int(m.group(1))
            if n > high:
                high = n
    return high


def gate_p4(mod: Path, workflow_text: str, h1_horizon: int) -> tuple[bool, str]:
    # CI-gate referenced: either the leaf dir name is mentioned, OR the
    # workflow uses a `spec/**` glob that transitively covers the module,
    # OR the module's spec-relative path is mentioned verbatim.
    try:
        rel = mod.relative_to(ROOT).as_posix()
    except ValueError:
        rel = mod.as_posix()
    covered = (
        mod.name in workflow_text
        or "spec/**" in workflow_text
        or rel in workflow_text
    )
    if not covered:
        return False, f"P4: '{mod.name}' not referenced in spec-health.yml (and no spec/** glob)"
    # §99 H1 stamp ≤ 30 phases stale.
    cr = mod / "99-consistency-report.md"
    if not cr.is_file():
        return False, "P4: §99 missing"
    cr_text = cr.read_text(encoding="utf-8", errors="replace")
    stamps = [int(m.group(1)) for m in H1_STAMP_RE.finditer(cr_text)]
    if not stamps:
        return False, "P4: §99 has no `<!-- verified-phase: NNN -->` stamp"
    newest = max(stamps)
    age = h1_horizon - newest
    if age > 30:
        return False, f"P4: §99 stamp phase {newest} is {age} phases stale (horizon={h1_horizon}, budget=30)"
    return True, f"P4 ok (stamp {newest}, age {age})"


def derive_tier(mod: Path, workflow_text: str, h1_horizon: int) -> tuple[Optional[str], list[str]]:
    """Return (derived_tier_or_None, reasons)."""
    ov = (mod / "00-overview.md").read_text(encoding="utf-8", errors="replace")
    reasons = []
    ok, why = gate_p1(mod, ov); reasons.append(why)
    if not ok:
        return None, reasons
    ok, why = gate_p2(mod); reasons.append(why)
    if not ok:
        return "Low", reasons
    ok, why = gate_p3(mod); reasons.append(why)
    if not ok:
        return "Medium", reasons
    ok, why = gate_p4(mod, workflow_text, h1_horizon); reasons.append(why)
    if not ok:
        return "High", reasons
    return "Production-Ready", reasons


def main() -> int:
    ap = argparse.ArgumentParser(description="P48-1-fu1 AI-Confidence rubric mechanization gate")
    ap.add_argument("--strict", action="store_true", help="exit 1 on ANY drift")
    ap.add_argument("--report-only", action="store_true", help="never fail; overrides --strict and stamps")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8", errors="replace") if WORKFLOW_PATH.is_file() else ""
    h1_horizon = _max_h1_stamp_in_tree()

    rows = []
    for mod in list_modules():
        ov_path = mod / "00-overview.md"
        ov = ov_path.read_text(encoding="utf-8", errors="replace")
        declared = parse_banner(ov)
        if declared is None:
            continue  # skip: no banner or unrecognized value
        derived, reasons = derive_tier(mod, workflow_text, h1_horizon)
        # `unset` derived (P1 fails) — this is a real finding (banner exists but P1 fails).
        head40 = "\n".join(ov.splitlines()[:40])
        stamp_m = STAMP_RE.search(head40)
        stamped = stamp_m is not None
        stamped_phase = int(stamp_m.group(1)) if stamp_m else None
        match = (declared == derived)
        try:
            mod_label = mod.relative_to(SPEC_ROOT).as_posix()
        except ValueError:
            mod_label = mod.name
        rows.append({
            "module": mod_label,
            "declared": declared,
            "derived": derived,
            "match": match,
            "stamped": stamped,
            "stamped_phase": stamped_phase,
            "reason_chain": reasons,
        })

    eligible = len(rows)
    matches = sum(1 for r in rows if r["match"])
    mismatches = eligible - matches
    stamped = sum(1 for r in rows if r["stamped"])
    stamped_failed = sum(1 for r in rows if r["stamped"] and not r["match"])

    if args.json:
        json.dump({
            "scanned_modules": len(list_modules()),
            "eligible": eligible,
            "matches": matches,
            "mismatches": mismatches,
            "stamped": stamped,
            "stamped_failed": stamped_failed,
            "h1_horizon": h1_horizon,
            "rows": rows,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"AI-Confidence rubric parity: scanned={len(list_modules())}; eligible={eligible}; "
              f"matches={matches}; mismatches={mismatches}; stamped={stamped}; stamped_failed={stamped_failed}; "
              f"h1_horizon={h1_horizon}")
        for r in rows:
            if r["match"]:
                continue
            tag = " [stamped]" if r["stamped"] else ""
            print(f"  (DRIFT) spec/{r['module']}: declared={r['declared']!r:18s} derived={r['derived']!r:18s}{tag}")
            for why in r["reason_chain"]:
                if why.startswith(("P1: ", "P2: ", "P3: ", "P4: ")):
                    print(f"      reason: {why}")

    if args.report_only:
        return 0
    if args.strict:
        return 1 if mismatches > 0 else 0
    # Default: only fail on STAMPED drift (per-file strict promotion).
    return 1 if stamped_failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

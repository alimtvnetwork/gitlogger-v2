#!/usr/bin/env python3
"""
check-version-parity.py — H10 §00 ↔ §98 Version-field parity gate.

Phase P15 (2026-04-28). Advisory-by-default per H1 pattern.

Codifies the Phase 21 lesson: when a spec module's `00-overview.md`
carries a `**Version:** vX.Y.Z` banner AND a sibling `98-changelog.md`
ships a release line, the §00 banner version SHOULD equal the latest
§98 release version. The lockstep gate (§24) only checks DATE relations
(L1: §98 latest date ≥ §00 Updated date) — it does NOT check version
strings, so the §00 banner can drift many releases behind §98 while
lockstep stays green (Phase 21 found §27 §00 v1.7.0 vs §98 v2.46.2;
P15 baseline sweep found 59/74 modules drifting).

Modes:
  default        : advisory; exit 0; emit one info line per mismatch.
                   Mismatches in STAMPED §00 files (see below) still fail
                   in default mode — that is the per-file strict promotion
                   path (Phase P20, mirrors H1 / check-99-summary-freshness).
  --strict       : exit 1 on ANY mismatch (tree-wide CI gate when adoption
                   matures; today 57/74 modules drift, so unused in CI).
  --report-only  : never fails (overrides --strict AND per-file stamps);
                   useful for dashboards.
  --json         : machine-readable output (adds `stamped`, `stamped_failed`).

Per-file opt-in stamp (Phase P20):
  Authors who have caught a §00 banner up to its §98 latest release can
  add a stamp INSIDE the first 40 lines of `00-overview.md`:

      <!-- h10-verified-phase: 152 -->

  Once stamped, ANY future §00 ↔ §98 mismatch on that file fails the
  gate even in default (advisory-tree) mode. This lets modules opt into
  strict enforcement one at a time without waiting for all 57 drifters
  to catch up. Mirrors the H1 `<!-- verified-phase: NNN -->` pattern.

Skip rules:
  - Files under `spec/_archive/**` (frozen by design — H2 lesson).
  - Modules whose `00-overview.md` has no `**Version:**` banner (opt-in).
  - Modules with no sibling `98-changelog.md`.
  - Changelogs with no parseable release line (heading or table-row).

Spec: spec/27-spec-toolchain/29-check-version-parity.md
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"

# §00 banner version: `**Version:** v1.2.3` or `**Version:** 1.2.3` near top.
BANNER_VER_RE = re.compile(r"\*\*Version:\*\*\s*v?(\d+\.\d+\.\d+)")

# Phase P20: per-file opt-in strict-promotion stamp under §00.
# Mirrors `check-99-summary-freshness.py`'s `<!-- verified-phase: NNN -->`.
H10_STAMP_RE = re.compile(r"<!--\s*h10-verified-phase:\s*(\d{1,4})\s*-->")

# §98 release line — accept four shapes used across the tree:
#   ## 1.2.0 — 2026-04-27
#   ### v4.0.0 — 2026-04-26
#   ## [4.1.0] — 2026-04-26
#   | 3.9.8 | 2026-04-28 | … |     ← table-row format (folder 22)
RELEASE_HEADING_RE = re.compile(
    r"^\s{0,3}#{2,4}\s+\[?v?(\d+\.\d+\.\d+)\]?\s*[—\-–]?\s*(\d{4}-\d{2}-\d{2})?",
    re.MULTILINE,
)
RELEASE_ROW_RE = re.compile(
    r"^\|\s*v?(\d+\.\d+\.\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})?\s*\|",
    re.MULTILINE,
)
# Phase J3-fu (Lesson #28-fu): blockquote release prose used in spec/22 and
# similar archive-pruned changelogs:
#   > **v3.22.0 update (Phase J15 — …):** …
# The leading `> ` blockquote marker prevents heading and row regexes from
# matching; without this regex, the SemVer-MAX comparator silently misses
# any release shipped only as blockquote prose (Lesson #28 reinforcement —
# whenever the parity gate flags drift, inspect the comparator + scanned
# shapes BEFORE mass-patching the tree).
RELEASE_BLOCKQUOTE_RE = re.compile(
    r"^>\s*\*\*v?(\d+\.\d+\.\d+)\b",
    re.MULTILINE,
)


def _semver_key(v: str) -> tuple[int, int, int]:
    """Parse 'X.Y.Z' into a comparable tuple. Used to find SemVer-max release."""
    parts = v.split(".")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def latest_release(text: str) -> str | None:
    """Return the SemVer-MAXIMUM release version found in §98.

    Phase 153 Task #35-fu: switched from positional-first to SemVer-max.
    Patch reconciliation rows (Tasks #29c/d/e/#31) sometimes prepend
    SemVer-LOWER patches (e.g. 4.0.1) above older SemVer-HIGHER minor
    releases (e.g. 4.1.0); §00 banner correctly tracks the SemVer max
    (e.g. 4.1.1 = 4.1.0 + reconciliation patch). Comparing against the
    positional-first row produced 15 false-positive mismatches at
    Phase 153 close. SemVer is source of truth, not row position.
    """
    versions: list[str] = []
    for line in text.split("\n"):
        m = RELEASE_HEADING_RE.match(line)
        if m:
            versions.append(m.group(1))
            continue
        m = RELEASE_ROW_RE.match(line)
        if m:
            versions.append(m.group(1))
            continue
        m = RELEASE_BLOCKQUOTE_RE.match(line)
        if m:
            versions.append(m.group(1))
    if not versions:
        return None
    return max(versions, key=_semver_key)


def banner_version(text: str) -> str | None:
    head = "\n".join(text.split("\n")[:40])
    m = BANNER_VER_RE.search(head)
    return m.group(1) if m else None


def h10_stamp(text: str) -> int | None:
    """Return the highest h10-verified-phase stamp value found in the §00 head,
    or None if unstamped. Searches the first 40 lines (same window as the
    banner) so the stamp lives near the version it certifies."""
    head = "\n".join(text.split("\n")[:40])
    stamps = [int(m.group(1)) for m in H10_STAMP_RE.finditer(head)]
    return max(stamps) if stamps else None


def find_pairs(spec_root: Path):
    for overview in spec_root.rglob("00-overview.md"):
        if "_archive" in overview.parts:
            continue
        changelog = overview.parent / "98-changelog.md"
        if not changelog.exists():
            continue
        yield overview, changelog


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any §00 ↔ §98 version mismatch")
    ap.add_argument("--report-only", action="store_true",
                    help="never fail (overrides --strict)")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON instead of text")
    ap.add_argument("--spec-root", default=str(SPEC),
                    help=f"spec root (default: {SPEC})")
    args = ap.parse_args(argv)

    root = Path(args.spec_root).resolve()
    if not root.is_dir():
        print(f"ERROR: spec root not found: {root}", file=sys.stderr)
        return 2

    scanned = 0
    eligible = 0          # both banner + parseable release present
    matches = 0
    mismatches: list[dict] = []
    skipped_no_banner = 0
    skipped_no_release = 0
    stamped = 0           # §00 files carrying h10-verified-phase stamp
    stamped_failed = 0    # stamped files whose §00 ↔ §98 versions diverge

    for overview, changelog in find_pairs(root):
        scanned += 1
        ov_text = overview.read_text(encoding="utf-8", errors="ignore")
        bv = banner_version(ov_text)
        if not bv:
            skipped_no_banner += 1
            continue
        cl_text = changelog.read_text(encoding="utf-8", errors="ignore")
        lr = latest_release(cl_text)
        if not lr:
            skipped_no_release += 1
            continue
        eligible += 1
        stamp = h10_stamp(ov_text)
        if stamp is not None:
            stamped += 1
        if bv == lr:
            matches += 1
        else:
            try:
                mod_path = str(overview.parent.relative_to(ROOT))
            except ValueError:
                # --spec-root may point outside the repo (self-tests use a tmpdir).
                mod_path = str(overview.parent)
            entry = {
                "module": mod_path,
                "banner": bv,
                "latest_release": lr,
                "stamped": stamp,
            }
            mismatches.append(entry)
            if stamp is not None:
                stamped_failed += 1

    if args.json:
        out = {
            "scanned": scanned,
            "eligible": eligible,
            "matches": matches,
            "mismatches": len(mismatches),
            "skipped_no_banner": skipped_no_banner,
            "skipped_no_release": skipped_no_release,
            "stamped": stamped,
            "stamped_failed": stamped_failed,
            "details": mismatches,
        }
        print(json.dumps(out, indent=2))
    else:
        print(
            f"§00 ↔ §98 Version-field parity: "
            f"scanned={scanned}; eligible={eligible}; "
            f"matches={matches}; mismatches={len(mismatches)}; "
            f"skipped(no-banner)={skipped_no_banner}; "
            f"skipped(no-release)={skipped_no_release}; "
            f"stamped={stamped}; stamped_failed={stamped_failed}"
        )
        for m in mismatches:
            tag = "FAIL" if m["stamped"] is not None else "info"
            stamp_note = f" [stamped phase {m['stamped']}]" if m["stamped"] is not None else ""
            print(f"  ({tag}) {m['module']}: §00={m['banner']} vs §98 latest={m['latest_release']}{stamp_note}")

    if args.report_only:
        if mismatches and not args.json:
            print("--report-only: not failing.")
        return 0
    # Per-file strict promotion (Phase P20): a stamped §00 with a mismatch
    # always fails, even in default (advisory-tree) mode.
    if stamped_failed > 0:
        if not args.json:
            print(f"FAIL: {stamped_failed} stamped §00 file(s) drift from §98 latest release.")
        return 1
    if args.strict and mismatches:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

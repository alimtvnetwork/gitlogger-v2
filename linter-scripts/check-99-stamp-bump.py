#!/usr/bin/env python3
"""
check-99-stamp-bump.py — enforce that §99 file edits bump the freshness stamp.

Phase H4 (2026-04-28): turns the H1/H2 honor-system into a CI check. When a
§99 file is materially edited (any non-stamp line changed), this validator
verifies that its `<!-- verified-phase: NNN -->` stamp was bumped to the
current phase in the same diff. Catches the failure mode where an author
edits a §99 narrative claim or inventory row but forgets to bump the stamp,
silently leaving the file's claim of freshness misleading.

## How it works

1. Determine current phase from `mem://index.md` / §27 changelog (same logic
   as `check-99-summary-freshness.py` — shares no code but mirrors behavior).
2. Run `git diff --name-only $BASE_REF...HEAD` to find changed §99 files
   (default base ref: `origin/main`, overridable via `--base-ref` or env
   `STAMP_BUMP_BASE_REF`).
3. For each changed §99 file:
   a. If the file has no tracked-heading stamp at all → SKIP (covered by the
      H1/H2 advisory gate; not this gate's concern).
   b. If the only diff lines are the stamp itself → SKIP (pure stamp bump).
   c. If non-stamp lines changed AND the stamp's current phase != current →
      FAIL (or warn in --report-only).
4. Exit 0 if all bumped, 1 if any unbumped (strict), 2 on structural error.

## CLI

    python3 linter-scripts/check-99-stamp-bump.py [--base-ref REF] [--report-only]

## Exit codes

    0 = all materially-edited stamped §99 files have a bumped stamp (or --report-only)
    1 = at least one materially-edited stamped §99 file has a stale stamp
    2 = structural error (cannot determine phase / git missing / no diff base)

## Skip-rule

Files without a tracked-heading stamp are SKIPPED, not failed. Adoption of
H1/H2 stamps is opt-in per file; this gate only enforces "if you stamped, you
must keep it fresh on edit". Once a file is stamped, this gate begins
enforcing it on subsequent edits — natural ratchet.

## Phase H4 design notes

- **Why diff-based not snapshot-based**: the existing freshness gate
  (`check-99-summary-freshness.py`) is snapshot-based with a `--max-age 20`
  budget. This gate is event-based (on edit) with budget=0. Together they
  form a two-layer defense: edits must bump (this gate), and unedited stamps
  decay over time (the freshness gate).
- **`_archive/` excluded** by Phase H3 convention.
- **Single-line stamp diffs are not "material"**: if the only change in a
  §99 file is the stamp line itself, that IS the bump — no failure.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = REPO / "spec"
MEM_INDEX = REPO / ".lovable" / "memory" / "index.md"
CHANGELOG_27 = SPEC / "27-spec-toolchain" / "98-changelog.md"

PHASE_RE = re.compile(r"\bPhase\s+(\d{1,4})\b")
STAMP_RE = re.compile(r"<!--\s*verified-phase:\s*(\d{1,4})\s*-->")
TRACKED_HEADING_RE = re.compile(
    r"^##+\s+(Summary|Module Health|File Inventory|Module Inventory|"
    r"Top-Level Modules|Document Inventory|Modules)\b",
    re.MULTILINE,
)


def detect_current_phase() -> int | None:
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


def find_summary_stamp(text: str) -> int | None:
    """Return the highest stamp under any tracked heading, or None."""
    matches = list(TRACKED_HEADING_RE.finditer(text))
    if not matches:
        return None
    best: int | None = None
    for i, m in enumerate(matches):
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
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


def git_diff_names(base_ref: str) -> list[Path] | None:
    """Return list of §99 files changed between base_ref and HEAD, or None on error."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
            cwd=REPO, stderr=subprocess.PIPE, text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        msg = getattr(e, "stderr", str(e))
        print(f"ERROR: git diff failed against base '{base_ref}': {msg}", file=sys.stderr)
        return None
    files: list[Path] = []
    for line in out.splitlines():
        line = line.strip()
        if not line.endswith("99-consistency-report.md"):
            continue
        p = REPO / line
        if "_archive" in p.parts:
            continue
        if not p.exists():
            continue
        files.append(p)
    return files


def git_diff_lines(base_ref: str, path: Path) -> str | None:
    """Return unified diff for a single file, or None on error."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "-U0", f"{base_ref}...HEAD", "--", str(path.relative_to(REPO))],
            cwd=REPO, stderr=subprocess.PIPE, text=True,
        )
        return out
    except subprocess.CalledProcessError:
        return None


def diff_is_stamp_only(diff_text: str) -> bool:
    """Return True if the only changed lines (+/-) are stamp lines."""
    has_change = False
    for line in diff_text.splitlines():
        if not line:
            continue
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@") or line.startswith("diff "):
            continue
        if line[0] not in "+-":
            continue
        has_change = True
        content = line[1:].strip()
        # Allow empty added/removed lines (whitespace churn around stamp).
        if not content:
            continue
        if not STAMP_RE.search(content):
            return False
    return has_change  # if no changes at all, treat as not-stamp-only (caller handles)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-ref", default=None,
                        help="Git ref to diff against (default: $STAMP_BUMP_BASE_REF or origin/main).")
    parser.add_argument("--report-only", action="store_true",
                        help="Never exit 1; print findings and exit 0.")
    parser.add_argument("--changed-files", default=None,
                        help="Test injection: path to a newline-separated list of §99 files to "
                             "treat as 'changed'. Each file is checked against its committed "
                             "version via git show; if --diff-stamp-only is also passed, the "
                             "file is treated as a stamp-only diff. Bypasses git entirely.")
    parser.add_argument("--treat-as-stamp-only", action="store_true",
                        help="Test injection: treat all --changed-files as stamp-only diffs.")
    args = parser.parse_args()

    base_ref = args.base_ref or os.environ.get("STAMP_BUMP_BASE_REF") or "origin/main"

    current = detect_current_phase()
    if current is None:
        print("ERROR: cannot determine current phase from mem://index.md or §27 changelog.",
              file=sys.stderr)
        return 2

    if args.changed_files:
        # Test-injection path: skip git entirely.
        print(f"Current phase: {current}; mode: --changed-files={args.changed_files}")
        try:
            lines = Path(args.changed_files).read_text().splitlines()
        except OSError as e:
            print(f"ERROR: cannot read --changed-files: {e}", file=sys.stderr)
            return 2
        changed = []
        for line in lines:
            line = line.strip()
            if not line or not line.endswith("99-consistency-report.md"):
                continue
            p = Path(line)
            if not p.is_absolute():
                p = REPO / p
            if "_archive" in p.parts:
                continue
            if p.exists():
                changed.append(p)
    else:
        print(f"Current phase: {current}; base ref: {base_ref}")
        changed = git_diff_names(base_ref)
        if changed is None:
            return 2
    if not changed:
        print("No §99 files changed in diff. ✅")
        return 0

    print(f"Changed §99 files: {len(changed)}")
    skipped_unstamped = 0
    skipped_stamp_only = 0
    bumped_ok = 0
    unbumped: list[tuple[Path, int]] = []

    for f in changed:
        text = f.read_text(encoding="utf-8", errors="ignore")
        stamp = find_summary_stamp(text)
        if stamp is None:
            skipped_unstamped += 1
            continue
        if args.changed_files and args.treat_as_stamp_only:
            stamp_only = True
        else:
            diff = git_diff_lines(base_ref, f) or ""
            stamp_only = diff_is_stamp_only(diff)
        if stamp_only:
            skipped_stamp_only += 1
            continue
        # Material edit. Stamp must equal current phase.
        if stamp == current:
            bumped_ok += 1
        else:
            unbumped.append((f, stamp))

    print(f"  unstamped (skip):     {skipped_unstamped}")
    print(f"  stamp-only diff:      {skipped_stamp_only}")
    print(f"  bumped to current:    {bumped_ok}")
    print(f"  unbumped (issue):     {len(unbumped)}")

    if unbumped:
        print()
        print(f"❌ {len(unbumped)} §99 file(s) materially edited without bumping the stamp:")
        for f, stamp in unbumped:
            rel = f.relative_to(REPO)
            print(f"  - {rel}  [stamp: Phase {stamp}, current: Phase {current}]")
        if args.report_only:
            print()
            print("  --report-only: not failing.")
            return 0
        return 1

    print("✅ All materially-edited stamped §99 files have a bumped stamp.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

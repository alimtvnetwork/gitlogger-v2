#!/usr/bin/env python3
"""
Slot 47 — check-ac-section-orphan-header.py (Gate #28)

Mechanises §22+§23+§24+§25+§26+§27+§28 §97 structural-hygiene floor
(closes §27 backlog `ac-section-orphan-header-check`, minted T-13;
extends with `ac-status-tag-and-parent-taxonomy-check` clauses 4+5,
T-22, Sess-67 G-T-22).

Five load-bearing invariants enforced across every
`97-acceptance-criteria.md` file under the seven in-scope folders:

  clause-1 (no-orphan-ac)        — every `### AC-…` MUST be preceded
                                    by at least one `## ` parent header
                                    earlier in the same file.
  clause-2 (ac-id-uniqueness)    — within a file, every `### AC-…`
                                    AC-ID (first whitespace token after
                                    `### `) MUST be unique.
  clause-3 (section-name-uniqueness)
                                  — within a file, every `## ` heading
                                    title MUST be unique.
  clause-4 (status-tag-vocabulary)
                                  — when an `### AC-…` header carries a
                                    trailing `` `[xxx]` `` status tag,
                                    `xxx` MUST be drawn from the frozen
                                    canonical vocabulary
                                    `STATUS_TAG_VOCABULARY` (Sess-67
                                    G-T-22 anchor). Untagged ACs are
                                    permitted (heterogeneity is real per
                                    T-21 disk survey); only the OPT-IN
                                    tag is validated.
  clause-5 (empty-parent-taxonomy)
                                  — `## ` parents that contain ZERO
                                    `### AC-…` children before the next
                                    `## ` header MUST come from the
                                    frozen `EMPTY_PARENT_ALLOWLIST` (or
                                    one of its prefixes for
                                    parenthetical-suffix variants).
                                    Parents not on the allowlist that
                                    have no AC children are regression
                                    candidates (someone added a section
                                    but never moved an AC under it).

R5 vacuous-pass: if zero §97 files are discovered or zero `### AC-…`
headers are parsed across the seven folders, exit `1` with
`vacuous-pass: zero §97 files or zero AC headers parsed`.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

IN_SCOPE_FOLDERS = [
    "spec/22-git-logs-v2",
    "spec/23-app-database",
    "spec/24-app-design-system-and-ui",
    "spec/25-app-issues",
    "spec/26-gitlogs-diagrams",
    "spec/27-spec-toolchain",
    "spec/28-universal-ci-cli",
]

AC_HEADER_RE = re.compile(r"^###\s+(AC-\S+)")
SECTION_HEADER_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$")
STATUS_TAG_RE = re.compile(r"`\[([a-z]+)\]`")

# Frozen canonical status-tag vocabulary (Sess-67 G-T-22). Adding a new
# tag REQUIRES (a) a row in this tuple, (b) a row in §47 spec doc, and
# (c) a §98 changelog entry. Lesson #15 reflexivity: any new tag without
# a §47 spec-doc row fails the gate the next CI cycle.
STATUS_TAG_VOCABULARY = (
    "active",
    "critical",
    "high",
    "medium",
    "low",
    "deferred",
    "deprecated",
    "draft",
)

# Frozen empty-parent allowlist (Sess-67 G-T-22). Sections matching one
# of these EXACT titles, or starting with one of these prefixes followed
# by " (" (parenthetical-suffix variant — e.g. "Slot Delegation Map
# (Phase 153 Task A24-fu6)"), are permitted to carry zero AC children.
# All other `## ` parents MUST host ≥1 `### AC-…` before the next `## `.
EMPTY_PARENT_ALLOWLIST = (
    "Format",
    "Module Summary",
    "Inlined Contracts",
    "Worked Examples",
    "Cross-References",
    "Purpose",
    "Notes",
    "Legacy Index",
    "Slot Delegation Map",
    "AC Family Prefix Index",
    "Per-artifact criteria",
    "Validation",
    "Test Invariant Index",
)

CHECKS = (
    "all",
    "no-orphan-ac",
    "ac-id-uniqueness",
    "section-name-uniqueness",
    "status-tag-vocabulary",
    "empty-parent-taxonomy",
)


def _is_empty_parent_allowed(title: str) -> bool:
    if title in EMPTY_PARENT_ALLOWLIST:
        return True
    for pfx in EMPTY_PARENT_ALLOWLIST:
        if title.startswith(pfx + " ("):
            return True
    return False



def discover_files(root: Path) -> List[Path]:
    out = []
    for folder in IN_SCOPE_FOLDERS:
        p = root / folder / "97-acceptance-criteria.md"
        if p.is_file():
            out.append(p)
    return out


def scan_file(path: Path) -> Tuple[List[str], int]:
    """Return (violations, ac_count) for a single §97 file."""
    violations: List[str] = []
    ac_count = 0
    seen_section = False
    section_titles: dict[str, List[int]] = {}
    ac_ids: dict[str, List[int]] = {}
    # parents: list of (title, lineno, ac_child_count)
    parents: List[List] = []

    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        sm = SECTION_HEADER_RE.match(line)
        if sm and not line.startswith("### "):
            seen_section = True
            title = sm.group(1).strip()
            section_titles.setdefault(title, []).append(lineno)
            parents.append([title, lineno, 0])
            continue
        am = AC_HEADER_RE.match(line)
        if am:
            ac_count += 1
            ac_id = am.group(1).rstrip(":").rstrip(",")
            ac_ids.setdefault(ac_id, []).append(lineno)
            if parents:
                parents[-1][2] += 1
            if not seen_section:
                violations.append(
                    f"{path}:{lineno}: clause-1 orphan-ac: `{ac_id}` "
                    f"declared before any `## ` parent section header"
                )
            # clause-4: validate any opt-in status tag
            tm = STATUS_TAG_RE.search(line)
            if tm and tm.group(1) not in STATUS_TAG_VOCABULARY:
                violations.append(
                    f"{path}:{lineno}: clause-4 status-tag-vocabulary: "
                    f"`{ac_id}` carries unknown status tag "
                    f"`[{tm.group(1)}]` (allowed: "
                    f"{', '.join('[' + t + ']' for t in STATUS_TAG_VOCABULARY)})"
                )

    for ac_id, lines in ac_ids.items():
        if len(lines) > 1:
            violations.append(
                f"{path}:{lines[1]}: clause-2 ac-id-duplicate: `{ac_id}` "
                f"appears at lines {lines}"
            )
    for title, lines in section_titles.items():
        if len(lines) > 1:
            violations.append(
                f"{path}:{lines[1]}: clause-3 section-name-duplicate: "
                f"`## {title}` appears at lines {lines}"
            )
    # clause-5: empty-parent taxonomy
    for title, lineno, ac_count_in in parents:
        if ac_count_in == 0 and not _is_empty_parent_allowed(title):
            violations.append(
                f"{path}:{lineno}: clause-5 empty-parent-taxonomy: "
                f"`## {title}` carries zero `### AC-…` children and is "
                f"not on the EMPTY_PARENT_ALLOWLIST "
                f"(regression candidate — either add an AC under it or "
                f"add `{title}` to the frozen allowlist with rationale)"
            )
    return violations, ac_count


def filter_violations(violations: List[str], check: str) -> List[str]:
    if check == "all":
        return violations
    keymap = {
        "no-orphan-ac": "clause-1",
        "ac-id-uniqueness": "clause-2",
        "section-name-uniqueness": "clause-3",
        "status-tag-vocabulary": "clause-4",
        "empty-parent-taxonomy": "clause-5",
    }
    needle = keymap[check]
    return [v for v in violations if needle in v]



def run_disk(check: str, root: Path) -> int:
    files = discover_files(root)
    if not files:
        print(
            "vacuous-pass: zero §97 files or zero AC headers parsed",
            file=sys.stderr,
        )
        return 1
    all_violations: List[str] = []
    total_ac = 0
    for f in files:
        viols, count = scan_file(f)
        total_ac += count
        all_violations.extend(viols)
    if total_ac == 0:
        print(
            "vacuous-pass: zero §97 files or zero AC headers parsed",
            file=sys.stderr,
        )
        return 1
    filtered = filter_violations(all_violations, check)
    if filtered:
        for v in filtered:
            print(v, file=sys.stderr)
        print(
            f"check-ac-section-orphan-header: {len(filtered)} violation(s) "
            f"across {len(files)} §97 file(s) ({total_ac} ACs scanned, "
            f"check={check})",
            file=sys.stderr,
        )
        return 1
    print(
        f"check-ac-section-orphan-header: OK — {len(files)} §97 file(s), "
        f"{total_ac} ACs, check={check}"
    )
    return 0


# ---------- self-test fixtures ----------

F1 = """# AC
## Group A
### AC-01 — Alpha
### AC-02 — Beta
## Group B
### AC-03 — Gamma
"""
F2 = """# AC
### AC-01 — orphan
## Later
### AC-02 — fine
"""
F3 = """# AC
## Group A
### AC-04 — first
### AC-04 — duplicate
"""
F4 = """# AC
## Mutations
### AC-01 — a
## Mutations
### AC-02 — b
"""
F5 = """# Empty file with no ACs and no sections
"""
# F-6: clause-4 status-tag-vocabulary failure (unknown `[wip]` tag)
F6 = """# AC
## Group A
### AC-01 — Alpha  `[critical]`
### AC-02 — Beta  `[wip]`
"""
# F-7: clause-5 empty-parent-taxonomy failure (`## Mutations` has no
# AC children and is NOT on the EMPTY_PARENT_ALLOWLIST)
F7 = """# AC
## Group A
### AC-01 — Alpha
## Mutations
## Group B
### AC-02 — Beta
"""
# F-8: clause-4 + clause-5 happy path (allowlist parent + canonical tag)
F8 = """# AC
## Module Summary
## Group A
### AC-01 — Alpha  `[critical]`
### AC-02 — Beta  `[active]`
## Cross-References
"""


def self_test() -> int:
    cases = [
        ("F-1", F1, True),
        ("F-2", F2, False),
        ("F-3", F3, False),
        ("F-4", F4, False),
        ("F-5", F5, False),
        ("F-6", F6, False),
        ("F-7", F7, False),
        ("F-8", F8, True),
    ]
    failures: List[str] = []
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        for name, body, should_pass in cases:
            # build a minimal in-scope tree with a single §97 file
            root = tdp / name
            for folder in IN_SCOPE_FOLDERS:
                (root / folder).mkdir(parents=True, exist_ok=True)
            target = root / IN_SCOPE_FOLDERS[0] / "97-acceptance-criteria.md"
            target.write_text(body, encoding="utf-8")
            # silence stdout/stderr during fixture run
            saved_out, saved_err = sys.stdout, sys.stderr
            sys.stdout = open(os.devnull, "w")
            sys.stderr = open(os.devnull, "w")
            try:
                rc = run_disk("all", root)
            finally:
                sys.stdout.close()
                sys.stderr.close()
                sys.stdout, sys.stderr = saved_out, saved_err
            passed = rc == 0
            if passed != should_pass:
                failures.append(
                    f"{name}: expected {'pass' if should_pass else 'fail'}, "
                    f"got rc={rc}"
                )
    if failures:
        for f in failures:
            print(f"self-test FAIL: {f}", file=sys.stderr)
        return 3
    print("check-ac-section-orphan-header: self-test OK (8 fixtures)")
    return 0



def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", choices=CHECKS, default="all")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--root", default=".")
    args = p.parse_args()
    if args.self_test:
        return self_test()
    return run_disk(args.check, Path(args.root))


if __name__ == "__main__":
    sys.exit(main())

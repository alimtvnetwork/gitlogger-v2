#!/usr/bin/env python3
"""
Slot 48 — check-ac-prefix-contract.py (Gate #29)

Mechanises §22+§23+§24+§25+§26+§27+§28 §97 cross-folder AC-prefix
ownership contract (closes §27 backlog `ac-prefix-contract-check`,
minted T-14). Cross-file complement to slot 47's within-file gate.

Five clauses (see slot doc):
  clause-1 owner-folder           — every `### AC-…` header in any
                                    §97 file MUST match its folder's
                                    owned-root set.
  clause-2 no-cross-folder-collision
                                  — every fully-qualified `AC-…` ID
                                    MUST be unique across the seven
                                    §97 files (excluding the bare-
                                    numeric grandfathered baseline).
  clause-3 bare-numeric-partition — bare-numeric `AC-NN` integers
                                    MUST NOT collide across §22/§25/§26
                                    beyond the T-22 baseline whitelist.
  clause-4 no-foreign-in-meta     — §00/§98/§99 files in any folder
                                    MUST NOT declare a `### AC-…`
                                    header whose prefix is NOT owned
                                    by that folder.
  clause-5 ownership-map-round-trip
                                  — every prefix-root present on disk
                                    MUST appear in this script's
                                    OWNED_ROOTS table (kept in lockstep
                                    with slot doc 48 ownership map).

R5 vacuous-pass: zero §97 files OR zero `### AC-…` headers parsed
across the seven folders → exit 1.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ---------- ownership map (mirror of slot doc 48 table) ----------

# Each folder maps to a list of (label, predicate) pairs. The predicate
# takes the AC-ID body (everything after the leading "AC-") and returns
# True when the AC is in the folder's owned set.

BARE_RE = re.compile(r"^\d+$")
F22_CE_RE = re.compile(r"^22-CE\d+$")
F22_LV_RE = re.compile(r"^22-LV\d+$")
F22_COHORT_RE = re.compile(r"^COHORT-\d+$")
F28_RE = re.compile(r"^28-\d+$")
F23_ADB_RE = re.compile(r"^ADB(-[A-Za-z0-9]+)+$")  # ADB-NN, ADB-REST-NN, ADB-SETTING-NN
F24_ADS_RE = re.compile(r"^ADS(-[A-Za-z0-9]+)+$")
F24_CAF_RE = re.compile(r"^CAF-\d+$")
F25_AI_RE = re.compile(r"^AI(-[A-Za-z0-9]+)+$")
F26_DG_RE = re.compile(r"^DG(-[A-Za-z0-9]+)+$")
F27_T_RE = re.compile(r"^T(-[A-Za-z0-9]+)+$")

OWNED: Dict[str, List[Tuple[str, "re.Pattern[str]"]]] = {
    "spec/22-git-logs-v2": [
        ("AC-NN (bare)", BARE_RE),
        ("AC-22-CE", F22_CE_RE),
        ("AC-22-LV", F22_LV_RE),
        ("AC-COHORT-", F22_COHORT_RE),
    ],
    "spec/23-app-database": [("AC-ADB-*", F23_ADB_RE)],
    "spec/24-app-design-system-and-ui": [
        ("AC-ADS-*", F24_ADS_RE),
        ("AC-CAF-NN", F24_CAF_RE),
    ],
    "spec/25-app-issues": [
        ("AC-AI-*", F25_AI_RE),
        ("AC-NN (bare)", BARE_RE),
    ],
    "spec/26-gitlogs-diagrams": [
        ("AC-DG-*", F26_DG_RE),
        ("AC-NN (bare)", BARE_RE),
    ],
    "spec/27-spec-toolchain": [("AC-T-*", F27_T_RE)],
    "spec/28-universal-ci-cli": [("AC-28-*", F28_RE)],
}

IN_SCOPE_FOLDERS = list(OWNED.keys())

# All known prefix-root tokens (clause-5 round-trip). A "root token"
# is the second dash-segment of the AC-ID (or "BARE" if the body is
# pure digits). Anything not in this set is an unknown-prefix mint.
KNOWN_ROOTS: Set[str] = {
    "BARE",
    "22-CE",
    "22-LV",
    "COHORT",
    "ADB",
    "ADS",
    "CAF",
    "AI",
    "DG",
    "T",
    "28",
}

# T-22 grandfathered bare-numeric collision baseline.
BARE_BASELINE_COLLISIONS: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 22, 23, 24, 25, 26}

AC_HEADER_RE = re.compile(r"^###\s+(AC-[A-Za-z0-9-]+?)(?=[\s:—,]|$)")

CHECKS = (
    "all",
    "owner-folder",
    "no-cross-folder-collision",
    "bare-numeric-partition",
    "no-foreign-in-meta",
    "ownership-map-round-trip",
)

META_FILES = ("00-overview.md", "98-changelog.md", "99-consistency-report.md")


def root_token(ac_body: str) -> str:
    """Return the prefix-root token for clause-5 round-trip.

    `ac_body` is the AC-ID with the leading "AC-" stripped.
    """
    if BARE_RE.match(ac_body):
        return "BARE"
    # 22-CE\d+ / 22-LV\d+ are special two-token roots
    if F22_CE_RE.match(ac_body):
        return "22-CE"
    if F22_LV_RE.match(ac_body):
        return "22-LV"
    if ac_body.startswith("28-"):
        return "28"
    # Otherwise the root is the first dash-segment.
    head = ac_body.split("-", 1)[0]
    return head


def is_owned(folder: str, ac_body: str) -> bool:
    for _, pat in OWNED[folder]:
        if pat.match(ac_body):
            return True
    return False


def parse_headers(path: Path) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = AC_HEADER_RE.match(line)
        if m:
            out.append((lineno, m.group(1).rstrip(":,;")))
    return out


def discover_97(root: Path) -> List[Tuple[str, Path]]:
    out = []
    for folder in IN_SCOPE_FOLDERS:
        p = root / folder / "97-acceptance-criteria.md"
        if p.is_file():
            out.append((folder, p))
    return out


def discover_meta(root: Path) -> List[Tuple[str, Path]]:
    out = []
    for folder in IN_SCOPE_FOLDERS:
        for fname in META_FILES:
            p = root / folder / fname
            if p.is_file():
                out.append((folder, p))
    return out


def run_disk(check: str, root: Path) -> int:
    files_97 = discover_97(root)
    if not files_97:
        print(
            "vacuous-pass: zero §97 files or zero AC headers parsed",
            file=sys.stderr,
        )
        return 1

    violations: List[str] = []
    total_ac = 0
    # Map ac_id -> [(folder, file, line)] for clause-2 collision check.
    global_ids: Dict[str, List[Tuple[str, Path, int]]] = {}
    # Map bare-int -> [(folder, file, line)] for clause-3.
    bare_ints: Dict[int, List[Tuple[str, Path, int]]] = {}
    # All discovered roots for clause-5.
    seen_roots: Dict[str, List[Tuple[str, Path, int, str]]] = {}

    for folder, path in files_97:
        for lineno, ac_id in parse_headers(path):
            total_ac += 1
            body = ac_id[len("AC-"):] if ac_id.startswith("AC-") else ac_id

            # clause-1
            if not is_owned(folder, body):
                violations.append(
                    f"{path}:{lineno}: clause-1 owner-folder: `{ac_id}` "
                    f"is not in {folder}'s owned-root set "
                    f"({', '.join(label for label, _ in OWNED[folder])})"
                )

            # clause-5 root tracking
            rt = root_token(body)
            seen_roots.setdefault(rt, []).append((folder, path, lineno, ac_id))

            # clause-2 collision tracking
            global_ids.setdefault(ac_id, []).append((folder, path, lineno))

            # clause-3 bare-numeric tracking
            if BARE_RE.match(body):
                bare_ints.setdefault(int(body), []).append((folder, path, lineno))

    if total_ac == 0:
        print(
            "vacuous-pass: zero §97 files or zero AC headers parsed",
            file=sys.stderr,
        )
        return 1

    # clause-2: cross-folder collisions (bare-numeric collisions handled
    # by clause-3; here we flag NON-bare collisions across folders).
    for ac_id, occs in global_ids.items():
        body = ac_id[len("AC-"):]
        if BARE_RE.match(body):
            continue  # clause-3 territory
        folders = {f for f, _, _ in occs}
        if len(occs) > 1:
            locs = ", ".join(f"{p}:{ln}" for _, p, ln in occs)
            if len(folders) > 1:
                violations.append(
                    f"clause-2 no-cross-folder-collision: `{ac_id}` "
                    f"declared in multiple folders at {locs}"
                )
            else:
                # within-file or within-folder dup — gate #28 territory,
                # but flag too for cross-file uniqueness completeness.
                violations.append(
                    f"clause-2 no-cross-folder-collision: `{ac_id}` "
                    f"declared more than once at {locs}"
                )

    # clause-3: bare-numeric partition
    for n, occs in bare_ints.items():
        folders = {f for f, _, _ in occs}
        if len(folders) > 1 and n not in BARE_BASELINE_COLLISIONS:
            locs = ", ".join(f"{p}:{ln}" for _, p, ln in occs)
            violations.append(
                f"clause-3 bare-numeric-partition: `AC-{n}` declared "
                f"across folders {sorted(folders)} at {locs} (NOT in "
                f"T-22 grandfathered baseline {sorted(BARE_BASELINE_COLLISIONS)})"
            )

    # clause-5: ownership-map round-trip
    for rt, occs in seen_roots.items():
        if rt not in KNOWN_ROOTS:
            sample = occs[0]
            violations.append(
                f"{sample[1]}:{sample[2]}: clause-5 ownership-map-round-trip: "
                f"unknown-prefix root `AC-{rt}-` from `{sample[3]}` not in "
                f"slot 48 ownership map (KNOWN_ROOTS={sorted(KNOWN_ROOTS)})"
            )

    # clause-4: foreign-prefix declaration in §00/§98/§99
    for folder, path in discover_meta(root):
        for lineno, ac_id in parse_headers(path):
            body = ac_id[len("AC-"):] if ac_id.startswith("AC-") else ac_id
            if not is_owned(folder, body):
                violations.append(
                    f"{path}:{lineno}: clause-4 no-foreign-in-meta: "
                    f"`### {ac_id}` declared in {path.name} but `{ac_id}` "
                    f"is not owned by {folder}"
                )

    # filter
    if check != "all":
        keymap = {
            "owner-folder": "clause-1",
            "no-cross-folder-collision": "clause-2",
            "bare-numeric-partition": "clause-3",
            "no-foreign-in-meta": "clause-4",
            "ownership-map-round-trip": "clause-5",
        }
        needle = keymap[check]
        violations = [v for v in violations if needle in v]

    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        print(
            f"check-ac-prefix-contract: {len(violations)} violation(s) "
            f"across {len(files_97)} §97 file(s) ({total_ac} ACs scanned, "
            f"check={check})",
            file=sys.stderr,
        )
        return 1
    print(
        f"check-ac-prefix-contract: OK — {len(files_97)} §97 file(s), "
        f"{total_ac} ACs, {len(seen_roots)} prefix-root(s), check={check}"
    )
    return 0


# ---------- self-test ----------

def _scaffold_root(td: Path, files: Dict[str, str]) -> Path:
    """Create the seven in-scope folders under td and write provided files."""
    for folder in IN_SCOPE_FOLDERS:
        (td / folder).mkdir(parents=True, exist_ok=True)
        (td / folder / "97-acceptance-criteria.md").write_text(
            "# AC\n## Group A\n", encoding="utf-8"
        )
    for rel, body in files.items():
        target = td / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return td


def _run_silent(root: Path) -> int:
    saved_out, saved_err = sys.stdout, sys.stderr
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    try:
        return run_disk("all", root)
    finally:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout, sys.stderr = saved_out, saved_err


def self_test() -> int:
    cases = []

    # F-1 complete-uniform passing
    cases.append(("F-1", {
        "spec/22-git-logs-v2/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-100 — bare\n### AC-22-CE9 — coh\n",
        "spec/23-app-database/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-ADB-77 — db\n### AC-ADB-REST-08 — sub\n",
        "spec/24-app-design-system-and-ui/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-ADS-09 — ui\n### AC-CAF-09 — caf\n",
        "spec/25-app-issues/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-AI-99 — ai\n",
        "spec/26-gitlogs-diagrams/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-DG-99 — dg\n",
        "spec/27-spec-toolchain/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-T-99 — t\n",
        "spec/28-universal-ci-cli/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-28-99 — cli\n",
    }, True))

    # F-2 §23 declares AC-ADS-99 → clause-1 fail
    cases.append(("F-2", {
        "spec/23-app-database/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-ADS-99 — foreign\n",
    }, False))

    # F-3 bare-numeric collision OUTSIDE baseline (AC-50 in §22 + §25)
    cases.append(("F-3", {
        "spec/22-git-logs-v2/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-50 — bare22\n",
        "spec/25-app-issues/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-50 — bare25\n",
    }, False))

    # F-4 cross-folder non-bare collision: AC-T-15 in both §27 and §28 §97
    # (impossible because §28 doesn't own AC-T-, so this also trips
    # clause-1 on §28 — gate fails either way)
    cases.append(("F-4", {
        "spec/27-spec-toolchain/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-T-15 — first\n",
        "spec/28-universal-ci-cli/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-T-15 — collide\n### AC-28-77 — own\n",
    }, False))

    # F-5 §24 §00 declares AC-AI-42 (foreign in meta) → clause-4 fail
    cases.append(("F-5", {
        "spec/24-app-design-system-and-ui/00-overview.md":
            "# Overview\n## Section\n### AC-AI-42 — foreign meta\n",
        # ensure §97 files have at least one valid AC so R5 passes
        "spec/22-git-logs-v2/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-100 — bare\n",
    }, False))

    # F-6 unknown prefix root → clause-5
    cases.append(("F-6", {
        "spec/22-git-logs-v2/97-acceptance-criteria.md":
            "# AC\n## Group\n### AC-FOO-01 — unknown\n",
    }, False))

    failures: List[str] = []
    with tempfile.TemporaryDirectory() as parent:
        for name, files, should_pass in cases:
            td = Path(parent) / name
            td.mkdir(parents=True, exist_ok=True)
            _scaffold_root(td, files)
            rc = _run_silent(td)
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
    print("check-ac-prefix-contract: self-test OK (6 fixtures)")
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

#!/usr/bin/env python3
"""Slot 39 — check-applink-xor-clause.py (gate #22 / Phase-5 T-15).

Promotes spec/23 AC-ADB-05 + AC-ADB-13 from contract-proven to load-proven.

Walks the canonical §23 contract (`spec/23-app-database/00-overview.md`) AND
the §22 DDL mirror (`spec/22-git-logs-v2/18-schema.sql`) in lockstep —
asserts the AppLink XOR + disconnect-invariant + locked-ID seed +
partial-index invariants byte-for-byte against EVERY known source so
the §22 mirror cannot drift from the §23 contract (Sess-67 G-6w-mirror —
mirror coverage promoted from deferred to load-proven; the §22 schema was
rebased to TargetGitProfileId/TargetRepoId + IsActive/DisconnectedAt in
the same PR that lit up `--all-sources`).

Use `--source <path>` to scan a single file (default: §23 §00) or
`--all-sources` to walk every entry in `MIRROR_SOURCES` and fail on the
first divergence. CI wires both: a single-source `--self-test` plus a
live `--all-sources` run; either failing hard-fails the gate.

Self-test: 6 in-memory fixtures (F-1..F-6) cover all four clauses + R5
vacuous-pass anchor.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC23_OVERVIEW = REPO / "spec" / "23-app-database" / "00-overview.md"
SPEC22_SCHEMA   = REPO / "spec" / "22-git-logs-v2" / "18-schema.sql"

# Lockstep mirror set. Both files MUST satisfy the same 4-clause contract.
# Adding a new mirror requires (a) appending here, (b) §27 §98 changelog row,
# (c) re-running --self-test (must stay 6/6) AND --all-sources clean.
MIRROR_SOURCES: tuple[Path, ...] = (SPEC23_OVERVIEW, SPEC22_SCHEMA)

# AppLink CREATE TABLE block detector
APPLINK_BLOCK_RE = re.compile(
    r"CREATE TABLE IF NOT EXISTS AppLink\s*\((.*?)^\s*\)\s*;",
    re.DOTALL | re.MULTILINE,
)

# Clause-1 — XOR CHECK pattern (two SELECT-discriminator disjuncts joined by OR).
XOR_GITPROFILE_RE = re.compile(
    r"AppLinkTypeId\s*=\s*\(\s*SELECT\s+AppLinkTypeId\s+FROM\s+AppLinkType\s+WHERE\s+Name\s*=\s*'GitProfile'\s*\)\s*"
    r"AND\s+TargetGitProfileId\s+IS\s+NOT\s+NULL\s+AND\s+TargetRepoId\s+IS\s+NULL",
    re.IGNORECASE | re.DOTALL,
)
XOR_REPO_RE = re.compile(
    r"AppLinkTypeId\s*=\s*\(\s*SELECT\s+AppLinkTypeId\s+FROM\s+AppLinkType\s+WHERE\s+Name\s*=\s*'Repo'\s*\)\s*"
    r"AND\s+TargetRepoId\s+IS\s+NOT\s+NULL\s+AND\s+TargetGitProfileId\s+IS\s+NULL",
    re.IGNORECASE | re.DOTALL,
)

# Clause-2 — Disconnect-invariant CHECK.
DISCONNECT_ACTIVE_RE = re.compile(
    r"IsActive\s*=\s*1\s+AND\s+DisconnectedAt\s+IS\s+NULL", re.IGNORECASE
)
DISCONNECT_INACTIVE_RE = re.compile(
    r"IsActive\s*=\s*0\s+AND\s+DisconnectedAt\s+IS\s+NOT\s+NULL", re.IGNORECASE
)

# Clause-3 — Locked-ID seed.
SEED_LOCKED_RE = re.compile(
    r"INSERT\s+OR\s+IGNORE\s+INTO\s+AppLinkType\s*\(\s*AppLinkTypeId\s*,\s*Name\s*\)\s+VALUES\s*"
    r"\(\s*1\s*,\s*'GitProfile'\s*\)\s*,\s*\(\s*2\s*,\s*'Repo'\s*\)",
    re.IGNORECASE,
)
SEED_BARE_RE = re.compile(
    r"INSERT\s+(?:OR\s+IGNORE\s+)?INTO\s+AppLinkType\s*\(\s*Name\s*\)\s+VALUES\s*"
    r"\(\s*'GitProfile'\s*\)\s*,\s*\(\s*'Repo'\s*\)",
    re.IGNORECASE,
)

# Clause-4 — Partial indexes on both target columns.
IX_REPO_RE = re.compile(
    r"CREATE\s+INDEX\s+IF\s+NOT\s+EXISTS\s+IX_AppLink_TargetRepoId\s+ON\s+AppLink\s*\(\s*TargetRepoId\s*\)\s+WHERE\s+TargetRepoId\s+IS\s+NOT\s+NULL",
    re.IGNORECASE,
)
IX_GP_RE = re.compile(
    r"CREATE\s+INDEX\s+IF\s+NOT\s+EXISTS\s+IX_AppLink_TargetGitProfileId\s+ON\s+AppLink\s*\(\s*TargetGitProfileId\s*\)\s+WHERE\s+TargetGitProfileId\s+IS\s+NOT\s+NULL",
    re.IGNORECASE,
)


def check_xor(block: str) -> list[str]:
    errs = []
    if not XOR_GITPROFILE_RE.search(block):
        errs.append("clause-1: GitProfile XOR disjunct missing or malformed")
    if not XOR_REPO_RE.search(block):
        errs.append("clause-1: Repo XOR disjunct missing or malformed")
    if errs:
        return errs
    # Reject AND-joined or 3+ disjuncts: count occurrences of the two patterns
    # and ensure they are joined by OR (not AND) within the same CHECK.
    # Heuristic: between the two disjunct anchors there must be an `OR` token,
    # not `AND`.
    gp = XOR_GITPROFILE_RE.search(block)
    rp = XOR_REPO_RE.search(block)
    a, b = sorted([gp.span(), rp.span()])
    bridge = block[a[1]:b[0]]
    if not re.search(r"\)\s*OR\s*\(", bridge, re.IGNORECASE):
        errs.append("clause-1: XOR disjuncts not joined by `OR` (found AND or other connector)")
    return errs


def check_disconnect(block: str) -> list[str]:
    errs = []
    if not DISCONNECT_ACTIVE_RE.search(block):
        errs.append("clause-2: disconnect-invariant active disjunct (`IsActive=1 AND DisconnectedAt IS NULL`) missing")
    if not DISCONNECT_INACTIVE_RE.search(block):
        errs.append("clause-2: disconnect-invariant inactive disjunct (`IsActive=0 AND DisconnectedAt IS NOT NULL`) missing")
    return errs


def check_seed(text: str) -> list[str]:
    errs = []
    if SEED_BARE_RE.search(text) and not SEED_LOCKED_RE.search(text):
        errs.append("clause-3: bare AppLinkType seed without explicit (1,'GitProfile'),(2,'Repo') IDs (T-10/WE-2)")
        return errs
    if not SEED_LOCKED_RE.search(text):
        errs.append("clause-3: locked-ID AppLinkType seed `INSERT OR IGNORE … VALUES (1,'GitProfile'),(2,'Repo')` missing (AC-ADB-13)")
    return errs


def check_indexes(text: str) -> list[str]:
    errs = []
    if not IX_REPO_RE.search(text):
        errs.append("clause-4: partial index `IX_AppLink_TargetRepoId … WHERE TargetRepoId IS NOT NULL` missing")
    if not IX_GP_RE.search(text):
        errs.append("clause-4: partial index `IX_AppLink_TargetGitProfileId … WHERE TargetGitProfileId IS NOT NULL` missing")
    return errs


def run_against(text: str, which: str = "all") -> list[str]:
    blocks = APPLINK_BLOCK_RE.findall(text)
    if not blocks:
        # R5 anchor — vacuous-pass guard
        return ["vacuous-pass: zero `CREATE TABLE … AppLink` DDL blocks found"]
    block = blocks[0]
    errs: list[str] = []
    if which in ("all", "xor"):
        errs.extend(check_xor(block))
    if which in ("all", "disconnect"):
        errs.extend(check_disconnect(block))
    if which in ("all", "seed-ids"):
        errs.extend(check_seed(text))
    if which in ("all", "indexes"):
        errs.extend(check_indexes(text))
    return errs


# ---------------- Self-test ----------------

F1_COMPLETE = """
```sql
CREATE TABLE IF NOT EXISTS AppLink (
  AppLinkId INTEGER PRIMARY KEY AUTOINCREMENT,
  AppLinkTypeId INTEGER NOT NULL,
  TargetGitProfileId INTEGER NULL,
  TargetRepoId INTEGER NULL,
  IsActive INTEGER NOT NULL,
  DisconnectedAt INTEGER NULL,
  CHECK (
    (AppLinkTypeId = (SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'GitProfile')
       AND TargetGitProfileId IS NOT NULL AND TargetRepoId IS NULL)
    OR
    (AppLinkTypeId = (SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'Repo')
       AND TargetRepoId IS NOT NULL AND TargetGitProfileId IS NULL)
  ),
  CHECK (
    (IsActive = 1 AND DisconnectedAt IS NULL)
    OR
    (IsActive = 0 AND DisconnectedAt IS NOT NULL)
  )
);
INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo');
CREATE INDEX IF NOT EXISTS IX_AppLink_TargetRepoId ON AppLink(TargetRepoId) WHERE TargetRepoId IS NOT NULL;
CREATE INDEX IF NOT EXISTS IX_AppLink_TargetGitProfileId ON AppLink(TargetGitProfileId) WHERE TargetGitProfileId IS NOT NULL;
```
"""


def self_test() -> int:
    cases = []
    cases.append(("F-1 complete", True, None, F1_COMPLETE))

    # Replace the OR between the two XOR disjuncts with AND (first OR only).
    f2 = re.sub(r"IS NULL\)\s*\n\s*OR\s*\n\s*\(AppLinkTypeId = \(SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'Repo'",
                "IS NULL)\n    AND\n    (AppLinkTypeId = (SELECT AppLinkTypeId FROM AppLinkType WHERE Name = 'Repo'",
                F1_COMPLETE, count=1)
    cases.append(("F-2 XOR weakened to AND", False, "clause-1", f2))

    f3 = F1_COMPLETE.replace(
        "INSERT OR IGNORE INTO AppLinkType(AppLinkTypeId, Name) VALUES (1,'GitProfile'),(2,'Repo');",
        "INSERT OR IGNORE INTO AppLinkType(Name) VALUES ('GitProfile'),('Repo');",
    )
    cases.append(("F-3 bare seed", False, "clause-3", f3))

    f4 = F1_COMPLETE.replace(
        "CREATE INDEX IF NOT EXISTS IX_AppLink_TargetRepoId ON AppLink(TargetRepoId) WHERE TargetRepoId IS NOT NULL;",
        "CREATE INDEX IF NOT EXISTS IX_AppLink_TargetRepoId ON AppLink(TargetRepoId);",
    )
    cases.append(("F-4 IX_TargetRepoId WHERE stripped", False, "clause-4", f4))

    f5 = re.sub(
        r"CHECK \(\s*\(IsActive = 1[^)]*\)\s*OR\s*\(IsActive = 0[^)]*\)\s*\)",
        "",
        F1_COMPLETE,
        flags=re.DOTALL,
    )
    cases.append(("F-5 disconnect CHECK absent", False, "clause-2", f5))

    cases.append(("F-6 R5 vacuous-pass empty", False, "vacuous-pass", ""))

    fails = 0
    for name, should_pass, expect, body in cases:
        errs = run_against(body)
        if should_pass and errs:
            print(f"FAIL {name}: expected pass, got: {errs}"); fails += 1
        elif not should_pass:
            if not errs:
                print(f"FAIL {name}: expected failure ({expect}), got pass"); fails += 1
            elif not any(expect in e for e in errs):
                print(f"FAIL {name}: expected {expect}, got: {errs}"); fails += 1
            else:
                print(f"ok  {name} ({expect})")
        else:
            print(f"ok  {name}")
    if fails:
        print(f"\n--self-test: {fails} fixture(s) failed", file=sys.stderr)
        return 1
    print(f"\n--self-test: {len(cases)}/{len(cases)} fixtures passed")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", default="all",
                    choices=["all", "xor", "disconnect", "seed-ids", "indexes"])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source", default=str(SPEC23_OVERVIEW),
                    help="Spec source to scan (default: spec/23-app-database/00-overview.md)")
    ap.add_argument("--all-sources", action="store_true",
                    help="Walk every entry in MIRROR_SOURCES (§23 contract + §22 mirror); "
                         "fail on the first divergence. Lockstep enforcement of G-6w-mirror.")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    sources = list(MIRROR_SOURCES) if args.all_sources else [Path(args.source)]
    total_errs = 0
    for src in sources:
        if not src.exists():
            print(f"FAIL: source not found: {src}", file=sys.stderr)
            total_errs += 1
            continue
        text = src.read_text(encoding="utf-8")
        errs = run_against(text, args.check)
        if errs:
            for e in errs:
                print(f"FAIL [{src.relative_to(REPO)}]: {e}")
            total_errs += len(errs)
        else:
            print(f"OK: AppLink XOR clause gate clean on {src.relative_to(REPO)} (--check={args.check})")
    return 1 if total_errs else 0


if __name__ == "__main__":
    sys.exit(main())

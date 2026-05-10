#!/usr/bin/env python3
"""Slot 59 — check-no-ci-yaml-in-issues-folder.py (gate #37 / Phase-5 T-30).

Asserts §25 folder owns ZERO CI workflow surface. Single source of truth
for CI workflows is §27 + §28. See spec/27-spec-toolchain/59-check-no-ci-yaml-in-issues-folder.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ISSUES_DIR = REPO / "spec" / "25-app-issues"
OVERVIEW = ISSUES_DIR / "00-overview.md"

YAML_FENCE_RE = re.compile(r"^[ ]{0,3}```\s*(yaml|yml)\b", re.IGNORECASE)
FENCE_OPEN_RE = re.compile(r"^[ ]{0,3}```")
CI_BODY_TOKENS = (
    "runs-on:",
    "uses: actions/",
)
CI_BODY_TOPLEVEL = re.compile(r"^(jobs|on):\s*$", re.MULTILINE)
CI_ON_TRIGGERS = ("on: push", "on: pull_request", "on: schedule")

YML_PATH_RE = re.compile(
    r"spec/25-[A-Za-z0-9_-]+/(workflows|ci|github)/[A-Za-z0-9_./-]+\.ya?ml",
    re.IGNORECASE,
)
OWNERSHIP_VERBS = ("owned by §25", "defined in §25", "ships from §25")

BARE_CI_LITERALS = (
    "runs-on: ubuntu-latest",
    "uses: actions/checkout@",
)
BOUNDARY_LITERALS = (
    "CI-workflow YAML is owned exclusively by §27",
    "Self-enforcing via §27 backlog gate `no-ci-yaml-in-issues-folder-check`",
)
GATE_NAME_RE = re.compile(r"`check-[a-z][a-z0-9-]+`")
INLINE_BACKTICKS = re.compile(r"`+[^`\n]*`+")


def strip_inline(s: str) -> str:
    return INLINE_BACKTICKS.sub(" ", s)


def scan_files(paths):
    return {p: p.read_text(encoding="utf-8").splitlines() for p in paths}


def is_ci_workflow_body(body_lines: list[str]) -> tuple[bool, str]:
    body = "\n".join(body_lines)
    for tok in CI_BODY_TOKENS:
        if tok in body:
            return True, tok
    if CI_BODY_TOPLEVEL.search(body):
        return True, "jobs:/on: top-level"
    for tok in CI_ON_TRIGGERS:
        if tok in body:
            return True, tok
    return False, ""


def check_no_ci_yaml_fences(files):
    errs = []
    for p, lines in files.items():
        i = 0
        while i < len(lines):
            ln = lines[i]
            if YAML_FENCE_RE.match(ln):
                start = i + 1
                j = start
                while j < len(lines) and not FENCE_OPEN_RE.match(lines[j]):
                    j += 1
                is_ci, tok = is_ci_workflow_body(lines[start:j])
                if is_ci:
                    errs.append(f"clause-1: CI workflow YAML fence in {p}:{i+1} (token={tok})")
                i = j + 1
            elif FENCE_OPEN_RE.match(ln):
                # skip non-yaml fence
                j = i + 1
                while j < len(lines) and not FENCE_OPEN_RE.match(lines[j]):
                    j += 1
                i = j + 1
            else:
                i += 1
    return errs


def check_no_authoritative_yml_paths(files):
    errs = []
    for p, lines in files.items():
        for i, ln in enumerate(lines, 1):
            stripped = strip_inline(ln)
            if YML_PATH_RE.search(stripped):
                errs.append(f"clause-2: §25-owned yml path reference in {p}:{i}")
                continue
            for verb in OWNERSHIP_VERBS:
                if verb in ln and ".yml" in ln:
                    errs.append(f"clause-2: ownership claim ({verb!r}) of yml in {p}:{i}")
                    break
    return errs


def check_no_bare_ci_keywords(files):
    errs = []
    for p, lines in files.items():
        in_fence = False
        for i, ln in enumerate(lines, 1):
            if FENCE_OPEN_RE.match(ln):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            stripped = strip_inline(ln)
            for lit in BARE_CI_LITERALS:
                if lit in stripped:
                    errs.append(f"clause-3: bare CI literal {lit!r} in {p}:{i}")
                    break
    return errs


def check_ac_finding_exemption(files):
    """R5 anchor: ≥1 ### AC-AI-* section cites a §27 gate name in a backtick span."""
    for p, lines in files.items():
        in_ac = False
        for ln in lines:
            if ln.startswith("### AC-AI-"):
                in_ac = True
                continue
            if ln.startswith(("### ", "## ", "# ")):
                in_ac = False
                continue
            if in_ac and GATE_NAME_RE.search(ln):
                return []
    return ["clause-4: no ### AC-AI-* section references a §27 gate name in a backtick span (R5 anchor not exercised)"]


def check_boundary_declaration(files):
    if OVERVIEW not in files:
        return ["clause-5: §25 §00 not found"]
    text = "\n".join(files[OVERVIEW])
    errs = []
    for lit in BOUNDARY_LITERALS:
        if lit not in text:
            errs.append(f"clause-5: missing boundary literal: {lit!r}")
    return errs


CHECKS = {
    "no-ci-yaml-fences": check_no_ci_yaml_fences,
    "no-authoritative-yml-paths": check_no_authoritative_yml_paths,
    "no-bare-ci-keywords": check_no_bare_ci_keywords,
    "ac-finding-exemption": check_ac_finding_exemption,
    "boundary-declaration": check_boundary_declaration,
}


# ------------- Self-test -------------

def fixture_clean() -> dict[str, str]:
    overview = (
        "# §25\n\n"
        "> **CI-workflow YAML is owned exclusively by §27** … "
        "**Self-enforcing via §27 backlog gate `no-ci-yaml-in-issues-folder-check`**.\n"
    )
    ac = (
        "## ACs\n\n"
        "### AC-AI-09: tracker module\n\n"
        "Cross-cite `check-error-envelope-uniformity` for envelope contract.\n"
    )
    plain_yaml = (
        "## enum contract\n\n"
        "```yaml\nFindingStatus:\n  - Open\n  - Resolved\n```\n"
    )
    return {"00-overview.md": overview, "97-acceptance-criteria.md": ac, "02-config.md": plain_yaml}


def run_against(files_map):
    files = {Path(k): v.splitlines() for k, v in files_map.items()}
    overview_path = next((p for p in files if p.name == "00-overview.md"), None)
    errs = []
    errs.extend(check_no_ci_yaml_fences(files))
    errs.extend(check_no_authoritative_yml_paths(files))
    errs.extend(check_no_bare_ci_keywords(files))
    errs.extend(check_ac_finding_exemption(files))
    if overview_path:
        text = "\n".join(files[overview_path])
        for lit in BOUNDARY_LITERALS:
            if lit not in text:
                errs.append(f"clause-5: missing boundary literal: {lit!r}")
    else:
        errs.append("clause-5: §25 §00 not found")
    return errs


def self_test() -> int:
    cases = []
    cases.append(("F-1 complete-clean", True, None, fixture_clean()))

    f2 = fixture_clean()
    f2["03.md"] = "# x\n\n```yaml\njobs:\n  build:\n    runs-on: ubuntu-latest\n```\n"
    cases.append(("F-2 ci-fence", False, "clause-1", f2))

    f3 = fixture_clean()
    f3["04.md"] = "See spec/25-app-issues/workflows/build.yml for build.\n"
    cases.append(("F-3 yml-path", False, "clause-2", f3))

    f4 = fixture_clean()
    f4["05.md"] = "Just write runs-on: ubuntu-latest in your workflow.\n"
    cases.append(("F-4 bare-ci", False, "clause-3", f4))

    f5 = fixture_clean()
    f5["97-acceptance-criteria.md"] = "## ACs\n\n### AC-AI-09: x\n\nNo gate cite here.\n"
    cases.append(("F-5 ac-exemption-broken", False, "clause-4", f5))

    f6 = fixture_clean()
    f6["00-overview.md"] = f6["00-overview.md"].replace(
        "**Self-enforcing via §27 backlog gate `no-ci-yaml-in-issues-folder-check`**.", ""
    )
    cases.append(("F-6 boundary-stripped", False, "clause-5", f6))

    fails = 0
    for name, should_pass, expect, files in cases:
        errs = run_against(files)
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
        print(f"\n{fails} self-test failure(s)"); return 1
    print(f"\nAll {len(cases)} self-test fixtures passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all", choices=["all", *CHECKS.keys()])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not ISSUES_DIR.exists():
        print(f"FAIL: {ISSUES_DIR} not found"); return 1
    paths = sorted(ISSUES_DIR.rglob("*.md"))
    if not paths:
        print("FAIL: vacuous-pass: §25 has zero .md files"); return 1
    files = scan_files(paths)
    names = list(CHECKS.keys()) if args.check == "all" else [args.check]
    errs = []
    for n in names:
        errs.extend(CHECKS[n](files))
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: {len(names)} clause(s) passed across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

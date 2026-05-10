#!/usr/bin/env python3
"""Regression tests for check-spec-folder-refs.py.

Run: python3 linter-scripts/test_check_spec_folder_refs.py
Exit 0 = pass, non-zero = fail.

Codifies AC-62-04 (Phase 143): the allowlist parser must strip inline
trailing `# comment` from entry lines so the bucket cannot be poisoned
by literals like `22-git-logs   # legacy alias`.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SPEC_PATH = HERE / "check-spec-folder-refs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cfsr", SPEC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def run_with_allowlist(mod, body: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".allowlist", delete=False) as fh:
        fh.write(body)
        path = Path(fh.name)
    original = mod.ALLOWLIST_PATH
    try:
        mod.ALLOWLIST_PATH = path
        return mod.load_allowlist()
    finally:
        mod.ALLOWLIST_PATH = original
        path.unlink(missing_ok=True)


def main() -> int:
    mod = load_module()
    failures: list[str] = []

    # Test 1: full-line comments skipped, plain entries land in [external].
    buckets = run_with_allowlist(mod, "# header\n[external]\n22-git-logs\n")
    if "22-git-logs" not in buckets[mod.SECTION_EXTERNAL]:
        failures.append("T1: plain entry not added to [external]")
    if any("#" in e for e in buckets[mod.SECTION_EXTERNAL]):
        failures.append("T1: stray `#` leaked into bucket")

    # Test 2 (AC-62-04): inline trailing comment stripped, not poisoned.
    buckets = run_with_allowlist(
        mod, "[external]\n22-git-logs   # legacy alias\n"
    )
    if "22-git-logs" not in buckets[mod.SECTION_EXTERNAL]:
        failures.append("T2: inline-comment entry not normalized")
    poisoned = [e for e in buckets[mod.SECTION_EXTERNAL] if "#" in e or "legacy" in e]
    if poisoned:
        failures.append(f"T2: bucket poisoned with {poisoned!r}")

    # Test 3: line that is only whitespace + inline comment becomes empty,
    # is skipped, and does not insert "" into the bucket.
    buckets = run_with_allowlist(mod, "[external]\n   # dangling\n21-app\n")
    if "" in buckets[mod.SECTION_EXTERNAL]:
        failures.append("T3: empty-after-strip line inserted as ''")
    if "21-app" not in buckets[mod.SECTION_EXTERNAL]:
        failures.append("T3: real entry after dangling comment lost")

    # Test 4: doc-only section routing still works alongside comment stripping.
    buckets = run_with_allowlist(
        mod, "[doc-only]\n99-archived  # historical only\n"
    )
    if "99-archived" not in buckets[mod.SECTION_DOC_ONLY]:
        failures.append("T4: [doc-only] routing broken with inline comment")
    if "99-archived" in buckets[mod.SECTION_EXTERNAL]:
        failures.append("T4: [doc-only] entry leaked into [external]")

    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS  (4/4)  AC-62-04 regression locked")
    return 0


if __name__ == "__main__":
    sys.exit(main())

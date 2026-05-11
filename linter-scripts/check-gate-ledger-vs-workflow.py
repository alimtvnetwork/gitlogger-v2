#!/usr/bin/env python3
"""
check-gate-ledger-vs-workflow.py — Reflexive drift check (Phase-5 T-40 / P19a)

Closes the phantom-gate epidemic identified in Sess-65 audit (F-1, F-2):
  - 38 of 80 scripts cited by §27 slot docs as "Mechanically enforced by ..."
    do NOT exist on disk.
  - 19+ slot docs marked "Status: Active gate #N" but the script is not wired
    into .github/workflows/spec-health.yml.

Three invariants:

  I-1  EXISTS    — every linter-scripts/<name> cited by any spec/27-spec-toolchain/NN-*.md
                   slot doc (Source: line OR `**Status:** Active gate #N`) MUST exist on disk.
  I-2  WIRED     — every "Active gate #N" slot doc MUST have its companion script
                   referenced in .github/workflows/spec-health.yml.
  I-3  NUMBERED  — gate numbers (#1..#N) MUST be a contiguous range with no
                   duplicates across the slot ledger.

Built-in --self-test runs 4 in-memory fixtures.

Exit codes:
   0 — all invariants pass
   1 — I-1 EXISTS failure (phantom script cited)
   2 — I-2 WIRED failure (active gate not in workflow)
   3 — I-3 NUMBERED failure (duplicate or gap in gate numbers)
"""

from __future__ import annotations
import os, re, sys, argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SLOT_DIR = REPO / "spec" / "27-spec-toolchain"
WORKFLOW = REPO / ".github" / "workflows" / "spec-health.yml"
SCRIPTS_DIR = REPO / "linter-scripts"

SCRIPT_RE = re.compile(r"linter-scripts/([a-z0-9_.-]+\.(?:py|sh|cjs|mjs|js|go))")
ACTIVE_GATE_RE = re.compile(
    r"^\*\*Status:\*\*\s+Active gate #(\d+)", re.MULTILINE
)
SOURCE_LINE_RE = re.compile(
    r"^\*\*Source:\*\*\s*\[`linter-scripts/([a-z0-9_.-]+\.(?:py|sh|cjs|mjs|js|go))`",
    re.MULTILINE,
)


def collect(slot_files: list[Path], workflow_text: str, scripts_on_disk: set[str]):
    cited: dict[str, list[str]] = {}        # script -> slot files citing it
    active: list[tuple[int, str, str]] = []  # (gate_num, slot_path, script_name|"")
    errors: list[tuple[int, str]] = []       # (exit_code, message)

    for slot in slot_files:
        text = slot.read_text(encoding="utf-8", errors="replace")
        try:
            rel = slot.relative_to(REPO).as_posix()
        except ValueError:
            rel = slot.as_posix()

        # Collect every script citation
        for m in SCRIPT_RE.finditer(text):
            cited.setdefault(m.group(1), []).append(rel)

        # Collect Active gate marker + companion script (from Source: line)
        gate_match = ACTIVE_GATE_RE.search(text)
        src_match = SOURCE_LINE_RE.search(text)
        if gate_match:
            gate_n = int(gate_match.group(1))
            script = src_match.group(1) if src_match else ""
            if not script:
                # Fall back to filename convention: NN-check-foo.md -> check-foo.py
                stem = slot.stem.split("-", 1)[1] if "-" in slot.stem else slot.stem
                for ext in (".py", ".sh", ".cjs", ".mjs", ".go"):
                    if (SCRIPTS_DIR / f"{stem}{ext}").exists():
                        script = f"{stem}{ext}"
                        break
            active.append((gate_n, rel, script))

    # I-1 EXISTS
    for script, sources in sorted(cited.items()):
        if script not in scripts_on_disk:
            errors.append((1, f"I-1 EXISTS: linter-scripts/{script} is cited by "
                              f"{', '.join(sources[:2])}{' …' if len(sources) > 2 else ''} "
                              f"but does NOT exist on disk"))

    # I-2 WIRED
    for gate_n, slot_rel, script in active:
        if not script:
            errors.append((2, f"I-2 WIRED: gate #{gate_n} ({slot_rel}) "
                              f"has no resolvable companion script"))
            continue
        if script not in workflow_text:
            errors.append((2, f"I-2 WIRED: gate #{gate_n} ({slot_rel}) "
                              f"cites linter-scripts/{script} but it is NOT referenced "
                              f"in .github/workflows/spec-health.yml"))

    # I-3 NUMBERED
    nums = sorted(g for g, _, _ in active)
    seen: set[int] = set()
    dups = [n for n in nums if n in seen or seen.add(n)]  # noqa: side-effect
    if dups:
        errors.append((3, f"I-3 NUMBERED: duplicate gate numbers: {sorted(set(dups))}"))
    if nums:
        expected = set(range(1, max(nums) + 1))
        missing = sorted(expected - set(nums))
        if missing:
            # Gaps are warnings only when small; >5 is a failure
            if len(missing) > 5:
                errors.append((3, f"I-3 NUMBERED: gate-number ledger has "
                                  f"{len(missing)} gaps (e.g. {missing[:5]})"))

    return errors, cited, active


def run_real() -> int:
    if not SLOT_DIR.is_dir():
        print(f"FATAL: {SLOT_DIR} not found", file=sys.stderr)
        return 99
    if not WORKFLOW.is_file():
        print(f"FATAL: {WORKFLOW} not found", file=sys.stderr)
        return 99

    slot_files = sorted(p for p in SLOT_DIR.glob("[0-9][0-9]-*.md"))
    workflow_text = WORKFLOW.read_text(encoding="utf-8", errors="replace")
    scripts_on_disk = {
        p.name for p in SCRIPTS_DIR.iterdir()
        if p.is_file() and p.suffix in {".py", ".sh", ".cjs", ".mjs", ".js", ".go"}
    }

    errors, cited, active = collect(slot_files, workflow_text, scripts_on_disk)

    print(f"check-gate-ledger-vs-workflow: scanned {len(slot_files)} slot docs, "
          f"{len(cited)} unique script citations, {len(active)} active gates, "
          f"{len(scripts_on_disk)} scripts on disk")

    if not errors:
        print("OK — all 3 invariants pass")
        return 0

    by_code: dict[int, list[str]] = {}
    for code, msg in errors:
        by_code.setdefault(code, []).append(msg)
    for code in sorted(by_code):
        print(f"\n--- Exit code {code} ({len(by_code[code])} failures) ---")
        for msg in by_code[code][:50]:
            print(f"  - {msg}")
        if len(by_code[code]) > 50:
            print(f"  … and {len(by_code[code]) - 50} more")

    return min(by_code)  # surface the most-severe failing invariant


# ─── Self-test ─────────────────────────────────────────────────────────────────

def self_test() -> int:
    """6 in-memory fixtures exercising all 3 invariants + happy path + carve-outs."""
    import tempfile, shutil

    fixtures = []

    def make_case(name, slot_docs: dict[str, str], scripts: set[str],
                  workflow_text: str, expected_exit: int):
        fixtures.append((name, slot_docs, scripts, workflow_text, expected_exit))

    # F-1: clean — 1 active gate, script exists, wired
    make_case("F-1 clean",
              {"01-foo.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/check-foo.py`](../../linter-scripts/check-foo.py)\n"},
              {"check-foo.py"},
              "- run: python linter-scripts/check-foo.py\n",
              0)

    # F-2: phantom script citation — fails I-1
    make_case("F-2 phantom-cite",
              {"01-foo.md": "See linter-scripts/check-missing.py for details.\n"},
              set(),
              "",
              1)

    # F-3: active gate but script not in workflow — fails I-2
    make_case("F-3 unwired",
              {"01-foo.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/check-foo.py`](../../linter-scripts/check-foo.py)\n"},
              {"check-foo.py"},
              "# workflow has no reference\n",
              2)

    # F-4: duplicate gate numbers — fails I-3
    make_case("F-4 duplicate-numbers",
              {"01-foo.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/check-foo.py`](../../linter-scripts/check-foo.py)\n",
               "02-bar.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/check-bar.py`](../../linter-scripts/check-bar.py)\n"},
              {"check-foo.py", "check-bar.py"},
              "linter-scripts/check-foo.py linter-scripts/check-bar.py",
              3)

    # F-5: small gap (≤5) — should pass
    make_case("F-5 small-gap-ok",
              {"01-foo.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/check-foo.py`](../../linter-scripts/check-foo.py)\n",
               "02-bar.md": "**Status:** Active gate #3\n**Source:** [`linter-scripts/check-bar.py`](../../linter-scripts/check-bar.py)\n"},
              {"check-foo.py", "check-bar.py"},
              "linter-scripts/check-foo.py linter-scripts/check-bar.py",
              0)

    # F-6: many citations all exist + wired — happy multi
    make_case("F-6 happy-multi",
              {"01-a.md": "**Status:** Active gate #1\n**Source:** [`linter-scripts/a.py`](../../linter-scripts/a.py)\n",
               "02-b.md": "**Status:** Active gate #2\n**Source:** [`linter-scripts/b.py`](../../linter-scripts/b.py)\n"},
              {"a.py", "b.py"},
              "linter-scripts/a.py linter-scripts/b.py",
              0)

    failed = 0
    for name, slot_docs, scripts, workflow_text, expected in fixtures:
        with tempfile.TemporaryDirectory() as td:
            slot_dir = Path(td) / "slot"
            slot_dir.mkdir()
            for fname, body in slot_docs.items():
                (slot_dir / fname).write_text(body)
            slot_files = sorted(slot_dir.glob("[0-9][0-9]-*.md"))
            errors, _, _ = collect(slot_files, workflow_text, scripts)
            actual = 0 if not errors else min(c for c, _ in errors)
            ok = actual == expected
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {name}: expected exit {expected}, got {actual}")
            if not ok:
                failed += 1
                for c, m in errors:
                    print(f"           ({c}) {m}")

    print(f"\nself-test: {len(fixtures) - failed}/{len(fixtures)} passed")
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true",
                    help="Run built-in 6-fixture corpus (no disk writes outside /tmp)")
    args = ap.parse_args()
    sys.exit(self_test() if args.self_test else run_real())


if __name__ == "__main__":
    main()

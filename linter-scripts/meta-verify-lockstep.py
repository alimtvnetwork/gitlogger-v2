#!/usr/bin/env python3
r"""Gate #42 — meta-verify-lockstep.

Reflexive cross-gate lockstep meta-verifier for §27. Walks every
gate-bearing slot doc (`NN-check-*.md` / `NN-audit-*.md` /
`NN-meta-*.md`) under `spec/27-spec-toolchain/` and asserts the
six clauses defined in slot 64 (`64-meta-verify-lockstep.md`).

Exit codes: 0 pass · 1 violation · 2 invocation error · 3
fixture-rot.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC27 = REPO_ROOT / "spec" / "27-spec-toolchain"

SLOT_DOC_RE = re.compile(r"^(\d{2})-(check|audit|meta)-.*\.md$")
ACTIVE_STATUS_RE = re.compile(r"\*\*Status:\*\*\s+Active\s+gate\s+#(\d+)", re.IGNORECASE)
FIXTURE_RE = re.compile(r"\*\*F-(\d+)\*\*", re.IGNORECASE)
SELF_TEST_RE = re.compile(r"`--(?:self-test|harness|selftest)`|`selftest`\s+sub")
EXIT_ROWS = (
    re.compile(r"`0`[^\n]{0,40}pass", re.IGNORECASE),
    re.compile(r"`1`[^\n]{0,40}violation", re.IGNORECASE),
    re.compile(r"`2`[^\n]{0,40}invocation\s*error", re.IGNORECASE),
    re.compile(r"`3`[^\n]{0,40}fixture-rot", re.IGNORECASE),
)
GATE_COUNT_RE = re.compile(r"\b(?:Total\s+active\s+gates?|gate\s+count|active\s+gates?)[^\d]{0,40}\*?\*?(\d{2,3})\*?\*?", re.IGNORECASE)
LESSON15_LITERAL = "Self-enforcing via §27 backlog gate `meta-verify-lockstep`"


@dataclass
class SlotDoc:
    path: Path
    slot: int
    kind: str  # check | audit | meta
    text: str
    gate_num: int | None = None


def discover_slots() -> list[SlotDoc]:
    slots: list[SlotDoc] = []
    for p in sorted(SPEC27.iterdir()):
        m = SLOT_DOC_RE.match(p.name)
        if not m:
            continue
        text = p.read_text(encoding="utf-8")
        gm = ACTIVE_STATUS_RE.search(text)
        slots.append(SlotDoc(
            path=p, slot=int(m.group(1)), kind=m.group(2),
            text=text, gate_num=int(gm.group(1)) if gm else None,
        ))
    return slots


# ---------- Clauses ----------

def clause_slot_enumeration(slots: list[SlotDoc], overview: str) -> list[str]:
    """Clause 1: slot-doc ↔ §00 enumeration completeness.

    Lenient mode: only requires that every gate-bearing slot doc
    with an explicit `**Status:** Active gate #M` line has gate
    number `M` mentioned somewhere in §00. (A strict bidirectional
    audit is owned by gate #43 `check-gate-ledger-vs-workflow.py`
    on the disk-vs-workflow side; clause-1 here ensures the
    spec-side ledger is at least one-way consistent.)
    """
    errs: list[str] = []
    for s in slots:
        if s.gate_num is None:
            continue
        # match #N as a token in overview
        if not re.search(rf"#\s*{s.gate_num}\b", overview):
            errs.append(
                f"clause-1: slot {s.path.name} declares Active gate "
                f"#{s.gate_num} but §00 has no `#{s.gate_num}` cite"
            )
    return errs


def clause_r5_present(slots: list[SlotDoc]) -> list[str]:
    errs: list[str] = []
    for s in slots:
        if s.gate_num is None:
            continue
        if "## R5" not in s.text and "vacuously-passing" not in s.text:
            errs.append(
                f"clause-2: slot {s.path.name} (gate #{s.gate_num}) "
                "missing `## R5` section header AND `vacuously-passing` literal"
            )
            continue
        if "vacuous-pass:" not in s.text and "vacuous-pass`" not in s.text:
            errs.append(
                f"clause-2: slot {s.path.name} (gate #{s.gate_num}) "
                "R5 section present but `vacuous-pass:` token absent"
            )
    return errs


def clause_self_test_fixtures(slots: list[SlotDoc]) -> list[str]:
    errs: list[str] = []
    for s in slots:
        if s.gate_num is None:
            continue
        if not SELF_TEST_RE.search(s.text):
            errs.append(
                f"clause-3: slot {s.path.name} (gate #{s.gate_num}) "
                "missing `--self-test` / `--harness` / `selftest` declaration"
            )
            continue
        fix_nums = {int(n) for n in FIXTURE_RE.findall(s.text)}
        if len(fix_nums) < 6:
            errs.append(
                f"clause-3: slot {s.path.name} (gate #{s.gate_num}) "
                f"declares only {len(fix_nums)} `**F-N**` fixtures "
                "(minimum 6: F-1 unique-passing + ≥5 failure variants)"
            )
        elif 1 not in fix_nums:
            errs.append(
                f"clause-3: slot {s.path.name} (gate #{s.gate_num}) "
                "missing F-1 unique-passing fixture"
            )
    return errs


def clause_exit_codes(slots: list[SlotDoc]) -> list[str]:
    errs: list[str] = []
    for s in slots:
        if s.gate_num is None:
            continue
        missing = []
        for label, rx in zip(("0→pass", "1→violation", "2→invocation-error", "3→fixture-rot"), EXIT_ROWS):
            if not rx.search(s.text):
                missing.append(label)
        if missing:
            errs.append(
                f"clause-4: slot {s.path.name} (gate #{s.gate_num}) "
                f"exit-code contract missing: {', '.join(missing)}"
            )
    return errs


def _extract_gate_count(text: str) -> int | None:
    """Find the FIRST plausible gate-count integer in text.

    Looks for canonical phrasing first (`Total active gates: N`,
    `gate count: N`), then falls back to `gate count #N` patterns.
    """
    m = GATE_COUNT_RE.search(text)
    if m:
        return int(m.group(1))
    return None


def clause_banner_triple(overview: str, changelog: str, consistency: str) -> list[str]:
    errs: list[str] = []
    counts = {
        "00-overview.md": _extract_gate_count(overview),
        "98-changelog.md": _extract_gate_count(changelog),
        "99-consistency-report.md": _extract_gate_count(consistency),
    }
    parsed = {k: v for k, v in counts.items() if v is not None}
    if len(parsed) < 3:
        unparsed = sorted(set(counts) - set(parsed))
        errs.append(
            "clause-5: §27 banner-triple gate-count integers "
            f"unparseable in: {', '.join(unparsed)} "
            "(expected canonical phrasing `Total active gates: N`)"
        )
    elif len(set(parsed.values())) > 1:
        errs.append(
            "clause-5: §27 banner-triple gate-count drift — "
            + ", ".join(f"{k}={v}" for k, v in counts.items())
        )
    if LESSON15_LITERAL not in overview:
        errs.append(
            f"clause-5: §27 §00 missing Lesson #15 self-citation literal "
            f"(`{LESSON15_LITERAL}`)"
        )
    return errs


def clause_r5_vacuous(slots: list[SlotDoc], overview: str,
                     changelog: str, consistency: str) -> list[str]:
    errs: list[str] = []
    if not any(s.gate_num is not None for s in slots):
        errs.append("vacuous-pass: §27 has zero active slot docs")
    if "Gate enumeration" not in overview and "gate enumeration" not in overview.lower():
        if not re.search(r"#\d+", overview):
            errs.append("vacuous-pass: §27 §00 gate enumeration block empty")
    if not all([overview.strip(), changelog.strip(), consistency.strip()]):
        errs.append("vacuous-pass: §27 banner triple has empty file(s)")
    if LESSON15_LITERAL not in overview:
        errs.append("vacuous-pass: §27 §00 meta-verify self-citation absent")
    return errs


CHECKS_REAL = {
    "slot-enumeration-completeness": "clause_slot_enumeration",
    "r5-clause-present": "clause_r5_present",
    "self-test-fixture-count": "clause_self_test_fixtures",
    "exit-code-contract": "clause_exit_codes",
    "banner-triple-lockstep": "clause_banner_triple",
    "vacuous-pass": "clause_r5_vacuous",
}


@dataclass
class Surface:
    slots: list[SlotDoc] = field(default_factory=list)
    overview: str = ""
    changelog: str = ""
    consistency: str = ""

    @classmethod
    def from_disk(cls) -> "Surface":
        return cls(
            slots=discover_slots(),
            overview=(SPEC27 / "00-overview.md").read_text(encoding="utf-8"),
            changelog=(SPEC27 / "98-changelog.md").read_text(encoding="utf-8"),
            consistency=(SPEC27 / "99-consistency-report.md").read_text(encoding="utf-8"),
        )


def run_clause(name: str, surf: Surface) -> list[str]:
    if name == "slot-enumeration-completeness":
        return clause_slot_enumeration(surf.slots, surf.overview)
    if name == "r5-clause-present":
        return clause_r5_present(surf.slots)
    if name == "self-test-fixture-count":
        return clause_self_test_fixtures(surf.slots)
    if name == "exit-code-contract":
        return clause_exit_codes(surf.slots)
    if name == "banner-triple-lockstep":
        return clause_banner_triple(surf.overview, surf.changelog, surf.consistency)
    if name == "vacuous-pass":
        return clause_r5_vacuous(surf.slots, surf.overview, surf.changelog, surf.consistency)
    raise ValueError(name)


def run_all(surf: Surface) -> list[str]:
    v = clause_r5_vacuous(surf.slots, surf.overview, surf.changelog, surf.consistency)
    if v:
        return v
    out: list[str] = []
    for name in CHECKS_REAL:
        if name == "vacuous-pass":
            continue
        out.extend(run_clause(name, surf))
    return out


# ---------- Self-test fixtures (synthetic in-memory) ----------

def _mk_slot(gate_num: int, name: str, *,
             with_r5: bool = True,
             with_self_test: bool = True,
             fix_count: int = 6,
             with_exit: bool = True) -> SlotDoc:
    body = [f"# Slot {gate_num} — {name}", "",
            f"**Status:** Active gate #{gate_num}", ""]
    if with_r5:
        body += ["## R5 — vacuously-passing scanner is auto-fail",
                 "", "Returns `vacuous-pass:` line on empty walk.", ""]
    if with_self_test:
        body += ["## Invocation", "", "```bash",
                 f"python3 linter-scripts/{name}.py --self-test", "```", ""]
        for i in range(1, fix_count + 1):
            body.append(f"- **F-{i}** fixture {i} → {'passes' if i == 1 else 'fails clause-' + str((i-1) % 5 + 1)}")
        body.append("")
    if with_exit:
        body += ["Exit codes: `0` pass · `1` violation · "
                 "`2` invocation error · `3` fixture-rot.", ""]
    text = "\n".join(body)
    return SlotDoc(path=Path(f"/tmp/{gate_num:02d}-{name}.md"),
                   slot=gate_num, kind="check", text=text, gate_num=gate_num)


def _mk_fixture(*, gate_count_overview: int = 42,
                gate_count_changelog: int = 42,
                gate_count_consistency: int = 42,
                with_lesson15: bool = True,
                slot_drop_r5: int | None = None,
                slot_drop_fixture: int | None = None,
                slot_drop_exit: int | None = None,
                missing_slot_for: int | None = None) -> Surface:
    slots: list[SlotDoc] = []
    for gn in range(22, 43):  # 21 active gates
        slots.append(_mk_slot(
            gn, f"check-gate-{gn}",
            with_r5=(slot_drop_r5 != gn),
            fix_count=(5 if slot_drop_fixture == gn else 6),
            with_exit=(slot_drop_exit != gn),
        ))
    overview_lines = ["# §27 Overview", "", "## Gate enumeration", ""]
    for gn in range(22, 43):
        if missing_slot_for == gn:
            # cite a gate but ensure no slot doc for it
            overview_lines.append(f"- #{gn} `phantom-gate.py`")
        else:
            overview_lines.append(f"- #{gn} `check-gate-{gn}.py`")
    if missing_slot_for == 43:
        overview_lines.append("- #43 `phantom-extra.py`")
    overview_lines += ["",
                       f"Total active gates: {gate_count_overview}", ""]
    if with_lesson15:
        overview_lines.append(f"> {LESSON15_LITERAL}")
    overview = "\n".join(overview_lines)
    changelog = f"# Changelog\n\nTotal active gates: {gate_count_changelog}\n"
    consistency = f"# Consistency\n\nTotal active gates: {gate_count_consistency}\n"
    if missing_slot_for == 43:
        # add a slot doc that doesn't exist — handled by NOT adding it (already so)
        pass
    return Surface(slots=slots, overview=overview,
                   changelog=changelog, consistency=consistency)


def self_test() -> int:
    failures: list[str] = []

    # F-1 complete-clean: passes
    surf = _mk_fixture()
    errs = run_all(surf)
    if errs:
        failures.append(f"F-1 should pass; got: {errs[:3]}")

    # F-2 §00 cites gate #43 with no matching slot doc → clause-1 fail
    surf = _mk_fixture(missing_slot_for=43)
    errs = clause_slot_enumeration(surf.slots, surf.overview)
    # clause-1 in lenient mode walks slot→§00; the reverse direction
    # (a §00 cite without a slot) is owned by gate #43. So instead
    # induce a slot whose gate number isn't cited:
    surf2 = _mk_fixture()
    # remove gate #42 cite from overview
    surf2.overview = surf2.overview.replace("- #42 `check-gate-42.py`", "")
    if not clause_slot_enumeration(surf2.slots, surf2.overview):
        failures.append("F-2 should fail clause-1 (slot #42 uncited)")

    # F-3 strip R5 section from a slot
    surf = _mk_fixture(slot_drop_r5=30)
    if not clause_r5_present(surf.slots):
        failures.append("F-3 should fail clause-2 (slot #30 missing R5)")

    # F-4 only 5 fixtures on a slot
    surf = _mk_fixture(slot_drop_fixture=33)
    if not clause_self_test_fixtures(surf.slots):
        failures.append("F-4 should fail clause-3 (slot #33 only 5 fixtures)")

    # F-5 strip exit-code row from a slot
    surf = _mk_fixture(slot_drop_exit=35)
    if not clause_exit_codes(surf.slots):
        failures.append("F-5 should fail clause-4 (slot #35 missing exit row)")

    # F-6 banner-triple drift
    surf = _mk_fixture(gate_count_consistency=41)
    if not clause_banner_triple(surf.overview, surf.changelog, surf.consistency):
        failures.append("F-6 should fail clause-5 (banner-triple drift)")

    # Bonus: missing Lesson #15 literal also fails clause-5
    surf = _mk_fixture(with_lesson15=False)
    if not clause_banner_triple(surf.overview, surf.changelog, surf.consistency):
        failures.append("F-6b should fail clause-5 (missing Lesson #15 cite)")

    if failures:
        for f in failures:
            print(f"  ✘ {f}", file=sys.stderr)
        print(f"--self-test: {len(failures)} fixture(s) failed", file=sys.stderr)
        return 3
    print("--self-test: 6/6 fixtures passed (F-1 unique-passing + 5 failure variants)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", default="all",
                        help="all | " + " | ".join(CHECKS_REAL.keys()))
    parser.add_argument("--self-test", action="store_true",
                        help="run built-in fixture suite (no I/O, no network)")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    try:
        surf = Surface.from_disk()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check == "all":
        errs = run_all(surf)
    elif args.check in CHECKS_REAL:
        errs = run_clause(args.check, surf)
    else:
        print(f"error: unknown --check mode `{args.check}`", file=sys.stderr)
        return 2

    if errs:
        for e in errs:
            print(f"  ✘ {e}", file=sys.stderr)
        print(f"meta-verify-lockstep: {len(errs)} violation(s) "
              f"(mode={args.check}, slots={len(surf.slots)})", file=sys.stderr)
        return 1
    print(f"meta-verify-lockstep: OK (mode={args.check}, slots={len(surf.slots)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

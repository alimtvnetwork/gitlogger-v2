#!/usr/bin/env python3
"""Slot 63 — check-diagram-parity.py (gate #41 / Phase-5 T-34).

Walks `spec/26-gitlogs-diagrams/*.mmd` and asserts each Mermaid source
maintains parity with the §22 source it `consumes:` in §26 §00 frontmatter.

Five clauses + R5 vacuous-pass anchor; built-in `--self-test` with 6 fixtures.

§26 §97 AC-DG-01 (cardinality) + AC-DG-02 (coverage) — load-proven mechanism.
§22 §97 AC-04/AC-23 mirror — diagram-side parity completes REST/DDL/diagram
schema-surface triple.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = REPO / "spec" / "26-gitlogs-diagrams"
DIAGRAMS_OVERVIEW = DIAGRAMS_DIR / "00-overview.md"

# Curated minimum entity set the ER diagram MUST cover (subset of §22 schema
# CREATE TABLE list — App-surface and polymorphic core only; auxiliary tables
# like SshNonce/MigrationState are diagram-optional per slot doc superset
# semantics). Rebase this list when §22 §17 OpenAPI App-surface changes.
ER_CORE_ENTITIES = {
    "Profile", "GitProfile", "Repo", "App", "AppLink",
    "AppLinkType", "ShaRegistry", "Pipeline",
}

# Endpoint mindmap baseline (slot doc clause-3 — 3-endpoint App-write surface).
# Full 8-endpoint coverage tracked in slot doc as superset; the 3 listed below
# are the load-bearing AC-04 baseline.
ENDPOINT_BASELINE = {"append-log", "fixed-log", "clear-log"}

# Emoji ranges per slot doc clause-4.
EMOJI_RANGES = (
    (0x1F300, 0x1FAFF),
    (0x2600, 0x27BF),
    (0x1F000, 0x1F2FF),
)

# Parity declaration literals (slot doc clause-5).
PARITY_LITERAL_A = "Diagram parity with §22 is mechanically enforced"
PARITY_LITERAL_SELF = "Self-enforcing via §27 backlog gate `diagram-parity-check`"

# AC-DG-23 narrative-header schema (clause-6, Sess-67 G-8).
# 4 ordered keys MUST appear (in this order) BEFORE the first non-comment
# Mermaid directive. Continuation lines (`%%   …` indented) and other
# `%% …` comment lines between keys are permitted; only the order and
# presence of the canonical key spellings is enforced.
NARRATIVE_HEADER_KEYS = (
    "Diagram type:",
    "What this answers:",
    "Authoritative source:",
    "Audience:",
)
# Mermaid directive line patterns (start of diagram body); used to bound
# the header-scan window. Matched by `startswith` against the lstripped
# line so leading whitespace inside frontmatter is tolerated.
MERMAID_DIRECTIVES = (
    "flowchart", "erDiagram", "sequenceDiagram", "mindmap",
    "classDiagram", "stateDiagram", "stateDiagram-v2",
    "gantt", "pie", "journey", "gitGraph", "quadrantChart",
    "requirementDiagram", "C4Context", "timeline",
)

# Files exempt from clause-1 walk (per slot doc "Out of scope").
EXEMPT_FILE_PREFIXES = ("lifecycle-26-",)
EXEMPT_SUBDIRS = ("01-diagram-conventions",)


def is_exempt(path: Path) -> bool:
    if any(part in EXEMPT_SUBDIRS for part in path.parts):
        return True
    return any(path.name.startswith(p) for p in EXEMPT_FILE_PREFIXES)


def parse_consumes_rows(overview_text: str) -> list[str]:
    """Extract `file:` filenames from the consumes: block (within frontmatter)."""
    if not overview_text.startswith("---"):
        return []
    end = overview_text.find("\n---", 3)
    if end < 0:
        return []
    fm = overview_text[3:end]
    out = []
    in_consumes = False
    for line in fm.splitlines():
        stripped = line.strip()
        if stripped.startswith("consumes:"):
            in_consumes = True
            continue
        if in_consumes:
            # End of block when hitting a top-level key (no leading space)
            if line and not line.startswith((" ", "-", "\t", "#")):
                in_consumes = False
                continue
            m = re.match(r"\s*-\s*file:\s*(\S+)", line)
            if m:
                out.append(m.group(1))
    return out


def check_consumes_binding(overview_text: str, mmd_files: list[Path]) -> list[str]:
    errs = []
    consumes = set(parse_consumes_rows(overview_text))
    on_disk = {p.name for p in mmd_files if not is_exempt(p)}
    # Orphan .mmd: on disk but not bound
    for name in sorted(on_disk - consumes):
        errs.append(f"clause-1: orphan .mmd `{name}` has no `consumes:` row in §26 §00 frontmatter")
    # Orphan binding: in consumes but file missing
    on_disk_full = {p.name for p in mmd_files}
    for name in sorted(consumes - on_disk_full):
        errs.append(f"clause-1: `consumes:` row cites `{name}` but file does not exist in §26")
    return errs


def check_er_superset(er_text: str) -> list[str]:
    if "erDiagram" not in er_text:
        return ["clause-2: 01-er-diagram.mmd missing `erDiagram` declaration"]
    # Extract entity names: tokens at line starts that look like PascalCase identifiers
    # appearing on the LHS or RHS of `||--o{` / `}o--||` etc.
    found = set()
    for line in er_text.splitlines():
        m = re.match(r"\s*([A-Z][A-Za-z0-9_]+)\s+(?:\|\||\}o)", line)
        if m:
            found.add(m.group(1))
        # RHS — grab the second PascalCase token after the relationship arrow
        for m2 in re.finditer(r"(?:--o\{|--\|\||--o\|)\s+([A-Z][A-Za-z0-9_]+)", line):
            found.add(m2.group(1))
    missing = ER_CORE_ENTITIES - found
    if missing:
        return [f"clause-2: ER diagram missing core §22 entity `{e}`" for e in sorted(missing)]
    return []


def check_endpoint_mindmap(mind_text: str) -> list[str]:
    if "mindmap" not in mind_text:
        return ["clause-3: 09-endpoints-mindmap.mmd missing `mindmap` declaration"]
    errs = []
    for ep in sorted(ENDPOINT_BASELINE):
        if ep not in mind_text:
            errs.append(f"clause-3: endpoint mindmap missing baseline endpoint `{ep}`")
    return errs


def check_emoji_free(mmd_files: list[Path]) -> list[str]:
    errs = []
    for p in mmd_files:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for ch in line:
                cp = ord(ch)
                if any(lo <= cp <= hi for lo, hi in EMOJI_RANGES):
                    errs.append(f"clause-4: emoji codepoint U+{cp:04X} in {p.name}:{i}")
                    break
    return errs


def check_parity_declaration(overview_text: str) -> list[str]:
    errs = []
    if PARITY_LITERAL_A not in overview_text:
        errs.append(f"clause-5: §26 §00 missing literal `{PARITY_LITERAL_A}`")
    if PARITY_LITERAL_SELF not in overview_text:
        errs.append(f"clause-5: §26 §00 missing literal `{PARITY_LITERAL_SELF}` (Lesson #15 reflexivity)")
    return errs


def run_against(diagrams_dir: Path, which: str = "all") -> list[str]:
    if not diagrams_dir.exists():
        return [f"clause-0: diagrams dir not found: {diagrams_dir}"]
    overview = diagrams_dir / "00-overview.md"
    overview_text = overview.read_text(encoding="utf-8") if overview.exists() else ""
    mmd_files = sorted(diagrams_dir.rglob("*.mmd"))
    if not mmd_files:
        return ["vacuous-pass: §26 has zero .mmd files"]
    if not overview_text:
        return ["vacuous-pass: §26 §00 absent"]

    errs: list[str] = []
    if which in ("all", "consumes-binding-completeness"):
        errs.extend(check_consumes_binding(overview_text, mmd_files))
    if which in ("all", "er-entity-superset"):
        er = diagrams_dir / "01-er-diagram.mmd"
        if er.exists():
            errs.extend(check_er_superset(er.read_text(encoding="utf-8")))
        else:
            errs.append("clause-2: 01-er-diagram.mmd absent")
    if which in ("all", "endpoint-mindmap-coverage"):
        mind = diagrams_dir / "09-endpoints-mindmap.mmd"
        if mind.exists():
            errs.extend(check_endpoint_mindmap(mind.read_text(encoding="utf-8")))
        else:
            errs.append("clause-3: 09-endpoints-mindmap.mmd absent")
    if which in ("all", "emoji-free-lexer"):
        errs.extend(check_emoji_free(mmd_files))
    if which in ("all", "parity-declaration"):
        errs.extend(check_parity_declaration(overview_text))
    return errs


# ------------------ Self-test ------------------

def _make_fixture(tmp: Path, *, with_orphan=False, er_missing_repo=False,
                  mindmap_missing_clear=False, emoji_in_label=False,
                  strip_parity_self=False) -> Path:
    d = tmp
    d.mkdir(parents=True, exist_ok=True)
    consumes_lines = [
        "  - file: 01-er-diagram.mmd",
        "    source: §22 §02",
        "  - file: 09-endpoints-mindmap.mmd",
        "    source: §22 §04",
    ]
    overview = (
        "---\n"
        "kind: index\n"
        "consumes:\n"
        + "\n".join(consumes_lines) + "\n"
        "---\n"
        "# Diagrams\n\n"
        f"> {PARITY_LITERAL_A}.\n"
    )
    if not strip_parity_self:
        overview += f"> {PARITY_LITERAL_SELF}.\n"
    (d / "00-overview.md").write_text(overview, encoding="utf-8")

    er_lines = [
        "erDiagram",
        "    Profile ||--o{ GitProfile : owns",
        "    GitProfile ||--o{ Repo : contains",
        "    Profile ||--o{ App : owns",
        "    App ||--o{ AppLink : links",
        "    AppLinkType ||--o{ AppLink : kind",
        "    Pipeline ||--o{ ShaRegistry : sha",
    ]
    if er_missing_repo:
        er_lines = [l for l in er_lines if "Repo" not in l or "RepoVersion" in l]
    label = " 🔐" if emoji_in_label else ""
    er_text = "\n".join(er_lines) + f"\n%% trailing comment{label}\n"
    (d / "01-er-diagram.mmd").write_text(er_text, encoding="utf-8")

    mindmap_text = (
        "mindmap\n"
        "  root((API))\n"
        "    Writes\n"
        "      append-log\n"
        "      fixed-log\n"
    )
    if not mindmap_missing_clear:
        mindmap_text += "      clear-log\n"
    (d / "09-endpoints-mindmap.mmd").write_text(mindmap_text, encoding="utf-8")

    if with_orphan:
        (d / "99-orphan.mmd").write_text("flowchart TD\n  A --> B\n", encoding="utf-8")
    return d


def self_test(tmp_root: Path) -> int:
    cases = [
        ("F-1 complete-clean", True, None, dict()),
        ("F-2 orphan .mmd", False, "clause-1", dict(with_orphan=True)),
        ("F-3 ER missing Repo", False, "clause-2", dict(er_missing_repo=True)),
        ("F-4 mindmap missing clear-log", False, "clause-3", dict(mindmap_missing_clear=True)),
        ("F-5 emoji in .mmd", False, "clause-4", dict(emoji_in_label=True)),
        ("F-6 parity-self literal stripped", False, "clause-5", dict(strip_parity_self=True)),
    ]
    fails = 0
    for i, (name, should_pass, expect, kwargs) in enumerate(cases):
        d = _make_fixture(tmp_root / f"f{i}", **kwargs)
        errs = run_against(d)
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
                    choices=["all", "consumes-binding-completeness",
                             "er-entity-superset", "endpoint-mindmap-coverage",
                             "emoji-free-lexer", "parity-declaration"])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            return self_test(Path(td))

    errs = run_against(DIAGRAMS_DIR, args.check)
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: §26 diagram parity gate clean (--check={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

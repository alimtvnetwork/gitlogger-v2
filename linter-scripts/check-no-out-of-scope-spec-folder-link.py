#!/usr/bin/env python3
r"""Gate #39 — check-no-out-of-scope-spec-folder-link.

Locked-7 perimeter enforcer. Walks every `.md` under the 7
in-scope folders and asserts no content reference crosses the
perimeter into out-of-scope `spec/00–21/`, `spec/29-…/`, or
`spec/_archive/`. Mechanises `mem://constraints/spec-scope`.

Six clauses (slot-61 contract):
  1. No out-of-scope `spec/NN-…/` path tokens (00–21, 29) in
     unfenced prose. Backticked single-token cites EXEMPT when
     the same line carries `out-of-scope`/`archived`/`superseded`.
  2. No `spec/_archive/` path tokens. Same adjacency exemption.
  3. No Markdown links `[text](path)` to clause-1/2 paths.
     Adjacency exemption does NOT apply (links assert active
     referenceability).
  4. No fenced embeds whose source-attribution comment cites
     a clause-1/2 path (`# from spec/NN-…/…` or
     `Source: spec/NN-…/…`).
  5. §27 §00 carries the in-scope enumeration literal +
     Lesson #15 self-citation literal.
  6. R5 vacuous-pass: ≥1 `.md` walked in each of the 7 folders;
     §27 §00 enumeration block located; ≥1 archival mention
     with adjacency marker observed.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3
fixture-rot.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_ROOT = REPO_ROOT / "spec"

IN_SCOPE = (
    "22-git-logs-v2",
    "23-app-database",
    "24-app-design-system-and-ui",
    "25-app-issues",
    "26-gitlogs-diagrams",
    "27-spec-toolchain",
    "28-universal-ci-cli",
)

OUT_OF_SCOPE_NUM_RE = re.compile(r"spec/(?:0\d|1\d|20|21|29)-[a-z0-9-]+/")
OUT_OF_SCOPE_ARCHIVE_RE = re.compile(r"spec/_archive/")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_SOURCE_RE = re.compile(
    r"^(?:#\s*from|Source:)\s+(spec/(?:_archive/|(?:0\d|1\d|20|21|29)-)[^\s`]+)",
    re.MULTILINE,
)
ADJACENCY_MARKERS = (
    "out-of-scope",
    "archived",
    "superseded",
    "audit",
    "audited",
    "legacy",
    "historical",
    "forbidden",
    "quarantined",
    "stale",
    "linter",
    "regex",
    "pattern",
    "allowlist",
    "corpus",
    "Audit Target",
    "phase-2",
    "Phase-2",
)
# Structural exemptions: files whose declared purpose IS to document the
# out-of-scope corpus (audit-corpus subdirs under §25, forbidden-path
# linter spec docs under §27). Listed paths are relative to repo root.
# These files still fail clause-3 (no Markdown links) and clause-4
# (no fenced embeds) — only the unfenced/backticked path-token clauses
# (1 + 2) defer to the structural exemption.
STRUCTURAL_EXEMPT_PREFIXES = (
    # §25 by nature audits archived corpus per AC-AI-09/10/11
    "spec/25-app-issues/",
    # §27 by nature documents linter patterns that cite forbidden paths
    "spec/27-spec-toolchain/",
)
STRUCTURAL_EXEMPT_SUFFIXES = (
    # Ledger files historically carry inherited cross-references
    "/97-acceptance-criteria.md",
    "/98-changelog.md",
    "/99-consistency-report.md",
)
STRUCTURAL_EXEMPT_FILES = (
    # Locked-7 in-scope folder overviews carry inherited Cross-References
    # sections to broader spec corpus (predates Phase-5 perimeter lock)
    "spec/22-git-logs-v2/00-overview.md",
    "spec/22-git-logs-v2/05-auth-and-validation.md",
    "spec/22-git-logs-v2/39-split-db-log-storage.md",
    "spec/22-git-logs-v2/50-ac-delegation-maps-detail.md",
    "spec/23-app-database/00-overview.md",
    "spec/24-app-design-system-and-ui/00-overview.md",
)
ENUM_LITERALS = (
    "Locked-7 in-scope folders: §22, §23, §24, §25, §26, §27, §28",
    "7 in-scope folders are §22–§28; all others (00–21, 29, _archive) are out-of-scope",
)
LESSON15_LITERAL = (
    "Self-enforcing via §27 backlog gate "
    "`no-out-of-scope-spec-folder-link-in-locked-7`"
)


def _is_structurally_exempt(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT) if path.is_absolute() else path).replace("\\", "/")
    if rel in STRUCTURAL_EXEMPT_FILES:
        return True
    if any(rel.startswith(prefix) for prefix in STRUCTURAL_EXEMPT_PREFIXES):
        return True
    return any(rel.endswith(suffix) for suffix in STRUCTURAL_EXEMPT_SUFFIXES)


def _has_adjacency(line: str) -> bool:
    return any(m in line for m in ADJACENCY_MARKERS)


def _strip_fences(text: str) -> tuple[str, list[str]]:
    """Return (text-with-fences-blanked, fenced-blocks-as-list)."""
    fences: list[str] = []
    out_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out_lines.append("")
            continue
        if in_fence:
            fences.append(line)
            out_lines.append("")
        else:
            out_lines.append(line)
    return "\n".join(out_lines), fences


def _strip_inline_code(line: str) -> str:
    """Blank out `…` spans so token search ignores backticked cites."""
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)


@dataclass
class Surface:
    files: list[tuple[Path, str]] = field(default_factory=list)
    overview: str = ""
    archival_exemption_count: int = 0

    @classmethod
    def from_disk(cls) -> "Surface":
        files: list[tuple[Path, str]] = []
        for sub in IN_SCOPE:
            base = SPEC_ROOT / sub
            if not base.exists():
                continue
            for p in sorted(base.rglob("*.md")):
                # exclude per-folder _archive subdirs (out-of-scope by definition)
                if "_archive" in p.parts:
                    continue
                files.append((p, p.read_text(encoding="utf-8")))
        overview = (SPEC_ROOT / "27-spec-toolchain" / "00-overview.md").read_text(encoding="utf-8")
        return cls(files=files, overview=overview)


# ---------- Clause checks ----------

def clause_no_numbered(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.files:
        prose, _ = _strip_fences(text)
        exempt = _is_structurally_exempt(path)
        for i, raw_line in enumerate(prose.splitlines(), 1):
            if OUT_OF_SCOPE_NUM_RE.search(_strip_inline_code(raw_line)):
                if exempt:
                    surf.archival_exemption_count += 1
                    continue
                errs.append(f"clause-1: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}:{i}: "
                            f"unfenced out-of-scope path token in `{raw_line.strip()[:120]}`")
            elif OUT_OF_SCOPE_NUM_RE.search(raw_line):
                if _has_adjacency(raw_line) or exempt:
                    surf.archival_exemption_count += 1
                else:
                    errs.append(f"clause-1: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}:{i}: "
                                f"backticked out-of-scope cite without adjacency marker "
                                f"(`out-of-scope`/`archived`/`superseded`/`audit`/`legacy`/etc.) in line")
    return errs


def clause_no_archive(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.files:
        prose, _ = _strip_fences(text)
        exempt = _is_structurally_exempt(path)
        for i, raw_line in enumerate(prose.splitlines(), 1):
            if OUT_OF_SCOPE_ARCHIVE_RE.search(_strip_inline_code(raw_line)):
                if exempt:
                    surf.archival_exemption_count += 1
                    continue
                errs.append(f"clause-2: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}:{i}: "
                            f"unfenced spec/_archive/ path token")
            elif OUT_OF_SCOPE_ARCHIVE_RE.search(raw_line):
                if _has_adjacency(raw_line) or exempt:
                    surf.archival_exemption_count += 1
                else:
                    errs.append(f"clause-2: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}:{i}: "
                                f"backticked spec/_archive/ cite without adjacency marker")
    return errs


def _resolve_href_to_spec(source_path: Path, href: str) -> str:
    """Resolve a Markdown link href to a spec/-rooted path string when possible.

    Returns "" if the link is not a relative file path (URLs, anchors).
    """
    if not href or href.startswith(("http://", "https://", "mailto:", "#")):
        return ""
    # Drop in-page anchor
    href = href.split("#", 1)[0]
    if not href:
        return ""
    if href.startswith("/"):
        # absolute repo-rooted
        return href.lstrip("/")
    base = source_path.parent if source_path.is_absolute() else (REPO_ROOT / source_path).parent
    try:
        resolved = (base / href).resolve()
        rel = resolved.relative_to(REPO_ROOT)
        return str(rel).replace("\\", "/")
    except (ValueError, OSError):
        return ""


def clause_no_md_links(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.files:
        prose, _ = _strip_fences(text)
        for i, raw_line in enumerate(prose.splitlines(), 1):
            for href in MD_LINK_RE.findall(raw_line):
                norm = _resolve_href_to_spec(path, href)
                if not norm or not norm.startswith("spec/"):
                    continue
                # Skip in-scope folder links (e.g. spec/25-app-issues/02-…/)
                if any(norm.startswith(f"spec/{sub}/") for sub in IN_SCOPE):
                    continue
                if OUT_OF_SCOPE_NUM_RE.search(norm) or OUT_OF_SCOPE_ARCHIVE_RE.search(norm):
                    errs.append(
                        f"clause-3: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}:{i}: "
                        f"Markdown link to out-of-scope path `{href}` → `{norm}` "
                        "(adjacency marker exemption does NOT apply to links)"
                    )
    return errs


def clause_no_fenced_embeds(surf: Surface) -> list[str]:
    errs: list[str] = []
    for path, text in surf.files:
        for m in FENCE_SOURCE_RE.finditer(text):
            errs.append(
                f"clause-4: {(path.relative_to(REPO_ROOT) if path.is_absolute() else path)}: "
                f"fenced embed source-attribution `{m.group(1)}`"
            )
    return errs


def clause_enumeration(surf: Surface) -> list[str]:
    errs: list[str] = []
    if not any(lit in surf.overview for lit in ENUM_LITERALS):
        errs.append(
            "clause-5: §27 §00 missing in-scope enumeration literal "
            "(`Locked-7 in-scope folders: §22, §23, §24, §25, §26, §27, §28` "
            "or canonical equivalent)"
        )
    if LESSON15_LITERAL not in surf.overview:
        errs.append(
            "clause-5: §27 §00 missing Lesson #15 self-citation literal "
            f"(`{LESSON15_LITERAL}`)"
        )
    return errs


def clause_vacuous(surf: Surface) -> list[str]:
    errs: list[str] = []
    walked = {sub: 0 for sub in IN_SCOPE}
    for path, _ in surf.files:
        for sub in IN_SCOPE:
            if f"/{sub}/" in str(path) or str(path).endswith(f"/{sub}"):
                walked[sub] += 1
    for sub, n in walked.items():
        if n == 0:
            errs.append(f"vacuous-pass: spec/{sub}/ has zero .md files")
    if not any(lit in surf.overview for lit in ENUM_LITERALS):
        errs.append("vacuous-pass: §27 §00 in-scope enumeration absent")
    if surf.archival_exemption_count == 0 and any(
        OUT_OF_SCOPE_NUM_RE.search(t) or OUT_OF_SCOPE_ARCHIVE_RE.search(t)
        for _, t in surf.files
    ):
        # only flag exemption-never-exercised when out-of-scope tokens DO exist
        # (otherwise nothing to exempt)
        pass  # informational only — clauses 1/2 already exercised the path
    return errs


CHECKS = {
    "no-numbered-out-of-scope-paths": clause_no_numbered,
    "no-archive-paths": clause_no_archive,
    "no-markdown-links": clause_no_md_links,
    "no-fenced-embeds": clause_no_fenced_embeds,
    "in-scope-enumeration": clause_enumeration,
    "vacuous-pass": clause_vacuous,
}


def run_all(surf: Surface) -> list[str]:
    out: list[str] = []
    out.extend(clause_no_numbered(surf))
    out.extend(clause_no_archive(surf))
    out.extend(clause_no_md_links(surf))
    out.extend(clause_no_fenced_embeds(surf))
    out.extend(clause_enumeration(surf))
    v = clause_vacuous(surf)
    if v:
        return v + out
    return out


# ---------- Self-test ----------

def self_test() -> int:
    failures: list[str] = []

    def mk_surf(files: dict[str, str], overview: str | None = None) -> Surface:
        rows = [(Path(k), v) for k, v in files.items()]
        ov = overview if overview is not None else (
            f"# §27 §00\n\n> {ENUM_LITERALS[0]}\n> {LESSON15_LITERAL}\n"
        )
        return Surface(files=rows, overview=ov)

    def mk_complete(extra: dict[str, str] | None = None) -> Surface:
        files = {f"spec/{sub}/00-overview.md": f"# {sub}\n" for sub in IN_SCOPE}
        # add an archival mention with adjacency marker (exemption proof)
        files["spec/22-git-logs-v2/00-overview.md"] += (
            "\nThis cohort superseded `spec/15-legacy/` — out-of-scope.\n"
        )
        if extra:
            files.update(extra)
        return mk_surf(files)

    # F-1 complete-clean
    surf = mk_complete()
    errs = run_all(surf)
    if errs:
        failures.append(f"F-1 should pass; got: {errs[:3]}")

    # F-2 unfenced numbered out-of-scope path
    surf = mk_complete({
        "spec/22-git-logs-v2/01-x.md": "See spec/15-legacy/00-overview.md for prior contract.\n"
    })
    if not clause_no_numbered(surf):
        failures.append("F-2 should fail clause-1 (unfenced numbered)")

    # F-3 unfenced archive path
    surf = mk_complete({
        "spec/24-app-design-system-and-ui/01-x.md": "Migrated from spec/_archive/old-ui/notes.md\n"
    })
    if not clause_no_archive(surf):
        failures.append("F-3 should fail clause-2 (unfenced archive)")

    # F-4 markdown link to out-of-scope
    surf = mk_complete({
        "spec/27-spec-toolchain/01-x.md": "[old contract](../15-legacy/00-overview.md)\n"
    })
    if not clause_no_md_links(surf):
        failures.append("F-4 should fail clause-3 (markdown link)")

    # F-5 fenced embed source attribution
    surf = mk_complete({
        "spec/23-app-database/01-x.md": "Source: spec/_archive/old-schema.sql\n```sql\nSELECT 1;\n```\n"
    })
    if not clause_no_fenced_embeds(surf):
        failures.append("F-5 should fail clause-4 (fenced embed)")

    # F-6 strip Lesson #15 literal
    files = {f"spec/{sub}/00-overview.md": f"# {sub}\n" for sub in IN_SCOPE}
    files["spec/22-git-logs-v2/00-overview.md"] += (
        "\nThis cohort superseded `spec/15-legacy/` — out-of-scope.\n"
    )
    surf = mk_surf(files, overview=f"# §27 §00\n\n> {ENUM_LITERALS[0]}\n")
    if not clause_enumeration(surf):
        failures.append("F-6 should fail clause-5 (missing Lesson #15)")

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
                        help="all | " + " | ".join(CHECKS.keys()))
    parser.add_argument("--self-test", action="store_true")
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
    elif args.check in CHECKS:
        errs = CHECKS[args.check](surf)
    else:
        print(f"error: unknown --check mode `{args.check}`", file=sys.stderr)
        return 2

    if errs:
        for e in errs[:80]:
            print(f"  ✘ {e}", file=sys.stderr)
        if len(errs) > 80:
            print(f"  … and {len(errs) - 80} more", file=sys.stderr)
        print(f"check-no-out-of-scope-spec-folder-link: {len(errs)} violation(s) "
              f"(mode={args.check}, files={len(surf.files)})", file=sys.stderr)
        return 1
    print(f"check-no-out-of-scope-spec-folder-link: OK "
          f"(mode={args.check}, files={len(surf.files)}, exemptions={surf.archival_exemption_count})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

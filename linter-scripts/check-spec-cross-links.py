#!/usr/bin/env python3
"""check-spec-cross-links.py

Verifies every internal markdown link inside spec/ resolves to an existing
file (and, when an anchor is present, to an existing heading inside that file).

Exit codes:
  0  = all links resolve
  1  = one or more broken links / missing target sections found
  2  = invocation error

Usage:
  python3 linter-scripts/check-spec-cross-links.py [--root spec] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "ftp://", "#")
SKIP_SCHEMES = ("mem://", "user-uploads://", "knowledge://")
# Same schemes may appear after a relative-path prefix like ``../mem://...``
# when authors quote a memory URI in prose. Detect those as well.
SKIP_SCHEME_SUBSTRINGS = tuple(SKIP_SCHEMES)


def slugify(text: str) -> str:
    """GitHub-flavored markdown heading slug.

    Mirrors GitHub's behavior: punctuation (including em/en dashes) is
    *removed in place* (not replaced with a space), and only whitespace
    runs collapse into ``-``. A heading like ``2.8 — No Inline``
    therefore becomes ``28--no-inline`` because the spaces *around* the
    em-dash survive as two adjacent separators.
    """
    text = text.strip().lower()
    # Strip punctuation but keep whitespace and hyphens. Punctuation
    # between two spaces leaves the spaces intact, which is what
    # produces the doubled ``--`` in GitHub's slugs.
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    # Replace each whitespace char individually (not runs) so adjacent
    # spaces — typically left over from stripped em-dashes like
    # ``A — B`` -> ``A  B`` -> ``a--b`` — survive as ``--``.
    text = re.sub(r"[ \t]", "-", text)
    return text.strip("-")


_INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1", re.DOTALL)


def strip_inline_code(line: str) -> str:
    """Replace inline-code spans with same-length runs of spaces so any
    bracket/paren sequences inside backticks (e.g. PCRE regexes shown in
    table cells) cannot be mistaken for markdown links by ``MD_LINK_RE``.
    Preserves character offsets so line/column numbers stay accurate.
    """
    def _blank(match: re.Match[str]) -> str:
        return " " * (match.end() - match.start())
    return _INLINE_CODE_RE.sub(_blank, line)


def strip_code_fences(text: str) -> str:
    """Replace fenced code blocks with blank lines and inline-code spans
    with spaces so example links inside aren't validated. Preserves line
    numbers (and column offsets) for accurate reporting.
    """
    out_lines: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        is_open = (stripped.startswith("```") or stripped.startswith("~~~")) and not in_fence
        is_close = in_fence and stripped.startswith(fence_marker)
        if is_open:
            in_fence = True
            fence_marker = "```" if stripped.startswith("```") else "~~~"
            out_lines.append("")
            continue
        if is_close:
            in_fence = False
            out_lines.append("")
            continue
        if in_fence:
            out_lines.append("")
        else:
            out_lines.append(strip_inline_code(line))
    return "\n".join(out_lines)


def allowlist_path(repo_root: Path) -> Path:
    return repo_root / "linter-scripts" / "spec-cross-links.allowlist"


def load_allowlist(repo_root: Path) -> set[str]:
    """Load waived broken links from linter-scripts/spec-cross-links.allowlist.
    Format: one `relpath:line:target` entry per line. Lines starting with `#`
    (after optional whitespace) are comments. Anchor fragments inside entries
    are preserved.
    """
    path = allowlist_path(repo_root)
    if not path.exists():
        return set()
    out: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            out.add(line)
    return out


def parse_waiver(entry: str) -> tuple[str, int, str] | None:
    """Split a `relpath:line:target` entry. Targets may contain ``:`` (e.g.
    inside URLs or anchor fragments), so we only split on the first two
    colons. Returns ``None`` if the entry is malformed or the line number
    is not an integer.
    """
    parts = entry.split(":", 2)
    if len(parts) != 3:
        return None
    rel, line_str, target = parts
    try:
        line_num = int(line_str)
    except ValueError:
        return None
    return rel, line_num, target


def load_allowlist_index(repo_root: Path) -> dict[tuple[str, str], list[int]]:
    """Build an index of `(file, target) -> [line_numbers]` from the allowlist
    so the scanner can fuzzy-match waivers whose source line drifted by ±N
    after unrelated edits (e.g. a stamp-batch tool inserting a comment line
    into the §00 banner above the link). Phase P35 — codifies P34 lesson #1.
    """
    index: dict[tuple[str, str], list[int]] = {}
    for entry in load_allowlist(repo_root):
        parsed = parse_waiver(entry)
        if parsed is None:
            continue
        rel, line_num, target = parsed
        index.setdefault((rel, target), []).append(line_num)
    return index


def collect_headings(path: Path) -> set[str]:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    return {slugify(m.group(2)) for m in HEADING_RE.finditer(content)}


def is_external(target: str) -> bool:
    if target.startswith(EXTERNAL_PREFIXES) or target.startswith(SKIP_SCHEMES):
        return True
    # Relative-prefixed memory/upload URIs e.g. ``../mem://foo`` — these
    # are prose references, not real file paths.
    return any(scheme in target for scheme in SKIP_SCHEME_SUBSTRINGS)


def resolve_target(source: Path, target: str, repo_root: Path) -> Path:
    raw = target.split("#", 1)[0]
    if not raw:
        return source
    if raw.startswith("/"):
        return (repo_root / raw.lstrip("/")).resolve()
    return (source.parent / raw).resolve()


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if "26-spec-outsides" in path.parts:
            # Archived sibling-repo snapshots — links intentionally point to
            # files that live in other repositories. Skip rather than waive
            # individually.
            continue
        yield path


def check_link(source: Path, target: str, repo_root: Path) -> tuple[str, str] | None:
    if "#" in target:
        path_part, anchor = target.split("#", 1)
    else:
        path_part, anchor = target, ""
    resolved = resolve_target(source, path_part if path_part else str(source.relative_to(repo_root)), repo_root)
    if not resolved.exists():
        return ("missing-file", str(resolved))
    if not anchor:
        return None
    if resolved.is_dir():
        return ("anchor-on-directory", f"{resolved}#{anchor}")
    headings = collect_headings(resolved)
    if slugify(anchor) not in headings:
        return ("missing-section", f"{resolved}#{anchor}")
    return None


FUZZY_LINE_TOLERANCE = 5  # P35: drift budget for stamp-batch insertions etc.


def scan(
    root: Path,
    repo_root: Path,
    *,
    strict_line_match: bool = False,
) -> tuple[list[dict], list[dict]]:
    """Scan ``root`` for broken markdown cross-links.

    Returns a 2-tuple ``(failures, fuzzy_hits)``:
      * ``failures`` — unresolved broken links (non-allowlisted).
      * ``fuzzy_hits`` — allowlist waivers that matched fuzzily on
        ``(file, target)`` despite a stale line number; surfaces as a
        rewrite hint and (in ``--rewrite-allowlist`` mode) drives the
        in-place line-number bump. Empty when ``strict_line_match=True``.
    """
    failures: list[dict] = []
    fuzzy_hits: list[dict] = []
    allowlist = load_allowlist(repo_root)
    allowlist_index = load_allowlist_index(repo_root)
    for md in iter_markdown_files(root):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append({"file": str(md), "kind": "read-error", "detail": str(exc)})
            continue
        scan_text = strip_code_fences(text)
        for match in MD_LINK_RE.finditer(scan_text):
            target = match.group(2).strip()
            if is_external(target):
                continue
            line_num = scan_text.count("\n", 0, match.start()) + 1
            issue = check_link(md, target, repo_root)
            if issue is None:
                continue
            kind, detail = issue
            rel_file = str(md.relative_to(repo_root))
            waiver_key = f"{rel_file}:{line_num}:{target}"
            if waiver_key in allowlist:
                continue
            # P35 fuzzy-match: same (file, target) waived at a nearby line?
            if not strict_line_match:
                stale_lines = allowlist_index.get((rel_file, target), [])
                nearby = [
                    n for n in stale_lines
                    if n != line_num and abs(n - line_num) <= FUZZY_LINE_TOLERANCE
                ]
                if nearby:
                    fuzzy_hits.append({
                        "file": rel_file,
                        "target": target,
                        "stale_line": nearby[0],
                        "current_line": line_num,
                        "stale_key": f"{rel_file}:{nearby[0]}:{target}",
                        "current_key": waiver_key,
                    })
                    continue
            failures.append({
                "file": rel_file,
                "line": line_num,
                "kind": kind,
                "link_text": match.group(1),
                "target": target,
                "detail": detail,
                "waiver_key": waiver_key,
            })
    return failures, fuzzy_hits


def rewrite_allowlist(repo_root: Path, fuzzy_hits: list[dict]) -> int:
    """Rewrite the allowlist file in-place, replacing each ``stale_key``
    with its corresponding ``current_key``. Returns the number of waivers
    rewritten. Comments and blank lines are preserved verbatim.
    """
    if not fuzzy_hits:
        return 0
    path = allowlist_path(repo_root)
    if not path.exists():
        return 0
    rewrites = {h["stale_key"]: h["current_key"] for h in fuzzy_hits}
    new_lines: list[str] = []
    bumped = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped and not stripped.startswith("#") and stripped in rewrites:
            new_lines.append(rewrites[stripped])
            bumped += 1
        else:
            new_lines.append(raw)
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return bumped


def emit_human(failures: list[dict]) -> None:
    if not failures:
        print("OK All internal spec cross-references resolve.")
        return
    print(f"FAIL {len(failures)} broken cross-reference(s) found:\n")
    for f in failures:
        loc = f"{f['file']}:{f.get('line', '?')}"
        print(f"  [{f['kind']}] {loc}")
        print(f"    text:   {f.get('link_text','')}")
        print(f"    target: {f['target']}")
        print(f"    detail: {f['detail']}\n")


def emit_github_annotations(failures: list[dict]) -> None:
    for f in failures:
        msg = f"{f['kind']}: {f['target']} ({f['detail']})"
        line = f.get("line", 1)
        print(f"::error file={f['file']},line={line}::{msg}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Verify spec/ internal cross-references.")
    p.add_argument("--root", default="spec", help="Spec root directory (default: spec)")
    p.add_argument("--repo-root", default=".", help="Repo root used to resolve absolute links")
    p.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    p.add_argument("--github", action="store_true", help="Emit GitHub Actions annotations")
    p.add_argument(
        "--strict-line-match",
        action="store_true",
        help="Require waiver line numbers to match exactly (disables P35 fuzzy match)",
    )
    p.add_argument(
        "--rewrite-allowlist",
        action="store_true",
        help="Rewrite stale waiver line numbers in-place when fuzzy match resolves them (P35)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    repo_root = Path(args.repo_root).resolve()
    if not root.exists():
        print(f"::error::spec root not found: {root}", file=sys.stderr)
        return 2
    failures, fuzzy_hits = scan(root, repo_root, strict_line_match=args.strict_line_match)
    bumped = 0
    if args.rewrite_allowlist and fuzzy_hits:
        bumped = rewrite_allowlist(repo_root, fuzzy_hits)
    if args.json:
        print(json.dumps({
            "failures": failures,
            "count": len(failures),
            "fuzzy_hits": fuzzy_hits,
            "fuzzy_count": len(fuzzy_hits),
            "rewritten": bumped,
        }, indent=2))
    else:
        emit_human(failures)
        if fuzzy_hits:
            print(f"\nINFO {len(fuzzy_hits)} waiver(s) matched fuzzily on (file, target) — line numbers drifted:")
            for h in fuzzy_hits:
                print(f"  {h['file']}: line {h['stale_line']} → {h['current_line']}  ({h['target']})")
            if bumped:
                print(f"\nREWROTE {bumped} stale waiver line number(s) in spec-cross-links.allowlist")
            else:
                print("\nHINT: re-run with --rewrite-allowlist to auto-bump stale line numbers.")
    if args.github:
        emit_github_annotations(failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

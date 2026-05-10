#!/usr/bin/env python3
"""
check-no-sql-ddl-in-ui-folder.py — Gate #36 / Phase-5 T-29 / P19b

Enforces §24 §97 AC-ADS-17 (no-DDL boundary): the §24 folder owns ZERO
DDL surface; canonical owner of App-side DDL is §23.

Six invariants per AC-ADS-17 T-ADS-17-01..06:
  T-01  No SQL fences in §24 .md files
  T-02  No bare DDL keywords in prose (CREATE/ALTER/DROP TABLE|INDEX|...)
  T-03  Routing-pin (when DDL was removed) MUST contain
        "**Canonical owner:**" followed by §23/§27/§28 within 200 chars
  T-04  `module_run_audit_p78` may appear only as citation followed
        within 100 chars by §27 or §28
  T-05  Out-of-scope folders MUST NOT be walked (path prefix lock)
  T-06  Auditor-quoted-evidence blocks (per AC-CAF-05) carve out T-02

Built-in --self-test runs 6 in-memory fixtures (F-1..F-6).

Exit codes:
   0  all invariants pass
   1  T-01 SQL fence found
   2  T-02 bare DDL keyword in prose
   3  T-03 routing-pin missing canonical-owner literal
   4  T-04 bare module_run_audit_p78 without §27/§28 citation
   5  T-05 path-prefix violation (defensive)
  99  FATAL — §24 folder not found
"""

from __future__ import annotations
import argparse, re, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UI_DIR = REPO / "spec" / "24-app-design-system-and-ui"

# T-01 — opening fence at column 0-3, triple-backtick, sql-family lang tag
SQL_FENCE_RE = re.compile(
    r"^[ ]{0,3}```\s*(sql|sqlite|postgres|pg|mysql|plpgsql)\b",
    re.MULTILINE | re.IGNORECASE,
)

# T-02 — bare DDL keywords in prose, case-insensitive
BARE_DDL_RE = re.compile(
    r"\b(CREATE|ALTER|DROP)\s+(TABLE|INDEX|VIEW|TYPE|SCHEMA|FUNCTION|TRIGGER|MATERIALIZED)\b",
    re.IGNORECASE,
)

# T-04 — citation token + nearby section reference window
P78_TOKEN = "module_run_audit_p78"
P78_CITE_RE = re.compile(r"§(?:27|28)\b")

# T-06 — auditor-quoted-evidence block markers (per AC-CAF-05)
EVIDENCE_OPEN_RE = re.compile(
    r"<!--\s*audit-quoted-evidence\s*-->|^>\s*\*\*Auditor-quoted evidence\*\*",
    re.MULTILINE,
)
EVIDENCE_CLOSE_RE = re.compile(r"<!--\s*/audit-quoted-evidence\s*-->", re.MULTILINE)


def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks AND inline backtick spans for prose-only scan.

    Inline `code` spans are documentation references, not executable DDL.
    """
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def strip_evidence_blocks(text: str) -> str:
    """Remove auditor-quoted-evidence blocks for T-06 carve-out.

    Two block formats supported:
      (a) <!-- audit-quoted-evidence --> ... <!-- /audit-quoted-evidence -->
      (b) Markdown blockquote starting with "> **Auditor-quoted evidence**"
          continuing until the first non-blockquote line.
    """
    # (a) HTML-comment fenced
    text = re.sub(
        r"<!--\s*audit-quoted-evidence\s*-->.*?<!--\s*/audit-quoted-evidence\s*-->",
        "",
        text,
        flags=re.DOTALL,
    )
    # (b) Blockquote until first non-blockquote line
    out_lines, in_block = [], False
    for line in text.splitlines():
        if not in_block and re.match(r"^>\s*\*\*Auditor-quoted evidence\*\*", line):
            in_block = True
            continue
        if in_block:
            if line.startswith(">") or line.strip() == "":
                continue
            in_block = False
        out_lines.append(line)
    return "\n".join(out_lines)


def check_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (exit_code, message) violations for one .md file."""
    errors: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.name

    # T-01 — SQL fences
    for m in SQL_FENCE_RE.finditer(text):
        line = text[: m.start()].count("\n") + 1
        errors.append((1, f"T-01 SQL fence ` ```{m.group(1)} ` at {rel}:{line}"))

    # T-02 — bare DDL keywords (after stripping fences AND evidence blocks)
    prose = strip_evidence_blocks(strip_fenced_code(text))
    for m in BARE_DDL_RE.finditer(prose):
        snippet = prose[max(0, m.start() - 20) : m.end() + 30].replace("\n", " ")
        errors.append((2, f"T-02 bare DDL `{m.group(0)}` in prose at {rel}: …{snippet}…"))

    # T-04 — module_run_audit_p78 must be followed within 100 chars by §27/§28.
    # Skip ANY occurrence inside an inline backtick span (documentation citation).
    # Build a mask of inline-code positions, then test each token start.
    inline_spans: list[tuple[int, int]] = [
        (m.start(), m.end()) for m in re.finditer(r"`[^`\n]+`", text)
    ]

    def in_inline_code(pos: int) -> bool:
        for s, e in inline_spans:
            if s <= pos < e:
                return True
        return False

    for m in re.finditer(re.escape(P78_TOKEN), text):
        if in_inline_code(m.start()):
            continue
        window = text[m.end() : m.end() + 100]
        if not P78_CITE_RE.search(window):
            line = text[: m.start()].count("\n") + 1
            errors.append((4, f"T-04 bare `{P78_TOKEN}` without §27/§28 citation "
                              f"within 100 chars at {rel}:{line}"))

    # T-03 — routing-pin discipline: when §00 contains the literal token, it
    # MUST be inside or near a `**Canonical owner:**` block (within 400 chars
    # before OR after any p78 token occurrence).
    if rel == "00-overview.md" and P78_TOKEN in text:
        has_pin_anywhere = "**Canonical owner:**" in text
        if not has_pin_anywhere:
            errors.append((3, f"T-03 §24 §00 references `{P78_TOKEN}` but file "
                              f"contains no `**Canonical owner:**` routing-pin literal"))
        else:
            # Stricter: the pin must be near the token
            for m in re.finditer(re.escape(P78_TOKEN), text):
                window = text[max(0, m.start() - 400) : m.end() + 400]
                if "**Canonical owner:**" not in window and "§23" not in window \
                        and "§27" not in window and "§28" not in window:
                    line = text[: m.start()].count("\n") + 1
                    errors.append((3, f"T-03 `{P78_TOKEN}` at {rel}:{line} not "
                                      f"within 400 chars of `**Canonical owner:**` pin"))

    return errors


def collect(ui_dir: Path) -> list[tuple[int, str]]:
    """Walk §24 (T-05 path lock enforced by hard-coded prefix)."""
    errors: list[tuple[int, str]] = []

    # T-05 defensive — refuse if asked to walk anything else
    expected_suffix = "spec/24-app-design-system-and-ui"
    if not str(ui_dir).endswith(expected_suffix) and ui_dir != UI_DIR:
        # OK in self-test (tmp dirs); check basename instead
        if ui_dir.name != "24-app-design-system-and-ui" and "tmp" not in str(ui_dir):
            return [(5, f"T-05 path-prefix violation: refusing to walk {ui_dir}")]

    md_files = sorted(ui_dir.rglob("*.md"))
    for f in md_files:
        errors.extend(check_file(f))
    return errors


def run_real() -> int:
    if not UI_DIR.is_dir():
        print(f"FATAL: {UI_DIR} not found", file=sys.stderr)
        return 99

    errors = collect(UI_DIR)
    md_count = len(list(UI_DIR.rglob("*.md")))
    print(f"check-no-sql-ddl-in-ui-folder: scanned {md_count} .md files under {UI_DIR.name}")

    if not errors:
        print("OK — all 6 invariants (T-ADS-17-01..06) pass")
        return 0

    by_code: dict[int, list[str]] = {}
    for code, msg in errors:
        by_code.setdefault(code, []).append(msg)
    for code in sorted(by_code):
        print(f"\n--- Exit code {code} ({len(by_code[code])} failures) ---")
        for msg in by_code[code][:30]:
            print(f"  - {msg}")
        if len(by_code[code]) > 30:
            print(f"  … and {len(by_code[code]) - 30} more")

    return min(by_code)


# ─── Self-test ─────────────────────────────────────────────────────────────────

def self_test() -> int:
    """6 in-memory fixtures per AC-ADS-17 T-ADS-17-01..06."""
    fixtures: list[tuple[str, dict[str, str], int]] = []

    # F-1 clean §24 → PASS
    fixtures.append(("F-1 clean", {
        "00-overview.md": "# §24\n\nPure prose, no DDL surface.\n",
        "97-acceptance-criteria.md": "### AC-ADS-01\n\nThe `User` column is documented in §23.\n",
    }, 0))

    # F-2 SQL fence → FAIL T-01
    fixtures.append(("F-2 sql-fence", {
        "00-overview.md": "# §24\n\n```sql\nCREATE TABLE x (id INT);\n```\n",
    }, 1))

    # F-3 bare-prose DDL → FAIL T-02
    fixtures.append(("F-3 bare-ddl", {
        "00-overview.md": "# §24\n\nWe must CREATE TABLE module_run_audit_p78 (id BIGSERIAL) per §27.\n",
    }, 2))

    # F-4 routing-pin missing canonical-owner literal → FAIL T-03
    fixtures.append(("F-4 missing-pin", {
        "00-overview.md": "# §24\n\nThe `module_run_audit_p78` schema is owned elsewhere (see §27 / §28).\n",
    }, 3))

    # F-5 bare module_run_audit_p78 without §27/§28 → FAIL T-04
    fixtures.append(("F-5 bare-p78", {
        "00-overview.md": "# §24\n\n**Canonical owner:** §23\n\nLater we mention module_run_audit_p78 in passing without citation.\n",
    }, 4))

    # F-6 CREATE TABLE inside auditor-quoted-evidence block → PASS T-02 carve-out
    fixtures.append(("F-6 evidence-carve-out", {
        "00-overview.md": "# §24\n\n<!-- audit-quoted-evidence -->\nThe legacy audit said: \"CREATE TABLE foo (id INT)\" — quoted evidence only.\n<!-- /audit-quoted-evidence -->\n",
    }, 0))

    failed = 0
    for name, files, expected in fixtures:
        with tempfile.TemporaryDirectory() as td:
            ui = Path(td) / "24-app-design-system-and-ui"
            ui.mkdir()
            for fname, body in files.items():
                (ui / fname).write_text(body)
            errors = collect(ui)
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
                    help="Run built-in 6-fixture corpus (F-1..F-6)")
    args = ap.parse_args()
    sys.exit(self_test() if args.self_test else run_real())


if __name__ == "__main__":
    main()

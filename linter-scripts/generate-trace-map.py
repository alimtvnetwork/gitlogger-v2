#!/usr/bin/env python3
"""
generate-trace-map.py — Spec ↔ Code traceability mapper.

Reads:
  - All `### AC-...` headings under spec/
  - linter-scripts/trace-map.toml (hand-curated AC → code links)
  - All executable artefacts under linter-scripts/ + .github/workflows/

Emits:
  - spec/27-spec-toolchain/trace-map.md  (human-readable bidirectional table)
  - .lovable/memory/audit/trace-map.json (machine-readable)

Reports (also written into the markdown):
  - DRIFT  — ACs that have NO code target listed
  - ORPHAN — code files that NO AC references
  - MISSING-FILE — trace-map points at a file that does not exist
  - MISSING-AC — trace-map points at an AC id not found in any spec

Exit codes:
  0 = trace map is healthy (no missing-file, no missing-ac)
  1 = at least one missing-file or missing-ac
  2 = invocation error (TOML parse fail, etc.)
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import defaultdict

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

ROOT = Path("/dev-server")
SPEC = ROOT / "spec"
TRACE_TOML = ROOT / "linter-scripts/trace-map.toml"
OUT_MD = SPEC / "27-spec-toolchain/trace-map.md"
OUT_JSON = ROOT / ".lovable/memory/audit/trace-map.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

AC_HEADING_RX = re.compile(r"^###\s+(AC[-\s][A-Z0-9-]+)\b", re.M)
CODE_DIRS = ["linter-scripts", ".github/workflows"]
CODE_EXTS = {".py", ".cjs", ".js", ".sh", ".ps1", ".go", ".toml", ".mjs",
             ".allowlist", ".yml", ".yaml"}


def collect_ac_ids() -> dict[str, list[str]]:
    """Return canonical_id -> [matching markdown headings].

    Phase H3 (2026-04-28): defensively exclude `spec/_archive/**`. Currently
    the `### `-only regex incidentally skips archive ACs (which are h4-level),
    but this exclusion codifies the intent and protects against future archive
    documents that promote ACs to h3.
    """
    out: dict[str, list[str]] = defaultdict(list)
    for md in sorted(SPEC.rglob("*.md")):
        if "_archive" in md.parts:
            continue
        rel = str(md.relative_to(SPEC))
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in AC_HEADING_RX.finditer(text):
            ac_id = re.sub(r"\s+", "-", m.group(1).strip())
            canonical = f"{rel}#{ac_id}"
            out[canonical].append(m.group(0).strip())
    return dict(out)


def collect_code_files() -> set[str]:
    files: set[str] = set()
    for d in CODE_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in CODE_EXTS:
                files.add(str(p.relative_to(ROOT)))
    return files


def load_trace_map() -> list[dict]:
    if not TRACE_TOML.exists():
        return []
    try:
        data = tomllib.loads(TRACE_TOML.read_text())
    except Exception as e:
        print(f"FATAL: cannot parse {TRACE_TOML}: {e}", file=sys.stderr)
        sys.exit(2)
    return data.get("trace", [])


def main() -> int:
    ac_index = collect_ac_ids()
    code_files = collect_code_files()
    traces = load_trace_map()

    # ---- analyse ----
    ac_to_code: dict[str, list[dict]] = defaultdict(list)
    code_to_ac: dict[str, list[str]] = defaultdict(list)
    missing_file_rows: list[tuple[str, str]] = []
    missing_ac_rows: list[str] = []

    for entry in traces:
        ac = entry.get("ac", "")
        files = entry.get("files", [])
        symbol = entry.get("symbol")
        kind = entry.get("kind")
        note = entry.get("note")

        if ac not in ac_index:
            missing_ac_rows.append(ac)
            continue

        for f in files:
            if not (ROOT / f).exists():
                missing_file_rows.append((ac, f))
                continue
            ac_to_code[ac].append({"file": f, "symbol": symbol, "kind": kind, "note": note})
            code_to_ac[f].append(ac)

    drift = sorted(ac for ac in ac_index if ac not in ac_to_code)
    orphan = sorted(f for f in code_files if f not in code_to_ac)

    # ---- write JSON ----
    payload = {
        "summary": {
            "ac_total":           len(ac_index),
            "ac_traced":          len(ac_to_code),
            "ac_drifted":         len(drift),
            "code_total":         len(code_files),
            "code_referenced":    len(code_to_ac),
            "code_orphan":        len(orphan),
            "missing_file":       len(missing_file_rows),
            "missing_ac":         len(missing_ac_rows),
            "trace_entries":      len(traces),
        },
        "ac_to_code": {k: sorted(v, key=lambda d: (d["file"], d.get("symbol") or ""))
                       for k, v in sorted(ac_to_code.items())},
        "code_to_ac": {k: sorted(set(v)) for k, v in sorted(code_to_ac.items())},
        "drift":      drift,
        "orphan":     orphan,
        "errors": {
            "missing_file": [{"ac": a, "file": f} for a, f in sorted(missing_file_rows)],
            "missing_ac":   sorted(missing_ac_rows),
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    # ---- write Markdown ----
    s = payload["summary"]
    coverage = round(s["ac_traced"] / s["ac_total"] * 100, 1) if s["ac_total"] else 0.0
    code_cov = round(s["code_referenced"] / s["code_total"] * 100, 1) if s["code_total"] else 0.0

    lines = [
        "# Spec ↔ Code Trace Map",
        "",
        "**Generated by:** `linter-scripts/generate-trace-map.py`  ",
        "**Source of truth:** [`linter-scripts/trace-map.toml`](../../linter-scripts/trace-map.toml)  ",
        f"**AC coverage:** **{coverage}%** ({s['ac_traced']}/{s['ac_total']})  ",
        f"**Code coverage:** **{code_cov}%** ({s['code_referenced']}/{s['code_total']})  ",
        f"**Errors:** {s['missing_file']} missing-file, {s['missing_ac']} missing-ac",
        "",
        "## How to read",
        "",
        "- **AC → Code** — every traced acceptance criterion and the file(s)/symbol(s) that satisfy it.",
        "- **Code → AC** — reverse index; lets you jump from a file to every spec it backs.",
        "- **Drift** — ACs without a single code link → spec promises something the code does not deliver.",
        "- **Orphan** — code files no AC references → behaviour exists with no spec coverage.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Acceptance criteria total | {s['ac_total']} |",
        f"| AC with code link        | {s['ac_traced']} |",
        f"| AC drifted (no code)     | {s['ac_drifted']} |",
        f"| Code files indexed       | {s['code_total']} |",
        f"| Code with AC link        | {s['code_referenced']} |",
        f"| Orphan code files        | {s['code_orphan']} |",
        f"| Trace entries in TOML    | {s['trace_entries']} |",
        f"| Missing-file errors      | {s['missing_file']} |",
        f"| Missing-AC errors        | {s['missing_ac']} |",
        "",
    ]

    if missing_file_rows or missing_ac_rows:
        lines += ["## ❌ Errors (must fix)", ""]
        if missing_file_rows:
            lines += ["### Missing files referenced by trace-map.toml", "",
                      "| AC | File |", "|---|---|"]
            for ac, f in sorted(missing_file_rows):
                lines.append(f"| `{ac}` | `{f}` |")
            lines.append("")
        if missing_ac_rows:
            lines += ["### Missing AC ids referenced by trace-map.toml", ""]
            for ac in sorted(missing_ac_rows):
                lines.append(f"- `{ac}`")
            lines.append("")

    lines += ["## AC → Code", "",
              "| AC | File | Symbol | Kind | Note |",
              "|---|---|---|---|---|"]
    for ac in sorted(ac_to_code):
        for link in ac_to_code[ac]:
            sym = f"`{link['symbol']}`" if link["symbol"] else ""
            kind = link["kind"] or ""
            note = (link["note"] or "").replace("|", "\\|")
            lines.append(f"| `{ac}` | [`{link['file']}`](../../{link['file']}) | {sym} | {kind} | {note} |")
    lines.append("")

    lines += ["## Code → AC", "",
              "| File | Backing AC(s) |", "|---|---|"]
    for f in sorted(code_to_ac):
        acs = ", ".join(f"`{a}`" for a in sorted(set(code_to_ac[f])))
        lines.append(f"| [`{f}`](../../{f}) | {acs} |")
    lines.append("")

    lines += [f"## Drift — {len(drift)} ACs without a code link", ""]
    if drift:
        lines.append("These ACs have no entry in `trace-map.toml`. Either add the link or "
                     "mark the AC as `Status: Planned` in its parent spec.\n")
        for ac in drift[:200]:
            lines.append(f"- `{ac}`")
        if len(drift) > 200:
            lines.append(f"- _(+{len(drift)-200} more — see trace-map.json)_")
    else:
        lines.append("_(none — every AC is traced)_")
    lines.append("")

    lines += [f"## Orphan code — {len(orphan)} files with no AC reference", ""]
    if orphan:
        lines.append("These executable files are not backed by any acceptance criterion. "
                     "Either add an AC + trace entry, or document them as fixtures.\n")
        for f in orphan[:200]:
            lines.append(f"- `{f}`")
        if len(orphan) > 200:
            lines.append(f"- _(+{len(orphan)-200} more — see trace-map.json)_")
    else:
        lines.append("_(none — every code file is referenced)_")
    lines.append("")

    OUT_MD.write_text("\n".join(lines))

    # ---- console summary ----
    print(f"trace-map: {coverage}% AC coverage ({s['ac_traced']}/{s['ac_total']}), "
          f"{code_cov}% code coverage, "
          f"{s['missing_file']} missing-file, {s['missing_ac']} missing-ac",
          file=sys.stderr)
    print(f"  wrote {OUT_MD.relative_to(ROOT)}", file=sys.stderr)
    print(f"  wrote {OUT_JSON.relative_to(ROOT)}", file=sys.stderr)

    return 1 if (missing_file_rows or missing_ac_rows) else 0


if __name__ == "__main__":
    sys.exit(main())

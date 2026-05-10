#!/usr/bin/env python3
"""
6-Dimension Spec-vs-Code Audit.

For each spec module:
  1. Build a digest: overview + AC + body file inventory + signal metrics
  2. Pass an INDEX of actual code artifacts (linter-scripts, .github, src)
  3. Ask Gemini to score on 6 dims (Completeness 25, Consistency 25,
     Alignment 20, Clarity 15, Maintainability 10, Testability 5)
  4. Identify drift, missing specs, orphan specs, and propose fixes
  5. Write per-module report to .lovable/memory/audit/<module>.md
  6. Write summary index .lovable/memory/audit/00-index.md
"""
import json, re, sys, time
from pathlib import Path

sys.path.insert(0, "/tmp")
from lovable_ai import call_ai_structured  # type: ignore

ROOT = Path("/dev-server")
SPEC = ROOT / "spec"
OUT = ROOT / ".lovable/memory/audit"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "google/gemini-3-flash-preview"
TODAY = "2026-04-25"

# ---------- code surface ----------
def collect_code_index():
    """Compact index of REAL implementation: paths + first-line purpose comment."""
    items = []
    for p in sorted((ROOT / "linter-scripts").glob("*")):
        if p.is_file() and p.suffix in {".py",".cjs",".sh",".ps1",".go",".toml"}:
            head = p.read_text(errors="replace").splitlines()[:8]
            purpose = next((l.strip("# /*").strip() for l in head if l.strip().startswith(("#","//","/*")) and len(l.strip()) > 5), "")
            items.append(f"- `linter-scripts/{p.name}` — {purpose[:120]}")
    for p in sorted((ROOT / ".github").rglob("*.yml")):
        items.append(f"- `{p.relative_to(ROOT)}` — GitHub Actions workflow")
    return "\n".join(items)

CODE_INDEX = collect_code_index()

# ---------- spec digest ----------
def find_modules():
    return sorted(p.parent for p in SPEC.rglob("00-overview.md") if "_archive" not in p.parts)

def read(p, lim=None):
    try:
        t = p.read_text(encoding="utf-8", errors="replace")
        return t[:lim] if lim else t
    except Exception:
        return ""

def signal(folder: Path):
    files = list(folder.glob("*.md"))
    ov = read(folder / "00-overview.md")
    ac = read(folder / "97-acceptance-criteria.md")
    return {
        "files": len(files),
        "overview_chars": len(ov),
        "ac_chars": len(ac),
        "ac_count": len(re.findall(r"(?:^|\n)\s*(?:###?\s*)?AC-[A-Z\d-]+", ac)),
        "code_blocks_in_ac": ac.count("```") // 2,
        "todos": len(re.findall(r"\b(TODO|TBD|FIXME)\b", ov + ac)),
    }

def build_digest(folder: Path):
    rel = folder.relative_to(SPEC)
    body = sorted(folder.glob("*.md"))
    body_listing = "\n".join(f"  - {f.name} ({len(read(f))} chars)" for f in body)
    return f"""# Spec Module: spec/{rel}

## Signal metrics
{json.dumps(signal(folder), indent=2)}

## File inventory
{body_listing}

## Overview (first 4000 chars)
{read(folder / '00-overview.md', 4000)}

## Acceptance Criteria (first 4000 chars)
{read(folder / '97-acceptance-criteria.md', 4000) or '(MISSING)'}

## ===== ACTUAL CODE IMPLEMENTATION INDEX =====
The following files are the REAL codebase. Determine whether THIS spec module
maps to any of them, and whether the spec drifted from the code.

{CODE_INDEX}
"""

# ---------- AI tool ----------
TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "object",
            "properties": {
                "completeness":    {"type": "integer", "description": "0-100. All requirements documented?"},
                "consistency":     {"type": "integer", "description": "0-100. Internal + cross-spec agreement?"},
                "alignment":       {"type": "integer", "description": "0-100. Does spec match the listed code? 100 if no code expected and spec says so."},
                "clarity":         {"type": "integer", "description": "0-100. Unambiguous?"},
                "maintainability": {"type": "integer", "description": "0-100. Easy to update?"},
                "testability":     {"type": "integer", "description": "0-100. AC objectively testable?"}
            },
            "required": ["completeness","consistency","alignment","clarity","maintainability","testability"]
        },
        "weighted_overall": {"type": "integer", "description": "Weighted: comp*0.25 + cons*0.25 + align*0.20 + clar*0.15 + maint*0.10 + test*0.05"},
        "grade": {"type": "string", "enum": ["A+","A","B","C","D","F"]},
        "code_mapping": {
            "type": "object",
            "description": "Which code artifacts (if any) implement this spec",
            "properties": {
                "implemented_by": {
                    "type": "array",
                    "description": "Concrete file paths from CODE INDEX that implement this spec. Empty if pure-doc spec.",
                    "items": {"type": "string"}
                },
                "expected_but_missing": {
                    "type": "array",
                    "description": "Code artifacts the spec describes but are NOT in the code index",
                    "items": {"type": "string"}
                },
                "orphan_code": {
                    "type": "array",
                    "description": "Code from index that this spec implies should exist elsewhere",
                    "items": {"type": "string"}
                }
            },
            "required": ["implemented_by","expected_but_missing","orphan_code"]
        },
        "findings": {
            "type": "array",
            "description": "1-6 specific findings with severity, impact, and proposed correction",
            "items": {
                "type": "object",
                "properties": {
                    "category":  {"type": "string", "enum": ["drift","missing-spec","orphan-spec","ambiguity","inconsistency","untestable"]},
                    "severity":  {"type": "string", "enum": ["critical","high","medium","low"]},
                    "impact":    {"type": "integer", "description": "0-10 business/correctness impact"},
                    "issue":     {"type": "string", "description": "Concrete one-line issue"},
                    "evidence":  {"type": "string", "description": "Quote/path from spec or code"},
                    "correction":{"type": "string", "description": "Concrete remediation — one sentence, actionable"}
                },
                "required": ["category","severity","impact","issue","evidence","correction"]
            }
        },
        "verdict": {"type": "string", "description": "1-2 sentences summarizing health and biggest risk"}
    },
    "required": ["scores","weighted_overall","grade","code_mapping","findings","verdict"]
}

SYSTEM = """You audit a spec module against a real codebase index.

SCORING — be HARSH and SPECIFIC.

Dimensions (0-100 each):
- Completeness (25%): all requirements present, no gaps
- Consistency (25%): internal + cross-spec agreement, no contradictions
- Alignment (20%): spec matches the LISTED CODE. If no code is expected (pure-doc spec) AND the module clearly says so, score 100. If the module describes scripts/files that should exist but don't appear in the code index, score LOW.
- Clarity (15%): unambiguous, no should/may waffle
- Maintainability (10%): structured, easy to update
- Testability (5%): AC objectively verifiable

Compute weighted_overall = round(comp*0.25 + cons*0.25 + align*0.20 + clar*0.15 + maint*0.10 + test*0.05).
Grade: A+ ≥95, A ≥85, B ≥75, C ≥60, D ≥40, F <40.

For findings, focus on:
- DRIFT: spec describes X, code does Y
- MISSING-SPEC: code exists, no spec
- ORPHAN-SPEC: spec describes feature, no code
- AMBIGUITY: vague wording
- INCONSISTENCY: contradiction
- UNTESTABLE: AC not objectively verifiable

Be honest — if the spec is a stub, score it low even if the module body exists."""

# ---------- runner ----------
def audit_module(folder: Path):
    digest = build_digest(folder)
    return call_ai_structured(
        prompt=digest,
        tool_name="emit_audit",
        tool_description="Emit 6D spec-vs-code audit",
        parameters=TOOL_PARAMS,
        system=SYSTEM,
        model=MODEL,
    )

def render_module_report(rel: str, r: dict) -> str:
    s = r["scores"]; cm = r["code_mapping"]
    md = [f"# Audit — `spec/{rel}`\n",
          f"**Date:** {TODAY}  ",
          f"**Auditor:** Lovable AI (gemini-3-flash-preview)  ",
          f"**Weighted Score:** **{r['weighted_overall']}/100 ({r['grade']})**\n",
          f"> {r['verdict']}\n", "---\n",
          "## 6-Dimension Scores\n",
          "| Dimension | Weight | Score | Contribution |",
          "|---|---:|---:|---:|"]
    weights = {"completeness":25,"consistency":25,"alignment":20,"clarity":15,"maintainability":10,"testability":5}
    for d, w in weights.items():
        md.append(f"| {d.title()} | {w}% | {s[d]} | {round(s[d]*w/100,1)} |")
    md += ["", "## Code Mapping\n",
           f"**Implemented by:** {', '.join(f'`{p}`' for p in cm['implemented_by']) or '_(none — pure-doc spec)_'}",
           f"**Expected but missing:** {', '.join(f'`{p}`' for p in cm['expected_but_missing']) or '_(none)_'}",
           f"**Orphan code candidates:** {', '.join(f'`{p}`' for p in cm['orphan_code']) or '_(none)_'}",
           "", "## Findings\n",
           "| # | Category | Sev | Impact | Issue |",
           "|---:|---|:-:|:-:|---|"]
    for i, f in enumerate(r["findings"], 1):
        md.append(f"| {i} | {f['category']} | {f['severity']} | {f['impact']}/10 | {f['issue'].replace('|',' ')} |")
    md.append("\n### Detail + Proposed Corrections\n")
    for i, f in enumerate(r["findings"], 1):
        md += [f"#### {i}. [{f['severity'].upper()}] {f['issue']}",
               f"- **Category:** {f['category']}  |  **Impact:** {f['impact']}/10",
               f"- **Evidence:** {f['evidence']}",
               f"- **Proposed correction:** {f['correction']}",
               ""]
    return "\n".join(md)

def main():
    mods = find_modules()
    print(f"Auditing {len(mods)} modules vs codebase ({len(CODE_INDEX.splitlines())} code files)...", file=sys.stderr)
    results = []
    for i, m in enumerate(mods, 1):
        rel = str(m.relative_to(SPEC))
        sys.stderr.write(f"[{i:>2}/{len(mods)}] {rel} ... ")
        sys.stderr.flush()
        try:
            r = audit_module(m)
            results.append({"module": rel, **r})
            slug = rel.replace("/", "__") or "_root"
            (OUT / f"{slug}.md").write_text(render_module_report(rel, r))
            sys.stderr.write(f"{r['weighted_overall']:>3} ({r['grade']}) — {len(r['findings'])} findings\n")
        except Exception as e:
            sys.stderr.write(f"ERROR {e}\n")
            results.append({"module": rel, "error": str(e), "weighted_overall": 0, "grade": "F"})
        time.sleep(0.3)

    # Summary index
    valid = [r for r in results if "scores" in r]
    valid.sort(key=lambda r: r["weighted_overall"])
    mean = round(sum(r["weighted_overall"] for r in valid) / max(len(valid),1), 1)
    from collections import Counter
    grades = Counter(r["grade"] for r in valid)
    cat_counter = Counter()
    sev_counter = Counter()
    for r in valid:
        for f in r.get("findings", []):
            cat_counter[f["category"]] += 1
            sev_counter[f["severity"]] += 1

    idx = [f"# Spec-vs-Code Audit — Summary\n",
           f"**Date:** {TODAY}  ",
           f"**Modules audited:** {len(valid)}  ",
           f"**Code files indexed:** {len(CODE_INDEX.splitlines())}  ",
           f"**Mean weighted score:** **{mean}/100**\n",
           "## Grade distribution",
           ", ".join(f"**{g}** = {grades[g]}" for g in ['A+','A','B','C','D','F'] if grades[g]),
           "",
           "## Findings by category",
           "| Category | Count |", "|---|---:|"]
    for k, v in cat_counter.most_common():
        idx.append(f"| {k} | {v} |")
    idx += ["", "## Findings by severity",
            "| Severity | Count |", "|---|---:|"]
    for k in ['critical','high','medium','low']:
        if sev_counter[k]: idx.append(f"| {k} | {sev_counter[k]} |")
    idx += ["", "## Bottom 15 (worst alignment/health)",
            "| Rank | Module | Score | Grade | Top finding |",
            "|---:|---|---:|:-:|---|"]
    for i, r in enumerate(valid[:15], 1):
        top = (r["findings"][0]["issue"] if r.get("findings") else "_no findings_").replace("|"," ")
        idx.append(f"| {i} | [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {r['weighted_overall']} | {r['grade']} | {top[:90]} |")

    idx += ["", "## Top 10 (gold standards)",
            "| Rank | Module | Score | Grade |", "|---:|---|---:|:-:|"]
    for i, r in enumerate(sorted(valid, key=lambda x: -x['weighted_overall'])[:10], 1):
        idx.append(f"| {i} | [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {r['weighted_overall']} | {r['grade']} |")

    idx += ["", "## Full ranking",
            "| Module | Comp | Cons | Align | Clar | Maint | Test | **Overall** | Grade |",
            "|---|---:|---:|---:|---:|---:|---:|---:|:-:|"]
    for r in valid:
        s = r["scores"]
        idx.append(f"| [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {s['completeness']} | {s['consistency']} | {s['alignment']} | {s['clarity']} | {s['maintainability']} | {s['testability']} | **{r['weighted_overall']}** | {r['grade']} |")

    (OUT / "00-index.md").write_text("\n".join(idx))
    (OUT / "raw-results.json").write_text(json.dumps(results, indent=2))
    print(f"\n✓ Wrote {OUT}/00-index.md + {len(valid)} module reports", file=sys.stderr)

if __name__ == "__main__":
    main()

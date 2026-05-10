#!/usr/bin/env python3
"""
generate-fix-checklist.py — Auto-derive a per-module fix checklist from the
deterministic audit results.

Reads:
  .lovable/memory/audit/v2-deterministic/raw-results.json
  (run linter-scripts/audit-spec-vs-code-v2.py with AUDIT_DETERMINISTIC=1 first)

Emits:
  .lovable/memory/audit/v2-deterministic/fix-checklists/<module-slug>.md
  .lovable/memory/audit/v2-deterministic/fix-checklists/00-master-checklist.md
  .lovable/memory/audit/v2-deterministic/fix-checklists/raw-checklist.json

Each action item has:
  - priority    P0 (blocker) | P1 | P2 | P3
  - target_file exact spec file to edit
  - action      verb-led instruction
  - ac_test     how to verify the fix is done (a Given/When/Then)
  - effort_min  rough minutes estimate

Exit codes:
  0 = checklist written
  1 = audit JSON missing (run the auditor first)
  2 = invocation error
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path("/dev-server")
AUDIT_JSON = ROOT / ".lovable/memory/audit/v2-deterministic/raw-results.json"
OUT_DIR = ROOT / ".lovable/memory/audit/v2-deterministic/fix-checklists"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TODAY = "2026-04-25"

# Heuristic: language hint based on module path → contract block to inline
LANG_HINT = {
    "database":   ("sql", "CREATE TABLE / CREATE INDEX statements"),
    "schema":     ("json", "JSON Schema document"),
    "api":        ("yaml", "OpenAPI fragment"),
    "endpoint":   ("yaml", "OpenAPI fragment"),
    "enum":       ("ts",  "TypeScript `enum` or `as const` literal union"),
    "error":      ("ts",  "TypeScript discriminated-union for error codes"),
    "router":     ("ts",  "Route table"),
    "config":     ("toml","TOML configuration block"),
    "workflow":   ("yaml","GitHub Actions YAML"),
}


def language_hint_for(module_rel: str) -> tuple[str, str]:
    rel_lower = module_rel.lower()
    for needle, hint in LANG_HINT.items():
        if needle in rel_lower:
            return hint
    return ("text", "normative contract block (DDL / schema / enum / OpenAPI)")


def actions_for_module(mod: dict) -> list[dict]:
    """Translate findings + metrics into concrete file-level actions."""
    rel = mod["module"]
    m = mod["metrics"]
    overview = f"spec/{rel}/00-overview.md"
    ac_file  = f"spec/{rel}/97-acceptance-criteria.md"
    cr_file  = f"spec/{rel}/99-consistency-report.md"
    cl_file  = f"spec/{rel}/98-changelog.md"
    out: list[dict] = []

    # ---- P0: missing contracts ----
    if not (m["has_sql_ddl"] or m["has_json_schema"] or m["has_ts_enums"] or m["has_yaml_openapi"]):
        lang, blurb = language_hint_for(rel)
        out.append({
            "priority":   "P0",
            "category":   "missing-contract",
            "target_file": overview,
            "action":     f"Inline a ```{lang}``` fenced block containing the {blurb}. Do not link to a sibling file — paste the contract directly.",
            "ac_test":    f"Given `{overview}`, When grepped, Then it MUST contain at least one ```{lang} fenced code block ≥10 non-blank lines.",
            "effort_min": 30,
        })

    # ---- P0: no acceptance criteria at all ----
    if m["ac_count"] == 0:
        out.append({
            "priority":   "P0",
            "category":   "untestable",
            "target_file": ac_file,
            "action":     "Run `python3 linter-scripts/generate-gwt-acceptance.py` to scaffold ACs, then hand-edit each into a Given/When/Then triplet.",
            "ac_test":    f"Given `{ac_file}`, When parsed, Then it MUST contain ≥3 `### AC-` headings each followed by a `**Given** … **When** … **Then**` block.",
            "effort_min": 60,
        })
    elif m["gwt_block_count"] < m["ac_count"]:
        gap = m["ac_count"] - m["gwt_block_count"]
        out.append({
            "priority":   "P1",
            "category":   "untestable",
            "target_file": ac_file,
            "action":     f"Rewrite {gap} acceptance criterion/criteria into Given/When/Then form.",
            "ac_test":    f"Given `{ac_file}`, When parsed, Then `gwt_block_count` MUST equal `ac_count` ({m['ac_count']}).",
            "effort_min": gap * 5,
        })

    # ---- P1: broken links ----
    if m["links_broken"] > 0:
        out.append({
            "priority":   "P1",
            "category":   "broken-link",
            "target_file": f"spec/{rel}/",
            "action":     ("Run `python3 linter-scripts/check-spec-cross-links.py --root spec/" + rel +
                           "` then either (a) fix each path or (b) add the link to "
                           "`linter-scripts/spec-cross-links.allowlist` with a justification comment."),
            "ac_test":    f"Given `python3 linter-scripts/check-spec-cross-links.py --root spec/{rel}`, When run, Then exit code MUST be 0.",
            "effort_min": m["links_broken"] * 5,
        })

    # ---- P2: waffle words ----
    if m["waffle_per_kchar"] > 3:
        out.append({
            "priority":   "P2",
            "category":   "ambiguity",
            "target_file": f"spec/{rel}/*.md",
            "action":     ("Replace `should` → `MUST`, `may` → `MAY` (RFC 2119), `optionally` → `MAY`, "
                           "`might` → remove, `preferably`/`ideally` → `MUST` or delete. Keep `may`/`MAY` "
                           "only when the behaviour is genuinely optional."),
            "ac_test":    f"Given the module body, When scanned, Then `waffle_per_kchar` MUST drop below 3.0 (currently {m['waffle_per_kchar']}).",
            "effort_min": 20,
        })

    # ---- P2: missing §99 consistency report ----
    if not m["consistency_report"]:
        out.append({
            "priority":   "P2",
            "category":   "inconsistency",
            "target_file": cr_file,
            "action":     "Run `node linter-scripts/fill-missing-consistency-reports.cjs`, then hand-edit each row to reflect actual code/spec status.",
            "ac_test":    f"Given `{cr_file}`, When read, Then file MUST exist and be non-empty.",
            "effort_min": 15,
        })

    # ---- P3: TODO/TBD/FIXME ----
    if m["todo_density"] > 0:
        out.append({
            "priority":   "P3",
            "category":   "drift",
            "target_file": f"spec/{rel}/*.md",
            "action":     (f"Resolve {m['todo_density']} TODO/TBD/FIXME marker(s). Either implement the "
                           "missing detail or move the marker into a tracked AC."),
            "ac_test":    "Given the module body, When grep'd for `TODO|TBD|FIXME|XXX|HACK`, Then 0 matches.",
            "effort_min": m["todo_density"] * 10,
        })

    # ---- P3: missing changelog row for any of the above edits ----
    if out:
        out.append({
            "priority":   "P3",
            "category":   "maintainability",
            "target_file": cl_file,
            "action":     ("After applying the above fixes, bump version (≥ minor) and add a row to "
                           "`98-changelog.md` summarising what changed."),
            "ac_test":    f"Given `{cl_file}`, When read, Then top-most version row MUST be dated {TODAY} and reference the fixes above.",
            "effort_min": 5,
        })

    return out


def render_module_md(mod: dict, actions: list[dict]) -> str:
    rel = mod["module"]
    m = mod["metrics"]
    s = mod["scores"]
    impact = sum(1 for a in actions if a["priority"] == "P0") * 10 + \
             sum(1 for a in actions if a["priority"] == "P1") * 5  + \
             sum(1 for a in actions if a["priority"] == "P2") * 2  + \
             sum(1 for a in actions if a["priority"] == "P3") * 1
    effort = sum(a["effort_min"] for a in actions)

    lines = [
        f"# Fix Checklist — `spec/{rel}`",
        "",
        f"**Generated:** {TODAY}  ",
        f"**Current score:** {mod['weighted_overall']}/100 ({mod['grade']})  ",
        f"**Implementability:** {s['implementability']}/100  ",
        f"**Estimated effort:** ~{effort} min  ",
        f"**Impact-weighted backlog:** {impact} points",
        "",
        "## Actions",
        "",
        "| # | Pri | Category | Target file | Effort | Action |",
        "|---:|:--:|---|---|---:|---|",
    ]
    for i, a in enumerate(actions, 1):
        action_text = a["action"].replace("|", "\\|")
        lines.append(f"| {i} | **{a['priority']}** | {a['category']} | `{a['target_file']}` | {a['effort_min']}m | {action_text} |")

    lines += ["", "## Detail + Acceptance test for each action", ""]
    for i, a in enumerate(actions, 1):
        lines += [
            f"### {i}. [{a['priority']}] {a['category']} — `{a['target_file']}`",
            "",
            f"**Action:** {a['action']}",
            "",
            f"**Acceptance test:** {a['ac_test']}",
            "",
            f"**Effort estimate:** ~{a['effort_min']} minutes",
            "",
        ]

    if not actions:
        lines += ["_No fixes required — module passes the deterministic rubric._", ""]

    lines += [
        "## Source metrics (from deterministic audit)",
        "",
        "```json",
        json.dumps(m, indent=2, sort_keys=True),
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    if not AUDIT_JSON.exists():
        print(f"FATAL: {AUDIT_JSON} not found.", file=sys.stderr)
        print("Run: AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py", file=sys.stderr)
        return 1

    audit = json.loads(AUDIT_JSON.read_text())
    audit = [m for m in audit if "scores" in m]

    all_checklists = []
    cat_counter: Counter = Counter()
    pri_counter: Counter = Counter()

    for mod in audit:
        rel = mod["module"]
        actions = actions_for_module(mod)
        slug = rel.replace("/", "__") or "_root"
        (OUT_DIR / f"{slug}.md").write_text(render_module_md(mod, actions))
        for a in actions:
            cat_counter[a["category"]] += 1
            pri_counter[a["priority"]]  += 1
        all_checklists.append({
            "module":            rel,
            "score":             mod["weighted_overall"],
            "grade":             mod["grade"],
            "implementability":  mod["scores"]["implementability"],
            "actions":           actions,
            "effort_min_total":  sum(a["effort_min"] for a in actions),
        })

    # Sort: lowest implementability first (highest urgency)
    all_checklists.sort(key=lambda c: (c["implementability"], c["score"]))

    # ---- master roll-up ----
    total_actions = sum(len(c["actions"]) for c in all_checklists)
    total_effort  = sum(c["effort_min_total"] for c in all_checklists)
    p0 = pri_counter["P0"]; p1 = pri_counter["P1"]; p2 = pri_counter["P2"]; p3 = pri_counter["P3"]

    md = [
        "# Master Fix Checklist — All Modules",
        "",
        f"**Generated:** {TODAY}  ",
        f"**Modules analysed:** {len(all_checklists)}  ",
        f"**Total actions:** {total_actions}  ",
        f"**Estimated total effort:** ~{total_effort} min ({round(total_effort/60, 1)} hours)",
        "",
        "## Priority distribution",
        "",
        "| Priority | Count | Meaning |",
        "|:--:|---:|---|",
        f"| **P0** | {p0} | Blocker — module fails AI-implementability without this |",
        f"| **P1** | {p1} | High — significantly raises score |",
        f"| **P2** | {p2} | Medium — clarity / hygiene |",
        f"| **P3** | {p3} | Low — polish |",
        "",
        "## Findings by category",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for k, v in cat_counter.most_common():
        md.append(f"| {k} | {v} |")

    md += [
        "",
        "## Per-module checklists (sorted by lowest implementability first)",
        "",
        "| Module | Score | Impl | P0 | P1 | P2 | P3 | Effort | Checklist |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for c in all_checklists:
        slug = c["module"].replace("/", "__") or "_root"
        per = Counter(a["priority"] for a in c["actions"])
        md.append(f"| `{c['module']}` | {c['score']} | {c['implementability']} | "
                  f"{per['P0']} | {per['P1']} | {per['P2']} | {per['P3']} | "
                  f"{c['effort_min_total']}m | [open](./{slug}.md) |")

    md += [
        "",
        "## How to use this checklist",
        "",
        "1. Open the lowest-implementability module first (top of table).",
        "2. Work each action in priority order P0 → P3.",
        "3. After each fix, the **Acceptance test** column tells you exactly how to verify the fix is done.",
        "4. Re-run `AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py` to refresh the score.",
        "5. Re-run `python3 linter-scripts/generate-fix-checklist.py` to regenerate this list.",
        "",
    ]
    (OUT_DIR / "00-master-checklist.md").write_text("\n".join(md))

    # ---- raw JSON (sorted, byte-stable) ----
    payload = {
        "generated":            TODAY,
        "modules_analysed":     len(all_checklists),
        "total_actions":        total_actions,
        "total_effort_minutes": total_effort,
        "priority_counts":      dict(pri_counter),
        "category_counts":      dict(cat_counter),
        "checklists":           all_checklists,
    }
    (OUT_DIR / "raw-checklist.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )

    print(f"✓ Wrote {OUT_DIR.relative_to(ROOT)}/00-master-checklist.md", file=sys.stderr)
    print(f"  {len(all_checklists)} module checklists, {total_actions} actions, "
          f"~{round(total_effort/60,1)}h total effort", file=sys.stderr)
    print(f"  P0={p0}, P1={p1}, P2={p2}, P3={p3}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

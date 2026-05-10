#!/usr/bin/env python3
"""
generate-gate-report.py — Explain which hard scoring gate caps each module's
score, dimension by dimension.

Reads:
  .lovable/memory/audit/v2-deterministic/raw-results.json
  (run AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py first)

Emits:
  .lovable/memory/audit/v2-deterministic/gate-report.md   (human roll-up)
  .lovable/memory/audit/v2-deterministic/gate-report.json (machine, byte-stable)

Each module's section shows:
  - rubric (raw) score per dimension
  - applied gates (active = lowered, passive = met-but-not-exceeded)
  - delta (raw_overall − final_overall) attributable to gates

Roll-up summarises gate firing rates so we can see which rules bite hardest.

Exit codes:
  0 = report written
  1 = audit JSON missing
  2 = invocation error
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/dev-server")
AUDIT_JSON = ROOT / ".lovable/memory/audit/v2-deterministic/raw-results.json"
OUT_MD   = ROOT / ".lovable/memory/audit/v2-deterministic/gate-report.md"
OUT_JSON = ROOT / ".lovable/memory/audit/v2-deterministic/gate-report.json"
TODAY = "2026-04-25"

WEIGHTS = {
    "implementability": 35, "completeness": 20, "alignment": 15,
    "consistency": 10, "clarity": 10, "testability": 7, "maintainability": 3,
}


def weighted(scores: dict) -> int:
    return round(sum(scores[k] * w / 100 for k, w in WEIGHTS.items()))


def main() -> int:
    if not AUDIT_JSON.exists():
        print(f"FATAL: {AUDIT_JSON} not found.", file=sys.stderr)
        print("Run: AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py", file=sys.stderr)
        return 1

    audit = [m for m in json.loads(AUDIT_JSON.read_text()) if "scores" in m]

    fire_counts: Counter = Counter()        # gate id -> active firings
    passive_counts: Counter = Counter()     # gate id -> passive (already capped) firings
    dim_loss: dict[str, int] = defaultdict(int)
    gate_rationales: dict[str, str] = {}
    gate_dimensions: dict[str, str] = {}
    gate_caps: dict[str, int] = {}

    per_module = []
    for mod in audit:
        rel = mod["module"]
        gates = mod.get("applied_gates", [])
        raw = mod.get("raw_scores", mod["scores"])
        final = mod["scores"]
        raw_overall = weighted(raw)
        final_overall = weighted(final)
        delta = raw_overall - final_overall

        active = [g for g in gates if g["active"]]
        passive = [g for g in gates if not g["active"]]

        for g in active:
            fire_counts[g["id"]] += 1
            dim_loss[g["dimension"]] += g["before"] - g["after"]
            gate_rationales[g["id"]] = g["rationale"]
            gate_dimensions[g["id"]] = g["dimension"]
            gate_caps[g["id"]] = g["cap"]
        for g in passive:
            passive_counts[g["id"]] += 1
            gate_rationales.setdefault(g["id"], g["rationale"])
            gate_dimensions.setdefault(g["id"], g["dimension"])
            gate_caps.setdefault(g["id"], g["cap"])

        per_module.append({
            "module":        rel,
            "raw_overall":   raw_overall,
            "final_overall": final_overall,
            "delta":         delta,
            "raw_scores":    raw,
            "final_scores":  final,
            "active_gates":  sorted(active, key=lambda g: g["id"]),
            "passive_gates": sorted(passive, key=lambda g: g["id"]),
        })

    # Sort: biggest delta first (most punished modules at top)
    per_module.sort(key=lambda r: (-r["delta"], r["module"]))

    # ---- markdown ----
    total_active = sum(fire_counts.values())
    total_passive = sum(passive_counts.values())
    capped_modules = sum(1 for r in per_module if r["delta"] > 0)

    lines = [
        "# Hard Gate Report",
        "",
        f"**Generated:** {TODAY}  ",
        f"**Modules analysed:** {len(per_module)}  ",
        f"**Modules capped by gates:** {capped_modules} ({round(capped_modules/max(len(per_module),1)*100,1)}%)  ",
        f"**Active gate firings:** {total_active}  ",
        f"**Passive gate firings:** {total_passive} _(rule triggered but score already at/below cap)_",
        "",
        "## How to read",
        "",
        "Hard gates are non-negotiable score ceilings applied AFTER the rubric. "
        "When a gate's predicate fires, the named dimension cannot exceed `cap`.",
        "An **active** gate actually reduced the score; a **passive** one fired but the rubric was already at/below the cap.",
        "",
        "## Gate firing leaderboard",
        "",
        "| Gate | Dimension | Cap | Active fires | Passive fires | Total dimension-points lost | Rationale |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    all_gate_ids = sorted(set(fire_counts) | set(passive_counts))
    leaderboard = []
    for gid in all_gate_ids:
        leaderboard.append((gid, fire_counts[gid], passive_counts[gid]))
    leaderboard.sort(key=lambda x: (-x[1], -x[2], x[0]))
    for gid, active_n, passive_n in leaderboard:
        loss = sum(g["before"] - g["after"]
                   for r in per_module
                   for g in r["active_gates"]
                   if g["id"] == gid)
        lines.append(
            f"| `{gid}` | {gate_dimensions[gid]} | {gate_caps[gid]} | "
            f"{active_n} | {passive_n} | {loss} | "
            f"{gate_rationales[gid].replace('|', '\\|')} |"
        )

    lines += [
        "",
        "## Dimension-loss totals",
        "",
        "| Dimension | Total points lost to gates |",
        "|---|---:|",
    ]
    for dim, loss in sorted(dim_loss.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {dim} | {loss} |")
    if not dim_loss:
        lines.append("| _(no active gates fired)_ | 0 |")

    lines += [
        "",
        "## Per-module gate detail (most-capped first)",
        "",
        "| Module | Raw | Final | Δ | Active gates |",
        "|---|---:|---:|---:|---|",
    ]
    for r in per_module:
        gate_ids = ", ".join(f"`{g['id']}`" for g in r["active_gates"]) or "_none_"
        lines.append(f"| `{r['module']}` | {r['raw_overall']} | {r['final_overall']} | "
                     f"−{r['delta']} | {gate_ids} |")

    # ---- per-module deep dive (only modules with active or passive gates) ----
    deep = [r for r in per_module if r["active_gates"] or r["passive_gates"]]
    if deep:
        lines += ["", "## Per-module breakdown", ""]
        for r in deep:
            lines += [
                f"### `spec/{r['module']}` — raw {r['raw_overall']} → final {r['final_overall']} (Δ −{r['delta']})",
                "",
                "| Dimension | Raw | Final | Capped by |",
                "|---|---:|---:|---|",
            ]
            for dim in WEIGHTS:
                raw = r["raw_scores"].get(dim, 0)
                fin = r["final_scores"].get(dim, 0)
                hits = [g["id"] for g in r["active_gates"] if g["dimension"] == dim]
                cap_str = ", ".join(f"`{h}`" for h in hits) or ""
                arrow = " ⬇" if fin < raw else ""
                lines.append(f"| {dim} | {raw} | **{fin}**{arrow} | {cap_str} |")
            if r["active_gates"]:
                lines.append("")
                lines.append("**Active gates fired (this module):**")
                for g in r["active_gates"]:
                    lines.append(f"- `{g['id']}` capped `{g['dimension']}` from {g['before']} → {g['after']}: {g['rationale']}")
            if r["passive_gates"]:
                lines.append("")
                lines.append("**Passive gates (already at/below cap, no score change):**")
                for g in r["passive_gates"]:
                    lines.append(f"- `{g['id']}` ({g['dimension']} cap={g['cap']}, current={g['before']})")
            lines.append("")

    OUT_MD.write_text("\n".join(lines))

    # ---- JSON (sorted, byte-stable) ----
    payload = {
        "generated":         TODAY,
        "modules_analysed":  len(per_module),
        "modules_capped":    capped_modules,
        "active_firings":    total_active,
        "passive_firings":   total_passive,
        "fire_counts":       dict(fire_counts),
        "passive_counts":    dict(passive_counts),
        "dim_loss":          dict(dim_loss),
        "per_module":        sorted(per_module, key=lambda r: r["module"]),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"✓ Wrote {OUT_MD.relative_to(ROOT)}", file=sys.stderr)
    print(f"  {capped_modules}/{len(per_module)} modules capped, "
          f"{total_active} active firings, {total_passive} passive",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Generate module-specific Given/When/Then acceptance criteria for F-tier
spec modules.

For each module:
  1. Read overview + every body file (NN-*.md) + sibling files referenced
  2. Send the consolidated digest to Gemini with strict GWT schema
  3. Receive 5–12 module-specific ACs with inlined contracts (DDL, enums,
     error codes, exact field names, file paths)
  4. Write to spec/<module>/97-acceptance-criteria.md (overwrite scaffold)
  5. Append a §98 changelog entry
"""
import json, re, sys, time
from pathlib import Path

sys.path.insert(0, "/tmp")
from lovable_ai import call_ai_structured  # type: ignore

SPEC = Path("/dev-server/spec")
AUDIT = json.loads(Path("/mnt/documents/spec-ai-audit.json").read_text())
MODEL = "google/gemini-3-flash-preview"
TODAY = "2026-04-25"

# ---- module selection ----
EXCLUDE = {
    ".",                              # root index, not a module
    "14-update/diagrams",             # pure diagrams
    "26-gitlogs-diagrams",            # pure diagrams
}

f_tier = [r["module"] for r in AUDIT
          if r.get("grade") == "F" and r["module"] not in EXCLUDE]

# ---- digest builder ----
def read(p, lim=None):
    try:
        t = p.read_text(encoding="utf-8", errors="replace")
        return t[:lim] if lim else t
    except Exception:
        return ""

def build_digest(folder: Path):
    """Pull EVERY body file in the module + sibling links it references."""
    rel = folder.relative_to(SPEC)
    chunks = [f"# Module: spec/{rel}\n"]
    body_files = sorted(folder.glob("*.md"))
    body_files = [f for f in body_files if not f.name.startswith(("97-","98-","99-"))]
    for f in body_files:
        chunks.append(f"\n## File: {f.name}\n")
        chunks.append(read(f, 4000))
    # sub-folders' overviews (often contain the real contract)
    for sub in sorted(folder.iterdir()):
        if sub.is_dir():
            ov = sub / "00-overview.md"
            if ov.exists():
                chunks.append(f"\n## Sub-overview: {sub.name}/00-overview.md\n")
                chunks.append(read(ov, 2000))
    return "\n".join(chunks)[:35000]   # cap context

# ---- AI tool schema ----
TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "module_summary": {
            "type": "string",
            "description": "1-3 sentences: what this module specifies. Concrete, no fluff."
        },
        "inlined_contracts": {
            "type": "string",
            "description": "Markdown block containing EVERY contract a mediocre AI needs: exact enum values, error codes, field names, file paths, DDL snippets, function signatures. Inline them here so AC can reference them. If module has no contracts, write 'N/A'."
        },
        "acceptance_criteria": {
            "type": "array",
            "description": "5–12 module-specific Given/When/Then triples. Each must reference concrete artifacts from the module body — never generic file-presence checks. Number them AC-01..AC-NN.",
            "items": {
                "type": "object",
                "properties": {
                    "id":        {"type": "string", "description": "AC-01, AC-02, ..."},
                    "title":     {"type": "string", "description": "Short title — 3-8 words"},
                    "given":     {"type": "string", "description": "Precondition referencing concrete module artifact"},
                    "when":      {"type": "string", "description": "Action — concrete, verifiable"},
                    "then":      {"type": "string", "description": "Expected outcome — observable + measurable"},
                    "verifies":  {"type": "string", "description": "Which file/section in the module body this AC verifies"},
                    "severity":  {"type": "string", "enum": ["critical","high","medium","low"]}
                },
                "required": ["id","title","given","when","then","verifies","severity"]
            }
        }
    },
    "required": ["module_summary","inlined_contracts","acceptance_criteria"]
}

SYSTEM = """You write module-specific Given/When/Then acceptance criteria for a software spec.

RULES:
- Read the module body carefully. Every AC must reference SPECIFIC artifacts from the body
  (file names, function names, enum values, table columns, error codes, exact strings).
- NEVER generic file-presence checks ("file exists", "AC file is non-empty").
- NEVER metadata checks ("version banner present").
- If the module is sparse, infer ACs from the FILE NAMES + folder context but still make
  them concrete. e.g. for `04-flag-parsing.md` write ACs about flag parsing behavior, not
  "file 04 exists".
- Inline every contract a mediocre AI needs to implement. If the module references
  enum X, write the enum's values. If it references an error code, write the code.
  If it references a DB table, write the columns.
- 5–12 ACs per module. Quality over quantity.
- Severity: 'critical' = breaks the system if wrong; 'high' = wrong behavior visible to users;
  'medium' = correctness/quality issue; 'low' = polish."""

# ---- writer ----
def render_ac_md(rel: str, payload: dict) -> str:
    title = rel.split("/")[-1].replace("-", " ").title()
    out = []
    out.append(f"# Acceptance Criteria — {title}\n")
    out.append(f"**Version:** 2.0.0  ")
    out.append(f"**Updated:** {TODAY}  ")
    out.append(f"**Scope:** `spec/{rel}/`  ")
    out.append(f"**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`\n")
    out.append("---\n")
    out.append("## Module Summary\n")
    out.append(payload["module_summary"] + "\n")
    out.append("---\n")
    out.append("## Inlined Contracts\n")
    out.append("> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.\n")
    out.append(payload["inlined_contracts"] + "\n")
    out.append("---\n")
    out.append("## Acceptance Criteria\n")
    for ac in payload["acceptance_criteria"]:
        out.append(f"### {ac['id']}: {ac['title']}  `[{ac['severity']}]`")
        out.append(f"- **Given** {ac['given']}")
        out.append(f"- **When** {ac['when']}")
        out.append(f"- **Then** {ac['then']}")
        out.append(f"- **Verifies:** {ac['verifies']}")
        out.append("")
    out.append("---\n")
    out.append("## Cross-References\n")
    out.append("- [Module overview](./00-overview.md)")
    out.append("- [Module changelog](./98-changelog.md)")
    out.append("- [Module consistency report](./99-consistency-report.md)")
    return "\n".join(out)

def append_changelog(folder: Path):
    cl = folder / "98-changelog.md"
    if not cl.exists():
        return
    txt = cl.read_text(encoding="utf-8")
    if "v2.0.0" in txt:
        return
    entry = f"\n### 2.0.0 — {TODAY}\n- **Changed** `97-acceptance-criteria.md`: replaced scaffolded placeholder with AI-extracted Given/When/Then acceptance criteria. Inlined required contracts (enums, DDL, error codes, file paths) directly into the AC file so a mediocre AI can implement without chasing cross-links. Generated by `linter-scripts/generate-gwt-acceptance.py` as part of root v3.7.x F-tier remediation sweep.\n"
    # Insert after "## Releases" header if present, else append
    if "## Releases" in txt:
        txt = txt.replace("## Releases", "## Releases" + entry, 1)
    else:
        txt += entry
    # Bump version banner
    txt = re.sub(r"\*\*Version:\*\*\s*\S+", "**Version:** 2.0.0", txt, count=1)
    txt = re.sub(r"\*\*Updated:\*\*\s*\S+", f"**Updated:** {TODAY}", txt, count=1)
    cl.write_text(txt)

def process(rel: str):
    folder = SPEC / rel
    if not folder.exists():
        return ("MISSING", rel)
    digest = build_digest(folder)
    payload = call_ai_structured(
        prompt=digest,
        tool_name="emit_acceptance_criteria",
        tool_description="Emit module-specific GWT acceptance criteria",
        parameters=TOOL_PARAMS,
        system=SYSTEM,
        model=MODEL,
    )
    md = render_ac_md(rel, payload)
    (folder / "97-acceptance-criteria.md").write_text(md)
    append_changelog(folder)
    return ("OK", len(payload["acceptance_criteria"]))

def main():
    print(f"Generating GWT ACs for {len(f_tier)} F-tier modules...", file=sys.stderr)
    results = []
    for i, rel in enumerate(f_tier, 1):
        sys.stderr.write(f"[{i:>2}/{len(f_tier)}] {rel} ... ")
        sys.stderr.flush()
        try:
            status, info = process(rel)
            sys.stderr.write(f"{status} ({info} ACs)\n" if status=="OK" else f"{status}\n")
            results.append({"module": rel, "status": status, "info": str(info)})
        except Exception as e:
            sys.stderr.write(f"ERROR {e}\n")
            results.append({"module": rel, "status": "ERROR", "info": str(e)})
        time.sleep(0.4)
    Path("/mnt/documents/gwt-generation-log.json").write_text(json.dumps(results, indent=2))
    ok = sum(1 for r in results if r["status"] == "OK")
    print(f"\n✓ {ok}/{len(results)} modules generated", file=sys.stderr)

if __name__ == "__main__":
    main()

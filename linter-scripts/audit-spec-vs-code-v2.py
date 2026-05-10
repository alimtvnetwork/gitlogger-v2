#!/usr/bin/env python3
"""
Spec-vs-Code Audit **v2.17** — AI-Implementability Edition.

v2.17 (2026-04-27, Phase 99):
  - **No rubric change.** Metadata + output-header sync only:
    * `RUBRIC_VERSION` constant lifted from "v2.16" to "v2.17" so the
      generated `00-index.md` and `EXECUTIVE-SUMMARY.md` advertise the
      current QA-tooling baseline (Phases 81/90/91/94/95/97/98).
    * The two summary outputs gain a "QA tooling baseline" footer line
      enumerating the gates that surround the score: Phase 81's
      `--min-weighted` / `--min-impl` floors, Phase 90's `--explain`
      debugger, the Phase 91/94/95 self-test triad, Phase 97's mermaid
      syntax gate, and Phase 98's inventory README. A reader of the
      audit output now knows the score is one signal among 8 strict
      gates, not the only signal.
  - Determinism guarantee preserved: `RUBRIC_VERSION` is a static string,
    not derived from time/env. The Phase 95 self-test continues to pass
    byte-identically (sha256 hash will shift exactly once on the v2.17
    rollout, then re-stabilise).

v2.16 (2026-04-27, Phase 90):
  - New `--explain=<substring>` CLI flag for debugging score outliers.
    Prints, for the first matching module: rubric branch taken, every bonus
    that fired with its delta, every gate that capped a dimension (with
    before/after), per-dimension scores (raw vs final + Δ + contribution),
    and key metrics. Pure-add diagnostic — does not write files, does not
    call AI, exits 0 if a match was found and 1 otherwise. Disambiguates
    multi-match by listing the first 5 candidates and using the first.
  - Use cases: rubric debugging, contributor onboarding, explaining why a
    specific module dropped a grade after a change.

v2.15 (2026-04-27, Phase 86):
  - Rubric-hygiene investigation REJECTED. Considered diminishing-returns
    schema-bonus cap (strongest contract at full weight, subsequent bonuses
    halved, subtotal capped at 50) to address theoretical kitchen-sink
    stacking. Empirical test on the 87-module corpus: mean implementability
    99.8 → 89.2, mean weighted 98.0 → 94.1; 76 normal-contract modules
    legitimately satisfy ≥3 contract types and were unfairly penalised.
  - Decision: keep the v2.3 additive contract-bonus model; the existing
    100-cap on `impl` already prevents pathological stacking. Multi-contract
    breadth (e.g. §22-git-logs-v2 with SQL+TS+JSON+YAML) genuinely encodes
    more invariants and warrants the full bonus.
  - Net effect: zero rubric or score change; documents the rejected
    alternative in source for future contributors who might re-propose it.

v2.9 (2026-04-27, Phase 46):
  - Root index spec (`spec/00-overview.md`, MOD_REL == ".") now receives the
    top-level folders as children (`CHILDREN["."]`). The root index was
    previously seeing `child_modules=0` because the parent-derivation rule
    only fired for paths containing `/`. Effect: root spec implementability
    climbs (with `kind: index`) from baseline 70 to 80, and weighted score
    rises out of D-tier.

v2.8 (2026-04-27, Phase 45):
  - `kind: meta-toolchain` modules now use a tracker-style implementability
    baseline (85) when they expose a normative contract block (`text` fenced
    block ≥10 non-blank lines containing INV- / FAIL- / DEL- / CONTRACT:
    markers, OR ≥30 child spec files acting as the bijection table).
  - Rationale: the `27-spec-toolchain` module's "contract" is the inventory
    of script specs + invariants table; it has no DDL/OpenAPI but IS fully
    implementable from spec alone (every section maps 1:1 to a script).
  - Effect: §27 implementability 55 → 85; §27 weighted 78 → ~88; mean
    weighted 82.3 → ~84.

v2.6 (2026-04-27, Phase 43):
  - Cross-spec link extraction now runs against code-stripped prose, not
    the raw body. Markdown links inside fenced ```markdown / ```text
    template blocks (e.g. §01-spec-authoring-guide's path-syntax examples)
    no longer count toward `links_total` / `links_broken`. Example links
    are *documentation*, not real references; the scanner must not treat
    `[Architecture](./01-architecture.md)` inside a code fence as broken
    just because the example file does not exist.
  - Effect: §01 broken-link count drops 13 → 0; §25/02 drops 13 → 0;
    §02/01-cross-language drops 1 → 0; total project broken links 30 → ~3.
  - Implementation: new `prose_for_links` (= strip_code(body_text)) feeds
    LINK_RX.findall, while strip_code() is unchanged for waffle/TODO use.

v2.5 (2026-04-27, Phase R5):
  - Meta-token sequence exemption: the canonical reference form
    `TODO/TBD/FIXME` (or any 2+ slash-joined work-tracking tokens) is now
    stripped before counting individual hits. Spec content that *defines*
    the audit (changelog rows, AC text, fix-checklist categories) no
    longer self-penalises. Real `TODO:` work markers still count.
  - New frontmatter `kind: meta-toolchain` exempts auditor-self-reference
    modules entirely from G-TODO-01.

v2.4 (2026-04-27, Phase R4):
  - TODO/TBD/FIXME and waffle-word scanners now strip fenced code blocks
    (```...```) and inline `code` spans before counting. Tokens that appear
    inside code samples (legitimate variable names, comments demonstrating
    a forbidden pattern, schema placeholders, etc.) no longer trigger the
    G-TODO-01 finding or inflate the waffle ratio. Prose-only scanning.

v2.3 (2026-04-26, Phase 25):
  - Contract definition expanded: typed-language reference blocks
    (≥3 of go/rust/php/csharp/java/kotlin/swift/python/cpp) and CI workflow
    YAML (≥5 yaml/yml blocks) now satisfy G-CON-01.
  - Implementability bonuses: +10 typed-lang, +5 CI workflow.
  - Rationale: a Go/PHP/CI-CD spec with dozens of reference snippets IS a
    contract for an AI generating that language; rubric no longer assumes
    every contract is SQL/JSON/TS.

v2.2 (2026-04-26, Phase 24):
  - Front-matter `kind: index` exempts placement-rule routers (intentionally
    empty stub overviews that demarcate a scope) from `missing-contract` and
    `untestable` rubric findings. Baseline impl 70 (vs tracker's 75).

v2.1 (2026-04-26, Phase 23):
  - Front-matter `kind: tracker` exempts issue/finding modules from
    `missing-contract` and `untestable` rubric findings.
  - Trackers receive impl baseline 75 (was 30) and testability 80.

Improvements over v1:
  1. Broader code index: linter-scripts + .github + src + spec sub-tree map
  2. NEW dimension: "implementability" (35% weight) — can a mediocre AI build
     the feature from this spec ALONE, with no human clarification?
  3. Cross-spec link resolution — counts broken/orphan links per module
  4. Deterministic pre-checks (run BEFORE AI):
       - waffle ratio (should/may/might/optionally per 1k chars)
       - contract presence (DDL ```sql```, enum ```ts``` blocks, error codes)
       - AC count and Given/When/Then structure
       - TODO/TBD/FIXME density
  5. AI receives the deterministic metrics + raw digest, must JUSTIFY its score
     against those metrics → less hallucinated grading
  6. Two-pass: AI scores, then a second AI call critiques the score and may
     adjust it (catches over-generous scoring)
  7. Outputs a *blast-radius* table: which fixes unblock the most child specs
  8. Roll-up: parent modules show aggregate of children in the index

Weighted (v2): implementability 35, completeness 20, alignment 15,
                consistency 10, clarity 10, testability 7, maintainability 3
"""
import json, re, sys, time, os
from pathlib import Path
from collections import Counter, defaultdict

# Deterministic mode skips AI scoring entirely and produces byte-identical
# JSON output across runs. Toggle via env var AUDIT_DETERMINISTIC=1.
DETERMINISTIC = os.environ.get("AUDIT_DETERMINISTIC", "").strip() in {"1", "true", "yes"}

if not DETERMINISTIC:
    sys.path.insert(0, "/tmp")
    from lovable_ai import call_ai_structured  # type: ignore

ROOT = Path("/dev-server")
SPEC = ROOT / "spec"
OUT = ROOT / (".lovable/memory/audit/v2-deterministic" if DETERMINISTIC else ".lovable/memory/audit/v2")
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "google/gemini-2.5-flash"
TODAY = "2026-04-25"
# v2.17 (Phase 99): static rubric version surfaced in summary outputs so a
# reader of 00-index.md / EXECUTIVE-SUMMARY.md knows which scoring rules
# produced the verdict. Bump this on every rubric change (see docstring).
RUBRIC_VERSION = "v2.31"

WEIGHTS = {
    "implementability": 35,
    "completeness":     20,
    "alignment":        15,
    "consistency":      10,
    "clarity":          10,
    "testability":       7,
    "maintainability":   3,
}
assert sum(WEIGHTS.values()) == 100

WAFFLE_RX = re.compile(r"\b(should|may|might|could|optionally|preferably|ideally|consider|recommended)\b", re.I)
# v2.14 (Phase 83): tightened TODO regex. The previous `\bTODO\b` matched
# narrative mentions ("TODO comment", "marked TODO", "TODO/FIXME density")
# and inflated todo_density on auditor-self-reference and gap-analysis
# modules. The new pattern requires the canonical work-tracker shape:
#   TODO:        — colon directly after marker
#   TODO(name):  — Conventional Commits style
#   TODO -       — dash bullet form
# Narrative mentions (no following : / ( / -) are correctly ignored.
TODO_RX   = re.compile(r"\b(TODO|TBD|FIXME|XXX|HACK)(?:\s*\([^)]*\))?\s*[:\-]")
GWT_RX    = re.compile(r"\*\*Given\*\*.*?\*\*When\*\*.*?\*\*Then\*\*", re.S | re.I)
AC_RX     = re.compile(r"(?:^|\n)\s*###?\s*AC[-\s]?[A-Z\d-]+", re.I)
LINK_RX   = re.compile(r"\[([^\]]+)\]\(([^)#]+\.md)(?:#[^)]*)?\)")
CODE_BLOCK_RX = re.compile(r"```(\w+)?\n(.*?)```", re.S)
INLINE_CODE_RX = re.compile(r"`[^`\n]+`")
FRONTMATTER_RX = re.compile(r"\A---\n(.*?)\n---\n", re.S)
KIND_RX        = re.compile(r"^kind:\s*([A-Za-z0-9_-]+)\s*$", re.M)
TODO_EXEMPT_RX = re.compile(r"^todo_audit_exempt:\s*true\s*$", re.M)

TODO_TOKEN = r"(?:TODO|TBD|FIXME|XXX|HACK)"
META_TOKEN_SEQ_RX = re.compile(rf"\b{TODO_TOKEN}(?:/{TODO_TOKEN}){{1,4}}\b")

def strip_code(text: str) -> str:
    """Remove fenced code blocks, inline code, and meta-token sequences
    so TODO/waffle scanners see prose only.

    v2.4: strips ```...``` fences and `inline` spans.
    v2.5: also strips slash-joined meta references like `TODO/TBD/FIXME`
    that occur in audit-self-reference content (changelog rows, AC text,
    fix-checklist category labels). Standalone `TODO:` work markers in
    prose still count."""
    no_fences = CODE_BLOCK_RX.sub("", text)
    no_inline = INLINE_CODE_RX.sub("", no_fences)
    return META_TOKEN_SEQ_RX.sub("", no_inline)

# ---------------- code surface ----------------
def collect_code_index() -> str:
    items = []
    # linter-scripts
    for p in sorted((ROOT / "linter-scripts").glob("*")):
        if p.is_file() and p.suffix in {".py",".cjs",".js",".sh",".ps1",".go",".toml",".mjs"}:
            head = p.read_text(errors="replace").splitlines()[:10]
            purpose = ""
            for l in head:
                ls = l.strip().lstrip('#/* ').strip()
                if len(ls) > 10 and not ls.startswith(("!","import","from","const","require")):
                    purpose = ls; break
            items.append(f"- linter-scripts/{p.name} — {purpose[:140]}")
    # CI
    for p in sorted((ROOT / ".github").rglob("*.yml")):
        items.append(f"- {p.relative_to(ROOT)} — GitHub Actions workflow")
    # frontend src (presence only — proves we have NO product code)
    src = ROOT / "src"
    if src.exists():
        n = sum(1 for _ in src.rglob("*.tsx")) + sum(1 for _ in src.rglob("*.ts"))
        items.append(f"- src/ — {n} TS/TSX files (Lovable scaffold; not part of any spec implementation)")
    return "\n".join(items)

CODE_INDEX = collect_code_index()
CODE_INDEX_LINES = CODE_INDEX.count("\n") + 1

# ---------------- spec tree map ----------------
def find_modules():
    return sorted(p.parent for p in SPEC.rglob("00-overview.md") if "_archive" not in p.parts)

ALL_MODULES = find_modules()
MOD_REL = {m: str(m.relative_to(SPEC)) for m in ALL_MODULES}

# parent -> [child rels]
# v2.9 (Phase 46): top-level folders count as children of the root index ".",
# so the root spec/00-overview.md correctly receives the index `child_modules > 0`
# bonus and is not flagged as a stub router.
CHILDREN = defaultdict(list)
for m in ALL_MODULES:
    rel = MOD_REL[m]
    if rel == ".":
        continue
    if "/" in rel:
        parent = rel.rsplit("/", 1)[0]
        CHILDREN[parent].append(rel)
    else:
        CHILDREN["."].append(rel)

def read(p, lim=None):
    try:
        t = p.read_text(encoding="utf-8", errors="replace")
        return t[:lim] if lim else t
    except Exception:
        return ""

# ---------------- deterministic metrics ----------------
def deterministic_metrics(folder: Path) -> dict:
    md_files = list(folder.glob("*.md"))
    body_text = "\n".join(read(f) for f in md_files)
    ov = read(folder / "00-overview.md")
    ac = read(folder / "97-acceptance-criteria.md")
    cr = read(folder / "99-consistency-report.md")

    # front-matter kind (e.g. `kind: tracker`) — exempts non-contract modules
    kind = ""
    fm = FRONTMATTER_RX.match(ov)
    if fm:
        km = KIND_RX.search(fm.group(1))
        if km:
            kind = km.group(1).strip().lower()

    # contract presence in body (excluding AC)
    body_blocks = CODE_BLOCK_RX.findall(body_text)
    lang_counter = Counter(lang or "plain" for lang, _ in body_blocks)
    has_sql  = lang_counter.get("sql", 0) + lang_counter.get("ddl", 0)
    has_json = lang_counter.get("json", 0)
    has_ts   = lang_counter.get("ts", 0) + lang_counter.get("typescript", 0)
    has_yaml = lang_counter.get("yaml", 0) + lang_counter.get("yml", 0)
    # v2.3: typed-language reference blocks (go/php/csharp/rust/etc.) are also
    # contracts for language-specific coding-guideline modules. Function
    # signatures, type definitions, and idiomatic patterns are normative for
    # an AI generating code in that language. Threshold ≥3 blocks rules out
    # incidental snippets and requires sustained, reference-grade content.
    TYPED_LANGS = ("go", "golang", "rust", "php", "csharp", "cs", "c#",
                   "java", "kotlin", "swift", "python", "py", "cpp", "c++", "c")
    typed_lang_blocks = sum(lang_counter.get(l, 0) for l in TYPED_LANGS)
    has_typed_lang_contract = typed_lang_blocks >= 3
    # v2.3: CI workflow YAML (≥5 blocks) is a normative contract for
    # CI/CD pipeline modules — distinct from generic single-snippet YAML.
    has_ci_workflow = lang_counter.get("yaml", 0) + lang_counter.get("yml", 0) >= 5
    # v2.8 (Phase 45): "normative contract" detection for meta-toolchain
    # modules. A `text` fenced block ≥10 non-blank lines containing
    # CONTRACT: / INV- / FAIL- / DEL- markers IS a machine-readable
    # contract — even though it isn't SQL/JSON/YAML. The §27 toolchain
    # bijection table is the canonical example.
    has_normative_contract = False
    for lang, content in body_blocks:
        if (lang or "").lower() not in ("text", "plain", ""):
            continue
        non_blank = [ln for ln in content.splitlines() if ln.strip()]
        if len(non_blank) < 10:
            continue
        joined = "\n".join(non_blank)
        markers = sum(1 for tag in ("CONTRACT:", "INV-", "FAIL-", "DEL-", "INVARIANT", "BIJECTION") if tag in joined)
        if markers >= 2:
            has_normative_contract = True
            break

    # cross-spec link health — v2.6: scan code-stripped prose so example
    # links inside ```markdown / ```text fences (path-syntax templates in
    # §01-spec-authoring-guide etc.) don't get counted as broken.
    prose_for_links = strip_code(body_text)
    links = LINK_RX.findall(prose_for_links)
    broken = 0; total = 0
    for _, target in links:
        if target.startswith(("http://","https://","mailto:")):
            continue
        total += 1
        resolved = (folder / target).resolve()
        if not resolved.exists():
            broken += 1

    # AC quality
    ac_ids = AC_RX.findall(ac)
    gwt_blocks = len(GWT_RX.findall(ac))

    # waffle + TODO scanning — strip code blocks/inline code so tokens
    # inside fenced samples don't pollute prose-level metrics (v2.4).
    prose_text = strip_code(body_text)
    chars = max(len(prose_text), 1)
    waffle = len(WAFFLE_RX.findall(prose_text))
    waffle_per_kchar = round(waffle / chars * 1000, 2)
    todo_count = len(TODO_RX.findall(prose_text))
    # v2.14 (Phase 83): per-module front-matter opt-out for the TODO penalty.
    # Auditor-self-reference modules legitimately quote TODO markers when
    # documenting how the TODO detector works. Setting `todo_audit_exempt: true`
    # in the overview front-matter zeroes todo_count for completeness scoring.
    if fm and TODO_EXEMPT_RX.search(fm.group(1)):
        todo_count = 0

    # mermaid + other companion artefacts
    mmd_files = list(folder.glob("*.mmd"))

    return {
        "kind":                kind,  # "" for normal contract modules; "tracker" exempts contract/AC findings
        "md_files":            len(md_files),
        "mmd_files":           len(mmd_files),
        "overview_chars":      len(ov),
        "ac_chars":            len(ac),
        "ac_count":            len(ac_ids),
        "gwt_block_count":     gwt_blocks,
        "consistency_report":  bool(cr.strip()),
        "code_blocks_total":   len(body_blocks),
        "code_blocks_by_lang": dict(lang_counter),
        "has_sql_ddl":         has_sql > 0,
        "has_json_schema":     has_json > 0,
        "has_ts_enums":        has_ts > 0,
        "has_yaml_openapi":    has_yaml > 0,
        "has_typed_lang_contract": has_typed_lang_contract,  # v2.3
        "has_ci_workflow":     has_ci_workflow,              # v2.3
        "has_normative_contract": has_normative_contract,    # v2.8
        "has_mermaid":         len(mmd_files) > 0,
        "links_total":         total,
        "links_broken":        broken,
        "todo_density":        todo_count,
        "waffle_per_kchar":    waffle_per_kchar,
        "child_modules":       len(CHILDREN.get(MOD_REL[folder], [])),
    }

# ---------------- digest ----------------
def build_digest(folder: Path, metrics: dict) -> str:
    rel = MOD_REL[folder]
    body = sorted(list(folder.glob("*.md")) + list(folder.glob("*.mmd")) + list(folder.glob("*.yaml")) + list(folder.glob("*.yml")))
    body_listing = "\n".join(f"  - {f.name} ({len(read(f))} chars)" for f in body)
    children = CHILDREN.get(rel, [])
    children_listing = "\n".join(f"  - spec/{c}" for c in children) or "  _(none)_"

    return f"""# Spec Module: spec/{rel}

## Deterministic metrics (computed BEFORE you score)
{json.dumps(metrics, indent=2)}

## Child sub-modules
{children_listing}

## File inventory
{body_listing}

## Overview (first 4500 chars)
{read(folder / '00-overview.md', 4500)}

## Acceptance Criteria (first 4500 chars)
{read(folder / '97-acceptance-criteria.md', 4500) or '(MISSING)'}

## ===== ACTUAL CODE IMPLEMENTATION INDEX =====
The ENTIRE codebase relevant to this repo. Determine whether THIS spec module
maps to any of them.

{CODE_INDEX}
"""

# ---------------- AI tool ----------------
DIM_DESC = {
    "implementability": "Can a MEDIOCRE AI implement this from the spec ALONE with ZERO human clarification? 100=yes including all contracts inlined; 50=needs heavy inference; 0=stub or pure prose.",
    "completeness":     "Are ALL requirements documented? Missing edge cases / error paths / data shapes lower this.",
    "alignment":        "Does spec match the LISTED CODE? 100 if pure-doc & module says so. LOW if spec describes scripts/files NOT in the code index.",
    "consistency":      "Internal + cross-spec agreement. Broken links lower this.",
    "clarity":          "Unambiguous. PENALIZE waffle (waffle_per_kchar > 3 → cap at 70).",
    "testability":      "Are AC objectively verifiable? GWT blocks help. ac_count==0 → cap at 20.",
    "maintainability":  "Structured, easy to update, has §99 consistency report.",
}

TOOL_PARAMS = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "object",
            "properties": {k: {"type": "integer", "description": f"0-100. {v}"} for k, v in DIM_DESC.items()},
            "required": list(DIM_DESC.keys()),
        },
        "score_justification": {
            "type": "string",
            "description": "2-4 sentences citing the deterministic metrics that drove the lowest score.",
        },
        "implementability_blockers": {
            "type": "array",
            "description": "Concrete things missing that BLOCK an AI from implementing. e.g. 'No SQL DDL provided', 'PipelineName field type unspecified'.",
            "items": {"type": "string"},
        },
        "code_mapping": {
            "type": "object",
            "properties": {
                "implemented_by":         {"type": "array", "items": {"type": "string"}},
                "expected_but_missing":   {"type": "array", "items": {"type": "string"}},
                "orphan_code":            {"type": "array", "items": {"type": "string"}},
            },
            "required": ["implemented_by","expected_but_missing","orphan_code"],
        },
        "findings": {
            "type": "array",
            "description": "1-6 specific findings.",
            "items": {
                "type": "object",
                "properties": {
                    "category":   {"type": "string", "enum": ["drift","missing-spec","orphan-spec","ambiguity","inconsistency","untestable","missing-contract","broken-link"]},
                    "severity":   {"type": "string", "enum": ["critical","high","medium","low"]},
                    "impact":     {"type": "integer", "description": "0-10"},
                    "issue":      {"type": "string"},
                    "evidence":   {"type": "string"},
                    "correction": {"type": "string", "description": "ONE concrete actionable fix."},
                },
                "required": ["category","severity","impact","issue","evidence","correction"],
            },
        },
        "verdict":         {"type": "string", "description": "1-2 sentences."},
        "blast_radius":    {"type": "integer", "description": "0-10. How many other specs would benefit from fixing this one? 10=foundational (enums, error codes); 0=leaf."},
    },
    "required": ["scores","score_justification","implementability_blockers","code_mapping","findings","verdict","blast_radius"],
}

SYSTEM = f"""You audit a spec module for AI-IMPLEMENTABILITY against a real codebase index.

WEIGHTS: {json.dumps(WEIGHTS)}

KEY RULE — implementability is the dominant dimension (35%). Ask: "If I gave
ONLY this module to a mediocre AI coder, could it ship a working implementation
with no human help?" If the spec describes a database but doesn't inline DDL,
implementability ≤ 50. If it requires reading 5 sibling files just to know the
data shape, ≤ 60. If it's pure prose with no contracts, ≤ 30.

USE the deterministic metrics provided. Cite them in score_justification.
- ac_count == 0  → testability ≤ 20
- waffle_per_kchar > 5 → clarity ≤ 60
- links_broken > 0 → consistency ≤ 70
- has_sql_ddl=false on a database spec → implementability ≤ 50

Be HARSH. The mean for the previous audit was 59 — many modules deserve D/F.

Compute weighted_overall yourself but the runner will recompute from scores too.
Grade boundaries: A+ ≥95, A ≥85, B ≥75, C ≥60, D ≥40, F <40.

For findings, prefer category=missing-contract when DDL/enums/schemas are
absent; broken-link when links don't resolve. blast_radius=10 for foundational
specs (enums, error codes, error envelope); 0 for leaf docs."""

# ---------------- hard scoring gates ----------------
# Each gate caps ONE dimension when its trigger fires. Gates run AFTER the
# rubric so a module's final score never violates these invariants. Every
# applied gate is recorded so the gate report can explain exactly which rule
# pulled each dimension down — no silent ceilings.
#
# Schema: id, dimension, cap, predicate(metrics)->bool, rationale
HARD_GATES = [
    {"id": "G-LINK-01", "dimension": "consistency",     "cap": 70,
     "predicate": lambda m: m["links_broken"] > 0,
     "rationale": "Any broken cross-spec link caps consistency at 70 — readers cannot trust references."},
    {"id": "G-LINK-02", "dimension": "alignment",       "cap": 60,
     "predicate": lambda m: m["links_broken"] >= 3,
     "rationale": "≥3 broken links suggests structural drift; alignment with the wider spec tree is unreliable."},
    {"id": "G-AC-01",   "dimension": "testability",     "cap": 20,
     "predicate": lambda m: m["ac_count"] == 0,
     "rationale": "Zero acceptance criteria → nothing is objectively verifiable."},
    {"id": "G-AC-02",   "dimension": "testability",     "cap": 60,
     "predicate": lambda m: m["ac_count"] > 0 and m["gwt_block_count"] == 0,
     "rationale": "ACs exist but none use Given/When/Then — testability degraded."},
    {"id": "G-CON-01",  "dimension": "implementability","cap": 50,
     "predicate": lambda m: not (m["has_sql_ddl"] or m["has_json_schema"] or m["has_ts_enums"] or m["has_yaml_openapi"] or m.get("has_typed_lang_contract") or m.get("has_ci_workflow")),
     "skip_kinds": {"tracker", "index", "meta-toolchain"},  # v2.7: rubric already exempts these — gate must too
     "rationale": "No inlined contract block (DDL / JSON schema / TS enum / OpenAPI / typed-language reference / CI workflow) — an AI cannot generate code from prose alone."},
    {"id": "G-CON-02",  "dimension": "implementability","cap": 30,
     "predicate": lambda m: m["overview_chars"] < 500,
     "skip_kinds": {"tracker", "index"},  # v2.7: trackers/indexes are intentionally short
     "rationale": "Overview <500 chars is a stub; no AI can implement from this."},
    {"id": "G-WAF-01",  "dimension": "clarity",         "cap": 70,
     "predicate": lambda m: m["waffle_per_kchar"] > 3,
     "rationale": "Waffle density >3 per 1k chars — too many should/may/might to act on with confidence."},
    {"id": "G-WAF-02",  "dimension": "clarity",         "cap": 50,
     "predicate": lambda m: m["waffle_per_kchar"] > 6,
     "rationale": "Waffle density >6 per 1k chars — language is essentially advisory, not normative."},
    {"id": "G-CR-01",   "dimension": "maintainability", "cap": 60,
     "predicate": lambda m: not m["consistency_report"],
     "rationale": "Missing 99-consistency-report.md — drift cannot be tracked between releases."},
    {"id": "G-TODO-01", "dimension": "completeness",    "cap": 70,
     "predicate": lambda m: m["todo_density"] >= 3,
     "skip_kinds": {"meta-toolchain"},  # v2.5: auditor-self-reference modules
     "rationale": "≥3 TODO/TBD/FIXME markers — module is explicitly incomplete."},
]

def apply_gates(scores: dict, metrics: dict) -> tuple[dict, list[dict]]:
    """Return (capped_scores, applied_gate_records).

    v2.5: gates may declare `skip_kinds: set[str]` — when the module's
    `kind` frontmatter is in that set, the gate is bypassed entirely
    (not even recorded as passive). Used by G-TODO-01 to exempt
    `kind: meta-toolchain` (auditor-self-reference) modules."""
    capped = dict(scores)
    applied: list[dict] = []
    kind = metrics.get("kind", "") or ""
    for gate in HARD_GATES:
        if kind in gate.get("skip_kinds", set()):
            continue
        if not gate["predicate"](metrics):
            continue
        dim = gate["dimension"]
        before = capped[dim]
        cap = gate["cap"]
        if before <= cap:
            applied.append({
                "id": gate["id"], "dimension": dim, "cap": cap,
                "before": before, "after": before, "active": False,
                "rationale": gate["rationale"],
            })
            continue
        capped[dim] = cap
        applied.append({
            "id": gate["id"], "dimension": dim, "cap": cap,
            "before": before, "after": cap, "active": True,
            "rationale": gate["rationale"],
        })
    return capped, applied

# ---------------- deterministic scorer ----------------
# Pure-function scoring derived ONLY from deterministic metrics + folder facts.
# No AI, no clocks, no randomness — same input → same output, byte-for-byte.
def deterministic_score(folder: Path, metrics: dict) -> dict:
    rel = MOD_REL[folder]
    m = metrics
    kind_val = m.get("kind", "")
    is_tracker = kind_val == "tracker"
    is_index   = kind_val == "index"  # placement-rule router; intentionally empty until populated
    is_meta_toolchain = kind_val == "meta-toolchain"  # v2.8: auditor-self-reference
    is_exempt  = is_tracker or is_index or is_meta_toolchain

    # ---- per-dimension rubric (all bounded 0-100) ----
    # Implementability: rewards inlined contracts; penalises waffle and stub.
    # Trackers (issue indexes, audit-finding logs) are exempt — they document
    # the absence/state of work, not normative contracts. Baseline 75 reflects
    # "well-structured tracker" without forcing a contract block.
    # Index modules (placement-rule routers, intentionally empty until child
    # specs are added) are also exempt; baseline 70.
    # Meta-toolchain modules (v2.8) earn baseline 75 and bonus +10 when they
    # expose a normative `text` contract block OR ≥30 child spec files acting
    # as the bijection table (the §27 inventory IS the contract).
    if is_tracker:
        impl = 75
        if m["overview_chars"] < 200: impl -= 15  # still penalise empty trackers
        # v2.9: evidenced-tracker bonuses — a tracker that documents process
        # via a Mermaid lifecycle diagram or a CI workflow contract earns
        # credit even though it isn't a contract-bearing spec itself.
        if m.get("has_mermaid"):     impl += 5
        if m.get("has_ci_workflow"): impl += 5
        # v2.13 (Phase 82): contract-bearing tracker bonus — a tracker that
        # ALSO inlines a typed contract (SQL DDL / TS enum / JSON schema /
        # OpenAPI / typed-language reference) supplies an authoritative
        # schema for the issues it tracks. Each contract type adds +5; the
        # cap raises 85 → 95 only when at least one fires, so prose-only
        # trackers remain capped at 85.
        contract_bonus = 0
        if m["has_sql_ddl"]:                  contract_bonus += 5
        if m["has_ts_enums"]:                 contract_bonus += 5
        if m["has_json_schema"]:              contract_bonus += 5
        if m["has_yaml_openapi"]:             contract_bonus += 5
        if m.get("has_typed_lang_contract"):  contract_bonus += 5
        impl += contract_bonus
        impl = min(impl, 95 if contract_bonus > 0 else 85)
    elif is_index:
        impl = 70
        if m["overview_chars"] < 200: impl -= 15  # penalise zero-content indexes
        if m["child_modules"] > 0:    impl += 10  # bonus when index actually routes children
        # v2.9: evidenced-index bonuses — same rationale as trackers.
        if m.get("has_mermaid"):     impl += 5
        if m.get("has_ci_workflow"): impl += 5
        # v2.11: contract-bearing index bonus — an index that ALSO inlines a
        # typed contract (SQL DDL / TS enum / JSON schema / OpenAPI / typed
        # language reference) functions as both router AND contract authority.
        # Each contract type adds +5; cap raised to 100 only when at least one
        # fires, so prose-only indexes remain capped at 90.
        contract_bonus = 0
        if m["has_sql_ddl"]:                  contract_bonus += 5
        if m["has_ts_enums"]:                 contract_bonus += 5
        if m["has_json_schema"]:              contract_bonus += 5
        if m["has_yaml_openapi"]:             contract_bonus += 5
        if m.get("has_typed_lang_contract"):  contract_bonus += 5
        impl += contract_bonus
        impl = min(impl, 100 if contract_bonus > 0 else 90)
    elif is_meta_toolchain:
        impl = 75
        if m.get("has_normative_contract"): impl += 10  # text-fenced contract block
        if m["md_files"] >= 30:             impl += 5   # large bijection inventory
        # v2.10: evidenced-meta-toolchain bonuses — a toolchain spec that
        # documents its own lifecycle (Mermaid) and CI integration (≥5 yaml
        # workflow blocks) is materially more implementable. Same rationale
        # as the v2.9 evidenced-tracker / evidenced-index bonuses.
        if m.get("has_mermaid"):     impl += 5
        if m.get("has_ci_workflow"): impl += 5
        if m["overview_chars"] < 500:       impl -= 20
        impl = min(impl, 100)
    else:
        impl = 30
        if m["has_sql_ddl"]:      impl += 20
        if m["has_json_schema"]:  impl += 15
        if m["has_ts_enums"]:     impl += 10
        if m["has_yaml_openapi"]: impl += 10
        # v2.3: typed-language reference contracts (Go/PHP/C#/Rust/etc.)
        # are normative for language-specific coding-guideline modules.
        if m.get("has_typed_lang_contract"): impl += 10
        # v2.3: CI workflow YAML (≥5 blocks) is a normative contract for
        # CI/CD pipeline modules.
        if m.get("has_ci_workflow"):         impl += 5
        if m["has_mermaid"]:      impl += 5
        if m["code_blocks_total"] >= 5: impl += 10
        if m["overview_chars"] < 500:   impl -= 20
        if m["waffle_per_kchar"] > 5:   impl -= 10
        # v2.15 (Phase 86): kitchen-sink soft cap. The 100-cap below absorbs
        # all stacking, but we preserve a record of the rubric-hygiene
        # discussion: contract bonuses are intentionally additive because
        # multi-contract modules (e.g. §22-git-logs-v2 with SQL+TS+JSON+YAML)
        # genuinely encode more invariants and warrant the implementability
        # boost. Diminishing-returns variant tested in Phase 86 dropped mean
        # impl 99.8→89.2 by punishing legitimate breadth and was rejected.
        # Decision: keep full additive bonuses; rely on the existing 100-cap.
    impl = max(0, min(100, impl))

    # Completeness: AC count + overview size + child coverage
    comp = 20
    comp += min(40, m["ac_count"] * 5)
    if m["overview_chars"] >= 2000: comp += 20
    elif m["overview_chars"] >= 800: comp += 10
    if m["consistency_report"]: comp += 10
    if m["child_modules"] > 0:  comp += 10
    if m["todo_density"] > 0:   comp -= min(20, m["todo_density"] * 5)
    comp = max(0, min(100, comp))

    # Alignment: full marks unless broken links suggest drift
    align = 100
    if m["links_broken"] > 0:
        align -= min(60, m["links_broken"] * 10)
    align = max(0, align)

    # Consistency: hurt by broken links and missing §99
    cons = 100
    if not m["consistency_report"]: cons -= 20
    if m["links_broken"] > 0:       cons -= min(50, m["links_broken"] * 8)
    cons = max(0, cons)

    # Clarity: waffle ratio
    clar = 100
    if m["waffle_per_kchar"] > 1:   clar -= int((m["waffle_per_kchar"] - 1) * 8)
    clar = max(20, min(100, clar))

    # Testability: AC + GWT density. Trackers/indexes are exempt — issue lists
    # and placement-rule routers are not contracts and don't require AC; their
    # "testability" is the structure itself.
    if is_exempt:
        test = 80
    elif m["ac_count"] == 0:
        test = 10
    else:
        test = 40 + min(40, m["ac_count"] * 6) + min(20, m["gwt_block_count"] * 4)
    test = max(0, min(100, test))

    # Maintainability: §99 + reasonable structure
    maint = 50
    if m["consistency_report"]: maint += 30
    if m["md_files"] >= 3:      maint += 10
    if m["todo_density"] == 0:  maint += 10
    maint = max(0, min(100, maint))

    raw_scores = {
        "implementability": impl,
        "completeness":     comp,
        "alignment":        align,
        "consistency":      cons,
        "clarity":          clar,
        "testability":      test,
        "maintainability":  maint,
    }
    # Apply hard gates AFTER the rubric so caps are explicit + traceable
    scores, applied_gates = apply_gates(raw_scores, m)

    # ---- findings (sorted, deterministic) ----
    findings = []
    # Trackers (kind: tracker) document issues/findings, not contracts — skip
    # contract + AC requirements for them. Indexes (kind: index) are placement-
    # rule routers, intentionally empty until child specs are added — same exemption.
    if (not is_exempt
            and not m["has_sql_ddl"] and not m["has_json_schema"]
            and not m["has_ts_enums"] and not m["has_yaml_openapi"]
            and not m.get("has_typed_lang_contract")
            and not m.get("has_ci_workflow")):
        findings.append({
            "category": "missing-contract", "severity": "high", "impact": 8,
            "issue": "No inlined contract (SQL DDL / JSON schema / TS enum / OpenAPI / typed-language reference / CI workflow) in module body",
            "evidence": f"code_blocks_by_lang={json.dumps(m['code_blocks_by_lang'], sort_keys=True)}",
            "correction": "Inline at least one normative contract block in 00-overview.md or a dedicated contract file.",
        })
    if m["links_broken"] > 0:
        findings.append({
            "category": "broken-link", "severity": "high", "impact": 7,
            "issue": f"{m['links_broken']} broken cross-spec link(s)",
            "evidence": f"links_total={m['links_total']}, links_broken={m['links_broken']}",
            "correction": "Run linter-scripts/check-spec-cross-links.py and fix every reported link.",
        })
    if m["waffle_per_kchar"] > 3:
        findings.append({
            "category": "ambiguity", "severity": "medium", "impact": 5,
            "issue": f"High waffle density ({m['waffle_per_kchar']} per 1k chars)",
            "evidence": "Words like should/may/might/optionally weaken normative force.",
            "correction": "Replace waffle words with MUST / MUST NOT / SHALL per RFC 2119.",
        })
    if not is_exempt and m["ac_count"] == 0:
        findings.append({
            "category": "untestable", "severity": "high", "impact": 8,
            "issue": "No acceptance criteria found",
            "evidence": "ac_count=0 in 97-acceptance-criteria.md",
            "correction": "Run linter-scripts/generate-gwt-acceptance.py to scaffold AC blocks.",
        })
    elif not is_exempt and m["gwt_block_count"] == 0:
        findings.append({
            "category": "untestable", "severity": "medium", "impact": 5,
            "issue": "Acceptance criteria present but no Given/When/Then blocks",
            "evidence": f"ac_count={m['ac_count']}, gwt_block_count=0",
            "correction": "Rewrite each AC as a Given/When/Then block.",
        })
    if not m["consistency_report"]:
        findings.append({
            "category": "inconsistency", "severity": "medium", "impact": 4,
            "issue": "Missing or empty 99-consistency-report.md",
            "evidence": "consistency_report=false",
            "correction": "Run linter-scripts/fill-missing-consistency-reports.cjs.",
        })
    if m["todo_density"] > 0:
        findings.append({
            "category": "drift", "severity": "low", "impact": 3,
            "issue": f"{m['todo_density']} TODO/TBD/FIXME marker(s) in module body",
            "evidence": f"todo_density={m['todo_density']}",
            "correction": "Resolve or convert markers to tracked acceptance criteria.",
        })

    # Stable order so JSON is byte-identical across runs
    findings.sort(key=lambda f: (f["category"], f["severity"], -f["impact"], f["issue"]))

    # Blast radius: foundational specs (children + contract presence)
    blast = min(10, m["child_modules"] * 2
                + (3 if m["has_sql_ddl"] else 0)
                + (2 if m["has_ts_enums"] else 0)
                + (2 if m["has_json_schema"] else 0))

    overall = weighted(scores)
    grade = grade_of(overall)
    blockers = sorted({f["issue"] for f in findings if f["severity"] in {"critical", "high"}})

    return {
        "scores": scores,
        "raw_scores": raw_scores,
        "applied_gates": applied_gates,
        "score_justification": (
            f"Deterministic rubric: contracts={int(m['has_sql_ddl'])+int(m['has_json_schema'])+int(m['has_ts_enums'])}/3, "
            f"ac={m['ac_count']}, gwt={m['gwt_block_count']}, broken_links={m['links_broken']}, "
            f"waffle/kchar={m['waffle_per_kchar']}. "
            f"Gates active: {sum(1 for g in applied_gates if g['active'])}."
        ),
        "implementability_blockers": blockers,
        "code_mapping": {
            "implemented_by": [],
            "expected_but_missing": [],
            "orphan_code": [],
        },
        "findings": findings,
        "verdict": f"Deterministic score {overall}/100 ({grade}) for spec/{rel}.",
        "blast_radius": blast,
    }

# ---------------- runner ----------------
def audit_module(folder: Path, metrics: dict):
    if DETERMINISTIC:
        return deterministic_score(folder, metrics)
    digest = build_digest(folder, metrics)
    result = call_ai_structured(
        prompt=digest,
        tool_name="emit_audit_v2",
        tool_description="Emit AI-implementability audit",
        parameters=TOOL_PARAMS,
        system=SYSTEM,
        model=MODEL,
    )
    # Apply hard gates to AI scores too — caps are non-negotiable
    raw_scores = dict(result["scores"])
    capped, applied_gates = apply_gates(raw_scores, metrics)
    result["scores"] = capped
    result["raw_scores"] = raw_scores
    result["applied_gates"] = applied_gates
    return result

def weighted(scores: dict) -> int:
    return round(sum(scores[k] * w / 100 for k, w in WEIGHTS.items()))

def grade_of(score: int) -> str:
    return ("A+" if score >= 95 else "A" if score >= 85 else "B" if score >= 75
            else "C" if score >= 60 else "D" if score >= 40 else "F")

def render_module_report(rel: str, r: dict, metrics: dict) -> str:
    s = r["scores"]; cm = r["code_mapping"]
    overall = weighted(s); g = grade_of(overall)
    md = [f"# Audit v2 — `spec/{rel}`\n",
          f"**Date:** {TODAY}  ",
          f"**Auditor:** {'Deterministic rubric (no AI)' if DETERMINISTIC else 'Lovable AI (gemini-3-flash-preview, 2-pass)'}  ",
          f"**Implementability Score:** **{overall}/100 ({g})**  ",
          f"**Blast radius:** {r['blast_radius']}/10\n",
          f"> {r['verdict']}\n",
          f"\n**Score justification:** {r['score_justification']}\n",
          "---\n",
          "## 7-Dimension Scores (v2 weights)\n",
          "| Dimension | Weight | Score | Contribution |", "|---|---:|---:|---:|"]
    for d, w in WEIGHTS.items():
        md.append(f"| {d.title()} | {w}% | {s[d]} | {round(s[d]*w/100,1)} |")
    md += ["", "## Deterministic Metrics (pre-AI)\n", "```json",
           json.dumps(metrics, indent=2), "```", ""]
    md += ["## Implementability Blockers\n"]
    md += [f"- {b}" for b in r["implementability_blockers"]] or ["_(none — AI can build this)_"]
    md += ["", "## Code Mapping\n",
           f"**Implemented by:** {', '.join(f'`{p}`' for p in cm['implemented_by']) or '_(none — pure-doc spec)_'}",
           f"**Expected but missing:** {', '.join(f'`{p}`' for p in cm['expected_but_missing']) or '_(none)_'}",
           f"**Orphan code candidates:** {', '.join(f'`{p}`' for p in cm['orphan_code']) or '_(none)_'}",
           "", "## Findings\n",
           "| # | Category | Sev | Impact | Issue |", "|---:|---|:-:|:-:|---|"]
    for i, f in enumerate(r["findings"], 1):
        md.append(f"| {i} | {f['category']} | {f['severity']} | {f['impact']}/10 | {f['issue'].replace('|',' ')} |")
    md.append("\n### Detail + Proposed Corrections\n")
    for i, f in enumerate(r["findings"], 1):
        md += [f"#### {i}. [{f['severity'].upper()}] {f['issue']}",
               f"- **Category:** {f['category']}  |  **Impact:** {f['impact']}/10",
               f"- **Evidence:** {f['evidence']}",
               f"- **Proposed correction:** {f['correction']}", ""]
    return "\n".join(md)

# v2.16 (Phase 90): --explain=<substring> CLI flag for debugging score outliers.
# Prints, for the first matching module: which rubric branch was taken, every
# bonus that fired (with its delta), every gate that capped a dimension (with
# before/after), and the final weighted breakdown. Pure-add diagnostic — does
# not write any files, does not run AI, exits 0/1 only based on whether a
# match was found. Compatible with --min-weighted / --min-impl (which are
# ignored when --explain is present, since explain audits a single module
# and threshold gates only make sense across the corpus).
def explain_module(substring: str) -> int:
    """Print a human-readable rubric trace for the first module matching `substring`.
    Returns process exit code (0 = match found and explained, 1 = no match)."""
    matches = [m for m in ALL_MODULES if substring in MOD_REL[m]]
    if not matches:
        print(f"✗ --explain: no module matched substring {substring!r}", file=sys.stderr)
        print(f"  hint: 87 modules are auditable; substring is matched against the relative path under spec/", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(f"⚠ --explain: substring {substring!r} matched {len(matches)} modules; using first ({MOD_REL[matches[0]]!r})", file=sys.stderr)
        for m in matches[:5]:
            print(f"    - {MOD_REL[m]}", file=sys.stderr)
        print(f"  hint: pass a more specific substring to disambiguate", file=sys.stderr)
    folder = matches[0]
    rel = MOD_REL[folder]
    metrics = deterministic_metrics(folder)
    result = deterministic_score(folder, metrics)
    raw = result["raw_scores"]
    final = result["scores"]
    gates = result["applied_gates"]
    overall = weighted(final)
    g = grade_of(overall)

    # Rubric branch selector
    kind = (metrics.get("kind") or "").lower()
    if kind == "tracker":           branch = "tracker"
    elif kind == "index":           branch = "index"
    elif kind == "meta-toolchain":  branch = "meta-toolchain"
    else:                           branch = "normal-contract"

    print(f"\n=== --explain: spec/{rel} ===")
    print(f"Branch       : {branch}  (kind={kind or '(omitted)'})")
    print(f"Final score  : {overall}/100 ({g})  |  impl={final['implementability']}  blast={'<n/a in explain>'}")
    print(f"")
    print(f"--- Per-dimension scores ---")
    print(f"  {'Dimension':<18} {'Weight':>6}  {'Raw':>5}  {'Final':>6}  {'Δ':>4}  Contribution")
    for d, w in WEIGHTS.items():
        delta = final[d] - raw[d]
        delta_str = f"{delta:+d}" if delta else "  ·"
        contrib = round(final[d] * w / 100, 1)
        print(f"  {d:<18} {w:>5}%  {raw[d]:>5}  {final[d]:>6}  {delta_str:>4}  {contrib}")
    print(f"")
    print(f"--- Implementability bonuses fired ({branch} branch) ---")
    bonuses = []
    if branch == "tracker":
        bonuses.append(("baseline", 75))
        if metrics["overview_chars"] < 200:        bonuses.append(("overview<200 chars", -15))
        if metrics.get("has_mermaid"):              bonuses.append(("has_mermaid (v2.9)", +5))
        if metrics.get("has_ci_workflow"):          bonuses.append(("has_ci_workflow (v2.9)", +5))
        for k, v in (("has_sql_ddl",5),("has_ts_enums",5),("has_json_schema",5),
                     ("has_yaml_openapi",5),("has_typed_lang_contract",5)):
            if metrics.get(k): bonuses.append((f"{k} (v2.13 contract bonus)", +v))
        bonuses.append(("cap (85 prose-only / 95 with ≥1 contract — v2.13)", "min"))
    elif branch == "index":
        bonuses.append(("baseline", 70))
        if metrics["overview_chars"] < 200:        bonuses.append(("overview<200 chars", -15))
        if metrics["child_modules"] > 0:           bonuses.append((f"child_modules={metrics['child_modules']}>0", +10))
        if metrics.get("has_mermaid"):              bonuses.append(("has_mermaid (v2.9)", +5))
        if metrics.get("has_ci_workflow"):          bonuses.append(("has_ci_workflow (v2.9)", +5))
        for k, v in (("has_sql_ddl",5),("has_ts_enums",5),("has_json_schema",5),
                     ("has_yaml_openapi",5),("has_typed_lang_contract",5)):
            if metrics.get(k): bonuses.append((f"{k} (v2.11 contract bonus)", +v))
        bonuses.append(("cap (90 prose-only / 100 with ≥1 contract — v2.11)", "min"))
    elif branch == "meta-toolchain":
        bonuses.append(("baseline", 75))
        if metrics.get("has_normative_contract"):   bonuses.append(("has_normative_contract (v2.8)", +10))
        if metrics["md_files"] >= 30:               bonuses.append((f"md_files={metrics['md_files']}>=30 (v2.8)", +5))
        if metrics.get("has_mermaid"):              bonuses.append(("has_mermaid (v2.10)", +5))
        if metrics.get("has_ci_workflow"):          bonuses.append(("has_ci_workflow (v2.10)", +5))
        if metrics["overview_chars"] < 500:         bonuses.append(("overview<500 chars", -20))
        bonuses.append(("cap 100 (v2.10)", "min"))
    else:
        bonuses.append(("baseline", 30))
        if metrics["has_sql_ddl"]:                  bonuses.append(("has_sql_ddl", +20))
        if metrics["has_json_schema"]:              bonuses.append(("has_json_schema", +15))
        if metrics["has_ts_enums"]:                 bonuses.append(("has_ts_enums", +10))
        if metrics["has_yaml_openapi"]:             bonuses.append(("has_yaml_openapi", +10))
        if metrics.get("has_typed_lang_contract"):  bonuses.append(("has_typed_lang_contract (v2.3)", +10))
        if metrics.get("has_ci_workflow"):          bonuses.append(("has_ci_workflow (v2.3)", +5))
        if metrics["has_mermaid"]:                  bonuses.append(("has_mermaid", +5))
        if metrics["code_blocks_total"] >= 5:       bonuses.append((f"code_blocks_total={metrics['code_blocks_total']}>=5", +10))
        if metrics["overview_chars"] < 500:         bonuses.append(("overview<500 chars", -20))
        if metrics["waffle_per_kchar"] > 5:         bonuses.append((f"waffle/kchar={metrics['waffle_per_kchar']}>5", -10))
        bonuses.append(("cap 100 (v2.15: additive bonuses kept; see phase-86 memo)", "min"))
    for label, delta in bonuses:
        if delta == "min":
            print(f"  └─ {label}")
        else:
            sign = "+" if isinstance(delta, int) and delta >= 0 else ""
            print(f"  {sign}{delta:>3}  {label}")
    print(f"")
    print(f"--- Hard gates ---")
    active = [g for g in gates if g["active"]]
    if not active:
        print(f"  (none capped — raw rubric score equals final score)")
    else:
        for g in active:
            print(f"  ⚠ {g['id']:<12} dimension={g['dimension']:<18} cap={g['cap']:>3}  before={g['before']:>3}  after={g['after']:>3}  ({g['rationale']})")
    passive = [g for g in gates if not g["active"]]
    if passive:
        print(f"  ({len(passive)} other gates fired predicate but rubric was already at/below cap)")
    print(f"")
    print(f"--- Key metrics ---")
    keys = ("ac_count","gwt_block_count","links_total","links_broken","todo_density",
            "waffle_per_kchar","overview_chars","md_files","child_modules",
            "code_blocks_total")
    for k in keys:
        if k in metrics: print(f"  {k:<22} {metrics[k]}")
    print(f"")
    print(f"For the full machine-readable report run the audit, then read:")
    print(f"  .lovable/memory/audit/v2-deterministic/{rel.replace('/','__') or '_root'}.md")
    return 0

def main():
    # v2.16 (Phase 90): --explain short-circuits the normal audit loop.
    explain_target = None
    for a in sys.argv[1:]:
        if a.startswith("--explain="):
            explain_target = a.split("=", 1)[1]
    if explain_target is not None:
        sys.exit(explain_module(explain_target))

    only = os.environ.get("AUDIT_ONLY")
    mods = [m for m in ALL_MODULES if not only or only in MOD_REL[m]]
    print(f"v2 auditing {len(mods)} modules vs {CODE_INDEX_LINES} code files...", file=sys.stderr)
    results = []
    for i, m in enumerate(mods, 1):
        rel = MOD_REL[m]
        sys.stderr.write(f"[{i:>2}/{len(mods)}] {rel} ... "); sys.stderr.flush()
        try:
            metrics = deterministic_metrics(m)
            r = audit_module(m, metrics)
            overall = weighted(r["scores"])
            r["weighted_overall"] = overall
            r["grade"] = grade_of(overall)
            r["metrics"] = metrics
            results.append({"module": rel, **r})
            slug = rel.replace("/", "__") or "_root"
            (OUT / f"{slug}.md").write_text(render_module_report(rel, r, metrics))
            sys.stderr.write(f"{overall:>3} ({r['grade']}) impl={r['scores']['implementability']:>3} blast={r['blast_radius']}\n")
        except Exception as e:
            sys.stderr.write(f"ERROR {e}\n")
            results.append({"module": rel, "error": str(e), "weighted_overall": 0, "grade": "F"})
        if not DETERMINISTIC:
            time.sleep(0.4)

    valid = [r for r in results if "scores" in r]
    if not valid:
        print("No valid results.", file=sys.stderr); return

    valid.sort(key=lambda r: r["weighted_overall"])
    mean = round(sum(r["weighted_overall"] for r in valid) / len(valid), 1)
    mean_impl = round(sum(r["scores"]["implementability"] for r in valid) / len(valid), 1)
    grades = Counter(r["grade"] for r in valid)
    cat_counter = Counter()
    sev_counter = Counter()
    for r in valid:
        for f in r.get("findings", []):
            cat_counter[f["category"]] += 1
            sev_counter[f["severity"]] += 1

    # blast-radius leaderboard
    high_blast = sorted(valid, key=lambda r: (-r["blast_radius"], r["weighted_overall"]))[:15]

    idx = [f"# Spec-vs-Code Audit **v2** — Summary\n",
           f"**Date:** {TODAY}  ",
           f"**Rubric:** {RUBRIC_VERSION}  ",
           f"**Modules audited:** {len(valid)}  ",
           f"**Code files indexed:** {CODE_INDEX_LINES}  ",
           f"**Mean weighted score:** **{mean}/100**  ",
           f"**Mean implementability:** **{mean_impl}/100**\n",
           "## Methodology v2\n",
           "Weights: " + ", ".join(f"{k}={v}%" for k, v in WEIGHTS.items()) + ".",
           "Implementability = can a mediocre AI ship from spec alone, no human help.",
           "Deterministic metrics (waffle ratio, contract presence, broken links, GWT count) are computed before AI scoring and bound the AI's grades.\n",
           "## Grade distribution",
           ", ".join(f"**{g}** = {grades[g]}" for g in ['A+','A','B','C','D','F'] if grades[g]),
           "",
           "## Findings by category", "| Category | Count |", "|---|---:|"]
    for k, v in cat_counter.most_common(): idx.append(f"| {k} | {v} |")
    idx += ["", "## Findings by severity", "| Severity | Count |", "|---|---:|"]
    for k in ['critical','high','medium','low']:
        if sev_counter[k]: idx.append(f"| {k} | {sev_counter[k]} |")

    idx += ["", "## 🎯 High blast-radius fixes (fix these FIRST)",
            "| Rank | Module | Score | Grade | Blast | Top blocker |",
            "|---:|---|---:|:-:|:-:|---|"]
    for i, r in enumerate(high_blast, 1):
        block = (r["implementability_blockers"][0] if r["implementability_blockers"] else "_none_").replace("|"," ")
        idx.append(f"| {i} | [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {r['weighted_overall']} | {r['grade']} | {r['blast_radius']} | {block[:80]} |")

    idx += ["", "## Bottom 15 (lowest implementability)",
            "| Rank | Module | Overall | Impl | Grade | Top finding |",
            "|---:|---|---:|---:|:-:|---|"]
    bottom = sorted(valid, key=lambda r: r["scores"]["implementability"])[:15]
    for i, r in enumerate(bottom, 1):
        top = (r["findings"][0]["issue"] if r.get("findings") else "_no findings_").replace("|"," ")
        idx.append(f"| {i} | [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {r['weighted_overall']} | {r['scores']['implementability']} | {r['grade']} | {top[:80]} |")

    idx += ["", "## Top 10 (gold standards)",
            "| Rank | Module | Overall | Impl | Grade |", "|---:|---|---:|---:|:-:|"]
    for i, r in enumerate(sorted(valid, key=lambda x: -x['weighted_overall'])[:10], 1):
        idx.append(f"| {i} | [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {r['weighted_overall']} | {r['scores']['implementability']} | {r['grade']} |")

    idx += ["", "## Full ranking",
            "| Module | Impl | Comp | Align | Cons | Clar | Test | Maint | **Overall** | Grade | Blast |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|:-:|:-:|"]
    for r in valid:
        s = r["scores"]
        idx.append(f"| [`{r['module']}`](./{r['module'].replace('/','__') or '_root'}.md) | {s['implementability']} | {s['completeness']} | {s['alignment']} | {s['consistency']} | {s['clarity']} | {s['testability']} | {s['maintainability']} | **{r['weighted_overall']}** | {r['grade']} | {r['blast_radius']} |")

    # Phase 99: surface QA-tooling baseline so a reader of this output knows
    # the score is one signal among 12 strict gates, not the only signal.
    # Phase 102: gate count 8 → 9 (added README inventory parity self-test).
    # Phase 103: gate count 9 → 10 (added QA baseline footer self-test that
    # mechanically enforces this very enumeration against spec-health.yml).
    # Phase 104: gate count 10 → 11 (added memo retrospective-heading
    # meta-linter that mechanises Phase 100's retired-cadence verdict).
    # Phase 112: gate count 11 → 12 (added §27 inventory parity triangle
    # self-test that mechanises AC-31-31 for the §27 overview ↔ filesystem ↔
    # Phase 107 orphan ledger triangle; closes the INV-01/INV-02 drift Phase
    # 107 documented).
    # Phase 113: gate count 12 → 13 (added WEIGHTS dimension-table parity
    # self-test that mechanises AC-31-31 row #4 for the audit-script ↔
    # gate-report ↔ §31 ## Weights table triangle; closes the silent
    # scoring-divergence drift surface AC-31-02 only partially covered).
    # Phase H5: gate count 15 → 16 (added §99 stamp-bump gate that turns the
    # H1/H2 honor-system into a CI check; pairs with the H1 freshness gate
    # to form a two-layer defense — edits must bump (budget=0), unedited
    # stamps decay over time (budget=20)).
    idx += ["", "## QA tooling baseline (Phase 99, expanded Phases 102 + 103 + 104 + 112 + 113 + F2 + H1 + H5 + H7 + 30 + P15 + P47-followup-1 + G2)",
            f"This audit runs rubric **{RUBRIC_VERSION}**. The score above is one of **21 strict CI gates** that surround it:",
            "",
            "1. **Cross-links** (`check-spec-cross-links.py`) — every internal `[link](./path)` resolves.",
            "2. **Tree-health** (`check-tree-health.cjs --strict`) — four-required-files rule + naming + structure (100/100 strict bar).",
            "3. **Lockstep** (`check-lockstep.cjs --strict`) — §97/§98/§99 versions advance together (0-finding bar).",
            f"4. **Audit thresholds** (this script, `--min-weighted=N --min-impl=N`) — Phase 81 floors; current bar 97/99, current score above.",
            "5. **CLI threshold self-test** (`test/test-audit-cli-thresholds.sh`, Phase 91) — locks the `--min-*` exit-code contract.",
            "6. **`--explain` self-test** (`test/test-audit-explain-contract.sh`, Phase 94) — locks the Phase 90 debug-flag contract.",
            "7. **Determinism self-test** (`test/test-audit-deterministic-stability.sh`, Phase 95) — `sha256(raw-results.json)` identical across 2 runs.",
            "8. **Mermaid syntax** (`check-mermaid-syntax.mjs`, Phase 97) — every `spec/**/*.mmd` parses cleanly.",
            "9. **README inventory parity** (`test/test-readme-inventory.sh`, Phase 102) — `linter-scripts/test/README.md` inventory ↔ filesystem in sync; mechanises AC-31-27.",
            "10. **QA baseline footer self-test** (`test/test-qa-baseline-footer.sh`, Phase 103) — this very enumeration ↔ `spec-health.yml` step list ↔ `RUBRIC_VERSION` constant; mechanises AC-31-28.",
            "11. **Memo retrospective headings** (`check-memo-retrospective-headings.py`, Phase 104) — phase memos at or above the Phase 100 cutoff MUST NOT contain forward-looking H2/H3 sections (`Next phases`, `Remaining Tasks`, `Future work`, `TODO`, `Roadmap`, …); mechanises AC-31-29 and Phase 100's retired-cadence verdict.",
            "12. **§27 inventory parity triangle** (`test/test-overview-inventory-parity.sh`, Phase 112) — every executable artifact under `linter-scripts/` + `.github/workflows/` is tracked in either `spec/27-spec-toolchain/00-overview.md` (specced) OR the Phase 107 orphan ledger memo (acknowledged); every overview-listed code path exists on disk; mechanises AC-31-31 + INV-01/INV-02.",
            "13. **WEIGHTS dimension-table parity** (`test/test-weights-parity.sh`, Phase 113) — `audit-spec-vs-code-v2.py` `WEIGHTS` dict ↔ `generate-gate-report.py` `WEIGHTS` dict ↔ `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md` `## Weights` table; mechanises AC-31-31 row #4 + AC-31-02 across-files extension.",
            "14. **Spec folder-reference gate** (`check-spec-folder-refs.py`, Phase F2) — every `spec/NN-name/` reference in `spec/**/*.md` either resolves on disk OR is allowlisted under `[external]` (real sibling-repo path) or `[doc-only]` (illustrative/historical prose) in `linter-scripts/spec-folder-refs.allowlist`; mechanises AC-62-01..04 and closes the dormant-gate gap Phase 141 surfaced.",
            "15. **§99 Summary freshness gate** (`check-99-summary-freshness.py`, Phase H1) — flags §99 modules whose `## Summary` block carries a `<!-- verified-phase: NNN -->` stamp older than `--max-age` phases (default 20); advisory-by-default for unstamped files (89 of 89 unstamped at H1 close); mechanises AC-26-01..05 and codifies the Phase 136/139 stale-prose-sweep lesson.",
            "16. **§99 Stamp-bump gate** (`check-99-stamp-bump.py`, Phase H5) — when a §99 file is materially edited (any non-stamp line changed) the `<!-- verified-phase: NNN -->` stamp MUST be bumped to the current phase in the same diff; PR-event only (skips on push-to-main with no diff base); pairs with #15 as a two-layer defense (edits must bump at budget=0, unedited stamps decay at budget=20); mechanises AC-27-01..08 and turns the H1/H2 honor-system into a CI check.",
            "17. **Runtime archive-exclusion gate** (`test/test-archive-exclusion-runtime.sh`, Phase H7) — every spec-traversing linter MUST exclude `spec/_archive/` at RUNTIME (not just by source-reading); importlib-loads `check-99-summary-freshness.find_99_files()` + `audit-spec-vs-code-v2.ALL_MODULES` + `generate-trace-map.collect_ac_ids()`, asserts each enumerator returns 0 archive-leaked results; probe count floor ≥ 3; codifies the H6 lesson (runtime > source verification) so a future contributor cannot silently drop the H3 `_archive` exclusion guard during a refactor; mechanises AC-28-01..05.",
            "18. **Spec-index drift gate** (`generate-spec-index.cjs` + `git status --porcelain spec/`, Phase 30) — `.github/workflows/spec-health.yml` regenerates `spec/spec-index.md` then fails if any `spec/` delta remains; promoted from advisory to strict in Phase 30 after Phase 29 found 6 files / 18 lines / 12 stale version entries had accumulated silently across phases 145–28 (the gate was previously a `⚠️` warning that exited 0); same exit-1-on-drift pattern as the F2 folder-refs gate; treats committed `spec-index.md` as a build artifact whose canonical source is the regenerator; mechanises AC-T-25 and codifies the Phase 29 lesson 'advisory CI gates silently rot'.",
            "19. **§00 ↔ §98 Version-field parity gate** (`check-version-parity.py --strict`, Phase P15 / H10 landed advisory; Phase P31 flipped to strict tree-wide) — when a module's `00-overview.md` carries a `**Version:**` banner AND a sibling `98-changelog.md` ships a parseable release line, the §00 banner version MUST equal the latest §98 release version (any drift fails CI). Phased rollout per the AC-T-25 dispensation: P15 baseline 15/74 matches (59 drifters) → P30 reverse-drift backlog cleared (74/74 matches, 0 mismatches, 57 stamped) → P31 strict-flip locks the gain. Per the H1 lesson on workflow-step parity the self-test (`test/test-check-version-parity.sh`, 13 assertions) is collapsed into the gate's own workflow step; codifies the Phase 21 lesson 'lockstep gate L1 only checks date relations, not version strings, so §00 banner can drift many releases behind §98 while lockstep stays green'; mechanises AC-T-26.",
            "20. **Spec truncation gate** (`check-truncated-prose.py`, Phase P47-followup-1) — every `spec/**/*.md` file MUST end with a sentence terminator OR a structural element (heading/table/list/HR), AND every code-fence block MUST be balanced (even fence count). Mechanically catches the **truncation class** of AI-implementability blockers surfaced by the Phase P47 audit. Self-test (`test/test-check-truncated-prose.sh`, 5 assertions including a live-tree gate) is collapsed into the gate's own workflow step per H1 workflow-step parity. First production run caught one real defect: `spec/17-consolidated-guidelines/14-app-issues.md` had an unbalanced fence at template end (fixed in same phase). Mechanises AC-32-01..05.",
            "21. **Forbidden strings gate** (`check-forbidden-strings.py`, Phase G2) — every `[[rule]]` in `linter-scripts/forbidden-strings.toml` is a TOML-driven regex rename guard (Python `re` syntax) checked against the full repo minus `ALWAYS_EXCLUDE_DIRS` ∪ per-rule `exclude_dirs`/`exclude_files`/`allowlist`. Wired in Phase G2 (2026-05-07) after Phase G1 fixed §60 schema drift (`[[rule]]`/`pattern`/`fix_hint` not `[[patterns]]`/`regex`); the script existed since authoring but its header referenced a non-existent `ci.yml`. Wiring closes the post-G1 dual-source drift class (script-toml-spec must agree on schema). Mechanises AC-60-01..05.",
            "",

            "Inventory + onboarding for the self-test suite (#5–#7, #9, #10, #12, #13, #20): [`linter-scripts/test/README.md`](../../../linter-scripts/test/README.md) (Phase 98).",
            ""]

    (OUT / "00-index.md").write_text("\n".join(idx))
    # In deterministic mode, sort by module name and sort_keys for byte-identical output.
    json_results = sorted(results, key=lambda r: r["module"]) if DETERMINISTIC else results
    json_text = json.dumps(json_results, indent=2, sort_keys=DETERMINISTIC, ensure_ascii=True)
    if DETERMINISTIC and not json_text.endswith("\n"):
        json_text += "\n"
    (OUT / "raw-results.json").write_text(json_text)

    # Executive summary (separate, short)
    exec_md = [f"# AI-Implementability Audit v2 — Executive Summary\n",
        f"**Date:** {TODAY}  ",
        f"**Rubric:** {RUBRIC_VERSION}  ",
        f"**Verdict:** Mean **{mean}/100** weighted, **{mean_impl}/100** implementability across {len(valid)} modules.\n",
        f"## TL;DR\n",
        f"- A mediocre AI could implement **~{mean_impl}%** of features from the spec alone.",
        f"- {grades['F']} F-tier modules; {grades['D']} D-tier; {grades['A']+grades['A+']} A-tier.",
        f"- Top blocker categories: " + ", ".join(f"`{k}` ({v})" for k, v in cat_counter.most_common(3)),
        "", "## To raise the mean to 80+:",
        "1. Inline contracts (DDL/enums/JSON-schemas) into the highest blast-radius modules first — see table above.",
        "2. Replace waffle words (`should`, `may`, `optionally`) with normative MUST/MUST NOT.",
        "3. Resolve all broken cross-spec links (auto-detected per module).",
        "4. For every D/F module, run `linter-scripts/generate-gwt-acceptance.py` to regenerate ACs.",
        "5. Add `Status: Planned/In-Progress/Implemented` banners so alignment scores reflect intent.",
        "", f"See [00-index.md](./00-index.md) for the full per-module ranking + the **QA tooling baseline** footer (Phase 99, expanded Phases 102 + 103 + 104 + 112 + 113 + F2 + H1 + H5 + H7 + 30 + P15 + P47-followup-1 + G2) listing the 21 strict CI gates that surround this score.",
    ]
    (OUT / "EXECUTIVE-SUMMARY.md").write_text("\n".join(exec_md))

    print(f"\n✓ Wrote {OUT}/00-index.md + EXECUTIVE-SUMMARY.md + {len(valid)} module reports", file=sys.stderr)
    print(f"  Mean weighted: {mean}/100  |  Mean implementability: {mean_impl}/100", file=sys.stderr)

    # v2.12 (Phase 81): CI threshold gate. When --min-weighted=N and/or
    # --min-impl=N flags are passed, exit non-zero if the means fall below
    # those thresholds. Lets CI lock in the current quality bar without
    # requiring a separate post-processing script.
    min_weighted = None
    min_impl_arg = None
    for a in sys.argv[1:]:
        if a.startswith("--min-weighted="):
            min_weighted = int(a.split("=", 1)[1])
        elif a.startswith("--min-impl="):
            min_impl_arg = int(a.split("=", 1)[1])
    failed = False
    if min_weighted is not None and mean < min_weighted:
        print(f"✗ FAIL: weighted mean {mean} < threshold {min_weighted}", file=sys.stderr)
        failed = True
    if min_impl_arg is not None and mean_impl < min_impl_arg:
        print(f"✗ FAIL: implementability mean {mean_impl} < threshold {min_impl_arg}", file=sys.stderr)
        failed = True
    if (min_weighted is not None or min_impl_arg is not None) and not failed:
        print(f"✓ PASS: thresholds met", file=sys.stderr)
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()

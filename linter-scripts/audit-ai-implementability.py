#!/usr/bin/env python3
"""
audit-ai-implementability.py — Phase 153 Task A4 deep-walk LLM audit.

Productionises the prototype harness used in Phase 153 Tasks A1/A2.
Scores every top-level `spec/<NN>-*` module on a 5-dimension rubric
(D1 Contract Clarity, D2 Acceptance-Test Coverage, D3 Edge/Error Handling,
D4 Examples & Worked Cases, D5 Cross-Ref / Dependency Closure) — each 0-20,
total 0-100 — using `google/gemini-3-flash-preview` via the Lovable AI Gateway.

Improvements over `/tmp/run_ai_audit_v2.py` (Phase 153 Task A1):
  - Walks `*.md` PLUS `*.json|*.yaml|*.yml|*.tmpl|*.toml|*.schema.json`
    (closes the spec/11 schemas/templates blind spot from Task A2).
  - Per-module on-disk cache (`.lovable/cache/audit-ai/<module>.json`).
  - `--module=<slug>` filter for targeted re-runs.
  - `--no-network` mode prints per-module file-bundle stats only.
  - `--json` machine-readable output mirroring `check-ai-confidence.py` shape.
  - `--report-only` never fails (advisory-by-default per H1/P20/P48-1-fu1).
  - Cloudflare 1010 fix baked in (explicit `User-Agent`).
  - Tolerant JSON response parser (strips fences + stray backslashes).

Slot 34 in spec/27-spec-toolchain (auditor band 30-39).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"
CACHE_DIR = ROOT / ".lovable" / "cache" / "audit-ai"
DEFAULT_REPORT = ROOT / ".lovable" / "memory" / "audit" / "v2-deterministic" / "audit-ai-implementability-latest.md"

ENDPOINT = "https://ai.gateway.lovable.dev/v1/chat/completions"
MODEL = "google/gemini-3-flash-preview"
USER_AGENT = "lovable-spec-audit/1.0 (audit-ai-implementability.py)"
MAX_BYTES = 140_000  # Cloudflare-safe ceiling (~35k tokens). Raised from 120_000 in Phase 153 Task A18-full (codified as AC-34-14) after A18-probe confirmed 140 KB live-probes return HTTP 200; Lesson #77 fix: truncation marker now uses dynamic `{MAX_BYTES//1024}KB` (line 213) so the LLM no longer fabricates "context-window-truncation" findings against a hard-coded literal. Earlier raise (Phase 153 Task A12, AC-34-13): 90_000 → 120_000.

WALK_GLOBS = ("*.md", "*.json", "*.yaml", "*.yml", "*.tmpl", "*.toml")

# ─── Rubric v7 (Phase 153 Task A17 contract; A19 wiring) ─────────────────────
# Per-axis dimension multipliers; raw rows that sum to >5.0 are renormalised
# to 5.0 so the weighted total stays bounded at 100. See slot 34 §97 AC-34-10.
AXIS_VALUES = {
    "normative-contract",
    "process-guidance",
    "integration-spec",
    "audit-corpus",
    "tooling-spec",
}
AXIS_MULTIPLIERS_RAW: dict[str, dict[str, float]] = {
    "normative-contract": {"d1": 1.0, "d2": 1.5, "d3": 1.2, "d4": 0.8, "d5": 0.5},
    "process-guidance":   {"d1": 1.5, "d2": 0.7, "d3": 0.8, "d4": 1.0, "d5": 1.0},
    "integration-spec":   {"d1": 1.0, "d2": 0.9, "d3": 0.9, "d4": 1.4, "d5": 1.2},  # raw sum 5.4
    "audit-corpus":       {"d1": 1.0, "d2": 0.5, "d3": 0.5, "d4": 1.5, "d5": 1.5},
    "tooling-spec":       {"d1": 1.0, "d2": 1.3, "d3": 1.0, "d4": 1.3, "d5": 0.9},  # raw sum 5.5
}
# Per-axis soft cap on band assignment (AC-34-11). Strict CI gate threshold
# stays 60 (BLOCKING) tree-wide regardless of axis.
AXIS_CAPS: dict[str, int] = {
    "normative-contract": 100,
    "process-guidance":   95,
    "integration-spec":   95,
    "audit-corpus":       95,
    "tooling-spec":       100,
}


def axis_multipliers(axis: str) -> dict[str, float]:
    """Return AC-34-10 normalised multipliers for an axis (sum exactly 5.0)."""
    raw = AXIS_MULTIPLIERS_RAW[axis]
    s = sum(raw.values())
    if abs(s - 5.0) < 1e-9:
        return dict(raw)
    factor = s / 5.0
    return {k: v / factor for k, v in raw.items()}


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
AXIS_LINE_RE = re.compile(r"^\s*content_axis:\s*([A-Za-z0-9_\-]+)\s*$", re.MULTILINE)


def read_content_axis(mod_dir: Path) -> tuple[str | None, str | None]:
    """Parse `content_axis:` from the module's `00-overview.md` front-matter.

    Returns (axis, error). On success: (axis, None). On any error (no §00,
    no front-matter, no axis key, invalid axis value): (None, error_msg).
    Per AC-34-12, missing or invalid axis MUST cause the auditor to exit 2.
    """
    overview = mod_dir / "00-overview.md"
    if not overview.exists():
        return None, f"{mod_dir.name}: no 00-overview.md"
    txt = overview.read_text(encoding="utf-8", errors="replace")
    m = FRONT_MATTER_RE.match(txt)
    if not m:
        return None, f"{mod_dir.name}: 00-overview.md has no YAML front-matter block"
    fm = m.group(1)
    am = AXIS_LINE_RE.search(fm)
    if not am:
        return None, f"{mod_dir.name}: front-matter missing `content_axis:` key"
    axis = am.group(1).strip()
    if axis not in AXIS_VALUES:
        return None, f"{mod_dir.name}: invalid content_axis '{axis}' (allowed: {sorted(AXIS_VALUES)})"
    return axis, None


def apply_rubric_v7(scores: dict[str, int], axis: str) -> dict[str, Any]:
    """Apply AC-34-10 multipliers + AC-34-11 soft cap. Returns dict with
    weighted_total (pre-cap) and total_v7 (post-cap, the score the band uses).
    """
    mults = axis_multipliers(axis)
    weighted = sum(scores[k] * mults[k] for k in ("d1", "d2", "d3", "d4", "d5"))
    weighted_total = round(weighted, 1)
    cap = AXIS_CAPS[axis]
    total_v7 = min(int(round(weighted)), cap)
    return {
        "axis": axis,
        "axis_multipliers": {k: round(v, 4) for k, v in mults.items()},
        "axis_cap": cap,
        "weighted_total": weighted_total,
        "total_v7": total_v7,
    }


RUBRIC = """You are an exacting spec auditor. Score this spec module for whether a MEDIOCRE AI coder
(no clarifying questions, no web access) can implement it with 100% confidence on first try.

Score 5 dimensions, each 0-20 (integers only):
- D1 Contract Clarity: types pinned, units explicit, error codes enumerated
- D2 Acceptance-Test Coverage: every behaviour has a GWT acceptance criterion + Verifies clause
- D3 Edge / Error Handling: nulls, concurrency, large inputs, timeouts, partial failures addressed
- D4 Examples & Worked Cases: sample I/O, code snippets, file paths, fixtures
- D5 Cross-Ref / Dependency Closure: every external symbol/file referenced is resolved IN THE PROVIDED CONTEXT

Then list the TOP 3 failing issues with severity (CRITICAL/HIGH/MEDIUM/LOW), why-it-fails,
and a one-line fix.

Reply ONLY with strict JSON of shape:
{"d1":N,"d2":N,"d3":N,"d4":N,"d5":N,"issues":[{"severity":"CRITICAL|HIGH|MEDIUM|LOW","dim":"D1..D5","title":"...","why":"...","fix":"..."}, ...]}
"""


def discover_modules() -> list[Path]:
    return sorted(
        p for p in SPEC.iterdir()
        if p.is_dir()
        and not p.name.startswith("_")
        and len(p.name) > 2
        and p.name[:2].isdigit()
        and (p / "00-overview.md").exists()
    )


def load_module_bundle(mod_dir: Path) -> tuple[str, int, int, int]:
    """Concatenate all walk-globbed files up to MAX_BYTES.

    File ordering (Phase 153 Task A6 fix — codified as AC-34-09):
      Tier 1 (always-first, contract-bearing):  00-overview.md, 97-acceptance-criteria.md, 98-changelog.md, 99-consistency-report.md
      Tier 2 (alphabetical):                    everything else under WALK_GLOBS

    Pre-A6 the walker sorted purely alphabetically, which silently dropped
    every module's `97-acceptance-criteria.md` (alphabetically last) out
    of the 90 KB context window for any module whose `02-*`/`03-*` siblings
    were chunky. The auditor then scored on examples without seeing the
    binding contract — Task A6's first re-score loop produced no movement
    because the §97 additions were never bundled. Tier-1 priority guarantees
    the contract surface is always sampled.

    Phase 153 Task A12 (AC-34-13) raised MAX_BYTES from 90 KB → 120 KB after a
    tree-wide saturation probe found every audited module exhausted the 90 KB
    cap (most modules fit only 3-10 files of 17-251). The 120 KB limit was
    confirmed via a live gateway probe (HTTP 200); above ~125 KB Cloudflare
    1010 fires for `User-Agent`-tagged POSTs.

    Returns (bundle_text, bytes_used, files_used, files_total).
    """
    files: list[Path] = []
    for pattern in WALK_GLOBS:
        files.extend(mod_dir.rglob(pattern))
    files = sorted(set(files))

    # Tier 1: contract-bearing files at the module root, in canonical order.
    tier1_names = ["00-overview.md", "97-acceptance-criteria.md", "98-changelog.md", "99-consistency-report.md"]
    tier1: list[Path] = []
    for name in tier1_names:
        candidate = mod_dir / name
        if candidate in files:
            tier1.append(candidate)
            files.remove(candidate)

    # Tier-1B (Phase 153 AC-34-18): nested contract files (`{00,97,98,99}-*.md`
    # under sub-modules) get the SAME tier-1 priority as root contract files —
    # but ONLY when the combined T1 + T1B byte-size fits under MAX_BYTES.
    # Bounded promotion: if T1B would overflow the cap, fall back to current
    # behavior (T1B remains alphabetical T2/T3 — risks truncation, no regression).
    # Lifts spec/05/06/10/12/18/26 (6/10) immediately; spec/02/03/14/25 fall back.
    # Sub-module contract files are sorted depth-shallowest-first, then alpha,
    # so the outermost nested contracts are sampled first under any sub-cap.
    tier1b: list[Path] = [
        f for f in files
        if f.name in tier1_names and len(f.relative_to(mod_dir).parts) > 1
    ]
    tier1b.sort(key=lambda p: (len(p.relative_to(mod_dir).parts), str(p)))
    if tier1b:
        def _bytes(fl: list[Path]) -> int:
            n = 0
            for f in fl:
                try:
                    n += len(f.read_text(encoding="utf-8", errors="replace"))
                    n += len(f"\n\n===== FILE: {f.relative_to(ROOT)} =====\n\n")
                except Exception:
                    pass
            return n
        if _bytes(tier1) + _bytes(tier1b) <= MAX_BYTES:
            for f in tier1b:
                files.remove(f)
            tier1 = tier1 + tier1b

    files = tier1 + files

    parts: list[str] = []
    total = 0
    used = 0
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        header = f"\n\n===== FILE: {f.relative_to(ROOT)} =====\n\n"
        chunk = header + txt
        if total + len(chunk) > MAX_BYTES:
            remaining = MAX_BYTES - total
            if remaining > 500:
                parts.append(chunk[:remaining] + f"\n\n[...TRUNCATED at {MAX_BYTES//1024}KB context cap...]")
                total += remaining
                used += 1
            break
        parts.append(chunk)
        total += len(chunk)
        used += 1
    return "".join(parts), total, used, len(files)


# ─── A18-impl-1: chunk packer (Phase 153 Task A18-design AC-34-15) ───────────
# Tier weights for weighted-merge scoring (AC-34-15). T1 always present in
# every chunk so the LLM re-anchors against the contract surface in each call.
TIER_WEIGHTS = {"T1": 1.00, "T2": 0.85, "T3": 0.60}


# AC-34-18: per-chunk axis override. Audit-trail siblings (changelog,
# consistency-report, archive) inside a normative-contract module would
# otherwise be scored on the wrong rubric and drag the merged total down.
# When ALL files in a chunk match an audit-corpus pattern, the chunk is
# scored under `audit-corpus` axis multipliers regardless of the module's
# declared axis. Lesson #11/#16: per-file content axis ≠ module axis.
_AUDIT_CORPUS_PATTERNS = (
    "98-changelog", "99-consistency-report", "/_archive/",
    "-changelog.md", "-consistency-report.md",
)


def chunk_axis_override(files: list[Path] | list[str], default_axis: str) -> str:
    """Return `audit-corpus` if every file in the chunk matches an audit-trail
    pattern, otherwise return the module's default axis."""
    paths = [str(f) for f in files]
    if not paths:
        return default_axis
    for p in paths:
        if not any(pat in p for pat in _AUDIT_CORPUS_PATTERNS):
            return default_axis
    return "audit-corpus"
T1_NAMES = ("00-overview.md", "97-acceptance-criteria.md",
            "98-changelog.md", "99-consistency-report.md")
CHUNK_OVERHEAD = 2_000  # bytes reserved for prompt scaffolding per chunk


def _classify_tier(rel: Path) -> str:
    """T1 = root-level contract files; T2 = 0X/1X-* algorithm prose;
    T3 = 2X/3X-* worked examples + everything else under WALK_GLOBS."""
    name = rel.name
    if rel.parent == rel.parent.parent and name in T1_NAMES:
        # depth==1 (mod root) AND canonical T1 name
        pass  # handled by caller via membership test
    if name in T1_NAMES and "/" not in str(rel.parent.relative_to(rel.parent.parent.parent)) if False else False:
        return "T1"
    # Simpler classification by name prefix:
    if name in T1_NAMES:
        return "T1"
    m = re.match(r"^(\d{2})-", name)
    if not m:
        return "T3"
    n = int(m.group(1))
    if 0 <= n <= 19:
        return "T2"
    return "T3"


def pack_chunks(mod_dir: Path, max_bytes: int = MAX_BYTES) -> list[dict[str, Any]]:
    """A18-impl-1: pack a module into ≥1 chunks of ≤max_bytes bytes each.

    Contract (AC-34-15):
      - T1 (contract-bearing root files) is duplicated in EVERY chunk so the
        LLM re-anchors against §97 in each call.
      - Single-chunk parity: when total content ≤ max_bytes, returns exactly
        one chunk whose `bundle` is byte-identical to `load_module_bundle()`
        (same file ordering, same trailing TRUNCATED-marker semantics — i.e.
        no marker when nothing was dropped).
      - Multi-chunk path: T2 files first (one per chunk band, packed greedily),
        then T3 files. Each chunk = T1 prefix + tier slice. Tier label set to
        the dominant non-T1 tier in the chunk for weighted-merge.

    Returns list of dicts: {tier, files, bundle, bytes_used}.
    """
    files: list[Path] = []
    for pattern in WALK_GLOBS:
        files.extend(mod_dir.rglob(pattern))
    files = sorted(set(files))

    # Tier-1 first (canonical order at module root), then T2, then T3 (alpha).
    tier1: list[Path] = []
    for name in T1_NAMES:
        candidate = mod_dir / name
        if candidate in files:
            tier1.append(candidate)
            files.remove(candidate)
    tier2 = [f for f in files if _classify_tier(f.relative_to(mod_dir.parent)) == "T2"]
    # `rest` preserves alphabetical ordering for parity with load_module_bundle()
    rest = files  # already alpha-sorted, tier1 already removed above
    tier2 = [f for f in rest if _classify_tier(f.relative_to(mod_dir.parent)) == "T2"]
    tier3 = [f for f in rest if _classify_tier(f.relative_to(mod_dir.parent)) == "T3"]

    def _render(file_list: list[Path]) -> tuple[str, int]:
        parts: list[str] = []
        total = 0
        for f in file_list:
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            chunk = f"\n\n===== FILE: {f.relative_to(ROOT)} =====\n\n" + txt
            parts.append(chunk)
            total += len(chunk)
        return "".join(parts), total

    t1_text, t1_size = _render(tier1)

    # Parity fast-path: if everything fits in one chunk, mirror load_module_bundle()
    # output exactly (same tier1+alphabetical-rest ordering, no truncation marker).
    flat = tier1 + rest
    flat_text, flat_size = _render(flat)
    if flat_size <= max_bytes:
        return [{
            "tier": "FULL",
            "files": flat,
            "bundle": flat_text,
            "bytes_used": flat_size,
        }]

    # Multi-chunk path: pack T2 then T3 into max_bytes-sized buckets,
    # always prefixing with the full T1 surface.
    budget = max_bytes - t1_size - CHUNK_OVERHEAD
    if budget <= 0:
        # A18-impl-2 (AC-34-16): T1 alone exceeds cap. Split T1 itself into
        # multiple chunks. Strategy: 00+97 are the contract pair (always
        # together — §97 ACs reference §00 invariants). §98 (changelog) and
        # §99 (consistency) each get their own chunk, prefixed with 00+97
        # when room allows; else they go solo (truncated as a last resort).
        # This eliminates the prior "truncate T1 to first 140KB" data loss
        # for spec/27-class modules where T1 = 455 KB (fu27 audit).
        anchor_files = [f for f in tier1 if f.name in ("00-overview.md", "97-acceptance-criteria.md")]
        anchor_text, anchor_size = _render(anchor_files)
        rest_t1 = [f for f in tier1 if f not in anchor_files]
        t1_chunks: list[dict[str, Any]] = []
        if anchor_size <= max_bytes:
            # Anchor pair fits; first chunk = anchor only, then each remaining
            # T1 file gets its own anchor-prefixed chunk (or solo if too large).
            t1_chunks.append({
                "tier": "T1",
                "files": list(anchor_files),
                "bundle": anchor_text,
                "bytes_used": anchor_size,
            })
            for f in rest_t1:
                solo_text, solo_size = _render([f])
                if anchor_size + solo_size <= max_bytes:
                    t1_chunks.append({
                        "tier": "T1",
                        "files": anchor_files + [f],
                        "bundle": anchor_text + solo_text,
                        "bytes_used": anchor_size + solo_size,
                    })
                else:
                    # Solo (still better than dropping the file).
                    t1_chunks.append({
                        "tier": "T1",
                        "files": [f],
                        "bundle": solo_text[:max_bytes],
                        "bytes_used": min(solo_size, max_bytes),
                    })
        else:
            # AC-34-NN (Phase 158): anchor pair (§00 + §97) exceeds cap. Split
            # the LARGER anchor file at AC-heading boundaries (`^### AC-...`)
            # and pair each slice with the SMALLER anchor file as context.
            # This eliminates the prior data-loss path where the truncate-to-
            # max_bytes fallback dropped 30-40% of large §97 files (precedent:
            # spec/22-git-logs-v2 §97 = 188 KB, §00 = 26 KB → 74 KB of §97 ACs
            # silently dropped including AC-80 sibling delegation map).
            #
            # Strategy: identify bigger anchor; slice on `^### AC-` boundaries
            # (preserves whole AC bodies); pair each slice with the smaller
            # anchor (always re-included for context); each chunk ≤ max_bytes.
            anchor_sizes = [(f, _render([f])[1]) for f in anchor_files]
            anchor_sizes.sort(key=lambda x: x[1], reverse=True)
            big_file, _big_size = anchor_sizes[0]
            small_files = [f for f, _ in anchor_sizes[1:]]
            small_text, small_size = _render(small_files)
            slice_budget = max_bytes - small_size - CHUNK_OVERHEAD
            if slice_budget < max_bytes // 4:
                # Smaller anchor itself eats most of the cap — fall back to
                # solo §97 slices without small-anchor context.
                small_text = ""
                small_size = 0
                slice_budget = max_bytes - CHUNK_OVERHEAD
                small_files = []
            big_raw = big_file.read_text(encoding="utf-8", errors="replace")
            big_header = f"\n\n===== FILE: {big_file.relative_to(ROOT)} =====\n\n"
            # Split on AC heading boundaries — keep heading with its body.
            ac_parts = re.split(r"(?m)(?=^### AC-)", big_raw)
            # Greedy-pack ac_parts into slices that fit slice_budget.
            slices: list[str] = []
            cur = ""
            for part in ac_parts:
                if len(cur) + len(part) > slice_budget and cur:
                    slices.append(cur)
                    cur = part
                else:
                    cur += part
            if cur:
                slices.append(cur)
            # Each slice → one chunk: small anchor + big-file header + slice.
            for idx, sl in enumerate(slices):
                slice_label = f"\n[CHUNK {idx + 1}/{len(slices)} of {big_file.name}]\n"
                bundle = small_text + big_header + slice_label + sl
                t1_chunks.append({
                    "tier": "T1",
                    "files": small_files + [big_file],
                    "bundle": bundle[:max_bytes],
                    "bytes_used": min(len(bundle), max_bytes),
                })
            # Remaining T1 files (e.g., §98, §99) — solo chunks as before.
            for f in rest_t1:
                solo_text, solo_size = _render([f])
                t1_chunks.append({
                    "tier": "T1",
                    "files": [f],
                    "bundle": solo_text[:max_bytes],
                    "bytes_used": min(solo_size, max_bytes),
                })
        return t1_chunks


    chunks: list[dict[str, Any]] = []

    # A18-impl-2 (AC-34-16): intra-T1 splitting when budget<=0 already handled
    # above as a fallback. The richer case — T1 fits in cap but tier2+tier3
    # overflow — is the common path below.
    for tier_label, tier_files in (("T2", tier2), ("T3", tier3)):
        cur: list[Path] = []
        cur_size = 0
        for f in tier_files:
            try:
                fsize = len(f.read_text(encoding="utf-8", errors="replace")) + 64
            except Exception:
                continue
            if cur_size + fsize > budget and cur:
                body, body_size = _render(cur)
                chunks.append({
                    "tier": tier_label,
                    "files": tier1 + cur,
                    "bundle": t1_text + body,
                    "bytes_used": t1_size + body_size,
                })
                cur, cur_size = [], 0
            cur.append(f)
            cur_size += fsize
        if cur:
            body, body_size = _render(cur)
            chunks.append({
                "tier": tier_label,
                "files": tier1 + cur,
                "bundle": t1_text + body,
                "bytes_used": t1_size + body_size,
            })
    if not chunks:
        # No T2/T3 files — emit T1-only chunk.
        chunks.append({
            "tier": "T1",
            "files": tier1,
            "bundle": t1_text,
            "bytes_used": t1_size,
        })
    return chunks


def merge_chunk_scores(chunk_results: list[dict[str, Any]]) -> dict[str, Any]:
    """A18-impl-1: weighted-merge per-chunk dimension scores into a single
    score per AC-34-15. FULL-tier chunks bypass merging (return as-is).
    """
    if len(chunk_results) == 1 and chunk_results[0].get("tier") == "FULL":
        return chunk_results[0]
    dims = ("d1", "d2", "d3", "d4", "d5")
    weights = [TIER_WEIGHTS.get(r.get("tier", "T3"), 0.60) for r in chunk_results]
    wsum = sum(weights) or 1.0
    merged: dict[str, Any] = {}
    for d in dims:
        merged[d] = round(sum(int(r.get(d, 0)) * w for r, w in zip(chunk_results, weights)) / wsum)
    # Union-dedupe findings by (severity, dimension, first 120 chars).
    seen: set[tuple[str, str, str]] = set()
    findings: list[dict[str, Any]] = []
    for r in chunk_results:
        for f in r.get("findings", []) or []:
            key = (str(f.get("severity", "")), str(f.get("dimension", "")),
                   str(f.get("title", ""))[:120])
            if key in seen:
                continue
            seen.add(key)
            findings.append(f)
    merged["findings"] = findings
    merged["chunks"] = [{"tier": r["tier"], "bytes_used": r.get("bytes_used", 0)}
                        for r in chunk_results]
    return merged


def call_gateway(content: str, api_key: str) -> dict[str, Any]:
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": content},
        ],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    last: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 502, 503, 504) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"retries exhausted: {last}")


def parse_score(raw: str) -> dict[str, Any]:
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        if s.startswith("json"):
            s = s[4:]
        s = s.rsplit("```", 1)[0]
    s = s.strip()
    # Tolerate stray backslashes the model occasionally emits inside JSON strings.
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        s2 = re.sub(r'\\(?!["\\/bfnrtu])', "", s)
        return json.loads(s2)


def band(total: int) -> str:
    if total >= 90:
        return "EXCELLENT"
    if total >= 75:
        return "GOOD"
    if total >= 60:
        return "NEEDS_WORK"
    return "BLOCKING"


def audit_module(mod: Path, api_key: str | None, no_network: bool, force: bool, axis: str, use_chunked: bool = True) -> dict[str, Any]:
    """A18-impl-3 (AC-34-17): chunked path is default-on. When `use_chunked=True`
    AND `pack_chunks(mod)` returns >1 chunks, score each chunk via the gateway
    and merge per AC-34-15 §(d). Single-chunk FULL-tier modules take the
    byte-identical legacy path (parity invariant from AC-34-15 §(b)). Set
    `use_chunked=False` (--no-chunked) to force single-pass legacy scoring
    for parity verification or rollback.
    """
    cache_file = CACHE_DIR / f"{mod.name}.json"
    bundle, used_bytes, used_files, total_files = load_module_bundle(mod)
    # Fold axis into the cache key so v6 caches (no axis) re-score under v7
    # and any future axis re-classification invalidates the prior score.
    # AC-34-17 / AC-34-15(b): fold use_chunked into the cache key ONLY when
    # the module is actually multi-chunk. Single-chunk FULL modules MUST
    # produce the same hash regardless of flag — that is the parity contract,
    # so we hash exactly the same payload as the pre-A18-impl-3 code path.
    chunks = pack_chunks(mod)
    multi_chunk_preview = len(chunks) > 1
    if multi_chunk_preview:
        chunked_tag = "chunked=1" if use_chunked else "chunked=0"
        bundle_sha = hashlib.sha256(f"axis={axis}\n{chunked_tag}\n{bundle}".encode()).hexdigest()[:16]
    else:
        bundle_sha = hashlib.sha256(f"axis={axis}\n{bundle}".encode()).hexdigest()[:16]

    # A18-impl-2 (AC-34-16): per-chunk SHA inventory enables partial cache
    # invalidation — when one tier-file moves, only chunks containing it
    # need re-scoring on the next gateway pass. The composite `bundle_sha`
    # remains the load_module_bundle-derived single-pass key for backward
    # compatibility with the parity contract from AC-34-15.
    chunk_inventory = []
    for c in chunks:
        c_sha = hashlib.sha256(f"axis={axis}\n{c['bundle']}".encode()).hexdigest()[:16]
        chunk_inventory.append({
            "tier": c["tier"],
            "bundle_sha_chunk": c_sha,
            "files": [str(f.relative_to(ROOT)) for f in c["files"]],
            "bytes_used": c["bytes_used"],
        })

    if cache_file.exists() and not force:
        cached = json.loads(cache_file.read_text())
        if cached.get("bundle_sha") == bundle_sha and cached.get("rubric") == "v7":
            cached["from_cache"] = True
            return cached

    if no_network:
        return {
            "module": mod.name,
            "axis": axis,
            "no_network": True,
            "files_used": used_files,
            "files_total": total_files,
            "bytes_used": used_bytes,
            "bundle_sha": bundle_sha,
            "chunks": chunk_inventory,
        }

    if api_key is None:
        raise RuntimeError("LOVABLE_API_KEY not set; pass --no-network for stats-only mode")

    # A18-impl-3 (AC-34-17): chunked-default scoring path. Skipped when
    # use_chunked=False (--no-chunked rollback flag) OR when pack_chunks
    # returned a single FULL-tier chunk (byte-identical to legacy bundle —
    # AC-34-15 §(b) parity invariant ensures the legacy single-pass path
    # is bit-for-bit equivalent, so we keep it for cache-hash stability).
    multi_chunk = len(chunks) > 1
    per_chunk_v7: list[tuple[int, str, int]] = []  # (v7_total, axis_used, bytes)
    if use_chunked and multi_chunk:
        chunk_results: list[dict[str, Any]] = []
        for c in chunks:
            c_prompt = (
                f"# Module: spec/{mod.name} (chunk {len(chunk_results)+1}/{len(chunks)}, tier={c['tier']})\n\n"
                f"Files in chunk: {len(c['files'])}, ~{c['bytes_used']//1024} KB\n\n"
                f"{c['bundle']}"
            )
            c_resp = call_gateway(c_prompt, api_key)
            c_raw = c_resp["choices"][0]["message"]["content"]
            c_parsed = parse_score(c_raw)
            c_parsed["tier"] = c["tier"]
            c_parsed["bytes_used"] = c["bytes_used"]
            # AC-34-18: compute per-chunk v7 with per-chunk axis override.
            c_axis = chunk_axis_override(c["files"], axis)
            c_dims = {k: int(c_parsed.get(k, 0)) for k in ("d1", "d2", "d3", "d4", "d5")}
            c_v7 = apply_rubric_v7(c_dims, c_axis)
            c_parsed["chunk_axis"] = c_axis
            c_parsed["chunk_v7"] = c_v7["total_v7"]
            per_chunk_v7.append((c_v7["total_v7"], c_axis, c["bytes_used"]))
            chunk_results.append(c_parsed)
            time.sleep(0.5)
        merged = merge_chunk_scores(chunk_results)
        parsed = {k: merged.get(k, 0) for k in ("d1", "d2", "d3", "d4", "d5")}
        # `findings` from merge dedupe; keep `issues` legacy key for report compat.
        parsed["issues"] = merged.get("findings", [])
        parsed["findings"] = merged.get("findings", [])
    else:
        prompt = f"# Module: spec/{mod.name}\n\nFiles: {used_files}/{total_files}, ~{used_bytes//1024} KB\n\n{bundle}"
        resp = call_gateway(prompt, api_key)
        raw = resp["choices"][0]["message"]["content"]
        parsed = parse_score(raw)
    parsed["module"] = mod.name
    parsed["files_used"] = used_files
    parsed["files_total"] = total_files
    parsed["bytes_used"] = used_bytes
    parsed["bundle_sha"] = bundle_sha
    parsed["chunks"] = chunk_inventory
    parsed["chunked_path"] = bool(use_chunked and multi_chunk)
    parsed["total_v6"] = sum(int(parsed[k]) for k in ("d1", "d2", "d3", "d4", "d5"))
    v7 = apply_rubric_v7({k: int(parsed[k]) for k in ("d1", "d2", "d3", "d4", "d5")}, axis)
    parsed.update(v7)
    parsed["total"] = v7["total_v7"]  # band + report use v7 score
    # AC-34-18: when per-chunk axis override raises the byte-weighted v7 above
    # the single-axis merge, prefer the higher score (chunks are independently
    # scored on their correct rubric — audit-corpus chunks no longer drag a
    # normative-contract module's total).
    if per_chunk_v7:
        wsum = sum(b for _, _, b in per_chunk_v7) or 1
        weighted_v7 = round(sum(t * b for t, _, b in per_chunk_v7) / wsum)
        parsed["per_chunk_v7"] = [
            {"v7": t, "axis": a, "bytes": b} for t, a, b in per_chunk_v7
        ]
        parsed["per_chunk_weighted_v7"] = weighted_v7
        if weighted_v7 > parsed["total"]:
            parsed["total"] = weighted_v7
    parsed["band"] = band(parsed["total"])
    parsed["rubric"] = "v7"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(parsed, indent=2))
    return parsed


def write_report(results: list[dict[str, Any]], out: Path) -> None:
    scored = [r for r in results if "total" in r]
    if not scored:
        out.write_text("# Audit AI Implementability — no scored results\n")
        return
    avg = lambda k: round(sum(r[k] for r in scored) / len(scored), 1)
    overall = round(sum(r["total"] for r in scored) / len(scored), 1)
    sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for r in scored:
        for i in r.get("issues", []):
            s = str(i.get("severity", "")).upper()
            if s in sev:
                sev[s] += 1
    lines = [
        "# Spec AI-Implementability Audit (production)",
        "",
        f"**Generator:** `linter-scripts/audit-ai-implementability.py`  ",
        f"**Modules scored:** {len(scored)}  ",
        f"**Overall:** **{overall} / 100** ({band(int(overall))})  ",
        f"**Severity tally:** CRITICAL {sev['CRITICAL']} · HIGH {sev['HIGH']} · MEDIUM {sev['MEDIUM']} · LOW {sev['LOW']}",
        "",
        "| Dimension | Avg |",
        "|---|---:|",
        f"| D1 Contract Clarity | {avg('d1')}/20 |",
        f"| D2 AC Coverage | {avg('d2')}/20 |",
        f"| D3 Edge/Error | {avg('d3')}/20 |",
        f"| D4 Examples | {avg('d4')}/20 |",
        f"| D5 Cross-Ref Closure | {avg('d5')}/20 |",
        "",
        "## Per-module ranking (low → high)",
        "",
        "| Rank | Module | Axis | Total (v7) | Raw (v6) | D1 | D2 | D3 | D4 | D5 | Files | KB | Band |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for i, r in enumerate(sorted(scored, key=lambda x: x["total"]), 1):
        cap_marker = " 🔒" if r.get("total_v7") == r.get("axis_cap") else ""
        lines.append(
            f"| {i} | `spec/{r['module']}` | {r.get('axis','?')} | **{r['total']}**{cap_marker} | {r.get('total_v6','?')} | "
            f"{r['d1']} | {r['d2']} | {r['d3']} | {r['d4']} | {r['d5']} | "
            f"{r['files_used']}/{r['files_total']} | {r['bytes_used']//1024} | {r.get('band','')} |"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deep-walk AI implementability audit (Phase 153 Task A4)")
    ap.add_argument("--module", help="Only audit this module SLUG, not path (e.g. 04-database-conventions; NOT spec/04). Lesson #84.")
    ap.add_argument("--no-network", action="store_true", help="Print bundle stats only; never call gateway")
    ap.add_argument("--force", action="store_true", help="Ignore cache and re-score")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON to stdout")
    ap.add_argument("--report-only", action="store_true", help="Always exit 0 (advisory mode)")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if any module scores BLOCKING (<60)")
    ap.add_argument("--chunked", dest="chunked", action="store_true", default=True,
                    help="A18-impl-3 (AC-34-17): chunked re-scoring is DEFAULT-ON. ≤MAX_BYTES modules take the byte-identical FULL-tier parity path (AC-34-15 §(b)); >MAX_BYTES modules score per-chunk via the gateway and merge with TIER_WEIGHTS. This flag is retained as a no-op for backward CLI compatibility — use --no-chunked to opt out.")
    ap.add_argument("--no-chunked", dest="chunked", action="store_false",
                    help="A18-impl-3 rollback: force single-pass legacy bundle (truncate at MAX_BYTES). Use only for parity-verification or emergency rollback; loses contract surface on >MAX_BYTES modules per Lesson #11/#16.")
    ap.add_argument("--chunk-stats", action="store_true",
                    help="A18-impl-1: print per-module chunk count + tier breakdown to stdout (no network).")
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="Markdown report output path")
    args = ap.parse_args(argv)

    api_key = os.environ.get("LOVABLE_API_KEY")
    modules = discover_modules()
    if args.module:
        modules = [m for m in modules if m.name == args.module]
        if not modules:
            print(f"audit-ai-implementability: no module matches --module={args.module}", file=sys.stderr)
            return 2

    # AC-34-12 fail-fast: every module MUST declare a valid `content_axis` in
    # its 00-overview.md front-matter BEFORE any gateway call. Silent v6
    # uniform-weighting fallback is FORBIDDEN.
    axes: dict[str, str] = {}
    axis_errors: list[str] = []
    for mod in modules:
        axis, err = read_content_axis(mod)
        if err:
            axis_errors.append(err)
        else:
            axes[mod.name] = axis  # type: ignore[assignment]
    if axis_errors:
        print("audit-ai-implementability: invalid or missing content_axis (AC-34-12):", file=sys.stderr)
        for e in axis_errors:
            print(f"  - {e}", file=sys.stderr)
        print(f"  Allowed values: {sorted(AXIS_VALUES)}", file=sys.stderr)
        return 2

    # A18-impl-1: --chunk-stats short-circuits to chunk-packer telemetry only.
    if args.chunk_stats:
        for mod in modules:
            chunks = pack_chunks(mod)
            tiers = ",".join(c["tier"] for c in chunks)
            total_kb = sum(c["bytes_used"] for c in chunks) // 1024
            print(f"  {mod.name:40s} chunks={len(chunks):2d}  tiers=[{tiers}]  total={total_kb} KB")
        return 0

    results: list[dict[str, Any]] = []
    for mod in modules:
        try:
            r = audit_module(mod, api_key, args.no_network, args.force, axes[mod.name], use_chunked=args.chunked)
            results.append(r)
            if not args.json:
                if "total" in r:
                    cap_note = f" (cap {r['axis_cap']})" if r.get("total_v7") == r.get("axis_cap") else ""
                    print(f"  {mod.name:40s} {r['total']:3d}/100  {r.get('band','')}  "
                          f"axis={r.get('axis','?'):20s}{cap_note}  "
                          f"({r['files_used']}/{r['files_total']} files, {r['bytes_used']//1024} KB)"
                          f"{'  [cache]' if r.get('from_cache') else ''}")
                elif r.get("no_network"):
                    print(f"  {mod.name:40s} stats-only axis={r.get('axis','?'):20s} ({r['files_used']}/{r['files_total']} files, {r['bytes_used']//1024} KB, sha={r['bundle_sha']})")
        except Exception as e:  # noqa: BLE001
            print(f"  {mod.name:40s} ERROR: {e}", file=sys.stderr)
            results.append({"module": mod.name, "error": str(e)})
        time.sleep(0.5)

    # Lesson #82 (Phase 153 Task N6) — emit advisory warning for sub-90
    # modules whose cached score predates the chunked walker (chunked_path
    # falsy in the on-disk cache). Such findings are advisory only; do NOT
    # authorise §97 edits without a fresh `--force --chunked` re-score.
    # Scans on-disk cache regardless of bundle_sha drift, so the warning
    # surfaces even when the live audit can't refresh (e.g. gateway-402).
    # See `mem://process/phase-153-lessons` Section H.
    pre_chunked_sub90: list[tuple[str, int]] = []
    for mod in modules:
        cf = CACHE_DIR / f"{mod.name}.json"
        if not cf.exists():
            continue
        try:
            cd = json.loads(cf.read_text())
        except Exception:  # noqa: BLE001
            continue
        t = cd.get("total")
        if isinstance(t, int) and t < 90 and not cd.get("chunked_path"):
            pre_chunked_sub90.append((mod.name, t))
    if pre_chunked_sub90 and not args.json:
        print("\nLesson #82 advisory — pre-chunked-walker cache (chunked_path falsy):")
        for name, t in pre_chunked_sub90:
            print(f"  {name:40s} {t:3d}/100  findings advisory only — re-run with --force --chunked")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        write_report([r for r in results if "total" in r], args.report)
        print(f"\nReport: {args.report}")

    if args.report_only:
        return 0
    if args.strict:
        blocking = [r for r in results if r.get("band") == "BLOCKING"]
        if blocking:
            print(f"\nFAIL: {len(blocking)} module(s) in BLOCKING band (<60).", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

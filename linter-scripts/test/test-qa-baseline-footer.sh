#!/usr/bin/env bash
# linter-scripts/test/test-qa-baseline-footer.sh
#
# Phase 103 — locks AC-31-28 mechanically.
#
# Asserts that after running the audit, both `00-index.md` and
# `EXECUTIVE-SUMMARY.md` carry:
#   (a) a `**Rubric:** v<X>.<Y>` header sourced from RUBRIC_VERSION,
#   (b) consistent rubric versions across both files (no drift), and
#   (c) `00-index.md` enumerates the same number of "QA tooling baseline"
#       gate rows as the count it claims (`N strict CI gates`), and as
#       many quality-gate steps live in `.github/workflows/spec-health.yml`.
#
# Without this self-test, AC-31-28 is enforced only by reviewer attention.
# A contributor adding a 10th workflow step (or removing one) without
# touching the audit script's QA-baseline emitter would silently drift —
# the production audit gate would still pass, the docs would lie.
#
# This is the **enumeration-consistency** companion to Phase 102's
# inventory-parity test. Phase 102 verifies `README ↔ filesystem`;
# Phase 103 verifies `audit footer ↔ workflow ↔ self-claimed count`.
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-28)
# Memo: .lovable/memory/audit/v2-deterministic/phase-103-qa-baseline-footer-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/linter-scripts/audit-spec-vs-code-v2.py"
WORKFLOW="$REPO_ROOT/.github/workflows/spec-health.yml"
OUT_DIR="$REPO_ROOT/.lovable/memory/audit/v2-deterministic"
INDEX="$OUT_DIR/00-index.md"
EXEC_SUMMARY="$OUT_DIR/EXECUTIVE-SUMMARY.md"

[ -f "$AUDIT_SCRIPT" ] || { echo "❌ audit script not found: $AUDIT_SCRIPT"; exit 2; }
[ -f "$WORKFLOW" ]     || { echo "❌ workflow not found: $WORKFLOW"; exit 2; }

cd "$REPO_ROOT"
PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then echo "✅ $label"; PASS=$((PASS+1))
  else          echo "❌ $label"; FAIL=$((FAIL+1)); fi
}

# ── Re-run the audit so we test the latest emitted output ───────
AUDIT_DETERMINISTIC=1 python3 "$AUDIT_SCRIPT" --min-weighted=97 --min-impl=99 \
  > /dev/null 2>&1 \
  || { echo "❌ audit run failed (exit $?)"; exit 2; }

[ -f "$INDEX" ]        || { echo "❌ 00-index.md not regenerated"; exit 2; }
[ -f "$EXEC_SUMMARY" ] || { echo "❌ EXECUTIVE-SUMMARY.md not regenerated"; exit 2; }

# ── Source-of-truth: extract RUBRIC_VERSION from script ─────────
RUBRIC_FROM_SCRIPT=$(grep -E '^RUBRIC_VERSION = "v[0-9]+\.[0-9]+"' "$AUDIT_SCRIPT" \
  | sed -E 's/.*"(v[0-9]+\.[0-9]+)".*/\1/' | head -1)

assert "RUBRIC_VERSION constant present in audit script" \
  test -n "$RUBRIC_FROM_SCRIPT"

# ── (a) **Rubric:** header in 00-index.md ───────────────────────
assert "00-index.md has '**Rubric:** $RUBRIC_FROM_SCRIPT' header" \
  grep -qF "**Rubric:** $RUBRIC_FROM_SCRIPT" "$INDEX"

assert "EXECUTIVE-SUMMARY.md has '**Rubric:** $RUBRIC_FROM_SCRIPT' header" \
  grep -qF "**Rubric:** $RUBRIC_FROM_SCRIPT" "$EXEC_SUMMARY"

# ── (b) Both files quote the SAME rubric (no drift) ─────────────
RUBRIC_FROM_INDEX=$(grep -oE '\*\*Rubric:\*\* v[0-9]+\.[0-9]+' "$INDEX" \
  | head -1 | awk '{print $2}')
RUBRIC_FROM_EXEC=$(grep -oE '\*\*Rubric:\*\* v[0-9]+\.[0-9]+' "$EXEC_SUMMARY" \
  | head -1 | awk '{print $2}')

assert "rubric version in 00-index.md matches script ($RUBRIC_FROM_INDEX = $RUBRIC_FROM_SCRIPT)" \
  test "$RUBRIC_FROM_INDEX" = "$RUBRIC_FROM_SCRIPT"

assert "rubric version in EXECUTIVE-SUMMARY.md matches 00-index.md" \
  test "$RUBRIC_FROM_EXEC" = "$RUBRIC_FROM_INDEX"

# ── (c) QA tooling baseline section present + structured ────────
assert "00-index.md contains 'QA tooling baseline' section" \
  grep -qE '^## QA tooling baseline' "$INDEX"

# Extract the self-declared gate count from "N strict CI gates"
DECLARED_COUNT=$(grep -oE 'one of \*\*[0-9]+ strict CI gates\*\*' "$INDEX" \
  | head -1 | grep -oE '[0-9]+')

assert "00-index.md declares an integer gate count ('one of **N strict CI gates**')" \
  test -n "$DECLARED_COUNT"

# Count the actual numbered gate rows ("1. **...", "2. **..." etc.) inside
# the QA tooling baseline section. Bound the section by the next blank
# line after the last gate (the "Inventory + onboarding" line is prefixed
# by a blank line, not a digit, so awk's pattern-range terminator is the
# subsequent blank line OR the EOF).
ROW_COUNT=$(awk '
  /^## QA tooling baseline/ {in_section=1; next}
  in_section && /^[0-9]+\. \*\*/ {count++}
  in_section && /^## / && !/^## QA tooling baseline/ {exit}
  END {print count+0}
' "$INDEX")

assert "QA tooling baseline section has $DECLARED_COUNT numbered gate rows (found $ROW_COUNT)" \
  test "$ROW_COUNT" = "$DECLARED_COUNT"

# ── Workflow lockstep: count quality-gate steps in spec-health.yml ──
# Quality-gate steps are those matching the patterns the audit footer
# advertises. We count by scanning step names and including only the
# ones that correspond to the 18 footer gates (excluding Setup steps,
# Self-heal, Trace-map, Summary). Phase 30 added entry #18 (Spec-index
# drift gate) — promoted from the previously-advisory "Regenerate
# spec-index.md (drift check)" step to strict; single workflow step
# (the regen IS the gate, no separate validator), per the H1
# workflow-step parity lesson.
WORKFLOW_GATES=$(grep -E '^      - name: ' "$WORKFLOW" | awk -F': ' '
  /Spec cross-link gate/                      {n++}
  /Spec folder-reference gate/                {n++}
  /Spec tree health gate/                     {n++}
  /Spec lockstep gate/                        {n++}
  /AI-implementability audit v2 gate/         {n++}
  /Audit CLI threshold contract self-test/    {n++}
  /Audit --explain contract self-test/        {n++}
  /Audit determinism \/ JSON-stability/       {n++}
  /Mermaid diagram syntax gate/               {n++}
  /Self-test README inventory parity/         {n++}
  /Self-test QA baseline footer/              {n++}
  /Memo retrospective headings/               {n++}
  /Self-test §27 inventory parity triangle/   {n++}
  /Self-test WEIGHTS dimension-table parity/  {n++}
  /§99 Summary freshness gate/                {n++}
  /§99 Stamp-bump gate/                       {n++}
  /Runtime archive-exclusion gate/            {n++}
  /Spec-index drift gate/                     {n++}
  /Version-field parity gate/                 {n++}
  /Spec truncation gate/                      {n++}
  /Forbidden strings gate/                    {n++}
  END {print n+0}
' )

assert "spec-health.yml has $DECLARED_COUNT quality-gate steps matching footer enumeration (found $WORKFLOW_GATES)" \
  test "$WORKFLOW_GATES" = "$DECLARED_COUNT"

# ── Onboarding link to the Phase 98 README is present ───────────
assert "QA tooling baseline links to linter-scripts/test/README.md (Phase 98)" \
  grep -qE 'linter-scripts/test/README\.md' "$INDEX"

# ── EXECUTIVE-SUMMARY.md cross-references the same gate count ──
assert "EXECUTIVE-SUMMARY.md references the $DECLARED_COUNT-gate baseline" \
  grep -qE "$DECLARED_COUNT strict CI gates" "$EXEC_SUMMARY"

# ── Side-effect-free: no spec/ files written ─────────────────────
# (This test only re-runs the audit, which writes to .lovable/memory/.
# Asserting `git diff --quiet -- spec/` would require git access; instead
# we rely on Phase 95's determinism test as the byte-identity guarantee.)

# ── Summary ──────────────────────────────────────────────────────
echo "======================================="
echo "Script RUBRIC_VERSION : $RUBRIC_FROM_SCRIPT"
echo "00-index.md rubric    : $RUBRIC_FROM_INDEX"
echo "EXEC-SUMMARY rubric   : $RUBRIC_FROM_EXEC"
echo "Declared gate count   : $DECLARED_COUNT"
echo "Footer rows           : $ROW_COUNT"
echo "Workflow gates        : $WORKFLOW_GATES"
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
echo "✅ QA tooling baseline footer contract intact (AC-31-28)."

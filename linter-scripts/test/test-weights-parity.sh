#!/usr/bin/env bash
# linter-scripts/test/test-weights-parity.sh
#
# Phase 113 — WEIGHTS dimension-table parity (3 sites).
#
# Locks: AC-31-31 registry row #4 (Phase 113, generalises AC-31-02).
# The 7-dimension scoring weights are restated verbatim across:
#   1. linter-scripts/audit-spec-vs-code-v2.py        (WEIGHTS dict — source of truth)
#   2. linter-scripts/generate-gate-report.py         (WEIGHTS dict — duplicated for offline analysis)
#   3. spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (## Weights markdown table)
#
# Without this self-test, a contributor adjusting one site without the
# other two would silently produce divergent scores: the production audit
# would compute one weighted-overall, the gate report would attribute
# capping decisions using a different denominator, and reviewers reading
# §31 would believe a third interpretation. AC-31-02 already mandates
# `implementability == 35 AND total == 100` as a runtime assertion in the
# audit script, but it does NOT mandate parity with `generate-gate-report.py`
# or with §31's documented table — exactly the AC-31-31 trigger condition
# (3+ files restating the same enumeration → parity test required).
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-02, AC-31-31)
# Memo: .lovable/memory/audit/v2-deterministic/phase-113-weights-parity-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/linter-scripts/audit-spec-vs-code-v2.py"
GATE_REPORT="$REPO_ROOT/linter-scripts/generate-gate-report.py"
SPEC_31="$REPO_ROOT/spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md"

[ -f "$AUDIT_SCRIPT" ] || { echo "❌ audit script not found: $AUDIT_SCRIPT"; exit 2; }
[ -f "$GATE_REPORT" ]  || { echo "❌ gate report not found: $GATE_REPORT"; exit 2; }
[ -f "$SPEC_31" ]      || { echo "❌ §31 spec not found: $SPEC_31"; exit 2; }

cd "$REPO_ROOT"
PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then echo "✅ $label"; PASS=$((PASS+1))
  else          echo "❌ $label"; FAIL=$((FAIL+1)); fi
}

# ── Extractor: pull `key:int` pairs from a Python WEIGHTS dict ───
# Both audit-spec-vs-code-v2.py and generate-gate-report.py declare:
#   WEIGHTS = {
#       "implementability": 35,
#       ...
#   }
# The extractor walks from the WEIGHTS line until the closing brace and
# captures `"<key>": <int>` pairs. We intentionally tolerate one-line
# vs multi-line dict layouts (gate-report uses one-line; audit uses
# multi-line) by stripping all whitespace before regex matching.
extract_python_weights() {
  local file="$1"
  python3 - "$file" <<'PY'
import re, sys, json
src = open(sys.argv[1]).read()
# Find the FIRST top-level WEIGHTS = { ... } block.
m = re.search(r'^WEIGHTS\s*=\s*\{([^}]*)\}', src, re.M | re.S)
if not m:
    print("ERROR: no WEIGHTS dict found", file=sys.stderr); sys.exit(2)
body = m.group(1)
pairs = re.findall(r'"([a-z]+)"\s*:\s*(\d+)', body)
out = {k: int(v) for k, v in pairs}
print(json.dumps(out, sort_keys=True))
PY
}

# ── Extractor: pull rows from §31 ## Weights markdown table ──────
# Table format:
#   | Dimension | Weight |
#   |-----------|-------:|
#   | Implementability | 35% |
#   ...
extract_spec_weights() {
  python3 - "$SPEC_31" <<'PY'
import re, sys, json
src = open(sys.argv[1]).read()
# Locate the "## Weights" heading and its immediately following table.
m = re.search(r'^##\s+Weights\s*\n(?:.*?\n)*?\|\s*Dimension\s*\|\s*Weight\s*\|\s*\n\|[-:|\s]+\|\s*\n((?:\|.*\|\s*\n)+)',
              src, re.M)
if not m:
    print("ERROR: §31 ## Weights table not found", file=sys.stderr); sys.exit(2)
out = {}
for row in m.group(1).strip().splitlines():
    parts = [c.strip() for c in row.strip().strip('|').split('|')]
    if len(parts) != 2: continue
    name, weight = parts
    name = name.lower()
    weight = int(weight.rstrip('%').strip())
    out[name] = weight
print(json.dumps(out, sort_keys=True))
PY
}

W_AUDIT=$(extract_python_weights "$AUDIT_SCRIPT")
W_GATE=$(extract_python_weights "$GATE_REPORT")
W_SPEC=$(extract_spec_weights)

# ── Existence + non-emptiness ────────────────────────────────────
assert "audit-spec-vs-code-v2.py exposes a non-empty WEIGHTS dict" \
  test "$(echo "$W_AUDIT" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')" -gt 0

assert "generate-gate-report.py exposes a non-empty WEIGHTS dict" \
  test "$(echo "$W_GATE" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')" -gt 0

assert "§31 ## Weights table parses to a non-empty mapping" \
  test "$(echo "$W_SPEC" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')" -gt 0

# ── Pairwise set + value equality ────────────────────────────────
assert "audit-script WEIGHTS == gate-report WEIGHTS (same keys, same values)" \
  test "$W_AUDIT" = "$W_GATE"
if [ "$W_AUDIT" != "$W_GATE" ]; then
  echo "    audit:       $W_AUDIT"
  echo "    gate-report: $W_GATE"
fi

assert "audit-script WEIGHTS == §31 ## Weights table (same keys, same values)" \
  test "$W_AUDIT" = "$W_SPEC"
if [ "$W_AUDIT" != "$W_SPEC" ]; then
  echo "    audit: $W_AUDIT"
  echo "    spec:  $W_SPEC"
fi

# ── AC-31-02 invariants (defence-in-depth — also asserted at script load) ──
IMPL_AUDIT=$(echo "$W_AUDIT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("implementability",0))')
TOTAL_AUDIT=$(echo "$W_AUDIT" | python3 -c 'import json,sys; print(sum(json.load(sys.stdin).values()))')

assert "implementability weight == 35 (AC-31-02 invariant)" \
  test "$IMPL_AUDIT" = "35"

assert "weights sum to 100 (AC-31-02 invariant)" \
  test "$TOTAL_AUDIT" = "100"

# ── Dimension count: exactly 7 (AC-31-31 row #4 trigger constraint) ──
DIM_COUNT=$(echo "$W_AUDIT" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')

assert "exactly 7 dimensions (matches §00-overview '7 dimensions' description)" \
  test "$DIM_COUNT" = "7"

# ── Summary ──────────────────────────────────────────────────────
echo "======================================="
echo "audit-script:    $W_AUDIT"
echo "gate-report:     $W_GATE"
echo "§31 spec table:  $W_SPEC"
echo "implementability: $IMPL_AUDIT  |  total: $TOTAL_AUDIT  |  dimensions: $DIM_COUNT"
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
echo "✅ WEIGHTS parity intact across audit-script ↔ gate-report ↔ §31 (AC-31-31 row #4)."

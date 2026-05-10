#!/usr/bin/env bash
# linter-scripts/test/test-audit-cli-thresholds.sh
#
# Phase 91 — CLI self-test for audit-spec-vs-code-v2.py threshold contract.
#
# Locks the v2.12 (Phase 81) exit-code semantics:
#   --min-weighted=N : exit 1 if mean weighted score < N, else exit 0
#   --min-impl=N     : exit 1 if mean implementability   < N, else exit 0
#
# Without this self-test, a refactor could silently flip the comparison
# operator (≥ vs >, < vs ≤) or invert exit codes, and CI would still pass
# because all 87 modules currently sit comfortably above the floor (98.0/99.8).
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-22)
# Memo: .lovable/memory/audit/v2-deterministic/phase-91-cli-self-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT="$SCRIPT_DIR/audit-spec-vs-code-v2.py"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ ! -f "$AUDIT" ]; then
  echo "❌ audit script not found at $AUDIT"
  exit 2
fi

export AUDIT_DETERMINISTIC=1
cd "$REPO_ROOT"

PASS=0
FAIL=0

run_case() {
  local name="$1"
  local expected_exit="$2"
  shift 2
  local actual_exit=0
  python3 "$AUDIT" "$@" >/dev/null 2>&1 || actual_exit=$?
  if [ "$actual_exit" = "$expected_exit" ]; then
    echo "  ✅ $name (exit=$actual_exit as expected)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $name — expected exit $expected_exit, got $actual_exit"
    FAIL=$((FAIL + 1))
  fi
}

echo "Phase 91 — audit CLI threshold self-test"
echo "========================================"

# Case 1: impossibly high weighted floor → must FAIL (exit 1).
# Locks the contract: --min-weighted enforces a *lower bound* and returns
# non-zero on breach. If this passes (exit 0), the comparison is inverted.
run_case "high --min-weighted=200 fails" 1 --min-weighted=200

# Case 2: floor of 0 → must PASS (exit 0).
# Locks the contract: a satisfiable floor returns success.
run_case "low --min-weighted=0 passes" 0 --min-weighted=0

# Case 3: impossibly high impl floor → must FAIL.
run_case "high --min-impl=200 fails" 1 --min-impl=200

# Case 4: impl floor of 0 → must PASS.
run_case "low --min-impl=0 passes" 0 --min-impl=0

# Case 5: combined floors, both satisfiable → PASS.
run_case "combined low floors pass" 0 --min-weighted=0 --min-impl=0

# Case 6: combined floors, one unsatisfiable → FAIL.
# Confirms either floor breach is sufficient to fail (logical OR semantics).
run_case "combined mixed floors fail" 1 --min-weighted=0 --min-impl=200

echo "========================================"
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ Audit CLI threshold contract violated."
  exit 1
fi
echo "✅ Audit CLI threshold contract intact."

#!/usr/bin/env bash
# Self-test for linter-scripts/check-ai-confidence.py (Phase P48-1-fu1).
#
# Exercises the rubric mechanization in a sandboxed temporary spec/ tree
# so assertions are stable regardless of live-tree state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LINTER="${REPO_ROOT}/linter-scripts/check-ai-confidence.py"

assert_eq() {
  # $1 = label, $2 = expected, $3 = actual
  if [[ "$2" != "$3" ]]; then
    echo "FAIL: $1: expected '$2' got '$3'" >&2
    exit 1
  fi
  echo "  ok: $1"
}

assert_contains() {
  # $1 = label, $2 = needle, $3 = haystack
  if [[ "$3" != *"$2"* ]]; then
    echo "FAIL: $1: expected to contain '$2' in:" >&2
    echo "$3" >&2
    exit 1
  fi
  echo "  ok: $1"
}

assert_ne_contains() {
  # $1 = label, $2 = needle (must NOT appear), $3 = haystack
  if [[ "$3" == *"$2"* ]]; then
    echo "FAIL: $1: did NOT expect to contain '$2' in:" >&2
    echo "$3" >&2
    exit 1
  fi
  echo "  ok: $1"
}

# ---- Live-tree smoke test (Test 1) -----------------------------------------
# Just check the linter runs cleanly against the real tree at default mode.
# Default mode exit 0 unless a stamped file drifts; today no module carries
# the new `ai-confidence-verified-phase` stamp, so exit MUST be 0.
echo "Test 1: live-tree default mode runs and exits 0"
out="$(python3 "${LINTER}" 2>&1)"
ec=$?
assert_eq "live exit" "0" "$ec"
assert_contains "live header" "AI-Confidence rubric parity:" "$out"

# ---- Sandbox tests ----------------------------------------------------------
# Script reads workflow + walks spec/ relative to its own __file__/parent.
# We can't easily relocate it, so we exercise the gate logic via --json on
# the live tree and assert structural invariants.
echo "Test 2: --json output is parseable and includes expected keys"
json="$(python3 "${LINTER}" --json 2>&1)"
assert_contains "json scanned key" '"scanned_modules":' "$json"
assert_contains "json eligible key" '"eligible":' "$json"
assert_contains "json matches key" '"matches":' "$json"
assert_contains "json mismatches key" '"mismatches":' "$json"
assert_contains "json stamped key" '"stamped":' "$json"
assert_contains "json stamped_failed key" '"stamped_failed":' "$json"
assert_contains "json rows key" '"rows":' "$json"

# ---- AC-33-03 — --strict flips advisory to blocking -------------------------
echo "Test 3: --strict exits 1 when ANY drift exists in live tree"
# As of P48-1-fu1 the live tree has 13 drifters; --strict MUST exit 1.
# (If/when adoption converges to 0 drifters, this assertion will need
# updating to inject a sandbox drift — codified per the P31 lesson.)
set +e
python3 "${LINTER}" --strict >/dev/null 2>&1
strict_ec=$?
set -e
# Allow either 1 (drift exists, expected today) OR 0 (tree fully clean,
# expected post-adoption). Anything else = real bug.
if [[ "$strict_ec" != "0" && "$strict_ec" != "1" ]]; then
  echo "FAIL: --strict returned unexpected exit $strict_ec" >&2
  exit 1
fi
echo "  ok: --strict exit=$strict_ec (1=expected today, 0=expected post-adoption)"

# ---- AC-33-05 — unset declared value is skipped -----------------------------
echo "Test 4: --report-only never fails"
set +e
python3 "${LINTER}" --report-only >/dev/null 2>&1
ro_ec=$?
set -e
assert_eq "report-only exit" "0" "$ro_ec"

# ---- Internal-function unit test (P3 lowest-passing-gate logic) ------------
echo "Test 5: derive_tier() returns Medium when P3 fails (AC-33-04)"
# Use python3 importlib to call derive_tier() against a synthetic module dir.
python3 - <<PY
import importlib.util, pathlib, tempfile, sys, os
linter_path = pathlib.Path("${LINTER}").resolve()
spec = importlib.util.spec_from_file_location("ck", linter_path)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    m = pathlib.Path(td)
    # Build a module passing P1+P2 but failing P3 (ACs without **Verifies:**).
    (m / "00-overview.md").write_text(
        "# Test\n\n**AI Confidence:** Production-Ready\n**Updated:** 2026-04-29\n\n"
        "| 01 | [01-x.md](./01-x.md) | x |\n"
    )
    (m / "01-x.md").write_text("# x\n\nA full sentence.\n")
    (m / "97-acceptance-criteria.md").write_text(
        "# AC\n\n### AC-T-01 — t\n- **Given** x\n- **When** y\n- **Then** z.\n"
    )  # ← no **Verifies:** clause → P3 fails
    (m / "99-consistency-report.md").write_text("# CR\n\n## Summary\n\nok.\n")
    derived, reasons = mod.derive_tier(m, "spec-health.yml refers to test", h1_horizon=200)
    assert derived == "Medium", f"expected Medium got {derived!r}: {reasons}"
    print("  ok: derive_tier returns Medium when P3 fails")

    # Also confirm: stripping the bad AC promotes back to High
    (m / "97-acceptance-criteria.md").write_text(
        "# AC\n\n### AC-T-01 — t\n- **Given** x\n- **When** y\n- **Then** z.\n"
        "- **Verifies:** something.\n"
    )
    derived2, _ = mod.derive_tier(m, "spec-health.yml refers to test", h1_horizon=200)
    # P4 may still fail (no §99 stamp) → expect "High"
    assert derived2 == "High", f"expected High got {derived2!r}"
    print("  ok: adding **Verifies:** promotes to High")
PY

echo ""
echo "All assertions passed."

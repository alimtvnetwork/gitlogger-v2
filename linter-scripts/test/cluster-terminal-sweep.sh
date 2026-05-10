#!/usr/bin/env bash
# linter-scripts/test/cluster-terminal-sweep.sh
#
# Phase P40 — Cluster-terminal sweep runner.
#
# Mechanizes the P34/P38 cluster-terminal cadence rule (codified in mem://index.md
# Core P34 lesson #2 + P38 refinement): at the END of any cluster of phases
# (advisory→strict landings, batch sweeps, refactors, etc.), run all critical
# CI gates as the terminal step BEFORE declaring the cluster closed. Both P34
# and P38 caught silent regressions (stale cross-link waivers; stale trace-map
# baseline) that strict CI would have flagged only at next PR — proving the
# cadence catches real failures.
#
# Why a script and not a memorized procedure: the procedure depends on AI/human
# discipline at end-of-cluster. A script removes that dependency — `bash
# linter-scripts/test/cluster-terminal-sweep.sh` is one command. It also gives
# new contributors a single "run this before claiming done" entry point.
#
# Naming: NO `test-` prefix on purpose. This file is a runner, not a self-test
# (it composes existing tests rather than asserting new behaviour). The
# `test/README.md` inventory parity gate (Phase 102, AC-31-27) scopes to
# `test-*.sh` glob, so this file is intentionally exempt. The
# `test-overview-inventory-parity.sh` gate (Phase 112) scopes to
# `linter-scripts/` top level only, so files under `linter-scripts/test/` are
# also exempt from §27 §00 inventory enumeration.
#
# Exit codes:
#   0 — all gates green
#   1 — one or more gates failed
#
# Spec: not a §27 slot (runner, not validator/generator). Documented inline.
# Memo: mem://index.md Core P40 entry.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0
FAILED_GATES=()

run_gate() {
  local label="$1"; shift
  echo "── ${label} ──"
  if "$@" >/tmp/cts-out.$$ 2>&1; then
    tail -2 /tmp/cts-out.$$
    PASS=$((PASS+1))
    echo "✅ ${label}"
  else
    cat /tmp/cts-out.$$
    FAIL=$((FAIL+1))
    FAILED_GATES+=("${label}")
    echo "❌ ${label}"
  fi
  echo
  rm -f /tmp/cts-out.$$
}

echo "================================================================"
echo "Cluster-terminal sweep — running 9 critical gates"
echo "(P34/P38 cadence rule — see mem://index.md Core P40 entry)"
echo "================================================================"
echo

run_gate "1/9 tree-health (--strict)" \
  node linter-scripts/check-tree-health.cjs --strict

run_gate "2/9 lockstep" \
  node linter-scripts/check-lockstep.cjs

run_gate "3/9 version-parity (--strict)" \
  python3 linter-scripts/check-version-parity.py --strict

run_gate "4/9 cross-links" \
  python3 linter-scripts/check-spec-cross-links.py

run_gate "5/9 folder-refs" \
  python3 linter-scripts/check-spec-folder-refs.py

run_gate "6/9 §99 freshness (--strict-position)" \
  python3 linter-scripts/check-99-summary-freshness.py --strict-position

run_gate "7/9 trace-map regression" \
  python3 linter-scripts/check-trace-map-regression.py

run_gate "8/9 §27 inventory parity" \
  bash linter-scripts/test/test-overview-inventory-parity.sh

run_gate "9/9 README inventory parity" \
  bash linter-scripts/test/test-readme-inventory.sh

echo "================================================================"
echo "Cluster-terminal sweep results: ${PASS} passed, ${FAIL} failed"
echo "================================================================"

if [ "${FAIL}" -eq 0 ]; then
  echo "✅ All 9 critical gates green — cluster safe to close."
  exit 0
fi

echo "❌ Failed gates:"
for g in "${FAILED_GATES[@]}"; do
  echo "   - ${g}"
done
echo
echo "Common remediations (per mem://index.md Core):"
echo "  - trace-map drift: if ac_traced flat AND drift growth = AC growth,"
echo "    rebaseline via 'python3 linter-scripts/check-trace-map-regression.py --update-baseline'"
echo "    (Phase 18 lesson). Otherwise it's a real regression — bind/fix required."
echo "  - cross-links stale: 'python3 linter-scripts/check-spec-cross-links.py --rewrite-allowlist'"
echo "    (P35 fuzzy-match auto-heal)."
echo "  - version-parity mismatch: per-module reverse-drift reconstruction"
echo "    (P23/P24/P25/P26 subcase taxonomy)."
exit 1

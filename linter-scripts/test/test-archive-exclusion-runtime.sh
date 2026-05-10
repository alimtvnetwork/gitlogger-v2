#!/usr/bin/env bash
# linter-scripts/test/test-archive-exclusion-runtime.sh
#
# Phase H7 — runtime archive-exclusion gate.
#
# Codifies the H6 lesson "runtime > source verification": every spec-traversing
# linter MUST exclude `spec/_archive/` at RUNTIME (not just by `grep`-ing the
# source). H3 audited 12 linters by source-reading; H6 elevated 3 critical ones
# (check-99-summary-freshness, audit-spec-vs-code-v2, generate-trace-map) to
# runtime probes via `importlib`-load + enumerator call. H7 turns the runtime
# probe into a standing CI gate so a future contributor cannot silently
# regress the exclusion (e.g. by dropping the `if "_archive" not in p.parts`
# guard during a refactor).
#
# How it works
# ============
# For each spec-traversing linter with a documented enumerator function:
#   1. importlib-load the module (sets AUDIT_DETERMINISTIC=1 to bypass
#      lovable_ai imports in audit-spec-vs-code-v2).
#   2. Call the enumerator on the live tree.
#   3. Assert 0 results contain `_archive` in their path components.
#
# Enumerators probed (Phase H7 baseline, must stay at 3+):
#   - check-99-summary-freshness.py     → find_99_files()
#   - audit-spec-vs-code-v2.py          → ALL_MODULES (module-level constant)
#   - generate-trace-map.py             → collect_ac_ids()
#
# Adding a new spec-traversing linter
# ===================================
# When you add a new linter that walks `spec/`, you MUST also add a runtime
# probe here. The probe is 3 lines: load + call + filter. See the existing
# probes below for the contract.
#
# Spec: spec/27-spec-toolchain/28-check-archive-exclusion-runtime.md (AC-28-01..05)
# Memo: .lovable/memory/audit/v2-deterministic/phase-h6-archive-isolation-audit.md
# Memo: .lovable/memory/audit/v2-deterministic/phase-h7-runtime-probe-gate.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0
assert() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  ✅ $desc"; PASS=$((PASS+1))
    else
        echo "  ❌ $desc"; FAIL=$((FAIL+1))
    fi
}

# ── Run the runtime probe in a single Python session ────────────
PROBE_OUT=$(AUDIT_DETERMINISTIC=1 python3 - <<'PY'
import os, sys, importlib.util
os.environ.setdefault('AUDIT_DETERMINISTIC', '1')

def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

results = {}

# ── Probe 1: check-99-summary-freshness.find_99_files() ──────────
try:
    m = load('freshness', 'linter-scripts/check-99-summary-freshness.py')
    files = list(m.find_99_files())
    leaked = [f for f in files if '_archive' in str(f).split('/')]
    results['freshness'] = (len(files), len(leaked))
except Exception as e:
    results['freshness'] = ('ERR', str(e))

# ── Probe 2: audit-spec-vs-code-v2.ALL_MODULES ──────────────────
try:
    m = load('audit', 'linter-scripts/audit-spec-vs-code-v2.py')
    mods = m.ALL_MODULES
    leaked = [x for x in mods if '_archive' in str(x).split('/')]
    results['audit'] = (len(mods), len(leaked))
except Exception as e:
    results['audit'] = ('ERR', str(e))

# ── Probe 3: generate-trace-map.collect_ac_ids() ────────────────
try:
    m = load('trace', 'linter-scripts/generate-trace-map.py')
    ids = m.collect_ac_ids()
    leaked = [k for k, v in ids.items()
              if any('_archive' in str(p).split('/') for p in v)]
    results['trace'] = (len(ids), len(leaked))
except Exception as e:
    results['trace'] = ('ERR', str(e))

# ── Print machine-parseable lines ────────────────────────────────
for name, (total, leaked) in results.items():
    print(f"{name}|{total}|{leaked}")
PY
)

echo "$PROBE_OUT"
echo

# ── Parse + assert ──────────────────────────────────────────────
get_total()  { echo "$PROBE_OUT" | awk -F'|' -v k="$1" '$1==k{print $2}'; }
get_leaked() { echo "$PROBE_OUT" | awk -F'|' -v k="$1" '$1==k{print $3}'; }

# Probe 1
T1=$(get_total freshness); L1=$(get_leaked freshness)
assert "freshness probe loaded successfully" test "$T1" != "ERR"
assert "freshness scanned ≥ 80 §99 files (sanity)"  test "$T1" -ge 80 2>/dev/null
assert "freshness probe: 0 archive-leaked files (got: $L1)" test "$L1" = "0"

# Probe 2
T2=$(get_total audit); L2=$(get_leaked audit)
assert "audit-v2 probe loaded successfully (deterministic mode)" test "$T2" != "ERR"
assert "audit-v2 enumerated ≥ 80 modules (sanity)" test "$T2" -ge 80 2>/dev/null
assert "audit-v2 probe: 0 archive-leaked modules (got: $L2)" test "$L2" = "0"

# Probe 3
T3=$(get_total trace); L3=$(get_leaked trace)
assert "trace-map probe loaded successfully" test "$T3" != "ERR"
assert "trace-map enumerated ≥ 1000 AC ids (sanity)" test "$T3" -ge 1000 2>/dev/null
assert "trace-map probe: 0 archive-sourced AC ids (got: $L3)" test "$L3" = "0"

# ── Probe count enforcement: at least 3 probes must be active ───
PROBE_COUNT=$(echo "$PROBE_OUT" | grep -cE '^[a-z]+\|' || true)
assert "self-test runs ≥ 3 runtime probes (got $PROBE_COUNT) — codifies H7 floor" \
    test "$PROBE_COUNT" -ge 3

echo
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" = "0" ] || exit 1
echo "✅ All spec-traversing linters runtime-exclude spec/_archive/ (AC-28-01..05)."

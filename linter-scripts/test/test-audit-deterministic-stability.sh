#!/usr/bin/env bash
# linter-scripts/test/test-audit-deterministic-stability.sh
#
# Phase 95 — JSON-stability self-test for audit-spec-vs-code-v2.py
#            (locks the AUDIT_DETERMINISTIC=1 byte-identical guarantee).
#
# Runs the audit script twice in deterministic mode and asserts the
# resulting raw-results.json is BYTE-IDENTICAL across both runs. Without
# this self-test, any of the following regressions would slip through CI:
#
#   - Adding a non-sorted dict / set iteration to the metrics or scorer
#   - Adding a timestamp / wall-clock value to a per-module field
#   - Adding random / hash-seeded sampling to AC parsing
#   - Reordering the `findings` list without sorting
#   - Removing the explicit `sort_keys=DETERMINISTIC` on the JSON write
#   - Reordering the `results` list without sorting by module name
#
# Determinism is the cornerstone of the entire CI quality bar (Phase 81's
# --min-weighted / --min-impl floors only make sense if scores are
# reproducible). The pre-existing audit gate doesn't catch determinism
# bugs because it only runs the script ONCE.
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-26)
# Memo: .lovable/memory/audit/v2-deterministic/phase-95-determinism-stability.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT="$SCRIPT_DIR/audit-spec-vs-code-v2.py"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RAW_JSON="$REPO_ROOT/.lovable/memory/audit/v2-deterministic/raw-results.json"

if [ ! -f "$AUDIT" ]; then
  echo "❌ audit script not found at $AUDIT"
  exit 2
fi

export AUDIT_DETERMINISTIC=1
cd "$REPO_ROOT"

PASS=0
FAIL=0
note_pass() { echo "  ✅ $1"; PASS=$((PASS + 1)); }
note_fail() { echo "  ❌ $1"; FAIL=$((FAIL + 1)); }

echo "Phase 95 — audit determinism / JSON-stability self-test"
echo "======================================================="

TMP_DIR="$(mktemp -d)"
RUN1="$TMP_DIR/run1.json"
RUN2="$TMP_DIR/run2.json"
LOG1="$TMP_DIR/log1"
LOG2="$TMP_DIR/log2"

# ─── Run 1 ──────────────────────────────────────────────────────────
echo "Run 1: AUDIT_DETERMINISTIC=1 python3 audit-spec-vs-code-v2.py"
RUN1_EXIT=0
python3 "$AUDIT" >"$LOG1" 2>&1 || RUN1_EXIT=$?
if [ "$RUN1_EXIT" = "0" ]; then
  note_pass "Run 1 exited 0"
else
  note_fail "Run 1 exited $RUN1_EXIT (expected 0)"
  tail -20 "$LOG1"
  rm -rf "$TMP_DIR"
  exit 1
fi
if [ -f "$RAW_JSON" ]; then
  cp "$RAW_JSON" "$RUN1"
  note_pass "Run 1 wrote raw-results.json"
else
  note_fail "Run 1 did not write raw-results.json"
  rm -rf "$TMP_DIR"
  exit 1
fi

# ─── Run 2 ──────────────────────────────────────────────────────────
echo "Run 2: same invocation"
RUN2_EXIT=0
python3 "$AUDIT" >"$LOG2" 2>&1 || RUN2_EXIT=$?
if [ "$RUN2_EXIT" = "0" ]; then
  note_pass "Run 2 exited 0"
else
  note_fail "Run 2 exited $RUN2_EXIT (expected 0)"
  rm -rf "$TMP_DIR"
  exit 1
fi
cp "$RAW_JSON" "$RUN2"

# ─── Byte-identical assertion (sha256) ─────────────────────────────
HASH1="$(sha256sum < "$RUN1" | awk '{print $1}')"
HASH2="$(sha256sum < "$RUN2" | awk '{print $1}')"
if [ "$HASH1" = "$HASH2" ]; then
  note_pass "raw-results.json sha256 identical across both runs"
  echo "      sha256: $HASH1"
else
  note_fail "raw-results.json DIFFERS between runs"
  echo "      run1 sha256: $HASH1"
  echo "      run2 sha256: $HASH2"
  echo "      first 20 differing lines:"
  # Pure-bash line-diff (no diff binary in sandbox)
  paste "$RUN1" "$RUN2" \
    | awk -F'\t' 'NR<=20000 && $1 != $2 { print "      L"NR":"; print "        run1: "$1; print "        run2: "$2; n++; if (n>=20) exit }'
fi

# ─── Byte-count sanity check (catches truncation regressions) ──────
SIZE1="$(wc -c < "$RUN1")"
SIZE2="$(wc -c < "$RUN2")"
if [ "$SIZE1" = "$SIZE2" ]; then
  note_pass "raw-results.json byte size identical ($SIZE1 bytes)"
else
  note_fail "raw-results.json byte size differs (run1=$SIZE1 run2=$SIZE2)"
fi

# ─── JSON validity & module count consistency ──────────────────────
COUNT1="$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))))" "$RUN1" 2>/dev/null || echo "ERR")"
COUNT2="$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))))" "$RUN2" 2>/dev/null || echo "ERR")"
if [ "$COUNT1" != "ERR" ] && [ "$COUNT1" = "$COUNT2" ] && [ "$COUNT1" -ge 80 ]; then
  note_pass "Both runs contain $COUNT1 valid module entries"
else
  note_fail "Module count mismatch or invalid JSON (run1=$COUNT1 run2=$COUNT2)"
fi

# ─── Sort-order assertion (modules sorted by name) ─────────────────
SORTED1="$(python3 -c "
import json,sys
mods = [r['module'] for r in json.load(open(sys.argv[1]))]
print('OK' if mods == sorted(mods) else 'UNSORTED')
" "$RUN1" 2>/dev/null || echo "ERR")"
if [ "$SORTED1" = "OK" ]; then
  note_pass "Modules sorted by name (deterministic ordering)"
else
  note_fail "Modules NOT sorted by name (DETERMINISTIC mode broken: $SORTED1)"
fi

# ─── P49 / AC-T-13 extension: spec-index + dashboard-data generators ─
# Per Lesson #21 (parity-AC graduation): a determinism contract that cites
# multiple generators MUST be mechanically locked across ALL of them, not
# just the first. AC-T-13 cites three generators; this self-test originally
# covered only the auditor. P49 (P46-followup-3) adds coverage for:
#   - linter-scripts/generate-spec-index.cjs   → spec/spec-index.md
#   - linter-scripts/generate-dashboard-data.cjs → spec/dashboard-data.json
# Both generators are pure single-day deterministic (the only wall-clock
# value is `new Date().toISOString().slice(0,10)` which is stable across
# back-to-back runs), so two-run byte-identity is the right contract.

run_twice_byte_identical() {
  # $1 = label, $2 = node script path, $3 = output file (relative to repo root)
  local label="$1" script="$2" out_rel="$3"
  local out_abs="$REPO_ROOT/$out_rel"
  local backup="$TMP_DIR/${label}.backup"
  local r1="$TMP_DIR/${label}.run1"
  local r2="$TMP_DIR/${label}.run2"

  if [ ! -f "$script" ]; then
    note_fail "$label: generator not found at $script"
    return
  fi

  # Snapshot pre-existing artifact so we can restore it (the working tree
  # MUST be byte-identical before and after this self-test).
  if [ -f "$out_abs" ]; then
    cp "$out_abs" "$backup"
  fi

  echo "Run 1: node $(basename "$script")"
  if ! node "$script" >"$TMP_DIR/${label}.log1" 2>&1; then
    note_fail "$label: Run 1 exited non-zero"
    tail -10 "$TMP_DIR/${label}.log1"
    [ -f "$backup" ] && cp "$backup" "$out_abs"
    return
  fi
  if [ ! -f "$out_abs" ]; then
    note_fail "$label: Run 1 did not write $out_rel"
    return
  fi
  cp "$out_abs" "$r1"
  note_pass "$label: Run 1 wrote $out_rel"

  echo "Run 2: same invocation"
  if ! node "$script" >"$TMP_DIR/${label}.log2" 2>&1; then
    note_fail "$label: Run 2 exited non-zero"
    tail -10 "$TMP_DIR/${label}.log2"
    [ -f "$backup" ] && cp "$backup" "$out_abs"
    return
  fi
  cp "$out_abs" "$r2"

  local h1 h2
  h1="$(sha256sum < "$r1" | awk '{print $1}')"
  h2="$(sha256sum < "$r2" | awk '{print $1}')"
  if [ "$h1" = "$h2" ]; then
    note_pass "$label: $out_rel sha256 identical across both runs ($h1)"
  else
    note_fail "$label: $out_rel DIFFERS between runs (run1=$h1 run2=$h2)"
  fi

  local s1 s2
  s1="$(wc -c < "$r1")"
  s2="$(wc -c < "$r2")"
  if [ "$s1" = "$s2" ]; then
    note_pass "$label: byte size identical ($s1 bytes)"
  else
    note_fail "$label: byte size differs (run1=$s1 run2=$s2)"
  fi

  # Restore pre-existing artifact (working tree contract).
  if [ -f "$backup" ]; then
    cp "$backup" "$out_abs"
  fi
}

echo ""
echo "P49 / AC-T-13 — generate-spec-index.cjs determinism"
echo "----------------------------------------------------"
run_twice_byte_identical "spec-index" "$SCRIPT_DIR/generate-spec-index.cjs" "spec/spec-index.md"

echo ""
echo "P49 / AC-T-13 — generate-dashboard-data.cjs determinism"
echo "--------------------------------------------------------"
run_twice_byte_identical "dashboard-data" "$SCRIPT_DIR/generate-dashboard-data.cjs" "spec/dashboard-data.json"

# ─── Cleanup ───────────────────────────────────────────────────────
rm -rf "$TMP_DIR"

echo "======================================================="
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ Determinism contract violated."
  exit 1
fi
echo "✅ Determinism contract intact (auditor + spec-index + dashboard-data byte-identical)."

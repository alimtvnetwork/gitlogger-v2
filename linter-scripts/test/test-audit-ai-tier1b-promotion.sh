#!/usr/bin/env bash
# Self-test for AC-34-18: bounded tier-1B promotion (nested contract files).
#
# Asserts (R2-followup extension — all 6 FITS modules + OVERFLOW + zero-T1B):
#   T1: spec/05 (FITS, 8 nested T1B)  → root_t1=4 · nT1B_first12=8 · total=8
#   T2: spec/02 (OVERFLOW-fallback, 116 nested T1B) → root_t1=4 · nT1B_first12 ≤ 3
#   T3: spec/22 (zero nested T1B) → behavior unchanged · nT1B_total=0
#   T4: spec/06 (FITS, 8 nested T1B)  → root_t1=4 · nT1B_first12=8 · total=8
#   T5: spec/10 (FITS, 4 nested T1B)  → root_t1=4 · nT1B_first12=4 · total=4
#   T6: spec/12 (FITS, 12 nested T1B) → root_t1=4 · nT1B_first12=8 · total=12
#         (only 8 fit in first 12 alongside 4 root-T1 — natural 12-slot ceiling)
#   T7: spec/18 (FITS, 4 nested T1B)  → root_t1=4 · nT1B_first12=4 · total=4
#   T8: spec/26 (FITS, 4 nested T1B)  → root_t1=4 · nT1B_first12=4 · total=4
#
# Codifies the bounded-promotion contract so future walker edits cannot
# silently regress the FITS path (clean lift) or the OVERFLOW path
# (graceful no-mass-promotion fallback).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

PASS=0
FAIL=0

assert() {
  local label="$1"; local expected="$2"; local actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    PASS=$((PASS+1))
    echo "  PASS  $label  (got: $actual)"
  else
    FAIL=$((FAIL+1))
    echo "  FAIL  $label  expected=$expected  got=$actual"
  fi
}

probe() {
  local slug="$1"
  python3 - "$ROOT" "$slug" <<'PY'
import sys, importlib.util, re
from pathlib import Path
root = Path(sys.argv[1])
slug = sys.argv[2]
spec = importlib.util.spec_from_file_location("aai", str(root/"linter-scripts/audit-ai-implementability.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
text, _t, _u, _tf = m.load_module_bundle(root/"spec"/slug)
headers = [h.strip() for h in re.findall(r"===== FILE: ([^=]+) =====", text)]
T1 = {"00-overview.md","97-acceptance-criteria.md","98-changelog.md","99-consistency-report.md"}
root_t1 = [h for h in headers if h.split("/")[-1] in T1 and h.count("/") == 2]
nested_t1b_first12 = [h for h in headers[:12] if h.split("/")[-1] in T1 and h.count("/") >= 3]
nested_t1b_total = [h for h in headers if h.split("/")[-1] in T1 and h.count("/") >= 3]
print(f"root_t1={len(root_t1)} nT1B_first12={len(nested_t1b_first12)} nT1B_total={len(nested_t1b_total)}")
PY
}

echo "AC-34-18: bounded tier-1B promotion self-test"
echo "---"

echo "T1: spec/05 (FITS path — full clean lift expected)"
out=$(probe "05-split-db-architecture")
echo "  probe → $out"
rt1=$(echo "$out" | sed -n 's/.*root_t1=\([0-9]*\).*/\1/p')
nt1b_top=$(echo "$out" | sed -n 's/.*nT1B_first12=\([0-9]*\).*/\1/p')
nt1b_all=$(echo "$out" | sed -n 's/.*nT1B_total=\([0-9]*\).*/\1/p')
assert "spec/05 root_t1 == 4"          "4" "$rt1"
assert "spec/05 nT1B in first12 == 8"  "8" "$nt1b_top"
assert "spec/05 nT1B total == 8"       "8" "$nt1b_all"

echo "T2: spec/02 (OVERFLOW-fallback — no mass promotion)"
out=$(probe "02-coding-guidelines")
echo "  probe → $out"
rt1=$(echo "$out" | sed -n 's/.*root_t1=\([0-9]*\).*/\1/p')
nt1b_top=$(echo "$out" | sed -n 's/.*nT1B_first12=\([0-9]*\).*/\1/p')
assert "spec/02 root_t1 == 4"            "4" "$rt1"
# Fallback contract: at most 3 nested T1B files may appear in first 12
# (they bubble up only via natural alphabetical order, not by promotion).
if [[ "$nt1b_top" -le 3 ]]; then
  PASS=$((PASS+1)); echo "  PASS  spec/02 nT1B_first12 ≤ 3 (got: $nt1b_top — fallback held)"
else
  FAIL=$((FAIL+1)); echo "  FAIL  spec/02 nT1B_first12 ≤ 3  expected≤3 got=$nt1b_top (mass-promotion regression!)"
fi

echo "T3: spec/22 (no nested T1B — no behavior change)"
out=$(probe "22-git-logs-v2")
echo "  probe → $out"
nt1b_all=$(echo "$out" | sed -n 's/.*nT1B_total=\([0-9]*\).*/\1/p')
assert "spec/22 nT1B total == 0"  "0" "$nt1b_all"

# R2-followup: extend coverage to all 6 FITS modules
fits_test() {
  local label="$1"; local slug="$2"; local exp_total="$3"; local exp_top12="$4"
  echo "$label: spec/$slug (FITS — clean lift expected)"
  local out; out=$(probe "$slug")
  echo "  probe → $out"
  local rt1; rt1=$(echo "$out" | sed -n 's/.*root_t1=\([0-9]*\).*/\1/p')
  local nt1b_top; nt1b_top=$(echo "$out" | sed -n 's/.*nT1B_first12=\([0-9]*\).*/\1/p')
  local nt1b_all; nt1b_all=$(echo "$out" | sed -n 's/.*nT1B_total=\([0-9]*\).*/\1/p')
  assert "spec/$slug root_t1 == 4"                "4"          "$rt1"
  assert "spec/$slug nT1B_first12 == $exp_top12"  "$exp_top12" "$nt1b_top"
  assert "spec/$slug nT1B_total == $exp_total"    "$exp_total" "$nt1b_all"
}

fits_test "T4" "06-seedable-config-architecture" "8"  "8"
fits_test "T5" "10-research"                     "4"  "4"
fits_test "T6" "12-cicd-pipeline-workflows"      "12" "8"
fits_test "T7" "18-wp-plugin-how-to"             "4"  "4"
fits_test "T8" "26-gitlogs-diagrams"             "4"  "4"

echo "---"
echo "AC-34-18 self-test: $PASS pass, $FAIL fail"
[[ "$FAIL" -eq 0 ]] || exit 1

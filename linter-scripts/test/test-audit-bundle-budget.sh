#!/usr/bin/env bash
# test-audit-bundle-budget.sh — self-test for linter-scripts/audit-bundle-budget.py
# Phase 153 Task A24-fu32

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$REPO_ROOT/linter-scripts/audit-bundle-budget.py"
PASS=0
FAIL=0

assert() {
  local label="$1"; local expected="$2"; local actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "  PASS  $label"
    PASS=$((PASS+1))
  else
    echo "  FAIL  $label  (expected=$expected actual=$actual)"
    FAIL=$((FAIL+1))
  fi
}

echo "T1: script exists + executable"
assert "exists" "yes" "$([ -f "$SCRIPT" ] && echo yes || echo no)"
assert "executable" "yes" "$([ -x "$SCRIPT" ] && echo yes || echo no)"

echo "T2: --help exits 0"
"$SCRIPT" --help > /dev/null
assert "help-exit" "0" "$?"

echo "T3: default mode exits 0 (advisory)"
"$SCRIPT" > /dev/null
assert "default-exit" "0" "$?"

echo "T4: --json emits valid JSON with required keys"
JSON="$("$SCRIPT" --json)"
KEYS="$(echo "$JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(','.join(sorted(d.keys())))")"
assert "json-keys" "cap,counts,modules" "$KEYS"

echo "T5: cap reads from auditor source (≥90KB, ≤200KB)"
CAP="$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['cap'])")"
assert "cap-in-range" "yes" "$([ "$CAP" -ge 90000 ] && [ "$CAP" -le 200000 ] && echo yes || echo no)"

echo "T6: every module has all 9 stat fields"
BAD="$(echo "$JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
need = {'module','s00','s97','s98','s99','tier1','siblings','sibling_count','headroom','deficit','status'}
bad = [m['module'] for m in d['modules'] if not need.issubset(m.keys())]
print(len(bad))
")"
assert "fields-complete" "0" "$BAD"

echo "T7: every status is one of {OVER,AT_CEILING,CLEAR}"
BAD="$(echo "$JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ok = {'OVER','AT_CEILING','CLEAR'}
bad = [m['module'] for m in d['modules'] if m['status'] not in ok]
print(len(bad))
")"
assert "status-vocab" "0" "$BAD"

echo "T8: OVER classification matches tier1>cap"
BAD="$(echo "$JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
cap = d['cap']
bad = [m['module'] for m in d['modules']
       if (m['status']=='OVER') != (m['tier1']>cap)]
print(len(bad))
")"
assert "over-rule" "0" "$BAD"

echo "T9: --strict exits 1 when OVER>0, 0 when OVER=0"
OVER="$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['counts']['OVER'])")"
set +e
"$SCRIPT" --strict > /dev/null 2>&1
RC=$?
set -e
if [ "$OVER" -gt 0 ]; then
  assert "strict-fails" "1" "$RC"
else
  assert "strict-passes" "0" "$RC"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]

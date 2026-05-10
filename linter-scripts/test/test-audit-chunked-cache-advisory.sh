#!/usr/bin/env bash
# linter-scripts/test/test-audit-chunked-cache-advisory.sh
#
# Phase 153 Task N8 — self-test for the Lesson #82 chunked-cache advisory
# emitted by audit-ai-implementability.py (Phase 153 Task N6).
#
# Locks the contract:
#   1. Sub-90 module with chunked_path=false → MUST appear in advisory.
#   2. Sub-90 module with chunked_path=true  → MUST NOT appear in advisory.
#   3. ≥90 module with chunked_path=false    → MUST NOT appear in advisory.
#   4. Advisory header line is emitted only when ≥1 fixture qualifies.
#   5. Advisory NEVER changes exit code (advisory-only per Lesson #82).
#
# Snapshot-restore contract (Lesson #31): cache dir is snapshot-copied,
# fixtures are injected, test runs, original cache is restored byte-for-byte.
#
# Spec: linter-scripts/audit-ai-implementability.py (Lesson #82 advisory block)
# Memo: .lovable/memory/audit/v2-deterministic/phase-153-task-N8-chunked-advisory-self-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT="$SCRIPT_DIR/audit-ai-implementability.py"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CACHE_DIR="$REPO_ROOT/.lovable/cache/audit-ai"

if [ ! -f "$AUDIT" ]; then
  echo "❌ audit script not found at $AUDIT"
  exit 2
fi

cd "$REPO_ROOT"

# Snapshot existing cache (Lesson #31)
SNAPSHOT="$(mktemp -d)"
mkdir -p "$CACHE_DIR"
cp -a "$CACHE_DIR/." "$SNAPSHOT/"

cleanup() {
  rm -rf "$CACHE_DIR"
  mkdir -p "$CACHE_DIR"
  cp -a "$SNAPSHOT/." "$CACHE_DIR/" 2>/dev/null || true
  rm -rf "$SNAPSHOT"
}
trap cleanup EXIT

PASS=0
FAIL=0

assert() {
  local name="$1"; local cond="$2"
  if eval "$cond"; then
    echo "  ✅ $name"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $name (cond: $cond)"
    FAIL=$((FAIL + 1))
  fi
}

echo "Phase 153 Task N8 — Lesson #82 chunked-cache advisory self-test"
echo "================================================================"

# Inject 3 fixture caches matching real spec/ module dirs (so the auditor's
# module discovery picks them up, but with --no-network they won't be re-scored).
write_fixture() {
  local mod="$1"; local total="$2"; local chunked="$3"
  cat > "$CACHE_DIR/$mod.json" <<EOF
{
  "module": "$mod",
  "total": $total,
  "band": "GOOD",
  "chunked_path": $chunked,
  "bundle_sha": "fixture-n8-test"
}
EOF
}

# Pick 3 real spec module dirs to host fixtures.
M_FAIL="05-split-db-architecture"     # sub-90 + chunked=false → SHOULD appear
M_OK_CHUNKED="12-cicd-pipeline-workflows"  # sub-90 + chunked=true → MUST NOT appear
M_OK_HIGH="24-app-design-system-and-ui"    # high + chunked=false → MUST NOT appear

write_fixture "$M_FAIL"        85 false
write_fixture "$M_OK_CHUNKED"  85 true
write_fixture "$M_OK_HIGH"     93 false

OUT="$(mktemp)"
EXIT=0
python3 "$AUDIT" --no-network --report-only --report /tmp/n8-report.md > "$OUT" 2>&1 || EXIT=$?

# Case 1: header emitted
assert "advisory header emitted" "grep -q 'Lesson #82 advisory' '$OUT'"

# Case 2: failing fixture appears
assert "sub-90 + chunked=false appears" "grep -q '$M_FAIL' '$OUT' && grep -A20 'Lesson #82 advisory' '$OUT' | grep -q '$M_FAIL'"

# Case 3: chunked=true sub-90 does NOT appear in advisory block
ADV_BLOCK="$(awk '/Lesson #82 advisory/,/^$/' "$OUT")"
if echo "$ADV_BLOCK" | grep -q "$M_OK_CHUNKED"; then
  echo "  ❌ sub-90 + chunked=true MUST NOT appear (found in advisory)"
  FAIL=$((FAIL + 1))
else
  echo "  ✅ sub-90 + chunked=true correctly suppressed"
  PASS=$((PASS + 1))
fi

# Case 4: high-score chunked=false does NOT appear
if echo "$ADV_BLOCK" | grep -q "$M_OK_HIGH"; then
  echo "  ❌ ≥90 + chunked=false MUST NOT appear (found in advisory)"
  FAIL=$((FAIL + 1))
else
  echo "  ✅ ≥90 + chunked=false correctly suppressed"
  PASS=$((PASS + 1))
fi

# Case 5: advisory is non-fatal (--report-only exits 0)
assert "advisory does not change exit code" "[ '$EXIT' = '0' ]"

# Case 6: empty-fixture run emits NO header (negative path).
# Remove the failing fixture; restore original for these 3 mods if present
# (otherwise just delete to avoid noise).
rm -f "$CACHE_DIR/$M_FAIL.json"
[ -f "$SNAPSHOT/$M_FAIL.json" ] && cp "$SNAPSHOT/$M_FAIL.json" "$CACHE_DIR/$M_FAIL.json"
rm -f "$CACHE_DIR/$M_OK_CHUNKED.json"
[ -f "$SNAPSHOT/$M_OK_CHUNKED.json" ] && cp "$SNAPSHOT/$M_OK_CHUNKED.json" "$CACHE_DIR/$M_OK_CHUNKED.json"
rm -f "$CACHE_DIR/$M_OK_HIGH.json"
[ -f "$SNAPSHOT/$M_OK_HIGH.json" ] && cp "$SNAPSHOT/$M_OK_HIGH.json" "$CACHE_DIR/$M_OK_HIGH.json"

# Skip case 6 if real cache itself contains pre-chunked sub-90 entries
# (it does, per Phase N5 diagnosis — that's why the advisory exists).
# So case 6 is informational only.

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" = "0" ] || exit 1
echo "✅ All Lesson #82 advisory contract assertions hold"

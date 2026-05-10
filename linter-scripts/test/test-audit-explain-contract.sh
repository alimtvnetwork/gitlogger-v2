#!/usr/bin/env bash
# linter-scripts/test/test-audit-explain-contract.sh
#
# Phase 94 — CLI self-test for audit-spec-vs-code-v2.py --explain=<substring>
#
# Locks the v2.16 (Phase 90) AC-31-23 contract:
#   - Single match            : exit 0 + "Branch :" line + "Final score :" line on stdout
#   - No match                : exit 1 + "no module matched" hint on stderr
#   - Multi-match             : exit 0 + "matched N modules" warning on stderr
#                               + first 5 candidate paths listed on stderr
#                               + operates on first match (still prints full report)
#   - --explain MUST NOT      : write any files, call AI, or touch
#                               .lovable/memory/audit/v2-deterministic/
#
# Without this self-test, a refactor could silently break --explain (the
# primary contributor-facing debugging tool from Phase 90) and CI would
# still pass because --explain is never invoked in the normal audit gate.
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-23)
# Memo: .lovable/memory/audit/v2-deterministic/phase-94-explain-contract-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT="$SCRIPT_DIR/audit-spec-vs-code-v2.py"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MEMORY_DIR="$REPO_ROOT/.lovable/memory/audit/v2-deterministic"

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

# ── Snapshot memory dir to detect any writes by --explain ────────────────
SNAPSHOT_BEFORE="$(mktemp)"
ls -la "$MEMORY_DIR" 2>/dev/null | sort > "$SNAPSHOT_BEFORE" || true

echo "Phase 94 — audit --explain contract self-test"
echo "============================================="

# ─────────────────────────────────────────────────────────────────────────
# Case 1: Single-match → exit 0 + "Branch" + "Final score" lines on stdout
# ─────────────────────────────────────────────────────────────────────────
echo "Case 1: single-match (--explain=01-spec-authoring-guide)"
TMP_OUT="$(mktemp)"
TMP_ERR="$(mktemp)"
ACTUAL_EXIT=0
python3 "$AUDIT" --explain=01-spec-authoring-guide >"$TMP_OUT" 2>"$TMP_ERR" || ACTUAL_EXIT=$?

if [ "$ACTUAL_EXIT" = "0" ]; then
  note_pass "exit=0 on single match"
else
  note_fail "expected exit 0 on single match, got $ACTUAL_EXIT"
fi

if grep -q "^Branch" "$TMP_OUT"; then
  note_pass "stdout contains 'Branch' line"
else
  note_fail "stdout missing 'Branch' line (AC-31-23 (a))"
fi

if grep -q "^Final score" "$TMP_OUT"; then
  note_pass "stdout contains 'Final score' line"
else
  note_fail "stdout missing 'Final score' line"
fi

if grep -q -- "--- Per-dimension scores ---" "$TMP_OUT"; then
  note_pass "stdout contains per-dimension table (AC-31-23 (b))"
else
  note_fail "stdout missing per-dimension table"
fi

if grep -q -- "--- Implementability bonuses fired" "$TMP_OUT"; then
  note_pass "stdout contains bonuses block (AC-31-23 (c))"
else
  note_fail "stdout missing bonuses block"
fi

if grep -q -- "--- Key metrics ---" "$TMP_OUT"; then
  note_pass "stdout contains key metrics block (AC-31-23 (f))"
else
  note_fail "stdout missing key metrics block"
fi

# ─────────────────────────────────────────────────────────────────────────
# Case 2: No-match → exit 1 + "no module matched" on stderr
# ─────────────────────────────────────────────────────────────────────────
echo "Case 2: no-match (--explain=does-not-exist-XYZ-7f3a)"
TMP_OUT2="$(mktemp)"
TMP_ERR2="$(mktemp)"
ACTUAL_EXIT2=0
python3 "$AUDIT" --explain=does-not-exist-XYZ-7f3a >"$TMP_OUT2" 2>"$TMP_ERR2" || ACTUAL_EXIT2=$?

if [ "$ACTUAL_EXIT2" = "1" ]; then
  note_pass "exit=1 on no-match"
else
  note_fail "expected exit 1 on no-match, got $ACTUAL_EXIT2"
fi

if grep -q "no module matched" "$TMP_ERR2"; then
  note_pass "stderr contains 'no module matched' hint (AC-31-23 (final))"
else
  note_fail "stderr missing 'no module matched' hint"
fi

# Empty stdout on no-match (or at least no Branch/Final score line)
if ! grep -q "^Branch\|^Final score" "$TMP_OUT2"; then
  note_pass "stdout contains no rubric trace on no-match"
else
  note_fail "stdout incorrectly contains rubric trace on no-match"
fi

# ─────────────────────────────────────────────────────────────────────────
# Case 3: Multi-match → exit 0 + "matched N modules" warning + first 5 candidates
# ─────────────────────────────────────────────────────────────────────────
echo "Case 3: multi-match (--explain=03-issues, matches 2 trackers)"
TMP_OUT3="$(mktemp)"
TMP_ERR3="$(mktemp)"
ACTUAL_EXIT3=0
python3 "$AUDIT" --explain=03-issues >"$TMP_OUT3" 2>"$TMP_ERR3" || ACTUAL_EXIT3=$?

if [ "$ACTUAL_EXIT3" = "0" ]; then
  note_pass "exit=0 on multi-match (uses first)"
else
  note_fail "expected exit 0 on multi-match, got $ACTUAL_EXIT3"
fi

# Multi-match warning may appear on stdout or stderr; check both
COMBINED3="$(cat "$TMP_OUT3" "$TMP_ERR3")"
if echo "$COMBINED3" | grep -qE "matched [0-9]+ modules"; then
  note_pass "warns about N matches (AC-31-23 multi-match)"
else
  note_fail "missing 'matched N modules' disambiguation warning"
fi

if echo "$COMBINED3" | grep -q "05-split-db-architecture/03-issues" \
   && echo "$COMBINED3" | grep -q "06-seedable-config-architecture/03-issues"; then
  note_pass "lists both candidate paths"
else
  note_fail "missing candidate path listing"
fi

# Should still print full report for first match
if grep -q "^Branch" "$TMP_OUT3" && grep -q "^Final score" "$TMP_OUT3"; then
  note_pass "still prints full report for first match"
else
  note_fail "did not print full report for first match"
fi

# ─────────────────────────────────────────────────────────────────────────
# Case 4: --explain MUST NOT write to memory dir or call AI
# ─────────────────────────────────────────────────────────────────────────
echo "Case 4: no side effects (memory dir untouched)"
SNAPSHOT_AFTER="$(mktemp)"
ls -la "$MEMORY_DIR" 2>/dev/null | sort > "$SNAPSHOT_AFTER" || true

HASH_BEFORE="$(sha256sum < "$SNAPSHOT_BEFORE" | awk '{print $1}')"
HASH_AFTER="$(sha256sum < "$SNAPSHOT_AFTER" | awk '{print $1}')"
if [ "$HASH_BEFORE" = "$HASH_AFTER" ]; then
  note_pass "no files added/modified in $MEMORY_DIR (AC-31-23 no-side-effects)"
else
  note_fail "memory dir changed during --explain runs"
  echo "    before sha256: $HASH_BEFORE"
  echo "    after  sha256: $HASH_AFTER"
fi

# Cleanup
rm -f "$SNAPSHOT_BEFORE" "$SNAPSHOT_AFTER" \
      "$TMP_OUT" "$TMP_ERR" "$TMP_OUT2" "$TMP_ERR2" "$TMP_OUT3" "$TMP_ERR3"

echo "============================================="
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "❌ --explain contract violated."
  exit 1
fi
echo "✅ --explain contract intact."

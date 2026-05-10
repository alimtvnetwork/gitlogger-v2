#!/usr/bin/env bash
# test-check-99-stamp-bump.sh — self-test for §27 stamp-bump gate (Phase H4).
#
# Per Phase F3 addendum: new self-tests SHOULD be `.sh` with `set -euo pipefail`.
#
# Strategy: tests use the gate's `--changed-files` test-injection flag to
# bypass git entirely (sandbox forbids `git add`/`commit`). The injection
# path verifies the same fail/skip/pass logic as the production git path.
# T8 covers the production git path with a deliberately bad base-ref to
# exercise the structural-error branch.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GATE="$ROOT/linter-scripts/check-99-stamp-bump.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

assert() {
  local desc="$1"; local actual="$2"; local expected="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "  ✓ $desc"
    PASS=$((PASS+1))
  else
    echo "  ✗ $desc — expected '$expected', got '$actual'"
    FAIL=$((FAIL+1))
  fi
}

# Build a synthetic spec tree with mem index + §27 changelog so the gate
# can detect the current phase. No git — uses --changed-files injection.
make_sandbox() {
  local sb="$1"
  rm -rf "$sb"
  mkdir -p "$sb/.lovable/memory" \
           "$sb/spec/27-spec-toolchain" \
           "$sb/spec/test-folder" \
           "$sb/spec/_archive/old-folder" \
           "$sb/linter-scripts"
  cp "$GATE" "$sb/linter-scripts/check-99-stamp-bump.py"
  echo "Phase 147 — synthetic" > "$sb/.lovable/memory/index.md"
  echo "Phase 147 — synthetic changelog" > "$sb/spec/27-spec-toolchain/98-changelog.md"
}

echo "== test-check-99-stamp-bump.sh =="

# --- T1: empty changed-files → exit 0
SB="$TMP/t1"; make_sandbox "$SB"
: > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T1 empty changed-files exits 0" "$RC" "0"
grep -q "No §99 files changed" /tmp/h4-out \
  && { echo "  ✓ T1 emits 'No §99 files changed'"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T1 'No §99 files changed' missing"; FAIL=$((FAIL+1)); }

# --- T2: unstamped §99 changed → SKIP, exit 0
SB="$TMP/t2"; make_sandbox "$SB"
cat > "$SB/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
Unstamped content.
MD
echo "spec/test-folder/99-consistency-report.md" > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T2 unstamped §99 exits 0 (skip)" "$RC" "0"
grep -q "unstamped (skip):     1" /tmp/h4-out \
  && { echo "  ✓ T2 counts 1 unstamped skip"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T2 unstamped skip count missing"; FAIL=$((FAIL+1)); }

# --- T3: stamped §99 with --treat-as-stamp-only → SKIP, exit 0
SB="$TMP/t3"; make_sandbox "$SB"
cat > "$SB/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
<!-- verified-phase: 100 -->
Body.
MD
echo "spec/test-folder/99-consistency-report.md" > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt --treat-as-stamp-only >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T3 stamp-only diff exits 0 (skip)" "$RC" "0"
grep -q "stamp-only diff:      1" /tmp/h4-out \
  && { echo "  ✓ T3 counts 1 stamp-only skip"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T3 stamp-only skip count missing"; FAIL=$((FAIL+1)); }

# --- T4: stamped §99 with stale stamp (material edit assumed) → FAIL, exit 1
SB="$TMP/t4"; make_sandbox "$SB"
cat > "$SB/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
<!-- verified-phase: 100 -->
Materially edited but stamp not bumped.
MD
echo "spec/test-folder/99-consistency-report.md" > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T4 unbumped material edit exits 1" "$RC" "1"
grep -q "unbumped (issue):     1" /tmp/h4-out \
  && { echo "  ✓ T4 counts 1 unbumped issue"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T4 unbumped count missing"; FAIL=$((FAIL+1)); }
grep -q "stamp: Phase 100, current: Phase 147" /tmp/h4-out \
  && { echo "  ✓ T4 reports stamp/current phases"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T4 stamp/current report missing"; FAIL=$((FAIL+1)); }

# --- T5: same as T4 + --report-only → exit 0
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt --report-only >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T5 unbumped + --report-only exits 0" "$RC" "0"
grep -q "not failing" /tmp/h4-out \
  && { echo "  ✓ T5 emits 'not failing' footer"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T5 footer missing"; FAIL=$((FAIL+1)); }

# --- T6: stamped §99 with stamp == current → exit 0 (bumped)
SB="$TMP/t6"; make_sandbox "$SB"
cat > "$SB/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
<!-- verified-phase: 147 -->
Edited body AND bumped to current.
MD
echo "spec/test-folder/99-consistency-report.md" > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T6 edit + bump exits 0" "$RC" "0"
grep -q "bumped to current:    1" /tmp/h4-out \
  && { echo "  ✓ T6 counts 1 bumped"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T6 bumped count missing"; FAIL=$((FAIL+1)); }

# --- T7: _archive/ §99 in changed-files → excluded, exit 0
SB="$TMP/t7"; make_sandbox "$SB"
cat > "$SB/spec/_archive/old-folder/99-consistency-report.md" <<'MD'
# Archived §99
## Summary
<!-- verified-phase: 100 -->
Archived stale claim.
MD
echo "spec/_archive/old-folder/99-consistency-report.md" > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T7 _archive excluded (exits 0)" "$RC" "0"
grep -q "No §99 files changed" /tmp/h4-out \
  && { echo "  ✓ T7 _archive excluded from changed list"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T7 _archive leaked into changed list"; FAIL=$((FAIL+1)); }

# --- T8 (production git path): bad base-ref → exit 2
SB="$TMP/t8"; make_sandbox "$SB"
(cd "$SB" && git init -q -b main 2>/dev/null || true)
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --base-ref nonexistent-ref-xyzzy >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T8 bad base-ref exits 2" "$RC" "2"
grep -q "git diff failed\|cannot determine current phase" /tmp/h4-out \
  && { echo "  ✓ T8 emits diagnostic error"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T8 diagnostic error missing"; FAIL=$((FAIL+1)); }

# --- T9: missing phase token → exit 2
SB="$TMP/t9"; make_sandbox "$SB"
echo "no phase token here at all" > "$SB/.lovable/memory/index.md"
echo "nor here" > "$SB/spec/27-spec-toolchain/98-changelog.md"
: > "$SB/changed.txt"
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T9 missing phase token exits 2" "$RC" "2"
grep -q "cannot determine current phase" /tmp/h4-out \
  && { echo "  ✓ T9 emits cannot-determine-phase error"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T9 phase-detection error missing"; FAIL=$((FAIL+1)); }

# --- T10: mixed batch (1 stamped-fresh + 1 stamped-stale + 1 unstamped) → exit 1, accurate counts
SB="$TMP/t10"; make_sandbox "$SB"
mkdir -p "$SB/spec/a" "$SB/spec/b" "$SB/spec/c"
cat > "$SB/spec/a/99-consistency-report.md" <<'MD'
## Summary
<!-- verified-phase: 147 -->
fresh
MD
cat > "$SB/spec/b/99-consistency-report.md" <<'MD'
## Summary
<!-- verified-phase: 100 -->
stale
MD
cat > "$SB/spec/c/99-consistency-report.md" <<'MD'
## Summary
unstamped
MD
cat > "$SB/changed.txt" <<EOF
spec/a/99-consistency-report.md
spec/b/99-consistency-report.md
spec/c/99-consistency-report.md
EOF
set +e
(cd "$SB" && python3 linter-scripts/check-99-stamp-bump.py --changed-files changed.txt >/tmp/h4-out 2>&1)
RC=$?
set -e
assert "T10 mixed batch (1 unbumped) exits 1" "$RC" "1"
grep -q "Changed §99 files: 3" /tmp/h4-out \
  && { echo "  ✓ T10 counts 3 changed"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T10 changed count missing"; FAIL=$((FAIL+1)); }
grep -q "bumped to current:    1" /tmp/h4-out \
  && { echo "  ✓ T10 counts 1 bumped"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T10 bumped count missing"; FAIL=$((FAIL+1)); }
grep -q "unstamped (skip):     1" /tmp/h4-out \
  && { echo "  ✓ T10 counts 1 unstamped"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T10 unstamped count missing"; FAIL=$((FAIL+1)); }

echo
echo "Results: $PASS passed, $FAIL failed"
if [[ "$FAIL" -gt 0 ]]; then exit 1; fi
echo "✅ §27 stamp-bump gate self-test green."

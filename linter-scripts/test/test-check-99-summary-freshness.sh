#!/usr/bin/env bash
# test-check-99-summary-freshness.sh — self-test for §26 gate (Phase H1).
#
# Per Phase F3 addendum: new self-tests SHOULD be `.sh` with `set -euo pipefail`
# + `assert` contract + `test-readme-inventory.sh` parity.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GATE="$ROOT/linter-scripts/check-99-summary-freshness.py"
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

echo "== test-check-99-summary-freshness.sh =="

# --- T1: real-tree run (default mode) — should exit 0 (Phase H2: gate now
# scans all §99 files except _archive/ and accepts stamps under Summary OR
# inventory-rubric headings; assert structural shape only, not exact counts
# which churn as adoption progresses).
set +e
PYTHONIOENCODING=utf-8 python3 "$GATE" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T1 real-tree default mode exits 0" "$RC" "0"
grep -qE "§99 files scanned: [0-9]+; stamped: [0-9]+; exempt: [0-9]+; unstamped: [0-9]+" /tmp/h1-out && echo "  ✓ T1 reports scan/stamped/exempt/unstamped counts" || { echo "  ✗ T1 counts line missing"; FAIL=$((FAIL+1)); }

# --- T2: real-tree --report-only also exits 0
set +e
python3 "$GATE" --report-only >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T2 --report-only exits 0" "$RC" "0"

# --- T3: --max-age default visible in header
python3 "$GATE" 2>&1 | grep -q "max stale delta: 20" \
  && { echo "  ✓ T3 default --max-age=20 in header"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T3 default --max-age missing from header"; FAIL=$((FAIL+1)); }

# --- T4: structural error path (no Phase token visible) — synthetic
SANDBOX="$TMP/sandbox"
mkdir -p "$SANDBOX/spec/test-folder" "$SANDBOX/.lovable/memory" "$SANDBOX/spec/27-spec-toolchain"
cp "$GATE" "$SANDBOX/check.py"
# rewrite REPO to point at sandbox
sed -i "s|REPO = Path(__file__).resolve().parent.parent|REPO = Path('$SANDBOX').resolve()|" "$SANDBOX/check.py"
echo "(no phase tokens here)" > "$SANDBOX/.lovable/memory/index.md"
echo "(no phase tokens here either)" > "$SANDBOX/spec/27-spec-toolchain/98-changelog.md"
echo "## Summary" > "$SANDBOX/spec/test-folder/99-consistency-report.md"
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T4 missing-phase-token exits 2" "$RC" "2"
grep -q "cannot determine current phase" /tmp/h1-out \
  && { echo "  ✓ T4 emits cannot-determine error"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T4 error message missing"; FAIL=$((FAIL+1)); }

# --- T5: stamped + stale exits 1 (synthetic)
echo "Phase 200" >> "$SANDBOX/.lovable/memory/index.md"
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
<!-- verified-phase: 100 -->
Some claim.
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T5 stamped+stale (delta 100, max 20) exits 1" "$RC" "1"
grep -q "stamp: Phase 100, delta: 100" /tmp/h1-out \
  && { echo "  ✓ T5 reports stamp + delta"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T5 stamp/delta line missing"; FAIL=$((FAIL+1)); }

# --- T6: stamped + stale + --report-only exits 0
set +e
python3 "$SANDBOX/check.py" --report-only >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T6 stamped+stale + --report-only exits 0" "$RC" "0"
grep -q "not failing" /tmp/h1-out \
  && { echo "  ✓ T6 emits 'not failing' footer"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T6 footer missing"; FAIL=$((FAIL+1)); }

# --- T7: stamped + fresh exits 0
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Summary
<!-- verified-phase: 195 -->
Some claim.
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T7 stamped+fresh (delta 5, max 20) exits 0" "$RC" "0"
grep -q "stamped: 1" /tmp/h1-out \
  && { echo "  ✓ T7 counts 1 stamped"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T7 stamped count missing"; FAIL=$((FAIL+1)); }

# --- T8 (Phase H2): stamp under ## Module Health is accepted (inventory rubric)
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## Module Health
<!-- verified-phase: 195 -->
Inventory rubric, no narrative summary.
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T8 (H2) stamp under ## Module Health accepted (exits 0)" "$RC" "0"
grep -q "stamped: 1" /tmp/h1-out \
  && { echo "  ✓ T8 counts 1 stamped under inventory rubric"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T8 inventory-rubric stamp not counted"; FAIL=$((FAIL+1)); }

# --- T9 (Phase H2): stamp under ## File Inventory also accepted
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
## File Inventory
<!-- verified-phase: 195 -->

| File | Present |
|------|---------|
| 00-overview.md | ✅ |
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T9 (H2) stamp under ## File Inventory accepted (exits 0)" "$RC" "0"
grep -q "stamped: 1" /tmp/h1-out \
  && { echo "  ✓ T9 counts 1 stamped under File Inventory"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T9 File-Inventory stamp not counted"; FAIL=$((FAIL+1)); }

# --- T10 (Phase H2): _archive/ files are excluded from scan
mkdir -p "$SANDBOX/spec/_archive/old-folder"
cat > "$SANDBOX/spec/_archive/old-folder/99-consistency-report.md" <<'MD'
# Archived §99
## Summary
Stale archived content with no stamp — must be excluded.
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T10 (H2) _archive/ excluded (still exits 0)" "$RC" "0"
# Should still report exactly 1 file scanned (the test-folder one), not 2.
grep -q "files scanned: 1" /tmp/h1-out \
  && { echo "  ✓ T10 _archive/ excluded from scan count"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T10 _archive/ leaked into scan"; FAIL=$((FAIL+1)); }

# --- T11 (Phase H7): exempt marker is honored — file with no tracked heading
# but carrying `<!-- freshness-exempt: audit-log-only -->` is counted exempt,
# not unstamped, and does not trip the unstamped advisory tally for that file.
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Audit-log-only §99
<!-- freshness-exempt: audit-log-only -->

## 2026-04-27 — Phase 69 audit
Past audit-log entry, no narrative summary.
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T11 (H7) exempt marker counted as exempt (exits 0)" "$RC" "0"
grep -q "exempt: 1" /tmp/h1-out \
  && { echo "  ✓ T11 exempt count reported"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T11 exempt count missing"; FAIL=$((FAIL+1)); }
grep -q "unstamped: 0" /tmp/h1-out \
  && { echo "  ✓ T11 exempt file does not increment unstamped"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T11 exempt file leaked into unstamped tally"; FAIL=$((FAIL+1)); }

# --- T12 (Phase H9): misplaced stamp (BEFORE tracked heading) is detected
# in advisory mode — exits 0 but emits warning.
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99
<!-- verified-phase: 195 -->

## Summary
Narrative claim — stamp is on wrong line (above heading, not under it).
MD
set +e
python3 "$SANDBOX/check.py" >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T12 (H9) misplaced stamp + default mode exits 0 (advisory)" "$RC" "0"
grep -q "placed immediately BEFORE a tracked heading" /tmp/h1-out \
  && { echo "  ✓ T12 misplaced-stamp warning emitted"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T12 misplaced-stamp warning missing"; FAIL=$((FAIL+1)); }
grep -q "advisory" /tmp/h1-out \
  && { echo "  ✓ T12 mode label says advisory"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T12 mode label missing"; FAIL=$((FAIL+1)); }

# --- T13 (Phase H9): --strict-position turns the misplaced stamp into a failure.
set +e
python3 "$SANDBOX/check.py" --strict-position >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T13 (H9) misplaced stamp + --strict-position exits 1" "$RC" "1"
grep -q "strict-position" /tmp/h1-out \
  && { echo "  ✓ T13 mode label says strict-position"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T13 mode label missing"; FAIL=$((FAIL+1)); }

# --- T14 (Phase H9): stamp inside blockquote (no nearby tracked heading) is
# NOT flagged as misplaced — only adjacency to a tracked heading triggers.
cat > "$SANDBOX/spec/test-folder/99-consistency-report.md" <<'MD'
# Test §99

> Past phase note: we stamped `<!-- verified-phase: 100 -->` here in Phase 100.
> This is documentation, not a real stamp.

Some prose unrelated to any tracked heading.
MD
set +e
python3 "$SANDBOX/check.py" --strict-position >/tmp/h1-out 2>&1
RC=$?
set -e
assert "T14 (H9) stamp in blockquote (no nearby heading) does not fail strict-position" "$RC" "0"
! grep -q "placed immediately BEFORE" /tmp/h1-out \
  && { echo "  ✓ T14 no false-positive misplaced warning"; PASS=$((PASS+1)); } \
  || { echo "  ✗ T14 false-positive misplaced warning emitted"; FAIL=$((FAIL+1)); }

echo
echo "Results: $PASS passed, $FAIL failed"
if [[ "$FAIL" -gt 0 ]]; then exit 1; fi
echo "✅ §26 freshness gate self-test green."

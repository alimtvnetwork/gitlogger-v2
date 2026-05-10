#!/usr/bin/env bash
# test-check-spec-cross-links.sh
#
# Phase P35 — Self-test for `linter-scripts/check-spec-cross-links.py` fuzzy
# waiver matching, --rewrite-allowlist, and --strict-line-match contracts
# (AC-01-05, AC-01-06, AC-01-07).
#
# Codifies the P34 lesson #1: stamp-batch tools that insert lines above a
# waived link drift the line number, silently breaking CI. The fuzzy match
# resolves drift up to ±5 lines; --rewrite-allowlist auto-bumps;
# --strict-line-match opts back into exact-line semantics.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LINTER="${REPO_ROOT}/linter-scripts/check-spec-cross-links.py"

if [[ ! -f "${LINTER}" ]]; then
  echo "❌ FATAL: ${LINTER} not found"
  exit 2
fi

PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then
    echo "  ✅ ${label}"
    PASS=$((PASS+1))
  else
    echo "  ❌ ${label}"
    FAIL=$((FAIL+1))
  fi
}

# Build a synthetic sandbox: tiny spec/ tree with one file that links to a
# missing target, plus a matching allowlist whose line number is drifted.
SANDBOX="$(mktemp -d -t cross-links-test-XXXXXX)"
trap 'rm -rf "${SANDBOX}"' EXIT

mkdir -p "${SANDBOX}/spec/sample" "${SANDBOX}/linter-scripts"

# 7-line file with the broken link at line 7.
cat > "${SANDBOX}/spec/sample/00-overview.md" <<'EOF'
# Sample

Header line 3.

Body line 5.

See [missing](./does-not-exist.md) for details.
EOF

# Allowlist waives the link at line 4 (drifted -3 from actual line 7).
cat > "${SANDBOX}/linter-scripts/spec-cross-links.allowlist" <<'EOF'
# Test allowlist
spec/sample/00-overview.md:4:./does-not-exist.md
EOF

cd "${SANDBOX}"

echo "==> T1: AC-01-05 — Fuzzy match accepts drift ≤ 5 lines (default mode)"
OUT="$(python3 "${LINTER}" --root spec --repo-root . --json 2>&1)"
EXIT=$?
assert "T1.1 exit code 0 despite drift"          test "${EXIT}" -eq 0
assert "T1.2 failures count is 0"                grep -q '"count": 0' <<< "${OUT}"
assert "T1.3 fuzzy_count is 1"                   grep -q '"fuzzy_count": 1' <<< "${OUT}"
assert "T1.4 fuzzy_hits names current line 7"    grep -q '"current_line": 7' <<< "${OUT}"
assert "T1.5 fuzzy_hits names stale line 4"      grep -q '"stale_line": 4' <<< "${OUT}"

echo "==> T2: AC-01-07 — --strict-line-match disables fuzzy match"
set +e
OUT2="$(python3 "${LINTER}" --root spec --repo-root . --strict-line-match --json 2>&1)"
EXIT2=$?
set -e
assert "T2.1 exit code 1 in strict mode"         test "${EXIT2}" -eq 1
assert "T2.2 failures count is 1"                grep -q '"count": 1' <<< "${OUT2}"
assert "T2.3 fuzzy_count is 0 in strict mode"    grep -q '"fuzzy_count": 0' <<< "${OUT2}"

echo "==> T3: AC-01-06 — --rewrite-allowlist bumps stale line + idempotent"
OUT3="$(python3 "${LINTER}" --root spec --repo-root . --rewrite-allowlist --json 2>&1)"
EXIT3=$?
assert "T3.1 exit code 0 after rewrite"          test "${EXIT3}" -eq 0
assert "T3.2 rewritten count is 1"               grep -q '"rewritten": 1' <<< "${OUT3}"
assert "T3.3 allowlist now contains line 7"      grep -q '^spec/sample/00-overview.md:7:./does-not-exist.md$' linter-scripts/spec-cross-links.allowlist
if grep -q '^spec/sample/00-overview.md:4:./does-not-exist.md$' linter-scripts/spec-cross-links.allowlist; then
  STALE_GONE=1
else
  STALE_GONE=0
fi
assert "T3.4 stale line 4 entry removed"         test "${STALE_GONE}" -eq 0
assert "T3.5 comment header preserved"           grep -q '^# Test allowlist$' linter-scripts/spec-cross-links.allowlist

echo "==> T4: idempotence — second rewrite is no-op"
OUT4="$(python3 "${LINTER}" --root spec --repo-root . --rewrite-allowlist --json 2>&1)"
EXIT4=$?
assert "T4.1 exit code 0"                        test "${EXIT4}" -eq 0
assert "T4.2 fuzzy_count is 0 (no drift left)"   grep -q '"fuzzy_count": 0' <<< "${OUT4}"
assert "T4.3 rewritten is 0"                     grep -q '"rewritten": 0' <<< "${OUT4}"

echo "==> T5: out-of-tolerance drift (+10) does NOT fuzzy-match"
# Reset allowlist to a line 12 lines away from actual link at line 7.
cat > "${SANDBOX}/linter-scripts/spec-cross-links.allowlist" <<'EOF'
# Test allowlist
spec/sample/00-overview.md:19:./does-not-exist.md
EOF
set +e
OUT5="$(python3 "${LINTER}" --root spec --repo-root . --json 2>&1)"
EXIT5=$?
set -e
assert "T5.1 exit code 1 (out-of-tolerance)"     test "${EXIT5}" -eq 1
assert "T5.2 fuzzy_count is 0 (no fuzzy match)"  grep -q '"fuzzy_count": 0' <<< "${OUT5}"
assert "T5.3 failures count is 1"                grep -q '"count": 1' <<< "${OUT5}"

echo
echo "Results: ${PASS} passed, ${FAIL} failed"
if [[ ${FAIL} -gt 0 ]]; then
  exit 1
fi
exit 0

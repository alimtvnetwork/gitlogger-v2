#!/bin/bash
# ============================================================
# Axios Version Safeguard
# ============================================================
# Validates that Axios is pinned to an approved safe version
# and not using any range symbols (^, ~, >=, *).
#
# Blocked versions: 1.14.1, 0.30.4
# Approved versions: 1.14.0, 0.30.3
#
# Usage:
#   bash linter-scripts/check-axios-version.sh             # check repo package.json
#   bash linter-scripts/check-axios-version.sh --self-test # run synthetic fixture probes
#   bash linter-scripts/check-axios-version.sh --pkg <path># check arbitrary package.json
# ============================================================

set -euo pipefail

BLOCKED_VERSIONS=("1.14.1" "0.30.4")
APPROVED_VERSIONS=("1.14.0" "0.30.3")

PKG_PATH="./package.json"
SELF_TEST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --self-test) SELF_TEST=1; shift ;;
    --pkg)       PKG_PATH="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--self-test] [--pkg <package.json>]"; exit 0 ;;
    *) echo "Unknown flag: $1" >&2; exit 2 ;;
  esac
done

check_pkg() {
  local pkg="$1"
  local current
  current=$(node -e "
    const pkg = require('$pkg');
    const v = (pkg.dependencies && pkg.dependencies.axios) || (pkg.devDependencies && pkg.devDependencies.axios) || 'NOT_FOUND';
    console.log(v);
  ")

  if [[ "$current" == "NOT_FOUND" ]]; then
    echo "  axios not declared in $pkg → vacuous-pass"
    return 0
  fi
  if [[ "$current" == ^* ]] || [[ "$current" == ~* ]] || [[ "$current" == ">="* ]] || [[ "$current" == "*" ]] || [[ "$current" == "latest" ]]; then
    echo "  ❌ axios=$current uses range symbol/tag (AC-52-01)"
    return 1
  fi
  for blocked in "${BLOCKED_VERSIONS[@]}"; do
    if [[ "$current" == "$blocked" ]]; then
      echo "  ❌ axios=$current is BLOCKED (AC-52-02)"
      return 1
    fi
  done
  for approved in "${APPROVED_VERSIONS[@]}"; do
    if [[ "$current" == "$approved" ]]; then
      echo "  ✅ axios=$current is approved (AC-52-03)"
      return 0
    fi
  done
  echo "  ⚠️  axios=$current not in approved list (${APPROVED_VERSIONS[*]})"
  return 1
}

run_self_test() {
  # Sess-66 G-6t — synthetic fixture probe (slot 52 phantom-clearing).
  # Three fixtures lock AC-52-01/02/03 contracts in CI.
  local td; td=$(mktemp -d)
  trap 'rm -rf "$td"' EXIT
  local fail=0

  # F-1 AC-52-01 range symbol → exit 1
  echo '{"dependencies":{"axios":"^1.14.0"}}' > "$td/p1.json"
  if check_pkg "$td/p1.json" >/dev/null; then
    echo "  ✘ F-1 AC-52-01: range symbol should fail"; fail=1
  else
    echo "  ✓ F-1 AC-52-01: range symbol correctly fails"
  fi

  # F-2 AC-52-02 blocked exact → exit 1
  echo '{"dependencies":{"axios":"1.14.1"}}' > "$td/p2.json"
  if check_pkg "$td/p2.json" >/dev/null; then
    echo "  ✘ F-2 AC-52-02: blocked exact should fail"; fail=1
  else
    echo "  ✓ F-2 AC-52-02: blocked exact correctly fails"
  fi

  # F-3 AC-52-03 approved exact → exit 0
  echo '{"dependencies":{"axios":"1.14.0"}}' > "$td/p3.json"
  if check_pkg "$td/p3.json" >/dev/null; then
    echo "  ✓ F-3 AC-52-03: approved exact correctly passes"
  else
    echo "  ✘ F-3 AC-52-03: approved exact should pass"; fail=1
  fi

  # F-4 second-approved (0.30.3)
  echo '{"devDependencies":{"axios":"0.30.3"}}' > "$td/p4.json"
  if check_pkg "$td/p4.json" >/dev/null; then
    echo "  ✓ F-4 AC-52-03: 0.30.3 approved (devDep) correctly passes"
  else
    echo "  ✘ F-4 AC-52-03: 0.30.3 should pass"; fail=1
  fi

  # F-5 second-blocked (0.30.4)
  echo '{"dependencies":{"axios":"0.30.4"}}' > "$td/p5.json"
  if check_pkg "$td/p5.json" >/dev/null; then
    echo "  ✘ F-5 AC-52-02: 0.30.4 should fail"; fail=1
  else
    echo "  ✓ F-5 AC-52-02: 0.30.4 correctly fails"
  fi

  # F-6 NOT_FOUND vacuous-pass anchor
  echo '{"dependencies":{}}' > "$td/p6.json"
  if check_pkg "$td/p6.json" >/dev/null; then
    echo "  ✓ F-6 vacuous-pass: missing axios correctly passes"
  else
    echo "  ✘ F-6 vacuous-pass: missing axios should pass"; fail=1
  fi

  if [ "$fail" -eq 0 ]; then
    echo "[check-axios-version --self-test] OK (6/6 fixtures)"
    return 0
  else
    echo "[check-axios-version --self-test] FAILED"
    return 1
  fi
}

if [ "$SELF_TEST" -eq 1 ]; then
  run_self_test
  exit $?
fi

echo "📦 Axios version check on $PKG_PATH"
check_pkg "$PKG_PATH"

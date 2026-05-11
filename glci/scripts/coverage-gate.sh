#!/usr/bin/env bash
# coverage-gate.sh — enforce per-package coverage minimums.
#
# Reads coverage.out (produced by `go test -coverprofile`), invokes
# `go tool cover -func`, and fails (exit 1) if any package listed in
# THRESHOLDS falls below its declared minimum percent. Packages not in
# THRESHOLDS are reported but do not gate.
#
# Usage:
#   ./scripts/coverage-gate.sh coverage.out
set -euo pipefail

PROFILE="${1:-coverage.out}"
if [[ ! -f "$PROFILE" ]]; then
  echo "coverage-gate: $PROFILE not found" >&2
  exit 2
fi

# Per-package floors (percent). Conservative: only gate packages that have
# tests today; raise as coverage grows. Packages omitted = no gate.
declare -A THRESHOLDS=(
  [ci]=70
  [config]=70
  [detect]=60
  [ship]=55
  [laneb]=40
  [runner]=30
  [selftest]=50
  [selfupdate]=30
  [auth]=40
  [classify]=60
  [cmd]=15

)

# Aggregate per-package coverage from `go tool cover -func`.
# Output rows look like:
#   github.com/example/glci/internal/ci/ci.go:42:    Foo   83.3%
# total row (last) is "total: ...". Skip it; we want per-package.
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
go tool cover -func="$PROFILE" > "$TMP"

declare -A COVERED_STMTS
declare -A TOTAL_STMTS

# Re-parse the raw profile to compute weighted package coverage
# (statement counts, not unweighted function-line averages).
# Profile format: "<file>:<startLine>.<startCol>,<endLine>.<endCol> <numStmt> <count>"
while IFS= read -r line; do
  [[ "$line" == mode:* ]] && continue
  [[ -z "$line" ]] && continue
  file="${line%%:*}"
  rest="${line#*:}"
  numStmt="$(awk '{print $2}' <<<"$rest")"
  count="$(awk '{print $3}' <<<"$rest")"
  # Extract package: strip "github.com/example/glci/internal/<pkg>/..."
  pkg="$(awk -F/ '{ for(i=1;i<=NF;i++) if($i=="internal"){print $(i+1); exit}}' <<<"$file")"
  [[ -z "$pkg" ]] && continue
  TOTAL_STMTS[$pkg]=$(( ${TOTAL_STMTS[$pkg]:-0} + numStmt ))
  if [[ "$count" -gt 0 ]]; then
    COVERED_STMTS[$pkg]=$(( ${COVERED_STMTS[$pkg]:-0} + numStmt ))
  fi
done < "$PROFILE"

FAIL=0
printf '%-14s %8s %8s %s\n' "PACKAGE" "COVERED" "FLOOR" "STATUS"
printf '%-14s %8s %8s %s\n' "-------" "-------" "-----" "------"

# Sort packages for deterministic output.
PKGS=()
for pkg in "${!TOTAL_STMTS[@]}"; do PKGS+=("$pkg"); done
IFS=$'\n' SORTED=($(sort <<<"${PKGS[*]}")); unset IFS

for pkg in "${SORTED[@]}"; do
  total=${TOTAL_STMTS[$pkg]}
  covered=${COVERED_STMTS[$pkg]:-0}
  if (( total == 0 )); then continue; fi
  pct=$(awk -v c="$covered" -v t="$total" 'BEGIN{ printf "%.1f", (c*100)/t }')
  floor="${THRESHOLDS[$pkg]:-}"
  status="info"
  if [[ -n "$floor" ]]; then
    cmp=$(awk -v p="$pct" -v f="$floor" 'BEGIN{ print (p+0 < f+0) ? "below" : "ok" }')
    if [[ "$cmp" == "below" ]]; then
      status="FAIL (<${floor}%)"
      FAIL=1
    else
      status="ok (>=${floor}%)"
    fi
  fi
  printf '%-14s %7s%% %7s%% %s\n' "$pkg" "$pct" "${floor:-—}" "$status"
done

if (( FAIL == 1 )); then
  echo ""
  echo "coverage-gate: at least one package fell below its declared floor." >&2
  exit 1
fi
echo ""
echo "coverage-gate: all gated packages meet their floors."

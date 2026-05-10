#!/usr/bin/env bash
# test-check-version-parity.sh — H10 (Phase P15) self-test.
#
# Spec: spec/27-spec-toolchain/29-check-version-parity.md
# Validates the §00 ↔ §98 Version-field parity gate's contract:
#   T1  banner shape line includes scanned/eligible/matches/mismatches/skipped fields
#   T2  default mode exits 0 even when mismatches present (advisory)
#   T3  --strict exits 1 when mismatches present
#   T4  --strict --report-only exits 0 (override)
#   T5  module with matched §00 ↔ §98 versions counts as match (synthetic)
#   T6  module with no §00 banner Version is skipped (skipped_no_banner++)
#   T7  module with no §98 release is skipped (skipped_no_release++)
#   T8  table-row §98 format (folder 22 style) parsed correctly
#   T9  --json output is valid JSON with required keys (incl. stamped/stamped_failed)
#   T10 _archive/ excluded from scan
#   T11 Phase P20: stamped §00 with mismatch fails default mode (per-file strict)
#   T12 Phase P20: stamped §00 with match passes (counts as stamped + match)
#   T13 Phase P20: --report-only overrides per-file stamp failure
#   T14 Phase 153 Task #35-fu: latest_release() returns SemVer-MAX, not positional-first

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
GATE="${ROOT}/linter-scripts/check-version-parity.py"

assert() {
    local label="$1"; shift
    if "$@"; then
        echo "  ✓ ${label}"
    else
        echo "  ✗ ${label}" >&2
        echo "    cmd: $*" >&2
        return 1
    fi
}

PASS=0
FAIL=0
run() {
    local name="$1"; shift
    if "$@"; then
        PASS=$((PASS+1))
    else
        echo "T${name} FAILED" >&2
        FAIL=$((FAIL+1))
    fi
}

# T1 banner shape
t1() {
    local out
    out="$(python3 "$GATE" 2>&1 | head -1)"
    [[ "$out" == *"scanned="* ]] && \
    [[ "$out" == *"eligible="* ]] && \
    [[ "$out" == *"matches="* ]] && \
    [[ "$out" == *"mismatches="* ]] && \
    [[ "$out" == *"skipped(no-banner)="* ]] && \
    [[ "$out" == *"skipped(no-release)="* ]]
}

# T2 default exit 0 with mismatches present (advisory mode, no stamps).
# Phase 153 Task #35-fu: switched from real-tree to sandbox — real tree now
# has 74/74 stamped modules, so per-file strict promotion fires whenever any
# mismatch exists, breaking the "default exits 0" assertion. Sandbox isolates
# the contract under test (advisory-by-default for unstamped drift).
t2() {
    local sb="$SANDBOX/t2/spec"
    rm -rf "$SANDBOX/t2"; mkdir -p "$sb"
    mk_module "$sb/drift" "1.0.0" "2.0.0" "heading"   # unstamped → advisory
    python3 "$GATE" --spec-root "$sb" >/dev/null 2>&1
}

# T3 strict exits 1 when sandbox contains a mismatch
# (Phase P31: real tree is now 74/74 matches, so we must inject drift
# in a sandbox to exercise this contract — was relying on real-tree
# mismatches pre-P30 backlog clearance.)
t3() {
    local sb="$SANDBOX/t3/spec"
    rm -rf "$SANDBOX/t3"; mkdir -p "$sb"
    mk_module "$sb/drift" "1.0.0" "2.0.0" "heading"
    ! python3 "$GATE" --strict --spec-root "$sb" >/dev/null 2>&1
}

# T4 strict + report-only exits 0
t4() {
    python3 "$GATE" --strict --report-only >/dev/null 2>&1
}

# Sandbox helpers
SANDBOX="$(mktemp -d)"
trap 'rm -rf "$SANDBOX"' EXIT

mk_module() {
    local dir="$1" banner_v="$2" release_v="$3" release_format="$4" stamp="${5:-}"
    mkdir -p "$dir"
    if [[ -n "$banner_v" ]]; then
        printf '# Test\n\n**Version:** %s\n**Updated:** 2026-04-28\n' "$banner_v" > "$dir/00-overview.md"
        if [[ -n "$stamp" ]]; then
            printf '<!-- h10-verified-phase: %s -->\n' "$stamp" >> "$dir/00-overview.md"
        fi
    else
        printf '# Test\n\n**Updated:** 2026-04-28\n' > "$dir/00-overview.md"
    fi
    case "$release_format" in
      heading)
        printf '# Changelog\n\n## %s — 2026-04-28\n- entry\n' "$release_v" > "$dir/98-changelog.md"
        ;;
      table)
        printf '# Changelog\n\n| Version | Date | Notes |\n|---------|------|-------|\n| %s | 2026-04-28 | entry |\n' "$release_v" > "$dir/98-changelog.md"
        ;;
      none)
        printf '# Changelog\n\n(empty)\n' > "$dir/98-changelog.md"
        ;;
    esac
}

# T5 matched module
t5() {
    local sb="$SANDBOX/t5/spec"
    rm -rf "$SANDBOX/t5"; mkdir -p "$sb"
    mk_module "$sb/mod" "1.2.3" "1.2.3" "heading"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"matches=1"* ]] && [[ "$out" == *"mismatches=0"* ]]
}

# T6 no banner skipped
t6() {
    local sb="$SANDBOX/t6/spec"
    rm -rf "$SANDBOX/t6"; mkdir -p "$sb"
    mk_module "$sb/mod" "" "1.2.3" "heading"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"skipped(no-banner)=1"* ]] && [[ "$out" == *"eligible=0"* ]]
}

# T7 no release skipped
t7() {
    local sb="$SANDBOX/t7/spec"
    rm -rf "$SANDBOX/t7"; mkdir -p "$sb"
    mk_module "$sb/mod" "1.2.3" "" "none"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"skipped(no-release)=1"* ]] && [[ "$out" == *"eligible=0"* ]]
}

# T8 table-row format parsed
t8() {
    local sb="$SANDBOX/t8/spec"
    rm -rf "$SANDBOX/t8"; mkdir -p "$sb"
    mk_module "$sb/mod" "3.9.8" "3.9.8" "table"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"matches=1"* ]] && [[ "$out" == *"mismatches=0"* ]]
}

# T9 --json valid (Phase P20: also asserts stamped/stamped_failed keys).
# Phase 153 Task #35-fu: switched to sandbox — same reason as T2 (real-tree
# stamped+drift now exits 1, killing stdin to the JSON parser).
t9() {
    local sb="$SANDBOX/t9/spec"
    rm -rf "$SANDBOX/t9"; mkdir -p "$sb"
    mk_module "$sb/mod" "1.2.3" "1.2.3" "heading"
    python3 "$GATE" --spec-root "$sb" --json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
required = {'scanned','eligible','matches','mismatches','skipped_no_banner','skipped_no_release','stamped','stamped_failed','details'}
sys.exit(0 if required.issubset(d.keys()) else 1)
"
}

# T10 _archive excluded
t10() {
    local sb="$SANDBOX/t10/spec"
    rm -rf "$SANDBOX/t10"; mkdir -p "$sb"
    mk_module "$sb/_archive/old" "1.2.3" "9.9.9" "heading"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"scanned=0"* ]]
}

# T11 Phase P20: stamped §00 with mismatch FAILS even in default mode
t11() {
    local sb="$SANDBOX/t11/spec"
    rm -rf "$SANDBOX/t11"; mkdir -p "$sb"
    mk_module "$sb/mod" "1.2.3" "1.2.4" "heading" "200"
    local out rc
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)" && rc=0 || rc=$?
    [[ $rc -eq 1 ]] && [[ "$out" == *"stamped=1"* ]] && [[ "$out" == *"stamped_failed=1"* ]] && [[ "$out" == *"(FAIL)"* ]]
}

# T12 Phase P20: stamped §00 with match passes (counts as stamped + match)
t12() {
    local sb="$SANDBOX/t12/spec"
    rm -rf "$SANDBOX/t12"; mkdir -p "$sb"
    mk_module "$sb/mod" "2.0.0" "2.0.0" "heading" "201"
    local out rc
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)" && rc=0 || rc=$?
    [[ $rc -eq 0 ]] && [[ "$out" == *"matches=1"* ]] && [[ "$out" == *"stamped=1"* ]] && [[ "$out" == *"stamped_failed=0"* ]]
}

# T13 Phase P20: --report-only overrides per-file stamp failure
t13() {
    local sb="$SANDBOX/t13/spec"
    rm -rf "$SANDBOX/t13"; mkdir -p "$sb"
    mk_module "$sb/mod" "1.0.0" "1.0.1" "heading" "202"
    python3 "$GATE" --spec-root "$sb" --report-only >/dev/null 2>&1
}

# T14 Phase 153 Task #35-fu: latest_release() returns SemVer-MAX, not positional-first.
# Builds a §98 where row order does NOT equal SemVer order:
#   ## 4.0.1 — 2026-04-29 (Phase 153 reconciliation patch, prepended top)
#   ## 4.1.0 — 2026-04-27 (older but SemVer-higher minor release)
# §00 banner = 4.1.0 (SemVer-max). Pre-fix gate compared 4.1.0 ↔ 4.0.1 → MISMATCH.
# Post-fix gate compares 4.1.0 ↔ 4.1.0 (max(4.0.1, 4.1.0)) → MATCH.
t14() {
    local sb="$SANDBOX/t14/spec"
    rm -rf "$SANDBOX/t14"; mkdir -p "$sb/mod"
    printf '# Test\n\n**Version:** 4.1.0\n**Updated:** 2026-04-29\n' > "$sb/mod/00-overview.md"
    printf '# Changelog\n\n## 4.0.1 — 2026-04-29 (reconciliation patch)\n- entry\n\n## 4.1.0 — 2026-04-27 (older minor)\n- entry\n' > "$sb/mod/98-changelog.md"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"matches=1"* ]] && [[ "$out" == *"mismatches=0"* ]]
}

# T15 Phase J3-fu (Lesson #28-fu): blockquote release prose `> **vX.Y.Z`
# is recognised as a release shape. §98 has no heading + no row, only a
# blockquote v2.0.0 update. §00 banner = 2.0.0 → MATCH.
t15() {
    local sb="$SANDBOX/t15/spec"
    rm -rf "$SANDBOX/t15"; mkdir -p "$sb/mod"
    printf '# Test\n\n**Version:** 2.0.0\n**Updated:** 2026-05-07\n' > "$sb/mod/00-overview.md"
    printf '# Changelog\n\n> **v2.0.0 update (Phase X — blockquote release):** entry body.\n' > "$sb/mod/98-changelog.md"
    local out
    out="$(python3 "$GATE" --spec-root "$sb" 2>&1)"
    [[ "$out" == *"matches=1"* ]] && [[ "$out" == *"mismatches=0"* ]] && [[ "$out" != *"skipped(no-release)=1"* ]]
}

echo "test-check-version-parity.sh"
run 1 t1
run 2 t2
run 3 t3
run 4 t4
run 5 t5
run 6 t6
run 7 t7
run 8 t8
run 9 t9
run 10 t10
run 11 t11
run 12 t12
run 13 t13
run 14 t14
run 15 t15

echo "──────────────────────────────"
echo "PASS: $PASS    FAIL: $FAIL"
[[ $FAIL -eq 0 ]] || exit 1

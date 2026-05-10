#!/usr/bin/env bash
# linter-scripts/test/test-readme-inventory.sh
#
# Phase 102 — README ↔ filesystem inventory parity for `linter-scripts/test/`.
#
# Locks: AC-31-27 (Phase 98) — the "Test inventory" table in
# `linter-scripts/test/README.md` MUST list exactly the set of `test-*.sh`
# scripts present in the directory, neither more nor fewer.
#
# Without this self-test, AC-31-27 is enforced only by reviewer attention:
# a contributor adding a new `test-foo.sh` (or removing an existing one)
# without updating the README would not fail any gate. The Phase 91/94/95
# self-tests check the *targets'* behaviour; this one checks the *suite's*
# discoverability.
#
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-27)
# Memo: .lovable/memory/audit/v2-deterministic/phase-102-readme-inventory-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
README="$SCRIPT_DIR/README.md"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

[ -f "$README" ] || { echo "❌ README not found: $README"; exit 2; }

cd "$REPO_ROOT"
PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then echo "✅ $label"; PASS=$((PASS+1))
  else          echo "❌ $label"; FAIL=$((FAIL+1)); fi
}

# ── Build the two sets ───────────────────────────────────────────
# Filesystem set: every executable test-*.sh in the directory (exclude this
# script itself? — no, this script IS test-readme-inventory.sh and SHOULD be
# in the README inventory once it's wired in).
FS_SCRIPTS=$(cd "$SCRIPT_DIR" && ls test-*.sh 2>/dev/null | sort)

# README set: extract filenames from markdown links in the inventory table.
# Pattern: [`test-foo.sh`](./test-foo.sh)
README_SCRIPTS=$(grep -oE '\(\./test-[a-z0-9-]+\.sh\)' "$README" \
  | sed -E 's|^\(\./||; s|\)$||' | sort -u)

# ── Set parity ───────────────────────────────────────────────────
MISSING_FROM_README=$(comm -23 <(echo "$FS_SCRIPTS") <(echo "$README_SCRIPTS"))
EXTRA_IN_README=$(comm -13 <(echo "$FS_SCRIPTS") <(echo "$README_SCRIPTS"))

assert "every test-*.sh on disk appears in README inventory" \
  test -z "$MISSING_FROM_README"
if [ -n "$MISSING_FROM_README" ]; then
  echo "    Missing from README: $MISSING_FROM_README"
fi

assert "every test-*.sh in README inventory exists on disk" \
  test -z "$EXTRA_IN_README"
if [ -n "$EXTRA_IN_README" ]; then
  echo "    Listed in README but missing on disk: $EXTRA_IN_README"
fi

# ── Per-script README contract ───────────────────────────────────
for script in $FS_SCRIPTS; do
  # Each script must be linked at least once via `[`name`](./name)` (inventory
  # table entry).
  assert "README links to ./$script" \
    grep -qF "[\`$script\`](./$script)" "$README"

  # Each script on disk must be executable (chmod +x is in the template).
  assert "$script is executable" \
    test -x "$SCRIPT_DIR/$script"
done

# ── Structural sections required by AC-31-27 ─────────────────────
assert "README has 'Test inventory' section" \
  grep -qE '^## Test inventory' "$README"

assert "README has 'Coverage triad' section" \
  grep -qE '^## Coverage triad' "$README"

assert "README has 'Adding a new self-test' section" \
  grep -qE '^## Adding a new self-test' "$README"

assert "README has 'Last updated:' line" \
  grep -qE '^\*\*Last updated:\*\*' "$README"

# ── Summary ──────────────────────────────────────────────────────
echo "======================================="
echo "Filesystem: $(echo "$FS_SCRIPTS" | wc -w | tr -d ' ') test-*.sh"
echo "README:     $(echo "$README_SCRIPTS" | wc -w | tr -d ' ') inventory entries"
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
echo "✅ README inventory ↔ filesystem parity intact (AC-31-27)."

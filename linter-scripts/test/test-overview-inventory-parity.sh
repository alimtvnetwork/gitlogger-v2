#!/usr/bin/env bash
# linter-scripts/test/test-overview-inventory-parity.sh
#
# Phase 112 — §27 inventory parity triangle: `00-overview.md` ↔ filesystem ↔
# Phase 107 audit memo.
#
# Locks: AC-31-31 (Phase 109 — multi-file enumeration parity contract).
# The §27 inventory enumeration is restated across 3 documentation/code sites:
#   1. spec/27-spec-toolchain/00-overview.md           (the canonical tables §38–§111)
#   2. linter-scripts/ + .github/workflows/            (the filesystem truth)
#   3. .lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md
#                                                      (the orphan-tracking memo)
#
# Without this self-test, the AC-31-31 obligation is enforced only by reviewer
# attention. A contributor adding a new script (e.g. `check-foo.py`) without
# updating §27 §00-overview AND the Phase 107 memo's "production orphans" list
# would not fail any gate — exactly the drift Phase 107 documented.
#
# This test asserts the bijection invariant INV-01 ("every code file MUST have
# exactly one spec section") at the documentation level: the §27 overview's
# code-artifact column MUST be a superset of the on-disk script set, and any
# on-disk file NOT listed in §27 MUST appear in the Phase 107 orphan ledger.
#
# Spec: spec/27-spec-toolchain/00-overview.md (Inventory section)
# Spec: spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md (AC-31-31)
# Memo: .lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md
# Memo: .lovable/memory/audit/v2-deterministic/phase-112-overview-inventory-parity-test.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OVERVIEW="$REPO_ROOT/spec/27-spec-toolchain/00-overview.md"
ORPHAN_MEMO="$REPO_ROOT/.lovable/memory/audit/v2-deterministic/phase-107-overview-inventory-drift-audit.md"

[ -f "$OVERVIEW" ] || { echo "❌ overview not found: $OVERVIEW"; exit 2; }
[ -f "$ORPHAN_MEMO" ] || { echo "❌ orphan memo not found: $ORPHAN_MEMO"; exit 2; }

cd "$REPO_ROOT"
PASS=0
FAIL=0

assert() {
  local label="$1"; shift
  if "$@"; then echo "✅ $label"; PASS=$((PASS+1))
  else          echo "❌ $label"; FAIL=$((FAIL+1)); fi
}

# ── Build the three sets ─────────────────────────────────────────
# (1) Filesystem: every executable artifact under linter-scripts/ (top level)
#     plus every workflow under .github/workflows/. Excludes:
#       - linter-scripts/test/  (covered by Phase 102 README inventory parity)
#       - data files .toml / .allowlist / .md  (specced as §60-69 config rows)
#     Excluded extensions are rechecked separately via the §60-69 contract.
FS_SCRIPTS=$(
  {
    find linter-scripts -maxdepth 1 -type f \
      \( -name '*.py' -o -name '*.cjs' -o -name '*.mjs' -o -name '*.sh' \
         -o -name '*.ps1' -o -name '*.go' \) \
      -printf '%P\n' \
      | sed 's|^|linter-scripts/|'
    find .github/workflows -maxdepth 1 -type f -name '*.yml' \
      -printf '%P\n' \
      | sed 's|^|.github/workflows/|'
  } | sort -u
)

# (2) Overview: every backticked code path in the §27 overview tables.
#     Pattern: `linter-scripts/...` or `.github/workflows/...`.
#     Strip the surrounding backticks, dedupe, sort.
OVERVIEW_SCRIPTS=$(
  grep -oE '`(linter-scripts/[a-zA-Z0-9_.-]+|\.github/workflows/[a-zA-Z0-9_.-]+\.yml)`' "$OVERVIEW" \
    | tr -d '`' \
    | grep -vE '\.toml$|\.allowlist$|\.md$' \
    | sort -u
)

# (3) Orphan memo: every backticked code path mentioned. The memo's role is to
#     enumerate KNOWN orphans (code files NOT in the overview); we use it as
#     the legitimate-exemption ledger.
ORPHAN_SCRIPTS=$(
  grep -oE '`(linter-scripts/[a-zA-Z0-9_./-]+|\.github/workflows/[a-zA-Z0-9_.-]+\.yml)`' "$ORPHAN_MEMO" \
    | tr -d '`' \
    | grep -vE '/test/|\.toml$|\.allowlist$|\.md$' \
    | sort -u
)

# ── Triangle parity: (FS) ⊆ (OVERVIEW ∪ ORPHAN_MEMO) ─────────────
# Every on-disk script MUST either be in §27 §00-overview OR be acknowledged
# as a known orphan in the Phase 107 memo. A script in NEITHER is a
# bijection violation that escaped reviewer attention.
KNOWN=$(printf '%s\n%s\n' "$OVERVIEW_SCRIPTS" "$ORPHAN_SCRIPTS" | sort -u)
UNTRACKED=$(comm -23 <(echo "$FS_SCRIPTS") <(echo "$KNOWN"))

assert "every on-disk script is tracked in §27 overview OR Phase 107 orphan memo (INV-01)" \
  test -z "$UNTRACKED"
if [ -n "$UNTRACKED" ]; then
  echo "    Untracked code files (drift since Phase 107):"
  echo "$UNTRACKED" | sed 's|^|      - |'
  echo "    Resolution: either add a §27 NN-*.md spec row OR add to the"
  echo "    orphan ledger at .lovable/memory/audit/v2-deterministic/phase-107-*.md"
fi

# ── Triangle parity: (OVERVIEW) ⊆ (FS) ───────────────────────────
# Every script the overview claims to spec MUST exist on disk. A "ghost spec"
# (overview row pointing at a non-existent file) is FAIL-02 from the
# Normative Contract.
GHOST_SPECS=$(comm -23 <(echo "$OVERVIEW_SCRIPTS") <(echo "$FS_SCRIPTS"))

assert "every code path listed in §27 overview exists on disk (INV-02)" \
  test -z "$GHOST_SPECS"
if [ -n "$GHOST_SPECS" ]; then
  echo "    Ghost-spec code paths (overview lists, disk lacks):"
  echo "$GHOST_SPECS" | sed 's|^|      - |'
fi

# ── Phase 107 memo health: orphans listed MUST still exist on disk ──
# If a file in the orphan memo no longer exists, the memo is stale and
# either the file was removed (good — remove from memo) or the path is wrong.
STALE_ORPHANS=$(comm -23 <(echo "$ORPHAN_SCRIPTS") <(echo "$FS_SCRIPTS"))

assert "every orphan path in Phase 107 memo still exists on disk" \
  test -z "$STALE_ORPHANS"
if [ -n "$STALE_ORPHANS" ]; then
  echo "    Stale orphan-memo entries (memo lists, disk lacks):"
  echo "$STALE_ORPHANS" | sed 's|^|      - |'
fi

# ── Structural anchors ───────────────────────────────────────────
assert "§27 overview has 'Inventory' H2 section" \
  grep -qE '^## Inventory' "$OVERVIEW"

assert "§27 overview has 'Normative Contract' block (INV-01/INV-02 source)" \
  grep -qF "INV-01: forall code in {linter-scripts/, .github/workflows/}" "$OVERVIEW"

assert "Phase 107 memo references AC-31-31 OR INV-01 anchor" \
  grep -qE 'AC-31-31|INV-01' "$ORPHAN_MEMO"

# ── Summary ──────────────────────────────────────────────────────
echo "======================================="
echo "Filesystem:    $(echo "$FS_SCRIPTS" | wc -l | tr -d ' ') executable artifacts"
echo "§27 overview:  $(echo "$OVERVIEW_SCRIPTS" | wc -l | tr -d ' ') tracked code paths"
echo "Phase 107:     $(echo "$ORPHAN_SCRIPTS" | wc -l | tr -d ' ') known orphans"
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
echo "✅ §27 inventory parity triangle intact (AC-31-31, INV-01/INV-02)."

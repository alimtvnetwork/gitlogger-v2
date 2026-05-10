#!/usr/bin/env bash
# test-check-truncated-prose.sh — Phase P47-followup-1 self-test
# Exercises detection of unclosed fences and mid-sentence endings.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$ROOT/linter-scripts/check-truncated-prose.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

assert() { if ! eval "$1"; then echo "ASSERT FAIL: $2"; exit 1; fi; }

# Fixture A: clean file (terminator)
mkdir -p "$TMP/a"
cat > "$TMP/a/00-overview.md" <<'EOF'
# Title
This is a complete sentence.
EOF

# Fixture B: clean structural ending (table)
mkdir -p "$TMP/b"
cat > "$TMP/b/00-overview.md" <<'EOF'
# Title
| col |
|---|
| val |
EOF

# Fixture C: unclosed fence
mkdir -p "$TMP/c"
cat > "$TMP/c/00-overview.md" <<'EOF'
# Title
```bash
echo hi
EOF

# Fixture D: mid-sentence ending
mkdir -p "$TMP/d"
cat > "$TMP/d/00-overview.md" <<'EOF'
# Title
This sentence is incomplete and just trails off
EOF

# Run on clean fixtures (a + b only)
mkdir -p "$TMP/clean/a" "$TMP/clean/b"
cp "$TMP/a/00-overview.md" "$TMP/clean/a/"
cp "$TMP/b/00-overview.md" "$TMP/clean/b/"
if ! python3 "$SCRIPT" --root "$TMP/clean" >/dev/null 2>&1; then
  echo "ASSERT FAIL: clean fixtures should pass"; exit 1
fi

# Run on dirty fixtures (c + d) — must fail with both flagged
mkdir -p "$TMP/dirty/c" "$TMP/dirty/d"
cp "$TMP/c/00-overview.md" "$TMP/dirty/c/"
cp "$TMP/d/00-overview.md" "$TMP/dirty/d/"
OUT="$(python3 "$SCRIPT" --root "$TMP/dirty" 2>&1 || true)"
RC=$(python3 "$SCRIPT" --root "$TMP/dirty" >/dev/null 2>&1; echo $?)
assert "[ $RC -eq 1 ]" "dirty fixtures should exit 1 (got $RC)"
assert "echo \"\$OUT\" | grep -q 'unclosed code fence'" "should flag unclosed fence"
assert "echo \"\$OUT\" | grep -q 'mid-sentence'" "should flag mid-sentence"

# Real-tree gate: live spec/ MUST be clean (proves Phase P47-followup-1 fix landed)
if ! python3 "$SCRIPT" --root "$ROOT/spec" >/dev/null 2>&1; then
  echo "ASSERT FAIL: live spec/ has truncation drift"
  python3 "$SCRIPT" --root "$ROOT/spec" || true
  exit 1
fi

echo "test-check-truncated-prose: OK (5 assertions)"

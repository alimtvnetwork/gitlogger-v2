#!/usr/bin/env bash
# test-check-forbidden-strings.sh — Phase G3 self-test
# Exercises check-forbidden-strings.py against synthetic fixtures + live tree.
# Contract: exits 0 iff (clean fixture passes) ∧ (dirty fixture fails) ∧ (live spec/ + linter-scripts/ clean).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$ROOT/linter-scripts/check-forbidden-strings.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

assert() { if ! eval "$1"; then echo "ASSERT FAIL: $2"; exit 1; fi; }

# ------------------------------------------------------------------
# Fixture: minimal TOML rule set + a script that drops the script's own
# config path beside it (the script reads forbidden-strings.toml from
# its own dirname).
# ------------------------------------------------------------------
mkdir -p "$TMP/clean/linter-scripts" "$TMP/dirty/linter-scripts"
cp "$SCRIPT" "$TMP/clean/linter-scripts/"
cp "$SCRIPT" "$TMP/dirty/linter-scripts/"

cat > "$TMP/clean/linter-scripts/forbidden-strings.toml" <<'EOF'
[[rule]]
id = "FORBID-FOO"
description = "FOO must not appear"
pattern = "FORBIDDEN_TOKEN_FOO"
fix_hint = "Remove FORBIDDEN_TOKEN_FOO."
exclude_dirs = []
exclude_files = ["forbidden-strings.toml", "check-forbidden-strings.py"]
allowlist = []
EOF
cp "$TMP/clean/linter-scripts/forbidden-strings.toml" "$TMP/dirty/linter-scripts/"

# Clean tree — no offending file
cat > "$TMP/clean/hello.md" <<'EOF'
all good here
EOF

# Dirty tree — contains the forbidden token
cat > "$TMP/dirty/hello.md" <<'EOF'
this line has FORBIDDEN_TOKEN_FOO in it
EOF

# ------------------------------------------------------------------
# Assertion 1: clean fixture exits 0
# ------------------------------------------------------------------
RC=$( cd "$TMP/clean" && (python3 linter-scripts/check-forbidden-strings.py >/dev/null 2>&1; echo $?) )
assert "[ $RC -eq 0 ]" "clean fixture should exit 0 (got $RC)"

# ------------------------------------------------------------------
# Assertion 2: dirty fixture exits 1 with finding output
# ------------------------------------------------------------------
OUT="$(cd "$TMP/dirty" && python3 linter-scripts/check-forbidden-strings.py 2>&1 || true)"
RC=$( cd "$TMP/dirty" && (python3 linter-scripts/check-forbidden-strings.py >/dev/null 2>&1; echo $?) )
assert "[ $RC -eq 1 ]" "dirty fixture should exit 1 (got $RC)"
assert "echo \"\$OUT\" | grep -q 'FORBID-FOO'" "should name the failing rule id"
assert "echo \"\$OUT\" | grep -q 'FORBIDDEN_TOKEN_FOO'" "should echo the offending line"
assert "echo \"\$OUT\" | grep -q 'Fix hint'" "should print fix hint"

# ------------------------------------------------------------------
# Assertion 3: allowlist suppresses a finding
# ------------------------------------------------------------------
cat > "$TMP/dirty/linter-scripts/forbidden-strings.toml" <<'EOF'
[[rule]]
id = "FORBID-FOO"
description = "FOO must not appear"
pattern = "FORBIDDEN_TOKEN_FOO"
fix_hint = "Remove FORBIDDEN_TOKEN_FOO."
exclude_dirs = []
exclude_files = ["forbidden-strings.toml", "check-forbidden-strings.py"]
allowlist = ["hello.md"]
EOF
RC=$( cd "$TMP/dirty" && (python3 linter-scripts/check-forbidden-strings.py >/dev/null 2>&1; echo $?) )
assert "[ $RC -eq 0 ]" "allowlisted file should suppress finding (got $RC)"

# ------------------------------------------------------------------
# Assertion 4: empty config (no [[rule]]) exits 0 with warning
# ------------------------------------------------------------------
echo "" > "$TMP/dirty/linter-scripts/forbidden-strings.toml"
WARN_OUT="$(cd "$TMP/dirty" && python3 linter-scripts/check-forbidden-strings.py 2>&1 || true)"
assert "echo \"\$WARN_OUT\" | grep -q 'No \\[\\[rule\\]\\] entries'" "empty config should warn"

# ------------------------------------------------------------------
# Assertion 5: real-tree gate — live repo MUST be clean.
# ------------------------------------------------------------------
LIVE_RC=$( cd "$ROOT" && (python3 linter-scripts/check-forbidden-strings.py >/dev/null 2>&1; echo $?) )
assert "[ $LIVE_RC -eq 0 ]" "live repo has forbidden-strings drift (rc=$LIVE_RC)"

echo "test-check-forbidden-strings: OK (6 assertions)"

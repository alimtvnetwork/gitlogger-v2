#!/usr/bin/env bash
# linter-scripts/test/test-inline-code-blanking-parity.sh
#
# Phase P45 — JS↔Python inline-code blanking parity self-test.
#
# Locks: AC-11-05 (Phase P44 — dual-implementation parity contract).
#
# The cross-link validation contract is implemented in TWO sites:
#   1. linter-scripts/check-spec-cross-links.py   (strict CI gate)
#        helper: strip_inline_code()  + _INLINE_CODE_RE
#   2. linter-scripts/generate-dashboard-data.cjs (dashboard Health.LegacyScore)
#        helper: blankInlineCode()    + INLINE_CODE_RE
#
# Both MUST produce byte-identical output for any input line so the dashboard
# `Links.Total.Broken` counter and the strict gate's broken-link enumeration
# agree (the P44 root-cause was a 22-phase divergence: JS lacked inline-code
# stripping, so `` [`foo`](./foo) `` example patterns were over-counted).
#
# This test invokes both helpers on a shared fixture corpus and asserts the
# outputs match exactly — char-offset-preserving (line numbers must stay
# accurate post-blanking, per AC-11-05's "same-length space runs" clause).
#
# Spec: spec/27-spec-toolchain/11-generate-dashboard-data.md (AC-11-05)
# Spec: spec/27-spec-toolchain/01-check-spec-cross-links.md
# Memo: P44 closure entry in .lovable/memory/index.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINTER_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PASS=0
FAIL=0

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    PASS=$((PASS + 1))
    echo "  ✓ ${label}"
  else
    FAIL=$((FAIL + 1))
    echo "  ✗ ${label}"
    echo "    expected: $(printf '%q' "$expected")"
    echo "    actual:   $(printf '%q' "$actual")"
  fi
}

# ── Fixture corpus ──────────────────────────────────────────────────────────
# Each line probes a distinct inline-code edge case from the helper contract.
FIXTURES=(
  # 1. The P44 root-cause pattern: inline-code wrapping a markdown link target
  '[`./test-foo.sh`](./test-foo.sh)'
  # 2. Bare inline code, no link
  'see `npm install` for setup'
  # 3. Multi-backtick fence (allows literal backtick inside)
  'use ``code with ` inside`` here'
  # 4. Multiple inline-code spans on one line
  '`foo` and `bar` and `baz`'
  # 5. No inline code at all (must round-trip identically)
  'plain prose with no code spans'
  # 6. Inline code adjacent to a real link (link must remain extractable)
  '`example` and [real](./real.md)'
  # 7. Empty input
  ''
  # 8. Triple-backtick INLINE (rare but valid per CommonMark)
  '```triple``` inline'
)

# ── Python helper invocation ────────────────────────────────────────────────
py_blank() {
  python3 -c '
import sys, importlib.util
spec = importlib.util.spec_from_file_location("ccl", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for line in sys.stdin.read().split("\n"):
    sys.stdout.write(mod.strip_inline_code(line) + "\n")
' "${LINTER_DIR}/check-spec-cross-links.py"
}

# ── JS helper invocation ────────────────────────────────────────────────────
js_blank() {
  node -e '
const path = require("path");
const fs = require("fs");
const src = fs.readFileSync(path.join(process.argv[1], "generate-dashboard-data.cjs"), "utf8");
// Extract the two helper definitions verbatim and eval in an isolated scope.
const reMatch = src.match(/const INLINE_CODE_RE = [^;]+;/);
const fnMatch = src.match(/function blankInlineCode\([^)]*\) \{[^}]+\}/);
if (!reMatch || !fnMatch) { console.error("helper extraction failed"); process.exit(2); }
eval(reMatch[0] + "\n" + fnMatch[0]);
let buf = "";
process.stdin.on("data", (c) => buf += c);
process.stdin.on("end", () => {
  for (const line of buf.split("\n")) process.stdout.write(blankInlineCode(line) + "\n");
});
' "${LINTER_DIR}"
}

echo "Inline-code blanking parity (JS ↔ Python)"
echo "─────────────────────────────────────────"

for fixture in "${FIXTURES[@]}"; do
  py_out=$(printf '%s' "$fixture" | py_blank)
  js_out=$(printf '%s' "$fixture" | js_blank)
  # Trim trailing newline from both (each emits exactly one)
  py_out="${py_out%$'\n'}"
  js_out="${js_out%$'\n'}"
  assert_eq "fixture: $(printf '%q' "$fixture")" "$py_out" "$js_out"

  # AC-11-05 invariant: output length MUST equal input length (char offsets
  # preserved so line numbers stay accurate).
  in_len=${#fixture}
  out_len=${#py_out}
  if [[ "$in_len" -eq "$out_len" ]]; then
    PASS=$((PASS + 1))
    echo "    ✓ length-preserved (${in_len} chars)"
  else
    FAIL=$((FAIL + 1))
    echo "    ✗ length drift: in=${in_len} out=${out_len}"
  fi
done

# ── Floor assertion: probe count MUST stay ≥ 8 (mirrors H7 AC-28-04) ───────
if [[ "${#FIXTURES[@]}" -ge 8 ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ fixture floor ≥ 8 (have ${#FIXTURES[@]})"
else
  FAIL=$((FAIL + 1))
  echo "  ✗ fixture floor regression: have ${#FIXTURES[@]}, need ≥ 8"
fi

echo "─────────────────────────────────────────"
echo "PASS: ${PASS}    FAIL: ${FAIL}"
[[ "$FAIL" -eq 0 ]] || exit 1

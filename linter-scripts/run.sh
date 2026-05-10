#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# run.sh — Pull latest changes and run the coding guidelines validator
#
# Usage:
#   ./scripts/run.sh                          # scan src/ (default)
#   ./scripts/run.sh -d                       # git pull only, skip validation
#   ./scripts/run.sh --path cmd --max-lines 20
#   ./scripts/run.sh --json
# ──────────────────────────────────────────────────────────────────────

set -euo pipefail

SCAN_PATH="src"
MAX_LINES=15
JSON_FLAG=""
SKIP_VALIDATION=false

# ── Parse args ─────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d)          SKIP_VALIDATION=true; shift ;;
    --path)      SCAN_PATH="$2"; shift 2 ;;
    --max-lines) MAX_LINES="$2"; shift 2 ;;
    --json)      JSON_FLAG="--json"; shift ;;
    -h|--help)
      echo "Usage: $0 [-d] [--path <dir>] [--max-lines <n>] [--json]"
      echo "  -d    Skip validation (git pull only)"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GO_FILE="$SCRIPT_DIR/validate-guidelines.go"

# ── Step 1: Git Pull ──────────────────────────────────────────────
echo ""
echo "═══ Step 1 — git pull ═══"
if git pull; then
  echo "✅ Repository up to date."
else
  echo "⚠️  git pull failed — continuing with local files..."
fi

# ── Skip validation if -d flag ────────────────────────────────────
if [ "$SKIP_VALIDATION" = true ]; then
  echo ""
  echo "⏭️  Skipping validation (-d flag)."
  exit 0
fi

# ── Step 2: Run Go Validator ──────────────────────────────────────
echo ""
echo "═══ Step 2 — Running coding guidelines validator ═══"

if [ ! -f "$GO_FILE" ]; then
  echo "❌ Cannot find $GO_FILE"
  exit 1
fi

if ! command -v go &>/dev/null; then
  echo "❌ Go is not installed or not in PATH."
  echo "   Install from https://go.dev/dl/"
  exit 1
fi

echo "Using $(go version)"
echo "Scanning: $SCAN_PATH (max $MAX_LINES lines/function)"
echo ""

if go run "$GO_FILE" --path "$SCAN_PATH" --max-lines "$MAX_LINES" $JSON_FLAG; then
  echo ""
  echo "✅ Validation passed!"
else
  EXIT_CODE=$?
  echo ""
  echo "❌ Validation failed with CODE RED violations."
  exit $EXIT_CODE
fi

# ── Step 3: Self-heal missing required & recommended files ───────
echo ""
echo "═══ Step 3 — Filling missing consistency reports, AC, and changelogs ═══"
if command -v node &>/dev/null; then
  [ -f "$SCRIPT_DIR/fill-missing-consistency-reports.cjs" ] && node "$SCRIPT_DIR/fill-missing-consistency-reports.cjs"
  [ -f "$SCRIPT_DIR/fill-missing-acceptance-criteria.cjs" ] && node "$SCRIPT_DIR/fill-missing-acceptance-criteria.cjs"
  [ -f "$SCRIPT_DIR/fill-missing-changelogs.cjs" ] && node "$SCRIPT_DIR/fill-missing-changelogs.cjs"
else
  echo "⏭️  Skipped (node not installed)."
fi

# ── Step 4: Regenerate spec-index.md ──────────────────────────────
echo ""
echo "═══ Step 4 — Regenerating spec-index.md ═══"
if command -v node &>/dev/null && [ -f "$SCRIPT_DIR/generate-spec-index.cjs" ]; then
  node "$SCRIPT_DIR/generate-spec-index.cjs"
else
  echo "⏭️  Skipped (node not installed or script missing)."
fi

# ── Step 5: Spec tree health gate ─────────────────────────────────
echo ""
echo "═══ Step 5 — Spec tree health gate ═══"
HEALTH_MIN="${SPEC_HEALTH_MIN:-100}"
if command -v node &>/dev/null && [ -f "$SCRIPT_DIR/check-tree-health.cjs" ]; then
  if node "$SCRIPT_DIR/check-tree-health.cjs" --min="$HEALTH_MIN"; then
    echo "✅ Spec tree health gate passed."
  else
    echo "❌ Spec tree health below threshold $HEALTH_MIN."
    exit 1
  fi
else
  echo "⏭️  Skipped (node not installed or script missing)."
fi

# ── Step 6: Mermaid diagram syntax gate (Phase 97) ────────────────
echo ""
echo "═══ Step 6 — Mermaid diagram syntax gate ═══"
if command -v node &>/dev/null && [ -f "$SCRIPT_DIR/check-mermaid-syntax.mjs" ]; then
  if node "$SCRIPT_DIR/check-mermaid-syntax.mjs"; then
    echo "✅ Mermaid syntax gate passed."
  else
    echo "❌ Mermaid syntax errors found in spec/**/*.mmd."
    exit 1
  fi
else
  echo "⏭️  Skipped (node not installed or script missing)."
fi


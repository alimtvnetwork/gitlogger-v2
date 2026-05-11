#!/usr/bin/env bash
# E2E + load smoke harness for glci ↔ git-logs plugin.
# Requires: WP_BASE_URL, WP_TEMP_TOKEN env vars pointing at a live test site.
set -euo pipefail

BASE="${WP_BASE_URL:?set WP_BASE_URL}"
TOKEN="${WP_TEMP_TOKEN:?set WP_TEMP_TOKEN}"
GLCI="${GLCI:-./glci/glci}"

echo "==> health"
curl -fsS "$BASE/wp-json/git-logs/v1/health" >/dev/null

echo "==> whoami"
"$GLCI" whoami --server "$BASE/wp-json/git-logs/v1" --temp-token "$TOKEN"

echo "==> doctor"
"$GLCI" doctor --cwd .

echo "==> single batched ship (no-op test phase)"
"$GLCI" run --cwd . --server "$BASE/wp-json/git-logs/v1" \
  --temp-token "$TOKEN" --phases test --json

echo "==> streaming mode"
"$GLCI" run --cwd . --server "$BASE/wp-json/git-logs/v1" \
  --temp-token "$TOKEN" --phases test --stream --json

echo "==> load: 20 parallel batched ships"
for i in $(seq 1 20); do
  "$GLCI" run --cwd . --server "$BASE/wp-json/git-logs/v1" \
    --temp-token "$TOKEN" --phases test --json &
done
wait

echo "OK — e2e smoke + load passed"

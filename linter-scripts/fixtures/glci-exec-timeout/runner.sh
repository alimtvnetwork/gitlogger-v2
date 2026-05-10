#!/usr/bin/env bash
# Fixture runner for T-28-30 (GLCI-EXEC-TIMEOUT).
# Sleeps far past any sane phase cap to force the wall-clock timeout path.
set -eu
echo '{"frame":1,"phase":"ts-test","status":"running"}'
sleep 600
echo '{"frame":2,"phase":"ts-test","status":"done"}'

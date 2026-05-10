#!/usr/bin/env bash
# Fixture runner for T-28-29 (GLCI-EXEC-RUNNER-CRASHED).
# Prints one progress frame, then SIGKILLs itself to simulate an
# uncatchable runner crash mid-phase.
set -eu
echo '{"frame":1,"phase":"ts-test","status":"running"}'
sleep 0.05
kill -9 $$
# unreachable
echo '{"frame":2,"phase":"ts-test","status":"done"}'

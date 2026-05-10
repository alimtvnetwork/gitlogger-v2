#!/usr/bin/env bash
# Fixture runner for T-28-36 (stream buffer overflow → drop-oldest + audit).
# Emits 50 000 NDJSON frames as fast as possible to overflow a 1024-frame cap.
set -eu
i=0
while [ "$i" -lt 50000 ]; do
  printf '{"frame":%d,"phase":"ts-test","status":"running"}\n' "$i"
  i=$((i + 1))
done
printf '{"frame":%d,"phase":"ts-test","status":"done"}\n' "$i"

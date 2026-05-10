# Fixture: glci-stream-buffer-overflow

**Owner:** spec/28-universal-ci-cli §97 **T-28-36** → **AC-28-36**
(streaming buffer cap drops oldest frames + audit log line, exit 0).

Synthetic fixture proving the §28 CLI honors `--buffer-cap=N` by dropping
the OLDEST frames when the runner emits faster than the sink consumes,
surfacing `BufferDroppedCount` in the final summary AND writing a single
audit line to stderr — and crucially, exiting `0` (drops are non-fatal).

## Files

- `runner.sh` — emits 50 000 NDJSON frames as fast as the kernel allows.
- `expected.json` — load-evidence contract.

## How to use

```
glci ts-test --fixture linter-scripts/fixtures/glci-stream-buffer-overflow/ \
             --stream --buffer-cap=1024
```

Expected:
- `BufferDroppedCount > 0` in final summary (stream-end OR batched fallback).
- Stderr contains exactly one line matching:
  `audit: dropped <N> oldest frames (buffer cap=1024)`
- exit code = `0`.

## Failure modes detected

- Drops silently (no `BufferDroppedCount`, no audit line) → observability gap.
- Exits non-zero on overflow (drop is normative non-fatal per AC-28-36).
- Drops NEWEST instead of OLDEST (wrong eviction policy).
- Emits the audit line per-drop (log-flooding) instead of one summary line.

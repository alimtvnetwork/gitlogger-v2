---
name: phase-tracker
description: Implementation phase progress and post-P8 backlog
type: feature
---
# Implementation Phase Tracker

## Phases
- P1–P8: ✅ all done

## Post-P8 Backlog
- #1 Lane B wire-up + SSHSIG verifier — ✅ done
- #2 Live integration test against hosted WP — ⏳ blocked (needs test WP URL + bootstrap token)
- #3 Codecov + golangci-lint CI badges — ✅ done
- #4 Starter Go unit tests — ✅ done
- #5 Expanded Go coverage (config/detect/ci/ship) — ✅ done
- #6 PHP plugin PHPUnit-lite harness (auth surface) — ✅ done
- #7 Go CLI/runner harness (runner/selftest/laneb/selfupdate) — ✅ done
- #8 REST controller PHP harness — ✅ done (48 tests, 106 assertions)
- #9 DB layer tests — wpdb shim for RepoStore/RunStore/EventStore/AuditLog/SHA-index/MigrationRunner — ⏳ todo (next default)
- #10 Admin UI E2E (Playwright) for the WP admin React/HTML page — ⏳ todo
- #11 Glci end-to-end harness: spawn `glci ship/selftest` against a stub WP server — ⏳ todo

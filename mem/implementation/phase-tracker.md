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
- #7 Go CLI/runner harness — ✅ done
- #8 REST controller PHP harness — ✅ done (48 tests, 106 assertions)
- #9 DB-layer tests with real PDO/SQLite — ✅ done (41 tests, 115 assertions)
- #10 Admin UI E2E (Playwright) — ✅ scaffolded; runs in CI via Playwright Docker image (sandbox lacks browser deps for local exec)
- #11 Glci end-to-end harness: spawn compiled `glci` against an httptest stub WP server — ✅ done (TestMain go-build + 7 exec tests covering version/help/ping/whoami/--self-test)
- #12 Per-package Go coverage gates in `ci-glci.yml` — ✅ done (`scripts/coverage-gate.sh`, statement-weighted, 10 packages gated)
- #13 Verify Playwright suite by triggering CI workflow once user pushes; fix any environmental issues that surface there — ⏳ followup
- #14 Cover the `cmd` dispatcher (`CodeOf`, `Run`, `filterOut`, `contains`, `exitCode`) — ✅ done (cmd_test.go, gate floor 15%)
- #15 Quickstart docs (`glci/README.md` + `git-logs-plugin/README.md`) — ✅ done

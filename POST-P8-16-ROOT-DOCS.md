# POST-P8 #16 — Top-level README + CONTRIBUTING

## Goal
Tie both halves of the repo together with a shared on-ramp and a contributor guide.

## Files
- `README.md` — overview diagram, repo layout map, quickstart pointing into the per-half READMEs, status link to the phase tracker.
- `CONTRIBUTING.md` — ground rules (specs are the contract, tests required, two auth lanes only), dev loops for `glci` / WP plugin / admin UI, CI workflow table, PR checklist, release-tag conventions.

## Verification
- Pure docs.
- All cross-links resolve to real paths in the repo (`glci/README.md`, `git-logs-plugin/README.md`, `mem/implementation/phase-tracker.md`, `.github/workflows/*.yml`, spec/22..28/).

## Notes
PR checklist mirrors what the phase-tracker workflow already enforces (acceptance MD per task) so contributors can self-verify before opening a PR.

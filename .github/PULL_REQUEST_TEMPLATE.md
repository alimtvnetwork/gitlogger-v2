<!-- Thanks for the contribution! Fill out what applies. -->

## What

<!-- One-paragraph summary. -->

## Why

<!-- The user-visible problem this solves, or the spec section this implements. -->

## Component

- [ ] glci (Go CLI)
- [ ] WordPress plugin
- [ ] Admin UI (React)
- [ ] Specs / docs / CI

## Spec link

<!-- e.g. spec/28 §06 R2. Required if this changes the wire contract. -->

## Checklist

- [ ] Unit tests added/updated and passing locally
- [ ] Coverage gate passes (`bash glci/scripts/coverage-gate.sh glci/coverage.out`) for Go changes
- [ ] `bun x tsc --noEmit` clean for admin-ui changes
- [ ] PHPUnit-lite suites pass for plugin changes (`php tests/run.php`, `php tests/run-db.php`)
- [ ] Acceptance note added (`POST-P8-N-*.md`) and `mem/implementation/phase-tracker.md` updated when closing a backlog item
- [ ] No silent divergence from spec/22..28/ (see CONTRIBUTING.md)

## Notes for reviewers

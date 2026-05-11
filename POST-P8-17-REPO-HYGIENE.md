# POST-P8 #17 — Repo hygiene: LICENSE + GitHub templates

## Goal
Make the repo look and behave like a proper open-source project.

## Files
- `LICENSE` — full GPL-2.0 text fetched from gnu.org. Matches the license declared in both READMEs and the WP plugin header.
- `.github/ISSUE_TEMPLATE/bug.yml` — structured bug report (component dropdown, version, repro, expected/actual, env).
- `.github/ISSUE_TEMPLATE/feature.yml` — feature request with spec-impact checkboxes.
- `.github/ISSUE_TEMPLATE/spec-question.yml` — narrow form for spec/22..28 ambiguities.
- `.github/ISSUE_TEMPLATE/config.yml` — disables blank issues; pushes new reporters to docs.
- `.github/PULL_REQUEST_TEMPLATE.md` — mirrors the CONTRIBUTING.md checklist (component, spec link, coverage/test gates, acceptance-note reminder).

## Verification
- LICENSE is the canonical 338-line GPL-2.0 file from gnu.org.
- Issue forms use GitHub's `name:`/`body:` schema; `config.yml` disables blank issues per GitHub's documented contract.
- PR template's checklist commands are the same ones CI runs.

## Notes
The `contact_links` URL in `config.yml` is a placeholder (`github.com/example/git-logs`) — swap once the canonical repo URL is set.

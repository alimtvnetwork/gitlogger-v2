# POST-P8 #15 — Quickstart docs

## Goal
Give end users a self-contained on-ramp for both halves of Git Logs v2.

## Files
- `glci/README.md` — install (source / binary / self-update), 5-step quickstart (ping → auth → detect → run → doctor), config precedence, exit-code table, dev loop.
- `git-logs-plugin/README.md` — requirements, install (manual + Composer/Bedrock), first-run setup (health → register key → wire CI → view runs), architecture sketch, security notes, dev loop.

## Verification
- Pure docs; no code paths affected.
- Cross-links between the two READMEs and to spec/22..28 for deeper reference.
- Commands referenced (`glci ping`, `glci keys generate`, `glci whoami`, etc.) all match the actual CLI surface in `glci/internal/cmd/`.

## Notes
Release-page URLs use `github.com/example/glci` as a placeholder — swap in the real org/repo once the project is published.

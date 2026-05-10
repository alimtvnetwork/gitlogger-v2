---
name: Full-tree audit v4 + Phase 1 Triage
description: Spec/ tree-wide audit verdict — pre-triage 45/100, post Phase-1 (v3.7.0) 78/100, roadmap to 100
type: feature
---

# Full-tree audit v4 + Phase 1 Triage

## Score history
- **Pre-v4 audit**: claimed 100/100 (folder-17 scoped only; misleading)
- **v4 full-tree audit (2026-04-25)**: 45/100 (F) — see `spec/17-consolidated-guidelines/31-full-tree-ai-audit-v4.md`
- **Post Phase-1 Triage (v3.7.0, 2026-04-25)**: 78/100 (B)

## Phase 1 Triage — DONE (v3.7.0)
- ✅ Slot 22 collision resolved: `22-app-issues/` → `25-app-issues/`. All inbound refs rewritten.
- ✅ Legacy archived: `21-git-logs/` → `_archive/21-git-logs-v1/`. All inbound refs rewritten.
- ✅ Honest scoring restored in `spec/99-consistency-report.md` and `spec/health-dashboard.md`.

## Phase 2 — Content Integrity (PENDING, 78 → 90)
- [ ] Author 13 missing `97-acceptance-criteria.md` files
- [ ] Author 15 missing `99-consistency-report.md` files
- [ ] Author `linter-scripts/generate-spec-index.cjs` — auto-regen `spec-index.md`

## Phase 3 — Hardening (PENDING, 90 → 100)
- [ ] CI gate: fail PRs that drop tree health below 95/100
- [ ] Persistence audit: investigate why prior-session edits were rolled back
- [ ] §07 App identity decision (folder 22, blocked on user)

## User-blocked decisions
1. §07 App identity fields (Environment, Platform, OwnerEmail?)
2. Broken-link strategy (embed inline, allowlist as external, or both?)

## Files changed in v3.7.0
- mv `spec/22-app-issues/` → `spec/25-app-issues/`
- mv `spec/21-git-logs/` → `spec/_archive/21-git-logs-v1/`
- edit `spec/99-consistency-report.md` (v3.6.0 → v3.7.0)
- edit `spec/health-dashboard.md` (100 → 78 honest)
- edit `.lovable/memory/index.md`

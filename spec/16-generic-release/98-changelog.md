# Changelog — Generic Release Pipeline Specification

**Version:** 2.3.0  
**Updated:** 2026-04-30 (Phase 153 Task A11h — AC-21 module asset inventory pin + cross-module link-don't-restate pin (Lesson #29 + Lesson #36); AC count 20 → 21)

### 2.3.0 — 2026-04-30 — Phase 153 Task A11h: AC-21 inventory + cross-module pin
- **Added** AC-21 `[critical]` — combined inventory pin (15-entry §99-authoritative on-disk asset list) + cross-module link-don't-restate pin (`../12/`, `../13/`, `../14/` cross-references are intentional per Lesson #36; restating would create dual-source drift). Classifies audit-v5 D5 HIGH (broken cross-refs), D3 MED (missing concurrency impl — already correctly bound to spec/13 AC-22), D4 MED (incomplete installer templates — deliberate spec-vs-implementation boundary; templates live in consuming repo per AC-15/AC-18) as harness scope / boundary artifacts. Mirror of spec/13 AC-24 + spec/28 AC-28-41 + spec/14 AC-21 + spec/22 AC-78.
- **Why**: per Lesson #29 + #36 — the spec defines normative installer fragments + cross-references; the consuming repo materialises copy-pasteable templates from the fragments. Restating concurrency or templating would create exactly the dual-source drift Lesson #36 forbids.
- **Spec lockstep**: §97 v2.0.0 → **v2.1.0** (AC count 20 → 21); §00 v2.2.1 → **v2.3.0** (h10 stamp 22 → 153); §98 v2.2.1 → **v2.3.0**; §99 v2.2.1 → **v2.3.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
**Scope:** `spec/16-generic-release/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.2.1 — 2026-04-30 (Phase 153 — Lesson #36 cross-ref inoculation)
- **Added** `### Local-tooling concurrency (cross-reference)` subsection under `## Concurrency` in `02-release-pipeline.md` linking local CLI invocations the pipeline shells out to (state-DB writes, asset staging via temp-then-rename) to the canonical concurrency contract at [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md). Pure cross-link — contract NOT restated; CI-job-level concurrency block (`concurrency: group: release-${{ github.ref }}`) untouched. Codifies Lesson #36 (link, never restate). **No §97 AC change**, no AC-31-31 cascade, no RUBRIC bump, no gate-count change. §00 v2.2.0 → v2.2.1; §99 v2.2.0 → v2.2.1. Sibling lockstep: spec/14 (v2.3.1) + spec/28 (v2.1.3) shipped same Lesson #36 inoculation in this phase.

### 2.2.0 — 2026-04-27 (Phase 123 — placeholder catalog)
- **Added** `09-placeholder-tokens.md` v1.0.0 — canonical SoT for 6 install-script placeholder tokens across 2 families (legacy `<NAME>_PLACEHOLDER` + modern `__<NAME>__`). Closes Phase 121 Candidate N — placeholders previously restated across §03/§08/§12/§14/§17 with no canonical catalog. Pre-req for Phase 117 containment harness. Inventory 11 → 12 files.
- **Doc-only — no behavior change.** All 6 tokens already in active use; this catalogues them.
- **P22 sync** (2026-04-28): §00 banner version field bumped 1.1.0 → 2.2.0 to match this release row (H10 §00 ↔ §98 parity catch-up; opt-in `<!-- h10-verified-phase: 22 -->` stamp added under §00 banner; no spec content change).

### 1.1.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Added 2 Go consumer references (Manifest reader + checksums.txt parser) so total Go block count ≥3 → `has_typed_lang_contract` flips true (+10 impl).

### 2.0.0 — 2026-04-26
- **Phase 16d-ii — §97 Depth Pass.** Per `mem://specs/full-tree-audit-v4.md` open backlog item ("deepen scaffolded AC content for high-traffic modules"), expanded `97-acceptance-criteria.md` from 5 generic scaffold ACs to **20 module-specific GWT ACs** (AC-01..AC-05 retained as universal scaffold floor; AC-06..AC-20 added). Each new AC averages 1500-2400 chars with explicit `**Given** / **When** / **Then**` triplet and a `**Verifies:**` cross-ref line. Harmonized with §15 AC-12/13/16/18 — `Verifies:` lines explicitly cite where overlap exists so the contracts stay in lockstep (this is the upstream generic blueprint; §15 is the concrete consumer).
- **Doc-only — no schema bump, no DDL change, no pipeline/installer code changes.** This is a contract clarification, not a behavior change.
- **§97 acceptance-criteria changes (AC-06..AC-20):** (a) **AC-06 Cross-compilation matrix** — 6 minimum target triples (`linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, `windows/amd64`, `windows/arm64`), `CGO_ENABLED=0` static linking enforced (`ldd`/`otool` checks), build-once + tool-version-pin discipline, `.exe` suffix for Windows only, missing target fails workflow before publish; (b) **AC-07 Tag-driven workflow** — triggers ONLY on `v*` tag pushes (no `main` push, no PR, no schedule), pinned to tag's commit SHA not branch HEAD, branch-agnostic, re-tag MUST NOT republish; (c) **AC-08 Atomic publication** — draft → checksum-verify-roundtrip → promote in single API call, verification failure deletes draft, published releases immutable, no auto-publish to package registries (npm/PyPI/Homebrew/Scoop/Chocolatey); (d) **AC-09 Asset naming** — `<binary>-<version>-<os>-<arch>.<ext>` (`.tar.gz` POSIX / `.zip` Windows), flat archive structure, `<version>` includes leading `v`, Go runtime tokens (`linux`/`darwin`/`windows` + `amd64`/`arm64`), `0755` mode, no symlinks; (e) **AC-10 release-metadata.json schema** — required keys `version`/`commit`/`built_at`/`targets`/`assets`, version derived from `${{ github.ref_name }}` via `-ldflags -X main.Version`, `built_at` is workflow start time, `assets` superset of `checksums.txt`, unknown keys allowed for forward-compat; (f) **AC-11 Version-pinned installers** — version embedded as literal constant (NOT `/releases/latest` probe), spec-first ordering (spec download+verify+extract → then binaries), `latest` alias forbidden even as fallback, deterministic re-generation; (g) **AC-12 SHA-256 protocol** — `sha256sum`-compat format (two-space separator, lowercase 64-char hex), every asset checksummed except `checksums.txt` itself, installers MUST verify before extract (supply-chain protection), generic spec doesn't mandate signing tool but allows detached `.sig` asset; (h) **AC-13 Post-install PATH activation** — detect `$SHELL`/`$PROFILE`, idempotent fenced-marker block in rc file OR clear manual-append message, no system-wide changes without `--system`, manual-append exits `0` not `1`, `doctor` sub-command for self-heal; (i) **AC-14 Terminal output discipline** — progress to stderr (stdout for machine-readable only), `NO_COLOR` honored, color suppressed when stderr non-TTY, verbose gated, error context actionable; (j) **AC-15 Known-issues ledger** — `REL-NNN` IDs, RCA + prevention rule REQUIRED in same fix PR, prevention rules promote to sibling specs when generalizable, duplicates link to canonical, reverse-chronological; (k) **AC-16 Mermaid diagrams** — both `.mmd` files parseable by `mermaid-cli`, unified-architecture covers all six referenced specs, re-validate on flow-affecting edit, `.mmd` source under `images/` (NOT embedded fences), `.svg`/`.png` artifacts regen-only-from-`.mmd`; (l) **AC-17 Generic vs concrete separation** — placeholder convention (`<binary>`/`<repo>`/`<version>`/`<module>`) preserved, consumer ACs MUST cite generic ACs, deviations require justification, generic spec stays out of language-specific concerns; (m) **AC-18 Bash+PowerShell installer parity** — functionally equivalent installs, OS-conventional defaults (`$HOME/.local/bin` POSIX vs `$env:LOCALAPPDATA\Programs\<binary>` Windows), shared 6-flag surface (`--version`, `--dest`, `--verify-only`, `--no-activate`, `--verbose`, `--help`), partial-parity forbidden, OS-mismatch detection (no Linux binaries on Windows via Git Bash), third installer flavor forbidden; (n) **AC-19 Cross-refs intact + bi-directional** — links to §12/§13 resolve, content stays consistent, back-references encouraged, lockstep maintenance on convention changes; (o) **AC-20 Sibling files versioned + content-aligned** — each has H1+banner, `**Verifies:**` MUST cite both §00 and the relevant sibling, §00 wins on conflict, §08 marked authoritative wins over §03 on installer questions.
- **Banner v1.0.0 → v2.0.0** (major bump per the "depth materially better" rule — 4× AC count + each new AC adds explicit verification cross-refs that change reviewer posture; harmonization with §15 is structural).
- **Lockstep:** §99 banner v1.0.0 → v2.0.0; spec-index entries for §97 + §98 + §99 bumped to 2.0.0; phased-roadmap Phase 16d-ii marked done.
- **Scope discipline (Phase 16d-ii ONLY):** §00 / §01 / §02 / §03 / §04 / §05 / §06 / §07 / §08 untouched (the ACs cite existing normative content from those sections, NOT new contracts). Sibling contract files remain at v1.0.0 — they were never the target. §15 AC-12/13/16/18 referenced but NOT modified — harmonization is one-directional citation, not edit propagation.

### 1.0.0 — 2026-04-25
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

| Date | Bump | Notes |
|------|------|-------|
| 2026-04-26 | patch | Phase 27d: Added Drift Acknowledgment for low-severity doc-hygiene findings. |

## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Generic Release enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).


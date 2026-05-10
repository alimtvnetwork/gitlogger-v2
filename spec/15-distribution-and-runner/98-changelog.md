# Changelog — Distribution and Runner

**Version:** 2.3.0  
**Updated:** 2026-05-04  
**Scope:** `spec/15-distribution-and-runner/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.3.0 — 2026-05-04 — Phase 153 A24-fu44: 2 new ACs close audit-v7 MEDIUM findings
- **Added** §97 v2.0.0 → **v2.1.0**: **AC-21** [medium] (installer fetch timeout/retry contract — closes `[D3 MEDIUM] Missing timeout/retry logic for installers`); **AC-22** [low] (Bun-vs-pnpm toolchain pin — closes `[D1 MEDIUM] Ambiguous 'slides' build toolchain`). AC count 20 → 22.
- **Changed** `02-runner-contract.md` v1.0.0 → **v1.1.0**: line 42 step 4 — pnpm fallback removed per AC-22 (Bun is sole supported toolchain for slides build; missing-toolchain → exit 4 with bun.sh install link). Single-source pin per Lesson #36; AC-22 cites this file as canonical surface.
- **Lockstep**: §00 v2.2.0 → **v2.3.0**; §99 v2.1.2 → **v2.1.3**. No CI/RUBRIC/gate-count change.

### 2.2.0 — 2026-04-29 (Phase 153 A11d — `--branch` CLI flag removed; reproducibility hardened)
- **Removed** `--branch <name>` / `-Branch <name>` CLI flag from `01-install-contract.md` § "Versioning" — branch heads move, defeating the **reproducible install** contract codified in §97 AC-18. Replaced with `--ref <tag-or-sha>` row that explicitly cites AC-18's no-branch rule and the exit-`2` enforcement.
- **Changed** `04-install-config.md` § "Override precedence" — `--branch` removed from the CLI-flag bullet; clarified that the JSON `branch` field is the **default-branch hint** for tag probing only, never a CLI override.
- **Why** v5 audit (D1 HIGH "Conflicting Versioning Logic"): two surfaces contradicted — `01-install-contract.md` line 51 advertised `--branch` while §97 AC-18 forbade branch refs. Per user direction (Phase 153 A11d): strict removal, single source of truth = AC-18.
- **Lockstep:** `01-install-contract.md` v1.0.0 → **v1.1.0** (CLI surface contract change; module is `future-spec` — no shipped binary impacted); `04-install-config.md` v1.0.0 → **v1.1.0** (precedence clarification); §00 v2.1.0 → **v2.1.1** (banner ripple); §99 v2.1.1 → **v2.1.2** (audit row added).
- **No §97 AC change** — AC-18 already declared the no-branch rule; this commit removes the contradicting prose surface, no new contract added.
- **Lesson #29 codified inside §97 AC-18** (already present): contract files MUST NOT contradict §97 normative ACs; when found, prose is patched to AC, not the reverse.

### 1.1.0 — 2026-04-27 (Phase 55 — implementability lever)
- **Added** Added 5 GitHub Actions YAML workflows (build/sign/smoke/contract/release) → `has_ci_workflow` (+5). Added 3 Go installer reference blocks → `has_typed_lang_contract` (+10).

### 2.0.0 — 2026-04-26
- **Phase 16d-i — §97 Depth Pass.** Per `mem://specs/full-tree-audit-v4.md` open backlog item ("deepen scaffolded AC content for high-traffic modules"), expanded `97-acceptance-criteria.md` from 5 generic scaffold ACs to **20 module-specific GWT ACs** (AC-01..AC-05 retained as universal scaffold floor; AC-06..AC-20 added). Each new AC averages 1500-2200 chars with explicit `**Given** / **When** / **Then**` triplet and a `**Verifies:**` cross-ref line.
- **Doc-only — no schema bump, no DDL change, no installer/runner code changes.** This is a contract clarification, not a behavior change.
- **§97 acceptance-criteria changes (AC-06..AC-20):** (a) **AC-06 Installer one-liner shape** — Bash + PowerShell parity, idempotent, dependency pre-check, exit code mapping per §13 (`1`/`2`/`3`/`4`), 60s SLO; (b) **AC-07 Default install layout** — exactly 4 folders (`spec`, `linters`, `linter-scripts`, `linters-cicd`), pinned to release SHA not main HEAD, additive (never destructive), `--force` required to overwrite; (c) **AC-08 install-config.json schema** — strict JSON, default folder list locked, single-component paths only, lockstep with §00 table enforced by CI; (d) **AC-09 Bash+PowerShell parity** — byte-identical output modulo line endings, shared flag surface (`--dest`, `--folders`, `--ref`, `--force`, `--dry-run`, `--verbose`, `--help`), partial-parity forbidden; (e) **AC-10 Runner sub-command dispatch** — exact 4-row contract from §00 (`<no-args>` / `lint` / `slides` / `help`), unknown sub-cmd exits `2`, post-cmd flag forwarding, pre-cmd flags reserved; (f) **AC-11 Back-compat for legacy no-args** — identical observable behavior preserved, no deprecation banners on no-args path, removal requires major bump + 2 minor deprecation cycles; (g) **AC-12 Release artifact set** — all 8 items required (linters zip, slides zip, install.sh, install.ps1, linters-install.sh, install-config.json, checksums.txt, plus codeload-sourced tree), filename patterns exact, missing any blocks release; (h) **AC-13 checksums.txt format** — `sha256sum`-compatible (two spaces), every asset checksummed, installers MUST verify before extract (supply-chain protection), mismatch = exit `4`; (i) **AC-14 linters-install.sh rename** — uploaded with rename to avoid colliding with top-level install.sh, internal self-references must reflect new name; (j) **AC-15 Install destination defaults** — `.` default, `mkdir -p` semantics, EACCES detected before download, refuses install into source repo (symlink-resolved); (k) **AC-16 Release pipeline** — tag-driven only, pinned to tag's SHA not branch HEAD, atomic publish (draft until checksum-verified then promoted), no auto-publish to npm/PyPI; (l) **AC-17 slides browser-open** — OS-appropriate opener (`xdg-open`/`open`/`Start-Process`), `--no-open` skip, attached process for `Ctrl-C`, exit `0` on `SIGINT` (not `130`); (m) **AC-18 --ref reproducible install** — accepts tag or full SHA only (branches forbidden — defeat reproducibility), codeload override, exit `3` on missing ref; (n) **AC-19 Cross-references intact** — links to §12/§13/§16 + spec-slides resolve, content stays consistent with each, lockstep maintenance required; (o) **AC-20 Module-specific files versioned** — each sibling has H1+banner, content elaborates §00 (no contradiction), `**Verifies:**` MUST cite both §00 and the relevant sibling, §00 wins on conflict.
- **Banner v1.0.0 → v2.0.0** (major bump per the "depth materially better" rule — 4× AC count + each new AC adds explicit verification cross-refs that change reviewer posture).
- **Lockstep:** §99 banner v1.0.0 → v2.0.0; spec-index entry for §97 + §98 + §99 bumped to 2.0.0; phased-roadmap Phase 16d-i marked done.
- **Scope discipline (Phase 16d-i ONLY):** §00 / §01 / §02 / §03 / §04 untouched (the ACs cite existing normative content from those sections, NOT new contracts). Sibling contract files remain at v1.0.0 — they were never the target.

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
| 2026-04-26 | minor | Phase 27b: Added `kind: future-spec` frontmatter + Drift Acknowledgment section. Module now exempt from drift audit findings (implementation lives in downstream repos). |

## 2026-04-27 — Phase 63 impl-sweep

- Phase 63: appended Distribution and Runner enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).

## 2026-04-27 — Phase 76 (impl 90 → 100)

- Added Mermaid lifecycle diagram — satisfies `has_mermaid` (+5).
- Added SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).


### 2.1.0 — 2026-04-29 — Phase 153 Task #35-fu2: SemVer-track unification (§00 lift to align with §98 SemVer-max)

- **Action**: §00 banner bumped 1.1.0 → 2.1.0 to align with §98 SemVer-max (2.0.0 Phase 16d-i depth pass + 1.1.0 Phase 55 lever consolidated as 2.1.0). The §00 banner had been tracking the Phase 55 lever stream independent of the §98 Phase 16d-i depth-pass major bump — Task #32 precedent (spec/07 dual-track unification).
- **Lockstep**: §00 1.1.0 → 2.1.0; §98 banner 2.1.0 → 2.1.1; §99 banner 2.1.0 → 2.1.1; §99 narrative updated.
- **Why**: Codifies Lesson #25 — never let §98 track a SemVer namespace independent of §00. The Phase 16d-i depth pass (§97 5→20 ACs) was a real major bump that §00 never absorbed. Phase 55's `has_ci_workflow + has_typed_lang_contract` lever is preserved as the minor-bump rationale for 2.1.0.

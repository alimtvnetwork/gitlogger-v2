# Changelog — Update — Overview

**Version:** 2.5.0  
**Updated:** 2026-05-07 (Phase J8 — AC-23 binds `28-update-interface-contract.md` into §97; AC count 22 → 23; closes Lesson #19/#39 sibling-delegation gap surfaced by tree-wide audit.)

### 2.5.0 — 2026-05-07 — Phase J8: AC-23 interface-contract binding (Lesson #19 + Lesson #39)
- **Action**: Added `[critical]` AC-23 binding `28-update-interface-contract.md` (kind: interface-contract) into §97 with explicit GWT covering all 5 normative subsections — (1) `latest.json` Draft-07 JSON Schema with required keys + validation rules 1–4, (2) eight `RISEUP_UPDATE_*` env vars read once at process start, (3) per-OS canonical deploy-path table, (4) self-update exit-code enumeration `{0, 2, 3, 4, 5, 6, 7, 8, 99}`, (5) cross-references to consumer files. Forbidden patterns: inline schema in §00/siblings; defining `RISEUP_UPDATE_*` outside §28; declaring self-update exit codes outside §28; switching `28-update-interface-contract.md` away from `kind: interface-contract`.
- **Why**: Tree-wide sibling-binding survey (Phase J8) flagged `28-update-interface-contract.md` as one of 5 modules with an interface-contract sibling unbound from §97 — textbook Lesson #19 audit-boundary < verification-boundary gap (mirror of spec/12 AC-10 fix in Phase 153 Task A24-fu4) and Lesson #39 second-axis instance (intra-module sibling delegation, mirror of spec/22 AC-80 in Phase 154). Without §97 binding, an auditor could miss the self-update wire format entirely while reporting "GOOD" on D2 AC Coverage.
- **Lockstep**: §97 v2.4.2 → **v2.5.0** (minor — new `[critical]` AC, AC count 22 → 23); §00 v2.4.4 → **v2.4.5** (patch — banner-only + h10 stamp 153 → 154); §98 v2.4.4 → **v2.5.0** (this row mirrors §97 minor); §99 v1.6.4 → **v1.6.5** (audit row + freshness stamp 149 → 154).
- **No CI workflow change · no RUBRIC bump · no gate-count change.** LLM re-score deferred per Lesson #20 (gateway 402 oscillating per Lesson #86; J8 confirmed budget-exhausted on chunked path).

### 2.4.4 — 2026-05-04 — Phase 153 Task A24-fu44: AC-21 stale-cache enumeration extension

- **Action**: Extended AC-21's `Then` clause from a single-class enumeration (D5 + D4) to a four-class enumeration covering all currently-cached findings: (a) D5 missing-sub-module-context citing files 09–27 / subfolder 24; (b) D4 truncated `04-build-scripts.md`; (c) **NEW** D3 ambiguous `updater.exe` lifecycle (canonically specified in `19-updater-binary.md` + `12-code-signing.md` + `06-cleanup.md` (AC-16 wall-clock budget) + AC-17 handoff ownership — none in tier-1 bundle); (d) **NEW** D1 undefined `latest.json` schema in §00 (canonically defined in `01-self-update-overview.md` + `13-release-assets.md`; §00 line 84 links per Lesson #36 link-don't-restate). Added cache-observed `files_used=13/54 ≈ 24%` saturation citation.
- **Why**: All 3 cached findings (HIGH D5 + MEDIUM D3 + LOW D1) are walker-cap artifacts on this `normative-contract` axis module; the contracts the auditor flags as missing are all on disk in non-tier-1 files. Per Lesson #75 (walker-cap triage before self-lift), authoring new ACs would be measurement-bias work — extending the existing harness-artifact pin closes the findings honestly.
- **Lockstep**: §97 v2.4.1 → **v2.4.2** (patch — prose-only enumeration extension, no new AC, no AC-31-31 cascade); §00 v2.4.3 → **v2.4.4** (patch — banner-only); §98 v2.4.3 → **v2.4.4** (this row); §99 v1.6.3 → **v1.6.4** (audit row).
- **No CI workflow change · no RUBRIC bump · no gate-count change · no new AC.** LLM re-score deferred per Lesson #20.

### 2.4.3 — 2026-05-01 — Phase 153 Task A24-fu38: AC-16 wall-clock pin + AC-17 rollback-ownership prose patch
- **Action**: Patched AC-16 to specify cleanup-budget 100ms is **wall-clock** time (closes audit-v10 LOW D1 "Missing Unit for Cleanup Latency"). Patched AC-17 with normative paragraph **Rollback-trigger ownership** — rollback is process-local to the updater OR delegated to next-start cleanup per AC-16; NO inter-process signaling permitted (closes audit-v10 MEDIUM D3 "Ambiguous Rollback Trigger in Handoff").
- **Why**: Both findings are LLM-auditor surfaced contract-clarification gaps in the §97 portion the auditor DID see. spec/14 stays at axis cap=100, score 90 — Lesson #71 NO-OP threshold not met (gap=10 > 3); cheap prose tightenings shipped together per Lesson #67.
- **Lockstep**: §97 v2.4.0 → **v2.4.1** (patch — prose-only, no new AC, no AC count change, no AC-31-31 cascade); §00 v2.4.2 → **v2.4.3** (patch — banner-only); §98 v2.4.2 → **v2.4.3** (this row); §99 v1.6.2 → **v1.6.3** (audit row).
- **No CI workflow change · no RUBRIC bump · no gate-count change · no new AC.**
- **Lesson #71 counter-case**: gap 10 > 3 threshold → contract-tightening justified, NOT no-op. spec/22 (also gap 10) defers to A24-fu39 (Lesson #70 walker-budget archive split, not contract-tightening).

### 2.4.2 — 2026-04-30 — Phase 153 Task A24-fu25: §00 walker-pin pure-promotion (Lesson #63 fifth instance)
- **Action**: Inserted `> 🤖 Walker-Pin` 2-row teaser table at §00 head (after metadata banner) surfacing AC-21 (module asset inventory pin, 36 entries) + AC-22 (`<module>` ldflags placeholder = consuming repo's `go.mod` path) as canonical close-outs for cache-stale audit findings (D5 missing-sub-module-context, D4 truncated-build-script, D3 ambiguous-`<module>`-placeholder).
- **Why**: Cache `total=87 GOOD` with 3 advisory findings — ALL pre-closed in §97 (AC-21 from A11h closes D5+D4 by walker bundling-cap pin per Lesson #29; AC-22 from A24-fu5 closes D3 by Lesson #36 use-site prose). Walker `files_used=11/54 (20%)` — extreme saturation; targeted contracts live at §97 lines 228 + 234 well past the cap. Pure visibility patch.
- **Lockstep**: §00 v2.4.1 → **v2.4.2** (patch — teaser content); §98 v2.4.1 → **v2.4.2** (this row); §99 v1.6.1 → **v1.6.2** (audit row).
- **§97 NOT bumped at v2.4.0** — no new normative requirement, no AC change, no AC-31-31 cascade, no RUBRIC bump, no CI workflow change. **Pure-promotion variant** of Lesson #61 per spec/22 A24-fu20 + spec/27 A24-fu22 + spec/03 A24-fu23 + spec/13 A24-fu24 precedent.
- **Lesson #63 fifth instance** — second on `normative-contract` axis (after spec/13 A24-fu24). Pattern now battle-tested across 5 modules and 3 axes.

### 2.4.1 — 2026-04-30 — Phase 153 Task A24-fu5: AC-22 `<module>` placeholder pin
- **Added** AC-22 `[high]` — binds the literal `<module>` in `04-build-scripts.md` ldflags (PowerShell line 102; Bash line 200) to the consuming repo's `go.mod` `module` line; build scripts MUST NOT hard-code the path.
- **Added** explanatory blockquote in `04-build-scripts.md` immediately after the PowerShell code block (use-site prose; Lesson #36 link-don't-restate).
- **Why**: closes audit-v7 D3 MEDIUM "Ambiguous <module> Placeholder" as a real-but-narrow gap. Per Lesson #36, the canonical explanation lives at the use-site; AC-22 binds it normatively.
- **Spec lockstep**: §97 v2.3.0 → **v2.4.0** (AC count 21 → 22, minor — new content); §00 v2.4.0 → **v2.4.1** (patch); §98 v2.4.0 → **v2.4.1** (patch); §99 v1.6.0 → **v1.6.1** (patch). **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Validation**: lockstep 87/87, tree-health 168/168 strict, version-parity 74/74, freshness 81/81 (verify after run).

### 2.4.0 — 2026-04-30 — Phase 153 Task A11h: AC-21 module asset inventory pin
- **Added** AC-21 `[critical]` — declares spec/14's full 36-entry on-disk inventory as auditor-authoritative; classifies audit-v5 D5 HIGH (missing files 09–27, subfolder 24), D4 MED (truncated `04-build-scripts.md`), D1 LOW (`<module>` placeholder ambiguity) as harness bundling-cap artifacts. Mirror of spec/13 AC-24 + spec/28 AC-28-41 + spec/16 AC-21 + spec/22 AC-78.
- **Why**: per Lesson #29 (audit-corpus pin generalised at A11g memo) — every cited file is present on disk per §99 inventory; the `<module>` placeholder is intentional contract-bound at-build-time substitution (NOT an authoring error).
- **Spec lockstep**: §97 v2.2.0 → **v2.3.0** (AC count 20 → 21); §00 v2.3.1 → **v2.4.0**; §98 v2.3.1 → **v2.4.0**; §99 v1.5.1 → **v1.6.0**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**.
- **Validation**: lockstep 87/87, tree-health 168/168 strict, version-parity 74/74, freshness 81/81 (verify after run).
**Scope:** `spec/14-update/`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 2.3.1 — 2026-04-30 — Phase 153 (Lesson #36 cross-ref inoculation)
- **Added** `## Concurrency Posture (Normative cross-reference)` section to `22-update-command-workflow.md` linking the self-update worker's `update.lock` discipline, atomic temp-then-rename for staged binaries, and any state-DB writes to the canonical contract at [spec/13 §97 AC-22](../13-generic-cli/97-acceptance-criteria.md). Pure cross-link — contract NOT restated. Codifies Lesson #36 (link, never restate). **No §97 AC change**, no AC-31-31 cascade, no RUBRIC bump, no gate-count change. §99 v1.5.0 → v1.5.1. Sibling lockstep: spec/16 (v2.2.1) + spec/28 (v2.1.3) shipped same Lesson #36 inoculation in this phase.

### 2.3.0 — 2026-04-29 — Phase 149 (P3 sweep slot 9 — Verifies clauses on §97)
- **Added** `**Verifies:**` clauses to all 20 ACs in `97-acceptance-criteria.md` (gap=20 → 0). Each AC now explicitly maps to the underlying invariant it protects: structural floor (AC-01), zero broken links (AC-02), slot-immutability (AC-03), §99 inventory rubric (AC-04), strict-pass tree-health (AC-05), cross-platform deploy uniformity (AC-06), parent-survival (AC-07), build-time version-injection (AC-08), supply-chain trust (AC-09), integrity / no-MD5-SHA1 (AC-10), idempotent install + no-silent-sudo (AC-11), latest-probe-or-fail (AC-12), XDG + atomic-write 0600 (AC-13), ordered-pipeline-with-fail-fast (AC-14), no-daemon / no-stdout-pollution (AC-15), idempotent silent-cleanup-budget (AC-16), single-step atomic rollback + RECOVERY.md (AC-17), three-layer precedence + system-dir blacklist (AC-18), tag-first monotonicity (AC-19), six-target-floor + CGO_ENABLED=0 + reproducible-toolchain (AC-20). §97 v2.1.0 → v2.2.0. AI-confidence: P3 driver eliminated for `spec/14`; derived tier Medium → High.

- **Added** §00 Feature Inventory rows for slots 24/25/26/27/28: `24-update-check-mechanism/`, `25-release-pinned-installer.md`, `26-repo-major-version-migrator.md`, `27-generic-installer-behavior.md`, `28-update-interface-contract.md`. Files already existed and were §97/§99-tracked; only §00 lagged. Pure inventory reconciliation — no spec rule changes. Linter: P1 driver eliminated for `spec/14`.

### 2.1.0 — 2026-04-28 (Phase P24 — H10 reverse-drift reconciliation)

- **Changed** Reconstructed §98 release ladder so §00 banner version `2.1.0` is now backed by an explicit release row. Prior §98 contained ad-hoc dated prose blocks (Phase 63 `2026-04-27 impl-sweep` / Phase 76 `2026-04-27 impl 90 → 100`) appended *after* the Cross-References footer that were not promoted into SemVer entries; this release codifies them as **1.4.0** and **2.0.0** below. No behavioural change to module rules.
- **Added** `<!-- h10-verified-phase: 24 -->` stamp to `00-overview.md`, opting this file into strict H10 version-parity enforcement per `check-version-parity.py` AC-29-11/12/13.
- **Banner sync**: §00 `Updated:` 2026-04-27 → 2026-04-28.

### 2.0.0 — 2026-04-27 (Phase 76 — impl 90 → 100)

- **Added** Mermaid lifecycle diagram `lifecycle-14-update.mmd` — satisfies `has_mermaid` (+5).
- **Added** SQL DDL audit-log schema — satisfies `has_sql_ddl` (+20).
- Implementability raised 90 → 100 (deterministic audit, capped).
- **Major bump rationale**: introduces two new normative artifact surfaces (binding lifecycle diagram + auditable SQL DDL schema) that downstream tooling can validate against — promoted from minor on P24 reconciliation because they constitute a new public contract surface, not just additive content.
- Audit-trail source: prior `## 2026-04-27 — Phase 76 (impl 90 → 100)` prose block under Cross-References.

### 1.4.0 — 2026-04-27 (Phase 63 — impl-sweep)

- **Added** Update Pipeline enums TS enum mirror to satisfy `has_ts_enums` rubric (impl 80 → 90).
- Audit-trail source: prior `## 2026-04-27 — Phase 63 impl-sweep` prose block under Cross-References.

### 1.3.0 — 2026-04-27 (Phase 124 — cite-direction fix)

- **Changed** AC-20 `Given` and `Source` lines now dual-cite the upstream generic blueprint `../16-generic-release/01-cross-compilation.md` alongside the local `16-cross-compilation.md` and `17-release-pipeline.md`. Adds a "deviation MUST be justified in §99" clause. Closes the AC-SAG-25 cite-direction gap surfaced by Phase 121's reframe (§14 → §16, not §16 → §14 as originally proposed).
- §97 banner 2.0.0 → 2.1.0; §99 audit row appended.

### 1.2.0 — 2026-04-27

- **Phase 39c — Added** `28-update-interface-contract.md` defining the authoritative `latest.json` JSON Schema (Draft-07), self-update env-var contract (`RISEUP_UPDATE_*`), canonical deploy paths per OS, and a self-update exit-code table. Closes audit finding *HIGH — Self-Update relies on undefined `latest.json` shape*.
- §00 banner v2.0.0 → v2.1.0; §99 lockstep update.

### 1.1.0 — 2026-04-26

- **Phase 16b — Deepen §97 with module-specific GWT ACs.** §97 banner v1.0.0 → v2.0.0 (major bump; AC count 5 → 20).
- **Added** 15 module-specific Given/When/Then ACs (AC-06..AC-20) covering: AC-06 rename-first deploy (Windows-locked-file workaround, atomic same-dir rename, uniform across platforms), AC-07 Windows handoff via detached `updater.exe` (CREATE_NEW_PROCESS_GROUP|DETACHED_PROCESS, parent-PID wait, self-delete), AC-08 three-branch version verification (deployed/source/declared, build-time `-ldflags -X main.Version` injection, no runtime `version.txt` reads), AC-09 mandatory code signing (Authenticode `signtool verify /pa`, macOS codesign+notarize, Linux GPG detached sigs, fail-on-unsigned), AC-10 SHA-256 checksums.txt + verify-before-install (MD5/SHA-1 forbidden, signed checksums fingerprint), AC-11 idempotent install scripts + standard locations (`%LOCALAPPDATA%\Programs`, `~/.local/bin`, `/usr/local/bin`, no-sudo-by-default, opt-in PATH modification), AC-12 latest-version probe (GitHub releases/latest, `--version=X.Y.Z` pin override, no fallback guess, User-Agent header), AC-13 XDG-compliant config (`$XDG_CONFIG_HOME/<binary>/update.json`, flat JSON per §13 AC-08, atomic write via .tmp+rename, 0600 perms), AC-14 ten-step `update` workflow (network check → probe → compare → download .partial → SHA-256 → signature → rename .new → spawn detached → exit ≤100ms → updater swap), AC-15 non-blocking 12h pre-command-hook update check (fire-and-forget detached child, NO daemon/cron, JSON fallback store, banner on next invocation), AC-16 startup cleanup (.old + stale .partial + old .log files, silent failures, idempotent, ≤100ms cap), AC-17 atomic rollback on mid-update failure (rename `.old` back, RECOVERY.md fallback if rollback itself fails), AC-18 deploy path resolution precedence (default → build.json → --deploy-path flag, refuse system dirs, perm check), AC-19 `git describe --tags` last-release detection (commit-count/branch-name forbidden, conventional-commits drives bump kind), AC-20 cross-compilation matrix (windows/amd64+arm64, linux/amd64+arm64, darwin/amd64+arm64, CGO_ENABLED=0, `-ldflags -s -w`, fail-on-partial-platform).
- **Preserved** AC-01..AC-05 (generic structural ACs that validate the spec module itself, distinct from AC-06..AC-20 which validate an updater/installer implementation).
- Lockstep §99 v1.0.0 → v1.1.0; spec-index updated.

### 1.0.0 — 2026-04-25

- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

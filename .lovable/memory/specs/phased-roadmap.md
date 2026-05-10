---
name: Phased Spec Roadmap
description: Authoritative phased task list for spec/22-git-logs-v2. On `next`, take top pending phase and complete it. Spec-only, no implementation.
type: feature
---

# Phased Spec Roadmap — Git Logs v2

**Rule:** On each `next`, take the **top pending phase** (lowest number, status = pending) and complete every task in it. Update the matching §98 changelog row, §99 consistency, and bump version. Mark phase ✅ here when done.

---

## ✅ Phase 0 — Q1 IsOrganization (DONE, v3.8.1)
## ✅ Phase 1 — Q2 PipelineAction + SystemEvent (DONE, v3.8.2)
## ✅ Phase 2 — Split-DB Schema Surgery (DONE, v3.8.3 / schema v2.9.0)

Landed in v3.8.3:
- §18: dropped `LogEntry` + `ErrorLogEntry` (and their indexes), added `ShaRegistry` table + 2 indexes, added 3 ConfigKv defaults (`ShaLogsRoot`, `MaxOpenShaDbHandles`, `ShaDbIdleCloseSec`), bumped PluginVersion 2.8.9→2.9.0, appended MigrationState 2.9.0.
- §02: banner 3.8.0→3.8.3, engine note rewritten, ConfigKv sub-table for new keys.
- §01: banner 3.8.1→3.8.3, ShaRegistry def refined, NEW glossary rows `PerShaDb` + `ShaLogsRoot`.
- §98 changelog v3.8.3 row added; §99 v3.8.3 audit table + Q3 status flip in v3.8.0 audit. Schema validated in-memory: 29 tables, no LogEntry/ErrorLogEntry, ShaRegistry present, 13 ConfigKv rows, 9 MigrationState markers.

---

## ✅ Phase 3 — Split-DB Error Codes & Cross-Section Updates (DONE, v3.8.4)

Landed in v3.8.4:
- §15: 4 new `GL-SHA-DB-*` codes (`OPEN-FAILED` 503, `CREATE-FAILED` 500, `CHECKSUM-MISMATCH` 500, `QUOTA-EXCEEDED` 507) under new section *Per-SHA log storage*. Banner v2.8.7→v2.9.0.
- §22: rewritten — eligibility on `ShaRegistry.LastSeenAt`, rename→delete-row→unlink crash-safety with `*.pruning` recovery, exit code 4 for FS errors, empty-shard cleanup. Banner v2.5.0→v2.9.0.
- §23: backup is now a directory tree; manifest gains `ShaFiles[]` with `{PipelineId,Sha,DbFilePath,RowCount,FileSizeBytes,Sha256}` + `ShaFileTotal`; restore is all-or-nothing with `.bak` rollback; new pre-v2.9.0 cross-version migration row. Banner v2.5.0→v2.9.0.
- §29: lifecycle table gained "Per-SHA tree" column; Wipe deletes `<ShaLogsRoot>/` first, then root DB, then `rmdir` parent. Banner v2.5.0→v2.9.0.

## ✅ Phase 4 — Split-DB Doc Closure (DONE, v3.8.5)

Landed in v3.8.5:
- §00: §39 inventory row refreshed for v2.9.0 path layout (`<dataDir>/<ShaLogsRoot>/<Sha[0:2]>/<Sha>.db`) + cross-refs to §15/§22/§23/§29. Banner v3.8.0→v3.8.5.
- §97: AC-49..AC-53 promoted from draft to **Active (v2.9.0)**, rewritten to match shipped DDL (`(PipelineId, Sha)` key, real ConfigKv defaults 32/120, GL-SHA-DB-* code refs, manifest `ShaFiles[]`, Wipe per-SHA-tree-first). Banner v3.8.2→v3.8.5.
- Root `spec/spec-index.md`: 9 version cells refreshed for files touched in Phases 2–4.
- `26-gitlogs-diagrams/01-er-diagram.mmd`: re-rendered for split-DB boundary — top annotation, stale edges removed, `ShaRegistry` entity rewritten to v2.9.0 columns.
- §98 v3.8.5 row + §99 Phase 4 audit table + Health Score updated.

---

## ✅ Phase 5 — SSH-Key Lane B: Schema & Errors (DONE, v3.8.6)

Landed in v3.8.6 / schema v2.9.1:
- §18: `CREATE TABLE SshKey` (11 cols) + 2 indexes; `CREATE TABLE SshNonce` + 1 index; 2 new ConfigKv (`SshAuthMode='optional'`, `SshNonceJanitorBatch='100'`); PluginVersion 2.9.0→2.9.1; MigrationState 2.9.1 appended. Banner v2.9.0→v2.9.1.
- §01: 3 new glossary rows (`SshKey`, `Ed25519Signature`, `SshNonce`). Banner v3.8.3→v3.8.6.
- §02: banner v3.8.3→v3.8.6 (existing SshKey/SshNonce sub-sections now backed by canonical DDL).
- §15: banner v2.9.0→v2.9.1 — 9 SSH lane codes already present, now backed by canonical schema.
- §31: banner v2.7.0→v2.9.1 with canonical-DDL note.
- AuditActionType seeds verified: `SshKeyRegister`(22), `SshKeyRevoke`(23), `SshKeyRotate`(24) already present.
- In-memory SQLite validation: 31 tables, 15 ConfigKv, 10 MigrationState markers, 3 SshKey* AuditActionTypes.

## ✅ Phase 6 — SSH-Key Lane B: Flow & Threat Doc (DONE, v3.8.7)

Landed in v3.8.7:
- §05: banner v2.1.0→v2.9.1. SSH lane block (10-step validation order) confirmed authoritative; cross-refs to §31/§15/§18 verified.
- §28: banner v2.7.0→v2.9.1. Drop-in `git-logs-ssh.yml` workflow (namespace `git-logs@v2`, four headers, canonical signing string, deploy-key rotation, key-wipe `if: always()`) confirmed authoritative.
- §30: banner v2.7.0→v2.9.1. Added 4 STRIDE Spoofing rows (S5 replay, S6 key theft, S7 sig stripping/lane downgrade, S8 lane-mode forgery) — closes the "S5–S8 SSH-lane additions" forward reference in summary.

---

## ✅ Phase 7 — AC Quality Pass (DONE, v3.8.8)

Landed in v3.8.8:
- §97 banner v3.8.5→v3.8.8. Every AC (AC-01..AC-59) rewritten from one-line table rows into Given/When/Then stanzas + `Verifies:` cross-refs + `[active]`/`[draft]`/`[deprecated]` status badges. Reorganized into 9 thematic sections (A UI · B Domain · C Auth/Lane · D Endpoints · E Logging/Migrations · F Audit · G Schema/Diagrams · H Per-SHA Split-DB · I SSH-Key Lane B).
- 7 new ACs added in Section I, all `[active]`: AC-60 SshKey registration shape; AC-61 SshNonce replay defense (skew + per-key uniqueness + janitor); AC-62 lane gating via `SshAuthMode` + mixed-lane `GL-SSH-LANE-CONFLICT`; AC-63 signature stripping defense (header-completeness ordered first + mandatory HTTPS); AC-64 SshKey rotation flow (`IsActive=0` no-cache reject + dual SystemEvent + dual AuditTrail); AC-65 deploy-key one-Repo blast radius (FK CASCADE + `LastUsedAt` anomaly + rate cap); AC-66 canonical signing string + `git-logs@v2` namespace + `-H sha512`.
- AC-38 amended to list SSH AuditActionType seeds (22/23/24). AC count 59 → 66.

## ✅ Phase 8 — API Streaming Spec (DONE, v3.8.9)

Landed in v3.8.9:
- §04 banner v2.8.3 → v2.9.2. Added new top-level §11 NDJSON Streaming Retrieval (v2.9.2) with 9 sub-sections covering rationale, opt-in via `Accept: application/x-ndjson`, 5-frame schema (`Header`/`Log`/`ErrorLog`/`Progress`/`End` + optional mid-stream `Error`), ordering & atomicity, 4 new ConfigKv keys (doc-only), resume via `?after-seq=N` + `?stream-id=<uuid>`, endpoint applicability matrix (#5–#10 ✅; #1–#4 ❌), wire example, cross-refs.
- 2 new error codes introduced doc-side: `GL-NDJSON-CLIENT-DISCONNECT` (499 informational), `GL-NDJSON-CURSOR-LOST` (500).
- **Streaming follow-ups deferred:** §18 ConfigKv seeding for 4 `Ndjson*` keys, §15 entries for 2 `GL-NDJSON-*` codes, §17 OpenAPI `application/x-ndjson` content variants for endpoints #5–#10, §97 ACs for streaming behavior. Tracked under "Streaming follow-ups" in §99 Phase 8 audit.

## ✅ Phase 9 — Pipeline PreviousHasError Flag (DONE, v3.8.10 / schema v2.9.2)

Landed in v3.8.10 / schema v2.9.2:
- §18: `Pipeline` table gained `PreviousHasError INTEGER NOT NULL DEFAULT 0 CHECK (PreviousHasError IN (0,1))` immediately after `HasError`; `HasError` itself gained explicit `CHECK (HasError IN (0,1))`. Inline back-fill rule (`UPDATE Pipeline SET PreviousHasError = HasError;` on v2.9.1→v2.9.2 upgrade) and write rule (single-`UPDATE` atomicity, no read-modify-write). PluginVersion 2.9.1→2.9.2; MigrationState 2.9.2 appended (11 markers).
- §02: banner v3.8.6→v3.8.10. Pipeline doc gains `PreviousHasError` row + state-transition labels (`first-failure`/`still-failing`/`just-recovered`/`still-green`).
- §01: banner v3.8.6→v3.8.10. Bare `Pipeline` glossary row split into 3 — `Pipeline`, `HasError`, `PreviousHasError`.
- **Phase 9 follow-ups deferred:** §97 ACs for `PreviousHasError` (state-transition matrix, back-fill correctness, single-statement write atomicity), §03 admin UI rendering of the four state labels, §04 NDJSON `Header` frame label exposure.

## ✅ Phase 10 — Diagram Render Pass (DONE, v2.1.0)

Landed in folder 26 v2.1.0:
- Rendered all 6 active `.mmd` sources to companion `.svg` artifacts via `@mermaid-js/mermaid-cli` v11+. Source `.mmd` unchanged.
- §00/§98/§99 banners + spec-index refreshed.

## ✅ Phase 11 — Streaming Follow-ups Pickup (DONE, v3.8.11 / schema v2.9.3)

Absorbed all Phase 8 streaming deferrals + AC coverage:
- §18: 4 NDJSON ConfigKv seeds (`NdjsonProgressEveryRows=10000`, `NdjsonProgressEveryMs=2000`, `NdjsonMaxRowsPerStream=1000000`, `NdjsonMaxFrameBytes=262144`); PluginVersion 2.9.2→2.9.3; MigrationState 2.9.3 appended (12 markers).
- §15: `GL-NDJSON-CLIENT-DISCONNECT` (499) + `GL-NDJSON-CURSOR-LOST` (500) registered.
- §17: `info.version` 2.8.2→2.9.3 (absorbs Phases 4/5/9/11). `ErrorCode` enum gained 4 `GL-SHA-DB-*` + 2 `GL-NDJSON-*` codes. 7 new `Ndjson*` schemas + `NdjsonStream` reusable response. All 4 GET paths carry `application/x-ndjson` content variant + `after-seq`/`stream-id` query params.
- §97: 6 new ACs (AC-67..AC-72) — opt-in, frame ordering, resume, disconnect, frame cap, Progress cadence. AC count 66→72.
- Validation: `pyyaml.safe_load` clean; in-memory SQLite confirms 19 ConfigKv rows, 12 MigrationState markers.

## ✅ Phase 12 — Phase 9 Follow-ups (DONE, v3.8.12 / OpenAPI v2.9.4)

Closed the unblocked subset of Phase 9 deferrals (§03 admin UI is consumer-side, intentionally out-of-scope for this spec-only project):
- §04 §11.3.1: `Header` frame example + bullet documents OPTIONAL `StateTransition` (4-value enum, single-pipeline-scope only). Banner v2.9.2→v2.9.3.
- §17: `info.version` 2.9.3→2.9.4. `NdjsonHeaderFrame` gained optional `StateTransition` enum property (NOT in `required`).
- §97: 3 new ACs (AC-73 label matrix, AC-74 NDJSON Header exposure, AC-75 back-fill + write atomicity). AC count 72→75.
- Validation: `pyyaml.safe_load` clean; `StateTransition` confirmed in `NdjsonHeaderFrame.properties` with all 4 enum values, confirmed absent from `required`.

## ✅ Phase 13 — Deepen Scaffolded ACs in §22 §97 (DONE, v3.8.13)

Closed §22-scope subset of `mem://specs/full-tree-audit-v4.md` deepening backlog. Doc-only, no schema/DDL/OpenAPI churn:
- §97: 8 high-traffic one-liner ACs deepened from ~200-260 chars to 1400-2200 chars each (5–10×): AC-02 (Profile no-password rule), AC-03 (migration semver ordering + 12-marker baseline), AC-12 (streaming ingest incremental caps), AC-14 (AckResponse Retrieval URLs), AC-17 (App columns + forbidden Phase B1 fields), AC-18 (AppLink XOR + CASCADE), AC-22 (§26 6-file Mermaid manifest), AC-30 (ErrorEnvelope shape + RequestId mirroring + NDJSON error split). AC count unchanged at 75 (verified sequential AC-01..AC-75).
- 4 simpler ACs (AC-04/AC-05/AC-25/AC-34) intentionally left lean.

---

## ✅ Phase 14 — Deepen Scaffolded ACs in §17 §97 (DONE, v1.1.0)

Closed §17-scope subset of the deepening backlog. Doc-only, no schema/DDL churn:
- §17 §97: 4 short ACs (AC-01..AC-04) deepened from ~209-260 chars to 1941-2254 chars each (8–10×): AC-01 module-entry-point structural contract (6 rules), AC-02 cross-link contract (6 rules incl. slot-immutability `../16-...` rule), AC-03 naming-regex contract with positive/negative examples + slot-collision precedent, AC-04 consistency-report freshness contract (7 rules incl. measured-not-narrated rule + version-≥-overview lockstep).
- AC-05 already deep (1803 chars) — left as-is. AC count unchanged at 5.
- Banner v1.0.0 → v1.1.0; lockstep §98 v1.1.0 + §99 v3.6.0 + spec-index updated.
- §07 design-system NOT touched in Phase 14 — it uses table-style AC-001..AC-NNN format (different surgery needed); flagged as candidate Phase 15.

---

## ✅ Phase 15a — Convert §07 §97 Theme & Variables to GWT (DONE, v3.3.0)

First slice of the §07 structural conversion. AC IDs preserved across format change:
- §07 §97 banner v3.2.0 → v3.3.0; AC count unchanged at 34 (AC-001..AC-034 sequential, verified — no IDs added/removed/renamed).
- **6 ACs converted (AC-001..AC-006 Theme & Variables)** from one-row table format (~80 chars each) to full GWT subsections (994-4231 chars each, 12-50× depth) with concrete contracts + cross-refs to `01-design-principles.md`, `02-theme-variable-architecture.md`, `src/index.css`, `tailwind.config.ts`, theme provider, WCAG 2.1 §1.4.3/§1.4.11.
- Added top-of-file **Format note** documenting the mid-conversion state (some sections GWT, others still table) so consumers and future maintainers aren't confused — IDs are stable across formats so ID-scraping tooling continues to work unchanged.
- Lockstep §98 v1.0.0 → v1.1.0 + §99 v3.2.0 → v3.3.0 + spec-index updated.

---

## ✅ Phase 15b — Convert §07 §97 Typography to GWT (DONE, v3.4.0)

Second slice of the §07 structural conversion. AC IDs preserved:
- §07 §97 banner v3.3.0 → v3.4.0; AC count unchanged at 34 (verified).
- **5 ACs converted (AC-007..AC-011 Typography)** from one-row table format (~70 chars each) to full GWT subsections (1209-4005 chars each, **17-57× depth**) with concrete contracts + cross-refs to `03-typography.md`, `index.html` font-loading, `tailwind.config.ts` font registration, `02-theme-variable-architecture.md`, `07-code-blocks.md`, `12-page-creation-rules.md`, WCAG 2.1 §1.3.1/§2.4.6.
- AC-007 Ubuntu headings (font stack, Google Fonts `display=swap`, `tailwind.config.ts` `fontFamily.heading`); AC-008 Poppins body (weights 300-700, default `fontFamily.sans` override); AC-009 Ubuntu Mono / JetBrains Mono code (full mono stack, ligatures-off-by-default with `format:ligatures` opt-in); AC-010 gradient H1/H2 (4-property cross-browser contract, token-only stops, accessibility decoupling); AC-011 no-skipped-levels (exactly-one-`<h1>`, monotonic descent, `level`/`as` polymorphic prop requirement).
- Format note bumped to reflect 11/34 ACs now GWT.
- Lockstep §98 v1.1.0 → v1.2.0 + §99 v3.3.0 → v3.4.0 + spec-index updated.

---

## ✅ Phase 15c — Convert §07 §97 Motion & Transitions to GWT (DONE, v3.5.0)

Third slice of the §07 structural conversion. AC IDs preserved:
- §07 §97 banner v3.4.0 → v3.5.0; AC count unchanged at 34 (verified).
- **5 ACs converted (AC-012..AC-016 Motion & Transitions)** from one-row table format (~70 chars each) to full GWT subsections (1703-3816 chars each, **24-54× depth**) with concrete contracts + cross-refs to `06-motion-transitions.md`, `09-button-system.md`, `tailwind.config.ts`, `src/index.css`, `package.json` dependency audit, WCAG 2.1 §2.3.3, MDN `prefers-reduced-motion`.
- AC-012 ≤300ms hover (fixed timing vocabulary {150/200/300ms}, `cubic-bezier(0.4,0,0.2,1)` mandate, symmetric in/out); AC-013 no-JS-animation (exhaustive forbidden list — framer-motion/gsap/lottie/etc — narrow exception allowlist); AC-014 `prefers-reduced-motion` (exact global override with `0.01ms` not `0`, per-component opt-in pattern, scroll/parallax/auto-play disable); AC-015 link underline sweep (`::after` pseudo-element with `right:0` anchor, `position: relative` parent, no-`text-decoration` mixing, focus-visible instant); AC-016 CTA slide text (two-stacked-spans `overflow:hidden` with `translateY`, vertical-only direction, `aria-hidden` on duplicate).
- Format note bumped to reflect 16/34 ACs now GWT.
- Lockstep §98 v1.2.0 → v1.3.0 + §99 v3.4.0 → v3.5.0 + spec-index updated.

---

## ✅ Phase 15d — Convert §07 §97 Code Blocks to GWT (DONE, v3.6.0)

Fourth slice of the §07 structural conversion. AC IDs preserved:
- §07 §97 banner v3.5.0 → v3.6.0; AC count unchanged at 34 (verified).
- **9 ACs converted (AC-017..AC-025 Code Blocks)** from one-row table format (~80 chars each) to full GWT subsections (2100-4200 chars each, **26-52× depth**) with concrete contracts + cross-refs to `07-code-blocks.md`, `02-theme-variable-architecture.md`, `src/index.css` (lines 264–605), `src/components/markdown/codeBlockBuilder.ts`, AC-001/AC-012/AC-014.
- AC-017 fixed-dark-bg contract (static HSL, exception to token-only rule); AC-018 language badge (7px dot + 10-language color mapping, `--lang-accent` injection); AC-019 font-size controls (12-32px bounds, `localStorage` persistence, 150ms animate); AC-020 line pin (React state toggle, 3 visual markers, hover-vs-pin precedence); AC-021 shift-click range (bidirectional, idempotent, selection bar trigger); AC-022 fullscreen (2rem inset, backdrop overlay, `z-index` stack, scale animation); AC-023 Escape exit (immediate, restore all state, cleanup listeners, `beforeunload` safeguard); AC-024 copy button (Clipboard API + fallback, 2s success state, `aria-live`); AC-025 tree prefixes (📁/📄 emoji, guide characters, "STRUCTURE" label).
- Format note bumped to reflect 25/34 ACs now GWT.
- Lockstep §98 v1.3.0 → v1.4.0 + §99 v3.5.0 → v3.6.0 + spec-index updated.

---

## ✅ Phase 15e — Convert §07 §97 Navigation + Page Consistency to GWT (DONE, v3.7.0) — §07 §97 CONVERSION COMPLETE

Final slice of the §07 structural conversion. AC IDs preserved:
- §07 §97 banner v3.6.0 → v3.7.0; AC count unchanged at 34 (verified: AC-001..AC-034 sequential, zero gaps).
- **9 ACs converted (AC-026..AC-030 Navigation + AC-031..AC-034 Page Consistency)** from one-row table format (~70 chars each) to full GWT subsections (1900-3500 chars each, **27-50× depth**) with concrete contracts + cross-refs to `08-header-navigation.md`, `10-sidebar-system.md`, `11-section-patterns.md`, `12-page-creation-rules.md`, `tailwind.config.ts`, `index.html`, `src/components/ui/sidebar.tsx`, AC-001/AC-007/AC-008/AC-009/AC-010/AC-012/AC-014/AC-026/AC-029, WCAG 2.1 §1.3.1/§2.4.7/§2.5.5.
- AC-026 header icon scale (1.05 hover + 0.95 active, no-bounce); AC-027 menu gradient underline (`::after` + `transform-origin` flip, heading-gradient tokens); AC-028 dropdown primary-tinted hover (0.08 alpha + primary text); AC-029 mobile Sheet (slide from left at 200ms, backdrop no-blur, auto-close on file-select/escape/outside-click/breakpoint-grow); AC-030 Ctrl+B toggle (global window listener, input-guard, localStorage persistence, mobile opens Sheet); AC-031 section pattern composition (Header → Hero → N×Section → CTA → Footer, no ad-hoc layouts); AC-032 font registry enforcement (only Ubuntu/Poppins/Mono, no per-page loading, no inline `style="font-family"`); AC-033 state language (REQUIRED hover+active+focus-visible+disabled, `--ring` token NEVER `--primary`, 2px min); AC-034 responsive breakpoints (md/lg, mobile-first, 44px touch targets, no horizontal scroll).
- **Format note bumped to reflect 34/34 ACs now GWT — conversion COMPLETE.** Zero table rows remain in §07 §97.
- Lockstep §98 v1.4.0 → v1.5.0 + §99 v3.6.0 → v3.7.0 + spec-index updated.

---

## ✅ Phase 16a — Deepen §13 generic-cli §97 with module-specific GWT ACs (DONE, v2.0.0)

First module deepening pass after §07 §97 conversion completed:
- §13 §97 banner v1.0.0 → **v2.0.0** (major bump because AC count tripled and the new ACs validate a different surface — the CLI implementation — distinct from the original 5 which validate the spec module structure).
- **15 new GWT ACs added (AC-06..AC-20)**, AC-01..AC-05 preserved verbatim.
- AC-06 single-switch subcommand dispatch (no cobra/urfave); AC-07 kebab-case per-command flagsets + flag-name constants; AC-08 three-layer config precedence (defaults → JSON file → flags) + flat-JSON-only contract; AC-09 pluggable `--format` (terminal/json/csv/markdown) + TTY-detect color suppression + RFC-4180 CSV; AC-10 fixed five-value exit code contract (0 success, 1 generic, 2 misuse, 3 config, 4 batch partial) + stderr discipline; AC-11 50-line function / 400-line file / camelCase-PascalCase / no-magic-strings code style; AC-12 compile-time `//go:embed` help + interception before flag parse; AC-13 `pkg/dateformat/` three layouts (display `2006-01-02 15:04:05 MST`, filename `2006-01-02-150405`, ISO8601 RFC-3339); AC-14 `pkg/constants/` category split (flags/commands/paths/formats/exit) + `<Category><Name>` naming; AC-15 `--verbose` to stderr + secret redaction + zero-overhead when disabled; AC-16 progress to stderr + 500ms appearance + non-TTY suppression; AC-17 batch `exec` exit-4-on-partial + `[item]` prefix + deterministic parallel; AC-18 generated-not-handwritten shell completion + hidden `__complete` provider; AC-19 fixed terminal palette (green/red/yellow/cyan/gray) + box-drawing headers + ASCII fallback; AC-20 post-install `doctor` + interactive shell-profile injection + `--json` mode.
- Lockstep §98 v1.0.0 → v1.1.0 + §99 v1.0.0 → v1.1.0 + spec-index updated.

---

## ✅ Phase 16b — Deepen §14 update §97 with module-specific GWT ACs (DONE, v2.0.0)

Second module deepening pass:
- §14 §97 banner v1.0.0 → **v2.0.0** (major; AC count 5 → 20).
- **15 new GWT ACs added (AC-06..AC-20)**, AC-01..AC-05 preserved.
- AC-06 rename-first deploy (Windows-locked-file workaround, atomic same-dir rename, uniform across platforms); AC-07 detached `updater.exe` handoff (CREATE_NEW_PROCESS_GROUP|DETACHED_PROCESS, parent-PID poll, self-delete, log to `%TEMP%`); AC-08 three-branch version verification (deployed/source/declared, build-time `-ldflags -X main.Version` injection, no runtime `version.txt`); AC-09 mandatory code signing (Authenticode `signtool verify /pa`, macOS codesign+notarize, Linux GPG `.sig`, fail-on-unsigned, 30-day cert-expiry warning); AC-10 SHA-256 checksums.txt + verify-before-install (MD5/SHA-1 forbidden, signed checksums fingerprint); AC-11 idempotent install scripts (`%LOCALAPPDATA%\Programs`, `~/.local/bin`, `/usr/local/bin`, no-sudo-by-default, opt-in PATH modification); AC-12 latest-version probe (`releases/latest`, `--version=X.Y.Z` pin, no fallback guess, User-Agent); AC-13 XDG-compliant config (`$XDG_CONFIG_HOME/<binary>/update.json`, flat JSON per §13 AC-08, atomic .tmp+rename writes, 0600 perms); AC-14 ten-step `update` workflow (network → probe → compare → .partial → SHA-256 → signature → .new → detached spawn → exit ≤100ms → swap); AC-15 non-blocking 12h pre-command-hook (fire-and-forget detached child, NO daemon/cron, JSON fallback store, banner on next invocation); AC-16 startup cleanup (.old + stale .partial + old .log, silent failures, idempotent, ≤100ms cap); AC-17 atomic rollback (rename .old back, RECOVERY.md fallback if rollback itself fails); AC-18 deploy path resolution (default → build.json → --deploy-path, refuse system dirs, perm check); AC-19 `git describe --tags` last-release detection (commit-count/branch-name forbidden, conventional-commits drives bump); AC-20 cross-compilation matrix (windows/amd64+arm64, linux/amd64+arm64, darwin/amd64+arm64, CGO_ENABLED=0, `-ldflags -s -w`, fail-on-partial).
- Lockstep §98 v1.0.0 → v1.1.0 + §99 v1.0.0 → v1.1.0 + spec-index updated.

---

## ✅ Phase 16c — §22 git-logs §97 depth pass on AC-04/AC-05/AC-25/AC-34 (DONE, v3.9.0)

Closed the four lean ACs Phase 13 explicitly deferred. AC IDs preserved (still 75; AC-04/AC-05/AC-25/AC-34 grew 10-15× in depth):
- §22 §97 banner v3.8.13 → **v3.9.0**.
- AC-04 logger gating (constant-time integer compare at call boundary, sink-side filtering forbidden, request-scoped cache, 6-level fixed `Trace=0..Fatal=5`); AC-05 dedup window (rolling 60s from FIRST hit, fingerprint = source+level+template+ctx_hash, error/fatal carve-out, process-local LRU bounded at 1024, `[deduped: N]` suffix on expiry); AC-25 `format:hide` omitted from DOM entirely (not CSS-hidden — defense-in-depth against view-source/DevTools/screen-reader/session-replay leakage, server-side-only omission, consistent across all projections, empty parent containers must collapse); AC-34 multisite per-site DB (per-`blog_id` SQLite file at `wp_upload_dir()` path, shared file forbidden even network-activated, `switch_to_blog`/`restore_current_blog` connection invalidation, per-site lazy migration, `wp_delete_site` cleanup).
- Lockstep §98 v3.9.0 row added + §99 v3.8.13 → v3.9.0 + spec-index updated.

---

## ✅ Phase 16d-i — §15 distribution-and-runner §97 deepen (DONE, v2.0.0)

Expanded §15 §97 from 5 generic scaffold ACs (AC-01..AC-05 retained as universal floor) to **20 module-specific GWT ACs** (AC-06..AC-20 added). Each new AC averages 1500-2200 chars with explicit `**Given** / **When** / **Then**` triplet plus `**Verifies:**` cross-ref.
- §15 §97 banner v1.0.0 → **v2.0.0**.
- New ACs: AC-06 installer one-liner shape (Bash+PS parity, idempotent, dep pre-check, exit `1`/`2`/`3`/`4`, 60s SLO); AC-07 default 4-folder layout pinned to release SHA (additive, `--force` to overwrite); AC-08 install-config.json strict schema + lockstep-with-§00 CI gate; AC-09 byte-identical Bash↔PS parity + shared 7-flag surface; AC-10 runner sub-cmd dispatch (4-row contract from §00, unknown=exit `2`, post-cmd flag forwarding); AC-11 back-compat for legacy no-args (no banners, removal needs major + 2 deprecation cycles); AC-12 8-artifact release set (filenames exact, missing any blocks release); AC-13 checksums.txt format (`sha256sum`-compat, installers MUST verify before extract = supply-chain protection, mismatch=`4`); AC-14 linters-install.sh rename (avoids collision with top-level install.sh); AC-15 install destination defaults (EACCES detected pre-download, refuses install into source repo with symlink resolution); AC-16 release pipeline (tag-driven, pinned to tag's SHA not branch HEAD, atomic publish, no auto-publish to npm/PyPI); AC-17 slides browser-open (OS-appropriate, `--no-open` skip, `Ctrl-C` exits `0` not `130`); AC-18 `--ref` reproducible install (tag-or-full-SHA only, branches forbidden); AC-19 cross-refs intact + lockstep maintenance with §12/§13/§16/spec-slides; AC-20 sibling files versioned + `**Verifies:**` MUST cite both §00 and the relevant sibling.
- Lockstep: §98 v2.0.0 row added + §99 v1.0.0 → v2.0.0 + spec-index 3 cells bumped.
- Tree-health: 100/100 (A+) maintained.

---

## ✅ Phase 16d-ii — §16 generic-release §97 deepen (DONE, v2.0.0)

Expanded §16 §97 from 5 generic scaffold ACs (AC-01..AC-05 retained) to **20 module-specific GWT ACs** (AC-06..AC-20 added). Harmonized with §15 AC-12/13/16/18 — citation-only, no edit propagation. §16 is the upstream generic blueprint; §15 is the concrete consumer.
- §16 §97 banner v1.0.0 → **v2.0.0**.
- New ACs: AC-06 cross-comp matrix (6 minimum targets, `CGO_ENABLED=0`, build-once); AC-07 tag-driven trigger (no `main`/PR/schedule, SHA-pinned); AC-08 atomic publication (draft → verify-roundtrip → promote, no auto-publish to npm/PyPI); AC-09 asset naming (`<binary>-<version>-<os>-<arch>.<ext>`, flat archive, Go runtime tokens, `0755`, no symlinks); AC-10 release-metadata.json schema (required keys, `-ldflags -X` version, assets-superset-of-checksums); AC-11 version-pinned installers (no `/releases/latest` probe, spec-first ordering, deterministic re-gen); AC-12 SHA-256 protocol (`sha256sum`-compat, install-time verify before extract, signing-tool-agnostic); AC-13 PATH activation (idempotent fenced-marker block, `doctor` self-heal, no system-wide without `--system`); AC-14 terminal output (stderr for progress, `NO_COLOR` honored, color-when-TTY); AC-15 known-issues ledger (`REL-NNN` IDs, prevention rule REQUIRED in same fix PR, generalizable rules promote to siblings); AC-16 Mermaid diagrams (parseable by `mmdc`, cover all six referenced specs, `.mmd` source separate from `.svg` artifact); AC-17 generic-vs-concrete separation (placeholder convention preserved, consumer ACs cite generic ACs, deviations require justification); AC-18 Bash+PS installer parity (functionally equivalent, OS-conventional defaults, shared 6-flag surface, OS-mismatch detection, third installer flavor forbidden); AC-19 cross-refs intact + bi-directional (back-refs to §12/§13 encouraged); AC-20 sibling files versioned + content-aligned (§08 marked authoritative wins over §03 on installer questions).
- Lockstep: §98 v2.0.0 row added + §99 v1.0.0 → v2.0.0 + spec-index 3 cells bumped.
- Tree-health: 100/100 (A+) maintained.

---

## ✅ Phase 16d-iii — §17 consolidated-guidelines §97 deepen (DONE, v2.0.0)

Expanded §17 §97 from 5 generic scaffold ACs to **20 module-specific GWT ACs** (AC-06..AC-20 added; AC-01..AC-05 preserved). Lockstep §98 v2.0.0 + §99 v4.0.0 + spec-index updated. Tree-health: 100/100 (A+).

---

## ✅ Phase 16d-iv — §27 spec-toolchain §97 deepen (DONE, v2.0.0)

Expanded §27 §97 from 10 ACs (AC-T-01..AC-T-10) to **20 module-specific GWT ACs** (AC-T-11..AC-T-20 added; AC-T-01..AC-T-10 preserved verbatim). New ACs cover: stderr-vs-stdout discipline (AC-T-11), filler tight-loop idempotency (AC-T-12), generator determinism + content-derived timestamps (AC-T-13), auditor JSON output contract (AC-T-14), config self-validation + bidirectional spec-config links (AC-T-15), runner cross-platform pipeline equivalence (AC-T-16), trace-map round-trip + FORBIDDEN-ideas hard-block per `mem://constraints/forbidden-trace-map-ideas` (AC-T-17), Python+Go twin byte-equivalence (AC-T-18), CI workflow trigger-path completeness + threshold lock at 100 (AC-T-19), `trace-map.md` informational-not-spec status with slot 80+ reservation (AC-T-20). Lockstep: §98 v2.0.0 row added + §99 v1.1.0 → v2.0.0 + spec-index regenerated (3 cells bumped). Tree-health: 100/100 (A+) maintained.

---


## ✅ Closed backlog (resolved)
- **Phase B1** — §07 App identity fields: CLOSED Phase 147 (locked decision 12 PERMANENT — Env/Platform/OwnerEmail forbidden).
- **Phase B2** — Slot-06 collision in `02-coding-guidelines/`: CLOSED Phase 47 via **co-location** (both `06-ai-optimization/` + `06-cicd-integration/` retain slot 06 per §16→§37 immutability precedent — once a slot ships a §97, the slot label is frozen). User confirmed 2026-04-28: honor Phase 47, no rename. Disambiguation by trailing slug. **Do NOT re-surface this in future `next` cycles.**
- **Phase 17** — §99 consistency-report deepening sweep: CLOSED Phase H14 2026-04-28 via **H10 deferral** (1/3 criteria met — tree-health 168/168, 6 candidate scaffolds are `freshness-exempt: audit-log-only` by contract, deepening would duplicate parent inventory blocks violating Phase 135 single-source rule). User confirmed defer. Right intervention for richer per-leaf §99 content is Phase H1's opt-in `verified-phase` stamp on parent §99 `## Summary`, not bulk-deepening of audit-only stubs. **Do NOT re-surface in future `next` cycles.**
- **Phase 18** — Tree-health drift sweep: CLOSED 2026-04-28. Tree-health gate held 168/168 strict, but expanded scope to all 5 sister gates caught **trace-map drift +2 ACs** (`ac_total:1320→1322`, `ac_drifted:1230→1232`, `ac_traced:90` flat, `code_orphan:26` flat). Rebaselined within 50-AC inspection budget. Memo: `phase-18-tree-health-drift-sweep.md`. Ambiguity logged: `01-trace-map-plus-2-untraced-acs.md`. **Lesson: drift sweeps MUST run all 5 sister gates, not just the named one** — sister-gate drift is independent of tree-health.
- **Phase 18-resolution** — Root-caused the +2 ACs to **stale baseline** (not new ACs); H5/H7 baseline writes against unsynced trace-map.json. Atomicity rule codified: never hand-edit `trace-map-baseline.json`; always go through `--update-baseline` (which re-runs generator first). Ambiguity logged: `02-stale-baseline-ci-guard.md` (H10 3/3 candidate, deferred to user review).
- **Phase 19** — Stale-baseline advisory: CLOSED 2026-04-28. Implemented Ambiguity-02 **option 3** (linter advisory inside existing gate). `check-trace-map-regression.py` now compares current vs baseline `ac_total`/`code_total` (tree-shape invariants); on mismatch emits `::warning::stale-baseline drift` to stderr without changing exit code. CI gate count unchanged at 15. RUBRIC unchanged. Memo: `phase-19-stale-baseline-advisory.md`. **Lesson: "advisory inside an existing gate" is a viable lower-ceremony pattern for H10 3/3 findings when failure mode is detector-friendly but not worth a 16th gate.**
- **Phase 20** — README stale-prose sweep: CLOSED 2026-04-28. Audited `linter-scripts/test/README.md` per Phase 19 close-out rec (b) — F3 codification confirmed correctly landed; surfaced 5 stale-prose narrative bugs from 7→8→10 self-test growth (parity gate covers inventory table, not narrative restatements). Fixed: "all eight wired"→"all ten reachable" + named the 3 broader-contract gates (H1/H5/H7) hosting tests 8/9/10; coverage-triad table gained 3 rows for §99-freshness/stamp-bump/archive-runtime blind spots; "seven tests"→"ten tests"; "Phase F2 blocked on F1"→accurate (F1+F2 both closed); local-execution block + "Run all N" updated. `test-readme-inventory.sh` (26 pass) + `test-overview-inventory-parity.sh` (6 pass) intact. No new gate, no AC-31-31 cascade. Memo: `phase-20-readme-stale-prose-sweep.md`. **Lesson candidate**: README narrative-count drift ("The N tests…", "Run all N…", "Add an Nth…") is a recurring class not covered by inventory parity gates — possible future H10 if it recurs (currently 1/3, single historical incident).
- **Phase 21** — §00-overview stale-prose sweep: CLOSED 2026-04-28. Audited `spec/27-spec-toolchain/00-overview.md` per Phase 20 close-out rec (b). Two findings: (1) banner stuck at v1.7.0 / 2026-04-27 while §98 was at v2.46.2 / 2026-04-28 (~39 patch releases behind); lockstep didn't catch because L1 rule is `§98 latest release date >= §00 Updated date` (date relation), not version-string parity. (2) Slot-70 description "Wires §05 + §10 into GitHub Actions (event-driven)" frozen at original 2-script wiring era; workflow now wires 17 production gates + 7 self-test steps. Fixed both. §98 v2.46.2 → v2.46.3, §99 v2.43.2 → v2.43.3 (lockstep). No new gate, no AC-31-31 cascade. Verified: lockstep 87/87 / 0 ✅, tree-health 168/168 strict ✅, §27-inventory 6/6 ✅, freshness `--strict-position` 0 stale / 0 misplaced ✅. Memo: `phase-21-overview-stale-prose-sweep.md`. **Lesson candidate**: Version-field drift between §00 and §98 is invisible to lockstep when date relation is technically OK — second narrative-stale class found in 2 phases (Phase 20 = README counts, Phase 21 = banner versions). Both are 1/3 H10 individually but the **pattern** suggests a future "narrative-claims advisory" sister to Phase 19's stale-baseline advisory if a third instance surfaces.
- **Phase 22** — Banner-drift fleet sweep: CLOSED 2026-04-28 (No-Questions Mode 6/40). Per Phase 21 close-out rec (a), wrote `/tmp/banner_drift.py` and scanned all 23 modules carrying both `00-overview.md` + `98-changelog.md`. **Result: 0 drift fleet-wide.** §27 (Phase 21) was the only historical case. **Decision: H10 candidate REJECTED** — no active regression surface = no new gate. Single-incident bugs belong in memory, not CI. **Lesson codified**: before authoring a new lint, run a one-shot fleet sweep to confirm population > 1. Memo: `phase-22-banner-drift-sweep.md`. No spec files touched (read-only sweep).
- **Phase 23** — Root spec/00-overview.md audit: CLOSED 2026-04-28 (No-Questions Mode 7/40). Per Phase 22 close-out rec (b); rec (a) target `linter-scripts/README.md` does not exist (only `readme-cross-links.md` config artifact). Three checks: banner parity (✅ both v3.5.0/2026-04-27), inventory bijection (✅ 23 active + 2 locked-vacant + 1 archived = 26 rows), narrative count drift (✅ zero count claims — root overview is purely table-driven). **No-op sweep**, narrative-claims advisory H10 candidate stays at 2/3 (no third instance contributed). Memo: `phase-23-root-overview-audit.md`. **Lesson**: table-driven inventories with no narrative count are immune to the README-N-tests drift class — pattern worth promoting if the issue recurs.
- **Phase 24** — CONTRIBUTING.md drift sweep: CLOSED 2026-04-28 (No-Questions Mode 8/40). Per Phase 23 close-out rec (a). Scanned `CONTRIBUTING.md` (126 lines), `README.md` (3-line Lovable placeholder, N/A), `readme.txt` (2 lines, no narrative). Found 3 drift hits: L9 banner phase ("Phase 86" → "Phase 147 / v2-det Phase 23"), **L52 version triple ("v1.8.0, script v2.15" → "v1.23.0, script v2.17, RUBRIC v2.26") = high severity** (3 fields all stale ~15 patches behind), L117 phase-range examples expanded to include 18-23. Verified non-drift: L5/L23 "the four CI gates" is intentional contributor-scoping (not 15), L102 "87-module corpus" matches `audit-spec-vs-code-v2.py` actual `[87/87]` output (different from tree-health 56). **H10 narrative-claims candidate GRADUATED to 3/3 then REJECTED**: 3 instances confirmed (Phase 20 + 21 + 24) but too heterogeneous for one detector — version-triple is freeform prose, not header-checkable. **Lesson codified: H10 graduation requires N instances PLUS shared mechanical signature**; pre-test "would one regex catch all 3?" before counting toward 3/3. Lightweight memory rule recorded: when bumping audit script version / RUBRIC / §31 spec version, grep `CONTRIBUTING.md` for old triple. Memo: `phase-24-contributing-drift-sweep.md`. No spec lockstep cascade (CONTRIBUTING is not §spec scope).
- **Phase 25** — Multi-target close-out sweep: CLOSED 2026-04-28 (No-Questions Mode 9/40). Per Phase 24 close-out recs (a)+(b)+(c) batched. Scanned `.github/PULL_REQUEST_TEMPLATE.md` (46 lines), `.github/workflows/spec-monthly-audit.yml` (130 lines), `spec/folder-structure-root.md` (33-line redirect). **All 3 clean**: PR template "all four" is same intentional contributor-scoping as CONTRIBUTING; monthly-audit "rubric v2.0.0" refers to TREE-HEALTH rubric (`check-tree-health.cjs` line 131 still v2.0.0) NOT audit `RUBRIC_VERSION = "v2.26"`; folder-structure-root is pure 33-line redirect. **Bonus lesson**: in-context Core memory summary appeared to say "CI gate count 15" but on-disk `.lovable/memory/index.md` line 13 already says "**17**" — context summary is auto-truncated, can lag the full file. Filed Ambiguity-03 as self-resolved. Memo: `phase-25-multi-target-closeout.md`. **Stale-prose sweep cycle (Phases 18-25) CLOSED**: 8 phases, 1 false-positive (P18), 4 with fixes (P19/20/21/24), 3 clean no-ops (P22/23/25). Net: drift exists but is rare, heterogeneous, and not mechanically detectable by single regex. Future sweeps should be **version-bump-triggered** (audit / RUBRIC) not periodic cadence.
- **Phase 26** — F3 "Adjacent .py tests" subsection verification: CLOSED 2026-04-28 (No-Questions Mode 10/40). Per Phase 25 close-out rec (c). Confirmed `linter-scripts/test/README.md` properly segregates the F3 sanctioned exception: F3 narrative intact (L107-132), "Adjacent `.py` tests" H3 present (L136), 1 row for `test-check-spec-folder-refs.py` matches 1 filesystem `.py` test, main inventory has 10 `.sh` rows matching 10 filesystem `.sh` tests. Both parity gates pass: `test-readme-inventory.sh` 26/26 ✅, `test-overview-inventory-parity.sh` 6/6 ✅. **No-op verification**, F3 codification has held since Phase 146. Memo: `phase-26-f3-adjacent-py-verify.md`. **Lesson**: when Core memory codifies a sanctioned-exception class, periodic verification confirms the pattern is working as designed (low-cost insurance against silent regression).
- **Phase 27** — Root §97 AC-ROOT-01..08 freshness verification: CLOSED 2026-04-28 (No-Questions Mode 11/40). Per Phase 26 close-out rec (c). Cross-checked all 8 root ACs against current `spec/00-overview.md` + filesystem: AC-01 (26-row bijection ✅), AC-02 (slots 08/09 locked ✅), AC-03 (SpecTreeIndex JSON-Schema present ✅), AC-04 (Slug+Path patterns ✅), AC-05 (Status enum exact match line 100 ✅), AC-06 (4 Supporting Files exist + listed ✅), AC-07 (`kind: index` frontmatter + AC-31-15 ref ✅), AC-08 (lockstep 0 findings ✅). Banner alignment: §00/§97/§98 all 2026-04-27, lockstep gate strict-pass. **No-op verification**. Memo: `phase-27-root-ac-verify.md`. **Lesson codified**: root-module ACs are stable because they describe **structural invariants** (bijection, locked slots, schema enforcement); module-level §97 files often embed numeric thresholds requiring more maintenance. **Pattern**: write structural-invariant ACs at root, defer numeric-bound ACs to module-level §97 close to source.
- **Phase 28** — `spec/health-dashboard.md` freshness sweep: CLOSED 2026-04-28 (No-Questions Mode 12/40). Per Phase 27 close-out rec (b). Audited dashboard prose vs canonical `spec/dashboard-data.json`. **8 fields drifted**: Generated 2026-04-25→2026-04-27, Folders 80→87, Modules 52→56, Required 104/104→112/112, Recommended 104/104→112/112; added Quality (167/168) + Rubric Version (2.0.0) rows; allowlist count "12" → **9** (corrected — the "12" double-counted 3 narrative-only rows like `mem://`/`dashboard-data.json` not in `EXTERNAL_REPO_PREFIXES` source array). Bumped `health-dashboard.md` v3.7.7 → **v3.7.8** + appended 2 Validation History rows. Lockstep §98 bumped 3.5.0 → **3.5.1**, Updated 2026-04-27 → 2026-04-28. Both gates green: lockstep 87/87 · 0 findings; tree-health 100/100 strict 56/56. Memo: `phase-28-health-dashboard-freshness.md`. **Lessons**: (1) supporting files drift too — Core memory's lockstep rule only protects banner+changelog+health surfaces; `health-dashboard.md` and similar prose-summary files accumulate drift between regenerator runs; add to periodic-sweep candidate list. (2) Future enhancement: have `generate-dashboard-data.cjs` also patch the dashboard.md banner+breakdown table (analog to spec-index auto-regen) — out of scope here. (3) Allowlist-count drift is silent (no CI gate compares the markdown table to the JS source array); flag for hardening if a 3rd instance appears.
- **Phase 29** — `spec/spec-index.md` regen + advisory-gate root-cause: CLOSED 2026-04-28 (No-Questions Mode 13/40). Per Phase 28 close-out rec (b). Regenerated `spec/spec-index.md` (877→**883 files**, 1042→1048 lines, +6 §27 slots: 18, 19, 25, 26, 27, 28). Flushed 12 stale version entries accumulated since Phase 145+. **Root cause identified**: `.github/workflows/spec-health.yml` line 63 step is **advisory** — prints `⚠️` warning and `exit 0` on drift. Phase 30 QUEUED = strict-promote + AC-31-31 cascade. Following H4→H5 "don't rush AC-31-31" playbook. Lessons: (1) advisory CI gates silently rot; (2) generator artifacts in `run.sh` need CI parity; (3) AC-31-31 cascade discipline. Memo: `phase-29-spec-index-regen.md`.
- **Phase 30** — Spec-index drift gate strict-promotion (full AC-31-31 cascade): CLOSED 2026-04-28 (No-Questions Mode 14/40). Per Phase 29 close-out rec (a). Promoted the existing `Regenerate spec-index.md (drift check)` workflow step from advisory (`⚠️` warn + exit 0) to **strict** (`exit 1` on `git status --porcelain spec/` delta). Step renamed `Spec-index drift gate` for naming consistency with F2/H7 peers. **AC-31-31 cascade across 9 sites**: (1) `audit-spec-vs-code-v2.py` `RUBRIC_VERSION` v2.26→**v2.27**; (2) same script footer enumeration "17 strict CI gates"→**"18"**, added entry **#18** (Spec-index drift gate, Phase 30, AC-T-25); (3) EXECUTIVE-SUMMARY back-ref `+ 30` appended; (4) `test-qa-baseline-footer.sh` workflow-gates awk +1 (`/Spec-index drift gate/`); (5) `.github/workflows/spec-health.yml` step rename + advisory→strict; (6) `27-spec-toolchain/00-overview.md` slot-70 description "17"→"18 production gates" + Version v2.46.3→**v2.47.0**; (7) `97-acceptance-criteria.md` v2.2.0→**v2.3.0**, added **AC-T-25** codifying the strict-promotion contract + Phase 29 lesson; (8) `98-changelog.md` v2.46.3→**v2.47.0** new release entry; (9) `99-consistency-report.md` v2.43.3→**v2.44.0** new prepended blockquote. Parity 18/18/18 (script=footer=workflow). **Stamp-numbering edge case**: stamping §27 §99 with session-local "Phase 30" caused freshness-gate (delta 117) and stamp-bump-gate failures because validator's `detect_current_phase()` returns global max=147 from mem-index+§27 changelog. Resolution: kept stamp at 147 (global head). **NEW LESSON CODIFIED** in Ambiguity-04 + AC-T-25 + Phase 30 memo as #4: **session-local phase counters MUST NOT collide with global integer sequence used by `detect_current_phase()`** — when stamping a §99 in a session-local counter session, use the global current_phase (147) value, not the session-local number; session-local names belong in narrative prose only (max() ignores them since they're lower than global head). All 11 gates green: lockstep 87/87/0 ✅; tree-health 168/168 strict ✅; QA-baseline-footer 11/11 (18/18/18) ✅; §27-inventory 6/6 ✅; README-inventory 26/26 ✅; freshness 81 stamped/0 stale ✅; stamp-bump 1/1 bumped ✅; archive-exclusion 10/10 ✅; spec-index regen 0 delta ✅; audit mean 98.0/99.8 ✅; sha256 stable post-rollover. Memo: `phase-30-spec-index-strict-promotion.md`. Ambiguity: `04-session-local-phase-vs-global.md` (self-resolved, codified). **Lessons**: (1) advisory→strict promotion always triggers AC-31-31 cascade if the gate counts toward the QA-baseline footer — H4→H5 split pattern works; (2) session-local naming + project-wide validators need explicit reconciliation rule (Ambiguity-04); (3) the new gate's first real test fires on the next contributor commit that bumps a tracked version without local `bash linter-scripts/run.sh` — Phase 29 already flushed the backlog so this commit's regen produced 0 delta.
- **Phase 31** — Advisory CI step sibling scan (NO-OP): CLOSED 2026-04-28 (No-Questions Mode 15/40). Per Phase 30 close-out rec (b). Hypothesis: Phase 29 advisory-rot pattern likely has siblings in spec-health.yml. Method: enumerated all 24 run: steps; grepped for || true, continue-on-error, exit 0, || echo. **Findings**: 5 || true hits — ALL in cosmetic Summary step (if: always(), lines 311/314/317/320/323) writing to GITHUB_STEP_SUMMARY AFTER all real gates; correct usage, NOT rot pattern. Self-heal step (line 57) inspected — [ -f X ] && node X chain fails on script error or missing script; defensible. **Verdict**: hypothesis disproven, no remediation. **Lesson codified**: || true acceptable ONLY in if: always() summary aggregators; any || true on real validation IS Phase 29 rot pattern and MUST be strict-promoted or commented with phase-ref. No spec edits, no version bumps, no AC changes, no CI changes. Memo: phase-31-advisory-sibling-scan.md.
- **Phase 32** — Memory Core staleness sweep & refresh (memory-only): CLOSED 2026-04-28 (No-Questions Mode 16/40). Per Phase 31 close-out rec (a). Reconciled Core memory line 13 with live state after Phases 28→29→30→31 advanced gate count to 18 and RUBRIC to v2.27. **Stale → Live**: gate count 17→**18**; RUBRIC v2.26→**v2.27**; footer parity 18/18/18 explicit; removed obsolete Phase 19 parenthetical "production CI gates remain 15". **Promoted to Core**: (1) Phases 28–31 close-out one-liners (dashboard freshness; spec-index regen + advisory-rot root-cause; strict-promotion + AC-31-31 cascade; sibling scan NO-OP); (2) **Ambiguity-04** — session-local phase counters MUST NOT be used as `<!-- verified-phase: NNN -->` stamp values; stamp with global `detect_current_phase()` value (currently 147); (3) **Phase 31 CI hygiene rule** — `|| true` / `continue-on-error: true` acceptable ONLY in `if: always()` summary aggregators; on real validation IS the Phase 29 advisory-rot pattern. **Verification**: lockstep 87/87/0 ✅; tree-health 168/168 strict ✅; QA-baseline-footer 11/11 (18/18/18) ✅. Zero spec edits, zero CI changes, zero version bumps. **Lesson codified for future phases**: Memory Core freshness sweep cadence — after any phase that bumps a project-wide invariant (RUBRIC, gate count, tree-health score, lockstep count, audit means), the next-but-one phase SHOULD be a Core sweep. Two-phase lag is deliberate. **Sub-lesson (this phase)**: Python-via-`bash -c '...'` heredocs with embedded backticks/parens trigger shell command-substitution and silently corrupt content — for memory edits with code-fence tokens, prefer `code--write` / `code--line_replace` over `code--exec` python. Memo: `phase-32-core-memory-refresh.md`.

---

## Status legend
- ✅ done · ⏳ pending · 🚧 blocked

## ✅ Phase 16d-v — §28 universal-ci-cli §97 deepen (DONE, v2.0.0)

Expanded §28 §97 from 28 ACs to **40 module-specific GWT ACs** (AC-28-29..AC-28-40 added; AC-28-01..AC-28-28 preserved). Closed all four v1.1-deferred error codes (`GLCI-EXEC-RUNNER-CRASHED`, `GLCI-EXEC-TIMEOUT`, `GLCI-PUSH-STREAM-BROKEN`, `GLCI-DETECT-MULTIPLE-MODULES`) + added GitLab/Azure/Bitbucket/generic-shell provider auto-fill, telemetry prohibition (Locked Decision #10), streaming buffer cap, per-runtime tool selection (TS/Go/PHP), and direct `glci push-fixed`/`clear` invocation. Lockstep §98 v2.0.0 + §99 v2.0.0 + spec-index regenerated. Tree-health: 100/100 (A+).

---

## ✅ Phase 16e — §02 coding-guidelines §97 deepen (DONE, v4.0.0)

Re-scan of all §97 files surfaced **15 modules with 0 GWT ACs** (table-row scaffolds only). Highest-impact target: **§02 coding-guidelines §97** (the parent governance module for all language subfolders). Rewrote from 22 table-row criteria to **20 module-specific GWT ACs** (AC-CG-01..AC-CG-20) covering numbering ranges, four-required-files rule, six CODE-RED rules (R1–R6), hybrid PascalCase / Rust-snake_case naming policy, AC-count compliance per subfolder, lockstep rule for consolidated review guides, cross-link health, language-vs-cross-language hierarchy, app-specific subfolder boundary, AI-rules canonicalization (`06-ai-optimization`), dependency version pinning, placeholder subfolder remediation, migration-history freshness, module tree-health gate ≥ 95, and recursive self-application (dogfooding). Legacy AC-001..022 preserved as AC-CG-LEGACY-001..022 for traceability. Lockstep: §98 v1.0.0 → v2.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16f — §01 spec-authoring-guide §97 deepen (DONE, v4.0.0)

The meta-spec — governs every OTHER spec in the tree. Rewrote §97 from 18 table-row criteria to **20 module-specific GWT ACs** (AC-SAG-01..AC-SAG-20). Tree-health: **100/100 (A+)**.

## ✅ Phase 16g — §26 gitlogs-diagrams §97 deepen (DONE, v3.0.0)

Completes the §22 Git Logs governance contract. Rewrote §97 from 9 table-row criteria (with 02/03/04 retired as locked gaps) to **20 module-specific GWT ACs** (AC-DG-01..AC-DG-20) covering: ER schema parity with §22 (entities + FK cardinalities, forbidden v1 entities `LogEntry`/`ErrorLogEntry`/`OwnerType`), auth validation locked order with `GL-*` reject codes, RBAC RolePermission-union resolution (never role name), header-comment contract for non-ER diagrams (`%% Diagram type:` + `%% What this answers:` mandatory), emoji-free + Mermaid-CLI rendering, JWT/RS256/JWKS forbidden, 8-endpoint mindmap completeness, encryption v3 7-node derivation chain, slot 02/03/04 locked-gap immutability, `.mmd` ↔ `.svg` build-artifact lockstep, kebab-case ASCII node IDs, `GL-*` codes cross-validated against §22 §14 registry, `puppeteer.json` reproducibility, governance rule **"§26 trails §22 — never leads"**, and self-application audit (AC-DG-20). Legacy AC-D-01..AC-D-11 preserved as AC-DG-LEGACY-* at end of §97. Lockstep: §98 v2.1.0 → v3.0.0 + §99 v2.1.0 → v3.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16h — §02/01-cross-language §97 deepen (DONE, v4.0.0)

Parent contract for ALL language subfolders under §02. Rewrote §97 from 6 stub checkboxes to **20 module-specific GWT ACs** (AC-CL-01..AC-CL-20) covering: inheritance contract + waiver discipline (AC-CL-01), positive boolean naming (AC-CL-02), boolean-flag method prefixes `is`/`has`/`can`/`should`/`will`/`was`/`did` (AC-CL-03), strict typing no implicit any/`interface{}`/`mixed`/`dynamic` (AC-CL-04), typed conversion over raw casts (AC-CL-05), cyclomatic complexity ≤ 10 hard / ≤ 5 preferred (AC-CL-06), nesting depth ≤ 3 (AC-CL-07), magic-value extraction on rule-of-two (AC-CL-08), JSON keys PascalCase wire-format (AC-CL-09), language-idiomatic function names with cross-language semantic-verb consistency (AC-CL-10), DB tables singular PascalCase + columns PascalCase + FK `<TargetTable>Id` (AC-CL-11), kebab-case ASCII slugs (AC-CL-12), explicit nullability typing (AC-CL-13), lazy evaluation for branched expensive computations (AC-CL-14), regex hygiene (AC-CL-15), code mutation avoidance with `mutate*` exception (AC-CL-16), Result/Option/Either over throwing (AC-CL-17), `types/` folder convention forbids `interfaces/`/`models/`/`dto/`/`entities/` (AC-CL-18), `<unit>.test.<ext>` + behavior-named tests (AC-CL-19), DRY rule-of-three forbids premature abstraction (AC-CL-20). Legacy AC-01/AC-02 preserved as AC-CL-LEGACY-* at end. Lockstep: §98 v3.2.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16i — §02/02-typescript §97 deepen (DONE, v4.0.0)

First language child to inherit AC-CL-*. Rewrote §97 from 6 stub checkboxes to **20 module-specific GWT ACs** (AC-TS-01..AC-TS-20) covering: explicit AC-CL-01..AC-CL-20 inheritance (AC-TS-01); 6-flag strict tsconfig including `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` (AC-TS-02); `any` forbidden, `unknown` + narrowing only escape (AC-TS-03); `as const` string-literal-union enums NEVER `enum` keyword (AC-TS-04); `Promise.all` for independent async — CODE-RED rule (AC-TS-05); discriminated unions with `never` exhaustive checks (AC-TS-06); `AppError` discriminated union over `throw new Error` (AC-TS-07); functional components + hooks only (AC-TS-08); Zustand for client / React Query for server — never inverse (AC-TS-09); `async` returns `Promise<Result<T,AppError>>` (AC-TS-10); Zod schema at every external boundary (AC-TS-11); `noUncheckedIndexedAccess` enforces `T | undefined` (AC-TS-12); kebab-case files + PascalCase exports (AC-TS-13); `@typescript-eslint/recommended-type-checked` + `--max-warnings 0` (AC-TS-14); `interface` for shapes / `type` for unions (AC-TS-15); generic constraints required (AC-TS-16); import grouping external→internal-alias→relative + named over default (AC-TS-17); `react-hooks/exhaustive-deps` as error (AC-TS-18); Vitest + RTL behavior-named tests (AC-TS-19); self-application doctest (AC-TS-20). Legacy AC-01/AC-02 preserved as AC-TS-LEGACY-* at end. Lockstep: §98 v3.2.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16j — §02/03-golang §97 deepen (DONE, v4.0.0)

Second language child to inherit AC-CL-*. Rewrote §97 from 6 stub checkboxes to **20 module-specific GWT ACs** (AC-GO-01..AC-GO-20) covering: explicit AC-CL-* inheritance (AC-GO-01); Go 1.22+ pinned toolchain (AC-GO-02); ALL-CAPS acronyms `URL`/`ID`/`HTTP`/`JSON`/`SQL` never `Url`/`Id` (AC-GO-03); `apperror.Result[T]` for project APIs / `(T, error)` for stdlib boundaries (AC-GO-04); `panic` forbidden outside main/init/_test.go (AC-GO-05); `errors.Is`/`As` over `==` or string match (AC-GO-06); `context.Context` first param, never struct field (AC-GO-07); defer placement immediately after acquisition + no unbounded-loop defers (AC-GO-08); `type X string` + `Validate()` enums NOT iota for wire types (AC-GO-09); generics over `interface{}` (AC-GO-10); goroutine cancellation discipline (AC-GO-11); channel direction in signatures, sender owns close (AC-GO-12); 11-linter `golangci-lint` config + CI zero-warning gate (AC-GO-13); 1-3 letter receiver names consistent across type (AC-GO-14); pointer/value receiver consistency (AC-GO-15); explicit `json:"PascalCase"` tags per AC-CL-09 (AC-GO-16); table-driven `t.Run` tests (AC-GO-17); minimal deps + no vendoring (AC-GO-18); `log/slog` over `fmt.Println` (AC-GO-19); self-application doctest (AC-GO-20). Legacy AC-01/AC-02 preserved as AC-GO-LEGACY-* at end. Lockstep: §98 v3.2.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16k — §02/04-php §97 deepen (DONE, v4.0.0)

Third language child to inherit AC-CL-*. Rewrote §97 from 7 table-row criteria (AC-01..AC-07) to **20 module-specific GWT ACs** (AC-PHP-01..AC-PHP-20) covering: explicit AC-CL-* inheritance (AC-PHP-01); PHP 8.1+ + `declare(strict_types=1)` mandatory first statement (AC-PHP-02); string-backed enums with PascalCase cases AND PascalCase values (AC-PHP-03); mandatory `isEqual(self $other): bool` on every enum (AC-PHP-04); `ResultHelper::ok|failed|error|errorWithCode|errorFromException` only on service returns (AC-PHP-05); `ResponseKeyType::Foo->value` array keys, no string literals (AC-PHP-06); role-based identifier casing (AC-PHP-07); boolean `is`/`has`/`can`/`should` camelCase prefix, no snake_case, no negative polarity (AC-PHP-08); `use`-imported globals with no leading backslash, grouped imports (AC-PHP-09); `safeExecute(fn() => ...)` REST wrap + `wp_die()` FORBIDDEN (AC-PHP-10); blank-line discipline before `if`/`throw`/`return` (AC-PHP-11); constructor property promotion + `readonly` for DTOs (AC-PHP-12); type declarations on every parameter and return (AC-PHP-13); `RiseupAsia\Exceptions\BaseException` hierarchy (AC-PHP-14); `phpstan --level=8` + `psalm` zero-issue gate, no baseline files (AC-PHP-15); PSR-4 file-per-class (AC-PHP-16); PHPUnit 10+ `#[Test]` attribute, no `@test` PHPDoc (AC-PHP-17); composer caret-with-patch + `composer.lock` checked in (AC-PHP-18); PSR-3 `LoggerInterface` structured logging (AC-PHP-19); self-application doctest (AC-PHP-20). Legacy AC-01..AC-07 preserved as AC-PHP-LEGACY-* at end. Lockstep: §98 v3.2.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16l — §02/05-rust §97 deepen (DONE, v4.0.0)

Fourth language child to inherit AC-CL-*. Rewrote §97 from 18 stub checkboxes (AC-01..AC-06) to **20 module-specific GWT ACs** (AC-RS-01..AC-RS-20) covering: explicit AC-CL-* inheritance with the SOLE documented AC-CL-12 file-naming waiver (snake_case `.rs` files per Rust convention) (AC-RS-01); Rust 1.75+ + edition pinned + `rust-toolchain.toml` (AC-RS-02); `thiserror` for domain errors / `anyhow` with `.context()` for application + `Box<dyn Error>` FORBIDDEN (AC-RS-03); `panic!`/`unwrap`/`expect`/`todo!`/`unreachable!`/`unimplemented!` FORBIDDEN outside main/tests with clippy deny lints (AC-RS-04); `// SAFETY:` comment + `# Safety` rustdoc on every `unsafe` + `#![forbid(unsafe_code)]` for non-FFI crates (AC-RS-05); Tokio sole runtime, mixing async-std/smol FORBIDDEN (AC-RS-06); Rust API guidelines naming (AC-RS-07); `#[serde(rename_all = "PascalCase")]` per AC-CL-09 (AC-RS-08); bounded `mpsc::channel(N)` only (AC-RS-09); cancellation-safe `tokio::select!` (AC-RS-10); borrow > Arc > clone, `Rc<T>` FORBIDDEN with Tokio (AC-RS-11); AAA tests + trait-mocked OS deps + integration tests in `tests/` (AC-RS-12); `PlatformApi` per-OS modules (AC-RS-13); FFI safety docs + `#[repr(C)]` + null checks (AC-RS-14); `cargo clippy --workspace --all-targets --all-features -- -D warnings` + `clippy::pedantic` + `cargo deny` + `cargo audit` (AC-RS-15); `Cargo.lock` checked in for binaries + caret-with-patch + git deps SHA-pinned (AC-RS-16); `tracing` structured logging + `println!`/`eprintln!`/`dbg!` FORBIDDEN (AC-RS-17); `#![deny(missing_docs)]` + `# Panics`/`# Errors`/`# Safety` rustdoc + doctest compile (AC-RS-18); lifetime elision idiom (AC-RS-19); self-application doctest harness (AC-RS-20). Legacy 18 stubs preserved as AC-RS-LEGACY-* at end. Lockstep: §98 v3.2.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16m — §02/07-csharp §97 deepen (DONE, v4.0.0)

Fifth and final mainstream-language child to inherit AC-CL-*. Rewrote §97 from 38 stub checkboxes (AC-01..AC-07) to **20 module-specific GWT ACs** (AC-CS-01..AC-CS-20) covering: explicit AC-CL-* inheritance with documented AC-CL-12 waiver for `PascalCase.cs` files (AC-CS-01); .NET 8+ LTS + `LangVersion=latest` + `Nullable=enable` + `TreatWarningsAsErrors=true` + `EnforceCodeStyleInBuild=true` (AC-CS-02); .NET naming guidelines, no SCREAMING_SNAKE_CASE consts (AC-CS-03); acronym casing differing from Go: ≥3 letters first-only (`UserId`/`HtmlParser`), 2 letters both-caps (`DbContext`/`IOStream`) (AC-CS-04); boolean prefix `Is`/`Has`/`Can`/`Should`/`Was` + no negative polarity (AC-CS-05); boolean-flag-branching params FORBIDDEN with 3 documented exemptions (AC-CS-06); one type per `PascalCase.cs` file — sole AC-CL-12 waiver (AC-CS-07); body ≤ 15 LOC + ≤ 3 params + options-record for 4+ (AC-CS-08); `Async` suffix + `CancellationToken cancellationToken = default` LAST parameter mandatory (AC-CS-09); `.Result`/`.Wait()`/`.GetAwaiter().GetResult()` FORBIDDEN, async-all-the-way (AC-CS-10); `Task.WhenAll` for independent awaits (AC-CS-11); `Result<T>`/`OneOf<T,Error>` for expected failures (AC-CS-12); `catch (Exception)` and silent swallow FORBIDDEN with documented top-level boundary exemption (AC-CS-13); `ArgumentNullException.ThrowIfNull(x)` + `nameof()` + early-return guard clauses (AC-CS-14); `record` for DTOs + `class` for behavior + `init` setters (AC-CS-15); `object` returns FORBIDDEN, generics + pattern matching only, no business-logic casts (AC-CS-16); `switch` expressions over statements + exhaustive matching + `_ => throw new UnreachableException()` (AC-CS-17); magic strings/numbers FORBIDDEN, use enums/`const`/`static readonly`/typed-record (AC-CS-18); Roslyn + StyleCop + NetAnalyzers + `.editorconfig` at repo root + CI `dotnet build -warnaserror` zero-warning gate (AC-CS-19); self-application doctest harness (AC-CS-20). Legacy 38 stubs preserved as AC-CS-LEGACY-* at end. Lockstep: §98 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

---

## ✅ Phase 16n — §02/06-ai-optimization §97 deepen (DONE, v4.0.0) — **All P1 §97 complete**

Last remaining P1 §97. Rewrote §97 from 7 stub checkboxes to **20 module-specific GWT ACs** (AC-AI-01..AC-AI-20) covering: explicit AC-CL-* + per-language AC-XX-* example-code inheritance (AC-AI-01); 6-language coverage including C# + AI-meta `AH-A*` namespace (AC-AI-02); rule ID regex `^AH-(X|G|T|P|R|C|A)\d+$` + retired-ID immutability (AC-AI-03); mandatory ❌Forbidden+✅Required+Source triplet per rule (AC-AI-04); machine-parsable `- [ ] CHK-NN` checklist with ≥ 50 checks (AC-AI-05); every check links to a rule or canonical spec (AC-AI-06); 7-section common-mistake schema with ≥ 15 entries (AC-AI-07); zero-overlap rule across rules+checks+mistakes per AC-CL-20 (AC-AI-08); condensed master ≤ 200 non-blank non-fence lines for context-window fit (AC-AI-09); enum quick-ref 5-section template per language (AC-AI-10); placeholder-name blocklist (`foo`/`bar`/`baz`/`xxx`/`todo`/`myVar`/`temp`/`data1`) with sole `❌ Before` exemption (AC-AI-11); fabricated-API ban — every imported symbol MUST exist (AC-AI-12); mandatory `AH-A*` AI-meta rules: STOP/scan/verify, no-silent-assumption, ask-when-ambiguous, cite-source (AC-AI-13); closed Severity {low,medium,high,critical} + Frequency {rare,occasional,common} enums (AC-AI-14); checklist 4-section ordering Pre-Output/During/Post-Output/Per-Language (AC-AI-15); language-tagged code fences mandatory, bare ``` FORBIDDEN (AC-AI-16); rule body ≤ 60 lines for atomicity (AC-AI-17); checklist runnable as self-graded test ≥ 90% green-rate (AC-AI-18); cross-language sibling-linking for universal concepts anchored at AC-CL-09 (AC-AI-19); self-application doctest gate (AC-AI-20). Legacy 7 stubs preserved as AC-AI-LEGACY-* at end. Lockstep: §98 v1.0.0 → v4.0.0 + §99 v3.2.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

**🎉 Milestone — Phase 16 P1 batch complete:** All §02 children (cross-language, TypeScript, Golang, PHP, Rust, C#, AI-Optimization) now carry full 20-GWT §97 contracts. The AI-implementer can read any one of these folders and have a self-contained, normative, testable spec without chasing parent docs.

---

## ✅ Phase 16o — §02/06-cicd-integration §97 deepen (DONE, v4.0.0) — **First P2 + B2 collision twin codified**

First P2 §97. Rewrote §97 from 7 prose criteria (AC-CI-001..007) to **20 module-specific GWT ACs** (AC-CI-01..AC-CI-20) covering: explicit AC-CL-* inheritance (AC-CI-01); stock-Ubuntu+python3≥3.10+bash baseline with zero `pip install`/`apt-get install` Phase 1 (AC-CI-02); SARIF 2.1.0 exact-version + schema URL gate (AC-CI-03); POSIX exit codes 0/1/2 only, all others FORBIDDEN (AC-CI-04); check filename regex `^[a-z0-9]+-[a-z0-9-]+\.(sh|py)$` with registered language-id prefix (AC-CI-05); zero-edit plugin addition with PR-template gate (AC-CI-06); plugin manifest TOML 5-required-key contract (AC-CI-07); SARIF rule-ID regex `^[A-Z]{2,4}-[A-Z]{1,3}-\d{1,3}$` (AC-CI-08); dogfooding gate — zero `level: error` against this repo (AC-CI-09); composite Action zero-required-input one-liner UX (AC-CI-10); release ZIP + SHA-256 checksums.txt for every `v*` tag (AC-CI-11); single-source-of-truth `linters-cicd/VERSION` file, hardcoded duplicates FORBIDDEN per AC-CL-20 (AC-CI-12); five mandatory CI templates GitHub/GitLab/Azure/Jenkins/Bitbucket (AC-CI-13); rules-mapping table EVERY-rule-row contract with relative spec-source link (AC-CI-14); closed severity enum {error,warning,note} matching SARIF + AC-AI-14 (AC-CI-15); performance budget single-check<5s + full-run<60s on 10k-LOC fixture (AC-CI-16); middle-out probe ordering by manifest cost tier (AC-CI-17); idempotent + checksum-verified + non-interactive `install.sh` one-liner (AC-CI-18); per-check `_tests/fixtures/{good,bad}/` gate (AC-CI-19); self-application `--self-test` mode (AC-CI-20). Legacy 7 prose criteria preserved as AC-CI-LEGACY-001..007 at end. Lockstep: §98 v1.0.0 → v4.0.0 + §99 v1.0.0 → v4.0.0 + spec-index regenerated. Tree-health: **100/100 (A+)** maintained.

**🚨 B2 collision now fully codified:** Both `02-coding-guidelines/06-ai-optimization/` (Phase 16n) AND `02-coding-guidelines/06-cicd-integration/` (Phase 16o) carry full 20-GWT §97 contracts. Both folders explicitly document the collision in their §97 module summary + §99 consistency report. Resolution requires a user decision (which folder keeps slot `06-`).

---

## Next-pointer
**Phase 16r complete (2026-04-26).** ALL P1 + ALL P2 §97 GWT deepening work is now DONE. The §97 backlog is empty.

Phase 16r landed:
- `spec/06-seedable-config-architecture/97-acceptance-criteria.md` v3.2.0 → **v4.0.0** (20 GWT ACs: AC-SC-01..20 + 2 legacy stubs preserved as AC-SC-LEGACY-001/002).
- `spec/05-split-db-architecture/97-acceptance-criteria.md` v3.2.0 → **v4.0.0** (20 GWT ACs: AC-SD-01..20 + 2 legacy stubs preserved as AC-SD-LEGACY-001/002).
- `spec/06-seedable-config-architecture/98-changelog.md` v1.0.0 → **v4.0.0** (Phase 16r row).
- `spec/05-split-db-architecture/98-changelog.md` v1.0.0 → **v4.0.0** (Phase 16r row).
- `spec/06-seedable-config-architecture/99-consistency-report.md` v3.2.0 → **v4.0.0** (Phase 16r audit row + dual-changelog observation).
- `spec/05-split-db-architecture/99-consistency-report.md` v3.2.0 → **v4.0.0** (Phase 16r audit row + dual-changelog observation).
- `spec/spec-index.md` 6 version cells refreshed for both modules.

**Cumulative §97 GWT inventory (post-16r):** 23 modules at full GWT — §07, §13, §14, §15, §16, §17, §22 (4 deferred deep), §26, §27, §28, §02 root, §01 root, §02/01-cross-language, §02/02-typescript, §02/03-golang, §02/04-php, §02/05-rust, §02/07-csharp, §02/06-ai-optimization, §02/06-cicd-integration, §02/01/16-static-analysis, §14/24-update-check-mechanism, **§06-seedable-config-architecture, §05-split-db-architecture**.

**0 remaining §97 files with 0 GWT ACs** (excluding `_archive/21-git-logs-v1/` which is archived and never edited).

Remaining roadmap work:
- ✅ **Phase B1** — CLOSED Phase 147 (locked decision 12).
- ✅ **Phase B2** — CLOSED Phase 47 via co-location; user re-confirmed 2026-04-28. No further action.
- ✅ **Phase 17** — CLOSED Phase H14 2026-04-28 (H10 deferral; freshness-exempt scaffolds are intentional).

On next `next`: all numbered roadmap backlog resolved through Phase 18. Remaining open work lives in monitor-mode (R1 blocked on Lovable Cloud, R2 session-persistence watch, audit-v5 baseline-drift watch). Future `next` cycles should look for: (e) new spec content additions surfacing new ACs/scripts; (f) any sister-gate drift caught by periodic 5-gate sweep (use Phase 18 as template); (g) deferred items in `.lovable/question-and-ambiguity/` once user reviews them.


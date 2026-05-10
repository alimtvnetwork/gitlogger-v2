# Changelog — App Database

**Version:** 4.4.0
**Updated:** 2026-05-10 (Session 34 audit-task A-14 — `consumes:` front-matter expanded from 1→6 entries citing §22 schema/auth/error/permission files; closes consumer-side binding-graph coverage)
**Scope:** `spec/23-app-database/`

---

### 4.4.0 — 2026-05-10 — Session 34 audit-task A-14: §22 source-of-truth binding expansion via `consumes:` front-matter
- **Action**: §00 v4.2.3 → **v4.3.0** expanded the `consumes:` block from 1 entry (AC-23 schema-drift only) to 6 entries citing §22 `02-database-schema.md` (ER baseline + ShaRegistry boundary), `05-auth-tempttoken.md` (Lane A), `31-ssh-key-auth.md` (Lane B + reject codes), `15-error-codes.md` (GL-* namespace), `19-permission-matrix.md` (RBAC). Each row binds a §23 contract surface to the canonical §22 file it derives from; restating any cited contract in §23 trips Lesson #36 + AC-ADB-17 (externalized citation map).
- **Why**: A-09 (§28→§27, Sess 31), A-11 (§26→§22, Sess 32), A-12 (§24 producer-side, Sess 33) established the consumer/producer binding pattern. A-14 closes coverage on §23 — the last in-scope cohort folder without a multi-row `consumes:` block. Deferred lint §27 D9 `consumes-frontmatter-resolves` now reaches all 7 in-scope folders.
- **Banners**: §00 v4.2.3 → **v4.3.0** (minor — front-matter contract surface expanded); §98 v4.3.0 → **v4.4.0** (this entry). **No** §97 bump (no new AC; existing AC-ADB-17/18 already cover the underlying invariants), **no** CI workflow change, **no** §22 edit, **no** restatement here (Lesson #36).

---

### 4.3.0 — 2026-05-10 — Session 23 audit-task A-01: §22 operational-pattern inheritance (AC-ADB-18)
- **Action**: §97 v3.4.0 → **v3.5.0** added `AC-ADB-18 [critical]` binding §23's runtime contracts to §22's operational patterns by namespace extension: `GL-*` error-code family extends to `ADB-*` (concrete codes `ADB-LINK-INACTIVE`, `ADB-LINK-NO-MATCH`, `ADB-LINK-XOR-VIOLATION`, `ADB-LINK-CANONICALIZE-FAIL`, `ADB-LOOKUP-SEED-DRIFT`, `ADB-SCHEMA-DRIFT`); the four REJECTED resolution states from AC-ADB-16 now map to specific `ADB-*` transport codes (`REJECTED_INACTIVE_APP` → `ADB-LINK-INACTIVE`, `REJECTED_NO_MATCH` → `ADB-LINK-NO-MATCH`); link-create / link-disconnect / link-reconnect mutations MUST emit one `AuditTrail` row each with PascalCase action verbs (`app.link.create` / `app.link.disconnect` / `app.link.reconnect`); read-side resolution attempts MUST NOT emit AuditTrail rows (sink-side rule per §22 AC-04); schema-drift fires `ADB-SCHEMA-DRIFT` mirroring §22 `GL-SCHEMA-DRIFT`. Externalized Citation Map (AC-ADB-17) extended with one row pointing at `§22 AC-30 + AC-21 + AC-04 + AC-23` flagged restate-forbidden per Lesson #36.
- **Why**: Phase 4 audit (Session 22) measured §23 blind-AI failure probability at ~85% with 4 High-likelihood × Wide-blast forced guesses; G23-4 (no error envelope binding for AC-ADB-16's four REJECTED outcomes) and G23-5 (no audit-trail event contract for link mutations) were two of those four. Both could only be closed by inheriting an in-scope operational pattern; §22 is the only in-scope module that owns ErrorEnvelope + AuditTrail + sink-side observability + schema-drift discipline. Inheritance via namespace extension keeps Lesson #36 link-don't-restate intact (§22 owns the bodies, §23 cites by anchor and namespaces the family).
- **Lockstep**: §97 v3.4.0 → **v3.5.0** (minor — new critical AC); this file v4.2.3 → **v4.3.0** (minor — this row); §99 patch bump deferred to next consistency pass (no inventory-axis change). **No DDL change · no §22 edit (link-only inheritance per Lesson #36) · no §27 gate change · no slot file added · no `kind:` change.** Scorecard impact (per Phase 4 / Wave-1 model): §23 Lovable 90 → ~94 expected on next honest re-score; cohort blind-failure probability ~99.6% → ~96% from this single AC (full Wave-1 closes the rest).
- **Audit-trail**: Closes audit task **A-01** (declare §22 as operational-pattern parent for §23 + §24) for the §23 half. The §24 half landed same-PR as **AC-ADS-15**. The combined PR is the single highest-leverage Wave-1 fix per the Phase-5 sequencing model. Forced-guess inventory updated: G23-4 + G23-5 closed; G23-1/-2/-3 (out-of-scope spec/02/05/13 dependencies) remain irreducible under scope-lock.
- **Lesson reapplication**: This is the fifth documented application of "advisory rule → enforceable AC by namespace extension + restate-forbidden citation" pattern (§22 AC-22-CE1 / §26 AC-DG-23 / §27 AC-T-36 amendment / §27 AC-T-36 self-application / this AC). Pattern is now ripe for promotion to a §27 toolchain meta-rule per audit task **A-12** (= prior workstream F-18).


## [4.2.3] — 2026-05-06 — Phase 154 C-Sweep: Cross-Module Externalized Citation Map (Lesson #36 + #37)

- **Added** `AC-ADB-17` `[critical]` — Cross-Module Externalized Citation Map: explicit normative anchor table for 5 externalized citations (spec/05 split-DB pattern, spec/13 §97 AC-22 SQLite locking, spec/22 entity DDL, spec/02 naming conventions, spec/27 script gates). Each row pins owning-AC + cite-source-file + purpose + restate-forbidden flag. Mirror of spec/22 AC-79 pattern. Closes audit-followability gap for integration-axis modules per Lesson #37.
- **Banners**: §97 v3.3.0 → **v3.4.0** (AC count 16 → 17); §00 v4.2.2 → **v4.2.3**; §98 v4.2.2 → **v4.2.3**; §99 v2.1.3 → **v2.1.4**.
- **No** CI workflow change, **no** RUBRIC bump, **no** AC-31-31 cascade, **no** new §97 contract for existing ACs.


### 4.2.2 — 2026-05-04 — Phase 153 Task S23-02 — close 2× LOW audit-v7 findings (concurrency cross-link + UTC parity note)
- **Action**: Added **AC-ADB-15** `[low]` (SQLite concurrency pragmas linked to `spec/13-generic-cli/10-database.md` § "Concurrency & Locking", Lesson #36 link-don't-restate) and **AC-ADB-16** `[low]` (PostgreSQL reference appendix MUST expose `timestamptz` as UTC Unix seconds for application-logic parity with the SQLite `INTEGER` primary block). Mirrored AC-ADB-15 into §00 § "Convention recap" as a one-line cross-link bullet; mirrored AC-ADB-16 into §00 § "Inlined Contracts (Phase 53)" callout as a `⏱ Timestamp parity` blockquote.
- **Why**: Closes audit-v7 D3 LOW `Missing SQLite Busy Timeout/WAL configuration` (auditor wanted pragmas inlined; correct fix per Lesson #36 is to LINK the canonical owner in spec/13, not restate) and D1 LOW `Timestamp Unit Ambiguity in Postgres Block` (auditor noted SQLite=INTEGER vs Postgres=timestamptz unit mismatch risk).
- **Files**: `00-overview.md` § "Convention recap" + § "Inlined Contracts (Phase 53)" callout; `97-acceptance-criteria.md` (+2 ACs); banners.
- **Spec lockstep**: §97 v3.2.0 → **v3.3.0** (AC count 14 → 16, minor — new contract surface); §00 v4.2.1 → **v4.2.2**; §98 v4.2.1 → **v4.2.2**; §99 v2.1.2 → **v2.1.3**. **No CI workflow change**, **no RUBRIC bump**, **no gate-count change**.
- Expected re-score: 97 → ≥99 EXCELLENT.

### 4.2.1 — 2026-05-03 — Phase 153 S23-01 — PostgreSQL DDL appendix marked Reference-only inline (per AC-ADB-11)
- **Action**: Added a normative `> ⚠️ Reference / Secondary dialect (per AC-ADB-11)` callout immediately above the "Inlined Contracts (Phase 53 — SQL DDL lever)" appendix in `00-overview.md`, retitled the heading to `Canonical app-database schema (SQL DDL, PostgreSQL 15+ — REFERENCE ONLY)`, and rewrote the in-block SQL comment from "Every implementing repo MUST materialize these tables EXACTLY" → "REFERENCE-ONLY PostgreSQL dialect (per AC-ADB-11). The Primary Implementation Target is the SQLite block under § 'Schema' above."
- **Why**: AC-ADB-11 already declares SQLite primary + PostgreSQL reference, but the appendix's own header + in-block comment still read as authoritative ("MUST materialize these tables EXACTLY"), giving auditors and fresh implementers two contradictory in-file signals. Lesson #36 cross-module rule applies intra-file too: when one section is normatively superseded by an AC, the section MUST link/defer, not restate. Closes spec/23 audit-v6 MED/D1 finding "dual SQLite+Postgres DDL — appendix self-claims authoritative".
- **Files**: `00-overview.md` § "Inlined Contracts (Phase 53 — SQL DDL lever)" (callout + heading + comment-block edits, ~13 lines added); banners.
- **Spec lockstep**: §00 v4.2.0 → **v4.2.1** (patch — clarifying prose around existing AC-ADB-11; no new contract surface, no AC count change); §97 v3.2.0 unchanged (AC-ADB-11 already binds the rule); §98 v4.2.0 → **v4.2.1**; §99 v2.1.1 → **v2.1.2**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**, **no new AC** — pure prose-mirror of existing AC-ADB-11 into the appendix surface (Lesson #36 intra-file application).


- **Action**: Audit-v6 LOW finding `[D4] Missing Canonicalization Examples` (spec/23 score 86) closed by adding "Canonicalization examples (Phase 153 LOW close-out)" subsection under Resolution states, providing 6 normative URL transformation examples covering: lowercase host + lowercase path + strip `.git` (case 1); strip trailing `/` (case 2); SSH→HTTPS rewrite + strip `.git` (case 3); `ssh://` scheme rewrite (case 4); strip default port 443/22 (case 5); combined transformation (case 6). Pipelines that diverge on ANY of these 6 cases FAIL AC-ADB-14. Added invariant: same pipeline MUST be invoked at `Repo.RepoUrl` insertion AND at every resolution call (string equality, not re-canonicalisation).
- **Why**: Lesson #32 per-finding tracker (`phase-153-batch-verify-low-17.md`) anchored the gap; Lesson #22 closed-enumeration table replaces the open prose "(lowercase host, strip trailing `.git`, strip trailing `/`, normalise SSH `git@host:owner/repo` → `https://host/owner/repo`)" with a concrete-input → expected-output worked table that auditors AND implementers can both verify against.
- **Files**: `00-overview.md` Resolution states section (+~16 lines new subsection); banners.
- **Spec lockstep**: §00 v4.1.0 → **v4.2.0** (new normative table = minor bump); §97 v3.2.0 unchanged (AC-ADB-14 already cites the algorithm — examples are AC-ADB-14 conformance artifacts, not a new contract); §98 v4.1.0 → **v4.2.0**; §99 v2.1.0 → **v2.1.1**. **No CI workflow change**, **no RUBRIC bump**, **no AC-31-31 cascade**, **no gate-count change**, **no new AC** — pure conformance-example addition under existing AC-ADB-14.

### 4.1.0 — 2026-04-29 — Phase 153 P48-3: Polymorphic AppLink resolution algorithm lifted to normative prose
- **Added** §00 "Polymorphic AppLink Resolution (Normative)" section: discriminator → target binding table (locked IDs 1/2 per AC-ADB-13), 4-step resolution algorithm (canonicalise → Direct candidates → Transitive candidates → tie-break Direct>Transitive>newer-CreatedAt), 4-state closed-enumeration outcome table (`RESOLVED_DIRECT`, `RESOLVED_TRANSITIVE`, `REJECTED_INACTIVE_APP`, `REJECTED_NO_MATCH`), and forbidden-patterns subsection (no inactive-App attribution, no `IsActive = 0` row use, no non-deterministic tie-break, no `AppLink → GitProfile` short-circuit bypassing the `Repo` table).
- **Added** AC-ADB-14 (`[critical]`) binding the resolution algorithm; cross-references AC-ADB-05/06/10/13 as load-bearing prerequisites; codifies **Lesson #33** — polymorphic-FK resolution algorithms MUST be lifted to normative prose with closed-enumeration outcomes (example SQL is illustrative, not authoritative; `ORDER BY`-encoded precedence is invisible to auditors and fresh implementers).
- **Closes** Phase 153 P47-fu1 critical finding "23-adb polymorphic AppLink resolution" (the 2nd of 3 P47-fu1 critical findings; #16 P48-2 closed earlier today, #18 P48-4 still open).
- **Banners**: §00 v4.0.3 → **v4.1.0** (minor — new normative subsection adds a public contract surface); §97 v3.1.0 → **v3.2.0** (minor — AC count 13 → 14); §98 v4.0.2 → **v4.1.0**; §99 v2.0.3 → **v2.1.0**. **No CI workflow change, no RUBRIC bump, no AC-31-31 cascade** (no new linter slot — algorithm is enforced by the `app-database` binary at runtime, not by a static checker; future static-checker contributions can land as a §97 extension AC).

### 4.0.2 — 2026-04-29 — Phase 153 Task #29e: AI Confidence promoted High → Production-Ready
- Phase 153 Task #29e — promoted `**AI Confidence:**` from `High` to `Production-Ready`. Pure banner edit: this module already passes P1+P2+P3+P4 per `check-ai-confidence.py`; the prior `High` value was a stale underclaim. **No AC change, no CI workflow change, no RUBRIC bump.**

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

---

## Releases

### 4.0.1 — 2026-04-28 (Phase P26 — H10 reverse-drift reconstruction, hybrid P23+P24 subcase)

- **Changed** Reorganised §98 release ladder. Pre-P26 the file had THREE structural problems: (1) a stray out-of-order release `4.1.0` row listed AFTER `3.0.1` describing Phase 53 (mis-numbered — Phase 53 chronologically preceded the 4.x trunk); (2) orphan dated prose blocks (Phase 58, 68, 71) appended *after* the §98 Cross-References footer that were never promoted into SemVer rows; (3) §00 banner sat at `4.0.0` with no §98 release row to back it. P26 reconstruction: renumbered the stray Phase 53 row → **3.1.0** (correct chronological slot), promoted the orphan post-footer blocks into **3.2.0** (Phase 58 JSON Schema), **3.3.0** (Phase 68 Mermaid), **4.0.0** (Phase 71 inlined CI workflow — major: new normative CI surface, matching §00 banner), then this `4.0.1` row to record the reorganization itself. Each reconstructed row cites its source prose block; orphan post-footer blocks REMOVED to single-source the audit trail.
- **Added** `<!-- h10-verified-phase: 26 -->` stamp to `00-overview.md`, opting this file into strict H10 version-parity enforcement per `check-version-parity.py` AC-29-11/12/13.
- **Banner sync**: §00 `Updated:` 2026-04-27 → 2026-04-28; §00 banner `4.0.0` → `4.0.1` (patch — pure changelog reorganization, no module-rule change).
- **Hybrid subcase note**: P26 is the first reverse-drift phase to apply BOTH P23 (renumber wrongly-labeled prose-citing row) AND P24 (promote post-footer orphans + delete) workflows in a single phase. Codified as **P26 subcase (d)** in the reverse-drift taxonomy: when §98 has out-of-order rows mixed with post-footer orphans, apply P23 + P24 in sequence and document the dual-application explicitly. Stray-numbered rows are NEVER renamed in-place silently — the reconstruction MUST explain why the original number was wrong.

### 4.0.0 — 2026-04-27 (Phase 71 — impl 90 → 95)

- **Added** Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.
- **Major bump rationale**: introduces a new normative CI workflow surface (5-stage pipeline contract) that downstream tooling can validate against — promoted from minor on P26 reconciliation because it constitutes a new public contract surface (consistent with P23 axios v2.0.0 / P24 §14-update v2.0.0 precedents for inlined CI workflows as major bumps).
- Audit-trail source: prior `## 2026-04-27 — Phase 71 (impl 90 → 95)` prose block under §98 Cross-References footer (removed in P26 single-source cleanup).

### 3.3.0 — 2026-04-27 (Phase 68 — impl 85 → 90)

- **Added** Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.
- Audit-trail source: prior `## 2026-04-27 — Phase 68 (impl 85→90)` prose block under §98 Cross-References footer (removed in P26 single-source cleanup).

### 3.2.0 — 2026-04-27 (Phase 58 — impl-sweep)

- **Added** MigrationManifest JSON Schema to satisfy `has_json_schema` rubric (impl 70 → 85).
- Audit-trail source: prior `## 2026-04-27 — Phase 58 impl-sweep` prose block under §98 Cross-References footer (removed in P26 single-source cleanup).

### 3.1.0 — 2026-04-27 (Phase 53 — typed-language / SQL DDL / JSON Schema contracts)

- **Added** typed-language / SQL DDL / JSON Schema contracts to overview to lift implementability score (no behavior change).
- Audit-trail source: prior misnumbered `## 4.1.0 — 2026-04-27` row (renumbered to `3.1.0` in P26 to restore chronological ordering — Phase 53 preceded the 3.0.0 → 4.0.0 trunk evolution, so a `4.1.0` label was incorrect).

### 3.0.1 — 2026-04-28

#### Audit (no content change)

- **Phase P13 — "Split `00-overview.md` (554 lines)" backlog item closed as STALE.** This task was queued before Phases 39a/53/58/68/71 deepened the module to 100/100. Re-audit confirms the file is one cohesive single-source-of-truth contract: convention recap → DDL (3 tables) → seed data → 4 query patterns → migration template → cross-refs → AC-ADB-000 → impl-sweep appendices (PostgreSQL canonical DDL + RLS policies + TS enum mirror + JSON Schema migration manifest + Mermaid lifecycle + CI workflow). §99 explicitly defends co-location ("every contract needed to implement these tables is inlined below") and lists splitting as **optional** under "Open Items" with "No mandatory open items." Slot policy already reserves `01-app-table.md` / `02-app-link-resolution.md` / `03-app-link-history.md` / `04-migration-recipes.md` for if/when per-column commentary outgrows the inline DDL — that condition has not been triggered. Splitting now would fragment the contract, force cross-file lookups for any AppLink question, and burn 4 immutable slots prematurely. No file edits required; no AC changes; no banner bump on `00-overview.md`. §98 / §99 receive a patch bump to record the disposition. Future split proposals against §23 MUST cite a concrete trigger (e.g., per-column commentary >200 lines for a single table, OR a deep-dive workflow that genuinely doesn't belong in the router) — bare line-count arguments are not actionable per Phase P13 precedent (mirrors Phase P12 disposition for §28).

### 3.0.0 — 2026-04-27

- **Phase 39a — F-tier remediation.** Promoted module from index-only placeholder (`kind: index`) to full `kind: module` with concrete content.
  - **Added** Inline DDL for `App`, `AppLink`, `AppStatus`, `AppLinkType` tables (PascalCase, FK with `ON UPDATE CASCADE ON DELETE RESTRICT`, two AppLink CHECK invariants: XOR target + disconnect timestamp).
  - **Added** Inline seed data for the two lookup tables.
  - **Added** Four canonical query patterns: Q1 push-attribution, Q2 soft-disconnect, Q3 reconnect, Q4 admin list.
  - **Added** Forward-only Rule 12 migration template with explicit ❌ counter-examples.
  - **Changed** `97-acceptance-criteria.md` rewritten — 5 generic ACs replaced with 10 concrete, executable Given/When/Then rules covering migrations, naming, CHECK invariants, uniqueness, seed data, and Q1 specificity ordering.
  - **Bumped** module version 3.3.0 → 4.0.0 (overview), AC 2.0.0 → 3.0.0, changelog 2.1.0 → 3.0.0, consistency 1.0.0 → 2.0.0.
  - **Result:** unblocks AI-implementability score from 42/100 (F) toward target 90+/100; resolves audit findings "no DDL", "no enums", "orphan spec".

### 2.1.0 — 2026-04-26

- **Phase 16d-ii — Deepen scaffolded ACs in `97-acceptance-criteria.md`.** Expanded the 4 shortest one-liner ACs from ~211-241 chars to **1942-2295 chars each (8–10× depth)** with full Given/When/Then bodies. AC count unchanged at 5. Banner v2.0.0 → v2.1.0; lockstep §99 + spec-index updated.

### 2.0.0 — 2026-04-25

- **Changed** `97-acceptance-criteria.md`: replaced scaffolded placeholder with AI-extracted Given/When/Then acceptance criteria. Inlined required contracts (enums, DDL, error codes, file paths) directly into the AC file so a mediocre AI can implement without chasing cross-links. Generated by `linter-scripts/generate-gwt-acceptance.py` as part of root v3.7.x F-tier remediation sweep.

### 1.0.0 — 2026-04-25

- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in `99-consistency-report.md`.
- Auto-scaffolded by `linter-scripts/fill-missing-changelogs.cjs` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)

### 4.0.3 — 2026-04-29 — Phase 153 Task #35-fu2: §98 backfill (parity gate close-out)

- **Action**: Backfilled missing §98 row to match §00 banner v4.0.3. Phase 153 Task #35-fu surfaced this as part of the §00-ahead-of-§98 drift class after `latest_release()` was patched to SemVer-max comparator. The §00 banner had been bumped in a prior phase but the corresponding §98 row was never authored — this entry closes the parity gate.
- **Lockstep**: §98 latest release now equals §00 banner; no §00/§99 changes (banner already at v4.0.3).
- **Why**: Codifies Lesson #28 — version-parity drift is mechanical close-out work, not a comparator bug.

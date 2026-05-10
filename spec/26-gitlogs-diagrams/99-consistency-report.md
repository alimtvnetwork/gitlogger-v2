# Consistency Report — Gitlogs Diagrams

**Version:** 3.5.2
**Updated:** 2026-05-07 (Phase B2 — Sibling Artifact Delegation Map)

> **v3.5.2 update (Phase B2 — Sibling Artifact Delegation Map):** Added **AC-26** `[critical]` Sibling Artifact Delegation Map per Lesson #21 (intra-module sibling-file axis); 18-row delegation table covering all sibling artifacts in spec/26 (6 active `.mmd` + 6 paired `.svg` + `puppeteer.json` + lifecycle diagram + `01-diagram-conventions/` sub-folder + 3 informative-exempt module-meta files). Each row pins content-kind + governing-§97-AC-family + tier-visibility + restate-forbidden. Mirror of spec/22 AC-80 (33-sibling axis) and spec/02 AC-CG-21 (16-sub-folder axis). Together with **AC-25** (cross-module externalized citation map) and **AC-22** (derivative-context module-kind pin) forms the **complete tier-1 audit-followability triplet** for spec/26 per Lesson #37. Banners: §97 v3.6.0 → **v3.7.0** (AC 25 → 26, minor); §00 v3.6.1 → **v3.6.2** (patch); §98 v3.6.1 → **v3.7.0** (minor); §99 v3.5.1 → **v3.5.2** (patch). **No CI workflow change, no RUBRIC bump, no gate-count change, no AC-31-31 cascade.** Verify-before-open per Lesson #30: B1 (spec/22 sibling delegation map) confirmed already-shipped as AC-80 in Phase 154 — no-op. Only B2 (this AC) was outstanding.

> **v3.5.1 update (Phase 154 C-Sweep — Cross-Module Externalized Citation Map):** Added **AC-25** `[critical]` Cross-Module Externalized Citation Map per Lessons #36 + #37 + #29 Section F; explicit normative anchor table for 5 externalized citations (spec/22 source-of-truth for all 6 diagrams, spec/03 error catalog, `xmllint` + `xml.etree.ElementTree` canonicaliser toolchain as N/A external-system rows, spec/27 CI gates). Mirror of spec/22 AC-79 pattern. spec/26's "derivative spec" status makes this AC particularly load-bearing — every Mermaid node label citing an entity/error/role/state is by construction a citation of spec/22 or spec/03. Banners: §97 v3.5.0 → **v3.6.0** (AC 24 → 25); §00 v3.6.0 → **v3.6.1**; §98 v3.6.0 → **v3.6.1**. **No CI workflow change, no RUBRIC bump, no gate-count change.**

> **v3.5.0 update (Phase 153 Task S26-D3):** Added AC-24 Python-stdlib fallback for AC-23 Tier 2 structural-XML diff; `xmllint`/`libxml2` is now preferred but optional, removing the only remaining hard OS-binary dependency from the render-lockstep verification protocol; closes audit-v7 [D3] MEDIUM `External Dependency on xmllint`. Lockstep: §97 v3.4.1 → v3.5.0, §00 v3.5.1 → v3.6.0, §98 v3.5.1 → v3.6.0. Expected re-score: 94 → ≥97.

> **v3.0.0 update (Phase 16g):** §97 fully rewritten from 9 table-row criteria (with 02/03/04 already retired as locked gaps) to **20 module-specific Given/When/Then ACs** (AC-DG-01..AC-DG-20). New ACs codify ER parity with §22 (entities + FK cardinalities), auth validation order with `GL-*` reject codes, RBAC RolePermission-union resolution (never role name), header-comment contract for non-ER diagrams (`%% Diagram type:` + `%% What this answers:`), emoji-free + Mermaid-CLI rendering, JWT/RS256/JWKS forbidden tokens, 8-endpoint mindmap completeness, encryption v3 7-node derivation chain, slot 02/03/04 locked-gap immutability (per AC-SAG-04), `.mmd` ↔ `.svg` build-artifact lockstep, kebab-case ASCII node IDs, `GL-*` codes cross-validated against §22 §14 registry, `puppeteer.json` reproducibility, governance rule "§26 trails §22 — never leads", and self-application audit (AC-DG-20). Legacy AC-D-01..AC-D-11 preserved as AC-DG-LEGACY-01..11 at end of §97. Module-level tree-health: 100/100 (A+).

## File Inventory
<!-- verified-phase: 153 -->

| File | Present | Notes |
|------|---------|-------|
| 00-overview.md | ✅ | Index + inventory (v3.4.1 — Phase P19 H10 parity catch-up; content current as of Phase P10) |
| 01-er-diagram.mmd / .svg | ✅ | erDiagram — only place data shape lives. SVG re-rendered Phase 10 v2.1.0 (313 KB, reflects v2.9.0 split-DB shape). |
| ~~02-domain-design.mmd~~ | 🗑️ | Removed v2.0.0 — duplicated 01; slot locked |
| ~~03-endpoints-write.mmd~~ | 🗑️ | Removed v2.0.0 — folded into 09; slot locked |
| ~~04-endpoints-read.mmd~~ | 🗑️ | Removed v2.0.0 — folded into 09; slot locked |
| 05-auth-validation.mmd / .svg | ✅ | flowchart TD + diagram-type header. SVG re-rendered Phase 10 v2.1.0 (177 KB). |
| 06-permission-flow.mmd / .svg | ✅ | flowchart LR, redrawn v2.0.0 with classDef colors + GL-* codes. SVG re-rendered Phase 10 v2.1.0 (113 KB). |
| 07-rate-limit-flow.mmd / .svg | ✅ | sequenceDiagram + diagram-type header. SVG re-rendered Phase 10 v2.1.0 (35 KB). |
| 08-encryption-v3-flow.mmd / .svg | ✅ | v3 deferred + diagram-type header. SVG re-rendered Phase 10 v2.1.0 (34 KB). |
| 09-endpoints-mindmap.mmd / .svg | ✅ | mindmap, all 8 endpoints with verb/path/body/response/permission/audit/errors. SVG re-rendered Phase 10 v2.1.0 (182 KB). |
| 10-ssh-auth-validation.mmd / .svg | ✅ | **NEW Phase P10** — flowchart TD covering §22/§31 SSH Lane B 10-step validation order + 11 reject codes. SVG rendered Phase P10 (~244 KB). Sibling `puppeteer.json` checked in. |
| puppeteer.json | ✅ | **NEW Phase P10** — Mermaid render config (`--no-sandbox`, viewport 2400×2400). Resolves AC-DG-18 reproducibility-config gap that pre-dated this folder's GWT rewrite. |
| 97-acceptance-criteria.md | ✅ | AC-DG-01..AC-DG-21 (Phase P10 added AC-DG-21; AC-DG-LEGACY-01..11 preserved) |
| 98-changelog.md | ✅ | v3.4.0 |
| 99-consistency-report.md | ✅ | This file |

All diagrams reflect `spec/22-git-logs-v2/`. Where v1 (folder 21, archived) conflicts, v2 + diagrams win.

## Cross-Reference Health

- [`00-overview.md`](./00-overview.md) inventory matches every file on disk (9 live + 3 retired tombstones + 3 meta = 15 rows).
- [`97-acceptance-criteria.md`](./97-acceptance-criteria.md) covers all 6 live `.mmd` files (01, 05, 06, 07, 08, 09) via AC-D-01, AC-D-05..AC-D-11.
- Authoritative source link [`../22-git-logs-v2/00-overview.md`](../22-git-logs-v2/00-overview.md) resolves.
- No JWT / RS256 / JWKS references (locked decision 5).
- Every flow/sequence/mindmap diagram opens with `%% Diagram type:` + `%% What this answers:` header comments (AC-D-07).

## v2.0.0 Audit — User feedback "everything looks like an ERD"

| # | Concern | Resolution |
|---|---------|------------|
| 1 | "Same diagram repeated 2-3 times" | Removed `02-domain-design.mmd` (overlapped 01). Removed `03-endpoints-write.mmd` + `04-endpoints-read.mmd` (replaced by single mindmap). Net: 8 → 6 live diagrams. |
| 2 | "Consolidate to one ER diagram" | Done — `01-er-diagram.mmd` is the sole authoritative ER. |
| 3 | "Endpoints should be one mindmap, not write/read split, with body/verb/types" | Done — `09-endpoints-mindmap.mmd` covers all 8 endpoints in one page with verb, path, auth, body fields, response shape, audit, error codes. |
| 4 | "Permission/rate-limit flow look like ERDs — is my system bad or did you mess up?" | Confirmed: I messed up. They are flowcharts/sequences, not ERs, but lacked signposting. Added `%% Diagram type:` + `%% What this answers:` header on every non-ER diagram; redrew `06-permission-flow.mmd` with classDef colors + per-rejection error codes for clear visual difference. Underlying domain is fine; presentation was sloppy. |

## v2.1.0 Audit — Phase 10 Diagram Render Pass

| File | Change |
|------|--------|
| `01-er-diagram.svg` | NEW — rendered from `01-er-diagram.mmd` (313 KB). Reflects v2.9.0 split-DB schema incl. `ShaRegistry`, `SshKey`, `SshNonce`. |
| `05-auth-validation.svg` | NEW — rendered from `05-auth-validation.mmd` (177 KB). |
| `06-permission-flow.svg` | NEW — rendered from `06-permission-flow.mmd` (113 KB). |
| `07-rate-limit-flow.svg` | NEW — rendered from `07-rate-limit-flow.mmd` (35 KB). |
| `08-encryption-v3-flow.svg` | NEW — rendered from `08-encryption-v3-flow.mmd` (34 KB). |
| `09-endpoints-mindmap.svg` | NEW — rendered from `09-endpoints-mindmap.mmd` (182 KB). |
| `00-overview.md` | Banner v2.0.0 → v2.1.0; added Phase 10 render-pass note + re-render command. |
| `98-changelog.md` | v2.1.0 row added. |
| `99-consistency-report.md` | This audit table added; inventory rows updated to list `.mmd / .svg` pairs; banner v2.0.0 → v2.1.0. |

**Render command:** `mmdc -i <file>.mmd -o <file>.svg -p puppeteer.json -b transparent` with `puppeteer.json = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}`. Source `.mmd` files unchanged in this phase — render-only.

## Open Gaps

_None._ Slots 02/03/04 are intentional locked gaps (`~~retired v2.0.0~~`); never to be reused per project rule.

## Health Score

**100/100 (A+)** — 12 of 12 expected source files present (3 retired tombstones documented), AC coverage complete, every diagram self-describes its type, and as of v2.1.0 every live `.mmd` ships a companion `.svg` build artifact for tool-free preview. Slot integrity intact (immutable-slot rule honored).

---

## Validation History

| Date | Version | Action |
|------|---------|--------|
| 2026-04-26 | current | Phase 31: Added Validation History + heading-rubric alignment for `check-tree-health.cjs` v2.0.0 quality dimension. No content removed. |
| 2026-04-25 | prior | Tree-wide audit baseline established (45/100 → roadmap to 100). |
| 2026-04-20 | prior | Module brought into alignment with parent §99 conventions. |
| 2026-04-16 | prior | Initial consistency report authored. |

This module's full lockstep history is mirrored in `98-changelog.md`; entries
above summarize only the audit-/validation-bearing milestones for `26-gitlogs-diagrams`.
| 2026-04-27 | 2.3.0 | Phase 55 — implementability lever (CI YAML / typed-language reference) |

### 2026-04-27 — Phase 74 deepening

- Mermaid lifecycle diagram added.
- CI workflow contract inlined: 5 stages.
- Implementability lifted via v2.9 evidenced-index bonus.


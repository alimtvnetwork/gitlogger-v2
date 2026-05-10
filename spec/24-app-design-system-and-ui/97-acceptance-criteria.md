# Acceptance Criteria — 24 App Design System & UI

**Version:** 3.5.0
**Updated:** 2026-05-10 (Session 55 audit-task A-41 — added per-AC Test invariant blocks (T-ADS-NN-NN) to AC-ADS-06, AC-ADS-09, AC-ADS-10 mirroring AC-ADS-15/16 format. Each AC gains 2-3 mechanical test stubs incl. negative-fixture proofs. No AC semantics change; minor version bump because new normative test surface.)
**Updated-prev:** 2026-05-10 (Session 44 audit-task A-24 — lockstep tail sweep: AC-ADS-16 "Verifies" line stale "deferred implementation" qualifier for `derives-from-restate-check` retired in-place — gate now Active #15 per §27 §00 since Sess-40 A-20. No AC text/contract change; editorial-only patch bump.)
**Updated-prev:** 2026-05-06 (Phase 154 C-Sweep — added **AC-ADS-14** `[critical]` Cross-Module Externalized Citation Map per Lessons #36 + #37; explicit normative anchor table for 2 externalized citations: spec/07 (primitive token registry), spec/27 (script gates). Mirror of spec/22 AC-79 pattern. AC count 13 → 14. spec/24's small citation surface reflects the strict-additive-overlay relationship to spec/07 — almost all design-system contracts already live in spec/07 by construction.)
**Scope:** `spec/24-app-design-system-and-ui/`
**Generated:** Hand-authored alongside the v4.0.0 overview (Phase 39a). Supersedes the auto-extracted v2.0.0 set.

---

## Module Summary

Verifies that the app overlay (§24) is strictly additive over the core design system (§07): app-only tokens exist with proper light/dark parity, are derived from §07 primitives (no raw HSL except the documented status-color exception), and that all app components consume tokens via Tailwind utilities — never raw color literals. Also verifies the AppShell layout invariant.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

### Token namespace

- App-only token names MUST start with `--app-`.
- App tokens MUST NOT shadow §07 token names (`--background`, `--foreground`, `--primary`, `--accent`, `--card`, `--popover`, `--muted`, `--border`, `--input`, `--ring`, `--space-*`, `--font-*`).

### Allowed raw HSL exception

- Only `--app-status-success`, `--app-status-warning`, `--app-status-danger` may declare raw HSL components in `:root` / `.dark`. Every other `--app-*` token MUST be expressed as `var(--<§07 token>)`.

### Forbidden literals (in app components under `src/components/app/**`)

Regex of forbidden substrings in `*.tsx` / `*.ts` / `*.css` under `src/components/app/`:

```
#[0-9a-fA-F]{3,8}\b           # hex literals
\brgb\(|\brgba\(              # rgb()/rgba()
\bhsl\([^v][^)]*\)            # hsl(literal,…) — but NOT hsl(var(--…))
```

### AppShell invariants

- `<header>` MUST be `position: fixed; top: 0; height: var(--app-toolbar-height)`.
- `<aside>` MUST be `position: fixed; left: 0; top: var(--app-toolbar-height); width: var(--app-sidebar-width)`.
- `<main>` MUST have `padding-top: var(--app-toolbar-height)` AND `padding-left: var(--app-sidebar-width)` so content never collides with the fixed header/sidebar.

### Verification scripts

- `npm run lint` — ESLint config enforces the forbidden-literal regexes above.
- `npm run test` — Vitest snapshot suite renders AppShell in light + dark.

---

## Acceptance Criteria

### AC-ADS-01: App tokens never redefine §07 primitives  `[critical]`
- **Given** The combined `:root` and `.dark` blocks of `src/index.css`.
- **When** All custom property declarations are extracted.
- **Then** No declaration whose name does NOT start with `--app-` may appear inside the §24-managed block; equivalently, no `--app-<x>` may share a name with any §07 token.
- **Verifies:** `00-overview.md` § "Token namespace"

### AC-ADS-02: App tokens derive from §07 primitives  `[critical]`
- **Given** Every `--app-*` declaration in `src/index.css`.
- **When** The right-hand side is parsed.
- **Then** It MUST be either (a) `var(--<§07 token>)`, OR (b) one of the three documented status tokens (`--app-status-success|warning|danger`) declared with raw HSL components.
- **Verifies:** `00-overview.md` § "App-only semantic tokens"

### AC-ADS-03: No raw color literals in app components  `[critical]`
- **Given** All `*.tsx`, `*.ts`, and `*.css` files under `src/components/app/**`.
- **When** ESLint runs the forbidden-literal regex set inlined above.
- **Then** Zero matches MUST be reported. Any match fails the build.
- **Verifies:** `00-overview.md` § "Inlined Contracts" + Verification command

### AC-ADS-04: Light/dark parity for every app token  `[critical]`
- **Given** The set of `--app-*` tokens declared in `:root`.
- **When** The same tokens are looked up in `.dark`.
- **Then** Every token MUST resolve to a real value in `.dark` — either by direct declaration or by inheriting from a §07 token that itself has both `:root` and `.dark` values.
- **Verifies:** `00-overview.md` § "Theme parity rule"

### AC-ADS-05: AppShell fixed-region geometry  `[high]`
- **Given** A rendered `<AppShell>` component in jsdom (Vitest).
- **When** Computed styles are inspected for `header`, `aside`, and `main`.
- **Then**
  - `header.position === "fixed"` AND `header.height === var(--app-toolbar-height)`.
  - `aside.position === "fixed"` AND `aside.top === var(--app-toolbar-height)` AND `aside.width === var(--app-sidebar-width)`.
  - `main.paddingTop === var(--app-toolbar-height)` AND `main.paddingLeft === var(--app-sidebar-width)`.
- **Verifies:** `00-overview.md` § "Layout container — the App Shell" + "AppShell invariants"

### AC-ADS-06: Marketing routes do not import AppShell  `[medium]`
- **Given** All routes under `src/pages/(marketing)/**` (or equivalent public-route folder).
- **When** Imports are scanned.
- **Then** None of these files MUST import from `src/components/app/AppShell`.
- **Verifies:** `00-overview.md` § "Layout container — the App Shell" — App Shell is for authenticated routes only.
- **Test invariant (T-ADS-06-01..T-ADS-06-02):** (T-01) Static AST scan of every `*.tsx`/`*.ts` file under `src/pages/(marketing)/**` (or the project's documented public-route folder) MUST find zero import specifiers resolving to `src/components/app/AppShell` or any re-export chain ending there. Failure is hard-fail at lint time. (T-02) Negative-fixture test: a synthetic marketing route file added under `linter-scripts/fixtures/marketing-appshell-violation/` that imports `AppShell` MUST be rejected by the same scan with exit code ≠ 0 — proves the scan is not vacuously passing.

### AC-ADS-07: Sidebar collapses below `md` breakpoint  `[medium]`
- **Given** A rendered `<AppShell>` at viewport width 767px (just below `md`).
- **When** The aside's computed width is read.
- **Then** It MUST equal `var(--app-sidebar-width-collapsed)` (4rem), and `main.paddingLeft` MUST equal the same value.
- **Verifies:** `00-overview.md` § "Responsive breakpoints (binding)"

### AC-ADS-08: Lint + test pipeline passes  `[critical]`
- **Given** A clean working tree on the spec branch.
- **When** Running `npm run lint && npm run test`.
- **Then** Exit code MUST be `0`. Any non-zero exit blocks merge.
- **Verifies:** `00-overview.md` § Verification

### AC-ADS-09: Ownership matrix has no overlap with §07  `[high]`
- **Given** The component inventories of `src/components/ui/**` (§07 primitives) and `src/components/app/**` (§24 composites).
- **When** Component names are compared.
- **Then** No name MUST appear in both folders. App composites MUST be built from §07 primitives, not parallel re-implementations.
- **Verifies:** `00-overview.md` § "Relationship to §07 (Core Design System)"
- **Test invariant (T-ADS-09-01..T-ADS-09-03):** (T-01) Set-intersection check: `basename(*.tsx)` collected from `src/components/ui/**` ∩ `basename(*.tsx)` collected from `src/components/app/**` MUST be the empty set. Comparison is case-insensitive; `.test.tsx` / `.stories.tsx` siblings excluded. (T-02) Every component file under `src/components/app/**` MUST contain at least one import from `src/components/ui/**` OR from `@/components/ui/*` — proves composites are built from primitives, not built parallel. Files exempt: layout-only wrappers documented in a same-PR allowlist `linter-scripts/_lib/app-composite-allowlist.txt`. (T-03) Negative-fixture test: a synthetic `src/components/app/Button.tsx` (collides with §07 `Button`) MUST be rejected by T-01 with exit code ≠ 0.

### AC-ADS-10: Status tokens are app-scoped only  `[low]`
- **Given** All references to `--app-status-*` tokens.
- **When** Their usage is scanned in `src/`.
- **Then** They MUST appear only inside `src/components/app/**` and `src/index.css`. They MUST NOT appear in `src/components/ui/**` (which is §07 territory).
- **Verifies:** `00-overview.md` § "App-only semantic tokens" warning block
- **Test invariant (T-ADS-10-01..T-ADS-10-02):** (T-01) Regex grep `\-\-app-status-[a-z0-9-]+` over `src/**` MUST yield zero matches whose containing file path begins with `src/components/ui/`. Allowed paths: `src/components/app/**`, `src/index.css`, `src/styles.css`. Any other path is hard-fail. (T-02) Negative-fixture test: a synthetic `src/components/ui/Banner.tsx` referencing `var(--app-status-error)` MUST be rejected by T-01 with exit code ≠ 0 — proves the scan is not vacuously passing.

### AC-ADS-11: §07 primitive token registry — inlined snippet  `[medium]`
- **Given** This module is a "strict additive overlay" on §07 (per `00-overview.md` § "Relationship to §07").
- **When** An AI implementer needs to resolve a `var(--<§07 token>)` reference cited by AC-ADS-02 / AC-ADS-04 without leaving the §24 bundle.
- **Then** The §07 primitive registry MUST be discoverable from §24 via either (a) the inlined snippet below, OR (b) the explicit cross-link to `../07-design-system/00-overview.md` in this file's Cross-References section. The minimum primitive set required for §24 token derivation is: `--background`, `--foreground`, `--card`, `--card-foreground`, `--popover`, `--popover-foreground`, `--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--muted`, `--muted-foreground`, `--accent`, `--accent-foreground`, `--destructive`, `--destructive-foreground`, `--border`, `--input`, `--ring`, plus spacing (`--space-*`) and typography (`--font-*`) families. Any `--app-*` whose RHS references a primitive outside this set MUST add a row to the Cross-References table.
- **Verifies:** `00-overview.md` § "Relationship to §07 (Core Design System)" — closes audit-v7 D5 MED `External Dependency §07 Missing` (Lesson #36 cross-reference: link, do not restate the canonical §07 registry).

### AC-ADS-12: Sidebar collapse — concurrency of breakpoint vs manual toggle  `[low]`
- **Given** A rendered `<AppShell>` where the user can manually toggle the sidebar AND the viewport can cross the `md` breakpoint (768px).
- **When** Both signals are observed concurrently (e.g., user clicks toggle while window resizes across the breakpoint).
- **Then** Sidebar collapsed-state MUST derive from a single unified `isCollapsed` source-of-truth that combines `(viewport < md) || userPreferToggleCollapsed`. Manual toggle MUST persist user preference; viewport crossing MUST NOT clobber an explicit user preference within the same session. Forbidden: two independent state slots (one for breakpoint, one for toggle) racing on render.
- **Verifies:** `00-overview.md` § "Responsive breakpoints (binding)" — closes audit-v7 D3 LOW `Sidebar State Concurrency`.

### AC-ADS-13: Linter-script references resolve to canonical §27 slots  `[low]`
- **Given** Any CI workflow / Verification section reference in this module to a script under `linter-scripts/` (e.g., `detect-changed-modules.sh`).
- **When** The reference is followed.
- **Then** It MUST resolve to a script catalogued in `spec/27-spec-toolchain/` (per Lesson #36 anchor-at-canonical-slot). The script's expected exit-code contract (0 = pass, non-zero = fail) and CI invocation pattern MUST be documented in §27, NOT restated here. Any script cited from §24 that lacks a §27 slot is a broken cross-reference and fails this AC.
- **Verifies:** `00-overview.md` § Verification — closes audit-v7 D5 LOW `Missing linter-scripts` (Lesson #36: link to canonical authority, do not duplicate behavior contracts).

### AC-ADS-14 — Cross-Module Externalized Citation Map (Lesson #36 + Lesson #37 — link-don't-restate anchor table)  `[critical]`

**Given** spec/24-app-design-system-and-ui is by design a "strict additive overlay" on spec/07-design-system whose normative content references contract surfaces owned by other top-level spec modules — concretely (a) `00-overview.md` line 41 cites `spec/07-design-system` as the canonical primitive token registry, (b) AC-ADS-02 / AC-ADS-04 reference `var(--<§07 token>)` derivation rules, (c) AC-ADS-11 lists the §07 primitive token set inherited by §24, (d) AC-ADS-13 routes linter-script references to spec/27 slots, (e) `00-overview.md` lines 573/585/597/611/625 cite 5 specific linter-scripts as the CI verification gates;

**When** an AI auditor walks spec/24 §97 (the tier-1 contract surface) and encounters any of these externalized citations OR a downstream contributor needs to follow the dependency chain to verify a normative claim,

**Then** the auditor MUST find the canonical anchor for each external citation in the table below — every row is a Lesson-#36 link-don't-restate boundary (the citation lives ONCE in its owning module's §97; spec/24 cites it but never restates it):

| External cite | Owning module + AC | Cited from spec/24 file | Citation purpose | Restate-in-24 forbidden? |
|---|---|---|---|---|
| spec/07-design-system (primitive token registry) | spec/07 §00 + §97 (token registry contract) | `00-overview.md` L41 + AC-ADS-02 + AC-ADS-04 + AC-ADS-11 | Canonical primitive token names: `--background`, `--foreground`, `--card`, `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--input`, `--ring`, `--space-*`, `--font-*` (every `--app-*` token MUST resolve to `var(--<§07 token>)` per AC-ADS-02 except 3 status-color exceptions) | **YES** — primitive token definitions + light/dark parity contract live in spec/07 §00 + §97; spec/24 inherits via `var()` references, never re-declares primitives |
| spec/27-spec-toolchain (script anchors) | spec/27 §97 (slot 02 = check-spec-folder-refs; slot 14 = generate-trace-map; slot 18 = audit-spec-vs-code-v2; slot 24 = check-lockstep) | `00-overview.md` L573/585/597/611/625 (Verification section) + AC-ADS-13 | Mechanical PR-time gates: changed-module detection, contract validation, deterministic spec-vs-code audit, artifact promotion, consistency-report regen | **YES** — script CLI surfaces + exit-code contracts live in spec/27 §97 per-slot ACs; spec/24 cites script paths only, never replicates CLI logic |

**AND** any future contributor authoring new normative content in spec/24 that references a contract surface owned by another top-level module MUST add a row to the table above (citation + owning module/AC + spec/24 file + purpose + restate-forbidden flag) before the new content ships — the table IS the audit-followable dependency chain;

**AND** any auditor finding citing "external dependency unresolved" or "dangling cross-module reference" against either of the 2 rows above MUST be classified as a stale-cache artifact (the anchor exists in the cited owning module's §97 — verify with `rg -n "AC-XX" spec/NN-*/97-acceptance-criteria.md` before flagging);

**AND** the table is **append-only** within a phase (rows MAY be added, never reworded);

**AND** restating any of the linked contracts inline within spec/24 is **FORBIDDEN** (Lesson #36 dual-source drift class) — every row's "Restate-in-24 forbidden?" cell is `YES` by construction. The "strict additive overlay" relationship to §07 is the architectural manifestation of this rule: §24 adds `--app-*` tokens that REFERENCE §07 primitives, never overrides or shadows them.

- **Verifies:** the cross-module externalized citation contract for spec/24 — both external dependencies (spec/07 primitives + spec/27 script gates) have explicit normative anchors in the table above. Codifies **Lesson #36** (link-don't-restate cross-module boundary) + **Lesson #37** (integration-axis module co-needs Lesson #19 + Lesson #36). Mirror of spec/22 AC-79 + spec/23 AC-ADB-17 + spec/26 AC-25 + spec/28 AC-28-45 (Phase 154 C-Sweep batch). Note: spec/24 has the smallest external-citation surface (only 2 rows) precisely because the spec/07 overlay relationship is so tight — almost all design system contracts already live in spec/07 by construction.

---

## Worked Examples

> Non-normative `kind: example` — illustrative implementations of opaque ACs. If example and AC ever diverge, the AC wins.

### WE-01 — AC-ADS-04 light/dark parity walked

**Setup:** `:root` declares `--app-toolbar-bg: var(--surface-1)` and `--app-sidebar-fg: #1a1a1a` (raw literal — already a violation of AC-ADS-03 but we use it to demonstrate parity).

**Parity check pseudo-code (the test harness AC-ADS-08 enforces):**
```ts
const rootTokens  = parseCssVars(":root");        // {--app-toolbar-bg: "var(--surface-1)", --app-sidebar-fg: "#1a1a1a"}
const darkTokens  = parseCssVars(".dark");        // {--app-toolbar-bg: "var(--surface-1)"}  ← missing --app-sidebar-fg
const sevenTokens = parseCssVars(":root, .dark", "@/07-design-system");

for (const name of Object.keys(rootTokens)) {
  if (!(name in darkTokens)) {
    // not directly redeclared — must inherit via a §07 token that itself has both modes
    const refs = extractCssVarRefs(rootTokens[name]);              // ["--surface-1"] for toolbar-bg; [] for sidebar-fg
    const inheritedOk = refs.length > 0 && refs.every(r => sevenTokens.root[r] && sevenTokens.dark[r]);
    if (!inheritedOk) fail(`AC-ADS-04: ${name} has no .dark resolution`);
  }
}
```

**Outcome on the seed:**
- `--app-toolbar-bg` → passes (inherits `--surface-1` which has `:root` + `.dark` values in §07).
- `--app-sidebar-fg` → **FAILS** AC-ADS-04 (raw `#1a1a1a` cannot inherit; no `.dark` declaration).

**Fix:** add `.dark { --app-sidebar-fg: var(--foreground); }` AND replace `:root` raw literal with `var(--foreground)` (also closes AC-ADS-03).

---

## Acceptance Criteria — Inheritance & Boundary (cont. — Phase-5 T-13 reconciliation)

> **Header reconciliation note:** AC-ADS-15 (§22 operational-pattern inheritance) and AC-ADS-16 (§07 dependency boundary) were appended after the Worked Examples section in earlier sessions and were therefore visually orphaned from the main `## Acceptance Criteria` block. Rather than reorder content (which would invalidate every existing line-anchored citation in §22/§25/§27), Phase-5 T-13 mints this `## Acceptance Criteria — Inheritance & Boundary (cont.)` header to make the structural relationship explicit. Both ACs below carry full normative weight equal to AC-ADS-01..14 above. The Cross-cutting App Framework section (`## Cross-cutting App Framework (CAF)` below) is its own sibling namespace, NOT a continuation of `AC-ADS-*`. Self-enforcing via §27 backlog gate `ac-section-orphan-header-check` (NEW from T-13).

### AC-ADS-15: §22 operational-pattern inheritance for runtime token & component contracts  `[critical]`

- **Given** §24 ships three runtime contract surfaces — (a) the design-token loader (§00 Phase 55 reference impls in Go / Python / PHP), (b) the AppShell layout invariants (AC-ADS-12 fixed header/sidebar geometry), and (c) the App UI Component Registry API (§00 Phase 61) — AND §22-git-logs-v2 owns the canonical operational-pattern surfaces in scope (AC-30 `ErrorEnvelope` shape; the `GL-*` `ErrorCode` enum in §22 §17 / §15; server-generated UUIDv4 `RequestId` correlation; `AuditTrail` row written with the same `RequestId`; AC-04 sink-side observability rule),
- **When** any consumer (the design-token loader at server boot, the AppShell render path on every route, the Component Registry API on component lookup) wraps the §24 runtime surfaces and surfaces a failure to a caller,
- **Then** the consumer MUST inherit §22's operational-pattern contracts as follows: (1) **Error envelope**: every runtime failure response from a §24 surface MUST conform to §22 AC-30 `ErrorEnvelope` shape `{Status, Code, Message, RequestId, HttpStatus}`; the App-design-system error-code family extends the `GL-*` enum under the namespace `ADS-*` — minimum required codes: `ADS-TOKEN-LOADER-FAIL` (token JSON parse / IO failure at boot or hot-reload), `ADS-TOKEN-PARITY-VIOLATION` (a `--app-*` token is missing a `.dark` resolution at runtime — runtime peer of AC-ADS-04 build-time check), `ADS-SHELL-GEOMETRY-DRIFT` (AppShell `<header>` / `<aside>` / `<main>` measured geometry diverges from AC-ADS-12 invariants), `ADS-COMPONENT-NOT-FOUND` (Phase 61 Component Registry lookup miss), `ADS-COMPONENT-VARIANT-INVALID` (variant not declared in registry). (2) **RequestId correlation**: server-side token-loader failures (Go / Python / PHP reference impls) MUST log under a server-generated UUIDv4 `RequestId` matching §22 AC-30; client-side AppShell failures MUST surface a request-scoped correlation ID (browser-generated UUIDv4 acceptable for client-only failures, but if the client subsequently calls an API the SAME ID MUST flow through `X-App-Trace-Id` request header which the server then correlates with its own `RequestId` — never overwriting the server's UUIDv4 per AC-30 client-supplied-header-ignored rule). (3) **AuditTrail event emission**: design-token mutations (admin theme editor when implemented per audit task A-15; runtime hot-reload of a token bundle) MUST emit one `AuditTrail` row with PascalCase action verbs `app.token.reload` / `app.token.update`; AppShell renders MUST NOT emit AuditTrail rows (sink-side rule per §22 AC-04 — render-fan-out would amplify per-route); Component Registry lookups MUST NOT emit AuditTrail rows (read-side, sink-side rule). (4) **§07 boundary preserved**: this AC governs §24's *own* runtime contracts only — §07 primitive token failures (`--background`, `--primary`, etc.) remain governed by §07's own operational pattern (out-of-scope under the locked 7-folder rule); §24 MUST NOT restate §07 error semantics, MUST NOT name `ADS-*` codes that overlap §07's domain, AND MUST NOT promote `--app-*` errors that are actually §07 primitive errors (e.g. a missing `--background` is a §07 failure, not an `ADS-TOKEN-LOADER-FAIL`).
- **Verifies:** §00 § "Inlined Contracts" / "App-only semantic tokens" (token-loader failure path now has a transport-layer error code); §00 § "Layout container — the App Shell" (AppShell geometry drift now has a runtime error code peer of build-time AC-ADS-12); §00 § "Implementation reference — design-token consumers (Phase 55)" (the three reference loaders gain a uniform error contract — closes audit task A-14 partial); §00 Phase 61 Component Registry API (lookup-miss + variant-invalid now bound); §22 AC-30 (ErrorEnvelope shape — restate-forbidden, link-only per Lesson #36); §22 AC-21 (AuditTrail row contract — restate-forbidden); §22 AC-04 (sink-side observability rule — restate-forbidden); §22 §15 (GL-* error code catalog as parent enum the `ADS-*` namespace extends); §22 §17 (OpenAPI ErrorEnvelope schema). Closes audit-derived task **A-01** (Phase 4 forced guesses G24-4 + G24-7 — token loader had no error contract; Phase 78 Module Run Audit Schema had no §22 inheritance binding; both now inherited by namespace extension). Reinforces audit task A-05 §07-boundary discipline by carving the `ADS-*` code namespace explicitly disjoint from §07's domain.
- **Test invariant (T-ADS-15-01..T-ADS-15-05):** (T-01) Every server-side token-loader failure (Go / Python / PHP) MUST emit a response validating against §22 §17 `components.schemas.ErrorEnvelope` AND its `Code` MUST start with `ADS-`. (T-02) `ErrorEnvelope.RequestId` MUST be a server-generated UUIDv4 (not derived from `X-App-Trace-Id`); when the client supplies `X-App-Trace-Id`, the server MUST log BOTH IDs but envelope MUST carry only the server's. (T-03) Every `--app-*` token missing `.dark` resolution at runtime MUST trigger an `ADS-TOKEN-PARITY-VIOLATION` log entry (peer of build-time AC-ADS-04). (T-04) AppShell renders MUST NOT produce AuditTrail rows under any test scenario (sink-side rule). (T-05) `ADS-*` code names MUST NOT include any §07 primitive token name as a substring (boundary discipline — automated regex scan).
- **Externalized Citation Map row** (extends AC-ADS-14): `spec/22-git-logs-v2 §97 AC-30 + AC-21 + AC-04` | this AC line | "ErrorEnvelope shape + AuditTrail row + sink-side observability rule — operational patterns inherited by namespace extension (`GL-*` → `ADS-*`)" | **YES** restate-forbidden. Note the asymmetry vs §23's AC-ADB-18: §24 inherits AC-30 + AC-21 + AC-04 (3 patterns) but NOT AC-23 (schema-drift) because §24 has no DDL surface.

---

### AC-ADS-16: §07 dependency boundary is normative and `restate_forbidden`  `[critical]`  (A-05, Session 27)

- **Given** §24 declares `derives_from: spec/07-design-system` and `restate_forbidden: true` in its front-matter, AND §00 ships the normative `### Dependency Boundary (A-05, Session 27 — normative)` subsection with five binding rules,
- **When** any §24 PR adds, modifies, or removes a token, component, or contract that touches the §07 boundary,
- **Then** the change MUST satisfy all five rules: (1) no `--app-*` token suffix MAY collide with a §07 primitive name (`--background`, `--foreground`, `--primary`, `--primary-foreground`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--input`, `--ring`, `--space-*`, `--font-*`, `--radius-*`); (2) every `--app-*` token value MUST resolve via `var(--<§07-primitive>)` — raw `oklch()` / `hsl()` / `rgb()` / hex literals are forbidden (also trips AC-ADS-03); (3) §07 contract text MUST NOT be restated verbatim or near-verbatim — cross-reference by anchored link only (Lesson #36); (4) under the active scope-lock (`spec/22..28` only), §24 MUST NOT propose edits to §07 — gaps are filed as §22 backlog tickets tagged `carry-up-to-§07` and noted in §99; (5) the §27 toolchain rule `derives-from-restate-check` (to be implemented) parses §24 markdown for §07 prose copies and fails the build — until shipped, this AC is enforced by reviewer discipline.
- **Verifies:** §00 § "Relationship to §07 (Core Design System)" (the prose ownership matrix); §00 § "Dependency Boundary (A-05, Session 27 — normative)" (the binding rules); §24 front-matter keys `derives_from` + `restate_forbidden`; §27 `derives-from-restate-check` lint rule (**Active gate #15 — shipped Sess-40 A-20; "deferred implementation" qualifier retired Sess-44 A-24**). Reinforces AC-ADS-15 T-05 and AC-ADS-03.
- **Test invariant (T-ADS-16-01..T-ADS-16-04):** (T-01) Front-matter parser MUST find `derives_from: spec/07-design-system` AND `restate_forbidden: true`; missing either is a fail. (T-02) Regex scan of all `--app-*` token declarations MUST reject any name whose suffix matches the §07 primitive set. (T-03) Regex scan of all `--app-*` token *values* MUST accept only `var(--<identifier>)`, `calc(...)`, `color-mix(...)` referencing other tokens, or numeric/keyword literals for non-color properties — raw color literals are rejected. (T-04) `derives-from-restate-check` (when shipped) compares §24 paragraphs against §07 paragraphs via 8-token shingle hash; ≥3 matching shingles in any single §24 paragraph fails the build.
- **Externalized Citation Map row** (extends AC-ADS-14): `spec/07-design-system §00 (primitive token registry)` | this AC + §00 Dependency Boundary subsection | "§07 primitive token names + values are inherited by reference; §24 forbids re-declaration and verbatim restatement" | **YES** restate-forbidden. Cohort consumers: AC-ADS-15 T-05; §22 `60-app-cohort-integration.md` Ownership Boundaries row "App-overlay tokens"; §25 `02-consolidated-audit-findings/00-overview.md` disposition-map row F-21 (`Irrelevant-in-v2`).

---

---

## Cross-cutting App Framework (CAF) — Phase-5 T-12

This section mints the `AC-CAF-NN` namespace covering cross-cutting App-layer
concerns that span §23 (database) + §24 (UI shell) + §25 (issues). CAF
contracts are deliberately thin pointers — each one binds an §24-anchored
contract to its mirror in §23 or §25 to make cross-module drift mechanically
detectable. New CAF entries MUST be co-introduced with a §27 backlog gate.

### AC-CAF-01: Wire-boolean parity is end-to-end (DB ↔ REST ↔ UI)  `[critical]`

**Given** the boolean field `IsActive` on `App` and `AppLink` rows,  
**When** a value flows DB → REST response → UI render OR UI input → REST request → DB write,  
**Then** the chain MUST be: DB INTEGER 0/1 ↔ JSON boolean true/false ↔ UI label "Active"/"Inactive" with `--app-status-active`/`--app-status-inactive` token. No layer is permitted to accept the integer form on the wire (§23 R-4 invariant 2 + §24 U-3 + AC-ADB-11). Self-enforcing via §27 backlog gate `rest-boolean-parity-check` (T-06) + WE-3 (T-11) byte-for-byte fixture.

### AC-CAF-02: Error envelope is uniform across DB-fault and UI-render paths  `[critical]`

**Given** any non-2xx response from R-01..R-15,  
**When** the §24 `<AppErrorState/>` slot renders the failure,  
**Then** the response body MUST match §23 R-3 envelope (Code/Message/Field/TraceId), AND `<AppErrorState/>` MUST surface `Code` as `data-error-code` attribute and `TraceId` as visible copy-to-clipboard text (§24 AC-ADS-UI-02). Inheriting §22 AC-ADS-15 ErrorCode taxonomy (`ADS-*` codes extend `GL-*`). Self-enforcing via §24 AC-ADS-UI-02 + §27 backlog gate `error-envelope-uniformity-check` (NEW from T-12).

### AC-CAF-03: Idempotency contract is observable at every layer  `[high]`

**Given** an endpoint flagged `Idempotent=Yes` in §23 R-1 (R-02, R-03, R-05, R-06, R-07, R-09, R-11, R-13),  
**When** the same request is issued N times,  
**Then** the second-and-subsequent responses MUST return the IDENTICAL body (modulo TraceId) AND no DB row mutation occurs (verifiable via `EXPLAIN QUERY PLAN` showing only SELECT after the first call). WE-4 is the canonical fixture for the disconnect path. Non-idempotent endpoints (R-01, R-04, R-08, R-15) MUST NOT be aliased as Idempotent in the UI layer (§24 U-1 binding column).

### AC-CAF-04: Seed-row/override separation extends seedable-config to App-layer  `[high]`

**Given** any setting introduced under §24 S-1..S-2 (Settings Surface),  
**When** the setting is mutated via R-10/R-12/R-14,  
**Then** the mutation MUST INSERT/UPDATE the `UserSettingOverride` row only — the seed row in `Setting` MUST remain immutable as the documented default and rollback target (§24 S-3 invariants 1+2). Removing a setting requires paired removal of seed + overrides in a single forward-only migration (§23 Rule 12 + §24 S-3 invariant 4). Self-enforcing via §27 backlog gate `seedable-config-row-present-check` (T-08).

### AC-CAF-05: Audit-finding strings cite, never restate (Lessons #36/#37 + AC-AI-10/11)  `[critical]`

**Given** a §25 audit finding contains an apparent App-layer claim (DDL, AC-ID, file path),  
**When** an AI walker reads the finding in partial context,  
**Then** the walker MUST treat the string as **auditor-quoted evidence** of the audited corpus (`spec/_archive/21-git-logs-v1/`), NOT as a §25-owned spec contract. §25 AC-AI-10/11 codify this disambiguation at the §25 surface; AC-CAF-05 lifts it to cross-cutting status so §23 + §24 walkers also apply the rule. Self-enforcing via §25 AC-AI-10/11 + §27 backlog gate `audit-quoted-evidence-marker-check` (NEW from T-12) + scope-lock memory clause.
## Cross-References


- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§07 Design System (canonical primitives)](../07-design-system/00-overview.md)

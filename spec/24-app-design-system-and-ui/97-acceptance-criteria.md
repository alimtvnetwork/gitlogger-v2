# Acceptance Criteria — 24 App Design System & UI

**Version:** 3.2.0
**Updated:** 2026-05-06 (Phase 154 C-Sweep — added **AC-ADS-14** `[critical]` Cross-Module Externalized Citation Map per Lessons #36 + #37; explicit normative anchor table for 2 externalized citations: spec/07 (primitive token registry), spec/27 (script gates). Mirror of spec/22 AC-79 pattern. AC count 13 → 14. spec/24's small citation surface reflects the strict-additive-overlay relationship to spec/07 — almost all design-system contracts already live in spec/07 by construction.)
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

### AC-ADS-10: Status tokens are app-scoped only  `[low]`
- **Given** All references to `--app-status-*` tokens.
- **When** Their usage is scanned in `src/`.
- **Then** They MUST appear only inside `src/components/app/**` and `src/index.css`. They MUST NOT appear in `src/components/ui/**` (which is §07 territory).
- **Verifies:** `00-overview.md` § "App-only semantic tokens" warning block

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

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [§07 Design System (canonical primitives)](../07-design-system/00-overview.md)

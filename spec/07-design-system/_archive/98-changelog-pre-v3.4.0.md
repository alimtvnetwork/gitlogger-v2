# Changelog Archive — AI-Adaptable Design System (pre-v3.4.0)

**Archived:** 2026-05-01 (Phase 153 A24-fu31 — §98 archive split per Lesson #65)  
**Reason:** Phase 153 A24-fu27 audit identified spec/07 tier-1 bundle at 137 KB (OVER ~125 KB walker cap). §98 was 27 KB; relocating historical rows v3.3.0 → v1.0.0 (1.x file-scaffold track + Phase 56 typed-language entry) reduces live §98 to ~18 KB and brings the bundle CLEAR.  
**Restoration:** These rows remain authoritative project history; reference via `spec/07-design-system/_archive/98-changelog-pre-v3.4.0.md`. Live §98 retains all v3.4.0+ entries (the Phase 151 P3 sweep onwards — current-contract entries the auditor needs).

---

### 3.3.0 — 2026-04-27 (Phase 56 — typed-language reference)
- **Added** Added Go/PHP/Python design-token loader references with HSL-triplet validation → flips `has_typed_lang_contract` true (+10 impl).

### 1.5.0 — 2026-04-26
- **Phase 15e — Convert §97 Navigation + Page Consistency sections from table-row to GWT format. §07 §97 conversion COMPLETE.** Final slice of the §07 structural conversion (Phases 15a + 15b + 15c + 15d prior). AC IDs unchanged (still AC-001..AC-034 sequential, count = 34). The 9 ACs in the **Navigation (AC-026..AC-030) + Page Consistency (AC-031..AC-034)** sections converted from one-row table format (~70 chars each) to full Given/When/Then subsections (1900-3500 chars each, **27-50× depth**) with concrete contracts + cross-refs to `08-header-navigation.md`, `10-sidebar-system.md`, `11-section-patterns.md`, `12-page-creation-rules.md`, `tailwind.config.ts`, `index.html`, `src/components/ui/sidebar.tsx`, AC-001/AC-007/AC-008/AC-009/AC-010/AC-012/AC-014/AC-026/AC-029, WCAG 2.1 §1.3.1/§2.4.7/§2.5.5.
- **AC-026** (header icon scale) — `scale(1.05)` on hover + `scale(0.95)` on active for tactile feedback, no-bounce/no-spring rule, color + bg combo, reduced-motion collapses scale only.
- **AC-027** (menu gradient underline) — `::after` pseudo-element with `transform-origin` flip from `bottom right` (resting) to `bottom left` (hover), heading-gradient tokens (NOT primary), focus-visible instant, distinct from prose link sweep (AC-015).
- **AC-028** (dropdown hover) — `hsl(var(--primary) / 0.08)` subtle tint + primary text color, 150ms on both bg+color, contained-vs-linear distinction from nav items, keyboard focus parity.
- **AC-029** (mobile Sheet) — slides from left at 200ms, backdrop `hsl(0 0% 0% / 0.5)` no-blur for perf, hamburger trigger md:hidden, auto-close on file-select/escape/outside-click/breakpoint-grow, shadcn Sheet primitive mandate.
- **AC-030** (Ctrl+B toggle) — global window keydown listener, `Ctrl||Cmd + B`, `preventDefault` to suppress browser bookmarks, input-guard (skip when typing in input/textarea/contenteditable), 200ms width animation, localStorage persistence, mobile opens Sheet instead.
- **AC-031** (section pattern composition) — `Header → [Hero] → N × [Section Pattern] → [CTA] → [Footer]` flow, no ad-hoc section layouts (must add to `11-section-patterns.md` first), shared header/footer components, `<main>` landmark, fixed py-* rhythm.
- **AC-032** (font registry enforcement) — only Ubuntu/Poppins/Ubuntu Mono/JetBrains Mono allowed, no per-page font loading, no generic fallbacks (serif/cursive), no inline `style="font-family"`, spec-first registration gate.
- **AC-033** (state language) — REQUIRED `:hover` + `:active` + `:focus-visible` + `:disabled` on every interactive element, `--ring` token for focus indicator (NEVER `--primary`), 2px minimum thickness, no-hover-only rule per Rule 5, `aria-disabled` for SR.
- **AC-034** (responsive breakpoints) — md/lg Tailwind breakpoints (768px/1024px), mobile-first utility ordering, single-column on mobile + Sheet sidebar + 44px touch targets per WCAG §2.5.5, 2-col tablet + icon-only header, 3-col desktop + full sidebar, no horizontal scroll, responsive images via `srcset` or `max-width: 100%`.
- Updated top-of-file Format note to reflect **34/34 ACs now GWT — conversion COMPLETE**.
- Banner v1.4.0 → v1.5.0; lockstep §97 v3.6.0 → v3.7.0 + §99 v3.6.0 → v3.7.0 + spec-index updated.

### 1.4.0 — 2026-04-26
- **Phase 15d — Convert §97 Code Blocks section from table-row to GWT format.** Continuation of the §07 structural conversion (Phases 15a + 15b + 15c prior). AC IDs unchanged (still AC-001..AC-034 sequential, count = 34). The 9 ACs in the **Code Blocks** section converted from one-row table format (~80 chars each) to full Given/When/Then subsections (2100-4200 chars each, **26-52× depth**) with concrete contracts + cross-refs to `07-code-blocks.md`, `02-theme-variable-architecture.md`, `src/index.css` (lines 264–605), `src/components/markdown/codeBlockBuilder.ts`, AC-001/AC-012/AC-014.
- **AC-017** (fixed dark background) — static HSL mandate (`hsl(220,14%,11%)`), exception to token-only rule, theme-invariant header/line-number backgrounds, syntax-highlighting tokens exempt.
- **AC-018** (language badge) — 7px dot + glow, 10-language color mapping (static brand colors, NOT theme tokens), `--lang-accent` inline injection, "TEXT" fallback.
- **AC-019** (font size controls) — 12-32px bounds, 2px step, 18px default, proportional line-number scaling (`* 0.7`), `localStorage` persistence, 150ms animate, `aria-label` on controls, clamp on corrupted storage.
- **AC-020** (line pin) — toggle via React state, `line-pinned` class with 3 visual markers (bg + border + number color), unpin on re-click, hover-vs-pin precedence (pin wins), full-gutter click target.
- **AC-021** (shift-click range) — bidirectional range selection, idempotent (no unpin), triggers selection bar, anchor-of-1 fallback, `event.shiftKey` at click time, visual parity with single-pin.
- **AC-022** (fullscreen) — 2rem inset, backdrop overlay (`blur(4px)`, `z-40`), block at `z-50`, language-accent shadow, body `overflow: hidden`, 300ms scale settle animation.
- **AC-023** (Escape exit) — immediate exit, restore inline position + body overflow + remove backdrop + return focus, overlay-click secondary trigger, idempotent, cleanup all listeners, `beforeunload` safeguard.
- **AC-024** (copy button) — full content copy (including off-screen), Clipboard API primary + `textarea` fallback, success state with green tint + "Copied ✓" label, 2-second timer with reset, `aria-label` + `aria-live` for a11y.
- **AC-025** (tree prefixes) — 📁/📄 emoji prefixes, bold/muted styling, guide characters at `muted-foreground/0.5`, ellipsis at `accent`, comments italic, "STRUCTURE" label, indentation preserved.
- Updated top-of-file Format note to reflect 25/34 ACs now GWT.
- Banner v1.3.0 → v1.4.0; lockstep §97 v3.5.0 → v3.6.0 + §99 v3.5.0 → v3.6.0 + spec-index updated.

### 1.3.0 — 2026-04-26
- **Phase 15c — Convert §97 Motion & Transitions section from table-row to GWT format.** Continuation of the §07 structural conversion (Phases 15a + 15b prior). AC IDs unchanged (still AC-001..AC-034 sequential, count = 34). The 5 ACs in the **Motion & Transitions** section converted from one-row table format (~70 chars each) to full Given/When/Then subsections (1703-3816 chars each, **24-54× depth**) with concrete contracts + cross-refs to `06-motion-transitions.md`, `09-button-system.md`, `tailwind.config.ts`, `src/index.css`, `package.json` dependency audit, WCAG 2.1 §2.3.3, MDN `prefers-reduced-motion` reference.
- **AC-012** (≤300ms hover) — fixed timing vocabulary {150/200/300ms}, `cubic-bezier(0.4,0,0.2,1)` mandate, symmetric in/out durations, reduced-motion collapse to ≤10ms.
- **AC-013** (no JS animation libraries) — exhaustive forbidden list (framer-motion, react-spring, react-motion, gsap, anime.js, lottie-*, mo.js, popmotion, react-transition-group, velocity-animate), narrow exception allowlist (tailwindcss-animate, embla-carousel-react, recharts/d3 for data viz only).
- **AC-014** (`prefers-reduced-motion`) — exact global CSS override (`0.01ms` not `0` so `transitionend` still fires), per-component opt-in pattern via `@media (prefers-reduced-motion: no-preference)`, scroll-behavior override, parallax/auto-play disable rule.
- **AC-015** (link underline sweep) — pseudo-element implementation with `right: 0` anchor for natural reverse direction, `position: relative` parent requirement, no-`text-decoration` mixing rule, focus-visible instant-fullwidth state, reduced-motion fallback.
- **AC-016** (CTA slide text) — two-stacked-spans `overflow: hidden` pattern with `translateY` mechanics, vertical-only direction (horizontal reserved for navigation), reversibility on mouse-out, reduced-motion fallback to instant tint, `aria-hidden="true"` on duplicate text for screen-reader correctness.
- Updated top-of-file Format note to reflect 16/34 ACs now GWT.
- Banner v1.2.0 → v1.3.0; lockstep §97 v3.4.0 → v3.5.0 + §99 v3.4.0 → v3.5.0 + spec-index updated.

### 1.2.0 — 2026-04-26
- **Phase 15b — Convert §97 Typography section from table-row to GWT format.** Continuation of the §07 structural conversion started by Phase 15a. AC IDs unchanged (still AC-001..AC-034 sequential, count = 34). The 5 ACs in the **Typography** section converted from one-row table format (~70 chars each) to full Given/When/Then subsections (1209-4005 chars each, **17-57× depth**) with concrete contracts + cross-refs to `03-typography.md`, `index.html` font-loading, `tailwind.config.ts` font registration, `02-theme-variable-architecture.md`, `07-code-blocks.md`, `12-page-creation-rules.md`, WCAG 2.1 §1.3.1/§2.4.6.
- **AC-007** (Ubuntu headings) — exact font stack, Google Fonts loading with `display=swap`, `tailwind.config.ts` `fontFamily.heading` registration, no-Poppins-mixing rule, child-component override prohibition.
- **AC-008** (Poppins body) — exact font stack with weights 300-700, `display=swap`, `tailwind.config.ts` `fontFamily.sans` default override, inline-`<code>` escape hatch to mono per AC-009.
- **AC-009** (Ubuntu Mono / JetBrains Mono code) — full monospace stack, dual font-loading (Ubuntu Mono 400/700 + JetBrains Mono 400/500/700), `font-feature-settings: "liga" 0;` ligatures-off-by-default, `format:ligatures` opt-in directive, inline-vs-block parity.
- **AC-010** (gradient H1/H2) — 4-property cross-browser gradient text contract (`background-image` + `background-clip` + `-webkit-background-clip` + `color: transparent` / `-webkit-text-fill-color`), token-only gradient stops per AC-001, H3..H6 exclusion, multi-line continuity, accessibility decoupling (gradient is decoration, semantic level carries meaning).
- **AC-011** (no skipped levels) — exactly-one-`<h1>` rule, monotonically descending sequence, screen-reader outline rationale, `level`/`as` polymorphic prop requirement for reusable wrappers, visual-vs-semantic decoupling via Tailwind utilities.
- Updated top-of-file Format note to reflect 11/34 ACs now GWT (Theme & Variables + Typography both converted).
- Banner v1.1.0 → v1.2.0; lockstep §97 v3.3.0 → v3.4.0 + §99 v3.3.0 → v3.4.0 + spec-index updated.

### 1.1.0 — 2026-04-26
- **Phase 15a — Convert §97 Theme & Variables section from table-row to GWT format.** Per `mem://specs/full-tree-audit-v4.md` deepening backlog + Phase 14 close-out. AC IDs unchanged (still AC-001..AC-034 sequential, count = 34). The 6 ACs in the **Theme & Variables** section converted from one-row-per-AC table format to full Given/When/Then subsections with concrete contracts + cross-refs to `01-design-principles.md`, `02-theme-variable-architecture.md`, `src/index.css`, `tailwind.config.ts`, the theme provider, WCAG 2.1 §1.4.3/§1.4.11.
- **AC-001** (no hardcoded colors) — exhaustive forbidden-pattern list (hex, rgb/rgba, named CSS colors, literal Tailwind utilities), explicit exception allowlist (token definitions, third-party SVG with `currentColor` wrapper).
- **AC-002** (`hsl(var(--token))` discipline) — bare-triplet token format rule (`--primary: 217 91% 60%;` NOT `hsl(...)`-wrapped), alpha-composition syntax, prohibition on inlining matching raw HSL.
- **AC-003** (`--primary` cascade) — explicit list of all surfaces that MUST update, paired-foreground manual-update obligation per AC-006, gradient-token cascade.
- **AC-004** (`:root` + `.dark` block parity) — set-equality rule, mode-invariant tokens MUST still appear in both, `.dark` MUST be applied to `<html>`/`<body>` not nested.
- **AC-005** (toggle correctness) — ≤16ms perceptible delay, FOUC prevention via synchronous pre-paint script in `index.html`, `localStorage` persistence, `prefers-color-scheme` first-visit honoring.
- **AC-006** (WCAG AA contrast) — 4.5:1 normal / 3:1 large text, BOTH modes independently, hover/focus/disabled inheritance, 3:1 non-text threshold per WCAG §1.4.11.
- Added **Format note** at top of §97 explaining that AC-007..AC-034 remain in table format pending Phase 15b..15e — IDs are stable across formats so tooling that scrapes by ID continues to work.
- Banner v1.0.0 → v1.1.0; lockstep §97 v3.2.0 → v3.3.0 + §99 v3.2.0 → v3.3.0 + spec-index updated.

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
| 2026-04-26 | patch | Phase 31: Added Validation History / File Inventory headings to §99 to satisfy rubric v2.0.0 quality dimension. |

## 2026-04-27 — Phase 58 impl-sweep

- Phase 58: appended Design Tokens OpenAPI contract to satisfy `has_yaml_openapi` rubric (impl 75 → 85).

## 2026-04-27 — Phase 68 (impl 85→90)

- Added Mermaid lifecycle diagram (`*.mmd`) and `## Phase 68 Reference` block in `00-overview.md`.
- Pushes implementability score to 90 via mermaid bonus.

## 2026-04-27 — Phase 72 (impl 90 → 95)

- Inlined 5-stage CI workflow contract (yaml) — satisfies `has_ci_workflow` gate.
- Documentation-only promotion; no behavioural rules changed.

## 3.4.2 — 2026-04-30 — Phase 153 (inventory-pin)

- Added **AC-35** (Module asset inventory pin) — Lesson #29 module asset inventory pin. Auditor-authoritative on-disk inventory declaration; closes audit-v6 HIGH [D5] missing-files class as bundling-cap artifact (cache-stale per Lesson #34 until A8 LLM re-score). Lockstep §00/§97/§98/§99 patch+minor coordinated.

## 3.4.3 — 2026-04-30 — Phase 153 A24-fu9 (spec/07 self-lift)

- Added **AC-036** (Canonical semantic token registry, `[critical]`) + canonical 23-row token table in §00 — closes audit-v7 [D4 MEDIUM] "Incomplete Token Registry Example" by lifting the full registry into tier-1 (Lesson #19 audit-boundary < verification-boundary). Registry is closed-set; HSL space-separated triplets only; `:root` + `.dark` MUST both declare every token.
- Added **AC-037** (FOUC-prevention theme bootstrap, `[high]`) + canonical 9-line `<script>` snippet in §00 — closes audit-v7 [D3 LOW] "Concurrency/Race Condition in Theme Script" by inlining the synchronous bootstrap pattern with `try`/`catch`/`prefers-color-scheme` fallback. Tightens AC-005 with copy-pasteable implementation. Forbidden patterns enumerated (React `useEffect` init, `defer`, post-stylesheet placement, missing `try`/`catch`).
- Lockstep: §97 v3.9.0 → **v3.10.0** (minor — 2 new ACs, AC count 36 → 38); §00 v3.4.2 → **v3.4.3** (patch — new normative subsections); §98 v3.4.2 → **v3.4.3** (patch); §99 v3.10.1 → **v3.10.2** (patch). h10 stamps refreshed to phase 153.
- v7 cache score predicted lift 80 → ≥85 (D4 +2, D3 +2, plus D5 stability via existing AC-35 pin); fresh re-score performed per Lesson #38.


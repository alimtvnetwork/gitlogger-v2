---
kind: ac-detail
content_axis: normative-ac-detail-section-a
axis_rationale: "Detailed normative bodies for Section A ACs (UI / Menu / First-Run) promoted out of §97-acceptance-criteria.md per Lesson #65 (structural surgery) + Lesson #36 (link-don't-restate). Slot 49 = sibling (01–96), not tier-1 — keeps §97 within walker cap so the audit can read full AC inventory."
---

# §97 AC — Section A Detail (UI / Menu / First-Run)

**Version:** 1.0.0
**Updated:** 2026-05-10
**Slot type:** sibling (non-tier1) — bound from `97-acceptance-criteria.md` Section A
**Promotion rationale:** AC-25 + AC-77 carried single-paragraph normative bodies that pushed `97-acceptance-criteria.md` to 184 KB, exceeding the 140 KB walker cap (`linter-scripts/audit-bundle-budget.py` → OVER class). Per **Lesson #65 — structural surgery > pure-promotion**, the bodies are moved here; §97 retains a slim Given/When/Then summary that **binds** to the section anchors below.

> **Status:** Normative tier-2 (sibling). The detail blocks below are the authoritative normative source for AC-25 and AC-77. Restating any of this content in §97, §03, or any other sibling is FORBIDDEN per **Lesson #19** (audit-boundary pin). The §97 entry MUST link here by anchor.

---

## AC-25 — `format:hide` items not rendered (DETAIL)  `[active]`

**Slim form (also in §97):**
- **Given** a mind-map node carries the `format:hide` annotation
- **When** the admin UI renderer projects the node into any DOM surface
- **Then** the node MUST be omitted from the rendered DOM entirely (never CSS-hidden), the rule MUST hold across every projection, and empty parents MUST also be omitted.
- **Verifies:** brief §1.j, §03, §49 §AC-25 detail below.

### AC-25 §D1 — Annotation source (normative)

The `format:hide` annotation is a leaf-level token in a mind-map node label (e.g. `Field: ApiKey  format:hide`) or a separate metadata entry on the node. It belongs to the format-pragma family alongside `format:section`, `format:badge`, and `format:hide`, and follows the same syntax rules as those siblings (per §03 spec layout).

### AC-25 §D2 — DOM-omission rule (normative)

A node carrying `format:hide` MUST be **omitted from the rendered DOM entirely**. The following are explicit SPEC VIOLATIONS:
- `display: none`
- `visibility: hidden`
- `hidden` HTML attribute
- `opacity: 0`
- off-screen positioning (`position: absolute; left: -9999px`)
- any other CSS- or attribute-based hiding that leaves the element in the DOM tree

The element MUST never enter the DOM tree in the first place.

### AC-25 §D3 — Defense-in-depth rationale (normative)

A CSS-hidden element is still:
- (a) visible in `view-source`
- (b) visible in browser DevTools without any user interaction
- (c) returned from `document.querySelectorAll('*')`
- (d) included in `outerHTML` snapshots that may be sent to error trackers / session-replay tools
- (e) selectable via screen-reader tab traversal in some configurations

Therefore omission MUST happen at the **server-side render boundary** (or React render-tree boundary for client-rendered admin UIs). A server that emits the element AND THEN strips it client-side is a SPEC VIOLATION.

### AC-25 §D4 — Cross-projection consistency (normative)

`format:hide` MUST be honored consistently across **every** UI surface that consumes the same node:
- list views
- detail views
- edit forms
- export-to-CSV
- JSON-API responses fed by the same projection
- audit-log diffs
- change-history viewers

Partial honoring (e.g. omitted from list but visible in detail) is a SPEC VIOLATION.

### AC-25 §D5 — Strictly subtractive (normative)

The inverse rule also holds: a node WITHOUT `format:hide` MUST appear in every projection that the spec layout indicates. The annotation is **strictly subtractive**, never additive.

### AC-25 §D6 — Empty-parent collapse (normative)

When a `format:hide` node is part of a parent that becomes empty after hiding all its `format:hide` children (e.g. a section group whose every member is hidden), the parent MUST also be omitted from the DOM. No empty `<fieldset>` / `<table>` / `<details>` shells — empty containers are visual noise and a tell for "something was here that we hid".

### AC-25 §D7 — Distinct from RBAC (normative)

`format:hide` is distinct from permission-driven hiding (per AC-06 + AC-39 — those drop based on RBAC at runtime per user). `format:hide` is a **structural authoring decision** baked into the spec, applied universally regardless of viewer. Both kinds of hiding MAY apply to the same node, but for different reasons.

### AC-25 §D8 — Verifies

brief §1.j (`format:hide` annotation contract); §03 (spec-driven UI layout pipeline); AC-06 / AC-39 (distinct from RBAC permission gates).

---

## AC-77 — History `HasError + StateLabel` column rendering (DETAIL)  `[active]`

**Slim form (also in §97):**
- **Given** a `Pipeline` row with `(PreviousHasError, HasError)` both NOT NULL CHECK IN (0,1) per §18 v2.9.2
- **When** the admin UI renders the `HasError + StateLabel` column
- **Then** the cell MUST render the raw `HasError` glyph + the AC-73 derived state-transition chip with `data-state-label="<key>"`, derived per AC-73's pure-function rule at render time, no caching, exhaustive over the 4-label set, color-blind-safe, sortable + filterable, and parity-equal to AC-74's NDJSON consumer.
- **Verifies:** §03 v2.3.0, AC-73, AC-74, AC-75, §18 v2.9.2, §17 (`NdjsonHeaderFrame.StateTransition`), §01 v3.8.10, §49 §AC-77 detail below.

### AC-77 §D1 — Cell composition (normative)

The cell MUST render BOTH:
1. The raw `HasError` boolean as a glyph: ✅ when `HasError=0`, ❌ when `HasError=1`
2. The AC-73 derived state-transition label as an immediately-adjacent chip

The chip MUST carry the canonical English key as a stable selector hook via the HTML attribute `data-state-label="<key>"` where `<key>` ∈ `{still-green, first-failure, still-failing, just-recovered}`.

### AC-77 §D2 — Pure-function derivation (normative)

The label MUST be derived per AC-73's pure-function rule from the row's current `(PreviousHasError, HasError)` tuple **at render time**. The following are explicit SPEC VIOLATIONS:
- caching the derived label
- recomputing from a separate query
- storing as a denormalized `StateLabelCache` column

AC-75's single-statement write atomicity guarantees the tuple is consistent at read time, so re-derivation is safe and correct.

### AC-77 §D3 — Exhaustive 4-label handling (normative)

The renderer MUST handle all four labels exhaustively with NO `unknown` / `initial` / `n/a` fallback. A tuple outside the 4-value space is a §18 CHECK violation and MUST surface via §15 `GL-INTERNAL`.

### AC-77 §D4 — Localization parity (normative)

Localization MAY translate the *display chip text* but MUST keep the `data-state-label="<key>"` attribute set to the canonical English key for:
- CSS / e2e selector stability
- OpenAPI `NdjsonHeaderFrame.StateTransition` enum parity (§17 v2.9.3+)

### AC-77 §D5 — Color-blind safety (normative)

Color MUST NOT carry meaning alone. Every chip MUST also include a glyph or the literal label text so users can distinguish `still-green` from `just-recovered` (both green) and `first-failure` from `still-failing` (both red).

### AC-77 §D6 — Column controls (normative)

Column-header click on the `HasError + StateLabel` column MUST offer:
- a 4-way label sort
- a 4-value multi-select filter defaulting to "all four selected" (no implicit hiding of `still-failing` rows)

### AC-77 §D7 — Cross-consumer parity (normative)

The rendered label for a given `PipelineId` at a given instant MUST equal the `Header.StateTransition` value emitted by the AC-74 NDJSON consumer for the same `PipelineId` at the same instant. Divergence is a bug filed under `GL-INTERNAL` per the cross-consumer parity rule of AC-73's pure-function derivation.

### AC-77 §D8 — Verifies

§03 v2.3.0 (`## State-Transition Label Rendering` section + History columns table revision); AC-73 (label enum + pure-function rule); AC-74 (NDJSON `Header.StateTransition` consumer — cross-consumer parity counterpart); AC-75 (back-fill + single-statement write atomicity); §18 v2.9.2 (`CHECK (PreviousHasError IN (0,1))` + `CHECK (HasError IN (0,1))`); §17 (`components.schemas.NdjsonHeaderFrame.StateTransition` wire enum); §01 v3.8.10 (`PreviousHasError` glossary entry).

---

## Cross-References

- [§97 — Acceptance Criteria](./97-acceptance-criteria.md) (binding parent — Section A entries)
- [§03 — Admin UI](./03-admin-ui.md)
- [§18 — schema.sql](./18-schema.sql)
- [§17 — OpenAPI](./17-openapi.yaml)
- [§01 — Glossary & enums](./01-glossary-and-enums.md)
- [§15 — Error codes](./15-error-codes.md)

# Acceptance Criteria — Top-Level Research Index

**Version:** 2.1.0
**Updated:** 2026-04-30 (Phase 153 Task A13 — AC-RESEARCH-05 Verifies clause + AC-RESEARCH-07 domain-registry validator)

---

### AC-RESEARCH-01: Inlined contract validates  `[critical]`
- **Given** The contract block in `00-overview.md`.
- **When** The contract is parsed by its language tooling (jsonschema/tsc/sqlite).
- **Then** Parsing MUST succeed with zero diagnostics.

### AC-RESEARCH-02: Schema-required fields enforced  `[critical]`
- **Given** A new entry conforming to the contract.
- **When** A required field is omitted.
- **Then** Validation MUST fail with a clear "missing required field" error citing the field name.

### AC-RESEARCH-03: ID pattern enforced  `[high]`
- **Given** An entry with an `id` field.
- **When** The id does not match the documented regex pattern.
- **Then** Validation MUST fail and the offending value MUST be echoed in the error.

### AC-RESEARCH-04: Lifecycle diagram present and valid  `[high]`
- **Given** This subfolder.
- **When** Listing files.
- **Then** Exactly one `lifecycle-*.mmd` file MUST exist and parse as a valid Mermaid `flowchart TD`.

### AC-RESEARCH-05: Forward-only updates  `[medium]`
- **Given** A change to the contract block in `00-overview.md` (the inlined JSON Schema for `TopLevelResearchEntry`).
- **When** A diff is computed between the prior `00-overview.md` (preceding §98 row) and the new one.
- **Then** Removed `properties.*` keys MUST first be marked deprecated (added to `description` with the prefix `DEPRECATED: …`) for at least one minor §98 version before deletion; renamed fields MUST add the new key AND keep the old key as an alias (both validate) for one minor §98 version.
- **Verifies:** the SemVer minor-bump invariant for the inlined schema (a removed/renamed required field is a breaking change and forbidden inside a single minor bump); enforced by `linter-scripts/check-version-parity.py` (any §00-schema diff without a paired §98 row fails parity) + manual PR review against this AC. **Source:** A13 close of v6 audit D2 LOW finding "Vague Verification Clauses".

### AC-RESEARCH-06: Cross-references stay valid  `[medium]`
- **Given** This subfolder's `00-overview.md`.
- **When** `linter-scripts/check-spec-cross-links.py` runs.
- **Then** Exit code MUST be 0; all relative links MUST resolve.

### AC-RESEARCH-07: `domains[]` entries resolve to on-disk spec modules  `[high]`
- **Given** A `TopLevelResearchEntry` with a `domains` array (per the inlined JSON Schema in `00-overview.md`).
- **When** Each entry is validated.
- **Then** Every element of `domains` MUST match the regex `^(?:spec/)?\d{2}-[a-z][a-z0-9-]*(?:/\d{2}-[a-z][a-z0-9-]*)*/?$` AND MUST resolve to an existing directory under the repo's `spec/` tree (top-level module slug `NN-kebab-name` or nested subfolder of the same form). Validation MUST fail with a clear error citing the unresolved path AND the offending entry's `id`.
- **Verifies:** the `"MUST be at least 2 spec module relpaths"` constraint inlined at `01-research-index/00-overview.md` line 30 — schema currently enforces only `type: string + minItems: 2`, leaving "spec module relpath" semantically un-validated. Closes **A13 v6 audit D3 MEDIUM finding "Undefined Domain Registry"** by binding the relpath shape to a regex AND requiring on-disk resolution against the `spec/` tree (the master module list is the on-disk inventory, not a hard-coded enum — automatically tracks new modules without a contract bump per Lesson #36 link-don't-restate). Implementations MUST treat archived paths under `spec/_archive/` as INVALID for new entries (deprecated content cannot be a research domain). **Source:** A13 close of v6 audit D3 MEDIUM finding "Undefined Domain Registry".

# Acceptance Criteria — Git Logs Diagram Conventions

**Version:** 2.0.0
**Updated:** 2026-04-27

---

### AC-DIAGRAMC-01: Inlined contract validates  `[critical]`
- **Given** The contract block in `00-overview.md`.
- **When** The contract is parsed by its language tooling (jsonschema/tsc/sqlite).
- **Then** Parsing MUST succeed with zero diagnostics.

### AC-DIAGRAMC-02: Schema-required fields enforced  `[critical]`
- **Given** A new entry conforming to the contract.
- **When** A required field is omitted.
- **Then** Validation MUST fail with a clear "missing required field" error citing the field name.

### AC-DIAGRAMC-03: ID pattern enforced  `[high]`
- **Given** An entry with an `id` field.
- **When** The id does not match the documented regex pattern.
- **Then** Validation MUST fail and the offending value MUST be echoed in the error.

### AC-DIAGRAMC-04: Lifecycle diagram present and valid  `[high]`
- **Given** This subfolder.
- **When** Listing files.
- **Then** Exactly one `lifecycle-*.mmd` file MUST exist and parse as a valid Mermaid `flowchart TD`.

### AC-DIAGRAMC-05: Forward-only updates  `[medium]`
- **Given** A change to the contract block.
- **When** Reviewed in PR.
- **Then** Removed fields MUST first be marked deprecated for at least one minor version before deletion; renamed fields MUST add the new name and keep the old one as an alias for one minor version.

### AC-DIAGRAMC-06: Cross-references stay valid  `[medium]`
- **Given** This subfolder's `00-overview.md`.
- **When** `linter-scripts/check-spec-cross-links.py` runs.
- **Then** Exit code MUST be 0; all relative links MUST resolve.

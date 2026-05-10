# Acceptance Criteria — 23 App Database

**Version:** 2.0.0  
**Updated:** 2026-04-25  
**Scope:** `spec/02-coding-guidelines/23-app-database/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

This module defines the application-specific database architecture, including data models, table designs, and query patterns, ensuring they align with the project's global database conventions.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

- Table Naming: snake_case, plural (e.g., `user_profiles`, not `UserProfile`).
- Column Naming: snake_case (e.g., `is_active`, not `isActive`).
- Mandatory Columns: 
    - `id` (UUID, Primary Key)
    - `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
    - `updated_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
    - `deleted_at` (TIMESTAMP WITH TIME ZONE, NULLABLE - for soft deletes)
- Constraints: All Foreign Keys (FK) must have an explicit name following the pattern `fk_[table_name]_[column_name]`.
- Indexes: All Indexes must follow the pattern `idx_[table_name]_[column_name]`.
- Enums: Stored as VARCHAR with application-level validation or native Postgres ENUM types as specified in the conventions document.

---

## Acceptance Criteria

### AC-01: Strict Numeric File Naming Convention  `[high]`
- **Given** A new database design document is being added to the `spec/02-coding-guidelines/23-app-database` folder
- **When** The file is created and committed to the repository
- **Then** The filename must follow the numeric prefixing pattern (e.g., `01-users-table.md`) as specified in the Contents section
- **Verifies:** 00-overview.md - Contents section

### AC-02: Compliance with Parent Database Conventions  `[critical]`
- **Given** An app-specific database design document within this module
- **When** Defining new table structures or columns
- **Then** The document must use the standard naming conventions defined in `../../17-consolidated-guidelines/18-database-conventions.md` (e.g. snake_case for table names, pluralized)
- **Verifies:** 00-overview.md - Cross-References table

### AC-03: Mandatory Audit Column Inclusion  `[medium]`
- **Given** A database table definition in any file in this module
- **When** A new table is documented in a numbered file in this folder
- **Then** The schema must include mandatory audit columns defined in the Consolidated Database Conventions: `created_at`, `updated_at`, and `deleted_at` (if soft-delete is enabled)
- **Verifies:** ../../17-consolidated-guidelines/18-database-conventions.md

### AC-04: Parameterized Query Enforcement  `[high]`
- **Given** A query pattern described in a numbered file within this module
- **When** Documentation specifies application-side query logic
- **Then** The query must demonstrate the use of parameterized inputs to prevent SQL injection as per the Coding Guidelines Overview
- **Verifies:** ../00-overview.md

### AC-05: UUID Primary Key Standardization  `[critical]`
- **Given** A table design documenting a Primary Key (PK)
- **When** Adding a new table schema to a markdown file in this folder
- **Then** The PK must be defined as a UUID (Universally Unique Identifier) unless a specific exception for BIGSERIAL/Identity is justified in the 'data model decisions' section
- **Verifies:** 00-overview.md - Purpose section

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
# 12 — Queued-Decisions Trail Format

**Version:** 1.0.0  
**Updated:** 2026-04-26  
**Scope:** `spec/01-spec-authoring-guide/`  
**Status:** Stable

---

## Purpose

When a spec module accumulates user decisions that span multiple sessions or multiple SemVer bumps, those decisions need a **queued-decisions trail** — a structured record of:

1. **What was decided** (the architectural commitment).
2. **What state it's in** (queued, in-progress, landed, abandoned).
3. **What files it touched** (or will touch) when it lands.
4. **What the next executable step is** (so a fresh AI session can resume without re-litigating).

This document codifies the trail format that has been used informally in `mem://specs/git-logs.md` since v3.7.x and is now mandatory for any module with ≥ 3 multi-session decisions.

---

## Why a formal trail

### Problem this solves
- Sessions are stateless. The next AI (or the next human reading the spec months later) cannot reconstruct *why* a particular table column exists, *what alternatives were rejected*, or *which decisions are still pending* from the spec body alone.
- The §98 changelog records what shipped, not what was *queued* and not yet shipped.
- The §99 consistency report records structural health, not architectural intent.
- Memory files (`mem://`) carry intent across sessions but have no enforced format → over time they decay into prose nobody can parse.

### What the trail guarantees
- Every multi-session decision has exactly **one** canonical row, in **one** canonical place (the module's `mem://specs/<slug>.md` file).
- A `next` command in any future session can locate the next executable decision by string-matching `### Q[0-9]+ — ` headings and filtering by status.
- Lockstep edits (banner + §98 + §99 + memory) are explicit, not implied.

---

## File location

The trail lives in the module's memory file:

```
mem://specs/<module-slug>.md
```

Where `<module-slug>` matches the spec folder slug (e.g. `git-logs` for `spec/22-git-logs-v2/`).

If the module has no memory file yet, create one with the standard frontmatter:

```markdown
---
name: <Module Name> spec layout
description: <one-line description with current banner version>
type: reference
---
```

Trail sections are **always** appended at the end, never interleaved with the architectural summary at the top. Order from top:

1. Authoritative folders / locked decisions (top-level summary)
2. Open questions (small, awaiting user input)
3. **Queued decisions — v<X.Y.Z>** sections (the trail; this document's subject)
4. Locked decisions awaiting implementation (queued, longer-form)
5. Pending housekeeping (queued, not blocking)

---

## Trail entry format

Each decision is a level-3 heading with a stable `Q<n>` identifier:

```markdown
### Q<n> — <short imperative title> <status-marker>

- **What:** 1-2 sentences. The architectural commitment.
- **Why:** 1 sentence. Rationale or rejected alternative.
- **Files to update (when landing):** comma-separated relative paths from the module folder.
- **New error codes / seeds / config keys (queue):** any side-effect rows that need to land in §15 / §18 seeds / `ConfigKv`.
- **Status notes:** any constraints, dependencies on other Q<n>, or blast-radius warnings.
```

### `Q<n>` numbering
- Monotonically increasing **per memory file**, never reset.
- Once assigned, **never reused** — even if the decision is abandoned, the slot stays with a tombstone.
- This mirrors the immutable-slot rule for spec files (cf. `mem://index.md` Core).

### Status markers (in the heading itself)

| Marker | Meaning |
|--------|---------|
| *(none)* | Queued — decided in principle, not yet shipped |
| `🔄 IN PROGRESS v<X.Y.Z>` | Actively being implemented in the named SemVer bump |
| `✅ LANDED v<X.Y.Z> (YYYY-MM-DD)` | Shipped; entry retained for archaeology |
| `❌ ABANDONED v<X.Y.Z> (YYYY-MM-DD)` | Decided against; entry retained as a tombstone explaining why |
| `⏸ PAUSED — <reason>` | Started then deferred (e.g. blocked on infra, awaiting user input) |

The marker MUST appear in the heading text so a regex `/^### Q\d+ — .* (✅|❌|⏸|🔄)/` can classify any trail without parsing the body.

### Landing-time updates (mandatory)

When a queued decision lands:

1. Flip the marker to `✅ LANDED v<X.Y.Z> (YYYY-MM-DD)`.
2. **Replace** the body with a landing report (not an append) — what actually shipped, what files were touched, any deviations from the queue plan.
3. Update the memory file's frontmatter `description:` if the high-level state changed.
4. Cross-reference the §98 changelog row that corresponds to this landing.

The pre-landing queue body is **not** preserved — it is superseded by the landing report. Git history is the audit trail for the original plan.

---

## Lockstep with §98 and §99

Per project memory Core: *"Spec edits keep these in lockstep: target file banner + §98 changelog row + §99 health/inventory + `mem://specs/<slug>.md` queued-decisions trail."*

When a queued decision lands, **all four** edits MUST happen in the same session:

| Edit | Location | What changes |
|------|----------|--------------|
| Target file banner | The spec file the decision modifies | Bump SemVer (at least minor on content change) |
| §98 changelog row | `spec/<module>/98-changelog.md` | New release row referencing the Q<n> identifier |
| §99 health/inventory | `spec/<module>/99-consistency-report.md` | Inventory row updated; banner bumped |
| Memory trail | `mem://specs/<slug>.md` | Q<n> marker flipped + body replaced with landing report |

Skipping any of the four breaks the audit chain. CI does not (yet) enforce this — it is on the AI to perform the lockstep edit set atomically.

### When the audit chain is broken

If a session ships a spec change without updating the memory trail (a known regression vector), the next session that opens the memory file will see a stale queue. The recovery procedure:

1. Read the §98 changelog rows since the last memory update.
2. For each row that corresponds to a Q<n>, retroactively flip the marker.
3. Add a `## Audit-recovery note` section at the bottom of the memory file noting the gap.
4. Do not silently overwrite — the tombstone explaining the gap is part of the audit chain.

---

## Worked example

Real, unredacted excerpt from `mem://specs/git-logs.md`:

```markdown
### Q1 — `IsOrganization` boolean on GitProfile ✅ LANDED v3.8.1 (2026-04-26)
- Replaced `OwnerType` lookup table (User|Organization) with explicit
  `IsOrganization INTEGER 0/1 NOT NULL DEFAULT 0` column on `GitProfile`.
  Drives URL canonicalization and admin-UI checkbox label "Is organization".
- Files updated: §03 admin-ui (banner v2.0.0→v2.1.0), §16 seed-data
  (banner v2.7.0→v2.7.1), §18 schema.sql (banner v2.8.7→v2.8.8),
  §97 (AC-54 + AC-55 added, banner v3.8.0→v3.8.1), §98 (v3.8.1 row),
  §99 (tombstone + audit subsection, banner v3.8.0→v3.8.1).
- Linters green: cross-link 0 broken; tree-health 100/100.

### Q3 — Per-SHA split-DB log storage (apply spec/05-split-db-architecture)
- Root DB keeps **only** the SHA *registry*. Move `LogEntry` and
  `ErrorLogEntry` out into per-SHA SQLite files.
- Files: new §39 split-db-log-storage.md, §02 schema, §15 error-codes,
  §18 schema.sql, §22 retention, §23 backup, §29 uninstall, 26-gitlogs-diagrams/01-er + 02-domain.
- New error codes (queue for §15): `GL-SHA-DB-CREATE-FAILED`,
  `GL-SHA-DB-OPEN-FAILED`, `GL-SHA-DB-CORRUPT`, `GL-SHA-DB-NOT-FOUND`.
- Status: queued. Largest blast radius of the v3.8.x decisions.
```

Q1 has landed and shows the post-landing report format. Q3 is still queued and shows the pre-landing format with `Files:` and `New error codes (queue for ...):` sections.

---

## When this document applies

| Trigger | Trail mandatory? |
|---------|------------------|
| Module has ≥ 3 multi-session architectural decisions | **Yes** |
| Module is in active rapid-iteration phase (≥ 2 SemVer bumps per week) | **Yes** |
| Module has any user-blocked decision (`B1` style) | **Yes** |
| Module has only 1-2 decisions, all shipped same session | No — `§98` changelog suffices |
| Module is feature-complete and frozen | No — but retain any existing trail as archaeology |

The trail is a tool for managing *flux*. Frozen modules don't need it; new high-flux modules do.

---

## Acceptance criteria

### AC-12-01 — Trail file exists for high-flux modules
- **Given** a module with ≥ 3 multi-session decisions in its §98 changelog,
- **When** `mem://specs/<slug>.md` is opened,
- **Then** it MUST contain at least one `## Queued decisions` or `## Locked decisions awaiting implementation` section.

### AC-12-02 — Q-identifier monotonicity
- **Given** any memory file with a queued-decisions trail,
- **When** Q-identifiers are extracted in document order,
- **Then** they MUST be strictly increasing (no reuse, no skips that hide tombstones).

### AC-12-03 — Status marker presence
- **Given** any `### Q<n> — ` heading older than 7 days,
- **When** the heading is inspected,
- **Then** it MUST carry one of the 4 non-default status markers (`🔄`, `✅`, `❌`, `⏸`) — pure-queued state is only acceptable for fresh decisions.

### AC-12-04 — Lockstep on landing
- **Given** a Q<n> marker flipped to `✅ LANDED v<X.Y.Z>` in this session,
- **When** the same session's edits are reviewed,
- **Then** the §98 changelog of the affected module MUST contain a row for `v<X.Y.Z>` AND the §99 banner MUST have been bumped AND the target spec file's banner MUST have been bumped.

### AC-12-05 — Landing report replaces queue body
- **Given** a Q<n> marked `✅ LANDED`,
- **When** the body is inspected,
- **Then** it MUST describe what shipped (with concrete file/banner pairs) — NOT the original "Files to update (when landing)" plan. Git history preserves the original plan.

---

## Cross-references

- [`07-memory-folder-guide.md`](./07-memory-folder-guide.md) — `.lovable/memory/` tree conventions.
- [`08-cross-references.md`](./08-cross-references.md) — link integrity rules referenced by trail entries.
- [`mem://index.md`](mem://index.md) — Core memory rule for lockstep edits.
- [`mem://specs/git-logs.md`](mem://specs/git-logs.md) — reference implementation of this format.
- [`spec/22-git-logs-v2/98-changelog.md`](../22-git-logs-v2/98-changelog.md) — example of §98 rows that correspond to landed Q<n> entries.

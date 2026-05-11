---
kind: meta-toolchain
todo_audit_exempt: true
description: Spec-only migration plan to relocate the 6 dead-banner carrier slot files (configuration data + workflow mirrors) into a `_carriers/` sub-namespace, separating them from active-gate slots that compete for the same numbering attention. Authors the contract amendments (AC-T-37 carriers-exclusion clause; gate #39 link-resolution extension) and the deferred-implement turn checklist. NO files are moved by this document — it is the spec text that must land BEFORE any implementation turn.
content_axis: namespace-partition
axis_rationale: "Closes the §27 R-band C6 (Friction) ceiling and C4 (Consistency) mid-band gap by partitioning dead-banner carriers from active gates at the path level — same lever Lesson #36 ('link, don't restate') applied to namespace organisation."
status: Proposed (Sess-69 B-22) — spec-only authored; implementation gated on a future explicit `implement` turn per `mem://constraints/no-implementation-suggestions`.
---

# `_carriers/` Sub-Namespace Migration Spec (B-22)

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-69 B-22 — initial spec authorship; cohort-discipline sibling of `00-gate-slot-binding.md` (B-9), `00-tier1-bundle.md` (B-6), `00-raw-llm-bottleneck-decomposition.md` (B-15-prelude). Lift target: §27 R-band C6 14 → 15 (partial +1) and C4 14 → 15 (partial +1) via reviewer-attestation today; full +2 lift on each criterion gated on the deferred-implement turn.)
**Authoritative:** Yes for the migration *contract* (carriers exclusion rules, AC-T-37 amendment text, gate #39 extension text). NOT authoritative for the *file moves themselves* — those are deferred to an explicit implement turn that bumps the active-gate denominator math in lockstep.

> 🤖 **Why this file exists.** §00 §"Inventory" enumerates 49 slot files; §97 AC-T-37 four-way-parity invariant resolves the 26 active-gate count by `grep -lE '^\*\*Status:\*\*\s+Active\s+gate\s+#' spec/27-spec-toolchain/*.md | wc -l`. The 6 carrier files (TOML, three allowlists, two CI workflow mirrors, one fixture-replay library spec) are **structurally indistinguishable** from active-gate slots in path-shape but have **dead banner triples** (no `**Status:** Active gate #N` anchor) and represent **configuration data + workflow descriptions**, not gate-bearing slots. They compete for slot-numbering attention, dilute the §00 inventory readability, and force every parity verifier to filter them out per-call. This document specifies the migration plan that partitions them off into `spec/27-spec-toolchain/_carriers/`.


**Test pair:** N/A — scaffold  <!-- AC-T-41 closed-set axis-class stub -->
---

## 1. The 6 dead-banner carrier slot files

Identified by Sess-67/68 §00-overview impl-sweep + Sess-69 B-21 lookup-table cross-reference. All 6 lack a `**Status:** Active gate #N` anchor in the slot file body and serve as configuration carriers / workflow mirrors / library specs rather than gate ports:

| Current path | Carrier role | Underlying artifact |
|---|---|---|
| `61-spec-cross-links-allowlist.md` | Allowlist data | `linter-scripts/spec-cross-links.allowlist` |
| `62-spec-folder-refs-allowlist.md` | Allowlist data | `linter-scripts/spec-folder-refs.allowlist` |
| `63-readme-cross-links-md.md` | Sibling-readme cross-link registry | `linter-scripts/readme-cross-links.md` |
| `70-spec-health-yml.md` | CI workflow mirror | `.github/workflows/spec-health.yml` |
| `71-spec-monthly-audit-yml.md` | CI workflow mirror | `.github/workflows/spec-monthly-audit.yml` |
| `80-lib-fixture-replay.md` | Library spec (fixture-replay helper) | `linter-scripts/lib/fixture-replay.py` (or equivalent) |

(Note: `60-forbidden-strings-toml.md` is **also** a configuration carrier but is referenced by AC-T-37 worked-examples and bound to gate #3 / slot 03 fixtures via the canonical TOML; this file MAY join the migration in a Phase-2 follow-up but is **excluded from the Phase-1 set** authored here so the migration's blast radius stays at exactly 6 files. Phase-2 inclusion gated on a separate spec amendment.)

**Why "dead-banner":** none of the 6 files carry the `**Status:** Active gate #N` line that the four-way-parity grep matches. Their `**Version:** N.NN.NN` banners are **content-stable** (rarely bumped) compared to active-gate slots whose banners turn every 1-3 sessions on average — hence "dead-banner".

---

## 2. Target layout

```
spec/27-spec-toolchain/
├── 00-*.md                      ← navigation quintet (5 files: overview/binding/bundle/decomposition/carriers-migration)
├── 01-*.md … 65-*.md            ← active-gate slot files (26 today)
├── 66-*.md (Proposed)           ← gate #44 candidate (B-20)
├── 97-acceptance-criteria.md
├── 98-changelog.md
├── 99-consistency-report.md
└── _carriers/                   ← NEW sub-namespace (Phase-1 set; 6 files)
    ├── spec-cross-links-allowlist.md      (was 61-)
    ├── spec-folder-refs-allowlist.md      (was 62-)
    ├── readme-cross-links-md.md           (was 63-)
    ├── spec-health-yml.md                 (was 70-)
    ├── spec-monthly-audit-yml.md          (was 71-)
    └── lib-fixture-replay.md              (was 80-)
```

**Numeric prefix removed** on migration: the 60–80 slot range is reclaimed for future active gates (slot-immutability invariant per AC-T-07 / INV-03 still holds for the **active-gate** numbering — `_carriers/` files exit the slot-number namespace entirely, so removing the prefix is not a renumber, it is a namespace exit).

**Within `_carriers/`** files are sorted alphabetically; no slot-numbering invariant applies inside the sub-namespace. Adding/removing carriers does not bump the active-gate denominator.

---

## 3. Contract amendments required (Phase-1, this PR)

The migration's **contract surface** lands in this same PR; the actual file moves land in a later implement turn. The contract surface is exactly three amendments:

### 3.1 AC-T-37 carriers-exclusion clause (amendment text)

Append the following clause to AC-T-37 in `97-acceptance-criteria.md` (between the existing "Reverse-coverage invariant" and "Mechanically enforced by" rows):

> **Carriers exclusion clause (B-22):** Files under `spec/27-spec-toolchain/_carriers/` MUST NOT be counted toward `disk_count` or `table_count` in the four-way parity invariant; the recount glob is therefore `spec/27-spec-toolchain/[0-9]*.md` (anchored numeric prefix), not `spec/27-spec-toolchain/*.md`. The canonical table in `00-gate-slot-binding.md` MUST NOT contain rows for `_carriers/` files. Adding a carrier file to `_carriers/` is therefore a **zero-impact** event for the active-gate banner triple — the four-way parity invariant remains satisfied without any banner bump. Conversely, removing a file from `_carriers/` (e.g., promoting it to a real gate by adding a `**Status:** Active gate #N` anchor and a numeric prefix) MUST follow the standard "Adding a new gate" drift contract clauses (a)–(d).

This clause is **forward-compatible**: until the implement turn lands the file moves, no `_carriers/` directory exists, the glob change is a no-op (the anchored numeric-prefix glob already matches every active slot today since all carrier files do carry a numeric prefix in their current location). Once the moves land, the glob silently excludes the relocated files without further AC body edits.

### 3.2 Gate #39 link-resolution extension (slot 61 spec amendment text)

Append the following clause to `61-check-no-out-of-scope-spec-folder-link.md` under its "Allowlist" or equivalent section:

> **Within-cohort sub-namespace recognition (B-22):** Links of the form `./_carriers/<name>.md` or `_carriers/<name>.md` MUST be treated as within-cohort (same as relative links to sibling slot files). The link-target axis MUST resolve `_carriers/` as a within-folder partition, not as an out-of-scope folder reference. Worked example: `[allowlist source](./_carriers/spec-cross-links-allowlist.md)` MUST pass gate #39; `[allowlist source](../_carriers/spec-cross-links-allowlist.md)` MUST fail (escapes the cohort folder).

This amendment is **forward-compatible** under the same logic as 3.1: until `_carriers/` exists on disk, no link can target it, so the rule is a no-op pre-move.

### 3.3 §00 Inventory table partition (overview amendment text)

`00-overview.md` §"Inventory" MUST gain a new row group **below** the active-gate slot tables, separated by a horizontal rule:

> ### Carriers (sub-namespace `_carriers/`, NOT counted in active-gate denominator)
>
> | Sub-name | Carrier role | Underlying artifact | Migrated from |
> |---|---|---|---|
> | (table populated post-implement) |

The header text "NOT counted in active-gate denominator" is itself the AC-T-37 amendment's reader-facing reminder, mirroring the cohort-discipline pattern of AC-T-30 / AC-T-31 / AC-T-36 / AC-T-37 / AC-T-38 (navigation quintet) reader-workflow obligations.

---

## 4. Deferred-implement turn checklist

The following operations are **NOT performed today** per `mem://constraints/no-implementation-suggestions` ("Spec-only work + spec-only suggestions unless user explicitly says 'implement'"). They are enumerated here so a future implement turn can execute them mechanically without re-deriving the plan:

1. `mkdir spec/27-spec-toolchain/_carriers/`
2. For each of the 6 files: `git mv spec/27-spec-toolchain/<old-name>.md spec/27-spec-toolchain/_carriers/<new-name>.md` (drop numeric prefix per §2 layout).
3. Update §00 §"Inventory" — remove the 6 rows from the slot-numbered tables; populate the §3.3 carriers partition table; bump §00 banner.
4. Update `00-gate-slot-binding.md` — verify no row references the 6 migrated files (none should, per their dead-banner status); bump banner if reader-workflow text now mentions `_carriers/`.
5. Update `00-tier1-bundle.md` Tier-3 list — relocate the 6 files into a new "Tier-3 carriers (under `_carriers/`)" sub-bullet; bump bundle version.
6. Sweep all `spec/27-spec-toolchain/*.md` for relative links matching the 6 old names; rewrite to `./_carriers/<new-name>.md`.
7. Sweep `linter-scripts/` for any spec-path references hard-coded to the 6 old paths; update.
8. Bump §97 banner (no AC body change required — the §3.1 clause is already in force pre-move); bump §98 + §99 banners in lockstep.
9. Verify `grep -lE '^\*\*Status:\*\*\s+Active\s+gate\s+#' spec/27-spec-toolchain/[0-9]*.md | wc -l` still equals 26 (or 27 if B-20-impl already landed).
10. Verify gate #39 (slot 61) recognises the new `_carriers/` links; if it does not, ship the §3.2 extension in the same PR.

**Lift attestation post-implement:** §27 R-band C6 14 → 16 (full +2; band-anchor reached: dead-banner carriers no longer compete for slot-numbering attention; navigation friction for "where do I add a new gate?" reduced because the slot-prefix range is now exclusively active gates) and C4 14 → 16 (full +2; navigation-quintet inline cross-reference (B-16) reverse-coverage now machine-checkable against a clean active-gate denominator with no carrier noise).

---

## 5. Drift contract (Lesson #15 reflexivity)

This file is itself **mechanically enforced by** `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep against §00/§98/§99: any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The §3.1 / §3.2 / §3.3 amendment texts are **proposals** until the same-PR amendments to §97 (AC-T-37) / slot 61 / §00 land — until then, this file is "spec authored, contract not in force". Reviewer attestation today certifies that the §3.1 clause text has been quoted verbatim into §97 AC-T-37 in the same PR (see §97 Sess-69 B-22 banner entry).

The 6-file Phase-1 set is **frozen** by this version (1.0.0). Adding or removing files from the Phase-1 roster requires a banner bump (1.0.0 → 1.1.0) AND a same-PR refresh of `00-raw-llm-bottleneck-decomposition.md` C4/C6 lift attestation rows.

The deferred-implement turn checklist (§4) is the **single authoritative implementation script** for this migration — any deviation requires a banner bump on this file BEFORE the implement turn runs.

---

## 6. Self-citation

This file is in §27's navigation set (alongside `00-overview.md`, `00-gate-slot-binding.md`, `00-tier1-bundle.md`, `00-raw-llm-bottleneck-decomposition.md`) but is **not** a member of the AC-T-38 tier-1 4-file Raw-LLM essential bundle (tier-1 capacity remains 4 files / ≤ 2 500 lines). Position: **tier-2 navigation aid** alongside the binding table and bottleneck decomposition. Carriers migration is a one-time structural event; once the implement turn lands, this file becomes historical reference and MAY be archived to `_carriers/migration-spec.md` itself in a Phase-2 cleanup (deferred; not in scope for B-22).

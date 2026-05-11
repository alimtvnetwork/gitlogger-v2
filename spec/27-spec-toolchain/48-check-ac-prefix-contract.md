# Slot 48 — `check-ac-prefix-contract.py`

**Status:** Active gate #29 (Phase-5 T-22)
**Implements:** §22 + §23 + §24 + §25 + §26 + §27 + §28 §97
cross-folder AC-prefix ownership contract (closes §27 backlog
`ac-prefix-contract-check` minted T-14)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§97 AC-prefix contract gate"

## Contract

Walks every `97-acceptance-criteria.md` file under the seven in-scope
folders and asserts the **AC-prefix↔folder ownership map** is honoured.
Closes the §27 backlog `ac-prefix-contract-check` ticket minted T-14
— the second-oldest un-shipped structural-hygiene backlog entry.
Slot 47 (gate #28) enforces *within-file* §97 hygiene; this slot
enforces *cross-file* AC-ID disjointness so foreign-AC restate is
machine-detectable.

### Ownership map (canonical, T-22 baseline)

| Folder | Owned prefix-root(s) | Notes |
|---|---|---|
| §22 `git-logs-v2` | `AC-NN` (bare-numeric), `AC-22-CE\d+`, `AC-22-LV\d+`, `AC-COHORT-\d+` | Bare-numeric is the legacy v2 namespace; new ACs SHOULD use a sub-prefix. |
| §23 `app-database` | `AC-ADB-*` | Single-root folder. Sub-namespaces `AC-ADB-REST-NN` + `AC-ADB-SETTING-NN` (declared in §23 §00) are owned by the `AC-ADB-` root and pass clause-1. |
| §24 `app-design-system-and-ui` | `AC-ADS-*`, `AC-CAF-NN` | `AC-CAF-NN` is the cross-cutting App-framework namespace owned by §24 (CAF-01..05 land here per T-12). Sub-namespace `AC-ADS-UI-NN` (declared in §24 §00) owned by `AC-ADS-` root. |
| §25 `app-issues` | `AC-AI-*`, `AC-NN` (bare-numeric, legacy phase-2) | `AC-AI-*` covers `AC-AI-NN`, `AC-AI-NNN` (e.g. `AC-AI-000`), and any future `AC-AI-XYZ-NN` sub-namespace. |
| §26 `gitlogs-diagrams` | `AC-DG-*`, `AC-NN` (bare-numeric, legacy diagram-inventory) | `AC-DG-*` covers `AC-DG-NN` and any future sub-namespace. |
| §27 `spec-toolchain` | `AC-T-*` | Single-root folder. Sub-namespaces (e.g. `AC-T-PROMOTE-NN`) reserved for future PRs. |
| §28 `universal-ci-cli` | `AC-28-*` | Single-root folder. |

**Owned-root semantics (T-22 clarification):** a root listed with `*` (e.g. `AC-ADB-*`) owns the whole sub-tree — any AC-ID whose prefix path starts with that root is in-scope. `AC-CAF-NN` (no `*`) is a flat namespace; `AC-22-CE\d+` / `AC-22-LV\d+` are flat with a regex tail. Ownership-map round-trip (clause-5) flags any new root not listed above.

The ownership map is the single source of truth; the gate hard-codes
this table. Any change requires a §27 PR amending this slot doc AND
the affected folder's §97 in lockstep (the gate IS the lockstep
enforcer).

**Bare-numeric collision baseline (T-22 grandfathered):** real-disk
inspection at T-22 found §22 owns bare integers `1..41,49..85,87..90`
(81 IDs); §25 owns bare integers `1..8` (8 IDs); §26 owns bare integers
`22..26` (5 IDs). The shared-namespace overlap `{1,2,3,4,5,6,7,8,
22,23,24,25,26}` (13 collisions) is GRANDFATHERED at T-22 baseline.
Clause-3 rejects any NEW bare-numeric collision outside this 13-element
whitelist; existing collisions accumulated before T-22 are tolerated
because retro-renumbering 21 ACs across 3 folders would invalidate
every external citation in the corpus. Going-forward, §25 and §26
SHOULD mint new ACs under their sub-prefix (`AC-AI-` / `AC-DG-`).

### Invariants

Fails CI when ANY of the following invariants fail:

1. **Owner-folder declaration** — every `### AC-…` header in any
   §97 file MUST carry a prefix listed under that folder's owned
   set above. An AC declared in `spec/23-app-database/97-acceptance-criteria.md`
   that uses `AC-ADS-` or `AC-AI-` is a foreign-prefix declaration
   and fails clause-1 with the offending AC-ID + line + correct
   owner folder.
2. **No cross-folder AC-ID collision** — across all seven §97 files,
   every `AC-<prefix>-NN` (or bare `AC-NN`) MUST be unique
   *globally*. Two folders declaring the same fully-qualified
   AC-ID is a collision and fails clause-2 with both file:line
   pairs. (Within-file uniqueness is gate #28's clause-4 — this
   gate covers the cross-file complement.)
3. **Bare-numeric `AC-NN` namespace partitioning** — bare-numeric
   `AC-NN` is the legacy namespace SHARED by §22, §25, and §26.
   Within that shared namespace, no two folders may declare the
   same `AC-NN` integer. Owner partition (T-22 baseline):
   §22 owns `AC-01..AC-99` integers currently in its §97; §25 owns
   integers it currently declares; §26 owns integers it currently
   declares. The gate snapshots the baseline at first run and
   thereafter rejects any new bare-numeric collision across these
   three folders. (New ACs in §25 / §26 SHOULD use the sub-prefix
   `AC-AI-` / `AC-DG-` per the ownership map; bare-numeric is
   frozen-legacy.)
4. **No foreign-prefix declaration in §00-overview / §98 / §99** —
   §00-overview, §98-changelog, and §99-consistency-report files
   under each in-scope folder MUST NOT declare a NEW AC-ID using
   a foreign prefix (a `### AC-FOREIGN-NN` header where `FOREIGN`
   is not in the folder's owned set). *Mentions* of foreign ACs
   inside backticks or fenced blocks are allowed (covered by gate
   #27 AC-CAF-05 audit-quoted-evidence-marker discipline); only
   `### AC-…` *header* declarations of foreign prefixes fail
   clause-4. This catches §00-narrative drift where a section
   accidentally re-declares an AC owned by a sibling folder.
5. **Ownership-map round-trip** — the `Ownership map` table in
   THIS slot doc MUST list every prefix actually present across
   the seven §97 files. If the gate discovers a `### AC-NEWPREFIX-…`
   header whose `NEWPREFIX` is not in the slot doc's table, the
   gate fails clause-5 with `unknown-prefix: AC-<NEWPREFIX>- found
   in §<NN> §97 but not in slot 48 ownership map`. Closes the
   "silent-prefix-mint" escape hatch — every new prefix MUST land
   in the same PR as a slot 48 doc amendment.

## Invocation

```bash
python3 linter-scripts/check-ac-prefix-contract.py --check all
python3 linter-scripts/check-ac-prefix-contract.py --check owner-folder
python3 linter-scripts/check-ac-prefix-contract.py --check no-cross-folder-collision
python3 linter-scripts/check-ac-prefix-contract.py --check bare-numeric-partition
python3 linter-scripts/check-ac-prefix-contract.py --check no-foreign-in-meta
python3 linter-scripts/check-ac-prefix-contract.py --check ownership-map-round-trip
python3 linter-scripts/check-ac-prefix-contract.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3` fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

A scanner that returns 0 because zero §97 files were discovered, or
because zero `### AC-…` headers parsed, is **itself a violation**
(exit `1`, message `vacuous-pass: zero §97 files or zero AC headers
parsed`). The `--self-test` mode is mandatory in CI and asserts the
scanner correctly REJECTS six synthetic fixtures:

- **F-1** complete-uniform (every AC under owner folder; no
  collisions; bare-numeric partitioned cleanly; no foreign-prefix
  in §00/§98/§99; every present prefix listed in ownership map)
  → passes
- **F-2** §23 §97 declares `### AC-ADS-99` (foreign prefix in §23)
  → fails clause-1
- **F-3** Both §22 §97 and §25 §97 declare `### AC-77` (bare-numeric
  cross-folder collision) → fails clauses 2+3
- **F-4** §27 §97 declares `### AC-T-15`, §27 §97 *also* declares
  `### AC-T-15` in a different section (full collision; gate #28
  clause-4 would also fire — this gate's clause-2 is the cross-file
  complement; in single-file fixture this is the within-file dup,
  but the gate should catch the global-uniqueness pass) → fails
  clause-2
- **F-5** §24 §00-overview.md inserts `### AC-AI-42` header in a
  narrative section → fails clause-4 (foreign-prefix declaration
  in meta surface; AC-AI- belongs to §25)
- **F-6** §22 §97 declares `### AC-FOO-01` where `FOO` is not in
  the slot 48 ownership map table → fails clause-5 (unknown
  prefix; ownership-map round-trip broken)

## 5-link self-enforcement chain

1. **AC text** — every §97 file's `### AC-…` header set, plus
   §00-overview / §98-changelog / §99-consistency-report file
   sets per folder.
2. **Fixture surface** — synthetic in-memory tempdirs created by
   `--self-test` (6 short Markdown blobs reproducing the AC-prefix
   ownership geometry).
3. **Script** — `linter-scripts/check-ac-prefix-contract.py`
   (this slot).
4. **`--self-test`** — built-in mode, runs 6 fixtures (F-1 unique
   passing fixture).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§97 AC-prefix contract gate" hard-fails CI on any violation.
6. **Ownership map** — the table in Section "Contract" of THIS
   slot doc IS the single source of truth; clause-5 round-trip
   forces all prefix additions through a slot 48 PR.

## Bindings

- **§27 backlog ticket `ac-prefix-contract-check`** (T-14) — closes
  this turn (T-22). Second-oldest un-shipped backlog entry; the
  cross-file complement to slot 47's within-file enforcement.
- **Slot 47 / gate #28** (T-21, prior turn) — sibling. Slot 47
  enforces within-file AC-ID uniqueness (gate #28 clause-4); slot
  48 enforces cross-file AC-ID uniqueness (this gate clause-2).
  Together they make the AC-ID namespace globally unique by
  machine-checked construction.
- **Gate #27 / AC-CAF-05** (T-20) — sibling on the foreign-AC
  axis. Gate #27 enforces foreign-AC *quoting discipline* in
  §23/§24 prose + §25 finding bodies; gate #29 enforces foreign-AC
  *declaration discipline* in §00/§98/§99 headers (clause-4) and
  the ownership map itself (clauses 1+5). Together they close
  both the prose-leak and header-declaration leak vectors for
  foreign-AC restate.
- **§27 gate #15 D7-self-enforcement** (`derives-from-restate-check`)
  — clause-4 (no foreign-prefix declaration in meta surface) is
  the AC-namespace application of the cross-cutting D7 anti-restate
  contract. Before T-22, a §00 narrative could silently mint a
  foreign-AC header with no qualifier-strip lockstep; T-22 closes
  the escape hatch.
- **Lesson #36 link-don't-restate** — clause-1 + clause-2 + clause-4
  are the AC-namespace surface application of the cross-cutting
  Lesson #36 rule against retained restate. Foreign-AC declaration
  IS restate; the gate enforces by-construction non-restate.

## Red-green test pairs (AC-T-39)

- **RED:** introduce a fixture violation against any clause of this gate's `## Contract` closed-set (use the negative example documented in this slot's `**Self-test:**` synthetic-fixture roster, e.g. an `F-N` failing fixture, OR a corresponding fixture path under `linter-scripts/_fixtures/slot-48/`) and run `python3 linter-scripts/check-ac-prefix-contract.py --self-test` — MUST exit non-zero with a clause-numbered failure citing the violated invariant (gate #29 clause-N). Restore fixture / state to revert.
- **GREEN:** with no violation present (every `F-N` synthetic fixture in clean state per this slot's frontmatter `**Self-test:**` declaration), `python3 linter-scripts/check-ac-prefix-contract.py --self-test` MUST exit 0 with the gate's standard pass banner (e.g. `OK: gate #29 clean`); the GREEN baseline is the union of all clean-pass fixtures cited in this slot's frontmatter.

## Scorecard impact (Rubric v2 /120)
- **§22 / §23 / §24 / §25 / §26 / §27 / §28** — C4 (Consistency)
  +1 each (cross-folder AC-ID collision detection converts paper-only
  → load-proven; foreign-prefix declaration leak vector closed).
- **§27** — C5 (Implementability) holds at 20 (gates #15 + #28 + #29
  jointly self-enforce the AC-namespace discipline); C6 (Friction)
  +1 (second-oldest backlog ticket closed; ownership map +
  exit-code enumeration in slot doc).
- **§24** — C4 +1 additionally (CAF-NN namespace ownership now
  load-proven — the cross-cutting AC family lives in §24 by
  ownership-map decree).

## Out of scope

- AC **content** correctness (whether `AC-ADB-05` actually describes
  what its §00 narrative says) — this gate enforces only NAMESPACE
  OWNERSHIP, not semantic alignment.
- Bare-numeric `AC-NN` integer minting in §22/§25/§26 going forward
  — bare-numeric is frozen-legacy per the ownership map; new ACs
  MUST use sub-prefixes. The gate detects new collisions but does
  not enforce sub-prefix migration of existing legacy ACs.
- AC-IDs inside `_archive/`, fenced code blocks, backticks, or
  blockquotes — these are quotation/preservation surfaces, not
  declaration. The gate scans only `### AC-…` Markdown headers
  at column-0.
- Non-§97 / non-§00 / non-§98 / non-§99 markdown files — child
  trackers, sub-folder narratives, lifecycle diagrams. AC declarations
  in those files would themselves be a §97-monopoly violation (a
  separate hygiene contract; out-of-scope here, scoped by §27
  gate #14 / future gate as needed).
- §22 `AC-T-30` cross-cite — `AC-T-30` is a §27-owned AC referenced
  by §22 in `consumes:` front-matter and prose-cite. Per ownership
  map, `AC-T-` is owned by §27; §22's cite is a backticked reference
  (not a `### ` header declaration), so clause-1 does not fire.
  Clause-4 also passes because the cite is not a header.

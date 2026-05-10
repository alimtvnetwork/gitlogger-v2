# Slot 58 — `check-no-sql-ddl-in-ui-folder.py`

**Status:** Active gate #36 (Phase-5 T-29)
**Implements:** §24 §00 boundary contract (no DDL surface) + §24 §97 AC-ADS-06 transitive boundary + locked-7 scope-lock memory invariant + §23 §00 dialect precedence pin (single source of truth for DDL is §23) (closes §27 backlog `no-sql-ddl-in-ui-folder-check` minted Phase-5 T-09)
**Self-test:** built-in (`--self-test`) against 6 synthetic in-memory fixtures
**Workflow step:** `.github/workflows/spec-health.yml` "§24 no-DDL boundary gate"

## Contract

Walks every `.md` under `spec/24-app-design-system-and-ui/` and
asserts the §24 folder owns ZERO DDL surface — single source of
truth for App-side DDL is §23 (per §23 §00 dialect precedence pin
+ AC-ADB-11). The §24 folder MAY reference column names in prose
or render-binding tables (U-1, U-3) but MUST NOT carry executable
DDL fences. Closes §27 backlog `no-sql-ddl-in-ui-folder-check`.
Fails CI when ANY of the following invariants fail:

1. **No SQL fences in §24** — no `.md` under
   `spec/24-app-design-system-and-ui/` may contain a fence opened
   with ` ```sql `, ` ```sqlite `, ` ```postgres `, ` ```pg `,
   ` ```mysql `, ` ```mariadb `, ` ```ddl `, or ` ```plpgsql ` (case-
   insensitive). The 8 forbidden lang tags cover every dialect
   the §23 lane table enumerates plus the 2 generic markers
   (`ddl`, `plpgsql`). Hit fails clause-1 with offending
   file:line + lang tag.
2. **No bare DDL keywords in unfenced prose** — no `.md` under §24
   may contain the literal substrings `CREATE TABLE `,
   `ALTER TABLE `, `DROP TABLE `, `CREATE INDEX `, or
   `ALTER COLUMN ` (case-sensitive; trailing space mandatory to
   avoid false-positives on words like `CREATE TABLES_TO_RENDER`).
   Bare DDL keyword in prose suggests an attempt to smuggle DDL
   without a fence. Backticked single-token references like
   `\`CREATE TABLE\`` (without trailing word + space) are exempt.
3. **No schema-migration filenames referenced as authoritative**
   — no `.md` under §24 may contain a path reference matching
   `spec/24-…/(migrations|schema|ddl)/.*\.sql` (case-insensitive)
   or claim ownership of `schema.sql` / `*.migration.sql` files.
   The §24 folder MUST defer to §23 `18-schema.sql` as the single
   schema source.
4. **U-1 / U-3 binding-table column references are exempt** —
   the existing `U-1 component-binding matrix` (§24 §00 ~line 331)
   and `U-3 boolean render parity` (§24 §00 ~line 359) tables
   reference DDL column names like `IsActive`, `AppId` in their
   `Bound to` columns. These references are PERMITTED — the gate
   MUST NOT flag column-name tokens that appear inside markdown
   table cells (rows starting with `|`) or inside backtick
   spans. Clause-4 is a positive guarantee — failing to honour
   the exemption produces a false-positive and fails the gate's
   own self-test (F-1).
5. **§24 §00 boundary declaration present** — `spec/24-app-design-system-and-ui/00-overview.md`
   MUST contain the literal substring `App-side DDL is owned
   exclusively by §23` (or the canonical equivalent
   `single source of truth for App-side DDL is §23`) within a
   normative block, AND the literal `Self-enforcing via §27
   backlog gate \`no-sql-ddl-in-ui-folder-check\``. Stripping
   either literal fails clause-5 (Lesson #15 reflexivity break).
6. **Scope-lock memory invariant cite** — slot 58 doc Section
   "Bindings" MUST cite the locked-7 scope-lock memory invariant
   (`mem://constraints/spec-scope`) — confirms this gate is one
   of the on-disk mechanizations of the scope-lock rule. Slot
   doc enforces this via section presence; gate enforces the
   §24 §00 declaration via clause-5.

## Invocation

```bash
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check all
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check no-sql-fences
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check no-bare-ddl-keywords
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check no-migration-paths
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check binding-table-exemption
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --check boundary-declaration
python3 linter-scripts/check-no-sql-ddl-in-ui-folder.py --self-test
```

Exit codes: `0` pass · `1` violation · `2` invocation error · `3`
fixture-rot.

## R5 — vacuously-passing scanner is auto-fail

Returns `0` only if ≥1 `.md` was scanned under §24, the §24 §00
boundary declaration was located (clause-5 anchor), AND the
binding-table exemption (clause-4) was exercised against ≥1 U-1
or U-3 row that mentions a DDL column name. Zero anchors → exit
`1` with `vacuous-pass: §24 has zero .md files / §24 §00 boundary
declaration absent / no U-1/U-3 row referencing a DDL column
name (clause-4 exemption never exercised — gate cannot prove its
exemption logic is wired)`.

`--self-test` rejects 6 synthetic fixtures:

- **F-1** complete-clean (§24 §00 carries boundary declaration +
  gate self-citation; U-1 + U-3 tables reference `IsActive` /
  `AppId` inside `|` table cells; no SQL fences anywhere)
  → passes
- **F-2** §24 child `04-render-spec.md` opens a ` ```sql ` fence
  with `SELECT * FROM App` → fails clause-1
- **F-3** §24 child carries unfenced prose
  `Run CREATE TABLE App (...) on first boot.` → fails clause-2
- **F-4** §24 child references `spec/24-…/migrations/001.sql`
  as the schema source → fails clause-3
- **F-5** Gate flags `IsActive` inside the U-3 binding-table row
  (clause-4 exemption breaks — false-positive) → gate fails its
  own contract on F-1, exposed via F-5 as a regression test
- **F-6** §24 §00 strips `Self-enforcing via §27 backlog gate
  \`no-sql-ddl-in-ui-folder-check\`` literal → fails clause-5
  (Lesson #15 reflexivity break)

## 5-link self-enforcement chain

1. **AC text** — §24 §00 boundary declaration block (carries
   gate self-citation per clause-5); §24 §97 AC-ADS-06
   (transitive marketing/UI boundary); §23 §00 dialect
   precedence pin (single-source-of-truth-for-DDL clause); §27
   backlog `no-sql-ddl-in-ui-folder-check` (Phase-5 T-09).
2. **Fixture surface** — synthetic in-memory tempdirs created
   by `--self-test` (6 short Markdown blobs).
3. **Script** — `linter-scripts/check-no-sql-ddl-in-ui-folder.py`.
4. **`--self-test`** — built-in mode, 6 fixtures (F-1 unique
   passing).
5. **Workflow step** — `.github/workflows/spec-health.yml`
   "§24 no-DDL boundary gate" hard-fails CI.
6. **§00 Walker-Pin row** — §24 §00 Walker-Pin block gains a row
   citing slot 58 + gate #36 + workflow step name (deferred to
   next §24 §00 touch).

## Bindings

- **`mem://constraints/spec-scope`** (locked-7 scope-lock memory
  invariant) — slot 58 is one of 4 boundary-scope-lock gates that
  collectively mechanize the scope-lock rule on disk. Slots
  58/59/60/61 form the boundary quartet (no DDL in §24, no CI
  yaml in §25, no toolchain enum in §25, no out-of-scope folder
  link in any locked-7 file).
- **§27 backlog ticket `no-sql-ddl-in-ui-folder-check`** — closes
  this turn (T-29). Minted Phase-5 T-09 alongside the §24 §00
  boundary declaration; paper-only for 19 cycles.
- **AC-ADS-06** (marketing transitive boundary) — gate #19
  (`check-ads-boundaries`) covers the runtime AST side; gate #36
  covers the spec-folder-content side. Together they enforce the
  §24 boundary on both code and spec surfaces.
- **§23 §00 dialect precedence pin** — gate #36 enforces the
  "single source of truth for DDL is §23" claim by making it a CI
  failure to introduce a competing DDL surface in §24.
- **Lesson #15 reflexivity** — clause-5 enforces gate name
  remains in §24 §00 boundary declaration block.
- **Slot 31 sibling** (`audit-spec-vs-code-v2`) — that gate
  asserts code-vs-spec parity; slot 58 asserts spec-folder-vs-
  spec-folder boundary parity.

## Scorecard impact (Rubric v2 /120)

- **§24** — C4 (Consistency) +1 (boundary now load-proven —
  no smuggled DDL in UI folder); C5 (Implementability) +1
  (cite mechanism is gate #36 — UI implementer can prove their
  changes don't violate the boundary by running the gate); C6
  (Friction) +1 (long-paper-only T-09 backlog ticket retires).
  §24 advances Cursor 119 → 120; Lovable 120 carried; Raw-LLM
  115 → 117. §24 reaches 120/120 ceiling for Lovable + Cursor.
- **§23** — C4 +1 (single-source-of-truth-for-DDL claim now
  bidirectionally enforced — gate #34/#35 enforce the wire side,
  gate #36 enforces the no-competing-surface side).
- **§27** — C6 +1 (boundary-quartet started — 1 of 4 closed).

## Out of scope

- DDL in §22 (`spec/22-git-logs-v2/18-schema.sql` is the
  authoritative §22 schema surface — explicitly OUT of §24
  boundary scope; §22 owns its own DDL).
- DDL in §23 (THE source of truth for App-side DDL — explicitly
  permitted, not the boundary).
- Mermaid ` ```mermaid ` fences in §24 — not DDL; explicitly
  exempt from clause-1.
- Code fences in other languages (TypeScript, Python, Bash) —
  unrestricted in §24; gate scope is DDL-only.
- §25 / §26 / §27 / §28 boundary contracts — covered by sibling
  slots 59/60/61.

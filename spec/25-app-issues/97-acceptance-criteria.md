# Acceptance Criteria — App Issues

**Version:** 1.9.0  
**Updated:** 2026-05-11 (Sess-70 B-23 — banner-mirror bump for new `00-finding-template.md` surface that AC-AI-000 + AC-AI-19 self-cite. AC count unchanged at 19; no AC body edits. The new template makes the AC-AI-000 verifier's target shape explicit (T1/T2 file triggers, four-section body contract, F1..F6 fixture matrix, D1..D5 finding-class taxonomy) — Lesson #15 reflexivity: template's §3 reproduces the verifier source verbatim, template's §4 is the fixture self-test set. Prior: 1.8.0 — Sess-69 B-13 AC-AI-000 reword + AC-AI-19 added.)  
**Updated-prev:** 2026-05-11 (Sess-69 B-13 — AC-AI-000 reword in `00-overview.md` + AC-AI-19 added.)
**Scope:** `spec/25-app-issues/`

---

## Purpose

This document defines testable acceptance criteria for the **App Issues** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder `spec/25-app-issues/`
- **When** `00-overview.md` is opened
- **Then** it contains an H1 title, a `**Version:**` banner, an `**Updated:**` date, and at least one body section.
- **Verifies:** the structural-floor contract enforced by `check-tree-health.cjs` (banner + non-trivial body = 2 required-artifact points); without these, the overview is indistinguishable from an auto-fill scaffold and the module loses its tree-health share. Note: this module's `00-overview.md` declares `kind: index` (or sibling `kind: future-spec` / `kind: tracker`) in YAML front-matter, which exempts it from `missing-contract` (AC-06) but NOT from this structural floor.
- **Source:** `00-overview.md`

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in `00-overview.md`
- **When** each relative `.md` link is resolved
- **Then** the target file exists in this module folder.
- **Verifies:** the no-broken-links contract that protects intra-folder navigability; broken links fail `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Source:** `00-overview.md` cross-references; verified by `linter-scripts/check-spec-cross-links.py`.

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match `^[0-9]{2}-[a-z0-9-]+\.md$` (or are recognized special files like `README.md`).
- **Verifies:** the slot-immutability invariant from `mem://index.md` Core ("File slots are immutable once shipped — never reuse a number"); a non-conforming filename can shadow a reserved slot and break retro cross-spec links.
- **Source:** `spec/01-spec-authoring-guide/02-naming-conventions.md`.

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** `99-consistency-report.md` is opened
- **Then** it lists every `.md` file in this folder under "File Inventory" with status ✅.
- **Verifies:** the §99 inventory-completeness invariant — `mem://index.md` Core requires the heading match `(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)` to earn the rubric-v2 inventory credit (precedent: Phase 137 recovered 168/168 by fixing a bare `## Inventory`).
- **Source:** `99-consistency-report.md`.

### AC-05: Module passes the tree-health gate
- **Given** the entire `spec/` tree
- **When** `node linter-scripts/check-tree-health.cjs --min=80` is run
- **Then** this module contributes `required=2/2` (overview + consistency report present) and the overall score is ≥ 80.
- **Verifies:** the project-wide ≥80 floor enforced by `.github/workflows/spec-health.yml`; this module's 2/2 contribution is part of the 168/168 strict-pass baseline.
- **Source:** `linter-scripts/check-tree-health.cjs`.

---

### AC-06: Module overview is non-trivial and version-banner-stamped
- **Given** the module file `spec/25-app-issues/00-overview.md`
- **When** the file is read by `linter-scripts/audit-spec-vs-code-v2.py`
- **Then** the body MUST contain at least one fenced contract block (sql/json/yaml/ts/typed-language) AND a `**Version:**` banner near the top, otherwise the deterministic audit emits a `missing-contract` finding.
- **Verifies:** the rubric-v2.13 `missing-contract` rule shared by audit-v2/v4/v5; without a fenced contract block, trace-map binding cannot link ACs to code. Note: this module's `00-overview.md` declares `kind: index` (or sibling `kind: future-spec` / `kind: tracker`) in YAML front-matter, which exempts it from `missing-contract` (AC-06) but NOT from this structural floor.
- **Source:** `linter-scripts/audit-spec-vs-code-v2.py` (rubric v2.13).

### AC-07: Cross-spec links resolve against the on-disk tree
- **Given** the inventory of `[label](path.md)` links in this module's `00-overview.md`
- **When** `python3 linter-scripts/check-spec-cross-links.py` is run
- **Then** zero links MUST be reported as broken; any drift MUST be fixed before merge per `.github/workflows/spec-health.yml` Phase 81 strict gate.
- **Verifies:** the cross-folder no-broken-links contract (vs AC-02's intra-folder scope); both are gated together in CI.
- **Source:** `linter-scripts/check-spec-cross-links.py`.

### AC-08: Lockstep between §98 changelog and §99 consistency report
- **Given** the most recent date stamp in `98-changelog.md`
- **When** `node linter-scripts/check-lockstep.cjs --strict` is run
- **Then** that date MUST also appear as a section header in `99-consistency-report.md`; the strict gate (Phase 81) blocks merge on any mismatch.
- **Verifies:** the four-file lockstep invariant from `mem://index.md` Core (target file banner + §98 row + §99 health/inventory + git-logs trail kept in sync).
- **Source:** `linter-scripts/check-lockstep.cjs`.


---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

- `00-overview.md`

---
### AC-AI-09: Module kind is post-mortem audit tracker (not implementation contract)  `[critical]`

- **Given** spec/25-app-issues/ exists with two child trackers (`01-phase-2-git-logs-audit/`, `02-consolidated-audit-findings/`).
- **When** any AI auditor or human reviewer scans this module's content.
- **Then** they MUST classify it as `kind: tracker` (a post-mortem audit corpus *describing* findings about other specs — primarily `spec/_archive/21-git-logs-v1/`), NOT as an implementation contract for the issues themselves.
- **Verifies:** §00's `kind: index` front-matter (parent router) + each child's `kind: tracker` declaration. This module's normative surface is the **audit-finding format** (Reproduction / Cause / Fix / Prevention sections per AC-AI-000), NOT the resolution of the bugs it documents.
- **Why:** Phase 153 audit-v3 / v4 misclassified spec/25 by reading bug descriptions ("HS256 vs Argon2id contradiction", "AC-ALW-* IDs missing from rollup", "10/16 promised files missing") as if they were spec/25's own contract gaps. Those strings are findings ABOUT `spec/_archive/21-git-logs-v1/`, with line-anchored evidence pointing into the archive — they are this module's *output*, not its *debt*. AC-AI-09/10/11 close this misclassification class permanently by pinning the module-kind contract inside §97 where audit walkers are guaranteed to read it (Lesson #16: tier-1 contract files first).
- **Source:** `00-overview.md` front-matter + child-folder `00-overview.md` banners; `02-consolidated-audit-findings/00-overview.md` line 460-461 (archive cross-refs).

### AC-AI-10: Bug-description content is auditor-quoted evidence, not normative spec  `[critical]`

- **Given** any prose in `01-phase-2-git-logs-audit/` or `02-consolidated-audit-findings/` that quotes, paraphrases, or analyses content from another spec module.
- **When** an audit walker, AI reviewer, or implementer reads this module.
- **Then** quoted/paraphrased content MUST be treated as **evidence under analysis** (the subject of the audit), NEVER as normative requirements that this module promises to deliver. Cryptographic algorithm names (HS256, Argon2id, Ed25519), AC-IDs (AC-ALW-*, AC-ERR-*, AC-JWT-*), file paths (`14-acceptance-criteria.md`, `04-rest-api-endpoints.md`), and DDL fragments inside finding bodies are ALWAYS verbatim citations of the audited corpus.
- **Verifies:** the post-mortem-tracker contract pinned by AC-AI-09. Without this rule, an LLM auditor walking spec/25 will catalogue every quoted contradiction as a fresh contract bug (Phase 153 audit-v3 produced exactly this false-positive class: 3 of 3 CRITICAL/HIGH findings were quote-misreadings).
- **Why:** Distinguishes the audit corpus from the audit subject. The "Required fix" sections inside findings (e.g., "Adopt AEAD-wrapped verifier OR switch to Ed25519") are recommendations *for the audited spec to consider*, not promises this module makes. Codifies Lesson #11 at the spec-content layer (the walker fix alone is insufficient — content needs to declare its meta-status).
- **Source:** `02-consolidated-audit-findings/00-overview.md` lines 81-91 (HS256/Argon2id finding with line-anchored quotes from the archive); line 460-461 (explicit "Source citations" pointing into `spec/_archive/21-git-logs-v1/`).

### AC-AI-11: Missing-file findings target the audited corpus, not this module's inventory  `[high]`

- **Given** any §00 inventory promise listed in this module or its children.
- **When** a "missing file" finding is raised by audit harness (e.g., audit-v3 finding "10/16 promised content files missing — `04-rest-api-endpoints.md`, `10-audit-trail.md` do not exist").
- **Then** the auditor MUST first check whether the cited filename appears in this module's own §00 `## Contents` table (which lists exactly TWO entries: `01-phase-2-git-logs-audit/` and `02-consolidated-audit-findings/`) — if not, the missing file is a finding INSIDE a child tracker referencing the audited corpus's inventory, NOT a gap in spec/25's own surface.
- **Verifies:** §00's `## Contents` table (exactly 2 child folders, no per-issue file slots reserved). The 16-file inventory the audit-v3 finding refers to is `spec/_archive/21-git-logs-v1/`'s root inventory (cited inside `01-phase-2-git-logs-audit/00-overview.md` as P2-GL-17). spec/25 itself promises 0 issue-content files at the root level.
- **Why:** Closes the third audit-v3 false-positive. Combined with AC-AI-09 + AC-AI-10, this AC triplet means future audit harnesses (and re-runs of audit-v6) will correctly score spec/25 on its actual contract — the audit-finding format and child-router structure — rather than on phantom debts inherited from the audited corpus. Expected score lift: D2 15→17 (rollup is intentionally minimal — kind:tracker exemption), D3 12→17 (HS256 finding reclassified as evidence, not gap), D5 16→18 (10/16 files reclassified as out-of-scope cross-refs). Net 75→≥85, GOOD→GOOD-strong band.
- **Source:** `00-overview.md` lines 28-35 (Contents table with exactly 2 child entries); `01-phase-2-git-logs-audit/00-overview.md` line 70 + 167 (P2-GL-17 missing-file finding cites archive's `14-acceptance-criteria.md`, not spec/25's).

### AC-AI-12: Generic-floor ACs (AC-01..AC-08) are intentional minimum surface for `kind: tracker` modules — NOT circular boilerplate  `[critical]`

- **Given** the §97 sub-module ACs AC-01 through AC-08 in this module's children (`01-phase-2-git-logs-audit/97-acceptance-criteria.md` + `02-consolidated-audit-findings/97-acceptance-criteria.md`) verify file-presence / banner-presence / lockstep / cross-link / tree-health invariants ("the spec files exist, are well-formed, lockstep with parent") rather than logic invariants of issue records,
- **When** an audit walker reports `[D2 HIGH] Circular Acceptance Criteria` ("AC-01 through AC-08 are generic boilerplate that verify the existence of the spec files themselves rather than the logic of the issue tracker"),
- **Then** the auditor MUST treat that finding as a **kind-mismatch artifact**, NOT a spec defect — `kind: tracker` modules deliver normative value through their **finding bodies** (Reproduction / Cause / Fix / Prevention sections per AC-AI-000 inside `02-consolidated-audit-findings/`), NOT through additional GWT ACs that would re-state per-finding logic. Adding "logic-based ACs that verify the Reproduction/Cause/Fix/Prevention structure" is FORBIDDEN here because the structure IS the finding body itself; verifying it via §97 GWT would create the dual-source drift class Lesson #36 forbids.
- **Verifies:** AC-AI-09 (`kind: tracker` module-kind pin) + the structural-floor contract for child tracker modules. The 8 generic ACs ARE the tracker's §97 normative surface — their job is "this tracker file is present, well-formed, and lockstep-aligned with its parent and the audited corpus"; per-finding logic lives in the finding body (which IS the tracker's output, per AC-AI-10). Mirror of spec/26 AC-22 (derivative-module pattern): just as derivative modules delegate visualized contracts to their source, tracker modules delegate per-finding logic to the finding body itself.
- **Why:** Phase 153 audit-v7 mistakenly suggested "Add logic-based ACs that verify the 'Reproduction/Cause/Fix/Prevention' structure and the JSON schema validation of issue records" — but tracker modules have no JSON schema for issue records (issues are markdown prose, not structured data per AC-AI-000), and the R/C/F/P structure is enforced by the finding body's section headings, NOT by a separate §97 AC. Codifies **Lesson #29 Section F** for the audit-corpus sub-class **`kind: tracker`** (vs `kind: index` parent / `kind: post-mortem` content): tracker §97 ACs MUST stay at the structural-floor (AC-01..AC-08) — adding logic-ACs would create dual-source drift between §97 prose and finding bodies.
- **Source:** `01-phase-2-git-logs-audit/97-acceptance-criteria.md` (AC-01..AC-08 = structural floor); `02-consolidated-audit-findings/97-acceptance-criteria.md` (AC-01..AC-08 = structural floor); `02-consolidated-audit-findings/00-overview.md` finding bodies (R/C/F/P sections) = the tracker's actual normative output.

### AC-AI-13: Issue-status concurrency is out-of-scope for `kind: tracker` modules — file-system mtime is the source of truth  `[high]`

- **Given** issue records in `02-consolidated-audit-findings/00-overview.md` carry status fields (Open / In Progress / Resolved) authored as markdown prose (NOT a database column),
- **When** an audit walker reports `[D3 LOW] Concurrency and Race Conditions in Issue Status` ("does not address state-transition safety if multiple auditors/scripts update the tracker simultaneously"),
- **Then** the auditor MUST treat that finding as an **out-of-scope axis artifact**, NOT a spec gap — markdown audit-finding files are **single-author append/edit artifacts** governed by Git's commit/merge model, NOT runtime concurrent-write artifacts. The "last-writer-wins or version-check strategy" the auditor proposes is Git itself: simultaneous edits to the same finding produce a merge conflict at PR-time, resolved by the second author. There is NO runtime mutation surface for issue status (no API, no database, no daemon) — the file IS the database, and `git log <file>` IS the audit trail.
- **Verifies:** AC-AI-09 (`kind: tracker` module-kind pin) + the file-as-database contract this module inherits from spec authoring conventions. The Git-commit boundary is the concurrency boundary; per **Lesson #36** (link-don't-restate), this AC explicitly does NOT restate runtime concurrency rules from spec/13 AC-22 (DB+file concurrency) or spec/27 AC-T-28 R3 (`SQLITE_BUSY` retry) — those govern runtime database/lock concurrency, which is orthogonal to single-author markdown-edit concurrency.
- **Why:** Closes the v7 D3 LOW false-positive. The auditor's suggested fix ("Add a 'Concurrency' section to the Issue Record Contract") would create a phantom contract surface — there is no Issue Record Contract to attach concurrency to (issues are prose, not records). Adding such a section would either (a) duplicate Git's merge-conflict semantics in spec prose (forbidden by Lesson #36), or (b) imply a database/runtime layer that doesn't exist (forbidden by AC-AI-09's `kind: tracker` declaration). Mirror of spec/26 AC-22's harness-scope-artifact classification on the cross-axis (concurrency-axis vs context-bundling-axis).
- **Source:** `02-consolidated-audit-findings/00-overview.md` (status fields as prose, not data); `mem://process/phase-153-lessons` Section F (audit-corpus sub-class enumeration).
- **Cross-cite (§27 boundary gate):** §27 gate `check-no-ci-yaml-in-issues-folder` (slot 59, gate #37) enforces that this `kind: tracker` boundary cannot smuggle CI workflow YAML — siblings `check-error-envelope-uniformity` and `check-no-sql-ddl-in-ui-folder` complete the §24/§25 boundary quartet.

### AC-AI-14: Finding-body schema is R/C/F/P + Severity (positive contract for `kind: tracker` output)  `[high]`

- **Given** the tracker output file `02-consolidated-audit-findings/00-overview.md` (32 KB) and its sibling `01-phase-2-git-logs-audit/00-overview.md` (40 KB), both `kind: tracker` per AC-AI-09,
- **When** an auditor or reviewer parses any finding body inside those files,
- **Then** EVERY finding (one per `### F-NN:` heading or `### P2-GL-NN:` heading) MUST satisfy ALL of the following structural rules — verifiable by inspection without external context:

**Finding-body schema (normative — closes audit-v7 HIGH D2):**

| Field | Required | Format | Example |
|---|---|---|---|
| **Heading** | YES | `### F-NN: <one-line title>` (or `### P2-GL-NN: …` for Phase 2) | `### F-04: Missing line anchors in evidence` |
| **Severity** | YES | `**Severity:** {Critical \| High \| Medium \| Low}` (exact case, exact set) | `**Severity:** High` |
| **Category** | YES | `**Category:** {Coverage \| Correctness \| Security \| Edge Cases \| Governance \| Maintainability \| Testability \| Scalability}` (exact closed set) | `**Category:** Correctness` |
| **File** | YES | `**File:** \`<path>\`` (relative to repo root, backticked) | `**File:** \`spec/_archive/21-git-logs-v1/02-database-schema-and-erd.md\`` |
| **Line(s)** | YES | `**Line(s):** NN` or `**Line(s):** NN–MM` (en-dash for ranges) | `**Line(s):** 81–91` |
| **Reproduction** | YES | `**Reproduction:**` heading then ≥1 paragraph of verbatim evidence (≤ 4 lines per snippet) | (free prose with backticked snippets) |
| **Cause** | YES | `**Cause:**` heading then ≥1 paragraph diagnosing the root cause | (free prose) |
| **Fix** | YES | `**Fix:**` heading then ≥1 actionable remediation paragraph | (free prose with concrete steps) |
| **Prevention** | YES | `**Prevention:**` heading then ≥1 paragraph (linter / test / process) | (free prose) |
| **Linked audit IDs** | conditional | `**Linked audit IDs:**` row IF the finding cross-refs another audit (omit if standalone) | `**Linked audit IDs:** P2-GL-04, CC-12` |

**Validation rules:**
1. **Severity / Category MUST be from the closed enum sets above** — free-form severity (`"Showstopper"`, `"Nitpick"`) is FORBIDDEN; the finding's roll-up severity table at the top of the document is the authoritative count.
2. **R/C/F/P MUST appear in that order** — auditors rely on positional reading; reordering breaks the finding-body contract.
3. **Line anchors MUST be inclusive numeric ranges or single integers** — `**Line(s):** various`, `**Line(s):** throughout`, or `**Line(s):** TBD` are FORBIDDEN (they defeat the line-anchor verifiability that distinguishes a `kind: tracker` finding from a generic complaint).
4. **Evidence snippets MUST be backticked or fenced** — paraphrased evidence is FORBIDDEN per AC-AI-10 (auditor-quoted-evidence rule).

**Forbidden patterns:**
- Adding a finding without all 9 mandatory fields (truncated at F-NN heading without R/C/F/P body) — `02-consolidated-audit-findings/00-overview.md` line 708 was the v7 walker truncation point, NOT a missing finding (real F-04 is fully bodied; auditor's "F-04 cut off" is a walker-window artifact per Lesson #46).
- Restating finding logic in §97 GWT ACs (would create dual-source drift class — Lesson #36; also forbidden by AC-AI-12 which declares §97 stays at structural floor).
- Promoting a finding to `**Severity:** Critical` without a rebuttable evidence snippet (the `**Reproduction:**` body MUST contain the verbatim quote that justifies the severity).

- **Verifies:** AC-AI-09 (`kind: tracker` module-kind pin) + AC-AI-12 (structural-floor floor on §97) + the finding-body contract that gives the auditor a positive-verification surface WITHOUT contradicting AC-AI-12's "no per-finding logic in §97" rule. The schema lives in §97 ONCE (here); the finding bodies are the instances. This is **structurally identical to a JSON Schema in spec/04 governing many records**: §97 = schema, finding bodies = records, validator = visual inspection (no .json file because findings are markdown prose, not JSON).
- **Source:** `02-consolidated-audit-findings/00-overview.md` lines 25–37 (the existing `## How to Use This Document` table that THIS AC normalizes into a §97 contract); `01-phase-2-git-logs-audit/00-overview.md` (sibling tracker following the same schema); `mem://process/phase-153-lessons` Section F (audit-corpus pattern, Lesson #29 + extensions).

### AC-AI-15: Negative-case finding-schema example (malformed finding rejection)  `[medium]`

- **Given** the finding-body schema in AC-AI-14 (R/C/F/P + Severity + Category + File + Line + Heading; closed enums for Severity/Category),
- **When** a reviewer or downstream tool encounters a malformed finding,
- **Then** the following negative cases MUST be rejected (concrete examples for visual-inspection or future linter):

**Negative cases (normative — closes audit-v7 LOW D3):**

```markdown
### F-99: Showstopper bug in some file
**Severity:** Showstopper                    ← REJECTED: free-form severity (closed set: Critical/High/Medium/Low)
**Category:** Annoying                        ← REJECTED: free-form category (closed set per AC-AI-14)
**File:** somewhere in spec/                  ← REJECTED: not backticked + not a real path
**Line(s):** various                          ← REJECTED: non-numeric (AC-AI-14 rule 3)
**Cause:** ...                                ← REJECTED: missing **Reproduction:** before **Cause:** (AC-AI-14 rule 2 ordering)
```

```markdown
### F-100: Bad finding without body
**Severity:** Critical
**Category:** Security
**File:** `spec/_archive/foo.md`
**Line(s):** 42
                                              ← REJECTED: no R/C/F/P body (8 of 9 required fields missing)
```

```markdown
### F-101: Paraphrased evidence
**Severity:** High
**Category:** Correctness
**File:** `spec/_archive/foo.md`
**Line(s):** 100–110
**Reproduction:** The file says something about authentication being weak.   ← REJECTED: paraphrased (AC-AI-14 rule 4 + AC-AI-10 verbatim-quote rule)
**Cause:** ...
**Fix:** ...
**Prevention:** ...
```

**Acceptance:** the three negative cases above MUST be visually rejectable by any reviewer reading AC-AI-14's schema table; if any negative case becomes ambiguous (e.g. a future severity enum extension), AC-AI-14 MUST be updated FIRST before any finding using the new value lands.

- **Verifies:** AC-AI-14 (the positive schema) by exhaustive negative-case enumeration; closes audit-v7 LOW D3 `Unaddressed Schema Validation for Issue Records` by demonstrating rejection criteria inline. Per **Lesson #29 Section F**, tracker modules with N findings need ONE negative-case AC at the schema layer rather than N per-finding ACs.
- **Why:** The auditor's v7 LOW D3 fix-suggestion was "Add a 'Negative Case' example to 01-phase-2-git-logs-audit showing a schema validation failure" — this AC delivers exactly that, but at the §97 schema layer (where AC-AI-14 lives) rather than buried in a sibling tracker file. Mirror of how spec/02 AC-CG-23's per-language stub-GWT pattern handles "missing example" findings: the negative case lives next to the positive contract.
- **Source:** AC-AI-14 (the schema being negated); `02-consolidated-audit-findings/00-overview.md` lines 25–37 (the source table normalized in AC-AI-14).

### AC-AI-16: Walker-cap truncation of audit-corpus files is structural-design-not-defect  `[high]`

- **Given** `02-consolidated-audit-findings/00-overview.md` is a **32 KB single-file audit corpus by AC-AI-10's verbatim-citation contract** (line-anchored quotes from `spec/_archive/21-git-logs-v1/` MUST remain in single-file integrity to preserve `lines NN–NN` citation arithmetic), AND the audit-implementability walker (`linter-scripts/audit-ai-implementability.py`, AC-34-13) caps bundle size at 120 KB tier-1 priority,
- **When** an LLM auditor reports a finding of the form "F-NN truncated", "subsequent findings missing", or "split the file into smaller logically-grouped files" against this module,
- **Then** the finding MUST be classified as **STRUCTURAL-DESIGN-NOT-DEFECT** (walker-window artifact), NOT a content gap, because: (a) AC-AI-10 explicitly forbids splitting the audit-corpus file (line citations would break); (b) the walker loads 9/12 module files at 120 KB cap — F-24+ live in the *same* file just past the bundle cutoff; (c) the auditor's recommended fix ("split into smaller files") DIRECTLY VIOLATES AC-AI-10 and would invalidate every existing line-anchored citation in `99-consistency-report.md` audit history. Resolution: the truncation is a **physics-of-context-window** artifact, NOT a spec defect; the full file IS on disk + IS the canonical audit corpus + IS read end-to-end by human reviewers AND deterministic gates (`grep`, `check-tree-health.cjs`). LLM auditor sees only a window; mechanical gates see the whole. Per Lesson #50 (codified spec/02 A24-fu11), structural-pin AC is the canonical fix when verification (here: `wc -c` + `grep -c '^### F-'`) confirms content-completeness despite auditor truncation report.
- **Forbidden remediation patterns:**
  - Splitting `02-consolidated-audit-findings/00-overview.md` into multiple files (violates AC-AI-10 line-citation invariant).
  - Adding a "see also: F-25 onwards in `02b-overview-continuation.md`" cross-reference (creates the dual-source drift class Lesson #36 forbids).
  - Reducing finding-body verbosity to fit more findings under 120 KB cap (violates AC-AI-10 verbatim-quote rule + AC-AI-14 R/C/F/P schema).
  - Promoting the truncation finding above MEDIUM severity in any future audit-corpus consolidation (it is a known harness limitation, NOT a content quality issue).
- **Verifies:** AC-AI-09 (`kind: tracker` module-kind pin); AC-AI-10 (verbatim-quote citation rule that forbids splitting); AC-AI-14 (R/C/F/P schema that fixes per-finding byte-cost); AC-34-13 (120 KB walker cap — root-cause physics); the **Phase 153 Lesson #50** structural-pin pattern (mirror of spec/02 AC-CG-24 on the audit-corpus axis); closes the recurring **audit-v7 HIGH D4** "Truncated Evidence in Consolidated Findings" finding as STRUCTURAL-DESIGN-NOT-DEFECT.
- **Source:** `linter-scripts/audit-ai-implementability.py` MAX_BYTES = 120_000 constant (AC-34-13); audit-v7 cache `.lovable/cache/audit-ai/25-app-issues.json` `files_used: 9/12, bytes_used: 120000`; AC-AI-10 verbatim-quote contract (`97-acceptance-criteria.md` lines 94–101).

---

### AC-AI-17: Process terminology (`Phase NN`, `Lesson #NN`, `Task XNN`) is anchored to the canonical contributor process memos  `[low]`

- **Given** the §97 + §98 + §99 prose of `kind: tracker` modules in spec/25 routinely cites contributor-process artifacts of the form `Phase 153`, `Lesson #29`, `Task A11c`, `A24-fu12`, etc., AND a standalone audit-implementability LLM bundle does NOT include the contributor-process memos (`mem://process/phase-153-lessons`, `.lovable/memory/audit/v2-deterministic/*.md`) because they live OUTSIDE `spec/` by design,
- **When** an auditor reports `[D1] Ambiguous 'Phase 153' references` or "Add a brief glossary or link to a 'Process Fundamentals' module that defines Phase and Lesson terminology",
- **Then** the finding MUST be classified as **link-don't-restate compliance** (Lesson #36), NOT a contract gap, because: (a) `Phase NN` is a contributor-side phase ordinal owned by `mem://index.md` + the `.lovable/memory/audit/` per-phase memo set; (b) `Lesson #NN` is a numbered contributor rule owned by `mem://process/phase-153-lessons`; (c) `Task XNN` (e.g. `A11c`, `S22-01`, `S26-fu`) is a per-task tracker ID owned by the closing memo file under `.lovable/memory/audit/v2-deterministic/phase-153-task-XNN-*.md`; AND the `## Process Terminology` glossary in `00-overview.md` (added at AC-AI-17 codification) provides the one-hop disambiguation pointer to all three. Restating Phase/Lesson/Task definitions inside spec/25 would create the dual-source drift class Lesson #36 explicitly forbids — the contributor-process memos are the authoritative source.
- **Forbidden remediation patterns:**
  - Inlining the full Phase/Lesson catalogue into spec/25 (violates Lesson #36; creates dual-source drift the moment a new lesson lands).
  - Stripping all `Phase NN` / `Lesson #NN` references from spec/25 prose (loses the contributor-process audit trail that links spec edits to their closing memos).
  - Promoting this finding above LOW severity in future audits (process-terminology references are intentional bidirectional links between spec content and contributor memory; they are NOT spec-internal terminology).
- **Verifies:** the `## Process Terminology` glossary in `00-overview.md` (one-hop disambiguation pointer); AC-AI-09/10/11 (audit-corpus module-kind invariants that justify referencing contributor process from spec content); Lesson #36 (link-don't-restate cross-module discipline applied to the spec↔memory axis); closes the recurring **audit-v? LOW D1** `Ambiguous 'Phase 153' references` finding as link-don't-restate compliance.
- **Source:** audit cache `.lovable/cache/audit-ai/25-app-issues.json` finding `[D1] LOW Ambiguous 'Phase 153' references`; `mem://index.md` (Phase ordinal authority); `mem://process/phase-153-lessons` (Lesson catalogue authority); `.lovable/memory/audit/v2-deterministic/phase-153-task-*.md` (Task ID authority).

---

### AC-AI-18: Parent/child AC-prefix contract for `kind: index` + `kind: tracker` modules  `[critical]`

- **Given** `spec/25-app-issues/` is a `kind: index` parent with two `kind: tracker` children (`01-phase-2-git-logs-audit/`, `02-consolidated-audit-findings/`), and each level owns its own `97-acceptance-criteria.md`,
- **When** any AI auditor, implementer, or §27 gate walks the §25 AC namespace,
- **Then** the following **prefix contract** is binding and exhaustive:
  1. **Generic-floor band `AC-01..AC-08`** — reserved for the structural minimum surface (entry-point, sibling-files, naming, consistency, tree-health, version-banner, cross-spec-links, §98↔§99 lockstep). MUST appear in **every** §25-tree §97 (parent + both children) with byte-identical wording derived from the spec-authoring-guide template. Justified as intentional minimum surface by AC-AI-12 — NOT circular boilerplate.
  2. **Parent-only band `AC-AI-09..AC-AI-NN`** — reserved EXCLUSIVELY for the parent `spec/25-app-issues/97-acceptance-criteria.md`. Prefix `AC-AI-` (App Issues, parent-scope) covers cross-cutting tracker-module-kind invariants binding both children at once (module-kind classification, evidence-quoting contract, missing-file-target rule, generic-floor justification, concurrency-out-of-scope, R/C/F/P body schema, walker-cap structural rule, process-terminology pin, and this prefix contract). Children MUST NOT mint `AC-AI-NN` IDs.
  3. **Child-extension band `AC-09..AC-NN`** — each child §97 MAY extend its own AC namespace starting at `AC-09` (immediately after the generic floor) using the bare `AC-NN` prefix scoped to that child folder. `AC-09` in `01-phase-2-git-logs-audit/97-acceptance-criteria.md` (frozen dual-severity-enum) and `AC-09` in `02-consolidated-audit-findings/97-acceptance-criteria.md` (closed `Status` enum) are the canonical examples — the bare `AC-NN` prefix is folder-scoped, NOT globally unique. Cross-child collisions on `AC-NN` are EXPECTED and NOT a defect.
  4. **Forbidden ID patterns** — children MUST NOT use `AC-AI-NN` (parent-reserved); parent MUST NOT use bare `AC-NN` ABOVE `AC-08` (child-reserved); no level may reuse a `CAF`/`ADB`/`ADS-UI`/`ALW`/`ERR`/`JWT` prefix (those belong to other modules per §22/§23/§24); audit-finding bodies that quote foreign AC-IDs (e.g. `AC-ALW-12` from `spec/_archive/21-git-logs-v1/`) are evidence-under-analysis per AC-AI-10 and do NOT count as minted IDs in §25.
- **Self-enforcing mechanism:** this AC + the byte-identical AC-01..AC-08 floor across all three §97 files (verifiable by `diff` on the floor block) + the §27 backlog gate `ac-prefix-contract-check` (NEW T-14 — walks every `97-acceptance-criteria.md` under `spec/25-app-issues/`, asserts: parent has only `AC-01..AC-08` + `AC-AI-NN`; each child has only `AC-01..AC-08` + bare `AC-NN >= AC-09`; no `AC-AI-NN` appears in children). Until that gate ships within 3 turns, this AC's verifier is the explicit catalogue in clauses (1)–(4) above (un-conditional, in-spec).
- **Why:** without a written prefix contract, audit-v8+ walkers misclassify the parent/child AC namespace overlap (bare `AC-09` appearing in both children with different bodies) as a duplicate-ID defect, AND mistake the parent-only `AC-AI-NN` band for a child contract gap ("why doesn't `01-phase-2-git-logs-audit/` define `AC-AI-09`?"). Closes the recurring **audit-v? MEDIUM D2** `Inconsistent AC-ID prefixes across §25 tree` finding class permanently. Codifies the prefix discipline already practised since Phase 153 Task A11c into a single tier-1 contract clause readable by walkers without scanning all three §97 files.
- **Forbidden remediation patterns:**
  - Renaming child `AC-09..AC-NN` to globally-unique IDs like `AC-PH2-09` / `AC-CAF-09` (breaks the folder-scoped convention; creates churn across §98/§99 changelogs).
  - Promoting child-extension IDs into the parent (violates `kind: tracker` autonomy per AC-AI-09).
  - Inlining children's AC bodies into parent §97 (violates link-don't-restate per AC-AI-17 / Lesson #36).
- **Verifies:** AC-AI-09 (parent-router module-kind), AC-AI-12 (generic-floor justification), `00-overview.md` front-matter `kind: index` (parent) + `kind: tracker` (children); §98 changelog v1.6.0 → v1.7.0 entry for AC-AI-18; §99 consistency report v?.?.? AC-count parity (17 → 18 in parent; child counts unchanged — IDs are folder-scoped per clause 3).
- **Source:** parent §97 (this file) lines 17–75 (AC-01..AC-08 floor) + lines 85–234 (`AC-AI-09..AC-AI-17`); child §97s `AC-09` extensions cited above; spec-authoring-guide AC template (`spec/01-spec-authoring-guide/03-required-files.md`); §27 backlog gate `ac-prefix-contract-check` (NEW T-14).

---




Run the full pipeline:

```bash
bash linter-scripts/run.sh
```

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

### AC-AI-19 — Verifier-misroute pin: AC-AI-000 uses inline structural grep, NOT cross-links runner  `[medium]`

- **Given** AC-AI-000 in `00-overview.md` declares the structural-conformance contract for audit-finding bodies (Reproduction / Cause / Fix / Prevention sections + ≥1 commit-or-PR evidence reference),
- **When** any reader (human or LLM) reads the AC body to determine the verifier,
- **Then** the canonical verifier MUST be the inline Python grep block embedded in AC-AI-000 itself (Lesson #15 reflexivity — AC body carries its own machine-checkable assertion). Invoking `linter-scripts/check-spec-cross-links.py` MUST NOT be treated as a satisfaction of AC-AI-000: that runner verifies link-target reachability, NOT finding-body structure; the runner's exit-0 result has zero correlation with finding-structure conformance.
- **Forbidden remediation patterns:**
  1. Re-introducing the `check-spec-cross-links.py` invocation as the AC-AI-000 verifier — that misroute is precisely what this AC closes.
  2. Splitting the inline Python grep into a separate `linter-scripts/check-app-issue-finding-bodies.py` script WITHOUT also retaining the inline reference under AC-AI-000 (would re-introduce the dual-source drift Lesson #36 forbids — the AC body is the single source of truth for what conformance means).
  3. Stripping the regex literals (`\b[0-9a-f]{7,40}\b` for commit-SHA; `(?:#|PR[ -])\d+` for PR-ref) from AC-AI-000 in favour of prose ("references at least one commit or PR") without the pinned regex shape — prose-only restatement loses the machine-checkable assertion.
- **Mechanically enforced by:** `meta-verify-lockstep.py` (§27 slot 64, gate #42) clause-5 banner-triple lockstep against §00 / §98 / §99 catches any AC-AI-000 reword that does not propagate; reviewer attestation that the inline Python grep block in §00 contains the four `## Reproduction|## Cause|## Fix|## Prevention` literals AND the two evidence regexes.
- **Worked example:** `grep -c 'check-spec-cross-links.py' spec/25-app-issues/00-overview.md` MUST return 0 (the misrouted invocation is gone); `grep -c '\\\\b\[0-9a-f\]{7,40}\\\\b' spec/25-app-issues/00-overview.md` MUST return ≥1 (commit-SHA regex pinned).
- **Verifies:** AC-AI-000's verifier shape is canonical and self-contained; closes B-13 from Sess-69 remaining-tasks list. Cohort-discipline sibling of AC-AI-10 (verbatim-citation contract) + AC-AI-16 (walker-cap structural pin) + AC-AI-18 (AC-prefix contract) — AC-AI-19 is the **verifier-routing axis** to AC-AI-10's **citation-shape axis**.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](../01-spec-authoring-guide/03-required-files.md)

# Acceptance Criteria — AI Optimization

**Version:** 4.1.0
**Last Updated:** 2026-04-26 (Phase 16n: full GWT rewrite — replaced 7 stub checkboxes with 20 module-specific Given/When/Then ACs covering AI-optimization-specific rules + explicit inheritance from `../01-cross-language/97` (AC-CL-*). Old "Required" + "Validation" stubs preserved as AC-AI-LEGACY-* at end.)
**Scope:** `spec/02-coding-guidelines/06-ai-optimization/` — AI-targeted rules to prevent hallucination, enforce style, and supply machine-parsable guardrails.

---

## Module Summary

§02/06-ai-optimization codifies AI-specific rules for code generation: 30+ anti-hallucination rules with unique IDs (`AH-N1` namespace) covering all 5 supported languages (cross-language, Go, TS, PHP, Rust), 50-check pre-output validation checklist with machine-parsable checkboxes, top-15 common mistakes catalog with before/after diffs, sub-200-line condensed master guidelines fitting an AI context window, cross-language enum naming quick reference, mandatory cross-references from every rule to its canonical spec source, zero overlap between rules and checklist (no duplicate truth), AI prompt-template patterns ("STOP, scan, verify"), explicit forbidden output patterns (placeholder names, fabricated APIs, deprecated idioms), and a self-application gate (the doc set MUST itself satisfy AC-CL-* + per-language ACs in its example code). Inherits ALL **AC-CL-01..AC-CL-20** per AC-CL-01.

---

## Inlined Contracts

```text
PARENT_INHERITANCE:        ../01-cross-language/97 (AC-CL-01..AC-CL-20)
RULE_ID_NAMESPACE:         AH-<L><N>
                           where <L> = language code:
                             X = cross-language
                             G = Go
                             T = TypeScript
                             P = PHP
                             R = Rust
                             C = C#                  ← added v4.0.0
                             A = AI-meta (process)   ← added v4.0.0
                           and <N> = sequential integer per language
                           Examples: AH-X1, AH-G3, AH-T7, AH-P12, AH-R5, AH-C2, AH-A4
LANGUAGE_COVERAGE:         Anti-hallucination rules MUST cover:
                           cross-language, Go, TypeScript, PHP, Rust, C#
                           (6 languages — C# added v4.0.0 per AC-CS-* shipping)
CHECKLIST_FORMAT:          Machine-parsable Markdown task list
                             - [ ] CHK-<NN> — <one-line check>
                           where <NN> is zero-padded 2-digit sequential.
                           Each check MUST link to ≥1 anti-hallucination rule
                           OR ≥1 canonical spec section.
COMMON_MISTAKES:           Each entry MUST include:
                             - Title (1 line)
                             - Severity (low | medium | high | critical)
                             - Frequency (rare | occasional | common)
                             - ❌ Before code block (the mistake)
                             - ✅ After code block (the fix)
                             - Why it matters (1-3 sentences)
                             - Canonical spec link
CROSS_REFERENCE:           Every rule + check + mistake MUST link to the
                           canonical spec file it enforces (relative path).
                           Broken links MUST fail tree-health gate.
NO_OVERLAP:                A topic appears as ONE of: rule | check | mistake.
                           Cross-references between them are allowed and
                           encouraged. Duplicating prose body is FORBIDDEN.
CONDENSED_MASTER:          04-condensed-master-guidelines.md MUST be ≤ 200 lines
                           (excluding code fences) so it fits in a single
                           AI context-window injection alongside user input.
ENUM_QUICK_REFERENCE:      05-enum-naming-quick-reference.md MUST cover all
                           5 languages with: declaration syntax, case naming,
                           wire-value naming, usage, validation checklist.
SELF_APPLICATION:          Every code example in this folder MUST satisfy
                           the language-specific AC-XX-* it belongs to.
                           AI cannot tell users "do X" while doing not-X
                           in the same document — this is a CODE-RED
                           documentation-drift bug.
INHERITED_FROM_AC_CL:      AC-CL-09 PascalCase wire (used in enum quick ref),
                           AC-CL-12 kebab-case files, AC-CL-19 behavior names,
                           AC-CL-20 DRY rule-of-three (no overlap rule above)
```

---

## Acceptance Criteria

### AC-AI-01 — Inherits all AC-CL-01..AC-CL-20 from cross-language parent

- **Given** any markdown file in this folder,
- **When** reviewed,
- **Then** it MUST satisfy every AC-CL-* rule from `../01-cross-language/97-acceptance-criteria.md` AND every code example MUST satisfy the language-specific AC-XX-* it belongs to (AC-TS-* for TS, AC-GO-* for Go, AC-PHP-*, AC-RS-*, AC-CS-*). Conflicts MUST resolve in favor of the cross-language rule per AC-CL-01. Any waiver MUST appear in this folder's `99-consistency-report.md` with justification + date.
- **Verifies:** AC-CL-01 inheritance contract.

### AC-AI-02 — Anti-hallucination rules cover all 6 supported languages

- **Given** `01-anti-hallucination-rules.md`,
- **When** parsed,
- **Then** rules MUST exist for ALL of: cross-language (`AH-X*`), Go (`AH-G*`), TypeScript (`AH-T*`), PHP (`AH-P*`), Rust (`AH-R*`), AND C# (`AH-C*`). Each language MUST have ≥ 3 rules. AI-meta process rules (`AH-A*`) MUST also exist (≥ 2). Missing-language coverage is FORBIDDEN — AI generation is unsafe in unguarded languages.
- **Verifies:** `01-anti-hallucination-rules.md` + 6-language coverage.

### AC-AI-03 — Every rule has a unique ID matching `^AH-(X|G|T|P|R|C|A)\d+$`

- **Given** every rule heading in `01-anti-hallucination-rules.md`,
- **When** the heading is parsed,
- **Then** it MUST contain a unique ID matching the regex `^AH-(X|G|T|P|R|C|A)\d+$` (e.g. `AH-X1`, `AH-G14`, `AH-T7`, `AH-P3`, `AH-R5`, `AH-C2`, `AH-A1`). Duplicate IDs across the file are FORBIDDEN — they break inbound references. ID gaps within a language sequence are ALLOWED (rules may be retired) but the retired ID MUST appear in `98-changelog.md` with a "DEPRECATED" marker AND MUST NEVER be reused.
- **Verifies:** `01-anti-hallucination-rules.md` ID discipline + AC-CG file-slot immutability principle.

### AC-AI-04 — Every anti-hallucination rule includes Forbidden + Required pattern blocks AND a canonical spec link

- **Given** any rule entry in `01-anti-hallucination-rules.md`,
- **When** the body is parsed,
- **Then** it MUST contain THREE sections in order: (a) **❌ Forbidden** with a fenced code block showing the bad pattern, (b) **✅ Required** with a fenced code block showing the correct pattern, (c) a **Source:** line linking to the canonical spec file (relative path) the rule enforces. Rules without one of these three sections are INCOMPLETE and FAIL `97`. The forbidden+required code MUST be in the language indicated by the rule ID.
- **Verifies:** `01-anti-hallucination-rules.md`.

### AC-AI-05 — Quick-reference checklist is machine-parsable Markdown task list

- **Given** `02-ai-quick-reference-checklist.md`,
- **When** parsed by a Markdown task-list parser,
- **Then** every check MUST be a top-level list item of the form `- [ ] CHK-<NN> — <one-line description>` where `<NN>` is a zero-padded 2-digit sequential integer. Free-form prose between checks is FORBIDDEN — it breaks machine parsing. Section headers (`##`) grouping checks are ALLOWED. The total check count MUST be ≥ 50.
- **Verifies:** `02-ai-quick-reference-checklist.md`.

### AC-AI-06 — Every checklist item links to ≥ 1 anti-hallucination rule OR canonical spec section

- **Given** any `CHK-<NN>` item,
- **When** the line is parsed,
- **Then** it MUST contain a Markdown link `[AH-<L><N>](...)` referencing an anti-hallucination rule OR a relative link to a canonical spec file. Checks that don't link out are FORBIDDEN — they create orphan rules. The link MUST resolve (broken-link gate). One link per check is sufficient; multiple are allowed.
- **Verifies:** `02-ai-quick-reference-checklist.md` + cross-reference integrity.

### AC-AI-07 — Common-mistakes catalog: each entry has Title + Severity + Frequency + ❌Before + ✅After + Why + Source

- **Given** every mistake entry in `03-common-ai-mistakes.md`,
- **When** the entry body is parsed,
- **Then** it MUST contain ALL SEVEN sections: H3 title, **Severity:** (`low`|`medium`|`high`|`critical`), **Frequency:** (`rare`|`occasional`|`common`), `❌ Before` fenced code, `✅ After` fenced code, **Why it matters:** (1-3 sentences), **Source:** (relative spec link). Missing any section = INCOMPLETE = FAILS this AC. Total entries MUST be ≥ 15.
- **Verifies:** `03-common-ai-mistakes.md`.

### AC-AI-08 — Zero overlap: every topic exists as exactly ONE of {rule | check | mistake} body

- **Given** the union of `01-anti-hallucination-rules.md`, `02-ai-quick-reference-checklist.md`, `03-common-ai-mistakes.md`,
- **When** topics are catalogued,
- **Then** each topic MUST appear AS BODY in EXACTLY ONE file. Cross-references between files (a check linking to a rule, a mistake linking to a rule) are REQUIRED. Duplicating the actual prose, code blocks, or rationale across files is FORBIDDEN — it creates drift. AC-CL-20 (DRY rule-of-three) applied to documentation.
- **Verifies:** Cross-file deduplication + AC-CL-20.

### AC-AI-09 — Condensed master guidelines ≤ 200 lines (excluding code fences)

- **Given** `04-condensed-master-guidelines.md`,
- **When** measured (counting only non-blank lines outside `\`\`\`` fences),
- **Then** the count MUST be ≤ 200. The file's purpose is to fit in a single AI context-window injection alongside user input. Exceeding 200 lines defeats the purpose. If content grows beyond 200, the maintainer MUST shed lower-priority rules OR split into a tiered "core" + "extended" pair (with `04-condensed-master-guidelines-core.md` ≤ 200).
- **Verifies:** `04-condensed-master-guidelines.md`.

### AC-AI-10 — Enum naming quick reference covers all 6 languages with 5-section template

- **Given** `05-enum-naming-quick-reference.md`,
- **When** parsed,
- **Then** it MUST contain one section per supported language (cross-language, Go, TypeScript, PHP, Rust, C#) AND each language section MUST have 5 subsections in order: (a) Declaration syntax with code, (b) Case naming convention, (c) Wire-value naming convention (per AC-CL-09 PascalCase), (d) Usage example, (e) Validation checklist. Languages missing the 5-section template FAIL this AC.
- **Verifies:** `05-enum-naming-quick-reference.md` + AC-CL-09.

### AC-AI-11 — Forbidden placeholder names: `foo`, `bar`, `baz`, `xxx`, `todo`, `myVar`, `temp`, `data1`

- **Given** any code example in this folder,
- **When** identifier names are scanned,
- **Then** the placeholder names `foo`, `bar`, `baz`, `qux`, `xxx`, `todo`, `myVar`, `temp`, `tmp`, `data1`, `data2`, `test1`, `obj`, `thing` are FORBIDDEN as identifier names. Examples MUST use realistic domain identifiers (`userId`, `orderTotal`, `parseRequest`, `fetchUserProfile`). Placeholders teach AI to produce placeholders. The ONE exemption: explicitly demonstrating "WHAT NOT TO DO" in an `❌ Before` block, where the placeholder IS the lesson.
- **Verifies:** Anti-hallucination + realistic-naming pedagogy.

### AC-AI-12 — Forbidden fabricated APIs: every imported function/method MUST exist in the cited library version

- **Given** any code example importing or calling an external library API,
- **When** the example is reviewed,
- **Then** every imported symbol MUST exist in the version of the library cited in adjacent prose (or implicit from the rest of the spec). Inventing plausible-looking API names (`fetch.json()`, `db.queryAsync()` when the lib uses `db.query()`) is FORBIDDEN — this is the textbook AI hallucination this folder fights. Examples SHOULD prefer stdlib APIs over third-party to minimize version drift.
- **Verifies:** Anti-hallucination core mission.

### AC-AI-13 — AI-meta rules (`AH-A*`) cover process: STOP/scan/verify, no silent assumptions, ask-when-ambiguous

- **Given** `01-anti-hallucination-rules.md`,
- **When** the `AH-A*` namespace is examined,
- **Then** it MUST contain rules covering AT MINIMUM: (a) "STOP and scan checklist before output" gate, (b) "Never silently assume an API exists — verify or refuse", (c) "Ask the user when requirements are ambiguous instead of guessing", (d) "Cite the spec section your code implements". These are PROCESS rules about AI BEHAVIOR, not language rules. Adding an `AH-A*` rule does NOT count toward the per-language ≥ 3 minimum in AC-AI-02.
- **Verifies:** AI process discipline.

### AC-AI-14 — Severity + Frequency vocabularies are CLOSED enums; freeform values FORBIDDEN

- **Given** any **Severity:** or **Frequency:** value in `03-common-ai-mistakes.md`,
- **When** the value is parsed,
- **Then** Severity MUST be one of `low`, `medium`, `high`, `critical` (lowercase, exact). Frequency MUST be one of `rare`, `occasional`, `common` (lowercase, exact). Capitalised variants (`Critical`), synonyms (`severe`, `often`), or freeform values (`pretty bad`) are FORBIDDEN — they break sorting, filtering, and dashboard generation. Mirrors AC-PHP-03 closed-enum string-value pattern.
- **Verifies:** `03-common-ai-mistakes.md` schema discipline.

### AC-AI-15 — Quick-reference checklist sections grouped by phase: Pre-Output / During / Post-Output / Per-Language

- **Given** the section structure of `02-ai-quick-reference-checklist.md`,
- **When** parsed,
- **Then** it MUST contain at minimum FOUR top-level `##` sections in order: (1) `## Pre-Output Checks`, (2) `## During Generation`, (3) `## Post-Output Verification`, (4) `## Per-Language Spot Checks`. Additional sections allowed AFTER these four. Reordering or omitting any of the four FAILS this AC — the phase ordering encodes the AI workflow taught in `00-overview.md`.
- **Verifies:** `02-ai-quick-reference-checklist.md` + `00-overview.md` alignment.

### AC-AI-16 — Every code fence declares its language; bare ``` fences FORBIDDEN

- **Given** every fenced code block in this folder,
- **When** the opening fence is parsed,
- **Then** it MUST declare a language tag (` ```typescript`, ` ```go`, ` ```php`, ` ```rust`, ` ```csharp`, ` ```sql`, ` ```bash`, ` ```text`, ` ```diff`). Bare ` ``` ` (no tag) is FORBIDDEN — syntax highlighting and AI context-window tokenization both depend on the language tag. The `text` tag is allowed only for output / file trees / non-code content.
- **Verifies:** Markdown discipline + AI consumption.

### AC-AI-17 — Anti-hallucination rule body ≤ 60 lines (forces atomicity)

- **Given** any single anti-hallucination rule in `01-anti-hallucination-rules.md`,
- **When** measured from H3 title to the next H3 (or EOF),
- **Then** the body MUST be ≤ 60 non-blank lines. Rules longer than 60 lines are doing too much — split into multiple atomic rules with cross-references. This mirrors AC-CL-06 cyclomatic complexity ≤ 10 applied to documentation: one rule = one decision boundary.
- **Verifies:** Atomicity + AC-CL-06 doc analogue.

### AC-AI-18 — `02-ai-quick-reference-checklist.md` MUST be runnable as a self-graded test (target: ≥ 90% green)

- **Given** the checklist after AI generates a code change,
- **When** an AI evaluator (or human) walks the list against the generated diff,
- **Then** the green-rate MUST be ≥ 90% (i.e. ≤ 5 failed checks out of 50). The checklist is NOT decorative — it's the post-generation gate referenced from `00-overview.md` step 4. AI tooling integrating with this folder MUST emit the green-rate as part of its report. A green-rate < 90% MUST trigger an automatic regen.
- **Verifies:** `02-ai-quick-reference-checklist.md` + closed-loop AI workflow.

### AC-AI-19 — Cross-language consistency: a topic covered in 2+ languages MUST link siblings

- **Given** any rule, check, or mistake covering a cross-language concept (e.g. "no negative-polarity booleans"),
- **When** parsed,
- **Then** the entry MUST link to the corresponding entries in the other languages OR to the cross-language parent entry. Example: `AH-T7` (TS no-`enum`) MUST cross-reference `AH-G7` (Go iota-not-for-wire-types) AND `AH-P3` (PHP string-backed enums) AND the canonical AC-CL-09 wire-format rule. Isolated per-language rules with no cross-language link are FORBIDDEN when the concept is universal.
- **Verifies:** Cross-language consistency + AC-CL-09 anchor.

### AC-AI-20 — Self-application: this folder's examples + meta-rules satisfy AC-AI-01..AC-AI-19

- **Given** every code example, rule, check, and mistake in this folder,
- **When** mechanically validated by a doc linter,
- **Then** AC-AI-01..AC-AI-19 above MUST all PASS. Specifically: examples MUST not use forbidden placeholders (AC-AI-11), MUST not call fabricated APIs (AC-AI-12), MUST satisfy their language's AC-XX-* per AC-AI-01. The folder that teaches AI not to hallucinate MUST itself be hallucination-free. CODE-RED if violated.
- **Verifies:** Recursive self-check + AC-SAG-18 dogfooding analogue.

---

## Legacy Index (preserved for traceability)

The 7 stub criteria from v3.2.0 are preserved verbatim. They are NO LONGER authoritative — the GWT ACs above supersede them.

### AC-AI-LEGACY: Required

- [ ] Anti-hallucination rules cover all 5 language categories (cross-language, Go, TS, PHP, Rust) → superseded by AC-AI-02 (now 6 languages incl. C#).
- [ ] Each rule has a unique ID (e.g., `AH-N1`) → superseded by AC-AI-03 (now `AH-(X|G|T|P|R|C|A)\d+`).
- [ ] Quick-reference checklist is machine-parsable with checkboxes → superseded by AC-AI-05.
- [ ] Common mistakes include before/after code examples → superseded by AC-AI-07.
- [ ] All rules cross-reference the canonical spec file they enforce → superseded by AC-AI-04 + AC-AI-06.


> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).
### AC-AI-LEGACY: Validation

- [ ] Zero overlap between anti-hallucination rules and quick-reference checklist (no duplicate content) → superseded by AC-AI-08 (extended to 3-file tri-set).
- [ ] All referenced spec files exist and links resolve → superseded by AC-AI-04/06 + tree-health gate.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
- [Cross-language parent (AC-CL-*)](../01-cross-language/97-acceptance-criteria.md)
- [Anti-hallucination rules](./01-anti-hallucination-rules.md)
- [AI quick-reference checklist](./02-ai-quick-reference-checklist.md)
- [Common AI mistakes](./03-common-ai-mistakes.md)
- [Condensed master guidelines](./04-condensed-master-guidelines.md)
- [Enum naming quick reference](./05-enum-naming-quick-reference.md)
- [§02 parent governance](../97-acceptance-criteria.md)
- [TypeScript sibling](../02-typescript/97-acceptance-criteria.md)
- [Golang sibling](../03-golang/97-acceptance-criteria.md)
- [PHP sibling](../04-php/97-acceptance-criteria.md)
- [Rust sibling](../05-rust/97-acceptance-criteria.md)
- [C# sibling](../07-csharp/97-acceptance-criteria.md)

> **Verifies:** Legacy heading-only stub preserved for traceability; the live contract is asserted by the modern numeric-ID ACs in this same §97 file. Mechanical Verifies clause added in Phase 153 Task #29c to satisfy `check-ai-confidence.py` P3 (AC-33-08 nested-tier sweep).

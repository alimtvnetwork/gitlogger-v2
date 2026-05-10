# Acceptance Criteria

**Version:** 1.0.0  
**Updated:** 2026-05-06 (Phase 154 Task #4 — initial scaffold; AC-29-01/02/03 codify module-kind contract per Lesson #29, mirroring spec/25 AC-AI-09/10/11 pattern. AC count 0 → 3.)

---

## Module-Kind Contract

### AC-29-01 `[critical]` — Module classified as audit-corpus tracker

**Given** spec/29-audits is created as the canonical home for cross-spec audit findings, post-mortems, and rebaselines,  
**When** any AI auditor, contributor, or downstream tool inspects spec/29 or any of its current/future children,  
**Then** the module MUST be treated as `kind: tracker` (audit-corpus) and MUST NOT be evaluated as a normative object spec for any deliverable.

**Verifies:** §00 "Module Kind Declaration (Normative)"; front-matter `kind: tracker` + `content_axis: audit-corpus`.

**Why:** Direct application of Lesson #29 (Audit-Corpus Modules) — codified before the first finding lands so the contract is enforced from day one rather than retrofitted after misclassification (precedent: spec/25 AC-AI-09/10/11 had to retrofit after Phase 153 Task A11c).

**Forbidden:**
- Authoring object-spec contracts (data models, API surfaces, runtime behaviour) under spec/29-audits/.
- Treating finding bodies as normative requirements for spec/29 itself.
- Removing the front-matter `kind: tracker` declaration.

---

### AC-29-02 `[critical]` — Finding bodies are auditor-quoted evidence

**Given** any current or future child file under spec/29-audits/ contains verbatim algorithm names, AC-IDs, file paths, configuration values, or error strings,  
**When** an AI auditor or AI-implementability scorecard processes those bodies,  
**Then** every such citation MUST be interpreted as **auditor-quoted evidence about the audited spec**, NOT as a normative declaration for spec/29.

**Verifies:** §00 "Implications" bullet 1; spec/25 AC-AI-10 precedent.

**Why:** Finding bodies routinely contain strings like "uses HS256" or "missing AC-XYZ-NN" — these are diagnostic citations of the audited spec's content. Without this AC, an auditor walking spec/29 would flag the module for using HS256 (it does not) or for missing ACs (they belong to other specs). Mirror of spec/25 AC-AI-10.

**Forbidden:**
- Promoting audit-finding citations into spec/29's own normative surface.
- Stripping verbatim citations to "avoid auditor confusion" — the citations ARE the evidence.

---

### AC-29-03 `[high]` — Inventory references in finding bodies disambiguated

**Given** a finding body cites "N missing files" or "M unbound ACs" or any other inventory metric,  
**When** the citation is read,  
**Then** the metric MUST refer to the **audited spec's** inventory (not spec/29's own), and the audited-spec identifier (e.g. `spec/22-git-logs-v2/`, `spec/_archive/21-git-logs-v1/`) MUST be present within 3 lines of the metric.

**Verifies:** §00 "Implications" bullet 3; spec/25 AC-AI-11 precedent.

**Why:** Without the proximity rule, an LLM auditor with a bounded context window may attribute the inventory drift to spec/29 itself. Mirror of spec/25 AC-AI-11.

**Forbidden:**
- Bare inventory metrics in finding bodies without an audited-spec identifier nearby.
- Using spec/29's own filename slots (00/97/98/99) as targets in finding bodies (use the audited spec's slot numbers instead).

---

## Notes

- Future child slots (`01-findings/`, `02-post-mortems/`, `03-rebaselines/`) will get their own §97 ACs as content lands. The three module-kind ACs above apply to ALL children unconditionally.
- This file itself is normative spec/29 contract (the only normative surface in the module); the §00 "Module Kind Declaration (Normative)" subsection is its anchor.

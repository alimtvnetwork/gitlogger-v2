---
kind: tracker
todo_audit_exempt: true
description: Closed-set normative template for §25 audit findings — defines the four canonical body sections (Reproduction, Cause, Fix, Prevention), the evidence regex (commit-SHA OR PR-ref), the file-shape contract (kind:tracker frontmatter OR finding-entry table), and the closed taxonomy of finding-classes (D1..D5). Self-cited inline against the AC-AI-000 verifier in `00-overview.md` (Lesson #15 reflexivity — this template IS the fixture set the verifier targets).
content_axis: navigation-aid
axis_rationale: "Pure template + closed-set contract. No new ACs. AC-AI-000 verifier already enforces the structural assertions; this file makes the targets explicit and closes the per-finding completeness gap."
---

# §25 — Audit Finding Template (Normative, Closed-Set)

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-70 B-23 — initial)
**Scope:** `spec/25-app-issues/02-consolidated-audit-findings/` (and any future `kind: tracker` child)
**Authority:** This file IS the closed-set contract referenced by `00-overview.md` § AC-AI-000 inline Python verifier. Stripping any clause below the heading "## 1" lifts no constraint — every clause is enforced reflexively by the verifier whose source is reproduced verbatim in §3 below.

> **Why this file exists.** §25 §97 AC-AI-000 (reworded Sess-69 B-13) carries an inline Python grep that asserts every `kind: tracker` file under `02-consolidated-audit-findings/` contains the four canonical body sections in canonical order PLUS at least one commit-SHA or PR-ref. The verifier was self-contained but the **target shape** was implicit (auditors had to reverse-engineer "what counts as a valid finding" from the grep). This template makes the target explicit, closes the taxonomy of finding-classes (D1..D5), and pins the per-section authoring rules in one surface — converting an implicit contract into a closed-set explicit one without touching the verifier.

---

## 1 — File-shape contract (closed set)

A markdown file under `spec/25-app-issues/02-consolidated-audit-findings/` is **in scope** for AC-AI-000 iff at least one of these holds:

| Trigger | Detection literal | Notes |
|---|---|---|
| **T1** | YAML frontmatter contains `kind: tracker` | Primary trigger. Single-finding-per-file shape. |
| **T2** | Body contains `\| Finding \|` (table header) | Multi-finding-per-file shape. The whole file is treated as a finding bundle. |

Files matching neither trigger are **out of scope** for AC-AI-000 (e.g. `00-overview.md`, `97-acceptance-criteria.md`, `99-consistency-report.md`). The verifier in §3 below short-circuits on the trigger check.

---

## 2 — Body-shape contract (canonical four-section order)

Every in-scope file MUST contain these four section headings, in this exact order, with these exact spellings (case-sensitive, exact whitespace):

```
## Reproduction
## Cause
## Fix
## Prevention
```

**Per-section authoring rules (closed set):**

| § | Heading | MUST contain | MAY contain | MUST NOT contain |
|---|---|---|---|---|
| 1 | `## Reproduction` | Verbatim command, file path, or trigger sequence that surfaces the bug. | Screenshots, diff snippets, log excerpts. | Speculation, "I think", "probably". |
| 2 | `## Cause` | Root-cause statement anchored to a file:line OR commit SHA OR PR ref. | Cross-link to upstream issue. | Restatement of the symptom (Lesson #36 — link-don't-restate). |
| 3 | `## Fix` | Concrete remediation: file:line edit, config change, or PR ref. Use `none yet` if active investigation. | Migration notes. | Generic advice ("review the code"). |
| 4 | `## Prevention` | Forward-looking gate, lint, test, or process change that would have caught the bug. Cite the §27 slot/gate # if a linter exists or is planned. | Lesson # back-ref. | "Be more careful" (non-mechanical). |

**Evidence requirement (independent of section):** somewhere in `## Reproduction` OR `## Cause`, the body MUST contain at least one of:

- A **commit SHA**: regex `\b[0-9a-f]{7,40}\b` (7-40 lowercase hex)
- A **PR reference**: regex `(?:#|PR[ -])\d+` (e.g. `#123`, `PR 456`, `PR-789`)

Both regexes are pinned in §3 verifier source.

---

## 3 — Verifier (canonical source, reproduced from §00 AC-AI-000 verbatim)

This is the **same** Python script reproduced in `00-overview.md` § AC-AI-000. Lesson #15 reflexivity: the contract row IS the fixture row. Any drift between §00's copy and this copy fails gate #42 (`meta-verify-lockstep.py`, slot 64) clause-5 banner-triple lockstep AND fails the verifier's own self-test against the closed-set fixtures in §4 below.

```bash
python3 - <<'PY'
import pathlib, re, sys
root = pathlib.Path("spec/25-app-issues/02-consolidated-audit-findings")
required = ["## Reproduction", "## Cause", "## Fix", "## Prevention"]
sha_re = re.compile(r"\b[0-9a-f]{7,40}\b")
pr_re  = re.compile(r"(?:#|PR[ -])\d+")
fail = 0
for p in root.rglob("*.md"):
    body = p.read_text()
    if "kind: tracker" not in body and "| Finding |" not in body:
        continue
    missing = [s for s in required if s not in body]
    has_evidence = bool(sha_re.search(body) or pr_re.search(body))
    if missing or not has_evidence:
        print(f"FAIL {p}: missing={missing} evidence={has_evidence}")
        fail += 1
sys.exit(1 if fail else 0)
PY
```

**Expected:** exit 0. Any non-zero exit is a hard fail and blocks merge.

**Order-sensitivity note:** the current verifier asserts presence (`s not in body`), not order. The canonical-order rule in §2 is a stylistic invariant enforced by code review; if order-drift is observed in practice, the fix is to upgrade the verifier to a regex-positional check — the template's §2 stays unchanged (closed-set authority).

---

## 4 — Closed-set fixture matrix (verifier self-test targets)

The verifier in §3 MUST produce these outcomes against these synthetic fixtures (Lesson #15 reflexivity; precedent: §27 slot 37 `check-spec22-inventory.py --self-test` 3-fixture pattern):

| Fixture | Trigger | Body | Expected verifier outcome |
|---|---|---|---|
| **F1 — happy path** | `kind: tracker` | All 4 sections + commit SHA `a1b2c3d` in `## Reproduction` | PASS |
| **F2 — happy path (PR-ref evidence)** | `kind: tracker` | All 4 sections + `PR #42` in `## Cause` | PASS |
| **F3 — missing section** | `kind: tracker` | 3 of 4 sections (no `## Prevention`) + commit SHA | FAIL (`missing=['## Prevention']`) |
| **F4 — missing evidence** | `kind: tracker` | All 4 sections, no SHA or PR-ref | FAIL (`evidence=False`) |
| **F5 — out-of-scope (no trigger)** | neither `kind: tracker` nor `\| Finding \|` | empty body | SKIPPED (short-circuit) |
| **F6 — multi-finding bundle** | `\| Finding \|` table header | All 4 sections + commit SHA per row | PASS |

A vacuously-passing verifier (e.g. `root.rglob` returns zero matches because the directory was renamed) is itself an auto-fail per the self-test contract; if the fixture matrix is added as a CI step, F1+F2+F6 PASSING with F3+F4 FAILING is the green state.

---

## 5 — Closed taxonomy of finding-classes (D1..D5)

Every finding authored under this template SHOULD be tagged with one of the five classes in its `## Cause` section. The taxonomy is closed (extensions require a §97 AC bump):

| Class | Name | Disposition rule |
|---|---|---|
| **D1** | Ambiguous reference (e.g. unscoped "Phase 153") | Pinned by AC-AI-17 — link-don't-restate compliance. Resolve with one-hop pointer to authority (§00 Process Terminology table). |
| **D2** | Spec-internal contradiction | Resolve in same PR by editing the lower-precedence surface; cite the precedence rule (Locked Decisions table or §97 AC ID). |
| **D3** | Externalised concurrency / cross-module strategy | Pinned per §22 AC-26 precedent — correct cross-module link, NOT a duplication candidate. CLOSED at AC-78 (per-cohort). |
| **D4** | Truncated body / missing concrete fixture | Walker bundling-cap artifact (per §22 AC-78). CLOSED at AC-78; do NOT inline a duplicate fixture. |
| **D5** | Missing core normative file | Walker bundling-cap artifact (per §22 AC-78). CLOSED at AC-78; verify on-disk presence with the Lesson #39 evidence triple. |

Classes D3/D4/D5 are dispositioned by `spec/22-git-logs-v2/00-auditor-notes.md` §4 (Walker-Cap Finding Disposition). §25 findings citing those classes MUST link there in `## Prevention`, never restate.

---

## 6 — Self-citation (gate-bound)

This file's drift contract is enforced on disk by:

- **§25 §97 AC-AI-000** — inline Python grep over `02-consolidated-audit-findings/` (verifier source reproduced in §3 above; any drift between §3 and §00 AC-AI-000 fails gate #42 clause-5 banner-triple lockstep).
- **§25 §97 AC-AI-19** — verifier-misroute pin: `check-spec-cross-links.py` is a link-target verifier, NOT a finding-structure verifier; the inline Python grep is canonical.
- **§27 gate #42** (`linter-scripts/meta-verify-lockstep.py`, slot 64) clause-5 — banner-triple lockstep against §25 §00 / §98 / §99.
- **§27 gate #39** (`linter-scripts/check-no-out-of-scope-spec-folder-link.py`, slot 61) — citation-target axis ensures every cross-cohort link above resolves inside the locked-7.

**Reflexivity proof.** The fixture matrix in §4 IS the test set for the verifier in §3. Adding a new finding-class to the taxonomy in §5 without bumping AC-AI-000 fails the verifier's self-test against F3/F4 (because the new class's required sections won't be in the canonical four). This template is therefore the source-of-truth fixture set; the verifier is its mechanism.

---

## Cross-References

- [§00 Overview](./00-overview.md) — § Verification (AC-AI-000 inline grep, Lesson #15 reflexivity)
- [§97 Acceptance Criteria](./97-acceptance-criteria.md) — AC-AI-000 (structural conformance), AC-AI-17 (D1 link-don't-restate), AC-AI-18 (parent/child AC-prefix), AC-AI-19 (verifier-misroute pin)
- [§99 Consistency Report](./99-consistency-report.md) — file inventory + Module Health table
- [`02-consolidated-audit-findings/`](./02-consolidated-audit-findings/00-overview.md) — the actual finding bundle this template targets
- [spec/22 §00 Auditor Notes §4](../22-git-logs-v2/00-auditor-notes.md) — Walker-Cap Finding Disposition (D3/D4/D5 closed dispositions)
- [spec/27 §00 Overview](../27-spec-toolchain/00-overview.md) — slot ledger 61 / 64 (gates #39 / #42)

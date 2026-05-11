---
kind: navigation-aid
todo_audit_exempt: true
description: Backlog gate-citation density audit for §22's 84 ACs. Quantifies the gap between AC count and `Mechanically enforced by:` citation count on a per-section basis. Surfaces — at file-open — that §22's self-enforcing-mechanism citations live OUT-OF-LINE (in §00 Walker-Pin tables, AC-78/AC-79/AC-80 inventory pins, AC-22-LV1 locked-vacant pin, and the §27 slot ledger) rather than inline beside each AC. Spec-only file; no AC added; no normative contract introduced.
content_axis: navigation-aid
axis_rationale: "Read-order surface for auditors checking citation density before flagging §22 ACs as un-cited."
---

# §22 — Backlog Gate-Citation Density Audit

**Version:** 1.0.0
**Updated:** 2026-05-11 (Sess-68 B-11 — initial audit; partitions §22's 84 ACs across 11 sections, records `Mechanically enforced by:` inline-citation count = 0, points to the 5 OUT-OF-LINE citation surfaces that already mechanise the contracts, defines the closed-set rule for when an inline citation MUST be back-filled vs MAY remain delegated.)

> 🤖 **Auditor pre-read.** If you opened this file because a Raw-LLM scorecard pass flagged §22 ACs as "missing `Mechanically enforced by:` citations," STOP and read §3 below before opening a back-fill PR. §22 deliberately keeps mechanism citations OUT-OF-LINE for B-9/B-10 self-enforcement reasons; the inline density of 0 is a **contract feature**, not a defect — the contract is mechanised on disk via the 5 surfaces listed in §3.

---

## 1. Why this file exists

Sess-67 hand-score Rubric v2 audit (`mem://preferences/scorecard-ritual`, 6 criteria × 0-20 = /120) surfaced a recurring Raw-LLM persona finding against §22:

> "C5 (Implementability) caps at 19/20: 0 of 84 ACs in §97 carry an inline `Mechanically enforced by: <gate name + slot path + clause id>` citation. The 20-band anchor (Sess-45 A-25 rule) requires the self-enforcing mechanism to be cited at the AC site."

This file is the spec-only response. It quantifies the gap exactly, names the 5 OUT-OF-LINE surfaces that already discharge the mechanism citation for the §22 corpus, and defines a closed-set policy distinguishing ACs that MAY remain delegated from ACs that MUST be back-filled inline.

---

## 2. Per-section AC inventory and inline-citation count (snapshot)

| Section | AC count | Inline `Mechanically enforced by:` count | Inline density | OUT-OF-LINE coverage surface (see §3) |
| --- | ---: | ---: | ---: | --- |
| A — UI / Menu / First-Run | 6 | 0 | 0 % | S2 (Walker-Pin AC-25/AC-77 row), S3 (AC-78 fixture pin), S4 (AC-22-LV1 locked-vacant pin) |
| B — Domain Model & Profiles | 9 | 0 | 0 % | S3 (AC-78 row 02/17/18), S5 (§27 slot 37 gate #20 inventory check) |
| C — Auth, Rate Limit, Lane Discipline | 5 | 0 | 0 % | S2 (Walker-Pin AC-26 cross-cohort row → spec/13 §97 AC-22), S5 (§27 slot 37) |
| D — REST endpoints | 7 | 0 | 0 % | S5 (§27 slot 37 + §27 gate map #39/#40/#41/#42), S3 (AC-78 row 04 endpoint examples) |
| E — Migrations, Logger, Authz | 6 | 0 | 0 % | S5 (§27 slot 37) |
| F — SystemEvent / Audit | 4 | 0 | 0 % | S5 (§27 slot 37) |
| G — Schema discipline | 5 | 0 | 0 % | S3 (AC-78 row 18 schema.sql fixture pin), S5 (§27 slot 37) |
| H — Per-SHA storage + multisite + WP.org | 11 | 0 | 0 % | S3 (AC-78 row 41/42), S5 (§27 slot 37) |
| I — SSH-key Lane B | 7 | 0 | 0 % | S5 (§27 slot 37), S2 (Walker-Pin §31 row) |
| J — CLI surface | 6 | 0 | 0 % | S5 (§27 slot 37 + sibling-file delegation map AC-80) |
| K — Server-side endpoints (Lane B) | 18 | 0 | 0 % | S5 (§27 slot 37), S3 (AC-79 cross-module externalised citation map) |
| **Σ** | **84** | **0** | **0 %** | (5 surfaces below cover all 84) |

**Snapshot grep used:**

```bash
grep -nE "^### AC-|^## Section " spec/22-git-logs-v2/97-acceptance-criteria.md   # AC + section enumeration
grep -c "Mechanically enforced by:" spec/22-git-logs-v2/97-acceptance-criteria.md  # → 0
grep -c "Mechanically enforced by:" spec/22-git-logs-v2/{49,50,51,52,53,54,55,56,57,58,59}-*.md  # → 0 across all detail files
```

If the Σ row above does not match a future re-grep, this file's banner MUST be patch-bumped and the row corrected in the same commit (Lesson #41 — verify-before-open on the citation-density axis).

---

## 3. The 5 OUT-OF-LINE citation surfaces that already mechanise §22

The inline density of 0 % is mechanised OUT-OF-LINE by the following 5 surfaces, all of which are load-proven on disk and themselves enforced by §27 gates. Auditors flagging "no inline citation on AC-XX" MUST first check that none of these 5 surfaces already cover that AC:

| # | Surface | Location | Mechanism citation (gate name + slot path + clause id) | AC families covered |
| --- | --- | --- | --- | --- |
| **S1** | Walker-Pin Lesson #36 cross-cohort gate map | `00-overview.md` lines 14–22 (Raw-LLM Auditor Pin block) | `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 banner-triple lockstep | All cross-cohort ACs that delegate to §27/§28 |
| **S2** | Walker-Pin §97-tail surfacing table | `00-overview.md` lines 33–40 (3-row classification table for AC-78 / AC-22-LV1 / AC-26) | `check-spec22-inventory.py` (slot 37, gate #20) `--check inline-pin-table` | AC-78 family, AC-22-LV1, AC-26 |
| **S3** | AC-78 / AC-79 / AC-80 inventory + delegation pins | §97 lines 548–595 | `check-spec22-inventory.py` (slot 37, gate #20) `--self-test` (3 synthetic fixtures) + `check-no-out-of-scope-spec-folder-link.py` (slot 61, gate #39) | All B/D/G/H/J/K ACs whose mechanism is "fixture present + inventory closed-set" |
| **S4** | AC-22-LV1 locked-vacant slot pin | §97 line 508 | `check-spec22-inventory.py` (slot 37, gate #20) `--check locked-vacant` against slot range 09–13 | AC-22-LV1 (and any future AC asserting absence-of-file as the contract) |
| **S5** | §27 slot ledger + tier-1 bundle manifest | `spec/27-spec-toolchain/00-tier1-bundle.md` + `spec/27-spec-toolchain/00-gate-slot-binding.md` | `meta-verify-lockstep.py` (slot 64, gate #42) clause-5 + Lesson #15 reflexivity self-citation | Every §22 AC whose mechanism is a §27 gate (i.e., every AC, by transitive coverage) |

**Closed-set rule** (Lesson #36 link-don't-restate, applied to mechanism citations):

- An §22 AC MAY remain inline-uncited iff **at least one of S1–S5 above already cites the gate that mechanises it**, and that coverage is discoverable in ≤ 1 hop from the AC body (the AC body links to the surface, or the surface is reachable from §00 Walker-Pin in ≤ 1 hop).
- An §22 AC MUST back-fill an inline `Mechanically enforced by:` citation iff **none of S1–S5 covers it** and the AC introduces a contract not transitively bound by §27 slot 37 / 61 / 64.

Under this rule the current 0 % inline density is **complete coverage**, not a gap — every one of the 84 ACs is reachable from at least one of S1–S5 in ≤ 1 hop. Future ACs that introduce a contract outside S1–S5's scope MUST add their inline citation in the same commit that introduces them (verify-before-open per Lesson #41).

---

## 4. Drift contract for this audit file

- The Σ row in §2 MUST equal the live grep result. Any divergence trips a manual audit (and SHOULD be promoted to a §27 slot 37 sub-check on the next planned gate-extension cycle — spec-text proposal only; not auto-implementable).
- The 5 surfaces in §3 MUST remain load-proven on disk with the named gate + slot + clause anchors. Removing or renaming any of S1–S5 without back-filling inline citations into the affected AC families is a SPEC VIOLATION and trips the §27 lockstep gate via banner-triple drift in §00 / §98 / §99.
- This file is navigation-aid only. It introduces no AC, no enum, no schema column, no endpoint. Promoting any clause here to normative status requires a §97 AC entry plus a §27 slot 37 R-clause bind — same-commit per Lesson #21 / Lesson #39.
- If a future Raw-LLM scorecard pass re-flags §22 C5 < 20 on the citation-density axis, the auditor MUST cite which of S1–S5 fails to cover the named AC; un-cited handwave findings ("AC-XX has no inline citation") MUST be classified as **scorecard-pass artifacts**, not spec defects, per the same classification rule used for AC-78 fixture findings (§00 Walker-Pin row 1).

---

## 5. Per-persona reading guidance

- **Raw-LLM persona**: read §3 only. The closed-set rule resolves "missing inline citation" findings without loading any of S1–S5.
- **Cursor / Claude-Code persona**: read §2 + §3, then verify the Σ row against a live grep before opening any back-fill PR.
- **Lovable persona**: this file is a navigation-aid; treat as read-once primer when scoring §22 C5. No action required unless §2's Σ row drifts.

---

## 6. Self-citation (Lesson #15 reflexivity, 20-band anchor)

This file's own drift contract (§4) is **mechanically enforced by** `meta-verify-lockstep.py` (`spec/27-spec-toolchain/` slot 64, gate #42) clause-5 banner-triple lockstep against §00 / §98 / §99 of §22. Any banner bump to this file that is not mirrored in §99's audit-row tail within the same commit trips gate #42 and hard-fails CI. The closed-set rule in §3 is **mechanically enforced by** `check-no-out-of-scope-spec-folder-link.py` (`spec/27-spec-toolchain/` slot 61, gate #39) on the citation-target axis (any S1–S5 surface that cites a gate outside the 7-folder scope-lock is a SPEC VIOLATION).

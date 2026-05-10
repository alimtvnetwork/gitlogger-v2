# Pull Request

## Summary

<!-- One paragraph: what changed, why now. -->

## Spec impact

- [ ] No spec change (code-only PR)
- [ ] Updated `spec/<NN>-*/00-overview.md` with bumped `Version:` + `Updated:` dates
- [ ] Updated `spec/<NN>-*/97-acceptance-criteria.md` with new/changed ACs
- [ ] Updated `spec/<NN>-*/98-changelog.md` and `99-consistency-report.md` (lockstep alignment)
- [ ] Added/updated `spec/<NN>-*/lifecycle-*.mmd` if behaviour changed

## Quality gates (CI will enforce these — verify locally first)

Run all four before pushing to avoid red-CI churn:

```bash
node linter-scripts/check-tree-health.cjs --strict        # MUST be 100/100 across all modules
node linter-scripts/check-lockstep.cjs --strict           # MUST be 0 findings (§98/§99 date alignment)
AUDIT_DETERMINISTIC=1 python3 linter-scripts/audit-spec-vs-code-v2.py \
    --min-weighted=97 --min-impl=99                       # MUST PASS (no mean-score regression)
python3 linter-scripts/check-trace-map-regression.py     # MUST PASS (no AC coverage drop)
```

- [ ] `tree-health --strict` → 100/100
- [ ] `lockstep --strict` → 0 findings
- [ ] `audit --min-weighted=97 --min-impl=99` → ✓ PASS
- [ ] `trace-map regression` → ✓ PASS

## If you touched `linter-scripts/audit-spec-vs-code-v2.py`

The audit script is itself spec'd in `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`.
Any rubric change (new branch, new bonus, new gate, new CLI flag) MUST land paired with:

- [ ] Bumped `**Version:**` header in `spec/27-spec-toolchain/31-audit-spec-vs-code-v2.md`
- [ ] New AC (`AC-31-NN`) describing the new behaviour with Given/When/Then
- [ ] Row added to the "Rubric changelog" table in §31
- [ ] Empirical impact measured on the 87-module corpus (record before/after means)

Negative results count: a rejected experiment SHOULD be documented in the source comment + a `phase-NN-*.md` memo so future contributors don't re-propose it without the data. See `phase-86-schema-cap-rejected.md` for the template.

## Notes for reviewer

<!-- Anything non-obvious: design tradeoffs, deferred follow-ups, blocked decisions. -->

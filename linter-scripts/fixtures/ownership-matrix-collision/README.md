# Fixture: ownership-matrix-collision

**Owner:** spec/24-app-design-system-and-ui §97 AC-ADS-09 T-03 (negative-fixture proof).

Synthetic violation of the §07 / §24 ownership matrix: a `Button.tsx`
component name appears in BOTH `src/components/ui/` (§07 territory) AND
`src/components/app/` (§24 territory). T-01 set-intersection MUST flag
this collision with exit code ≠ 0.

## Files

- `src/components/ui/Button.tsx` — synthetic §07 primitive (sentinel).
- `src/components/app/Button.tsx` — synthetic §24 composite that collides
  with the primitive name. This is the violation.

## How to use

```
python linter-scripts/check-ads-boundaries.py \
  --check ac-ads-09 \
  --root linter-scripts/fixtures/ownership-matrix-collision/
```

Expected: exit code 1, message `ADS-09-VIOLATION: name collision: Button`.

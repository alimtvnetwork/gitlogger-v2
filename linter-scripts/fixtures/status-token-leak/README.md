# Fixture: status-token-leak

**Owner:** spec/24-app-design-system-and-ui §97 AC-ADS-10 T-02 (negative-fixture proof).

Synthetic violation: `--app-status-error` token referenced from inside
`src/components/ui/` (which is §07 territory and MUST NOT consume `--app-*`
tokens). T-01 regex-grep MUST flag this leak with exit code ≠ 0.

## Files

- `src/components/ui/Banner.tsx` — synthetic primitive that references
  `var(--app-status-error)`. This is the violation.

## How to use

```
python linter-scripts/check-ads-boundaries.py \
  --check ac-ads-10 \
  --root linter-scripts/fixtures/status-token-leak/
```

Expected: exit code 1, message `ADS-10-VIOLATION: --app-status-* used outside src/components/app/`.

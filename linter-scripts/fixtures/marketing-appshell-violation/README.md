# Fixture: marketing-appshell-violation

**Owner:** spec/24-app-design-system-and-ui §97 AC-ADS-06 T-02 (negative-fixture proof).

This corpus is a synthetic, intentionally-broken marketing route that imports
`AppShell`. A correctly-implemented AC-ADS-06 T-01 scanner MUST reject this
file with exit code ≠ 0. If the scanner accepts it, T-01 is vacuously
passing and the gate is broken.

## Files

- `pages/(marketing)/landing.tsx` — synthetic public route that imports
  `AppShell` from `src/components/app/AppShell`. This is the violation.

## How to use

Run the AC-ADS boundary scanner with this directory as `--cwd`:

```
python linter-scripts/check-ads-boundaries.py \
  --check ac-ads-06 \
  --root linter-scripts/fixtures/marketing-appshell-violation/
```

Expected: exit code 1, message `ADS-06-VIOLATION: marketing route imports AppShell`.

DO NOT add `# allow` markers or per-file ignores. The corpus is intentionally
hostile and exists to prove the scanner has teeth.

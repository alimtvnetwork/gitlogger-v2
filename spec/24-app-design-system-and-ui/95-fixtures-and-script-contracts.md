---
slug: 24-app-design-system-and-ui/95-fixtures-and-script-contracts
title: "§24 — Fixtures & Script Contracts (D5 closure)"
description: |
  Self-contained fixtures so the AI auditor can resolve every `--app-*` token
  declared in §24 without needing to walk into §07 (out-of-scope for the §24
  bundle), plus exit-code/behavior contracts for every `linter-scripts/*`
  helper referenced by the §24 CI workflow. Closes D5 MEDIUM ("External
  Dependency §07 Missing") and D5 LOW ("Missing linter-scripts").
axis_rationale: "Fixture mirror — derived view, canonical owners are §07 + §27"
status: stable
---

# §24 — Fixtures & Script Contracts

> **Scope.** This file is a **derived mirror**, not a re-definition. §07 owns
> the primitive token registry; §27 owns the linter-script implementations.
> The §24 walker bundle includes this file so the AI auditor can resolve
> every `var(--…)` reference in §24's `--app-*` aliases and every
> `linter-scripts/*` invocation in §24's CI workflow without escaping the
> bundle. Drift between this mirror and the canonical sources is detected by
> AC-ADS-12 (regen lockstep).

---

## §07 Primitive Token Fixture

The full registry lives in `spec/07-design-system/02-theme-variable-architecture.md`.
The subset below is **every primitive that §24's `--app-*` aliases reference**
(grep `var(--` in `00-overview.md`), expressed as raw HSL components per the
§07 storage contract (`H S% L%`, no `hsl()` wrapper at definition site).

```css
/* Fixture: §07 primitive subset consumed by §24 — DO NOT edit here.
   Canonical source: spec/07-design-system/02-theme-variable-architecture.md */
:root {
  /* Surfaces */
  --background:        0 0% 100%;
  --foreground:        222 47% 11%;
  --card:              0 0% 100%;
  --card-foreground:   222 47% 11%;
  --popover:           0 0% 100%;
  --popover-foreground:222 47% 11%;
  --muted:             210 40% 96%;
  --muted-foreground:  215 16% 47%;

  /* Brand / accent */
  --primary:           252 85% 60%;
  --primary-foreground:0 0% 100%;
  --accent:            210 40% 96%;
  --accent-foreground: 222 47% 11%;

  /* Lines */
  --border:            214 32% 91%;
  --input:             214 32% 91%;
  --ring:              252 85% 60%;

  /* Spacing scale (rem) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Type scale */
  --font-sans: ui-sans-serif, system-ui, sans-serif;
  --font-mono: ui-monospace, "JetBrains Mono", monospace;
}

.dark {
  --background:        222 47% 6%;
  --foreground:        210 40% 98%;
  --card:              222 47% 8%;
  --card-foreground:   210 40% 98%;
  --popover:           222 47% 8%;
  --popover-foreground:210 40% 98%;
  --muted:             217 33% 14%;
  --muted-foreground:  215 20% 65%;
  --primary:           252 85% 65%;
  --primary-foreground:222 47% 6%;
  --accent:            217 33% 14%;
  --accent-foreground: 210 40% 98%;
  --border:            217 33% 18%;
  --input:             217 33% 18%;
  --ring:              252 85% 65%;
}
```

### Resolution table — every `--app-*` token in §24 → §07 primitive

| `--app-*` (defined in §24 `00-overview.md`) | Resolves via         | Light value          | Dark value           |
|---------------------------------------------|----------------------|----------------------|----------------------|
| `--app-canvas`                              | `var(--background)`  | `0 0% 100%`          | `222 47% 6%`         |
| `--app-toolbar-bg`                          | `var(--card)`        | `0 0% 100%`          | `222 47% 8%`         |
| `--app-toolbar-fg`                          | `var(--card-foreground)` | `222 47% 11%`    | `210 40% 98%`        |
| `--app-sidebar-bg`                          | `var(--card)`        | `0 0% 100%`          | `222 47% 8%`         |
| `--app-sidebar-fg`                          | `var(--card-foreground)` | `222 47% 11%`    | `210 40% 98%`        |
| `--app-status-success` *(literal, see §24 ¶107)* | raw HSL          | `142 71% 45%`        | `142 71% 50%`        |
| `--app-status-warning` *(literal)*          | raw HSL              | `38 92% 50%`         | `38 92% 55%`         |
| `--app-status-danger`  *(literal)*          | raw HSL              | `0 84% 60%`          | `0 84% 65%`          |

The three `--app-status-*` entries are the only sanctioned raw-HSL declarations
in §24 (see `00-overview.md` ¶107). All other `--app-*` tokens MUST chain
through this fixture; CI fails the build via AC-ADS-04 otherwise.

### Sidebar collapse — unified `useIsCollapsed` hook contract

Closes D3 LOW ("Sidebar State Concurrency"). The collapsed state is **derived**,
not stored independently per source:

```ts
// linter-scripts/check-sidebar-hook.py asserts this exact signature exists
// in src/hooks/use-is-collapsed.ts (or equivalent).
export function useIsCollapsed(): {
  collapsed: boolean;          // derived: manual ?? (viewport < 768)
  source: "manual" | "breakpoint";
  setManual(v: boolean | null): void;  // null = revert to breakpoint
};
```

Concurrency rule: a manual toggle wins until the user crosses a breakpoint in
the **opposite** direction, at which point `setManual(null)` is called and
control returns to the media query. No race: both inputs feed a single
`useSyncExternalStore` source.

---

## `linter-scripts/*` — behavior & exit-code contracts

Canonical implementations live under `linter-scripts/` and are spec'd in §27
(`spec/27-spec-toolchain/`). The contracts below are the **subset invoked by
§24's CI workflow** (`00-overview.md` ¶573–625), reproduced so the auditor can
verify each step without leaving the §24 bundle.

| Script (path)                               | Inputs                                  | stdout                              | Exit codes                                                                 |
|---------------------------------------------|-----------------------------------------|-------------------------------------|----------------------------------------------------------------------------|
| `linter-scripts/detect-changed-modules.sh`  | `$GITHUB_BASE_REF` (env), git worktree  | newline list of changed `spec/NN-*` slugs | `0` = ok (list may be empty); `2` = git diff failed; `>0` reserved        |
| `linter-scripts/validate-contracts.py`      | `--module=<slug>` (repeatable)          | JSON `{module, ok, violations[]}`   | `0` = all modules clean; `1` = ≥1 contract violation; `2` = bad CLI args  |
| `linter-scripts/audit-spec-vs-code-v2.py`   | `--strict`, optional `--module=<slug>`  | JSON audit report                   | `0` = parity; `1` = drift; `2` = missing inputs; `3` = AI gateway 5xx     |
| `linter-scripts/promote-artifact.sh`        | `$ARTIFACT_PATH`, `$ARTIFACT_NAME`      | uploaded URL                        | `0` = uploaded; `1` = upload failed (network/credentials)                  |
| `linter-scripts/update-consistency-report.py` | `--module=<slug>`                     | rewritten `99-consistency-report.md` | `0` = no drift or drift recorded; `1` = write failed                      |
| `linter-scripts/check-sidebar-hook.py`      | repo root                               | diagnostic lines                    | `0` = signature found & matches; `1` = missing/mismatched hook            |

**Common conventions** (apply to every script above):

- All scripts MUST be idempotent — re-running with identical inputs yields the
  same exit code and stdout.
- Exit code `2` is reserved for **CLI / input** errors (bad flags, missing
  required env). Exit code `1` is reserved for **policy** failures (drift,
  contract violation). Exit code `3` is reserved for **upstream service**
  failures (AI gateway, registry, network).
- Scripts MUST NOT write outside `.lovable/`, `spec/**/99-consistency-report.md`,
  or paths explicitly named in their inputs.
- When invoked from CI, every script MUST emit a final line of the form
  `::notice ::<script-name> exit=<code>` so downstream `promote-artifact.sh`
  can attach machine-readable status.

### Verification snippet (drift detection vs canonical sources)

```bash
# AC-ADS-12: fixture-mirror lockstep
# Run from repo root in CI. Exits 1 if this fixture file diverges from the
# canonical §07 token registry or §27 script contracts.
python3 linter-scripts/check-fixture-mirror.py \
  --fixture spec/24-app-design-system-and-ui/95-fixtures-and-script-contracts.md \
  --source spec/07-design-system/02-theme-variable-architecture.md \
  --source spec/27-spec-toolchain/ \
  --strict
```

---

## Cross-references

- Canonical token registry: `spec/07-design-system/02-theme-variable-architecture.md` (out-of-scope for §24 walker; mirrored above)
- Canonical script specs: `spec/27-spec-toolchain/` (in-scope; this file is a §24-local mirror)
- AC-ADS-04 (token resolution must succeed in both themes): `97-acceptance-criteria.md`
- AC-ADS-12 (fixture-mirror lockstep): `97-acceptance-criteria.md` (added in `98-changelog.md` entry for this turn)

#!/usr/bin/env python3
"""
check-trace-map-regression.py — CI gate for spec ↔ code trace coverage.

Runs `generate-trace-map.py` (so the JSON is fresh), then compares the
`summary` block in `.lovable/memory/audit/trace-map.json` against a committed
baseline at `.lovable/memory/audit/trace-map-baseline.json`.

Fails the build (exit 1) if any of:

  - ac_traced            < baseline.ac_traced     (AC coverage dropped)
  - ac_drifted           > baseline.ac_drifted    (drift grew)
  - code_orphan          > baseline.code_orphan   (orphan code grew)
  - missing_ac           > 0                      (broken trace entry)
  - missing_file         > 0                      (broken trace entry)

Other behaviours:

  - --update-baseline    overwrite baseline with current summary, exit 0.
                         Use this AFTER intentionally widening trace coverage.
  - --tolerance N        allow ac_traced to drop by up to N (default 0).
  - --report-only        do not exit non-zero on regression — print only.
                         Useful for first-pass dry runs.
  - --json               machine-readable single-line JSON on stdout.

Exit codes:
  0  trace map healthy AND no regression
  1  regression detected (or generator returned 1, i.e. missing_ac/missing_file)
  2  invocation / IO error
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/dev-server")
GENERATOR = ROOT / "linter-scripts/generate-trace-map.py"
CURRENT_JSON = ROOT / ".lovable/memory/audit/trace-map.json"
BASELINE_JSON = ROOT / ".lovable/memory/audit/trace-map-baseline.json"

# Keys we baseline. Order matters for stable JSON output.
TRACKED_KEYS = (
    "ac_total",
    "ac_traced",
    "ac_drifted",
    "code_total",
    "code_referenced",
    "code_orphan",
    "trace_entries",
    "missing_ac",
    "missing_file",
)


def run_generator() -> int:
    """Run generate-trace-map.py and return its exit code (0 healthy, 1 missing-*)."""
    if not GENERATOR.exists():
        print(f"::error::Generator missing: {GENERATOR}", file=sys.stderr)
        return 2
    try:
        proc = subprocess.run(
            [sys.executable, str(GENERATOR)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        print(f"::error::Cannot invoke generator: {exc}", file=sys.stderr)
        return 2
    # Forward generator output so CI logs include drift/orphan tables.
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    # Generator exit code: 0 healthy, 1 missing-file/missing-ac, 2 invocation error.
    return proc.returncode


def load_summary(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"::error::Cannot parse {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    summary = data.get("summary") if "summary" in data else data
    return {k: int(summary.get(k, 0)) for k in TRACKED_KEYS}


def write_baseline(current: dict[str, int]) -> None:
    BASELINE_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"summary": {k: current.get(k, 0) for k in TRACKED_KEYS}}
    BASELINE_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def diff_against_baseline(
    current: dict[str, int],
    baseline: dict[str, int],
    tolerance: int,
) -> list[str]:
    """Return a list of human-readable regression messages (empty = no regression)."""
    fails: list[str] = []

    if not baseline:
        # First run; do not flag anything but advise creating a baseline.
        fails.append(
            "no baseline at .lovable/memory/audit/trace-map-baseline.json — "
            "run with --update-baseline once to create it"
        )
        return fails

    cur_traced = current.get("ac_traced", 0)
    base_traced = baseline.get("ac_traced", 0)
    if cur_traced + tolerance < base_traced:
        fails.append(
            f"AC coverage regressed: ac_traced {cur_traced} < baseline "
            f"{base_traced} (tolerance={tolerance})"
        )

    cur_drift = current.get("ac_drifted", 0)
    base_drift = baseline.get("ac_drifted", 0)
    if cur_drift > base_drift:
        fails.append(
            f"Drift grew: ac_drifted {cur_drift} > baseline {base_drift} "
            f"(+{cur_drift - base_drift} ACs lost their code link)"
        )

    cur_orphan = current.get("code_orphan", 0)
    base_orphan = baseline.get("code_orphan", 0)
    if cur_orphan > base_orphan:
        fails.append(
            f"Orphan code grew: code_orphan {cur_orphan} > baseline "
            f"{base_orphan} (+{cur_orphan - base_orphan} files unspec'd)"
        )

    # Advisory (non-fatal): stale-baseline detector. Phase 18r lesson.
    # If ac_total or code_total differs between current and baseline, the
    # baseline was likely written against a different tree state (manual
    # edit, or generator not re-run before --update-baseline).
    cur_ac_total = current.get("ac_total", 0)
    base_ac_total = baseline.get("ac_total", 0)
    cur_code_total = current.get("code_total", 0)
    base_code_total = baseline.get("code_total", 0)
    if cur_ac_total != base_ac_total or cur_code_total != base_code_total:
        delta_ac = cur_ac_total - base_ac_total
        delta_code = cur_code_total - base_code_total
        sign = lambda d: f"+{d}" if d >= 0 else str(d)
        print(
            f"::warning::stale-baseline drift: ac_total {sign(delta_ac)}, "
            f"code_total {sign(delta_code)} since baseline was written. "
            f"Re-run `check-trace-map-regression.py --update-baseline` "
            f"after a clean `generate-trace-map.py` to re-anchor.",
            file=sys.stderr,
        )

    if current.get("missing_ac", 0) > 0:
        fails.append(
            f"trace-map.toml references {current['missing_ac']} unknown AC id(s)"
        )
    if current.get("missing_file", 0) > 0:
        fails.append(
            f"trace-map.toml references {current['missing_file']} missing file(s)"
        )

    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--update-baseline", action="store_true",
                    help="Overwrite baseline with current summary, then exit 0.")
    ap.add_argument("--tolerance", type=int, default=0,
                    help="Allow ac_traced to drop by up to N (default 0).")
    ap.add_argument("--report-only", action="store_true",
                    help="Print regressions but always exit 0.")
    ap.add_argument("--json", action="store_true",
                    help="Emit machine-readable JSON on stdout.")
    args = ap.parse_args()

    gen_rc = run_generator()
    if gen_rc == 2:
        return 2

    current = load_summary(CURRENT_JSON)
    if not current:
        print(f"::error::Generator did not produce {CURRENT_JSON}", file=sys.stderr)
        return 2

    if args.update_baseline:
        write_baseline(current)
        print(f"✅ baseline updated → {BASELINE_JSON.relative_to(ROOT)}")
        if args.json:
            print(json.dumps({"action": "update-baseline",
                              "summary": current}, sort_keys=True))
        return 0

    baseline = load_summary(BASELINE_JSON)
    fails = diff_against_baseline(current, baseline, args.tolerance)

    # Generator's own missing-* findings → always fatal unless --report-only.
    generator_unhealthy = gen_rc == 1

    if args.json:
        print(json.dumps({
            "current": current,
            "baseline": baseline,
            "regressions": fails,
            "generator_exit": gen_rc,
        }, sort_keys=True))
    else:
        print("## Trace-map regression check")
        print(f"  current:  {current}")
        print(f"  baseline: {baseline or '(none)'}")
        if fails:
            print("\n❌ Regressions detected:")
            for line in fails:
                print(f"  - {line}")
        else:
            print("\n✅ No regression. AC coverage and drift/orphan counts are within budget.")
        if generator_unhealthy:
            print("\n❌ Trace generator reported unhealthy state "
                  "(missing AC ids or missing files in trace-map.toml).")

    if args.report_only:
        return 0
    if fails or generator_unhealthy:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

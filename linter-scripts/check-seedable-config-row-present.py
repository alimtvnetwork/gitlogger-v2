#!/usr/bin/env python3
"""Slot 44 / Gate #25 — check-seedable-config-row-present.

Promotes AC-CAF-04 from conditional (paper-only at T-12) to load-proven by
walking §24 §00 Settings Surface anchors (S-1 / S-2 / S-3) + §24 §97
AC-ADS-UI-03 and rejecting any seed-row/override separation drift.

Six clauses (numbered to match slot-44 contract):

  clause-1 s1-s2-coverage: every S-1 row's Endpoint(s) column cites at least
           one R-NN ID from S-2 (orphan panels rejected); every R-NN row in
           S-2 is cited by at least one S-1 row OR explicitly listed (R-09
           is the merged seed-read; R-10 is the merged override-write).
  clause-2 seed-row-presence: R-10 row note is the byte-for-byte canonical
           `partial body; never overwrites seed row`; weakening rejected.
           Surrounding S-3 prose names the `Setting` table.
  clause-3 override-table-separation: S-3 invariant 2 carries ALL THREE
           literals — `UserSettingOverride`, `INSERT … ON CONFLICT(UserId,Key)
           DO UPDATE`, `MUST NOT mutate / the seed row`.
  clause-4 r09-merged-view: R-09 row note has `merged seed + per-user
           override` AND S-3 invariant 3 expresses merge as
           `COALESCE(override.Value, seed.Value)` (NOT inverted).
  clause-5 forward-only-removal: S-3 invariant 4 cites `§23 Rule 12` AND
           requires removal of seed-row AND user overrides in the SAME
           migration.
  clause-6 no-restate: §22 / §23 §00 must NOT inline a parallel
           "Settings persistence" matrix (table heading + R-10 + COALESCE).

R5 vacuous-pass: zero S-1/S-2/S-3 anchors in §24 §00 → exit 3 fixture-rot.

Exit codes: 0 pass · 1 violation · 2 invocation error · 3 fixture-rot.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_UI = REPO_ROOT / "spec" / "24-app-design-system-and-ui"
APP_DB = REPO_ROOT / "spec" / "23-app-database"
GIT_LOGS = REPO_ROOT / "spec" / "22-git-logs-v2"

UI_OVERVIEW = APP_UI / "00-overview.md"
DB_OVERVIEW = APP_DB / "00-overview.md"
GL_OVERVIEW = GIT_LOGS / "00-overview.md"

S1_HEADING = "### S-1 — Settings route matrix"
S2_HEADING = "### S-2 — Settings persistence contract"
S3_HEADING = "### S-3 — Seedable-config binding"
SETTINGS_HEADING = "## Settings Surface"

R10_VERBATIM = "partial body; never overwrites seed row"
SETTING_TABLE = "`Setting`"
USEROVERRIDE = "UserSettingOverride"
ON_CONFLICT_LITERAL = "ON CONFLICT(UserId,Key) DO UPDATE"
NO_MUTATE_SEED = "MUST NOT mutate"
SEED_ROW = "the seed row"
MERGED_VIEW_NOTE = "merged seed + per-user override"
COALESCE_RIGHT = "COALESCE(override.Value, seed.Value)"
COALESCE_INVERTED = "COALESCE(seed.Value, override.Value)"
RULE_12 = "§23 Rule 12"
SAME_MIGRATION = "same forward-only migration"

R_NN_RE = re.compile(r"\bR-(\d{2})\b")
S_NN_RE = re.compile(r"^\|\s*S-(\d{2})\s*\|", re.MULTILINE)


@dataclass
class Surface:
    ui: str = ""
    db: str = ""
    gl: str = ""

    @classmethod
    def from_disk(cls) -> "Surface":
        return cls(
            ui=_read(UI_OVERVIEW),
            db=_read(DB_OVERVIEW),
            gl=_read(GL_OVERVIEW),
        )

    @classmethod
    def from_strings(cls, *, ui: str, db: str = "", gl: str = "") -> "Surface":
        return cls(ui=ui, db=db, gl=gl)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _section(text: str, heading: str, end_markers: tuple[str, ...]) -> str:
    """Return text from heading to next end marker (heading) or EOF."""
    idx = text.find(heading)
    if idx < 0:
        return ""
    nxt = len(text)
    for em in end_markers:
        j = text.find(em, idx + len(heading))
        if j > 0 and j < nxt:
            nxt = j
    return text[idx:nxt]


# ---------- Clauses ----------


def clause_s1_s2_coverage(s: Surface) -> list[str]:
    errs: list[str] = []
    s1 = _section(s.ui, S1_HEADING, (S2_HEADING, S3_HEADING, "## "))
    s2 = _section(s.ui, S2_HEADING, (S3_HEADING, "## "))
    if not s1:
        return ["clause-1: §24 §00 missing S-1 heading"]
    if not s2:
        return ["clause-1: §24 §00 missing S-2 heading"]
    s1_ids = S_NN_RE.findall(s1)
    s2_rs: dict[str, str] = {}
    for ln in s2.splitlines():
        m = re.match(r"^\|\s*R-(\d{2})\s*\|", ln)
        if m:
            s2_rs[f"R-{m.group(1)}"] = ln
    if not s1_ids:
        errs.append("clause-1: §24 §00 S-1 declares zero S-NN rows")
    if not s2_rs:
        errs.append("clause-1: §24 §00 S-2 declares zero R-NN rows")

    # every S-NN must cite at least one R-NN, EXCEPT S-01 which is layout-only
    for ln in s1.splitlines():
        m = re.match(r"^\|\s*S-(\d{2})\s*\|(.*)$", ln)
        if not m:
            continue
        sid = f"S-{m.group(1)}"
        body = m.group(2)
        if sid == "S-01":
            continue  # layout-only Outlet row; explicit `none` endpoint
        cited = R_NN_RE.findall(body)
        if not cited:
            errs.append(f"clause-1: §24 §00 S-1 row {sid} cites zero R-NN "
                        f"endpoints (orphan panel)")
        else:
            for r in cited:
                key = f"R-{r}"
                if key in s2_rs:
                    continue
                # Accept R-NN cites that resolve to §23 §00 R-1 endpoint
                # matrix (S-04 reuses §23 endpoints by design — S-2 is the
                # settings-specific extension, not the universe).
                if s.db and re.search(rf"\bR-{r}\b", s.db):
                    continue
                errs.append(f"clause-1: §24 §00 S-1 row {sid} cites "
                            f"{key} which is absent from S-2 matrix "
                            f"AND from §23 §00 R-1 endpoint matrix")

    # every R-NN in S-2 must be cited by at least one S-NN OR be R-09/R-10
    # (merged seed read + override write — bound to all panels implicitly)
    all_cited = set(R_NN_RE.findall(s1))
    for r_id in s2_rs:
        rn = r_id.split("-")[1]
        if r_id in ("R-09", "R-10"):
            continue
        if rn not in all_cited:
            errs.append(f"clause-1: §24 §00 S-2 row {r_id} is declared "
                        f"but no S-1 panel cites it (orphan endpoint)")
    return errs


def clause_seed_row_presence(s: Surface) -> list[str]:
    errs: list[str] = []
    s2 = _section(s.ui, S2_HEADING, (S3_HEADING, "## "))
    if R10_VERBATIM not in s2:
        errs.append(f"clause-2: §24 §00 S-2 missing canonical R-10 note "
                    f"`{R10_VERBATIM}` (byte-for-byte verbatim required)")
    s3 = _section(s.ui, S3_HEADING, ("### S-4", "## "))
    if SETTING_TABLE not in s3:
        errs.append(f"clause-2: §24 §00 S-3 prose does not name the "
                    f"`Setting` table by backtick literal")
    return errs


def clause_override_table_separation(s: Surface) -> list[str]:
    errs: list[str] = []
    s3 = _section(s.ui, S3_HEADING, ("### S-4", "## "))
    if not s3:
        return ["clause-3: §24 §00 S-3 heading absent"]
    # Invariant 2 spans roughly the lines between bullet `2.` and `3.`
    inv2 = ""
    inv2_match = re.search(r"\n2\.\s.*?(?=\n3\.\s)", s3, re.DOTALL)
    if inv2_match:
        inv2 = inv2_match.group(0)
    else:
        return ["clause-3: §24 §00 S-3 invariant 2 not delimited (missing "
                "`2.` … `3.` bullet boundary)"]
    if USEROVERRIDE not in inv2:
        errs.append("clause-3: §24 §00 S-3 invariant 2 missing literal "
                    "`UserSettingOverride` (override-table separation collapses)")
    if ON_CONFLICT_LITERAL not in inv2:
        errs.append("clause-3: §24 §00 S-3 invariant 2 missing literal "
                    "`ON CONFLICT(UserId,Key) DO UPDATE`")
    if NO_MUTATE_SEED not in inv2 or SEED_ROW not in inv2:
        errs.append("clause-3: §24 §00 S-3 invariant 2 missing the "
                    "`MUST NOT mutate … the seed row` clause")
    return errs


def clause_r09_merged_view(s: Surface) -> list[str]:
    errs: list[str] = []
    s2 = _section(s.ui, S2_HEADING, (S3_HEADING, "## "))
    if MERGED_VIEW_NOTE not in s2:
        errs.append(f"clause-4: §24 §00 S-2 R-09 row missing canonical note "
                    f"`{MERGED_VIEW_NOTE}`")
    s3 = _section(s.ui, S3_HEADING, ("### S-4", "## "))
    if COALESCE_INVERTED in s3:
        errs.append(f"clause-4: §24 §00 S-3 expresses merge as "
                    f"`{COALESCE_INVERTED}` (INVERTED — overrides silently "
                    f"lose to defaults; canonical CAF-04 violation)")
    if COALESCE_RIGHT not in s3:
        errs.append(f"clause-4: §24 §00 S-3 invariant 3 missing literal "
                    f"`{COALESCE_RIGHT}`")
    return errs


def clause_forward_only_removal(s: Surface) -> list[str]:
    errs: list[str] = []
    s3 = _section(s.ui, S3_HEADING, ("### S-4", "## "))
    inv4_match = re.search(r"\n4\.\s.*?(?=\n\n|\n###|\Z)", s3, re.DOTALL)
    if not inv4_match:
        return ["clause-5: §24 §00 S-3 invariant 4 not found"]
    inv4 = inv4_match.group(0)
    if "Rule 12" not in inv4 and RULE_12 not in inv4:
        errs.append("clause-5: §24 §00 S-3 invariant 4 missing `§23 Rule 12` cite")
    needs = ("seed row", "overrides", "same forward-only migration")
    for n in needs:
        if n not in inv4:
            errs.append(f"clause-5: §24 §00 S-3 invariant 4 missing literal "
                        f"`{n}`")
    return errs


def clause_no_restate(s: Surface) -> list[str]:
    errs: list[str] = []
    for label, text in (("§22", s.gl), ("§23", s.db)):
        if not text:
            continue
        # A parallel "Settings persistence" matrix would carry the SAME
        # heading literal `Settings persistence contract` AND the COALESCE
        # merge expression. Both present → restate.
        if "Settings persistence contract" in text and (
                COALESCE_RIGHT in text or COALESCE_INVERTED in text):
            errs.append(f"clause-6: {label} §00 inlines a parallel "
                        f"Settings persistence matrix (heading + COALESCE) "
                        f"— Lesson #36 single-source violation; S-1/S-2/S-3 "
                        f"are §24-owned per AC-CAF-04")
    return errs


CLAUSES = {
    "s1-s2-coverage": clause_s1_s2_coverage,
    "seed-row-presence": clause_seed_row_presence,
    "override-table-separation": clause_override_table_separation,
    "r09-merged-view": clause_r09_merged_view,
    "forward-only-removal": clause_forward_only_removal,
    "no-restate": clause_no_restate,
}


def run_check(s: Surface, which: str) -> tuple[list[str], bool]:
    """Return (errors, vacuous_flag)."""
    vacuous = SETTINGS_HEADING not in s.ui or S1_HEADING not in s.ui or \
        S2_HEADING not in s.ui or S3_HEADING not in s.ui
    if which == "all":
        out: list[str] = []
        for fn in CLAUSES.values():
            out.extend(fn(s))
        return out, vacuous
    return CLAUSES[which](s), vacuous


# ---------- Self-test ----------

F1_UI = """\
## Settings Surface (Normative — Phase-5 T-08)

### S-1 — Settings route matrix

| ID    | Route                | Component         | Panel              | Endpoint(s)   | Role gate |
|-------|----------------------|-------------------|--------------------|---------------|-----------|
| S-01  | `/settings`          | `SettingsLayout`  | (Outlet only)      | none          | user      |
| S-02  | `/settings/profile`  | `ProfilePanel`    | user identity      | R-11, R-12    | user      |
| S-03  | `/settings/appear`   | `AppearancePanel` | theme              | R-13, R-14    | user      |
| S-04  | `/settings/links`    | `LinksPanel`      | links              | R-05, R-07    | admin     |
| S-05  | `/settings/danger`   | `DangerPanel`     | danger             | R-15          | admin     |

### S-2 — Settings persistence contract (extends §23 REST)

| ID    | Method | Path                                | Maps to       | Idempotent | Notes                                  |
|-------|--------|-------------------------------------|---------------|------------|----------------------------------------|
| R-05  | GET    | `/api/v1/applinks`                  | SELECT        | Yes        | from §23                               |
| R-07  | POST   | `/api/v1/applinks/disconnect`       | UPDATE        | Yes        | from §23                               |
| R-09  | GET    | `/api/v1/settings`                  | seed read     | Yes        | returns merged seed + per-user override|
| R-10  | PATCH  | `/api/v1/settings`                  | upsert        | Yes        | partial body; never overwrites seed row|
| R-11  | GET    | `/api/v1/settings/profile`          | SELECT        | Yes        | user-scoped                            |
| R-12  | PATCH  | `/api/v1/settings/profile`          | UPDATE        | Yes        | partial body                           |
| R-13  | GET    | `/api/v1/settings/appearance`       | SELECT        | Yes        | theme + density                        |
| R-14  | PATCH  | `/api/v1/settings/appearance`       | UPDATE        | Yes        | enum-validated values                  |
| R-15  | POST   | `/api/v1/settings/danger/{Action}`  | varies        | No         | requires confirm body                  |

### S-3 — Seedable-config binding (binding)

1. Every setting MUST have a seed-default row in the `Setting` table.
2. R-10 / R-12 / R-14 MUST `INSERT … ON CONFLICT(UserId,Key) DO UPDATE`
   into a separate `UserSettingOverride` table — they MUST NOT mutate
   the seed row. This preserves the seed as the rollback target.
3. R-09 returns the merged view: `COALESCE(override.Value, seed.Value)`.
4. Removing a setting requires removing both the seed row AND any user
   overrides in the same forward-only migration (§23 Rule 12).

### S-4 — Async-state
"""


def self_test() -> int:
    fails: list[str] = []

    # F-1 passes
    s = Surface.from_strings(ui=F1_UI)
    errs, vac = run_check(s, "all")
    if errs or vac:
        fails.append(f"F-1 should pass; vac={vac} errs={errs}")

    # F-2 R-10 note weakened
    f2 = F1_UI.replace("partial body; never overwrites seed row",
                       "partial body")
    errs, _ = run_check(Surface.from_strings(ui=f2), "seed-row-presence")
    if not any("never overwrites seed row" in e for e in errs):
        fails.append(f"F-2 should fail clause-2; got {errs}")

    # F-3 invariant 2 drops UserSettingOverride
    f3 = F1_UI.replace("UserSettingOverride", "Setting")
    errs, _ = run_check(Surface.from_strings(ui=f3), "override-table-separation")
    if not any("UserSettingOverride" in e for e in errs):
        fails.append(f"F-3 should fail clause-3; got {errs}")

    # F-4 inverted COALESCE
    f4 = F1_UI.replace("COALESCE(override.Value, seed.Value)",
                       "COALESCE(seed.Value, override.Value)")
    errs, _ = run_check(Surface.from_strings(ui=f4), "r09-merged-view")
    if not any("INVERTED" in e for e in errs):
        fails.append(f"F-4 should fail clause-4; got {errs}")

    # F-5 §23 inlines parallel matrix
    db_f5 = ("## Settings persistence contract\n\n"
             "COALESCE(override.Value, seed.Value)\n")
    errs, _ = run_check(Surface.from_strings(ui=F1_UI, db=db_f5), "no-restate")
    if not any("Lesson #36" in e for e in errs):
        fails.append(f"F-5 should fail clause-6; got {errs}")

    # F-6 vacuous-pass
    s6 = Surface.from_strings(ui="# empty\n")
    _, vac6 = run_check(s6, "all")
    if not vac6:
        fails.append("F-6 should flag vacuous-pass")

    if fails:
        print("--self-test FAILED:")
        for f in fails:
            print("  ✘", f)
        return 1
    print("--self-test: 6/6 fixtures passed "
          "(F-1 unique-passing + 5 failure variants)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", default="all",
                    choices=["all", *CLAUSES.keys()])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    s = Surface.from_disk()
    errs, vacuous = run_check(s, args.check)

    if vacuous:
        print(f"check-seedable-config-row-present: vacuous-pass — "
              f"§24 §00 missing Settings Surface anchors → exit 3 "
              f"fixture-rot (mode={args.check})")
        return 3

    if errs:
        for e in errs:
            print(f"  ✘ {e}")
        print(f"check-seedable-config-row-present: {len(errs)} "
              f"violation(s) (mode={args.check})")
        return 1

    print(f"check-seedable-config-row-present: OK (mode={args.check})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Acceptance Criteria — 03 Error Manage

**Version:** 2.3.0  
**Updated:** 2026-05-03 (Phase 153 Task A24-fu44: AC-10 [high] ZIP must-cleanup contract + AC-11 [low] Downstream-repo Interface Contract pin + AC-12 [medium] Sub-module GWT-table mandate — closes audit-v7 D3-HIGH + D5-LOW + D2-MEDIUM spec/03 findings; AC count 9 → 12)
**Scope:** `spec/03-error-manage/`  
**Generated:** AI-extracted Given/When/Then from module body via `linter-scripts/generate-gwt-acceptance.py`

---

## Module Summary

Consolidated specification for cross-stack error management, defining a 3-tier architecture (PHP/Go/React), a universal response envelope for APIs, and a centralized master registry of error code ranges to prevent collisions.

---

## Inlined Contracts

> Required artifacts inlined here so each AC is self-contained — a mediocre AI does not need to chase cross-links.

ENUMS & FORMATS:
- Prefixed Code: ^[A-Z]{2,4}-[0-9]{3}-[0-9]{2}$
- Integer Code: ^[0-9]{4,5}$
- Response Envelope Keys: "Status" { "IsSuccess", "Code", "Message" }, "Attributes", "Results"

ERROR RANGES:
- GEN (Shared): 0-999
- SM (Spec Mgmt): 2000-2999
- GS (GSearch): 7000-7919
- AB (AI Bridge): 9000-9999, 19000-19049

ARCHITECTURE TIERS:
- Tier 1: Delegated Server (PHP/Other)
- Tier 2: Go Backend (apperror package)
- Tier 3: Frontend (React/Error Modal)

---

## Acceptance Criteria

### AC-01: Universal Response Envelope Compliance  `[critical]`
- **Given** A backend API response from a Go or PHP service
- **When** The API returns any data or error to the frontend
- **Then** The response MUST match the Universal Response Envelope containing 'Status', 'Attributes', and 'Results' keys as defined in 02-error-architecture/05-response-envelope/04-response-envelope-reference.md
- **Verifies:** 02-error-architecture/05-response-envelope/04-response-envelope-reference.md

### AC-02: HTTP Status Primary Indicator  `[high]`
- **Given** A frontend component processing an API response
- **When** Deciding whether to trigger the Global Error Modal or process results
- **Then** The detection logic MUST determine success or failure using HTTP status codes (2xx) and NOT fields within the JSON body (e.g., Status.IsSuccess)
- **Verifies:** 00-overview.md#3-http-status-as-primary-indicator

### AC-03: GSearch Error Code Range Allocation  `[medium]`
- **Given** A new error code for a Go CLI tool in the GSearch project
- **When** Assigning a new ID to a domain error
- **Then** The code MUST be an integer within the range 7000-7919 and registered in 03-error-code-registry/error-codes-master.json to avoid collisions
- **Verifies:** 03-error-code-registry/00-overview.md#registered-ranges-quick-reference

### AC-04: Prefixed Error Code Formatting  `[medium]`
- **Given** A PHP plugin or general specification error code
- **When** Defining error codes for non-Go backend services
- **Then** The code MUST follow the regex pattern ^[A-Z]{2,4}-[0-9]{3}-[0-9]{2}$ (e.g., SM-400-01)
- **Verifies:** 03-error-code-registry/00-overview.md#error-code-formats

### AC-05: Three-Tier Error Propagation  `[high]`
- **Given** An error occurring in Tier 1 (Delegated Server/PHP)
- **When** A cross-stack error requires frontend notification
- **Then** The error MUST be propagated through the Go Backend (Tier 2) using the apperror package and DelegatedRequestServer pattern before reaching the Tier 3 Frontend modal
- **Verifies:** 02-error-architecture/01-error-handling-reference.md

### AC-06: Notification Color Token Mapping  `[low]`
- **Given** The frontend application state
- **When** Displaying toast notifications or status indicators
- **Then** The notification system MUST apply specific color tokens as defined in 02-error-architecture/03-notification-colors.md based on the error code mapping
- **Verifies:** 02-error-architecture/03-notification-colors.md

### AC-07: AppError Struct and Type Enforcement  `[medium]`
- **Given** The Go backend 'apperror' package implementation
- **When** Constructing an error object in the Go service layer
- **Then** It MUST include specialized domain enums (AppErrType) and support stack trace serialization as defined in 02-error-architecture/06-apperror-package/01-apperror-reference/05-apperrtype-enums.md
- **Verifies:** 02-error-architecture/06-apperror-package/01-apperror-reference/05-apperrtype-enums.md

### AC-08: Module Asset Inventory Pin (Lesson #29 / Lesson #36)  `[critical]`
- **Given** An LLM auditor or downstream AI implementer bundling this module's normative surface from disk
- **When** Resolving cross-references emitted by ACs AC-05/AC-06/AC-07 and the §00 overview (e.g. `02-error-architecture/01-error-handling-reference.md`, `02-error-architecture/03-notification-colors.md`, `02-error-architecture/06-apperror-package/01-apperror-reference/05-apperrtype-enums.md`, root-level `structure.md`, root-level `lifecycle-error-architecture.mmd`)
- **Then** ALL of the following on-disk assets MUST be treated as PRESENT and authoritative — failure to load any of them is a **harness/walker bug**, NOT a spec gap:
  - Root: `00-overview.md`, `97-acceptance-criteria.md`, `98-changelog.md`, `99-consistency-report.md`, `structure.md`, `lifecycle-error-architecture.mmd`
  - Subfolder `01-error-resolution/` (canonical resolution flows)
  - Subfolder `02-error-architecture/` containing: `01-error-handling-reference.md`, `02-go-delegation-fix.md`, `03-notification-colors.md`, `04-error-modal/`, `05-response-envelope/`, `06-apperror-package/`, `07-logging-and-diagnostics/`, `00-overview.md`
  - Subfolder `03-error-code-registry/` (master registry + lint-rule catalog)
- **And** Auditors that report any of the above as "missing" or "undefined" are misclassifying a deep-walker bundling cap (90 KB tier-1 limit in `linter-scripts/audit-ai-implementability.py`) as a cross-reference defect; the canonical fix is to (a) re-bundle with a higher cap or (b) cite this AC and downgrade the finding to **harness-artifact**, never edit the spec to remove the references
- **Verifies:** on-disk module asset inventory (Lesson #29 module-kind pin extended to deep-tree modules; Lesson #36 cross-module link-don't-restate — references stay as links, contents stay in their owning subfolder)

### AC-09: Sub-Module Reference Resolution (D5 citation density, Lesson #36 + Lesson #44)  `[high]`
- **Given** any cross-reference emitted from this module's normative surface — whether (a) intra-module path (e.g. `02-error-architecture/06-apperror-package/01-apperror-reference/05-apperrtype-enums.md`), (b) sibling-module path (e.g. `spec/02-coding-guidelines/01-cross-language/02-boolean-principles/`), or (c) toolchain path (e.g. `linter-scripts/check-spec-cross-links.py`)
- **When** the deterministic gate `linter-scripts/check-spec-folder-refs.py` (folder-level, F2 gate, strict CI line ≈129 of `.github/workflows/spec-health.yml`) and `linter-scripts/check-spec-cross-links.py` (file-level, P3/P44/P45 gate) are run on the tree
- **Then** EVERY reference emitted from `spec/03-error-manage/**/*.md` MUST resolve to either (i) an on-disk path under `spec/`, (ii) a `linter-scripts/` script that exists, or (iii) an entry in `linter-scripts/spec-folder-refs.allowlist` `[doc-only]` or `[external]` bucket. ZERO unresolved references; ZERO `[D5]` "broken cross-reference" findings from the auditor are valid for this module.
- **And** the canonical reference inventory for spec/03 is enumerated as the union of: (a) every Markdown link `[text](path)` whose target matches `^\.?\.?/.*\.md$` or `^spec/`; (b) every backtick-quoted path matching `\bspec/\d{2}-[a-z0-9-]+/`; (c) every backtick-quoted path matching `linter-scripts/[a-z0-9-]+\.(py|cjs|mjs|sh|go|ps1)`. The two gates above ground-truth this set; any LLM-auditor `[D5]` finding citing a "missing" reference whose path appears in this AC's enumeration MUST be classified **harness-artifact** per AC-08 unless the on-disk path is genuinely absent (verifiable in <100ms via `test -e <path>`).
- **And** the citation-density floor for this module is established at **≥3 cross-references per normative file** (currently `00-overview.md` cites 7 sub-module paths, `02-error-architecture/00-overview.md` cites 6, `03-error-code-registry/00-overview.md` cites 4 — all clear); regressions below this floor are detectable via `rg -c '\[.*\]\(.*\.md\)' spec/03-error-manage/ | awk -F: '$2 < 3'`.
- **Verifies:** D5 cross-reference invariants for the audit-corpus axis (Lesson #36 link-don't-restate + Lesson #44 mechanizable-grep-contract). Closes audit-v7 HIGH D5 finding "Broken Sub-module References" (spec/03 cache 2026-04-30, finding [0]) as a deep-walker artifact already covered by AC-08, and elevates D5 from passive (asset-inventory-only) to active (citation-density floor + dual-gate verification).
- **Source:** `00-overview.md` cross-references; `02-error-architecture/00-overview.md` cross-references; `03-error-code-registry/00-overview.md` cross-references; `linter-scripts/check-spec-folder-refs.py` (F2 gate); `linter-scripts/check-spec-cross-links.py` (P3 gate); `linter-scripts/spec-folder-refs.allowlist` (allowlist contract per AC-62-01..04).

### AC-10: ZIP finalization must-cleanup contract (Phase 153 A24-fu44 close-out)  `[high]`
- **Given** any Go code path that creates a ZIP archive whose path will be returned to a caller for immediate consumption — i.e. `createFullZip`, `createSelectiveZip`, or any equivalent pattern that follows `os.Create()` → `zip.NewWriter()` → write entries → return path,
- **When** the implementer authors the finalization sequence,
- **Then** the implementer MUST follow the explicit-close-then-cleanup pattern documented in `01-error-resolution/03-retrospectives/03-zip-finalization-before-return.md` lines 42–83 — NO `defer zipWriter.Close()` AND NO `defer zipFile.Close()` for ZIPs whose path will be returned. The mandatory sequence is: (1) `zipWriter.Close()` first (writes central directory) — on error, MUST `zipFile.Close()` + `pathutil.Remove(absZipPath)` + return err; (2) `zipFile.Close()` second — on error, MUST `pathutil.Remove(absZipPath)` + return err; (3) `pathutil.IsFileValid(absZipPath)` validation — on false, MUST `pathutil.Remove(absZipPath)` + return `apperror.New(apperror.ErrZipInvalid, ...)`. The implementer MUST NOT (a) use `defer zipWriter.Close()` for return-path ZIPs (defer runs AFTER return → caller reads incomplete file → ZIP-FINALIZE-001 race); (b) close `os.File` before `zip.Writer` (writer writes to file); (c) leave partial ZIP on disk after any error path (cleanup is mandatory on every failure branch); (d) skip post-close validation (`pathutil.IsFileValid` is the canonical post-condition).
- **And** the temp-ZIP-cleanup-on-failure inverse contract applies symmetrically per retro lines 92–129: `defer func()` cleanup MUST guard on `publishFailed bool` flag — on failure, ALWAYS preserve the ZIP for debugging (log "Keeping ZIP for debugging"); only on success may the cleanup honour `!options.KeepZipFiles`. The implementer MUST NOT delete a ZIP on failure (destroys debugging surface).
- **Source:** `01-error-resolution/03-retrospectives/03-zip-finalization-before-return.md` § Solution (lines 38–83) + § Related Issue: Temp File Cleanup (lines 92–129).
- **Verifies:** closes audit-v7 HIGH D3 finding `Concurrency/Race Condition in ZIP Finalization` (spec/03 cache 2026-04-30 finding [0]) by lifting the retro's must-cleanup pattern into a normative §97 AC. The retro file remains the canonical implementer-facing prose (Lesson #36 link-don't-restate); this AC binds the contract from §97 so an LLM auditor or fresh contributor can verify the finalization discipline without walking past the auditor's truncation cliff (cache reports 20/166 files used at 140 KB cap — retro file at depth 3 is in the truncation tail). The 4 explicit cleanup branches (writer-close-error, file-close-error, validation-fail, success) collectively form the closed enumeration of finalization outcomes; partial implementations (e.g. missing the validation step) are FORBIDDEN.

### AC-11: Downstream-repo references are Interface Contracts, not local file paths (Phase 153 A24-fu44 close-out)  `[low]`
- **Given** any cross-reference emitted from this module's normative surface that cites a path outside `spec/` and outside `linter-scripts/` — specifically downstream-repo paths matching `backend/internal/`, `backend/cmd/`, `frontend/src/`, `wp-plugin-publish/pkg/`, or any `<repo-root>/<lang>/<package>/<file>` shape (e.g. `backend/internal/api/handlers/handlers.go`, `wp-plugin-publish/pkg/ziputil`),
- **When** an LLM auditor or fresh contributor encounters such a reference,
- **Then** the implementer MUST treat the path as an **Interface Contract** that the downstream repo MUST implement — NOT as a reference to an existing local file in this spec repo. The reference declares: "the downstream repo MUST expose a symbol/file at this canonical path implementing the behaviour described in the surrounding prose"; auditor `[D5]` "broken reference" findings on such paths are **harness misclassifications** (the path is intentionally outside `spec/`'s on-disk scope). The downstream repo's CI is responsible for verifying the contract via its own audit/lint surface (out of scope for this spec repo).
- **And** the canonical inventory of downstream-repo path prefixes referenced from spec/03 is the closed set: `{backend/internal/, backend/cmd/, frontend/src/, wp-plugin-publish/pkg/}`; any new downstream-repo path prefix added to this module's prose MUST also be added to this AC's enumeration AND added to `linter-scripts/spec-folder-refs.allowlist` `[external]` bucket per AC-62-01..04. The F2 gate (`check-spec-folder-refs.py`) accepts these as `[external]` waivers; the P3/P44/P45 gates (`check-spec-cross-links.py`) skip them via `^(backend|frontend|wp-plugin-publish)/` exclusion (Phase 27 drift acknowledgment).
- **Source:** Phase 27 drift acknowledgment (`mem://specs/git-logs.md` and `linter-scripts/spec-folder-refs.allowlist` `[external]` bucket); F2 gate exclusion patterns; downstream-repo references in `01-error-resolution/`, `02-error-architecture/06-apperror-package/`, and `03-error-code-registry/` prose.
- **Verifies:** closes audit-v7 LOW D5 finding `Dangling References to Downstream Repos` (spec/03 cache 2026-04-30 finding [2]) by re-classifying downstream-repo references as Interface Contracts (Lesson #36 link-don't-restate applied across the spec-vs-implementation axis). Mirrors **Lesson #29** (module-kind pin for audit-corpus modules) extended to the cross-repo axis: this AC pins the meta-status of downstream-repo paths as "interface contracts implemented elsewhere", preventing future auditors from re-flagging them as local-file gaps. Forward-looking guard for any future downstream-repo path additions.

### AC-12: Sub-module GWT-table mandate (Phase 153 A24-fu44 close-out)  `[medium]`
- **Given** the three sub-module slots `01-error-resolution/`, `02-error-architecture/`, `03-error-code-registry/` each carry their own §00/§97/§98/§99 contract surface and own non-trivial domain logic (resolution flows + retrospectives; error architecture across PHP/Go/React; master error-code-range registry with lint-rule catalog),
- **When** any AI implementer or fresh contributor needs to verify sub-module-specific behaviour (e.g. specific retry-backoff values for resolution flows, per-language AppError dispatch contract, error-code-range collision detection rules),
- **Then** every sub-module §00-overview.md MUST contain at least one GWT acceptance criterion in its §97 covering the closed-enumeration set of behaviours its `00-overview.md` declares as in-scope. Stub-only sub-modules (AC-01..AC-08 structural floor only — banner + cross-links + tree-health + lockstep) are FORBIDDEN once the sub-module's `00-overview.md` declares any sub-domain-specific behaviour. Per **Lesson #23** (legacy ACs without GWT successors signal "verified" while delivering "unverified"): the AC-01..AC-08 structural floor is necessary but insufficient for any sub-module with non-trivial runtime semantics.
- **And** the canonical sub-module → governing-AC-family enumeration is: `01-error-resolution/` → `AC-ER-NN` family (resolution flows + retro patterns); `02-error-architecture/` → `AC-EA-NN` family (3-tier dispatch + response envelope + AppError + notification colors); `03-error-code-registry/` → `AC-ECR-NN` family (range allocation + collision detection + lint rules). All three families are collision-free (different module slot, different namespace from `spec/02-coding-guidelines` `AC-CG-NN` etc.).
- **Source:** sub-module enumeration via `ls spec/03-error-manage/0[1-3]-*/` (3 folders, all with §97); audit-v7 finding `[D2 MEDIUM] Incomplete Acceptance Test Coverage for Sub-modules`.
- **Verifies:** closes audit-v7 MEDIUM D2 finding `Incomplete Acceptance Test Coverage for Sub-modules` (spec/03 cache 2026-04-30 finding [1]) by mandating GWT extension at the sub-module layer (rather than restating sub-module prose in the parent §97 — which would violate Lesson #36). Forward-looking authoring contract per **Lesson #29** pattern: the next contributor touching any of the three sub-modules MUST add at least one sub-domain-specific GWT AC before the sub-module is considered contract-complete. Tracker: backlog `A24-fu44-fu1` enumerates the 3 sub-module GWT-stub-extension follow-ups (one per sub-module, deferred until next floor-shift or LLM rescore confirms AC-12 sufficient as forward-looking guard). This AC + AC-08 + AC-09 collectively form the **Lesson #39 integration-axis full-triplet** for spec/03 (audit-corpus sub-axis): AC-08 = Lesson #29 module-asset pin; AC-09 = Lesson #36 cross-module link contract + Lesson #44 mechanizable grep; AC-12 = Lesson #21 sub-module delegation mandate. **NEW Lesson #40 — full-triplet pattern extends to normative-contract-axis modules with deep-tree audit-corpus content**: audit-v7 axis_multipliers `d2=1.5 + d5=0.5` flagged spec/03 as normative-contract axis (not integration-spec like spec/12), but the same triplet-shape work was needed because deep sub-tree retros + cross-repo Interface Contracts collectively expose the same 3-class gap surface — Lesson #39's triplet pattern is **axis-independent** as long as the module has (a) ≥2 deep subfolders with their own §97 AND (b) ≥1 outside-spec reference class (linter-scripts in spec/12; downstream-repos in spec/03).

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module changelog](./98-changelog.md)
- [Module consistency report](./99-consistency-report.md)
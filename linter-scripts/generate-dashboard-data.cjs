#!/usr/bin/env node

/**
 * generate-dashboard-data.cjs
 *
 * Scans the spec/ tree to:
 *   1. Validate all markdown cross-references (broken link detection)
 *   2. Check for required files (00-overview.md, 99-consistency-report.md)
 *   3. Count files per subfolder
 *   4. Compute per-module rubric-v2.0.0 quality credits
 *      (mirrors `linter-scripts/check-tree-health.cjs` Phase 30 rubric)
 *   5. Output a JSON report to spec/dashboard-data.json
 *
 * Rubric (v2.0.0, propagated Phase 34):
 *   Required (60%): 00-overview.md, 99-consistency-report.md
 *   Recommended (25%): 97-acceptance-criteria.md, 98-changelog.md
 *   Quality (15%): §99 ≥30 non-blank lines + Validation History heading
 *                  + File/Module/Document Inventory heading
 *
 * Usage:  node linter-scripts/generate-dashboard-data.cjs [--json] [--quiet]
 */

const fs = require("fs");
const path = require("path");

// ── CLI flags ───────────────────────────────────────────────
const args = process.argv.slice(2);
const jsonOnly = args.includes("--json");
const quiet = args.includes("--quiet");

const SPEC_ROOT = path.resolve(__dirname, "..", "spec");
const ARCHIVE_SEGMENTS = ["_archive", "archive"];

// ── Rubric v2.0.0 (mirrors check-tree-health.cjs Phase 30) ──
const RUBRIC_VERSION = "2.0.0";
const REQUIRED_FILES = ["00-overview.md", "99-consistency-report.md"];
const RECOMMENDED_FILES = ["97-acceptance-criteria.md", "98-changelog.md"];
const RUBRIC_WEIGHTS = { required: 60, recommended: 25, quality: 15 };
const QUALITY_MIN_LINES = 30;
const QUALITY_HISTORY_RE = /^##+\s+(Validation History|Findings|Audit History|Change History)/im;
const QUALITY_INVENTORY_RE = /^##+\s+(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)/im;

// Cross-repo path prefixes that resolve OUTSIDE this repo's spec/ tree
// (e.g., gitmap-v3 sibling repo, monorepo siblings like scripts/, docs/,
// linters-cicd/, eslint-plugins/, spec-slides/). These targets cannot be
// `fs.existsSync()`-checked here because the sibling repo/folder is not in
// the working tree. Treat as intentional external references and exclude
// from broken-link counts.
//
// A target is allowlisted when its resolved path (relative to SPEC_ROOT)
// matches any of these patterns. Add new prefixes as new sibling repos or
// external doc trees are referenced.
const EXTERNAL_REPO_PREFIXES = [
  // gitmap-v3 sibling repo (folders 01-app, 02-app-issues, 03-general live there)
  "01-app/",
  "02-app-issues/",
  "03-general/",
  // monorepo siblings outside spec/ (resolved paths start with ../)
  "../scripts/",
  "../docs/",
  "../linters-cicd/",
  "../eslint-plugins/",
  "../spec-slides/",
  // mem:// virtual filesystem references
  "../mem:/",
];

function isExternalRepoRef(resolvedRel) {
  return EXTERNAL_REPO_PREFIXES.some((p) => resolvedRel.startsWith(p))
    || resolvedRel === "../spec-slides"
    || resolvedRel === "dashboard-data.json";
}

// ── Cross-link waiver allowlist (parity with check-spec-cross-links.py) ─────
// File format: <relpath>:<line>:<target> per line. Lines starting with # ignored.
// Used to suppress documentation-example links (e.g. `[link](../foo)` inside
// prose that demonstrates a forbidden pattern). Keeps dashboard in lockstep
// with the Python CI gate which already honors the same file.
const WAIVER_FILE = path.join(__dirname, "spec-cross-links.allowlist");
const WAIVED_LINKS = new Set();
if (fs.existsSync(WAIVER_FILE)) {
  for (const raw of fs.readFileSync(WAIVER_FILE, "utf8").split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    // Allowlist entries are written relative to repo root (e.g. "spec/foo.md:42:bar"),
    // but our sourceRel is relative to SPEC_ROOT. Strip a leading "spec/" if present
    // so both forms match. Key shape stored: "<source-relpath>:<line>:<target>".
    const normalized = line.startsWith("spec/") ? line.slice(5) : line;
    WAIVED_LINKS.add(normalized);
  }
}

function isWaivedLink(sourceRel, lineNum, target) {
  return WAIVED_LINKS.has(`${sourceRel}:${lineNum}:${target}`);
}

// ── Helpers ─────────────────────────────────────────────────

function isArchivePath(filePath) {
  const segments = filePath.split(path.sep);
  return segments.some((s) => ARCHIVE_SEGMENTS.includes(s.toLowerCase()));
}

function walkMarkdown(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkMarkdown(full));
    } else if (entry.name.endsWith(".md") && !isArchivePath(full)) {
      results.push(full);
    }
  }

  return results;
}

function walkDirs(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && !isArchivePath(full)) {
      results.push(full);
      results.push(...walkDirs(full));
    }
  }

  return results;
}

// ── 1. Broken link detection ────────────────────────────────

const LINK_RE = /\[([^\]]*)\]\((\.[^)]+)\)/g;
// P44: blank inline-code spans before link extraction (parity with
// check-spec-cross-links.py:strip_inline_code). Without this, `[`foo`](./foo)`
// inside narrative text is mis-parsed as a real link, producing
// false-positive broken-link counts (precedent: `./test-foo.sh` example
// pattern in §27 §98 line 501 P102 narrative). Preserves char offsets.
const INLINE_CODE_RE = /(`+)(?:(?!\1).)+?\1/g;
function blankInlineCode(line) {
  return line.replace(INLINE_CODE_RE, (m) => " ".repeat(m.length));
}

function extractLinks(filePath, content) {
  const links = [];
  const lines = content.split("\n");
  let inCodeBlock = false;

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    if (rawLine.trimStart().startsWith("```")) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    const line = blankInlineCode(rawLine);
    let match;
    LINK_RE.lastIndex = 0;
    while ((match = LINK_RE.exec(line)) !== null) {
      const linkTarget = match[2];
      const filePart = linkTarget.split("#")[0];
      if (!filePart) continue;

      links.push({
        Line: i + 1,
        Text: match[1],
        Target: linkTarget,
        FilePart: filePart,
      });
    }
  }

  return links;
}

function validateLinks(mdFiles) {
  const broken = [];
  const externalAllowed = [];
  const waived = [];
  const total = { Checked: 0, Ok: 0, Broken: 0, ExternalAllowed: 0, Waived: 0 };

  for (const filePath of mdFiles) {
    const content = fs.readFileSync(filePath, "utf8");
    const links = extractLinks(filePath, content);
    const sourceRel = path.relative(SPEC_ROOT, filePath);

    for (const link of links) {
      total.Checked++;
      const resolved = path.resolve(path.dirname(filePath), link.FilePart);
      const resolvedRel = path.relative(SPEC_ROOT, resolved);

      if (fs.existsSync(resolved)) {
        total.Ok++;
      } else if (isExternalRepoRef(resolvedRel)) {
        total.ExternalAllowed++;
        externalAllowed.push({
          Source: sourceRel,
          Line: link.Line,
          Target: link.Target,
          Resolved: resolvedRel,
        });
      } else if (isWaivedLink(sourceRel, link.Line, link.Target)) {
        total.Waived++;
        waived.push({
          Source: sourceRel,
          Line: link.Line,
          Target: link.Target,
        });
      } else {
        total.Broken++;
        broken.push({
          Source: sourceRel,
          Line: link.Line,
          Text: link.Text,
          Target: link.Target,
          Resolved: resolvedRel,
        });
      }
    }
  }

  return { Broken: broken, ExternalAllowed: externalAllowed, Waived: waived, Total: total };
}

// ── 2. Required-file checks ────────────────────────────────

function checkRequiredFiles(dirs) {
  const missingOverview = [];
  const missingConsistency = [];

  for (const dir of dirs) {
    const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md"));
    const rel = path.relative(SPEC_ROOT, dir);

    if (files.length === 0) continue;

    const hasOverview = files.includes("00-overview.md");
    const hasConsistency = files.includes("99-consistency-report.md");

    if (!hasOverview && files.length >= 2) {
      missingOverview.push({ Folder: rel, FileCount: files.length });
    }

    if (!hasConsistency && files.length >= 3) {
      missingConsistency.push({ Folder: rel, FileCount: files.length });
    }
  }

  return { MissingOverview: missingOverview, MissingConsistency: missingConsistency };
}

// ── 3. Folder inventory ─────────────────────────────────────

function buildInventory(dirs) {
  const inventory = [];

  for (const dir of dirs) {
    const allEntries = fs.readdirSync(dir, { withFileTypes: true });
    const mdFiles = allEntries.filter(
      (e) => e.isFile() && e.name.endsWith(".md")
    );
    const subDirs = allEntries.filter((e) => e.isDirectory());
    const rel = path.relative(SPEC_ROOT, dir);

    if (mdFiles.length === 0 && subDirs.length === 0) continue;

    inventory.push({
      Folder: rel,
      MdFiles: mdFiles.length,
      Subfolders: subDirs.length,
      HasOverview: mdFiles.some((f) => f.name === "00-overview.md"),
      HasConsistency: mdFiles.some((f) => f.name === "99-consistency-report.md"),
      HasChangelog: mdFiles.some((f) => f.name === "98-changelog.md"),
      HasAcceptance: mdFiles.some((f) => f.name === "97-acceptance-criteria.md"),
      Files: mdFiles.map((f) => f.name).sort(),
    });
  }

  return inventory;
}

// ── 4a. Per-module rubric v2.0.0 quality scoring ────────────

function scoreModuleQuality(modAbsPath) {
  const reportPath = path.join(modAbsPath, "99-consistency-report.md");
  if (!fs.existsSync(reportPath)) {
    return { score: 0, max: 3, hits: [] };
  }
  const text = fs.readFileSync(reportPath, "utf8");
  const nonBlankLines = text.split("\n").filter((l) => l.trim().length > 0).length;
  let score = 0;
  const hits = [];
  if (nonBlankLines >= QUALITY_MIN_LINES) { score += 1; hits.push("depth"); }
  if (QUALITY_HISTORY_RE.test(text)) { score += 1; hits.push("history"); }
  if (QUALITY_INVENTORY_RE.test(text)) { score += 1; hits.push("inventory"); }
  return { score, max: 3, hits };
}

function buildRubricV2(allDirs) {
  // Same module-discovery rules as check-tree-health.cjs:
  // - Top-level numbered folders under spec/
  // - One level of nested folders that have their own 00-overview.md
  const modules = [];
  for (const dir of allDirs) {
    if (dir === SPEC_ROOT) continue;
    const rel = path.relative(SPEC_ROOT, dir);
    if (rel.split(path.sep).length > 2) continue;
    const hasOverview = fs.existsSync(path.join(dir, "00-overview.md"));
    if (rel.includes(path.sep) && !hasOverview) continue;
    const required = REQUIRED_FILES.filter((f) => fs.existsSync(path.join(dir, f))).length;
    const recommended = RECOMMENDED_FILES.filter((f) => fs.existsSync(path.join(dir, f))).length;
    const quality = scoreModuleQuality(dir);
    modules.push({
      Module: rel,
      Required: required,
      RequiredMax: REQUIRED_FILES.length,
      Recommended: recommended,
      RecommendedMax: RECOMMENDED_FILES.length,
      QualityScore: quality.score,
      QualityMax: quality.max,
      QualityHits: quality.hits,
    });
  }
  const totalRequired = modules.reduce((s, m) => s + m.Required, 0);
  const maxRequired = modules.length * REQUIRED_FILES.length;
  const totalRecommended = modules.reduce((s, m) => s + m.Recommended, 0);
  const maxRecommended = modules.length * RECOMMENDED_FILES.length;
  const totalQuality = modules.reduce((s, m) => s + m.QualityScore, 0);
  const maxQuality = modules.length * 3;
  const reqPct = maxRequired ? (totalRequired / maxRequired) * RUBRIC_WEIGHTS.required : 0;
  const recPct = maxRecommended ? (totalRecommended / maxRecommended) * RUBRIC_WEIGHTS.recommended : 0;
  const qPct = maxQuality ? (totalQuality / maxQuality) * RUBRIC_WEIGHTS.quality : 0;
  const score = Math.round(reqPct + recPct + qPct);
  return {
    RubricVersion: RUBRIC_VERSION,
    Weights: RUBRIC_WEIGHTS,
    Score: score,
    Required: { Earned: totalRequired, Max: maxRequired, PctOfTotal: Math.round(reqPct * 10) / 10 },
    Recommended: { Earned: totalRecommended, Max: maxRecommended, PctOfTotal: Math.round(recPct * 10) / 10 },
    Quality: { Earned: totalQuality, Max: maxQuality, PctOfTotal: Math.round(qPct * 10) / 10 },
    ModuleCount: modules.length,
    Modules: modules,
  };
}

// ── 4b. Health score (legacy deduction-based, preserved) ────

function computeHealth(linkResult, requiredFiles, rubricV2) {
  let score = 100;
  const deductions = [];

  if (linkResult.Total.Broken > 0) {
    const d = Math.min(linkResult.Total.Broken * 2, 20);
    score -= d;
    deductions.push(
      `${linkResult.Total.Broken} broken links (-${d})`
    );
  }

  if (requiredFiles.MissingConsistency.length > 0) {
    const d = Math.min(requiredFiles.MissingConsistency.length, 15);
    score -= d;
    deductions.push(
      `${requiredFiles.MissingConsistency.length} missing consistency reports (-${d})`
    );
  }

  if (requiredFiles.MissingOverview.length > 0) {
    const d = Math.min(requiredFiles.MissingOverview.length * 3, 15);
    score -= d;
    deductions.push(
      `${requiredFiles.MissingOverview.length} missing overviews (-${d})`
    );
  }

  // Rubric v2.0.0 is now the authoritative score; legacy kept for back-compat.
  const rubricScore = rubricV2.Score;
  const grade =
    rubricScore >= 95 ? "A+" :
    rubricScore >= 90 ? "A" :
    rubricScore >= 85 ? "B+" :
    rubricScore >= 80 ? "B" :
    rubricScore >= 70 ? "C" :
    rubricScore >= 60 ? "D" : "F";

  return {
    Score: rubricScore,
    Grade: grade,
    RubricVersion: RUBRIC_VERSION,
    Deductions: deductions,
    LegacyScore: Math.max(score, 0),
  };
}

// ── Main ────────────────────────────────────────────────────

function main() {
  const mdFiles = walkMarkdown(SPEC_ROOT);
  const allDirs = [SPEC_ROOT, ...walkDirs(SPEC_ROOT)];

  const linkResult = validateLinks(mdFiles);
  const requiredFiles = checkRequiredFiles(allDirs);
  const inventory = buildInventory(allDirs);
  const rubricV2 = buildRubricV2(allDirs);
  const health = computeHealth(linkResult, requiredFiles, rubricV2);

  const report = {
    Generated: new Date().toISOString().slice(0, 10),
    Health: health,
    RubricV2: rubricV2,
    Links: {
      TotalChecked: linkResult.Total.Checked,
      Ok: linkResult.Total.Ok,
      Broken: linkResult.Total.Broken,
      ExternalAllowed: linkResult.Total.ExternalAllowed,
      ExternalAllowedDetails: linkResult.ExternalAllowed,
      BrokenDetails: linkResult.Broken,
    },
    RequiredFiles: {
      MissingOverview: requiredFiles.MissingOverview,
      MissingConsistency: requiredFiles.MissingConsistency,
    },
    Inventory: {
      TotalFolders: inventory.length,
      TotalMdFiles: mdFiles.length,
      Folders: inventory,
    },
  };

  const outPath = path.join(SPEC_ROOT, "dashboard-data.json");
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + "\n");

  if (jsonOnly) {
    process.stdout.write(JSON.stringify(report, null, 2) + "\n");
    return;
  }

  if (!quiet) {
    console.log("╔══════════════════════════════════════════════════╗");
    console.log("║        SPEC HEALTH DASHBOARD GENERATOR          ║");
    console.log("╚══════════════════════════════════════════════════╝\n");

    console.log(`  Health Score:  ${health.Score}/100 (${health.Grade})  [rubric v${health.RubricVersion}]`);
    console.log(`    └─ Required:    ${rubricV2.Required.Earned}/${rubricV2.Required.Max}  (${rubricV2.Required.PctOfTotal}/${RUBRIC_WEIGHTS.required})`);
    console.log(`    └─ Recommended: ${rubricV2.Recommended.Earned}/${rubricV2.Recommended.Max}  (${rubricV2.Recommended.PctOfTotal}/${RUBRIC_WEIGHTS.recommended})`);
    console.log(`    └─ Quality:     ${rubricV2.Quality.Earned}/${rubricV2.Quality.Max}  (${rubricV2.Quality.PctOfTotal}/${RUBRIC_WEIGHTS.quality})`);
    if (health.Deductions.length > 0) {
      console.log(`    └─ Legacy deductions (LegacyScore=${health.LegacyScore}):`);
      health.Deductions.forEach((d) => console.log(`        · ${d}`));
    }

    console.log(`\n  Files scanned: ${mdFiles.length}`);
    console.log(`  Folders:       ${inventory.length}`);
    console.log(
      `  Links checked: ${linkResult.Total.Checked} (${linkResult.Total.Ok} ok, ${linkResult.Total.Broken} broken)`
    );

    if (linkResult.Broken.length > 0) {
      console.log("\n  ── Broken Links ──────────────────────────────");
      for (const b of linkResult.Broken) {
        console.log(`    ${b.Source}:${b.Line}`);
        console.log(`      → ${b.Target}`);
      }
    }

    if (requiredFiles.MissingConsistency.length > 0) {
      console.log("\n  ── Missing 99-consistency-report.md ──────────");
      for (const m of requiredFiles.MissingConsistency) {
        console.log(`    ${m.Folder}/ (${m.FileCount} files)`);
      }
    }

    if (requiredFiles.MissingOverview.length > 0) {
      console.log("\n  ── Missing 00-overview.md ────────────────────");
      for (const m of requiredFiles.MissingOverview) {
        console.log(`    ${m.Folder}/ (${m.FileCount} files)`);
      }
    }

    console.log(`\n  Output: ${path.relative(process.cwd(), outPath)}`);
  }

  process.exit(linkResult.Total.Broken > 0 ? 1 : 0);
}

main();

#!/usr/bin/env node
/**
 * check-tree-health.cjs
 *
 * Computes spec/ tree health from disk and fails (exit 1) if below threshold.
 * Designed as a CI gate to lock progress and prevent regressions.
 *
 * Metrics (each module folder under spec/ is a unit):
 *   Required (weight 60%):
 *     +1 if 00-overview.md present
 *     +1 if 99-consistency-report.md present
 *   Recommended (weight 25%):
 *     +1 if 97-acceptance-criteria.md present
 *     +1 if 98-changelog.md present
 *   Quality — §99 depth (weight 15%, NEW v2.0.0 / Phase 30):
 *     +1 if 99-consistency-report.md ≥ 30 non-blank lines (substantive content)
 *     +1 if §99 has a "Validation History" or "Findings" section
 *     +1 if §99 has a "File Inventory" or "Module Inventory" or "Top-Level Modules" section
 *
 * Score = required_pct + recommended_pct + quality_pct (max 100)
 *
 * Usage:
 *   node linter-scripts/check-tree-health.cjs            # uses default threshold 75
 *   node linter-scripts/check-tree-health.cjs --min=80   # custom threshold
 *   node linter-scripts/check-tree-health.cjs --strict   # equivalent to --min=100; also fails
 *                                                        # on ANY module with quality < max,
 *                                                        # even if composite still rounds to 100
 *   node linter-scripts/check-tree-health.cjs --report   # print per-module breakdown
 *
 * --strict (Phase 36) converts "100/100" from aspirational to enforced. CI
 * workflows that expect zero regression should pass --strict; default
 * behaviour stays at threshold 75 to avoid breaking ad-hoc local runs.
 */
const fs = require('fs');
const path = require('path');

const SPEC_DIR = path.resolve(__dirname, '..', 'spec');
const ARCHIVE_PREFIX = '_archive';

const args = process.argv.slice(2);
const minArg = args.find((a) => a.startsWith('--min='));
const STRICT = args.includes('--strict');
const MIN_SCORE = STRICT ? 100 : (minArg ? parseInt(minArg.split('=')[1], 10) : 75);
const SHOW_REPORT = args.includes('--report');

const REQUIRED = ['00-overview.md', '99-consistency-report.md'];
const RECOMMENDED = ['97-acceptance-criteria.md', '98-changelog.md'];

// Quality checks for §99 depth (Phase 30 rubric upgrade)
const QUALITY_MIN_LINES = 30;
const QUALITY_HISTORY_RE = /^##+\s+(Validation History|Findings|Audit History|Change History)/im;
const QUALITY_INVENTORY_RE = /^##+\s+(File Inventory|Module Inventory|Top-Level Modules|Document Inventory|Modules)/im;

function listModules(dir, prefix = '') {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (entry.name.startsWith('.')) continue;
    if (entry.name === ARCHIVE_PREFIX) continue;
    const full = path.join(dir, entry.name);
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    out.push({ rel, full });
    // Recurse one level deeper for nested modules
    for (const sub of fs.readdirSync(full, { withFileTypes: true })) {
      if (!sub.isDirectory()) continue;
      if (sub.name.startsWith('.')) continue;
      const subFull = path.join(full, sub.name);
      // Only count as a module if it has its own 00-overview.md
      if (fs.existsSync(path.join(subFull, '00-overview.md'))) {
        out.push({ rel: `${rel}/${sub.name}`, full: subFull });
      }
    }
  }
  return out;
}

function scoreQuality(modPath) {
  const reportPath = path.join(modPath, '99-consistency-report.md');
  if (!fs.existsSync(reportPath)) return { score: 0, max: 3, hits: [] };
  const text = fs.readFileSync(reportPath, 'utf8');
  const nonBlankLines = text.split('\n').filter((l) => l.trim().length > 0).length;
  let score = 0;
  const hits = [];
  if (nonBlankLines >= QUALITY_MIN_LINES) { score += 1; hits.push('depth'); }
  if (QUALITY_HISTORY_RE.test(text)) { score += 1; hits.push('history'); }
  if (QUALITY_INVENTORY_RE.test(text)) { score += 1; hits.push('inventory'); }
  return { score, max: 3, hits };
}

function scoreModule(modPath) {
  const credits = { required: 0, recommended: 0, quality: 0, qualityMax: 3, qualityHits: [], missing: [] };
  for (const f of REQUIRED) {
    if (fs.existsSync(path.join(modPath, f))) credits.required += 1;
    else credits.missing.push(f);
  }
  for (const f of RECOMMENDED) {
    if (fs.existsSync(path.join(modPath, f))) credits.recommended += 1;
  }
  const q = scoreQuality(modPath);
  credits.quality = q.score;
  credits.qualityMax = q.max;
  credits.qualityHits = q.hits;
  return credits;
}

function main() {
  const modules = listModules(SPEC_DIR);
  const maxRequired = modules.length * REQUIRED.length;
  const maxRecommended = modules.length * RECOMMENDED.length;
  const maxQuality = modules.length * 3;

  let totalRequired = 0;
  let totalRecommended = 0;
  let totalQuality = 0;
  const breakdown = [];

  for (const mod of modules) {
    const c = scoreModule(mod.full);
    totalRequired += c.required;
    totalRecommended += c.recommended;
    totalQuality += c.quality;
    breakdown.push({ rel: mod.rel, ...c });
  }

  // Phase 30 rubric: required 60%, recommended 25%, quality 15%
  const requiredPct = (totalRequired / maxRequired) * 60;
  const recommendedPct = (totalRecommended / maxRecommended) * 25;
  const qualityPct = (totalQuality / maxQuality) * 15;
  const score = Math.round(requiredPct + recommendedPct + qualityPct);

  console.log('━━━ Spec Tree Health (rubric v2.0.0) ━━━');
  console.log(`Modules scanned:        ${modules.length}`);
  console.log(`Required files present: ${totalRequired} / ${maxRequired}  (60% weight)`);
  console.log(`Recommended present:    ${totalRecommended} / ${maxRecommended}  (25% weight)`);
  console.log(`§99 quality credits:    ${totalQuality} / ${maxQuality}  (15% weight)`);
  console.log(`Score:                  ${score} / 100`);
  console.log(`Threshold:              ${MIN_SCORE}`);
  console.log('');

  if (SHOW_REPORT) {
    console.log('━━━ Per-module breakdown ━━━');
    for (const b of breakdown.sort((a, b) => (b.missing.length - a.missing.length) || (a.quality - b.quality))) {
      const status = b.missing.length === 0 && b.quality === b.qualityMax ? '✓' : '✗';
      const qualityStr = `q=${b.quality}/${b.qualityMax}` + (b.qualityHits.length ? `[${b.qualityHits.join(',')}]` : '');
      console.log(
        `${status} ${b.rel.padEnd(60)} req=${b.required}/${REQUIRED.length} rec=${b.recommended}/${RECOMMENDED.length} ${qualityStr}` +
          (b.missing.length ? ` missing: ${b.missing.join(', ')}` : '')
      );
    }
    console.log('');
  }

  if (score < MIN_SCORE) {
    console.error(`✗ FAIL: tree health ${score} is below threshold ${MIN_SCORE}`);
    process.exit(1);
  }

  if (STRICT) {
    // Strict mode: also fail on any module that is not at full marks.
    // Composite score can round to 100 while individual modules slip; strict
    // closes that loophole so CI cannot regress silently.
    const imperfect = breakdown.filter(
      (b) => b.missing.length > 0 || b.quality < b.qualityMax
    );
    if (imperfect.length > 0) {
      console.error(`✗ FAIL: --strict mode — ${imperfect.length} module(s) below full marks:`);
      for (const b of imperfect) {
        const gaps = [];
        if (b.missing.length) gaps.push(`missing: ${b.missing.join(', ')}`);
        if (b.quality < b.qualityMax) gaps.push(`quality ${b.quality}/${b.qualityMax}`);
        console.error(`    ${b.rel}  →  ${gaps.join('; ')}`);
      }
      process.exit(1);
    }
    console.log(`✓ PASS: tree health ${score} ≥ threshold ${MIN_SCORE} (strict — all ${modules.length} modules at full marks)`);
    return;
  }

  console.log(`✓ PASS: tree health ${score} ≥ threshold ${MIN_SCORE}`);
}

main();

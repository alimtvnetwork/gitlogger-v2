#!/usr/bin/env node
/**
 * check-lockstep.cjs
 *
 * Phase 40 — Lockstep enforcement gate.
 *
 * Enforces the project memory Core rule:
 *   "Spec edits keep these in lockstep:
 *     §00 banner + §98 changelog row + §99 health/inventory."
 *
 * Static checks per module folder under spec/:
 *
 *   L1. §99 "Updated" date >= §00 "Updated" date
 *       (§99 is the trailing receipt; it cannot be older than what it
 *        certifies. Equal dates are OK — same-day lockstep edit.)
 *
 *   L2. §98 contains a release line whose date >= §00 "Updated" date
 *       (every banner bump must be witnessed in the changelog).
 *
 *   L3. §98 banner "Updated" date >= max(§00, all release-line dates)
 *       (the changelog file's own banner is itself bumped on each edit).
 *
 * Modes:
 *   default  : warn-only; exit 0; useful for incremental adoption.
 *   --strict : exit 1 on any failure; CI gate.
 *   --json   : machine-readable output.
 *
 * Spec: spec/27-spec-toolchain/24-check-lockstep.md
 */

'use strict';

const fs = require('fs');
const path = require('path');

const SPEC_ROOT = path.resolve(__dirname, '..', 'spec');
const args = new Set(process.argv.slice(2));
const STRICT = args.has('--strict');
const JSON_OUT = args.has('--json');

// ── Date parsing ──────────────────────────────────────────────────
// Accept YYYY-MM-DD anywhere on a line. Return ISO date string or null.
const DATE_RE = /(\d{4}-\d{2}-\d{2})/;
function firstDate(line) {
  const m = DATE_RE.exec(line || '');
  return m ? m[1] : null;
}

// "Updated" banner date: first line in file that matches `**Updated:** YYYY-MM-DD`
// or `> **Updated:** YYYY-MM-DD` (blockquote variant).
function bannerUpdated(text) {
  const lines = text.split(/\r?\n/).slice(0, 40);
  for (const ln of lines) {
    // Accept: `**Updated:** 2026-04-26`, `> **Updated:** 2026-04-26`,
    // `Last Updated: 2026-04-26`, `**Generated:** 2026-04-26`.
    if (/Updated\s*:|Generated\s*:/i.test(ln)) {
      const d = firstDate(ln);
      if (d) return d;
    }
  }
  return null;
}

// All release dates in §98: lines like `### 1.2.0 — 2026-04-27`
// Release headings vary by author. Accept any of:
//   ### 1.2.0 — 2026-04-27
//   ## v4.0.0 — 2026-04-26
//   ## [4.1.0] — 2026-04-26
//   ## [2026-03-30] v2.0.0 ...
//   | 3.8.7 | 2026-04-27 | … |     ← table-row format (folder 22)
function releaseDates(text) {
  const out = [];
  for (const ln of text.split(/\r?\n/)) {
    const isHeading = /^#{2,3}\s+/.test(ln);
    const isTableRow = /^\|\s*v?\d+\.\d+\.\d+\s*\|/.test(ln);
    if (!isHeading && !isTableRow) continue;
    const d = firstDate(ln);
    if (!d) continue;
    if (isHeading) {
      const hasVer = /\bv?\d+\.\d+\.\d+\b|\[\d+\.\d+\.\d+\]/.test(ln);
      if (hasVer) out.push(d);
    } else {
      out.push(d);
    }
  }
  return out;
}

function readSafe(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return null; }
}

// ── Walk spec/ for module folders ─────────────────────────────────
// Phase H3 (2026-04-28): exclude `spec/_archive/**` — archived modules are
// frozen by design and lack §98/§99, which formerly produced 3 noisy
// `skip: missing 00/98/99` rows on every run. Codifies the H2 lesson:
// `_archive/` exclusion should be standard for any spec-traversing gate.
function listModules(root) {
  const out = [];
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    const hasOverview = entries.some(e => e.isFile() && e.name === '00-overview.md');
    if (hasOverview) out.push(dir);
    for (const e of entries) {
      if (e.isDirectory() && !e.name.startsWith('.') && e.name !== '_archive') {
        walk(path.join(dir, e.name));
      }
    }
  }
  walk(root);
  return out;
}

// ── Per-module check ──────────────────────────────────────────────
function checkModule(mod) {
  const rel = path.relative(SPEC_ROOT, mod) || '.';
  const findings = [];

  const overview = readSafe(path.join(mod, '00-overview.md'));
  const changelog = readSafe(path.join(mod, '98-changelog.md'));
  const consistency = readSafe(path.join(mod, '99-consistency-report.md'));

  // Modules without §98/§99 are out of scope (not enforced — many leaf
  // index folders intentionally lack changelogs). Only enforce when both
  // §98 and §99 exist alongside §00.
  if (!overview || !changelog || !consistency) {
    return { module: rel, status: 'skip', reason: 'missing 00/98/99', findings: [] };
  }

  const dOverview = bannerUpdated(overview);
  const dChangelog = bannerUpdated(changelog);
  const dConsistency = bannerUpdated(consistency);
  const releases = releaseDates(changelog);

  if (!dOverview) findings.push({ rule: 'L0', severity: 'error', msg: '§00 has no parseable Updated date' });
  if (!dChangelog) findings.push({ rule: 'L0', severity: 'error', msg: '§98 has no parseable Updated date' });
  if (!dConsistency) findings.push({ rule: 'L0', severity: 'error', msg: '§99 has no parseable Updated/Generated date' });

  if (dOverview && dConsistency && dConsistency < dOverview) {
    findings.push({
      rule: 'L1',
      severity: 'error',
      msg: `§99 Updated (${dConsistency}) < §00 Updated (${dOverview}) — consistency report is stale`,
    });
  }

  if (dOverview && releases.length === 0) {
    findings.push({
      rule: 'L2',
      severity: 'error',
      msg: '§98 has zero release entries (### N.N.N — YYYY-MM-DD)',
    });
  } else if (dOverview && releases.length > 0) {
    const latest = releases.sort().slice(-1)[0];
    if (latest < dOverview) {
      findings.push({
        rule: 'L2',
        severity: 'error',
        msg: `§98 latest release (${latest}) < §00 Updated (${dOverview}) — banner bumped without changelog row`,
      });
    }
  }

  if (dChangelog && releases.length > 0) {
    const latest = releases.sort().slice(-1)[0];
    if (dChangelog < latest) {
      findings.push({
        rule: 'L3',
        severity: 'error',
        msg: `§98 banner Updated (${dChangelog}) < latest release (${latest}) — changelog file's own banner stale`,
      });
    }
    if (dOverview && dChangelog < dOverview) {
      findings.push({
        rule: 'L3',
        severity: 'error',
        msg: `§98 banner Updated (${dChangelog}) < §00 Updated (${dOverview})`,
      });
    }
  }

  return {
    module: rel,
    status: findings.length === 0 ? 'pass' : 'fail',
    dates: { overview: dOverview, changelog: dChangelog, consistency: dConsistency, latestRelease: releases.sort().slice(-1)[0] || null },
    findings,
  };
}

// ── Run ───────────────────────────────────────────────────────────
const modules = listModules(SPEC_ROOT);
const results = modules.map(checkModule);

const pass = results.filter(r => r.status === 'pass').length;
const fail = results.filter(r => r.status === 'fail').length;
const skip = results.filter(r => r.status === 'skip').length;
const totalFindings = results.reduce((n, r) => n + r.findings.length, 0);

if (JSON_OUT) {
  console.log(JSON.stringify({
    summary: { modules: modules.length, pass, fail, skip, findings: totalFindings, strict: STRICT },
    results: results.filter(r => r.status === 'fail'),
  }, null, 2));
} else {
  console.log('━━━ Spec Lockstep Gate (Phase 40) ━━━');
  console.log(`Modules scanned : ${modules.length}`);
  console.log(`  pass          : ${pass}`);
  console.log(`  fail          : ${fail}`);
  console.log(`  skip (no §98/§99): ${skip}`);
  console.log(`Findings        : ${totalFindings}`);
  console.log('');
  if (fail > 0) {
    console.log('Failing modules:');
    for (const r of results) {
      if (r.status !== 'fail') continue;
      console.log(`  • ${r.module}`);
      for (const f of r.findings) console.log(`      [${f.rule}] ${f.msg}`);
    }
    console.log('');
  }
  console.log(STRICT
    ? (fail === 0 ? '✓ PASS: lockstep gate (strict)' : `✗ FAIL: ${fail} module(s) drifted (strict)`)
    : (fail === 0 ? '✓ PASS: lockstep gate' : `⚠ WARN: ${fail} module(s) drifted (warn-only — re-run with --strict to enforce)`));
}

process.exit(STRICT && fail > 0 ? 1 : 0);

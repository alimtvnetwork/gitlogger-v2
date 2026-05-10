#!/usr/bin/env node
/**
 * check-mermaid-syntax.mjs
 *
 * Parse every spec/**\/*.mmd file with the mermaid library to catch broken
 * diagram syntax pre-merge. Pure parser invocation — no rendering, no
 * Chromium, no network. Each file must parse cleanly; any parse error
 * fails the gate with the file path + first error line.
 *
 * Locked by AC-SAG-24 in spec/01-spec-authoring-guide/97-acceptance-criteria.md.
 *
 * Usage:
 *   node linter-scripts/check-mermaid-syntax.mjs
 *
 * Exit codes:
 *   0 — all .mmd files parse
 *   1 — one or more parse failures (details printed)
 *   2 — infrastructure failure (mermaid lib missing, no files found, etc.)
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(import.meta.url), '..', '..');
const SPEC_DIR = join(ROOT, 'spec');

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, out);
    else if (entry.endsWith('.mmd')) out.push(p);
  }
  return out;
}

// Mermaid uses DOMPurify which expects a browser-like environment. Provide
// a minimal jsdom + DOMPurify shim so .parse() works under plain Node.
try {
  const { JSDOM } = await import('jsdom');
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.DOMPurify = {
    addHook: () => {},
    removeAllHooks: () => {},
    sanitize: (s) => s,
    isSupported: true,
  };
} catch (e) {
  console.error('✗ jsdom not available (needed to shim mermaid DOM deps):', e.message);
  console.error('  Install with: bun add -d jsdom');
  process.exit(2);
}

let mermaid;
try {
  mermaid = (await import('mermaid')).default;
} catch (e) {
  console.error('✗ mermaid library not available:', e.message);
  console.error('  Install with: bun add -d mermaid');
  process.exit(2);
}

mermaid.initialize({ startOnLoad: false, suppressErrorRendering: true });

const files = walk(SPEC_DIR).sort();
if (files.length === 0) {
  console.error('✗ No .mmd files found under spec/');
  process.exit(2);
}

let pass = 0;
const failures = [];

for (const file of files) {
  const rel = relative(ROOT, file);
  const src = readFileSync(file, 'utf8').trim();
  if (!src) {
    failures.push({ file: rel, error: 'empty file' });
    continue;
  }
  try {
    await mermaid.parse(src);
    pass++;
  } catch (e) {
    // mermaid throws structured errors; extract the useful bit
    const msg = (e && e.message) ? e.message.split('\n').slice(0, 3).join(' | ') : String(e);
    failures.push({ file: rel, error: msg });
  }
}

console.log(`Mermaid syntax check: ${pass}/${files.length} files parsed cleanly`);

if (failures.length > 0) {
  console.error(`\n✗ FAIL: ${failures.length} file(s) with syntax errors:\n`);
  for (const f of failures) {
    console.error(`  ${f.file}`);
    console.error(`    ${f.error}\n`);
  }
  process.exit(1);
}

console.log('✓ PASS: all mermaid diagrams have valid syntax');
process.exit(0);

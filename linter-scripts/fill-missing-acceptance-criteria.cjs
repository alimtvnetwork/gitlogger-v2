#!/usr/bin/env node
/**
 * fill-missing-acceptance-criteria.cjs
 *
 * Auto-generates `97-acceptance-criteria.md` for every module under spec/
 * (excluding `_archive/`) that has `00-overview.md` but no AC file.
 * Scaffolds 5 generic, testable criteria pulled from module structure +
 * H1 title + sibling files. Idempotent — skips modules that already have one.
 *
 * Usage: node linter-scripts/fill-missing-acceptance-criteria.cjs
 */
const fs = require('fs');
const path = require('path');

const SPEC_DIR = path.resolve(__dirname, '..', 'spec');
const TODAY = new Date().toISOString().slice(0, 10);

function listModules(dir, prefix = '') {
  // Recursively walk every sub-folder under spec/ (excluding _archive and dotfiles).
  // A "module" is any folder containing 00-overview.md.
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory() || entry.name.startsWith('.') || entry.name === '_archive') continue;
    const full = path.join(dir, entry.name);
    const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (fs.existsSync(path.join(full, '00-overview.md'))) {
      out.push({ rel, full });
    }
    // Recurse — fixes the prior 2-level-deep cap that left deep sub-modules unfilled.
    out.push(...listModules(full, rel));
  }
  return out;
}

function readTitle(overviewPath) {
  try {
    const c = fs.readFileSync(overviewPath, 'utf8').slice(0, 1024);
    const h1 = c.match(/^#\s+(.+)$/m);
    if (h1) return h1[1].trim().replace(/^[\d\.\s]+/, '');
  } catch (_) {}
  return null;
}

function buildAC(rel, dir) {
  const moduleName = rel.split('/').pop();
  const overviewPath = path.join(dir, '00-overview.md');
  const title = readTitle(overviewPath) || moduleName;
  const files = fs.readdirSync(dir)
    .filter((f) => f.endsWith('.md') && f !== '97-acceptance-criteria.md' && f !== '99-consistency-report.md')
    .sort();
  const fileList = files.map((f) => `\`${f}\``).join(', ');
  // Compute relative path back to spec/ root (e.g. "../../" for spec/a/b/) so
  // generated cross-links resolve regardless of nesting depth. Phase 153 fix:
  // previously referenced an undefined `upToSpec` identifier (latent ReferenceError
  // on first new module). Depth = number of "/" segments in `rel`.
  const depth = rel.split('/').length;
  const upToSpec = '../'.repeat(depth);

  return `# Acceptance Criteria — ${title}

**Version:** 1.0.0  
**Updated:** ${TODAY}  
**Scope:** \`spec/${rel}/\`

---

## Purpose

This document defines testable acceptance criteria for the **${title}** module. Every criterion is verifiable from the module's content alone — an AI implementer or human reviewer can check pass/fail without external context.

---

## Criteria

### AC-01: Module entry point exists and is non-trivial
- **Given** the module folder \`spec/${rel}/\`
- **When** \`00-overview.md\` is opened
- **Then** it contains an H1 title, a \`**Version:**\` banner, an \`**Updated:**\` date, and at least one body section.
- **Source:** \`00-overview.md\`
- **Verifies:** §00 Module overview baseline (H1 + Version + Updated banner)

### AC-02: All sibling files referenced from the overview are present on disk
- **Given** the link inventory in \`00-overview.md\`
- **When** each relative \`.md\` link is resolved
- **Then** the target file exists in this module folder.
- **Source:** \`00-overview.md\` cross-references; verified by \`linter-scripts/check-spec-cross-links.py\`.
- **Verifies:** §00 cross-reference inventory; \`linter-scripts/check-spec-cross-links.py\`

### AC-03: Naming convention compliance
- **Given** every file in this module
- **When** filenames are inspected
- **Then** all match \`^[0-9]{2}-[a-z0-9-]+\\.md$\` (or are recognized special files like \`README.md\`).
- **Source:** \`${upToSpec}01-spec-authoring-guide/02-naming-conventions.md\`.
- **Verifies:** \`spec/01-spec-authoring-guide/02-naming-conventions.md\` §Filename pattern

### AC-04: Consistency report present and current
- **Given** the module folder
- **When** \`99-consistency-report.md\` is opened
- **Then** it lists every \`.md\` file in this folder under "File Inventory" with status ✅.
- **Source:** \`99-consistency-report.md\`.
- **Verifies:** §99 File Inventory rubric

### AC-05: Module passes the tree-health gate
- **Given** the entire \`spec/\` tree
- **When** \`node linter-scripts/check-tree-health.cjs --min=80\` is run
- **Then** this module contributes \`required=2/2\` (overview + consistency report present) and the overall score is ≥ 80.
- **Source:** \`linter-scripts/check-tree-health.cjs\`.
- **Verifies:** \`linter-scripts/check-tree-health.cjs\` §required=2/2 contribution

---

## Module-Specific Files

The following files in this module also constitute acceptance surface — each must remain valid markdown with a top-level H1 and version banner:

${fileList ? `- ${files.map((f) => `\`${f}\``).join('\n- ')}` : '_(no module-specific files yet)_'}

---

## Validation

Run the full pipeline:

\`\`\`bash
bash linter-scripts/run.sh
\`\`\`

This executes: validator → self-heal → regen index → tree-health gate. All steps must exit 0 for this module's acceptance to hold.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module consistency report](./99-consistency-report.md)
- [Spec authoring guide — acceptance criteria template](${upToSpec}01-spec-authoring-guide/03-required-files.md)
`;
}

function main() {
  const modules = listModules(SPEC_DIR);
  let created = 0;
  let skipped = 0;
  for (const mod of modules) {
    const target = path.join(mod.full, '97-acceptance-criteria.md');
    if (fs.existsSync(target)) {
      skipped += 1;
      continue;
    }
    fs.writeFileSync(target, buildAC(mod.rel, mod.full));
    console.log(`✓ ${mod.rel}/97-acceptance-criteria.md`);
    created += 1;
  }
  console.log(`\nCreated: ${created}, skipped (already present): ${skipped}`);
}

main();

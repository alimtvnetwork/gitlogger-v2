#!/usr/bin/env node
/**
 * fill-missing-changelogs.cjs
 *
 * Auto-generates `98-changelog.md` for every module under spec/
 * (excluding `_archive/`) that has `00-overview.md` but no changelog.
 * Idempotent — skips modules that already have one.
 *
 * Usage: node linter-scripts/fill-missing-changelogs.cjs
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
    // Recurse — fixes the prior 2-level-deep cap that left ~17 sub-modules unfilled.
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

function buildChangelog(rel, dir) {
  const moduleName = rel.split('/').pop();
  const title = readTitle(path.join(dir, '00-overview.md')) || moduleName;
  return `# Changelog — ${title}

**Version:** 1.0.0  
**Updated:** ${TODAY}  
**Scope:** \`spec/${rel}/\`

---

## Format

- Versions follow [SemVer](https://semver.org/): MAJOR.MINOR.PATCH.
- Entries are reverse-chronological (newest first).
- Each entry lists: date (YYYY-MM-DD), version, change category, summary.
- Change categories: \`Added\`, \`Changed\`, \`Deprecated\`, \`Removed\`, \`Fixed\`, \`Security\`.

---

## Releases

### 1.0.0 — ${TODAY}
- **Added** baseline module structure (00-overview, 97-acceptance-criteria, 98-changelog, 99-consistency-report).
- **Added** module-specific files per current inventory in \`99-consistency-report.md\`.
- Auto-scaffolded by \`linter-scripts/fill-missing-changelogs.cjs\` as part of root v3.7.x Phase 2c sweep.

---

## Cross-References

- [Module overview](./00-overview.md)
- [Module acceptance criteria](./97-acceptance-criteria.md)
- [Module consistency report](./99-consistency-report.md)
`;
}

function main() {
  const modules = listModules(SPEC_DIR);
  let created = 0;
  let skipped = 0;
  for (const mod of modules) {
    const target = path.join(mod.full, '98-changelog.md');
    if (fs.existsSync(target)) { skipped += 1; continue; }
    fs.writeFileSync(target, buildChangelog(mod.rel, mod.full));
    console.log(`✓ ${mod.rel}/98-changelog.md`);
    created += 1;
  }
  console.log(`\nCreated: ${created}, skipped (already present): ${skipped}`);
}

main();

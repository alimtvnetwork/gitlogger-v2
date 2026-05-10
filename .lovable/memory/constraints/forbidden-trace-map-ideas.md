---
name: Forbidden trace-map enhancements
description: Three trace-map ideas the user has explicitly forbidden — do not propose, scaffold, or implement.
type: constraint
---

# Forbidden trace-map enhancements

The following three ideas were explicitly REJECTED on 2026-04-26. Do not propose them, do not scaffold a spec for them, do not implement them, do not bring them up as "next steps" or "future work" — even in passing. If a future request appears to be edging toward any of them, stop and confirm with the user before proceeding.

## Forbidden idea #1 — Auto-proposer for trace-map.toml entries
- An assistant tool / linter-script that scans code for referenced symbols / endpoints and matches them to AC headings to propose new `[[trace]]` entries.
- Includes any "diff suggester", "AI-assisted trace filler", "AC ↔ symbol matcher", or similar variant.
- **Why forbidden:** user wants trace-map.toml entries to remain hand-curated. Automating proposals is off-limits.

## Forbidden idea #2 — Trace map exported as OpenAPI/Swagger metadata
- Embedding AC links inside OpenAPI/Swagger documents (e.g. `x-trace-ac`, `externalDocs`, vendor extensions, or any other mechanism) so API tooling can jump from endpoint docs to owning ACs.
- Includes generating a derived `openapi-with-trace.yaml`, patching `spec/28-universal-ci-cli/17-openapi-client.yaml`, or adding a generator that injects trace metadata into any API contract.
- **Why forbidden:** user does not want trace data leaking into API contracts.

## Forbidden idea #3 — Endpoint / function name extraction for sub-file trace targets
- Parsing source files to extract REST route handlers, function definitions, or class members so trace-map entries can point to exact endpoints inside a file rather than only whole-file paths.
- Includes AST walkers, regex extractors for `@app.route`, Express `.get(/post)`, FastAPI decorators, Go handlers, PHP route registrations, etc.
- Includes extending the `symbol` field semantics or adding `endpoint`, `route`, `method` columns derived from code.
- **Why forbidden:** user wants the trace-map to stay file-grain (with optional hand-written `symbol`); deeper extraction is off-limits.

## How to apply
- If the user asks for any of the three above, push back and reference this memory file before doing anything.
- Do not list these as "remaining tasks", "future enhancements", or "nice-to-haves" in any session summary.
- This rule overrides any conflicting guidance from earlier sessions.

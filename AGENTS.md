# Agent Instructions

This repository is the **Baseline JSON Integration Kit**. It documents Baseline's public JSON data contract for import payload creation and exported-workbook mapping.

## Your Two Jobs

1. **Create import JSON** from a user's narrative request or source files. Follow [docs/agent-playbook-create-import.md](docs/agent-playbook-create-import.md) and [docs/agentic-property-generation.md](docs/agentic-property-generation.md). Use the `property-generation/` folders as your workspace.
2. **Map exported JSON** extracted from a Baseline Excel export into another system. Follow [docs/agent-playbook-map-export.md](docs/agent-playbook-map-export.md). Extract payloads with `tools/extract-polyglot-json.py`.

## Hard Rules

- Generate **inputs only**. Never include calculated outputs, valuation results, or fields not present in `schemas/`.
- For `% of Line` references, use only the keys documented in [docs/line-reference-options.md](docs/line-reference-options.md) or line IDs defined in the same payload.
- Validate every generated payload before delivering it:

  ```sh
  python tools/validate-import-json.py path/to/payload.json
  ```

  This checks the JSON Schema contract **and** reference integrity (dangling `*_ref` fields and `ref_key` values). Fix only what the validator reports.
- Put assumptions, uncertainties, and notes **outside** the JSON body (e.g. in `property-generation/working-notes/`). JSON does not support comments.
- Do not infer, explain, or attempt to recreate Baseline's calculations. Treat exported `outputs` as read-only reported results.

## File Map

| Path | Purpose |
| --- | --- |
| `schemas/dcf-input-envelope.schema.json` | Top-level import contract |
| `schemas/*.schema.json` | Section schemas |
| `docs/import-guide.md` | Import contract walkthrough |
| `docs/line-reference-options.md` | Allowed `% of Line` reference keys |
| `docs/export-guide.md`, `docs/excel-embedded-json.md` | Exported-workbook extraction and mapping |
| `examples/` | Starter payloads — see `examples/README.md` before validating them |
| `tools/` | Validator and workbook extractor |

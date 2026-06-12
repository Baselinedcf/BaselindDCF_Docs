# Baseline JSON Integration Kit

This kit helps client teams and AI agents create, validate, extract, and map Baseline JSON without exposing Baseline's calculation engine.

Use it for two workflows:

- **Agentic import creation:** turn narrative prompts or source files into schema-valid Baseline JSON that can jump-start model building.
- **Export mapping:** extract JSON from a Baseline Excel export and map the embedded inputs or outputs into downstream databases, reports, or workflow tools.

This kit documents the data contract only. It does not document formulas, calculation order, proprietary assumptions, or engine internals.

## Contents

```text
schemas/              JSON Schema files for model sections and the DCF input envelope
docs/                 Human and agent-readable guides
examples/             Safe starter examples (see examples/README.md)
tools/                Lightweight extraction and validation utilities
property-generation/  Working folders for agentic generation jobs
AGENTS.md             Entry point for AI coding agents
```

## Start Here

1. Read [Import Guide](docs/import-guide.md) to create import JSON.
2. Use [Agentic Property Generation](docs/agentic-property-generation.md) when working in Codex, Claude, ChatGPT, or another agentic coding environment. AI agents should start at [AGENTS.md](AGENTS.md).
3. Use [Agent Playbook: Create Import](docs/agent-playbook-create-import.md) as the agent instruction block.
4. Use [Percent-Of-Line Reference Options](docs/line-reference-options.md) when creating `% of Line` income, expense, CapEx, or hotel operating lines.
5. Use [Sample Portfolio Example](docs/sample-portfolio-generation.md) only as an example multi-property pattern.
6. Validate output with `tools/validate-import-json.py` (schema validation plus reference-integrity checks).
7. Read [Export Guide](docs/export-guide.md) and [Excel Embedded JSON](docs/excel-embedded-json.md) to extract and map exported workbooks.

## Why A Git Repo Instead Of A PDF

A PDF is useful as a static overview, but a Git repo is the safer and more useful format for agentic property generation. The repo keeps the public schemas, examples, source files, generated JSON, validation tools, and revision history together while preserving the boundary around Baseline's calculation engine.

## Contract Scope

The top-level import payload follows this shape:

```json
{
  "project": {},
  "tenants": [],
  "market_leasing": [],
  "recoveries": [],
  "unit_rental": null,
  "hotel": null,
  "dictionaries": {},
  "income": [],
  "expenses": [],
  "capex": [],
  "debt": [],
  "resale_pv": null
}
```

The section schemas live in `schemas/`. The combined top-level schema is `schemas/dcf-input-envelope.schema.json`.

## Safety Boundary

Allowed in this kit:

- field names, types, enums, required fields, and validation ranges,
- plain-language business definitions,
- import and export mapping guidance,
- extraction instructions for embedded Excel JSON,
- examples that show JSON structure.

Not included:

- formulas,
- calculation sequences,
- engine implementation details,
- paired examples designed to infer calculations,
- internal model assurance or source-code commentary.

## Versioning

Schemas in this kit are generated from Baseline's canonical input models and copied here. They are never hand-edited, except that field descriptions may be trimmed for the public kit.

This kit matches Baseline input schema version `1.0`. Import payloads may carry that marker in the optional top-level `schema_version` field. When the product contract changes, the kit is rebuilt from the current generated schemas and the [Changelog](docs/changelog.md) is updated.

## License

See [LICENSE.md](LICENSE.md). This kit is provided for authorized Baseline integration use.

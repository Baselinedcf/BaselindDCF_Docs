# Property Generation Workspace

Use this folder for agentic property-generation jobs.

## Folder Pattern

```text
incoming/
  Drop source files here: rent rolls, operating statements, OMs, budgets, notes, CSVs, or spreadsheets.
working-notes/
  Agent summaries, assumptions, source-data conflicts, and unresolved questions.
outputs/
  Generated Baseline import JSON files.
validation/
  Validator results and repair notes.
```

## Agent Instruction

Create Baseline import JSON from the user's narrative request and files in `incoming/`. Use the schemas in `../schemas/`, the workflow in `../docs/agentic-property-generation.md`, and the playbook in `../docs/agent-playbook-create-import.md`.

Generated JSON must describe inputs only. Do not include formulas, calculated outputs, valuation results, or Baseline calculation-engine details.

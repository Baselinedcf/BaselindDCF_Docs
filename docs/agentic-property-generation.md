# Agentic Property Generation

Use this guide when a user wants to work with an AI assistant in Codex, Claude, ChatGPT, or another coding agent to create Baseline import JSON from narrative instructions or source files.

The recommended delivery format is a Git repository, not a PDF. A repo lets the user and agent work with schemas, examples, validation tools, source files, generated outputs, and change history in one place. A PDF can summarize the workflow, but it should not be the primary agent workspace.

This kit exposes the Baseline JSON input contract only. It does not expose formulas, calculation order, engine internals, proprietary assumptions, or calculated outputs.

## Recommended Repo Layout

Use a small working folder inside the repo for each generation job:

```text
property-generation/
  incoming/
    source files from the user
  working-notes/
    agent summaries, assumptions, unresolved questions
  outputs/
    generated Baseline JSON files
  validation/
    validator results and repair notes
```

The user can drop offering memoranda, rent rolls, trailing financials, budgets, narrative notes, CSVs, spreadsheets, or plain-text instructions into `incoming/`. The agent should read those files, identify the property type, map source facts into the schema, and create one or more import JSON files in `outputs/`.

## Agent Workflow

1. Read the user's narrative request and all files in `incoming/`.
2. Identify the supported Baseline property type.
3. Select the correct property family: commercial, unit rental, or hotel.
4. Read only the relevant schemas from `schemas/`.
5. Draft a source-data summary in `working-notes/`.
6. List assumptions and missing fields separately from JSON.
7. Generate strict schema-valid JSON in `outputs/`.
8. Check `% of Line` references against [Percent-Of-Line Reference Options](line-reference-options.md).
9. Run `tools/validate-import-json.py` against each generated file.
10. Repair only schema or reference issues found by validation.
11. Provide the final JSON path and a short assumption summary.

## Supported Property Families

Commercial property types:

- `office`
- `industrial`
- `industrial_outdoor_storage`
- `retail`

Unit-rental property types:

- `apartment`
- `senior_housing`
- `manufactured_housing`
- `sfr`
- `student_housing`
- `self_storage`

Hotel property types:

- `hotel`
- `resort`
- `extended_stay`

## What The Agent May Generate

The agent may generate:

- project identity, dates, area, property type, and high-level assumptions,
- tenant rent rolls for commercial properties,
- market leasing categories, recovery methods, and reference dictionaries,
- unit-rental unit types, occupancy, rent, turnover, and line items,
- hotel operating assumptions and hotel-specific line items,
- income, expense, capex, debt, and resale input sections where schema-supported,
- concise human-readable assumption notes outside the JSON.

The agent must not generate:

- calculated outputs,
- valuation results presented as engine results,
- formulas or calculation explanations,
- fields not present in the schemas,
- hidden implementation details,
- examples designed to reverse-engineer the calculation engine.

## Narrative Input Pattern

A user can ask for a property without providing files:

```text
Create a realistic Baseline import JSON file for a 145-unit garden apartment property in Raleigh.
Use 2026 as the analysis start year, a 5-year hold, 5% vacancy, 3% expense growth, and simple operating line items.
Keep it schema-valid and do not include calculated outputs.
```

The agent should turn this into a normal import file, making conservative assumptions only where the user has not provided details. Any meaningful assumption should be documented outside the JSON.

## File Drop Pattern

A user can also provide files:

```text
Use the files in property-generation/incoming to create a Baseline import JSON file.
Map the rent roll, operating statement, and budget into the public JSON schema.
Ask only if a required input cannot be inferred safely.
```

The agent should prefer source facts over generic assumptions. If files conflict, the agent should document the conflict in `working-notes/` and choose the most recent or most explicit source unless the user says otherwise.

## Property-Type Mapping Rules

Use commercial modules when the property has tenants, suites, lease terms, market leasing, recoveries, and commercial rent-roll concepts.

Use unit-rental modules when the property is modeled by unit types, homes, beds, sites, or storage units rather than named tenants.

Use hotel modules when the property is modeled by rooms, occupancy, ADR, RevPAR, department revenue, department expenses, undistributed expenses, fixed charges, management fees, reserves, or hotel comps.

Never mix tenant rent-roll modules into unit-rental or hotel workflows unless the current schema and product workflow explicitly support it.

## Validation Boundary

Validation confirms that the generated JSON fits the public schema. It does not confirm investment quality, underwriting correctness, or model output accuracy.

Before delivering any generated property, run:

```sh
python tools/validate-import-json.py property-generation/outputs/example-property.json
```

The final response should include:

- generated file path,
- validation status,
- important assumptions,
- source-data gaps that a human should review.

## Examples

Use [Sample Portfolio Example](sample-portfolio-generation.md) as an example pattern for creating a multi-property demo suite. It is not the only acceptable portfolio, and agents should not force user requests into those exact property names or assumptions.

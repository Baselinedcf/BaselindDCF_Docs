# Agent Playbook: Create Import JSON

Use this playbook when an AI agent receives source property data and must produce Baseline import JSON.

For repo-based workflows where the user provides narrative instructions or drops files into a folder, also use [Agentic Property Generation](agentic-property-generation.md).

## Instructions For The Agent

You are creating a Baseline import payload. Produce strict schema-valid JSON only. Do not add comments inside JSON. Do not include fields that are not present in the provided schemas.

## Steps

1. Read the user's narrative instructions and any provided source files.
2. Identify the property type and property family: commercial, unit rental, or hotel.
3. Read the top-level envelope schema and only the section schemas needed for that property family.
4. Build the `project` object first.
5. Add only the sections relevant to the property family.
6. Preserve source identifiers when available. Otherwise create stable, readable IDs.
7. Ensure references resolve.
8. Use `null` only when the schema permits it.
9. Do not create calculated output fields.
10. For `% of Line` methods, use only documented reference keys from [Percent-Of-Line Reference Options](line-reference-options.md) or user-defined line IDs in the same payload.
11. Validate with `python tools/validate-import-json.py <file>` (schema and reference checks).
12. Return any uncertainty outside the JSON body.

## Source File Handling

When source files are provided, extract facts before drafting JSON:

- property identity, location, type, size, and analysis dates,
- rent roll, unit mix, room count, or other operating inventory,
- in-place revenue and recurring income lines,
- operating expenses, capex, debt, and resale assumptions,
- explicit assumptions supplied by the user.

Prefer source data over generic assumptions. If a required field is missing, make the smallest reasonable assumption and document it outside the JSON, or ask the user when the assumption would materially change the model.

## Multi-Property Mode

When the user asks for a portfolio or multiple properties, create one valid import JSON document per property. Do not force the exact sample portfolio names unless the user asks for that specific demo suite.

Use [Sample Portfolio Example](sample-portfolio-generation.md) only as an example of realistic scale, line-item depth, and property-family coverage.

## Reference Integrity Checks

Check these relationships:

- tenant `market_leasing_category_ref` matches a `market_leasing.market_leasing_category_id`,
- tenant `recovery_method_ref` matches a `recoveries.recovery_method_id`,
- line item inflation references match dictionary growth method IDs,
- `% of Line` references use documented aggregate keys or line IDs in the same payload,
- unit rental category references match dictionary IDs when used.

`tools/validate-import-json.py` checks these relationships automatically and reports each unresolved reference.

## Output Format

When the user asks for JSON, return only the JSON object.

When the user asks for a review, return:

- validation status,
- missing required source data,
- assumptions made,
- fields that should be confirmed by a human.

Keep the review separate from the JSON payload.

## Forbidden Behavior

Do not infer Baseline formulas. Do not compute valuation outputs. Do not include implementation notes. Do not explain how Baseline calculates results.

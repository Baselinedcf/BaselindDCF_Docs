# Import Guide

Use import JSON to create or seed a Baseline property model from external property data. The JSON should describe inputs only. Do not include calculated output fields.

For agentic workflows where a user drops files into a repo folder or gives a narrative prompt, use [Agentic Property Generation](agentic-property-generation.md) together with this guide.

## Top-Level Shape

Use `schemas/dcf-input-envelope.schema.json` as the top-level contract. Each section points to a schema in `schemas/`.

Required:

- `project`

Common optional sections:

- `tenants`
- `market_leasing`
- `recoveries`
- `unit_rental`
- `hotel`
- `dictionaries`
- `income`
- `expenses`
- `capex`
- `debt`
- `resale_pv`

Unknown fields are outside the public contract. Agents should not add fields that are not present in the schemas.

## Property Families

### Commercial

Commercial property types include office, industrial, industrial outdoor storage, and retail.

Typical sections:

- `project`
- `tenants`
- `market_leasing`
- `recoveries`
- `income`
- `expenses`
- `capex`
- `dictionaries`
- `resale_pv`

Use tenant IDs and category IDs consistently. For example, a tenant's `market_leasing_category_ref` should match a `market_leasing_category_id` in `market_leasing`.

### Unit Rental

Unit rental property types include apartment, senior housing, manufactured housing, single-family rental, student housing, and self-storage.

Typical sections:

- `project`
- `unit_rental`
- `dictionaries`
- `income`
- `expenses`
- `capex`
- `resale_pv`

Do not create tenant rent-roll records for unit rental properties unless the schema and product workflow explicitly require them.

### Hotel

Hotel property types include hotel, resort, and extended stay.

Typical sections:

- `project`
- `hotel`
- `resale_pv`

Hotel-specific operating assumptions belong in `hotel`, not in commercial tenant sections.

## Agentic Generation

For a user or agent creating properties from narrative instructions or dropped-in source files, use [Agentic Property Generation](agentic-property-generation.md). That guide explains the recommended Git repo workflow, source-file folder pattern, property-type mapping rules, validation boundary, and output expectations.

The important distinction is that this import guide explains the JSON contract, while the agentic guide explains how to work from source material to validated JSON.

## Values and Nulls

Use `null` only where the schema allows it. If source data is unknown and the field is optional, omit it or set it to `null` when allowed. Do not guess important IDs, dates, rates, or property attributes.

Percentages are represented as decimals where the schema uses numeric rates. For example, 5% is usually represented as `0.05`.

Dates should use ISO-style strings such as `2026-01-01` when a schema field expects a date-like value.

For `% of Line` methods, use [Percent-Of-Line Reference Options](line-reference-options.md). Do not invent `ref_key` values that are not documented there or defined as line IDs in the same payload.

## Validation

Before import, validate the payload:

```sh
python tools/validate-import-json.py examples/commercial-minimal-import.json
```

The validator checks the top-level envelope, each section schema, and reference integrity (`*_ref` fields and `% of Line` `ref_key` values must resolve). It does not calculate model outputs. See [Validation And Errors](validation-and-errors.md).

## Agent Output Rule

When an AI agent is asked to create import JSON, it should return strict JSON only. Any notes, uncertainties, or validation summary should be outside the JSON body.

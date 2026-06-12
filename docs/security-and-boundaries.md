# Security And Boundaries

This kit is designed for integration, not reverse engineering.

## Safe To Share

- generated JSON schemas,
- field names and types,
- enum values,
- required and optional fields,
- safe field descriptions,
- import and export workflow guidance,
- embedded JSON extraction instructions,
- validation tooling,
- minimal examples.

## Do Not Share

- calculation formulas,
- implementation code from the calculation engine,
- formula-adjacent model assurance docs,
- internal source maps of calculation flow,
- paired input/output examples designed to infer calculations,
- proprietary assumptions or decision trees.

## Output Handling

Calculated output fields can be visible because clients need them for reporting and workflow mapping. They should be described as system-produced, read-only values.

Example safe wording:

> `total_pv` is a system-produced valuation result available in exported outputs.

Avoid wording that explains how the value is calculated.

The process for maintaining and publishing this kit is documented in the Baseline product repository, not here.


# Agent Playbook: Map Export JSON

Use this playbook when an AI agent receives embedded JSON from a Baseline Excel export and must map it into another database, report, or workflow.

## Instructions For The Agent

Map fields by name and business meaning. Treat output values as reported results. Do not derive formulas or attempt to recreate Baseline calculations.

## Steps

1. Extract `audit_manifest`, `inputs`, and `outputs` when available.
2. Preserve `schema_version`, `engine_version`, and payload hashes.
3. Identify whether the downstream task needs model inputs, reported outputs, or both.
4. Create a field mapping table from Baseline paths to target fields.
5. Flag unmapped required target fields.
6. Flag Baseline fields with no target destination.
7. Preserve source arrays as arrays unless the target system requires flattening.
8. Do not add unsupported Baseline fields to the extracted JSON.

## Suggested Mapping Table

```text
Baseline path | Target field | Transform | Notes
project.property_name | property_name | copy | Source identity
project.property_type | asset_type | map enum | Confirm target enum names
outputs.valuation.total_pv | valuation_amount | copy | Reported result
outputs.annual_waterfall.noi | annual_noi_series | copy array | Reported result
```

## Read-Only Output Rule

Fields in `outputs` are system-produced. They can be stored, displayed, compared, or summarized. They should not be used as instructions for how to rebuild Baseline's calculation engine.


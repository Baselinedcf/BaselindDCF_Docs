# Export Guide

Baseline Excel exports can carry embedded JSON payloads. These payloads are useful for workflow automation, reporting, audit trails, and migration into other systems.

## Embedded Payloads

An exported workbook may include:

| Payload | Purpose |
| --- | --- |
| `inputs` | Original model input JSON. Use this to recreate, migrate, or map model assumptions. |
| `outputs` | Result/report JSON. Use this for reporting and downstream workflow mapping. |
| `audit_manifest` | Version and hash metadata for the embedded payloads. |

Use `inputs` when the task is to recreate or modify a model. Use `outputs` when the task is to map reported results to another system.

## Extraction

Use the extraction tool:

```sh
python tools/extract-polyglot-json.py path/to/Baseline_Report.xlsx --part inputs
python tools/extract-polyglot-json.py path/to/Baseline_Report.xlsx --part outputs
python tools/extract-polyglot-json.py path/to/Baseline_Report.xlsx --verify
```

The tool reads the workbook's custom XML payloads. Some spreadsheet tools can strip custom XML on re-save, so extract from the original exported workbook whenever possible.

## Mapping Outputs

Output JSON should be mapped by business meaning and field name, not by trying to infer formulas.

Common output areas include:

- `valuation`
- `annual_waterfall`
- `income_lines`
- `expense_lines`
- `capex_lines`
- `tenant_cash_flows`
- `recovery_details`
- `tenant_occupancy`
- `property_occupancy`
- `reversion`
- `hotel_metrics`
- `hotel_waterfall`
- `unit_type_details`

Calculated values are system-produced. Treat them as read-only reported results.

## Lineage Fields

Preserve these fields when available:

- `schema_version`
- `engine_version`
- `audit_manifest.created_at`
- `audit_manifest.parts.inputs.sha256`
- `audit_manifest.parts.outputs.sha256`

These values help downstream systems understand which data contract and engine version produced the export.

## Do Not Recreate Logic

The export payload is not a formula reference. It is a reporting and integration surface. Client systems should store, display, compare, or map the values; they should not attempt to recreate Baseline calculations from this documentation.


# Excel Embedded JSON

Baseline Excel exports are `.xlsx` files that may include machine-readable JSON in addition to visible workbook sheets.

## Payloads

| Name | Description |
| --- | --- |
| `inputs` | Full input payload used to build the model. |
| `outputs` | Report/result payload produced by the engine for the export. |
| `audit_manifest` | Metadata with schema version, creation time, generator, and payload hashes. |

## Where Payloads Live

Primary storage is inside the workbook's Office Open XML package under `customXml/itemN.xml`.

The input payload may also be present in a hidden worksheet named `_baseline_json` as a fallback. Outputs and the manifest are custom-XML only in the current export format.

## Extract With Tool

```sh
python tools/extract-polyglot-json.py report.xlsx
python tools/extract-polyglot-json.py report.xlsx --part inputs
python tools/extract-polyglot-json.py report.xlsx --part outputs
python tools/extract-polyglot-json.py report.xlsx --part audit_manifest
python tools/extract-polyglot-json.py report.xlsx --verify
```

`--verify` compares embedded payload hashes against the audit manifest. This is tamper-evident, not tamper-proof.

## Recommended Workflow

1. Keep the original exported workbook unchanged.
2. Extract and verify `audit_manifest`.
3. Extract `inputs` for model migration or assumption mapping.
4. Extract `outputs` for reporting workflows.
5. Store `schema_version`, `engine_version`, and hashes with downstream records.

## Limitations

- Not every workbook in circulation is guaranteed to include embedded JSON.
- If a workbook is opened and re-saved by tools that strip custom XML, `outputs` and `audit_manifest` may be removed.
- Embedded outputs are reported results, not calculation documentation.


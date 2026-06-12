# Examples

## Import payloads

These are minimal, schema-valid **import** payloads. They pass `tools/validate-import-json.py`:

| File | Property family |
| --- | --- |
| `commercial-minimal-import.json` | Commercial (office) |
| `apartment-minimal-import.json` | Unit rental (apartment) |
| `hotel-minimal-import.json` | Hotel |

## Export shape illustration

`exported-workbook-extraction-shape.json` is **not** an import payload. It illustrates the top-level shape (`inputs`, `outputs`, `audit_manifest`) you get when extracting embedded JSON from a Baseline Excel export with `tools/extract-polyglot-json.py`. It intentionally fails the import validator — do not use it as an import template. See [docs/export-guide.md](../docs/export-guide.md).

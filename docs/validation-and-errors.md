# Validation And Errors

Validate import JSON before attempting to import it into Baseline.

## Local Validation

```sh
python tools/validate-import-json.py examples/commercial-minimal-import.json
```

The validator checks:

- top-level envelope shape,
- known section schemas,
- required fields,
- types,
- enums,
- simple numeric ranges declared by schema,
- reference integrity: `*_ref` fields and `% of Line` `ref_key` values must resolve to IDs defined in the same payload or to documented public aggregate keys.

Reference checks are plain ID matching. Skip them with `--no-check-refs` if needed.

The validator only accepts import payloads. If you point it at extracted exported-workbook JSON (with `outputs` or `audit_manifest` keys), it explains the mismatch instead of validating.

## Common Issues

| Issue | Fix |
| --- | --- |
| Missing `project` | Add a valid `project` object. |
| Unknown top-level key | Remove it unless it is added to the public schema. |
| Invalid enum | Use one of the enum values from the schema. |
| Reference does not resolve | Make referenced IDs match an object in the related section. |
| Percent entered as whole number | Use decimal rate form when the schema expects a rate. |
| Notes embedded in JSON comments | JSON does not support comments. Put notes outside the JSON body. |

## API Errors

If an import reaches the Baseline API and fails validation, the API may return a 422 response. The response usually indicates a missing field, wrong type, unsupported enum, future schema version, or obsolete schema version.

## Agent Guidance

If validation fails, the agent should repair only the invalid fields and should not invent unsupported fields. If source data is insufficient, the agent should ask for the missing value or provide a validation summary outside the JSON.


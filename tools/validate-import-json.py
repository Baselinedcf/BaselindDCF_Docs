#!/usr/bin/env python3
"""Validate a Baseline import JSON payload against the kit schemas.

Validation has two layers:

1. JSON Schema validation against ``schemas/dcf-input-envelope.schema.json``
   (full validation requires the ``jsonschema`` package; without it a basic
   shape check runs instead):

       python -m pip install jsonschema

2. Reference-integrity checks: every ``*_ref`` field and ``% of Line``
   ``ref_key`` must resolve to an ID defined in the same payload or to a
   documented public aggregate key. This is plain ID matching — it does not
   calculate anything.

Usage:

    python tools/validate-import-json.py examples/commercial-minimal-import.json
    python tools/validate-import-json.py payload.json --no-check-refs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


TOP_LEVEL_KEYS = {
    "schema_version",
    "project",
    "tenants",
    "market_leasing",
    "recoveries",
    "unit_rental",
    "hotel",
    "dictionaries",
    "income",
    "expenses",
    "capex",
    "debt",
    "resale_pv",
}

# Public aggregate keys for income/expense/capex `pct_of_line_item` refs.
AGGREGATE_REF_KEYS = {"__EGI__", "__GPR__", "__SCHEDULED_RENT__"}

# Public aggregate keys for hotel `pct_line_refs`.
HOTEL_AGGREGATE_REF_KEYS = {
    "rooms_revenue",
    "total_revenue",
    "total_dept_expense",
    "departmental_profit",
    "gross_operating_profit",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _looks_like_export_payload(payload: dict) -> bool:
    return isinstance(payload, dict) and (
        "outputs" in payload or "audit_manifest" in payload
    )


def _basic_validate(payload: dict, payload_path: Path) -> int:
    errors: list[str] = []
    if not isinstance(payload, dict):
        errors.append("payload must be a JSON object")
    else:
        if "project" not in payload:
            errors.append("missing required top-level key: project")
        unknown = sorted(set(payload) - TOP_LEVEL_KEYS)
        if unknown:
            errors.append(f"unknown top-level keys: {', '.join(unknown)}")
        project = payload.get("project")
        if project is not None and not isinstance(project, dict):
            errors.append("project must be an object")
        for key in ("tenants", "market_leasing", "recoveries", "income", "expenses", "capex", "debt"):
            if key in payload and not isinstance(payload[key], list):
                errors.append(f"{key} must be an array when provided")
        for key in ("unit_rental", "hotel", "dictionaries", "resale_pv"):
            if key in payload and payload[key] is not None and not isinstance(payload[key], dict):
                errors.append(f"{key} must be an object or null when provided")

    if errors:
        print(f"FAIL: {payload_path} failed basic validation.")
        for err in errors:
            print(f"- {err}")
        return 1

    print(
        f"OK: {payload_path} passed basic validation. "
        "Install `jsonschema` for full schema validation."
    )
    return 0


def _dict_ids(dictionaries: dict | None, key: str) -> set[str]:
    if not isinstance(dictionaries, dict):
        return set()
    entries = dictionaries.get(key) or []
    return {e["id"] for e in entries if isinstance(e, dict) and e.get("id")}


def check_references(payload: dict) -> list[str]:
    """Return a list of unresolved-reference error messages.

    Pure ID matching between ``*_ref`` fields, documented aggregate keys,
    and IDs defined in the same payload.
    """
    errors: list[str] = []

    tenants = payload.get("tenants") or []
    market_leasing = payload.get("market_leasing") or []
    recoveries = payload.get("recoveries") or []
    income = payload.get("income") or []
    expenses = payload.get("expenses") or []
    capex = payload.get("capex") or []
    dictionaries = payload.get("dictionaries")
    hotel = payload.get("hotel")

    mlc_ids = {m.get("market_leasing_category_id") for m in market_leasing if isinstance(m, dict)}
    recovery_ids = {r.get("recovery_method_id") for r in recoveries if isinstance(r, dict)}
    income_ids = {i.get("income_line_id") for i in income if isinstance(i, dict)}
    expense_ids = {e.get("expense_line_id") for e in expenses if isinstance(e, dict)}
    mlc_ids.discard(None)
    recovery_ids.discard(None)
    income_ids.discard(None)
    expense_ids.discard(None)

    growth_ids = _dict_ids(dictionaries, "growth_methods")
    renewal_prob_ids = _dict_ids(dictionaries, "renewal_probabilities")
    lc_ids = _dict_ids(dictionaries, "lc_categories")
    ti_ids = _dict_ids(dictionaries, "ti_categories")
    abatement_ids = _dict_ids(dictionaries, "rent_abatements")
    expense_group_ids = _dict_ids(dictionaries, "expense_groups")
    alt_area_ids = _dict_ids(dictionaries, "alternate_property_areas")

    def expect(value, valid: set[str], where: str, target: str) -> None:
        if value is not None and value not in valid:
            errors.append(f"{where}: '{value}' does not match any {target}")

    def check_dictionary_refs(obj: dict, where: str) -> None:
        """Check the dictionary-backed ref fields shared by several sections."""
        for field, value in obj.items():
            if value is None or not isinstance(field, str):
                continue
            if field.endswith("_inflation_ref") or field.endswith("_growth_ref"):
                expect(value, growth_ids, f"{where}.{field}", "dictionaries.growth_methods id")
        expect(obj.get("renewal_probability_ref"), renewal_prob_ids,
               f"{where}.renewal_probability_ref", "dictionaries.renewal_probabilities id")
        expect(obj.get("lc_category_ref"), lc_ids,
               f"{where}.lc_category_ref", "dictionaries.lc_categories id")
        expect(obj.get("ti_category_ref"), ti_ids,
               f"{where}.ti_category_ref", "dictionaries.ti_categories id")
        expect(obj.get("abatement_ref"), abatement_ids,
               f"{where}.abatement_ref", "dictionaries.rent_abatements id")

    # Tenants
    for idx, tenant in enumerate(tenants):
        if not isinstance(tenant, dict):
            continue
        where = f"tenants[{idx}]"
        expect(tenant.get("market_leasing_category_ref"), mlc_ids,
               f"{where}.market_leasing_category_ref", "market_leasing_category_id")
        expect(tenant.get("recovery_method_ref"), recovery_ids,
               f"{where}.recovery_method_ref", "recovery_method_id")
        check_dictionary_refs(tenant, where)

    # Market leasing categories
    for idx, mlc in enumerate(market_leasing):
        if not isinstance(mlc, dict):
            continue
        where = f"market_leasing[{idx}]"
        expect(mlc.get("recovery_ref"), recovery_ids,
               f"{where}.recovery_ref", "recovery_method_id")
        expect(mlc.get("upon_reversion_category_ref"), mlc_ids,
               f"{where}.upon_reversion_category_ref", "market_leasing_category_id")
        check_dictionary_refs(mlc, where)

    # Recovery methods
    for idx, rec in enumerate(recoveries):
        if not isinstance(rec, dict):
            continue
        where = f"recoveries[{idx}]"
        expect(rec.get("flat_inflation_ref"), growth_ids,
               f"{where}.flat_inflation_ref", "dictionaries.growth_methods id")
        expect(rec.get("pro_rata_alternate_area_ref"), alt_area_ids,
               f"{where}.pro_rata_alternate_area_ref", "dictionaries.alternate_property_areas id")
        for ref in rec.get("expense_group_refs") or []:
            expect(ref, expense_group_ids,
                   f"{where}.expense_group_refs", "dictionaries.expense_groups id")

    # Expense group entries reference expense lines
    if isinstance(dictionaries, dict):
        for gidx, group in enumerate(dictionaries.get("expense_groups") or []):
            if not isinstance(group, dict):
                continue
            for eidx, entry in enumerate(group.get("entries") or []):
                if isinstance(entry, dict):
                    expect(entry.get("expense_ref"), expense_ids,
                           f"dictionaries.expense_groups[{gidx}].entries[{eidx}].expense_ref",
                           "expense_line_id")

    # % of Line refs for income / expenses / capex
    line_ref_targets = AGGREGATE_REF_KEYS | income_ids | expense_ids
    for section_name, section in (("income", income), ("expenses", expenses), ("capex", capex)):
        for idx, line in enumerate(section):
            if not isinstance(line, dict):
                continue
            where = f"{section_name}[{idx}]"
            check_dictionary_refs(line, where)
            for ridx, ref in enumerate(line.get("pct_line_item_refs") or []):
                if isinstance(ref, dict):
                    expect(ref.get("ref_key"), line_ref_targets,
                           f"{where}.pct_line_item_refs[{ridx}].ref_key",
                           "documented aggregate key or income/expense line id")

    # Hotel % of Line refs
    if isinstance(hotel, dict):
        assumptions = hotel.get("assumptions") or {}
        if isinstance(assumptions, dict):
            hotel_keys = set(HOTEL_AGGREGATE_REF_KEYS)
            for prefix, group in (
                ("dept", "revenue_departments"),
                ("dept_exp", "departmental_expenses"),
                ("undist", "undistributed_expenses"),
                ("fixed", "fixed_charges"),
            ):
                for item in assumptions.get(group) or []:
                    if isinstance(item, dict) and item.get("name"):
                        hotel_keys.add(f"{prefix}:{item['name']}")
            for group in ("undistributed_expenses", "fixed_charges"):
                for idx, item in enumerate(assumptions.get(group) or []):
                    if not isinstance(item, dict):
                        continue
                    for ridx, ref in enumerate(item.get("pct_line_refs") or []):
                        if isinstance(ref, dict):
                            expect(ref.get("ref_key"), hotel_keys,
                                   f"hotel.assumptions.{group}[{idx}].pct_line_refs[{ridx}].ref_key",
                                   "documented hotel aggregate key or hotel line key")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Baseline import JSON payload.")
    parser.add_argument("payload", help="Path to import JSON.")
    parser.add_argument(
        "--schemas-dir",
        default=str(Path(__file__).resolve().parents[1] / "schemas"),
        help="Directory containing schema files.",
    )
    parser.add_argument(
        "--no-check-refs",
        action="store_true",
        help="Skip reference-integrity checks.",
    )
    args = parser.parse_args()

    payload_path = Path(args.payload)
    schemas_dir = Path(args.schemas_dir)
    schema_path = schemas_dir / "dcf-input-envelope.schema.json"

    try:
        payload = _load_json(payload_path)
    except FileNotFoundError as exc:
        print(f"ERROR: file not found: {exc.filename}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    if _looks_like_export_payload(payload):
        print(
            f"FAIL: {payload_path} looks like an exported-workbook payload "
            "(it has 'outputs' or 'audit_manifest' keys), not an import payload.\n"
            "This validator checks import JSON only. To work with exported "
            "workbook JSON, see docs/export-guide.md."
        )
        return 1

    schema_result: int
    try:
        import jsonschema
        from referencing import Registry, Resource
    except ImportError:
        schema_result = _basic_validate(payload, payload_path)
    else:
        try:
            envelope_schema = _load_json(schema_path)
        except FileNotFoundError as exc:
            print(f"ERROR: file not found: {exc.filename}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid schema JSON: {exc}", file=sys.stderr)
            return 2

        resources = []
        for path in schemas_dir.glob("*.schema.json"):
            schema = _load_json(path)
            resources.append((path.name, Resource.from_contents(schema)))
        registry = Registry().with_resources(resources)

        validator = jsonschema.Draft202012Validator(envelope_schema, registry=registry)
        schema_errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))

        if schema_errors:
            print(f"FAIL: {payload_path} is not schema-valid.")
            for err in schema_errors[:25]:
                loc = "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in err.path)
                print(f"- {loc}: {err.message}")
            if len(schema_errors) > 25:
                print(f"... {len(schema_errors) - 25} more errors")
            schema_result = 1
        else:
            print(f"OK: {payload_path} is schema-valid.")
            schema_result = 0

    if args.no_check_refs:
        return schema_result

    if not isinstance(payload, dict):
        return schema_result or 1

    ref_errors = check_references(payload)
    if ref_errors:
        print(f"FAIL: {payload_path} has unresolved references.")
        for err in ref_errors[:25]:
            print(f"- {err}")
        if len(ref_errors) > 25:
            print(f"... {len(ref_errors) - 25} more errors")
        return 1

    print(f"OK: {payload_path} reference check passed.")
    return schema_result


if __name__ == "__main__":
    raise SystemExit(main())

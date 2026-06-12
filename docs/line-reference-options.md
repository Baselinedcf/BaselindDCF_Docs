# Percent-Of-Line Reference Options

Use this guide when an import JSON line uses a percentage-of-line method and needs a `ref_key`.

The public schemas expose `pct_of_line_item`, `pct_line_item_refs`, and hotel `pct_line_refs`. This page documents the supported public reference keys. Agents should use only these keys or user-defined line IDs from the same import payload.

Do not invent engine-style names such as `effective_gross_income`. For EGI, use the documented public key `__EGI__`.

## Standard Income, Expense, And CapEx Lines

Applies to:

- `income[].input_method: "pct_of_line_item"`
- `expenses[].input_method: "pct_of_line_item"`
- `capex[].input_method: "pct_of_line_item"`

Each reference entry uses this shape:

```json
{
  "ref_key": "__EGI__",
  "flat_pct": 0.03,
  "by_year": false,
  "year_pcts": null
}
```

### Public Aggregate Keys

| Property Family | Supported Aggregate `ref_key` Values |
| --- | --- |
| Commercial | `__EGI__`, `__GPR__` |
| Unit rental | `__EGI__`, `__GPR__`, `__SCHEDULED_RENT__` |
| Hotel generic income lines | `__EGI__`, `__GPR__` when using the shared `income` section; prefer hotel-specific fields for hotel operating lines |

### User-Defined Line IDs

The `ref_key` may also point to a line ID defined in the same import payload:

| Reference Target | Use This ID Field |
| --- | --- |
| Income line | `income[].income_line_id` |
| Expense line | `expenses[].expense_line_id` |

For CapEx lines, use income or expense line IDs as the reference base. Do not reference another CapEx line unless the target product build explicitly supports that workflow.

### Example: Management Fee As 3% Of EGI

For non-hotel or generic income/expense modeling, use:

```json
{
  "expense_line_id": "management_fee",
  "line_item_name": "Management Fee",
  "occupancy_type": "fixed",
  "input_method": "pct_of_line_item",
  "pct_line_item_refs": [
    {
      "ref_key": "__EGI__",
      "flat_pct": 0.03,
      "by_year": false,
      "year_pcts": null
    }
  ]
}
```

Do not use `effective_gross_income` unless a future public schema or guide explicitly publishes it.

## Hotel Operating Line References

Hotel operating lines use hotel-specific references, not the standard `__EGI__` aggregate keys.

Applies to hotel assumptions where `input_method` is one of:

- `pct_of_line`
- `pct_of_line_detailed`
- `detailed_pct_of_line`

Hotel reference entries use `pct_line_refs`:

```json
{
  "ref_key": "total_revenue",
  "flat_pct": 0.03,
  "by_year": false,
  "year_pcts": null
}
```

### Hotel Aggregate Keys

| `ref_key` | Meaning |
| --- | --- |
| `rooms_revenue` | Rooms revenue |
| `total_revenue` | Total hotel revenue |
| `total_dept_expense` | Total departmental expenses |
| `departmental_profit` | Total revenue less departmental expenses |
| `gross_operating_profit` | Departmental profit less undistributed expenses |

### Hotel Dynamic Line Keys

These keys are created from the hotel line names supplied in the same import payload:

| Key Pattern | Reference Target |
| --- | --- |
| `dept:<name>` | `hotel.assumptions.revenue_departments[].name` |
| `dept_exp:<name>` | `hotel.assumptions.departmental_expenses[].name` |
| `undist:<name>` | `hotel.assumptions.undistributed_expenses[].name` |
| `fixed:<name>` | `hotel.assumptions.fixed_charges[].name` |

The `<name>` portion must exactly match the line name in the generated hotel assumptions.

### Hotel Management Fee And Capital Reserve

For hotel management fees and capital reserves, prefer the dedicated hotel fields instead of generic `% of Line` references:

```json
{
  "management_fee": {
    "pct_of_total_revenue": 0.03,
    "basis": "departmental_profit"
  },
  "capital_reserve": {
    "pct_of_total_revenue": 0.04,
    "basis": "total_revenue"
  }
}
```

Allowed `basis` values:

- `total_revenue`
- `departmental_profit`

## Agent Rules

- Use decimal rates, such as `0.03` for 3%.
- Use documented aggregate keys exactly as written.
- Use stable line IDs for generated income and expense lines so references are easy to resolve.
- Keep referenced lines in the same property JSON document.
- Document any assumption outside the JSON.
- If the desired reference base is not listed here, use a direct amount method or ask the user instead of inventing a `ref_key`.

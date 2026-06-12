# Sample Portfolio Example

Use this guide as an example pattern when a user wants an AI assistant or integration script to create a realistic Baseline demo portfolio from scratch. The specific property names and assumptions below are optional. For general narrative or source-file-driven generation, use [Agentic Property Generation](agentic-property-generation.md).

This guide describes input construction only. Do not include calculated outputs, valuation results, formulas, or engine internals in generated JSON.

## Example Portfolio

One possible portfolio is named `Sample` and includes these eight properties:

| Property Type | Sample Name |
| --- | --- |
| Office | Briarwood Office Center (Sample) |
| Industrial | Crossridge Industrial Park (Sample) |
| Apartments | Fairmont Apartments (Sample) |
| Student Housing | Grandview Student Housing (Sample) |
| Manufactured Housing | Highland Manufactured Housing Community (Sample) |
| SFR | Juniper Ridge SFR Community (Sample) |
| Self-Storage | Lakeview Self-Storage (Sample) |
| Hotel | Meridian Hotel (Sample) |

Each generated property should be simple, realistic, and internally consistent. Prefer a few clear line items over a long list of overly precise assumptions.

## Generation Rules

- Use one Baseline JSON document per property.
- Use the user's requested property names. If the user asks for this example suite, use `project.property_name` exactly as listed above.
- Use fictitious addresses and markets. Do not use real client assets or private data.
- Use stable readable IDs such as `sample-office-001`, `mlc_office`, `payroll`, or `1br`.
- Use decimal rate form for percentages, such as `0.03` for 3%.
- Use ISO dates such as `2026-01-01`.
- Include only fields supported by the current public schemas.
- Validate every property payload before packaging or import.
- Do not include calculated outputs in import JSON.

## Shared Project Setup

Use a consistent setup unless the source data says otherwise:

| Field | Suggested Value |
| --- | --- |
| `currency` | `USD` |
| `currency_symbol` | `$` |
| `analysis_start_year` | `2026` |
| `analysis_start_month` | `1` |
| `holding_period_years` | `5` |
| `holding_period_months` | `0` |
| `income_expense_start_method` | `analysis_start` |
| `default_inflation_method` | `constant` |
| `default_inflation_rate` | `0.03` |
| `sale_date_method` | `end_of_holding_period` |
| `reversion_method` | `capitalize_forward_noi` |
| `cost_of_sale_pct` | `0.02` |

Use property-type-appropriate area units:

| Property Type | `area_unit` | Primary Quantity |
| --- | --- | --- |
| Office | `sf` | rentable square feet |
| Industrial | `sf` | rentable square feet |
| Apartment | `units` | apartment units |
| Student Housing | `beds` | beds, with unit counts in `number_of_units` when useful |
| Manufactured Housing | `units` | sites or pads |
| SFR | `units` | homes |
| Self-Storage | `sf` | rentable square feet, plus storage unit count |
| Hotel | `rooms` | room count |

## Suggested Property Assumptions

Use values in these ranges for a realistic but lightweight sample suite. Values should be round-number estimates that make sense against the size, rent, occupancy, and cap-rate assumptions.

| Type | Size | Value Range | Occupancy / Vacancy | Discount Rate | Terminal Cap |
| --- | ---: | ---: | ---: | ---: | ---: |
| Office | 75,000-100,000 SF | $18M-$28M | 10%-15% vacancy | 8.25%-9.00% | 7.25%-8.00% |
| Industrial | 125,000-160,000 SF | $16M-$26M | 4%-7% vacancy | 7.50%-8.25% | 6.25%-6.75% |
| Apartments | 125-175 units | $22M-$38M | 4%-6% vacancy | 7.25%-7.75% | 5.25%-5.75% |
| Student Housing | 350-500 beds | $28M-$48M | 3%-5% vacancy | 7.75%-8.25% | 5.75%-6.25% |
| Manufactured Housing | 150-220 sites | $18M-$32M | 4%-7% vacancy | 7.50%-8.00% | 5.75%-6.25% |
| SFR | 50-80 homes | $16M-$30M | 4%-6% vacancy | 7.75%-8.25% | 5.75%-6.25% |
| Self-Storage | 60,000-85,000 rentable SF | $10M-$18M | 8%-12% vacancy | 7.75%-8.25% | 6.00%-6.75% |
| Hotel | 90-130 rooms | $14M-$24M | 60%-66% occupancy | Use hotel direct-cap fields where supported | 8.00%-8.75% overall cap |

For demonstration samples, avoid creating a large rollover shock in the terminal year. Commercial sample tenants should usually have lease terms that extend beyond the 5-year hold, or the market-leasing assumptions should be strong enough that the forward NOI at sale remains positive.

## Commercial Samples

Use this structure for Office and Industrial:

- `project`
- `tenants`
- `market_leasing`
- `income`
- `expenses`
- `capex`
- `dictionaries`
- `resale_pv`

Recommended tenant setup:

- 3 to 5 tenants.
- Status: `leased_occupied`.
- Lease start: around the analysis start date.
- Lease terms: 84 to 120 months for sample stability.
- Rent type: `per_uom_year`.
- Rent method: `flat_rent`.
- Include one `market_leasing` category referenced by all tenants.

Recommended line items:

| Office Expense Lines | Industrial Expense Lines |
| --- | --- |
| Common Area Maintenance | Real Estate Taxes |
| Real Estate Taxes | Property Insurance |
| Property Insurance | Repairs & Maintenance |
| Utilities | Common Utilities |
| Management Fee | Management Fee |

Include one or two simple income lines such as parking, signage, or trailer parking.

## Unit-Rental Samples

Use this structure for Apartments, Student Housing, Manufactured Housing, SFR, and Self-Storage:

- `project`
- `unit_rental`
- `income`
- `expenses`
- `capex`
- `dictionaries`
- `resale_pv`

Apartment, manufactured housing, and SFR use the apartment-style unit type shape. Set `subtype` to `apartment` inside `unit_rental.unit_types` unless the current schema provides a dedicated subtype for the asset class.

Student housing uses `subtype: "student_housing"` with per-bed rent methods.

Self-storage uses `subtype: "self_storage"` with street rent, in-place rent, churn, and ECRI fields.

Recommended unit-type counts:

| Type | Unit-Type Examples |
| --- | --- |
| Apartments | Studio, 1 BR, 2 BR, 3 BR |
| Student Housing | 2x2, 4x4, 5x5 |
| Manufactured Housing | Standard Site, Premium Site |
| SFR | 3 BR Home, 4 BR Home |
| Self-Storage | 5x5 CC, 5x10 CC, 10x10 Standard, 10x15 Drive-Up, 10x20 Drive-Up |

Recommended expense lines:

- Payroll & Benefits
- Real Estate Taxes
- Property Insurance
- Utilities
- Repairs & Maintenance
- Marketing & Leasing, where relevant
- Management Fee
- General & Administrative

## Hotel Sample

Use the existing hotel/InTown-style data shape for `Meridian Hotel (Sample)`. The hotel sample should include detailed hotel line items rather than only top-line revenue and expense totals.

Use this structure:

- `project`
- `hotel`
- `resale_pv` if supported by the current workflow

Recommended hotel identity:

| Field | Suggested Value |
| --- | --- |
| `property_name` | `Meridian Hotel (Sample)` |
| `property_type` | `hotel` |
| `area_unit` | `rooms` |
| `property_area` | `112` |
| `rooms` | `112` |
| `hotel_type` | `select_service` |
| `str_scale` | `upper_midscale` |

Recommended performance assumptions:

| Field | Suggested Value |
| --- | --- |
| Year 1 occupancy | `0.625` |
| Stabilized occupancy | `0.65` |
| Year 1 ADR | approximately `167.00` |
| ADR growth | approximately 2.5%-3.0% annually |
| Inflation rate | `0.03` |
| Stabilization year | `3` |

Recommended `hotel.assumptions` line-item groups:

| Group | Example Lines |
| --- | --- |
| `revenue_departments` | Food & Beverage, Other Operated, Miscellaneous |
| `departmental_expenses` | Rooms Expense, F&B Expense, Other Operated Expense, Other Income Expense |
| `undistributed_expenses` | A&G, Payroll & Benefits, IT Systems, Sales & Marketing, Franchise Fees, POM, Utilities |
| `fixed_charges` | Property Taxes, Insurance, Other Fixed |
| `management_fee` | 3% of departmental profit, where supported |
| `capital_reserve` | 4% of total revenue, where supported |

The hotel sample may also include `competitive_set`, `sales_comparison`, `cost_approach`, and `direct_cap` when those fields are supported. Keep comps fictitious and clearly generic.

## Packaging The Portfolio

If packaging multiple properties into one importable portfolio file, use the app's current portfolio package extension and format. Current desktop builds may use `.baselinedcf`; newer source code may use `.baselineportfolio`. Match the extension accepted by the target build's import dialog.

The package should contain:

- portfolio name: `Sample`
- portfolio analysis date: `2026-01-01`
- all eight property JSON inputs
- no calculated result requirement for import

After import, each property should behave like a normal user-owned model. Users may keep, edit, or delete the sample portfolio.

## AI Prompt Template

Use this prompt when asking an AI assistant to generate this example portfolio:

```text
Create a Baseline example portfolio named "Sample" using the Baseline JSON Integration Kit schemas.

Generate one valid property JSON input for each of these properties:
- Briarwood Office Center (Sample): office
- Crossridge Industrial Park (Sample): industrial
- Fairmont Apartments (Sample): apartment
- Grandview Student Housing (Sample): student_housing
- Highland Manufactured Housing Community (Sample): manufactured_housing
- Juniper Ridge SFR Community (Sample): sfr
- Lakeview Self-Storage (Sample): self_storage
- Meridian Hotel (Sample): hotel

Rules:
- Use fictitious addresses and realistic but simple assumptions.
- Use one JSON document per property.
- Include only schema-supported input fields.
- Do not include calculated outputs.
- Use stable readable IDs and ensure all _ref fields resolve.
- Use decimal rate form for percentages.
- Keep commercial sample leases stable through the 5-year hold so the forward NOI at sale remains positive.
- For the hotel, include detailed hotel.assumptions line items: revenue departments, departmental expenses, undistributed expenses, fixed charges, management fee, and capital reserve.
- Validate each JSON against the current Baseline schemas before returning it.
```

## Review Checklist

Before delivering a generated sample package:

- Every property has a valid `project` block.
- `project.property_type` matches the intended workflow.
- Commercial tenants reference existing market-leasing categories.
- Unit-rental properties do not include commercial tenant rent rolls.
- Hotel line items are under `hotel.assumptions`, not generic commercial tenant modules.
- All growth, inflation, LC, and recovery references resolve.
- Rates are decimals, not whole-number percentages.
- Commercial lease rollovers do not create obvious terminal-year instability.
- The package imports into the target desktop build.
- A user can open and save at least one property from each family: commercial, unit rental, hotel.

# Changelog

## 0.2.0 — 2026-06-11

Matches Baseline input schema version `1.0` (contract snapshot of 2026-06-11).

- Refreshed all schemas from the current Baseline contract: BOMA fields renamed to `area_remeasurement_*` (`project`, `tenants`), `SizeScheduleEntry` removed (`tenants`), min/max tenant recovery cap fields added (`recoveries`).
- `tools/validate-import-json.py` now also checks reference integrity: dangling `*_ref` fields and undocumented `% of Line` `ref_key` values fail validation. Skip with `--no-check-refs`.
- The validator now detects exported-workbook payloads and explains they are not import payloads.
- `tools/extract-polyglot-json.py` is fully standalone (stdlib only).
- Added `AGENTS.md` / `CLAUDE.md` agent entry points, `examples/README.md`, and `LICENSE.md`.
- Command examples use portable `sh` fences (they run unchanged in PowerShell).
- Removed internal process material from the public docs.

## 0.1.0

- Initial repo-local Baseline JSON Integration Kit.
- Includes portable schema copies, import/export guides, agent playbooks, safe examples, and extraction/validation tools.
- Added sample portfolio generation guidance for creating a realistic eight-property `Sample` portfolio with property-type-specific assumptions and line items.
- Added agentic property generation guidance for repo-based workflows where users provide narrative instructions or source files and agents create any supported property type from the public JSON schemas.
- Added public `% of Line` reference-key documentation for standard income, expense, CapEx, and hotel operating lines.

# Change: Add CSV Export Endpoint

## Status
✅ **Implemented & Tested**

## Summary
Added a production-grade CSV export endpoint (`GET /reports/export/csv`) for the Reports API with streaming, validation, and security hardening.

## What Changed

### Files Modified
- `app/main.py` — Added CSV export endpoint and supporting functions

### Files Created
- `tests/test_csv_export.py` — 5 comprehensive test cases

## Implementation Details

### Features
- **Streaming Response** — Memory-efficient export via `StreamingResponse` and `generate_csv()` generator
- **Field Validation** — `SortField` Enum whitelist prevents invalid sort parameters
- **CSV Injection Protection** — `sanitize_csv()` function prefixes dangerous characters (`=`, `+`, `-`, `@`)
- **Centralized Logic** — `get_filtered_reports()` shared across endpoints eliminates duplication
- **Version Bump** — API version bumped to 0.2.0

### New Endpoint
```
GET /reports/export/csv
Query Parameters:
  - status: ReportStatus (optional) — Filter by status
  - date_from: datetime (optional) — Filter by creation date
  - date_to: datetime (optional) — Filter by creation date
  - sort: SortField (optional, default: created_at) — Sort field (validated Enum)
  - descending: bool (optional, default: true) — Sort direction

Response:
  - Content-Type: text/csv
  - Content-Disposition: attachment; filename=reports.csv
  - Returns all matching rows as CSV (no pagination limit)
```

### Validation & Security
- Sort fields validated against `SortField` Enum (whitelist: created_at, amount, title, status, owner)
- CSV injection protection: `=`, `+`, `-`, `@` prefixes sanitized to `'=`, etc.
- Internal fields excluded: `internal_id`, `owner_email` never exposed

## Acceptance Criteria Met

✅ Returns downloadable CSV file  
✅ Applies same filtering as `/reports` endpoint  
✅ Returns sorted results (valid field)  
✅ Returns HTTP 400 for invalid sort field  
✅ Excludes internal fields from export  
✅ Includes filename `reports.csv` in response  

## Test Coverage

All 5 tests passing:

```
tests/test_csv_export.py::test_csv_export_success PASSED
tests/test_csv_export.py::test_csv_export_filters PASSED
tests/test_csv_export.py::test_invalid_sort_returns_400 PASSED
tests/test_csv_export.py::test_csv_headers_present PASSED
tests/test_csv_export.py::test_internal_fields_hidden PASSED
===================== 5 passed in 0.88s =====================
```

## Branch
- **Feature Branch**: `openspec-work`
- **Base Branch**: `main`
- **Status**: Pushed to GitHub, ready for PR

## Related Files
- Specification: [SPEC_TEMPLATE.md](../../app/SPEC_TEMPLATE.md)
- Implementation: [app/main.py](../../app/main.py)
- Tests: [tests/test_csv_export.py](../../tests/test_csv_export.py)

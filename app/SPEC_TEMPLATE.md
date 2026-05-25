# Spec — Reports CSV export (v0.1)

## What

Add a CSV export endpoint for reports with filtering and sorting support.

## Acceptance criteria

- WHEN the client requests `/reports/export/csv` THE SYSTEM SHALL return a downloadable CSV file.
- WHEN filters are provided THE SYSTEM SHALL apply the same filtering behavior as `/reports`.
- WHEN a valid sort field is provided THE SYSTEM SHALL return sorted results.
- WHEN an invalid sort field is provided THE SYSTEM SHALL return HTTP 400.
- WHEN reports are exported THE SYSTEM SHALL exclude internal fields.
- WHEN the CSV is returned THE SYSTEM SHALL include the filename `reports.csv`.

## Out of scope

- Authentication and authorization
- Database schema changes
- XLSX or PDF export support

## Tests required

- `tests/test_csv_export.py`
  - test_csv_export_success
  - test_csv_export_filters
  - test_invalid_sort_returns_400
  - test_csv_headers_present
  - test_internal_fields_hidden

## Notes

Use StreamingResponse for CSV downloads and reuse existing report query logic.
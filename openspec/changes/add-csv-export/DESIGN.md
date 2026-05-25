# Design — CSV Export Implementation

## Purpose

Document the technical approach for implementing CSV export with production-grade features: streaming, validation, security, and code reuse.

## Requirements

### Requirement: Streaming Response Architecture
The CSV export SHALL use FastAPI's StreamingResponse to yield rows incrementally, not build the entire file in memory.

#### Scenario: Generator-Based Streaming
The implementation SHALL use a generator function `generate_csv(rows)` that:
1. Creates a CSV writer with output buffer
2. Yields header row
3. Yields each data row after writing
4. Clears buffer between yields

This ensures memory usage stays constant regardless of file size.

### Requirement: Centralized Filtering Logic
Filter and sort logic SHALL be shared across `/reports` and `/reports/export/csv` endpoints to eliminate duplication.

#### Scenario: Shared Query Function
A `get_filtered_reports()` function SHALL:
1. Accept status, date_from, date_to, sort, descending parameters
2. Call the existing `reports.query()` function
3. Handle ValueError exceptions by raising HTTPException with HTTP 400

Both endpoints use this function for consistent filtering behavior.

### Requirement: Sort Field Validation via Enum
Sort fields SHALL be validated using a `SortField` enum instead of accepting arbitrary strings.

#### Scenario: SortField Enum
Create `SortField(str, Enum)` with values:
- created_at
- amount
- title
- status
- owner

FastAPI automatically validates query parameters against the enum, returning HTTP 422 (validation error) for invalid values.

### Requirement: CSV Injection Protection
Values that could trigger spreadsheet formula execution SHALL be sanitized.

#### Scenario: Sanitize CSV Values
A `sanitize_csv(value)` function SHALL:
1. Check if value is a string starting with =, +, -, or @
2. Prepend a single quote (') to make it safe
3. Return the value unchanged if no injection risk

This prevents LibreOffice/Excel from interpreting formulas.

### Requirement: Public Field Exclusion
Internal fields (internal_id, owner_email) SHALL never appear in CSV exports.

#### Scenario: Use ReportPublic Model
All rows exported SHALL use `ReportPublic.from_internal(report)` to strip internal fields before CSV writing. This ensures consistency with the HTTP `/reports` endpoint.

### Requirement: Response Headers
The CSV response SHALL include proper headers for browser download.

#### Scenario: Content-Disposition Header
The response SHALL include:
```
Content-Disposition: attachment; filename=reports.csv
Content-Type: text/csv
```

This ensures browsers download the file with the correct name and format.

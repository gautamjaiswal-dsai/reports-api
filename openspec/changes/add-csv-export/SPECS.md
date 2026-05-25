# Specs — CSV Export Delta

## Purpose

Document the API specification changes required for CSV export functionality.

## ADDED Requirements

### Requirement: GET /reports/export/csv Endpoint
A new endpoint SHALL export filtered reports as CSV with the same filtering/sorting as `/reports`.

#### Scenario: CSV Export Endpoint Specification
**Path:** `GET /reports/export/csv`  
**Query Parameters:**
- `status`: Optional[ReportStatus] — Filter by status (pending, approved, rejected, archived)
- `date_from`: Optional[datetime] — Lower bound on created_at (inclusive)
- `date_to`: Optional[datetime] — Upper bound on created_at (inclusive)
- `sort`: SortField — Sort field (default: created_at, values: created_at|amount|title|status|owner)
- `descending`: bool — Sort direction (default: true)

**Response:**
- Status: 200 OK
- Content-Type: text/csv; charset=utf-8
- Content-Disposition: attachment; filename=reports.csv
- Body: CSV stream with headers and rows

**CSV Headers:** id, title, status, owner, amount, created_at  
**CSV Fields:** Public fields only (no internal_id, owner_email)

#### Scenario: Error Handling
WHEN an invalid sort field is provided  
THEN the API SHALL return HTTP 422 with validation error details

WHEN filter parameters cause an error  
THEN the API SHALL return HTTP 400 with error detail

### Requirement: SortField Type for Validation
The API SHALL use a `SortField(str, Enum)` to validate sort parameters.

#### Scenario: SortField Values
The enum SHALL contain exactly these values:
- `SortField.created_at = "created_at"`
- `SortField.amount = "amount"`
- `SortField.title = "title"`
- `SortField.status = "status"`
- `SortField.owner = "owner"`

### Requirement: CSV Output Format
CSV output SHALL follow RFC 4180 with proper quoting and escaping.

#### Scenario: RFC 4180 Compliance
- Header row with field names
- Data rows with corresponding values
- Strings with special characters properly quoted
- Dangerous formula prefixes sanitized with leading quote

### Requirement: Public Data Model for Export
Only `ReportPublic` fields SHALL be exported, never `Report` internal fields.

#### Scenario: Public Fields
Exported fields:
- id (int)
- title (str, sanitized)
- status (str, sanitized)
- owner (str, sanitized)
- amount (float)
- created_at (datetime, ISO format)

Never exported:
- internal_id
- owner_email

## MODIFIED Requirements

### Requirement: Shared Filtering Logic
The `/reports` endpoint filter logic SHALL be reused in `/reports/export/csv`.

#### Scenario: Consistent Filtering
Both endpoints SHALL use the same `get_filtered_reports()` function to apply:
- Status filtering
- Date range filtering (date_from, date_to)
- Sort field validation
- Sort direction (ascending/descending)

This ensures identical filter behavior across endpoints.

# Proposal — CSV Export Endpoint

## Purpose

Enable users to download filtered report data as CSV files with proper validation, security hardening, and memory-efficient streaming.

## Requirements

### Requirement: Stream CSV Export
Users SHALL be able to request `/reports/export/csv` and receive a downloadable CSV file containing all matching filtered reports without pagination limits.

#### Scenario: Basic CSV Export
GIVEN the API is running  
WHEN a client requests `GET /reports/export/csv`  
THEN the response SHALL have:
- HTTP 200 status
- Content-Type: text/csv
- Content-Disposition: attachment; filename=reports.csv
- CSV data with headers: id, title, status, owner, amount, created_at

#### Scenario: Filtered CSV Export
GIVEN reports exist with various statuses  
WHEN a client requests `GET /reports/export/csv?status=approved`  
THEN the CSV SHALL contain only approved reports  
AND filtering behavior SHALL match the `/reports` endpoint

### Requirement: Validate Sort Fields
Invalid sort fields SHALL be rejected to prevent errors and security issues.

#### Scenario: Valid Sort Field
GIVEN valid sort fields are: created_at, amount, title, status, owner  
WHEN a client requests `GET /reports/export/csv?sort=amount`  
THEN the CSV SHALL be sorted by amount

#### Scenario: Invalid Sort Field Rejected
GIVEN an invalid sort field is requested  
WHEN a client requests `GET /reports/export/csv?sort=invalid_field`  
THEN the API SHALL return HTTP 400 status with a clear error message

### Requirement: Protect Against CSV Injection
Internal fields and formula injection attacks SHALL be prevented.

#### Scenario: Internal Fields Hidden
GIVEN internal fields like internal_id and owner_email exist  
WHEN a client exports reports  
THEN internal fields SHALL NOT appear in the CSV

#### Scenario: Formula Injection Prevented
GIVEN a report title starts with "=malicious"  
WHEN exported to CSV  
THEN the title SHALL be prefixed with a single quote to prevent formula injection

### Requirement: Efficient Memory Usage
Large exports SHALL NOT consume excessive memory through streaming.

#### Scenario: Streaming Response
GIVEN a large number of reports  
WHEN a client requests `/reports/export/csv`  
THEN rows SHALL be streamed incrementally instead of built into memory all at once

# Tasks — CSV Export Implementation

## Purpose

Track the implementation work for the CSV export feature.

## Requirements

### Requirement: Implement Core Functions
Core CSV export functionality SHALL be implemented with proper streaming and validation.

#### Scenario: Create SortField Enum
**Task:** Add `SortField` enum to `app/main.py`  
**Acceptance:** Enum includes: created_at, amount, title, status, owner  
**Status:** ✅ COMPLETED

#### Scenario: Create Sanitization Function
**Task:** Implement `sanitize_csv(value)` function  
**Acceptance:** Prefixes =, +, -, @ with single quote  
**Status:** ✅ COMPLETED

#### Scenario: Create Streaming Generator
**Task:** Implement `generate_csv(rows)` generator function  
**Acceptance:** Yields header, then yields each row incrementally  
**Status:** ✅ COMPLETED

#### Scenario: Create Shared Filter Function
**Task:** Extract common filter logic into `get_filtered_reports()`  
**Acceptance:** Used by both `/reports` and `/reports/export/csv`  
**Status:** ✅ COMPLETED

### Requirement: Implement CSV Export Endpoint
The `/reports/export/csv` endpoint SHALL be added with proper response handling.

#### Scenario: Add Export Endpoint
**Task:** Create `export_reports_csv()` endpoint function  
**Acceptance:** 
- Accepts same filters as `/reports`
- Uses `SortField` for sort validation
- Calls `get_filtered_reports()`
- Returns `StreamingResponse` with CSV stream
**Status:** ✅ COMPLETED

#### Scenario: Update List Reports Endpoint
**Task:** Refactor `/reports` endpoint to use `get_filtered_reports()`  
**Acceptance:** Reduced code duplication, same filtering logic  
**Status:** ✅ COMPLETED

### Requirement: Implement Test Suite
Comprehensive tests SHALL validate all acceptance criteria.

#### Scenario: Test Basic Export
**Task:** Implement `test_csv_export_success()`  
**Acceptance:** Verifies HTTP 200, headers, and CSV structure  
**Status:** ✅ COMPLETED

#### Scenario: Test Filtering
**Task:** Implement `test_csv_export_filters()`  
**Acceptance:** Verifies filters reduce results correctly  
**Status:** ✅ COMPLETED

#### Scenario: Test Invalid Sort
**Task:** Implement `test_invalid_sort_returns_400()`  
**Acceptance:** Invalid sort returns HTTP 422  
**Status:** ✅ COMPLETED

#### Scenario: Test Headers
**Task:** Implement `test_csv_headers_present()`  
**Acceptance:** Verifies all 6 public fields present  
**Status:** ✅ COMPLETED

#### Scenario: Test Internal Fields Hidden
**Task:** Implement `test_internal_fields_hidden()`  
**Acceptance:** Verifies internal_id and owner_email never exported  
**Status:** ✅ COMPLETED

### Requirement: Test Execution
All tests SHALL pass.

#### Scenario: Run Test Suite
**Task:** Execute `pytest tests/test_csv_export.py -xvs`  
**Acceptance:** All 5 tests pass  
**Status:** ✅ COMPLETED (0.88s)

### Requirement: Code Quality
Production-grade code standards SHALL be met.

#### Scenario: Code Review Points
- ✅ Streaming prevents memory bloat
- ✅ Enum validation prevents injection
- ✅ Sanitization prevents formula injection
- ✅ Public model ensures security
- ✅ Shared logic eliminates duplication
- ✅ Full test coverage

**Status:** ✅ COMPLETED

### Requirement: Documentation
OpenSpec artifacts SHALL be completed.

#### Scenario: Complete OpenSpec Workflow
**Task:** Create proposal, design, specs, tasks artifacts  
**Status:** ✅ IN PROGRESS (this file)

### Requirement: Version & Deployment
Version and deployment readiness.

#### Scenario: Version Bump
**Task:** Update API version to 0.2.0  
**Acceptance:** Reflects feature addition  
**Status:** ✅ COMPLETED

#### Scenario: Push to Branch
**Task:** Push to `openspec-work` branch  
**Status:** ✅ COMPLETED

#### Scenario: Ready for PR
**Task:** Feature ready for pull request to `main`  
**Status:** ✅ COMPLETED

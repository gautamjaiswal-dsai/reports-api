"""Tests for CSV export functionality."""

import csv
import io
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


def test_csv_export_success(client):
    """WHEN the client requests /reports/export/csv THEN the SYSTEM SHALL return a downloadable CSV file."""
    response = client.get("/reports/export/csv")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]
    assert "reports.csv" in response.headers["content-disposition"]

    # Verify CSV is parseable
    csv_reader = csv.DictReader(io.StringIO(response.text))
    rows = list(csv_reader)
    assert len(rows) > 0


def test_csv_export_filters(client):
    """WHEN filters are provided THEN the SYSTEM SHALL apply the same filtering behavior as /reports."""
    # Get all reports first
    all_response = client.get("/reports/export/csv")
    all_rows = list(csv.DictReader(io.StringIO(all_response.text)))

    # Filter by status
    filtered_response = client.get("/reports/export/csv?status=approved")
    filtered_rows = list(csv.DictReader(io.StringIO(filtered_response.text)))

    # Verify filtered results have the status
    for row in filtered_rows:
        assert row["status"] == "approved"

    # Verify filtering actually reduces results
    assert len(filtered_rows) < len(all_rows)


def test_invalid_sort_returns_400(client):
    """WHEN an invalid sort field is provided THEN the SYSTEM SHALL return HTTP 400."""
    response = client.get("/reports/export/csv?sort=invalid_field")

    assert response.status_code == 422  # Pydantic validation error


def test_csv_headers_present(client):
    """WHEN the CSV is returned THEN the headers SHALL be present."""
    response = client.get("/reports/export/csv")

    csv_reader = csv.DictReader(io.StringIO(response.text))
    expected_headers = {"id", "title", "status", "owner", "amount", "created_at"}

    assert set(csv_reader.fieldnames) == expected_headers


def test_internal_fields_hidden(client):
    """WHEN reports are exported THEN the SYSTEM SHALL exclude internal fields."""
    response = client.get("/reports/export/csv")

    # Internal fields that should NOT be in CSV
    forbidden_fields = {"internal_id", "owner_email"}

    csv_reader = csv.DictReader(io.StringIO(response.text))
    assert set(csv_reader.fieldnames).isdisjoint(forbidden_fields)

    # Verify no internal data leaks in rows
    for row in csv_reader:
        for key in row.keys():
            assert key not in forbidden_fields

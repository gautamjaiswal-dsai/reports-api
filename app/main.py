"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

import csv
import io
from datetime import datetime
from enum import Enum
from typing import Iterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query

app = FastAPI(title="SDD Workshop — Reports API", version="0.2.0")


# Allowed sort fields
class SortField(str, Enum):
    created_at = "created_at"
    amount = "amount"
    title = "title"
    status = "status"
    owner = "owner"


def get_filtered_reports(
    status: ReportStatus | None,
    date_from: datetime | None,
    date_to: datetime | None,
    sort: SortField,
    descending: bool,
):
    """Shared filtering + sorting logic."""
    try:
        return query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort.value,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


def sanitize_csv(value: object) -> object:
    """
    Prevent CSV injection attacks in spreadsheet software.
    """
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(
        None,
        description="Lower bound on created_at (inclusive)",
    ),
    date_to: datetime | None = Query(
        None,
        description="Upper bound on created_at (inclusive)",
    ),
    sort: SortField = Query(
        SortField.created_at,
        description="Sort field",
    ),
    descending: bool = Query(
        True,
        description="Sort descending",
    ),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> ReportListResponse:
    """
    Return paginated public reports.
    """

    rows = get_filtered_reports(
        status=status,
        date_from=date_from,
        date_to=date_to,
        sort=sort,
        descending=descending,
    )

    page = rows[offset : offset + limit]

    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )


def generate_csv(rows) -> Iterator[str]:
    """
    Stream CSV rows efficiently.
    """

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "title",
            "status",
            "owner",
            "amount",
            "created_at",
        ],
    )

    # Header
    writer.writeheader()
    yield output.getvalue()
    output.seek(0)
    output.truncate(0)

    # Rows
    for row in rows:
        public_report = ReportPublic.from_internal(row)

        writer.writerow(
            {
                "id": public_report.id,
                "title": sanitize_csv(public_report.title),
                "status": sanitize_csv(public_report.status),
                "owner": sanitize_csv(public_report.owner),
                "amount": public_report.amount,
                "created_at": public_report.created_at.isoformat(),
            }
        )

        yield output.getvalue()

        output.seek(0)
        output.truncate(0)


@app.get("/reports/export/csv")
def export_reports_csv(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(
        None,
        description="Lower bound on created_at (inclusive)",
    ),
    date_to: datetime | None = Query(
        None,
        description="Upper bound on created_at (inclusive)",
    ),
    sort: SortField = Query(
        SortField.created_at,
        description="Sort field",
    ),
    descending: bool = Query(
        True,
        description="Sort descending",
    ),
) -> StreamingResponse:
    """
    Export filtered reports as downloadable CSV.
    """

    rows = get_filtered_reports(
        status=status,
        date_from=date_from,
        date_to=date_to,
        sort=sort,
        descending=descending,
    )

    return StreamingResponse(
        generate_csv(rows),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=reports.csv"
        },
    )
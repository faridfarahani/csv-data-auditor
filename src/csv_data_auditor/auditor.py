from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class AuditResult:
    file_name: str
    row_count: int
    column_count: int
    columns: tuple[str, ...]
    empty_cells: int
    duplicate_rows: int
    missing_required_columns: tuple[str, ...]


def audit_csv(
    path: str | Path,
    required_columns: Iterable[str] | None = None,
) -> AuditResult:
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames is None:
            raise ValueError("CSV file must contain a header row.")

        columns = tuple(reader.fieldnames)
        rows = list(reader)

    empty_cells = sum(
        1
        for row in rows
        for column in columns
        if not (row.get(column) or "").strip()
    )

    seen: set[tuple[str, ...]] = set()
    duplicate_rows = 0

    for row in rows:
        values = tuple((row.get(column) or "").strip() for column in columns)
        if values in seen:
            duplicate_rows += 1
        else:
            seen.add(values)

    required = tuple(required_columns or ())
    missing_required_columns = tuple(
        column for column in required if column not in columns
    )

    return AuditResult(
        file_name=csv_path.name,
        row_count=len(rows),
        column_count=len(columns),
        columns=columns,
        empty_cells=empty_cells,
        duplicate_rows=duplicate_rows,
        missing_required_columns=missing_required_columns,
    )

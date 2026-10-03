from __future__ import annotations

import argparse

from csv_data_auditor.auditor import audit_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit a CSV file for common data quality issues."
    )
    parser.add_argument("file", help="Path to the CSV file.")
    parser.add_argument(
        "--required",
        nargs="+",
        default=[],
        help="Column names that must exist in the CSV file.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = audit_csv(args.file, required_columns=args.required)

    print(f"File: {result.file_name}")
    print(f"Rows: {result.row_count}")
    print(f"Columns: {result.column_count}")
    print(f"Empty cells: {result.empty_cells}")
    print(f"Duplicate rows: {result.duplicate_rows}")

    if result.missing_required_columns:
        missing = ", ".join(result.missing_required_columns)
        print(f"Missing required columns: {missing}")
    else:
        print("Missing required columns: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

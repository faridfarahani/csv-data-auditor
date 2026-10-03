from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from csv_data_auditor.auditor import audit_csv


class AuditCsvTests(unittest.TestCase):
    def test_counts_rows_empty_cells_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.csv"
            path.write_text(
                "name,email,age\n"
                "Alice,alice@example.com,30\n"
                "Bob,,25\n"
                "Bob,,25\n",
                encoding="utf-8",
            )

            result = audit_csv(path)

            self.assertEqual(result.row_count, 3)
            self.assertEqual(result.column_count, 3)
            self.assertEqual(result.columns, ("name", "email", "age"))
            self.assertEqual(result.empty_cells, 2)
            self.assertEqual(result.duplicate_rows, 1)


    def test_rejects_csv_without_header(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.csv"
            path.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "header row"):
                audit_csv(path)

    def test_reports_missing_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.csv"
            path.write_text(
                "name,email\n"
                "Alice,alice@example.com\n",
                encoding="utf-8",
            )

            result = audit_csv(
                path,
                required_columns=["name", "email", "age"],
            )

            self.assertEqual(result.missing_required_columns, ("age",))

if __name__ == "__main__":
    unittest.main()

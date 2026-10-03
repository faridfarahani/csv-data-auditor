# CSV Data Auditor

A small Python CLI tool for checking common CSV data quality issues.

## Features

- Count rows and columns
- Detect empty cells
- Detect duplicate rows
- Read UTF-8 CSV files with headers
- Simple command-line interface

## Usage

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m csv_data_auditor.cli .\samples\customers.csv
```

Example output:

```text
File: customers.csv
Rows: 4
Columns: 3
Empty cells: 3
Duplicate rows: 1
```

## Tests

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

## Requirements

- Python 3.10 or newer
- No third-party runtime dependencies

## Required columns

You can check whether specific columns exist in the CSV file:

```powershell
python -m csv_data_auditor.cli .\samples\customers.csv --required name email age id
```

Example:

```text
Missing required columns: id
```

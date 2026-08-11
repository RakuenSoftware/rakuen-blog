"""CSV ingest helpers."""

import csv
import io

from app.money import parse_amount


def parse_rows(text):
    """Parse CSV text while preserving quoted commas and newlines."""
    return list(csv.reader(io.StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        if not row:
            continue
        total += parse_amount(row[index])
    return total

"""CSV ingest."""

import csv
from io import StringIO

from app.money import parse_amount


def parse_rows(text):
    return list(csv.reader(StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    rows = iter(row for row in parse_rows(text) if row)
    next(rows, None)
    for row in rows:
        total += parse_amount(row[index])
    return total

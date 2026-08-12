"""CSV ingest helpers."""

import csv
import io


def parse_rows(text):
    """Parse CSV text according to the standard quoting rules."""
    return list(csv.reader(io.StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

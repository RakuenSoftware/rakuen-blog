"""CSV ingest helpers."""

import csv
import io


def parse_rows(text):
    """Parse comma-separated rows, including quoted and multiline fields."""
    source = io.StringIO(text.strip(), newline="")
    return list(csv.reader(source))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

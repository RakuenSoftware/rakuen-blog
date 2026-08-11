"""CSV ingest helpers."""

import csv
import io


def parse_rows(text):
    """Parse CSV text while honoring quoting and embedded newlines."""
    with io.StringIO(text.strip(), newline="") as stream:
        return list(csv.reader(stream))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

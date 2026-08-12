"""CSV ingest."""
import csv
from io import StringIO


def parse_rows(text):
    return list(csv.reader(StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

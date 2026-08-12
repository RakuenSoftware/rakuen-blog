"""CSV ingest."""
import csv
from io import StringIO

from app.money import parse_amount


def parse_rows(text):
    return [row for row in csv.reader(StringIO(text, newline="")) if row]


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += parse_amount(row[index])
    return total

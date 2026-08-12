"""Helpers for ingesting CSV exports."""
import csv
import io

from app.money import parse_amount


def parse_rows(text):
    """Parse CSV text while honoring quoting and embedded newlines."""
    # A UTF-8 BOM is commonly left at the start after decoding uploaded files.
    if text.startswith("\ufeff"):
        text = text[1:]
    return list(csv.reader(io.StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    rows = [row for row in parse_rows(text) if row and any(cell.strip() for cell in row)]
    for row in rows[1:]:
        total += parse_amount(row[index].strip())
    return total

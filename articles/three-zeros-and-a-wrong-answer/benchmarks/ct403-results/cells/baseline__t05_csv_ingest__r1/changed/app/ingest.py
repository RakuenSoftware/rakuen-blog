"""Helpers for reading uploaded CSV files."""

import csv
import io


def parse_rows(text):
    """Parse CSV text according to the standard CSV quoting rules.

    Passing the complete stream to :mod:`csv` is important: a quoted field may
    contain both commas and newlines.  ``newline=""`` also lets the reader
    handle files produced on Windows without leaving carriage returns in
    fields.
    """
    return list(csv.reader(io.StringIO(text, newline="")))


def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

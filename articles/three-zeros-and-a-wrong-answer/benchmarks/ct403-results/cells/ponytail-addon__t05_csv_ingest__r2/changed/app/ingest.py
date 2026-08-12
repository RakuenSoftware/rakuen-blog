"""CSV ingest."""
import csv
import io


def parse_rows(text):
    return list(csv.reader(io.StringIO(text, newline="")))

def sum_column(text, index):
    total = 0.0
    for row in parse_rows(text)[1:]:
        total += float(row[index])
    return total

import unittest

from app.ingest import parse_rows, sum_column


class CsvIngestTests(unittest.TestCase):
    def test_parse_rows_honors_quoted_fields(self):
        text = 'description,notes,amount\r\n"Large, blue widget","first line\nsecond line",10.50\r\n'

        self.assertEqual(
            parse_rows(text),
            [
                ["description", "notes", "amount"],
                ["Large, blue widget", "first line\nsecond line", "10.50"],
            ],
        )

    def test_sum_column_handles_accounting_thousands_separators(self):
        text = 'description,amount\nWidget,"1,200.50"\nService,49.50\n'

        self.assertEqual(sum_column(text, 1), 1250.0)

    def test_sum_column_ignores_blank_records(self):
        text = "description,amount\nWidget,10\n\nService,20\n"

        self.assertEqual(sum_column(text, 1), 30.0)


if __name__ == "__main__":
    unittest.main()

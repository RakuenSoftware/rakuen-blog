import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_parse_rows_handles_quoted_fields(self):
        text = (
            'description,notes,amount\r\n'
            '"Consulting, July","first line\r\nsecond ""quoted"" line",123.45\r\n'
        )

        self.assertEqual(
            parse_rows(text),
            [
                ["description", "notes", "amount"],
                [
                    "Consulting, July",
                    'first line\r\nsecond "quoted" line',
                    "123.45",
                ],
            ],
        )

    def test_sum_column_handles_quoted_thousands_and_blank_rows(self):
        text = 'description,amount\n"Consulting, July","1,234.50"\n\nHosting,10.25\n'

        self.assertEqual(sum_column(text, 1), 1244.75)


if __name__ == "__main__":
    unittest.main()

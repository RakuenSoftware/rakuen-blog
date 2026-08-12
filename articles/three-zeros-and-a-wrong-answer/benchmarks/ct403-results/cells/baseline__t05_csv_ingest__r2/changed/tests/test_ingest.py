import unittest

from app.ingest import parse_rows, sum_column


class CsvIngestTests(unittest.TestCase):
    def test_parse_rows_honors_csv_quoting(self):
        text = 'description,amount\n"Widget, large",12.50\n"Say ""hello""",2.50'

        self.assertEqual(
            parse_rows(text),
            [
                ["description", "amount"],
                ["Widget, large", "12.50"],
                ['Say "hello"', "2.50"],
            ],
        )

    def test_parse_rows_supports_newlines_inside_fields(self):
        text = 'description,amount\r\n"first line\r\nsecond line",10\r\n'

        self.assertEqual(
            parse_rows(text),
            [["description", "amount"], ["first line\r\nsecond line", "10"]],
        )

    def test_sum_column_with_quoted_commas_in_other_fields(self):
        text = 'description,amount\n"Widget, large",12.50\nSmall widget,2.50'

        self.assertEqual(sum_column(text, 1), 15.0)


if __name__ == "__main__":
    unittest.main()

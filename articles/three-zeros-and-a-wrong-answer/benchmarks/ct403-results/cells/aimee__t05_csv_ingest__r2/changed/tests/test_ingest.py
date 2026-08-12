import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_parse_rows_honors_csv_quoting(self):
        text = 'description,amount\r\n"Widget, large",12.50\r\n'

        self.assertEqual(
            parse_rows(text),
            [["description", "amount"], ["Widget, large", "12.50"]],
        )

    def test_parse_rows_handles_multiline_and_escaped_quotes(self):
        text = 'description,amount\n"First line\nSecond ""quoted"" line",7.25\n'

        self.assertEqual(
            parse_rows(text),
            [
                ["description", "amount"],
                ['First line\nSecond "quoted" line', "7.25"],
            ],
        )

    def test_sum_column_uses_parsed_csv_columns(self):
        text = 'description,amount\n"Widget, large",12.50\nSmall widget,7.25\n'

        self.assertEqual(sum_column(text, 1), 19.75)

    def test_parse_rows_ignores_surrounding_blank_lines(self):
        self.assertEqual(parse_rows("\nname,amount\nwidget,1.00\n\n"), [
            ["name", "amount"],
            ["widget", "1.00"],
        ])


if __name__ == "__main__":
    unittest.main()

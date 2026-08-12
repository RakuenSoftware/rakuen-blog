import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_parse_rows_preserves_quoted_fields(self):
        text = 'description,amount\r\n"Widget, large",12.50\r\n'

        self.assertEqual(
            parse_rows(text),
            [["description", "amount"], ["Widget, large", "12.50"]],
        )

    def test_sum_column_handles_quoted_commas_in_earlier_columns(self):
        text = 'description,amount\n"Widget, large",12.50\n"Widget, small",7.50'

        self.assertEqual(sum_column(text, 1), 20.0)

    def test_parse_rows_handles_escaped_quotes_and_multiline_fields(self):
        text = 'description,amount\n"A ""special""\nwidget",5.00\n'

        self.assertEqual(
            parse_rows(text),
            [["description", "amount"], ['A "special"\nwidget', "5.00"]],
        )


if __name__ == "__main__":
    unittest.main()

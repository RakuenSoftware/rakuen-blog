import unittest

from app.ingest import parse_rows, sum_column


class CsvIngestTests(unittest.TestCase):
    def test_parses_quoted_commas_and_escaped_quotes(self):
        text = 'customer,amount\r\n"Widgets, Inc.",10\r\n"A ""quoted"" name",20\r\n'

        self.assertEqual(
            parse_rows(text),
            [
                ["customer", "amount"],
                ["Widgets, Inc.", "10"],
                ['A "quoted" name', "20"],
            ],
        )
        self.assertEqual(sum_column(text, 1), 30.0)

    def test_parses_newlines_inside_quoted_fields(self):
        text = 'description,amount\n"first line\nsecond line",12.50\nplain,7.50\n'

        self.assertEqual(
            parse_rows(text)[1], ["first line\nsecond line", "12.50"]
        )
        self.assertEqual(sum_column(text, 1), 20.0)


if __name__ == "__main__":
    unittest.main()

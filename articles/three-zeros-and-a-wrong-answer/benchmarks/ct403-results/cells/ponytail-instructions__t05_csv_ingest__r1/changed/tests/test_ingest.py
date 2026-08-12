import unittest

from app.ingest import parse_rows, sum_column


class IngestTest(unittest.TestCase):
    def test_quoted_fields_do_not_shift_columns_or_split_rows(self):
        text = 'description,amount\r\n"Widgets, large",12.50\r\n"Two\nlines",7.25\r\n\r\n'

        self.assertEqual(parse_rows(text)[1], ["Widgets, large", "12.50"])
        self.assertEqual(sum_column(text, 1), 19.75)


if __name__ == "__main__":
    unittest.main()

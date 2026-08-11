import unittest

from app.ingest import parse_rows, sum_column


class IngestTest(unittest.TestCase):
    def test_quoted_fields(self):
        text = 'description,amount\r\n"large, \"\"deluxe\"\" widget",12.50\r\n"two\nlines",7.50\r\n'

        self.assertEqual(parse_rows(text)[1][0], 'large, "deluxe" widget')
        self.assertEqual(parse_rows(text)[2][0], "two\nlines")
        self.assertEqual(sum_column(text, 1), 20.0)


if __name__ == "__main__":
    unittest.main()

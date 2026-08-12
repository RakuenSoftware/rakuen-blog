import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_quoted_fields_keep_their_columns(self):
        text = 'description,amount\r\n"Widgets, large",10.25\r\n"Widgets, small",2.75\r\n'

        self.assertEqual(sum_column(text, 1), 13.0)

    def test_quoted_fields_can_span_lines(self):
        text = 'description,amount\n"First line\nsecond line",4.50\n'

        self.assertEqual(parse_rows(text)[1], ["First line\nsecond line", "4.50"])


if __name__ == "__main__":
    unittest.main()

import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_quoted_fields(self):
        text = 'description,amount\r\n"Consulting, phase 1",10.25\r\n"Multi-line\nwork",20.50\r\n'

        self.assertEqual(parse_rows(text)[1][0], "Consulting, phase 1")
        self.assertEqual(parse_rows(text)[2][0], "Multi-line\nwork")
        self.assertEqual(sum_column(text, 1), 30.75)


if __name__ == "__main__":
    unittest.main()

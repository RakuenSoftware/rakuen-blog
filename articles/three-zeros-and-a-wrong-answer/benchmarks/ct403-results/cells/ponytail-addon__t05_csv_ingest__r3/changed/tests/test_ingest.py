import unittest

from app.ingest import parse_rows, sum_column


class IngestTest(unittest.TestCase):
    def test_real_world_quoted_fields(self):
        text = 'description,amount\n"Consulting, phase 1","1,234.50"\n"Two\ndays",5.50\n\n'

        self.assertEqual(parse_rows(text)[2], ["Two\ndays", "5.50"])
        self.assertEqual(sum_column(text, 1), 1240.0)


if __name__ == "__main__":
    unittest.main()

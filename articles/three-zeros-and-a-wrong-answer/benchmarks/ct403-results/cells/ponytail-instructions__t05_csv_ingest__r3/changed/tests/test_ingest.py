import unittest

from app.ingest import parse_rows, sum_column


class IngestTests(unittest.TestCase):
    def test_quoted_commas_and_newlines(self):
        text = (
            "\r\n"
            "date,description,amount\r\n"
            '2026-08-01,"Consulting, August","1,234.50"\r\n'
            '2026-08-02,"Rush\nwork",-34.50\r\n'
            "\r\n"
        )

        self.assertEqual(parse_rows(text)[3][1], "Rush\nwork")
        self.assertEqual(sum_column(text, 2), 1200.0)


if __name__ == "__main__":
    unittest.main()

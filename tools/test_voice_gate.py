from __future__ import annotations

import unittest

from tools.voice_gate import prose_without_code_or_tables


class ProseExtractionTests(unittest.TestCase):
    def test_figure_keeps_only_its_caption(self) -> None:
        body = """Before.

<figure class="sg-figure"><input value="very noisy"><div class="sg-figure__tabs">Chart Raw data</div><svg><text>chart words</text></svg><div class="sg-figure__legend">E2B 12B</div><table><tr><td>raw words</td></tr></table><figcaption>Measured <strong>result</strong>.</figcaption></figure>

After.
"""

        self.assertEqual(
            prose_without_code_or_tables(body),
            "Before.\n\nMeasured  result .\n\nAfter.",
        )

    def test_multiple_figures_do_not_consume_intervening_prose(self) -> None:
        body = """<figure class="sg-figure"><figcaption>First.</figcaption></figure>

Keep a < b intact.

<figure class="sg-figure"><figcaption>Second.</figcaption></figure>"""

        self.assertEqual(
            prose_without_code_or_tables(body),
            "First.\n\nKeep a < b intact.\n\nSecond.",
        )


if __name__ == "__main__":
    unittest.main()

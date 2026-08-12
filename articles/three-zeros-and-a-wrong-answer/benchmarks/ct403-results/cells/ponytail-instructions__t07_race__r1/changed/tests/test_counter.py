import threading
import unittest

from app import counter


class CounterTest(unittest.TestCase):
    def test_concurrent_increments_are_not_lost(self):
        counter.reset()
        workers = 20
        increments = 1_000

        threads = [
            threading.Thread(
                target=lambda: [counter.increment("busy-page") for _ in range(increments)]
            )
            for _ in range(workers)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(counter.get("busy-page"), workers * increments)


if __name__ == "__main__":
    unittest.main()

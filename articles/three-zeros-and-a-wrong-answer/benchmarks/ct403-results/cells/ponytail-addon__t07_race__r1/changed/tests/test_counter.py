import unittest
import sys
from concurrent.futures import ThreadPoolExecutor

from app import counter


class CounterTest(unittest.TestCase):
    def test_concurrent_increments_are_not_lost(self):
        counter.reset()
        workers = 8
        increments = 10_000

        interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(lambda _: [counter.increment("busy") for _ in range(increments)], range(workers)))
        finally:
            sys.setswitchinterval(interval)

        self.assertEqual(counter.get("busy"), workers * increments)


if __name__ == "__main__":
    unittest.main()

import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from app import counter


class SlowHashKey:
    """A key that makes thread switches during the counter update likely."""

    def __hash__(self):
        time.sleep(0.0001)
        return 1


class CounterTests(unittest.TestCase):
    def setUp(self):
        counter.reset()

    def test_concurrent_increments_are_not_lost(self):
        key = SlowHashKey()
        worker_count = 8
        increments_per_worker = 100

        def increment_repeatedly():
            for _ in range(increments_per_worker):
                counter.increment(key)

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = [executor.submit(increment_repeatedly) for _ in range(worker_count)]
            for future in futures:
                future.result()

        self.assertEqual(
            counter.get(key),
            worker_count * increments_per_worker,
        )


if __name__ == "__main__":
    unittest.main()

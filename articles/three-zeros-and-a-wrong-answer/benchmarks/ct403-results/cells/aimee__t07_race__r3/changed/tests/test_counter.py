import threading
import time
import unittest
from unittest.mock import patch

from app import counter


class CounterTest(unittest.TestCase):
    def setUp(self):
        counter.reset()

    def test_concurrent_increments_are_not_lost(self):
        class SlowReads(dict):
            def get(self, key, default=None):
                value = super().get(key, default)
                time.sleep(0.0001)
                return value

        workers = 10
        increments_per_worker = 50
        start = threading.Barrier(workers)

        def increment_many():
            start.wait()
            for _ in range(increments_per_worker):
                counter.increment("busy-page")

        with patch.object(counter, "_counts", SlowReads()):
            threads = [
                threading.Thread(target=increment_many) for _ in range(workers)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(
                counter.get("busy-page"), workers * increments_per_worker
            )


if __name__ == "__main__":
    unittest.main()

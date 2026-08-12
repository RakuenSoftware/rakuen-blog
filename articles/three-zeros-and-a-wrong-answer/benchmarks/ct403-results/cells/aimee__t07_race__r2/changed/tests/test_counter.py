import sys
import threading
import unittest

from app import counter


class CounterTests(unittest.TestCase):
    def setUp(self):
        counter.reset()

    def test_concurrent_increments_are_not_lost(self):
        worker_count = 8
        increments_per_worker = 5_000
        start = threading.Barrier(worker_count)

        def increment_views():
            start.wait()
            for _ in range(increments_per_worker):
                counter.increment("busy-page")

        previous_interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            threads = [threading.Thread(target=increment_views) for _ in range(worker_count)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        finally:
            sys.setswitchinterval(previous_interval)

        self.assertEqual(
            counter.get("busy-page"), worker_count * increments_per_worker
        )


if __name__ == "__main__":
    unittest.main()

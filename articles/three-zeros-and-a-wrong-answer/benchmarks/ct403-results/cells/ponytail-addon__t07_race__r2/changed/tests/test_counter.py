import sys
import threading
import unittest

from app import counter


class CounterTest(unittest.TestCase):
    def setUp(self):
        counter.reset()

    def test_concurrent_increments_are_not_lost(self):
        workers = 16
        increments = 5000
        old_interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            threads = [
                threading.Thread(
                    target=lambda: [counter.increment("busy") for _ in range(increments)]
                )
                for _ in range(workers)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        finally:
            sys.setswitchinterval(old_interval)

        self.assertEqual(counter.get("busy"), workers * increments)


if __name__ == "__main__":
    unittest.main()

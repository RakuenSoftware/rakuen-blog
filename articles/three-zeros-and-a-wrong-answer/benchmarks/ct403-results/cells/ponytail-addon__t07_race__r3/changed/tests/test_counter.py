import threading
import time
import unittest
from unittest.mock import patch

from app import counter


class SlowReads(dict):
    def get(self, key, default=None):
        value = super().get(key, default)
        time.sleep(0.0001)
        return value


class CounterTest(unittest.TestCase):
    def test_concurrent_increments_are_not_lost(self):
        workers = [threading.Thread(target=counter.increment, args=("page",)) for _ in range(20)]
        with patch.object(counter, "_counts", SlowReads()):
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()
            self.assertEqual(counter.get("page"), len(workers))


if __name__ == "__main__":
    unittest.main()

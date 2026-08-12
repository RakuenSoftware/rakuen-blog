import threading
import unittest

from app import counter


class CounterTest(unittest.TestCase):
    def test_concurrent_increments_are_not_lost(self):
        counter.reset()
        threads = [threading.Thread(target=self._increment, args=(1_000,)) for _ in range(20)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(counter.get("page"), 20_000)

    @staticmethod
    def _increment(times):
        for _ in range(times):
            counter.increment("page")


if __name__ == "__main__":
    unittest.main()

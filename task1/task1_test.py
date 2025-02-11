import random
import time
import unittest

from task1 import (
    range_sum_no_cache,
    update_no_cache,
    range_sum_with_cache,
    update_with_cache,
    lru_cache
)


class TestLRUCacheOptimization(unittest.TestCase):
    # The original initial data was changed to achieve at least some
    # non-unique range operations to guarantee cache hits
    def setUp(self):
        self.array = [random.randint(1, 100) for _ in range(1000)]
        self.queries = []
        for _ in range(15_000):
            if random.random() > 0.3:
                L = random.randint(0, 999)
                R = random.randint(max(0, L - 10), min(999, L + 10))
                self.queries.append(("Range", L, R))
            else:
                index, value = random.randint(0, 999), random.randint(1, 100)
                self.queries.append(("Update", index, value))

    def test_non_unique_range_percentage(self):
        range_operations = [query for query in self.queries if query[0] == "Range"]
        unique_ranges = set((query[1], query[2]) for query in range_operations)
        percentage_non_unique = (1 - len(unique_ranges) / len(range_operations)) * 100
        print(f"Percentage of non-unique Range operations: {percentage_non_unique:.2f}%")

    def test_no_cache_performance(self):
        start_time = time.time()
        for query in self.queries:
            if query[0] == "Range":
                range_sum_no_cache(self.array, query[1], query[2])
            elif query[0] == "Update":
                update_no_cache(self.array, query[1], query[2])
        duration = time.time() - start_time
        print(f"Execution time without cache: {duration:.2f} seconds")

    # It seems like using of DoubleLinkedList for LRUCache implementation has significant overhead
    # resulting in worse performance when cache is used
    def test_with_cache_performance(self):
        start_time = time.time()
        for query in self.queries:
            if query[0] == "Range":
                range_sum_with_cache(self.array, query[1], query[2])
            elif query[0] == "Update":
                update_with_cache(self.array, query[1], query[2])
        duration = time.time() - start_time
        print(f"Execution time with LRU cache: {duration:.2f} seconds")

    def test_cache_efficiency(self):
        hit_count = 0
        miss_count = 0
        for query in self.queries:
            if query[0] == "Range":
                key = (query[1], query[2])
                if lru_cache.get(key) != -1:
                    hit_count += 1
                else:
                    miss_count += 1
                    range_sum_with_cache(self.array, query[1], query[2])

        print(f"Cache hits: {hit_count}")
        print(f"Cache misses: {miss_count}")


if __name__ == "__main__":
    unittest.main()
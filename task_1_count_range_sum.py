import random
from functools import lru_cache
from count_time_execution import count_execution_time


class RangeSumArray:
    def __init__(self, array):
        self.array = array

    def range_sum_no_cache(self, L, R):
        return sum(self.array[L : R + 1])

    def update_no_cache(self, index, value):
        self.array[index] = value
        return self.array

    @lru_cache(maxsize=1000)
    def range_sum_with_cache(self, L, R):
        return sum(self.array[L : R + 1])

    def update_with_cache(self, index, value):
        self.array[index] = value
        self.range_sum_with_cache.cache_clear()
        return self.array


@count_execution_time
def test_no_cache(class_instance, requests_array):
    for request in requests_array:
        if request[0] == "Range":
            class_instance.range_sum_no_cache(request[1], request[2])

        elif request[0] == "Update":
            class_instance.update_no_cache(request[1], request[2])


@count_execution_time
def test_with_cache(class_instance, requests_array):
    for request in requests_array:
        if request[0] == "Range":
            class_instance.range_sum_with_cache(request[1], request[2])
        elif request[0] == "Update":
            class_instance.update_with_cache(request[1], request[2])


if __name__ == "__main__":
    # generate numbers list from 0 to 100000
    numbers_list = []
    for i in range(100000):
        numbers_list.append(random.randint(0, 100000))

    # generate requests list
    requests_list = []
    request_types = ["Range", "Update"]
    for i in range(50000):
        requests_list.append(
            (
                random.choices(request_types, weights=[1000, 1], k=1)[0],
                random.randint(0, 100000),
                random.randint(0, 100000),
            )
        )

    # initialize instance of RangeSumArray
    range_sum_array = RangeSumArray(numbers_list)

    # test without cache
    print("======= Test no cache =======")
    test_no_cache(range_sum_array, requests_list)

    # test with cache
    print("======= Test with cache =======")
    test_with_cache(range_sum_array, requests_list)

    print("======= Cache info  =======")
    print(range_sum_array.range_sum_with_cache.cache_info())

    # let's decrease the number of numbers and requests and use only range requests
    # generate numbers list from 0 to 1000
    numbers_list_decreased = []
    for i in range(1000):
        numbers_list_decreased.append(random.randint(0, 1000))

    # generate requests list
    requests_list_decreased = []
    request_types = ["Range", "Update"]
    for i in range(50000):
        requests_list_decreased.append(
            (
                "Range",
                random.randint(0, 1000),
                random.randint(0, 1000),
            )
        )

    # initialize instance of RangeSumArray
    range_sum_array_decreased = RangeSumArray(numbers_list_decreased)

    range_sum_array_decreased.range_sum_with_cache.cache_clear()

    # test without cache with decreased array
    print("\n")
    print("======= Test no cache with decreased array=======")
    test_no_cache(range_sum_array_decreased, requests_list_decreased)

    # test with cache with decreased array
    print("======= Test with cache with decreased array =======")
    test_with_cache(range_sum_array_decreased, requests_list_decreased)

    print("======= Cache info with decreased array =======")
    print(range_sum_array_decreased.range_sum_with_cache.cache_info())

import timeit
from functools import lru_cache
from count_time_execution import count_execution_time
from splay_tree import SplayTree
from matplotlib import pyplot as plt


@lru_cache(maxsize=100)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    number_from_cache = tree.find(n)
    if number_from_cache is not None:
        return number_from_cache
    fibonacci_value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert((n, fibonacci_value))
    return fibonacci_value


if __name__ == "__main__":
    # test fibonacci number with lru cache and splay tree count
    splay_tree_test = SplayTree()

    print("========= FIBONACCI COUNT TEST =========")
    print("LRU-Cache:", fibonacci_lru(150))
    print("Splay-tree Cache:", fibonacci_splay(150, splay_tree_test))
    print("========================================")

    # initiate check points
    check_points = [0]
    while check_points[-1] < 1000:
        check_points.append(check_points[-1] + 50)

    lru_cache_results = []
    for n in check_points:
        exec_time_lru_cache = timeit.timeit(lambda: fibonacci_lru(n), number=5)
        lru_cache_results.append((n, exec_time_lru_cache))

    splay_tree = SplayTree()
    splay_tree_results = []
    for n in check_points:
        exec_time_splay_tree = timeit.timeit(
            lambda: fibonacci_splay(n, splay_tree), number=5
        )
        splay_tree_results.append((n, exec_time_splay_tree))

    # build results table
    print("========= FIBONACCI COUNT RESULTS ====================")
    print(
        f"{'Fibonacci number':<20} | {"LRU Cache Time (s)":<20} | {"Splay Tree Time (s)":<20} | "
    )
    for index, result in enumerate(lru_cache_results):
        print(
            f"{result[0]:<20} | {result[1]:<20.7f} | {splay_tree_results[index][1]:<20.7f}"
        )
    print("======================================================")

    # results visualization
    # extract Fibonacci numbers and times for each method
    lru_fib, lru_times = zip(*lru_cache_results)
    splay_fib, splay_times = zip(*splay_tree_results)

    # plotting
    plt.figure(figsize=(10, 6))
    plt.plot(lru_fib, lru_times, label="LRU Cache", marker="o")
    plt.plot(splay_fib, splay_times, label="Splay Tree Cache", marker="s")

    # adding labels, title, and legend
    plt.title("Comparison of Fibonacci Computation Times", fontsize=16)
    plt.xlabel("Fibonacci Number", fontsize=14)
    plt.ylabel("Computation Time (seconds)", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # show the plot
    plt.show()

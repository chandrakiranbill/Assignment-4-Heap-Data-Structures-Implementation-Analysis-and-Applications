"""
Assignment 4: Heap Data Structures
Heapsort implementation and empirical comparison with Quicksort and Merge Sort.
"""

from __future__ import annotations
import random
import time
import statistics
from typing import Callable, List


def max_heapify(arr: List[int], heap_size: int, root: int) -> None:
    """Restore the max-heap property for the subtree rooted at root."""
    while True:
        left = 2 * root + 1
        right = 2 * root + 2
        largest = root

        if left < heap_size and arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest == root:
            return

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest


def build_max_heap(arr: List[int]) -> None:
    """Build a max heap in-place using bottom-up heap construction."""
    for i in range(len(arr) // 2 - 1, -1, -1):
        max_heapify(arr, len(arr), i)


def heapsort(values: List[int]) -> List[int]:
    """Return values sorted in ascending order using Heapsort."""
    arr = list(values)
    n = len(arr)

    build_max_heap(arr)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        max_heapify(arr, end, 0)

    return arr


def quicksort(values: List[int]) -> List[int]:
    """Return values sorted using randomized Quicksort."""
    arr = list(values)

    def partition(lo: int, hi: int) -> int:
        pivot_index = random.randint(lo, hi)
        arr[pivot_index], arr[hi] = arr[hi], arr[pivot_index]
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        return i

    def sort(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        p = partition(lo, hi)
        sort(lo, p - 1)
        sort(p + 1, hi)

    sort(0, len(arr) - 1)
    return arr


def mergesort(values: List[int]) -> List[int]:
    """Return values sorted using top-down Merge Sort."""
    arr = list(values)

    def merge(left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort(seq: List[int]) -> List[int]:
        if len(seq) <= 1:
            return seq
        mid = len(seq) // 2
        return merge(sort(seq[:mid]), sort(seq[mid:]))

    return sort(arr)


def generate_data(n: int, distribution: str) -> List[int]:
    """Generate sorted, reverse-sorted, or random integer data."""
    if distribution == "sorted":
        return list(range(n))
    if distribution == "reverse":
        return list(range(n, 0, -1))
    if distribution == "random":
        return random.sample(range(max(2 * n, 2)), n)
    raise ValueError("distribution must be sorted, reverse, or random")


def benchmark(
    sizes=(1000, 5000, 10000),
    distributions=("sorted", "reverse", "random"),
    repeats=3,
) -> list[dict]:
    """Benchmark the three sorting algorithms and return timing records."""
    algorithms: dict[str, Callable[[List[int]], List[int]]] = {
        "Heapsort": heapsort,
        "Quicksort": quicksort,
        "Merge Sort": mergesort,
    }

    rows = []
    for n in sizes:
        for distribution in distributions:
            source = generate_data(n, distribution)
            expected = sorted(source)

            for name, algorithm in algorithms.items():
                times = []
                for _ in range(repeats):
                    start = time.perf_counter()
                    result = algorithm(source)
                    elapsed = time.perf_counter() - start
                    if result != expected:
                        raise AssertionError(f"{name} produced an incorrect result")
                    times.append(elapsed)

                rows.append(
                    {
                        "algorithm": name,
                        "size": n,
                        "distribution": distribution,
                        "seconds_mean": statistics.mean(times),
                        "seconds_min": min(times),
                    }
                )
    return rows


def save_benchmark_csv(rows: list[dict], filename: str = "benchmark_results.csv") -> None:
    """Save benchmark results without external dependencies."""
    import csv

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    random.seed(42)
    rows = benchmark()
    save_benchmark_csv(rows)

    print("Heapsort correctness examples:")
    sample = [12, 3, 17, 8, 25, 1, 9]
    print("Input :", sample)
    print("Output:", heapsort(sample))

    print("\nBenchmark results:")
    for row in rows:
        print(
            f"{row['algorithm']:10s} | n={row['size']:5d} | "
            f"{row['distribution']:7s} | mean={row['seconds_mean']:.6f}s"
        )
    print("\nSaved benchmark_results.csv")

# Assignment 4: Heap Data Structures

This repository contains a Python implementation of Heapsort, an empirical
comparison with Quicksort and Merge Sort, an array-backed binary-heap priority
queue, and a priority-based scheduler simulation.

## Files

- `heapsort_analysis.py` — Heapsort, Quicksort, Merge Sort, input generation,
  benchmarking, and CSV output.
- `priority_queue_scheduler.py` — Task class, binary max-heap priority queue,
  key updates, and scheduler simulation.
- `report.md` — Detailed assignment report.
- `benchmark_results.csv` — Generated benchmark data after running the
  Heapsort analysis script.

## Requirements

Python 3.10 or newer is recommended. The programs use only the Python
standard library.

## Run Heapsort and benchmarks

```bash
python heapsort_analysis.py
```

The script verifies sorting correctness, benchmarks all three algorithms on
sorted, reverse-sorted, and random inputs, and creates `benchmark_results.csv`.

## Run the priority queue scheduler

```bash
python priority_queue_scheduler.py
```

The scheduler prints execution order, waiting time, turnaround time, and
deadline performance.

## GitHub

Create a repository, add these files, commit, and push them to GitHub. The
final submission should be the URL of the GitHub repository.

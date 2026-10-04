# Assignment 4: Heap Data Structures: Implementation, Analysis, and Applications

## 1. Introduction

Heap data structures provide an efficient way to organize elements according
to a priority while supporting fast insertion and removal of the highest- or
lowest-priority element. This assignment implements a binary max-heap using a
Python list and applies the structure to two related problems: Heapsort and
priority-based task scheduling. The implementation also compares Heapsort
empirically with Quicksort and Merge Sort on sorted, reverse-sorted, and
random data.

The design emphasizes standard array representations because a complete
binary tree maps naturally to an array. For an element at index `i`, its left
child is at `2i + 1`, its right child is at `2i + 2`, and its parent is at
`(i - 1) // 2`. This representation avoids explicit tree nodes and pointer
overhead while keeping the main heap operations efficient.

## 2. Heapsort Implementation

Heapsort is implemented in `heapsort_analysis.py`. The algorithm first calls
`build_max_heap`, which transforms the input array into a max-heap using
bottom-up heap construction. The largest element is then located at index
zero. The algorithm repeatedly swaps that element with the last item in the
current heap, reduces the heap size, and calls `max_heapify` to restore the
heap property.

The implementation returns a new sorted list so that the caller's original
input is not modified. The heap construction and extraction operations are
performed in place inside the working list.

### Algorithmic steps

1. Copy the input into a working array.
2. Build a max-heap from the array.
3. Swap the root with the final element in the active heap.
4. Reduce the active heap size by one.
5. Restore the max-heap property with `max_heapify`.
6. Repeat until one element remains.

## 3. Heapsort Complexity Analysis

### Worst case

The worst-case time complexity of Heapsort is **O(n log n)**. Building the
heap using bottom-up heap construction takes **O(n)**. After construction,
there are `n - 1` extraction steps. Each extraction performs a constant-time
swap followed by heap restoration, which can take **O(log n)** because the
element can move from the root to a leaf. Therefore, the extraction phase is
O(n log n), and the total is O(n + n log n) = **O(n log n)**.

### Average case

The average-case complexity is also **O(n log n)**. Regardless of the
initial distribution of the elements, Heapsort performs the same overall
pattern of heap construction followed by approximately `n` extractions.
Each heap restoration is bounded by the height of the binary heap, which is
O(log n). Unlike Quicksort, Heapsort does not depend on finding favorable
pivots to obtain its asymptotic bound.

### Best case

The best-case complexity remains **O(n log n)** under the standard
implementation. Even when the input is already sorted, the algorithm still
builds the heap and performs the extraction phase. Some individual
heapify operations may terminate early, but the algorithm does not have a
linear-time best-case path comparable to algorithms that can detect an
already sorted input.

### Space complexity

The core Heapsort procedure uses **O(1) auxiliary heap space** beyond the
working array because the heap is represented in place. The implementation
creates a copy of the input so that the caller's list remains unchanged;
therefore, the practical memory used by the wrapper is O(n). The sorting
algorithm itself does not require an additional O(n) data structure.

## 4. Comparison with Quicksort and Merge Sort

The benchmarking program compares three algorithms:

- **Heapsort:** O(n log n) worst, average, and best case; O(1) auxiliary
  space for an in-place implementation.
- **Quicksort:** average O(n log n), but worst O(n^2) for poor pivot choices.
  Randomized pivot selection reduces the likelihood of consistently poor
  partitions.
- **Merge Sort:** O(n log n) in the best, average, and worst cases, with
  O(n) auxiliary space in the list-based implementation.

The experiment uses sorted, reverse-sorted, and random input distributions at
multiple sizes. Three repetitions are performed for each algorithm,
distribution, and input size. Mean and minimum elapsed times are recorded in
`benchmark_results.csv`.

The benchmark is intentionally empirical rather than a substitute for
asymptotic analysis. Runtime can vary because of Python interpreter overhead,
machine load, memory behavior, recursion costs, and implementation details.

### Expected interpretation

On random data, Quicksort can often perform very well because partitioning
has favorable cache behavior and relatively low constant factors. Merge Sort
has predictable O(n log n) behavior but allocates additional lists during
merging. Heapsort provides a strong worst-case guarantee and low auxiliary
space, although its repeated parent-child comparisons and swaps can give it
higher practical constants than highly optimized alternatives.

For sorted and reverse-sorted data, the randomized Quicksort implementation
avoids the deterministic worst case that a fixed poor pivot could create.
Heapsort maintains its O(n log n) bound regardless of distribution. Merge Sort
also maintains O(n log n) behavior across all three distributions.

Actual timing values should be taken from the generated CSV file rather than
assumed in advance. This distinction is important because theoretical
complexity describes growth as input size increases, while measured runtime
also reflects implementation and hardware effects.

## 5. Priority Queue Design

The priority queue uses a **binary max-heap stored in a Python list**.
A max-heap is appropriate because the scheduling policy gives the highest
priority value to the task that should be selected first.

A list is preferable to a pointer-based binary tree for this assignment
because a binary heap is a complete tree. The array representation provides
direct parent and child index calculations, avoids node allocation, and
supports efficient cache-friendly access.

The `Task` class stores:

- task ID
- priority
- arrival time
- deadline
- duration

Tasks with equal priority use earlier arrival time as a tie-breaker, followed
by task ID. This creates deterministic scheduling behavior.

## 6. Priority Queue Operations

### insert(task)

A task is appended to the end of the heap and moved upward using
`sift_up` until the max-heap property is restored. The task can move through
at most the height of the heap.

**Time complexity: O(log n)** worst case.

### extract_max()

The root contains the highest-priority task. It is removed, the final heap
element is moved to the root, and `sift_down` restores the heap property.

**Time complexity: O(log n)** worst case.

### increase_key(task, new_priority)

The implementation maintains a dictionary mapping task IDs to heap indices.
This allows the target task to be located in O(1) expected time. After its
priority increases, the task moves upward as necessary.

**Time complexity: O(log n)** including the adjustment.

### decrease_key(task, new_priority)

The target is located through the index dictionary, its priority is reduced,
and `sift_down` moves it toward the correct position.

**Time complexity: O(log n)** including the adjustment.

### is_empty()

The queue checks whether the underlying list contains zero elements.

**Time complexity: O(1)**.

### Auxiliary position map

The position dictionary is an intentional design choice. Without it,
finding an arbitrary task by ID would require scanning the heap and would take
O(n). The dictionary adds O(n) auxiliary storage but makes key updates
efficient and predictable.

## 7. Scheduler Simulation

The scheduler is non-preemptive. Tasks become eligible when their arrival
time is less than or equal to the current clock time. All available tasks are
inserted into the priority queue, and the highest-priority task is extracted
and executed until completion.

For every completed task, the program records start time, finish time,
waiting time, turnaround time, and whether the deadline was met.

Waiting time is calculated as:

`start time - arrival time`

Turnaround time is calculated as:

`finish time - arrival time`

Deadline compliance is determined by comparing the finish time with the
task deadline.

This simulation demonstrates a practical use of priority queues. Similar
structures are used in scheduling systems, operating-system task selection,
event management, network processing, and other applications where the next
item should be selected according to priority rather than simple insertion
order.

## 8. Scheduling Results

The supplied demonstration contains six tasks with different priorities,
arrival times, deadlines, and durations. Because the queue is a max-heap,
the scheduler selects the highest-priority task among the tasks that have
already arrived.

Tasks with equal priority are resolved using earlier arrival time, which
prevents arbitrary ordering. The program prints the resulting schedule and
calculates average waiting time and the percentage of tasks that meet their
deadlines.

The exact numerical results are produced when
`priority_queue_scheduler.py` is executed. Keeping the results generated by
the program in the repository makes the analysis reproducible and avoids
presenting manually estimated measurements.

## 9. Design Trade-Offs

The binary max-heap provides an effective balance between speed and
simplicity. A sorted list could provide immediate access to the highest
priority item, but insertion could require O(n) movement. An unsorted list
would make insertion O(1) but extraction O(n). The binary heap provides
O(log n) insertion and extraction, making it more appropriate when both
operations occur frequently.

The position dictionary increases memory use but is valuable for the
`increase_key` and `decrease_key` operations. It changes task lookup from
O(n) to expected O(1), after which heap restructuring takes O(log n).

## 10. Applications

Priority queues are useful whenever work must be processed according to
importance or urgency. Examples include CPU scheduling, network packet
handling, emergency service dispatching, event simulation, shortest-path
algorithms, and resource management.

Heapsort is useful when a predictable O(n log n) worst-case bound and low
auxiliary memory are important. Priority queues are especially valuable when
data arrive dynamically and the system repeatedly needs the next highest-
priority item.

## 11. Conclusion

The implementation demonstrates that binary heaps are useful both as a
sorting mechanism and as the foundation of efficient priority queues.
Heapsort achieves O(n log n) time in the best, average, and worst cases,
while an in-place implementation requires only constant auxiliary sorting
space. The priority queue supports insertion, maximum extraction, and key
updates in O(log n), while checking whether the queue is empty takes O(1).

The empirical comparison also illustrates why theoretical and practical
performance should be considered together. Quicksort may have strong
practical performance on many inputs, Merge Sort offers predictable
O(n log n) performance at the cost of additional memory, and Heapsort offers
a strong worst-case guarantee with low auxiliary space. The scheduler
simulation further shows how the heap abstraction can solve a realistic
task-selection problem.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
*Introduction to algorithms* (4th ed.). MIT Press.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014).
*Data structures and algorithms in Java* (6th ed.). Wiley.

Python Software Foundation. (2026). *heapq — Heap queue algorithm*.
Python documentation. https://docs.python.org/3/library/heapq.html

"""
Assignment 4: Priority Queue and Scheduler Simulation.

The implementation uses an array-backed binary max-heap. Larger priority
values are served first. Tasks with equal priority are ordered by earlier
arrival time and then by task ID for deterministic behavior.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    task_id: str
    priority: int
    arrival_time: int
    deadline: int
    duration: int

    def __lt__(self, other: "Task") -> bool:
        """Return True when self has lower scheduling priority than other."""
        if self.priority != other.priority:
            return self.priority < other.priority
        if self.arrival_time != other.arrival_time:
            return self.arrival_time > other.arrival_time
        return self.task_id > other.task_id


class PriorityQueue:
    """Array-backed binary max-heap priority queue."""

    def __init__(self) -> None:
        self.heap: list[Task] = []
        self.positions: dict[str, int] = {}

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.positions[self.heap[i].task_id] = i
        self.positions[self.heap[j].task_id] = j

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if not (self.heap[parent] < self.heap[index]):
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index: int) -> None:
        n = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < n and self.heap[largest] < self.heap[left]:
                largest = left
            if right < n and self.heap[largest] < self.heap[right]:
                largest = right

            if largest == index:
                break

            self._swap(index, largest)
            index = largest

    def insert(self, task: Task) -> None:
        if task.task_id in self.positions:
            raise ValueError(f"Duplicate task ID: {task.task_id}")
        self.positions[task.task_id] = len(self.heap)
        self.heap.append(task)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self) -> Task:
        if self.is_empty():
            raise IndexError("Cannot extract from an empty priority queue")

        maximum = self.heap[0]
        last = self.heap.pop()
        del self.positions[maximum.task_id]

        if self.heap:
            self.heap[0] = last
            self.positions[last.task_id] = 0
            self._sift_down(0)

        return maximum

    def increase_key(self, task_id: str, new_priority: int) -> None:
        index = self._index_of(task_id)
        if new_priority < self.heap[index].priority:
            raise ValueError("increase_key requires a larger priority")
        self.heap[index].priority = new_priority
        self._sift_up(index)

    def decrease_key(self, task_id: str, new_priority: int) -> None:
        index = self._index_of(task_id)
        if new_priority > self.heap[index].priority:
            raise ValueError("decrease_key requires a smaller priority")
        self.heap[index].priority = new_priority
        self._sift_down(index)

    def _index_of(self, task_id: str) -> int:
        if task_id not in self.positions:
            raise KeyError(f"Task not found: {task_id}")
        return self.positions[task_id]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def __len__(self) -> int:
        return len(self.heap)


def simulate_scheduler(tasks: list[Task]) -> list[dict]:
    """
    Simulate a non-preemptive priority scheduler.

    At each clock time, all arrived tasks are inserted. The highest-priority
    available task runs to completion. Waiting time and deadline status are
    recorded for analysis.
    """
    pending = sorted(tasks, key=lambda t: (t.arrival_time, t.task_id))
    queue = PriorityQueue()
    completed: list[dict] = []
    current_time = 0
    next_index = 0

    while next_index < len(pending) or not queue.is_empty():
        if queue.is_empty() and next_index < len(pending):
            current_time = max(current_time, pending[next_index].arrival_time)

        while next_index < len(pending) and pending[next_index].arrival_time <= current_time:
            queue.insert(pending[next_index])
            next_index += 1

        task = queue.extract_max()
        start = current_time
        finish = start + task.duration
        waiting = start - task.arrival_time
        turnaround = finish - task.arrival_time
        met_deadline = finish <= task.deadline

        completed.append(
            {
                "task_id": task.task_id,
                "priority": task.priority,
                "arrival_time": task.arrival_time,
                "deadline": task.deadline,
                "duration": task.duration,
                "start_time": start,
                "finish_time": finish,
                "waiting_time": waiting,
                "turnaround_time": turnaround,
                "deadline_met": met_deadline,
            }
        )

        current_time = finish

    return completed


def demo() -> None:
    tasks = [
        Task("T1", priority=3, arrival_time=0, deadline=8, duration=3),
        Task("T2", priority=5, arrival_time=1, deadline=6, duration=2),
        Task("T3", priority=2, arrival_time=2, deadline=12, duration=4),
        Task("T4", priority=4, arrival_time=3, deadline=10, duration=2),
        Task("T5", priority=1, arrival_time=5, deadline=15, duration=3),
        Task("T6", priority=5, arrival_time=6, deadline=13, duration=2),
    ]

    results = simulate_scheduler(tasks)

    print("Priority Queue Scheduler Simulation")
    print("-" * 75)
    print(
        f"{'Task':<6}{'Pri':<5}{'Arr':<5}{'Start':<7}"
        f"{'Finish':<8}{'Wait':<6}{'Deadline':<10}{'Met?':<5}"
    )
    for r in results:
        print(
            f"{r['task_id']:<6}{r['priority']:<5}{r['arrival_time']:<5}"
            f"{r['start_time']:<7}{r['finish_time']:<8}"
            f"{r['waiting_time']:<6}{r['deadline']:<10}{str(r['deadline_met']):<5}"
        )

    avg_wait = sum(r["waiting_time"] for r in results) / len(results)
    deadline_rate = (
        sum(r["deadline_met"] for r in results) / len(results) * 100
    )
    print(f"\nAverage waiting time: {avg_wait:.2f}")
    print(f"Deadline completion rate: {deadline_rate:.2f}%")


if __name__ == "__main__":
    demo()

"""基于 multiprocessing 的 CPU 密集任务池示例"""

from __future__ import annotations

import hashlib
import time
from multiprocessing import Manager, Process, Queue
from typing import Any
from uuid import uuid4

SENTINEL = None


def _fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def _worker(task_queue: Queue, results: dict[str, Any]) -> None:
    while True:
        task = task_queue.get()
        if task is SENTINEL:
            break
        task_id, op, value = task
        if op == "fibonacci":
            result: Any = _fibonacci(value)
        elif op == "hash":
            result = hashlib.sha256(str(value).encode()).hexdigest()
        else:
            result = {"error": f"unknown op: {op}"}
        results[task_id] = result


class TaskPool:
    """使用 Process + Manager + Queue 隔离 CPU 密集任务。"""

    def __init__(self, num_workers: int = 2) -> None:
        self._num_workers = num_workers
        self._manager: Any = None
        self._task_queue: Any = None
        self._results: Any = None
        self._workers: list[Process] = []

    def start(self) -> None:
        if self._workers:
            return
        self._manager = Manager()
        self._task_queue = self._manager.Queue()
        self._results = self._manager.dict()
        self._workers = [
            Process(target=_worker, args=(self._task_queue, self._results))
            for _ in range(self._num_workers)
        ]
        for worker in self._workers:
            worker.start()

    def submit(self, op: str, value: int) -> str:
        if self._task_queue is None:
            raise RuntimeError("TaskPool is not started")
        task_id = str(uuid4())
        self._task_queue.put((task_id, op, value))
        return task_id

    def get_result(self, task_id: str, timeout: float = 30.0) -> Any:
        if self._results is None:
            raise RuntimeError("TaskPool is not started")
        deadline = time.time() + timeout
        while time.time() < deadline:
            if task_id in self._results:
                return self._results.pop(task_id)
            time.sleep(0.05)
        raise TimeoutError(f"Task {task_id} timed out after {timeout}s")

    def shutdown(self) -> None:
        if self._task_queue is not None:
            for _ in self._workers:
                self._task_queue.put(SENTINEL)
        for worker in self._workers:
            worker.join(timeout=5)
            if worker.is_alive():
                worker.terminate()
        self._workers.clear()
        if self._manager is not None:
            self._manager.shutdown()
            self._manager = None
        self._task_queue = None
        self._results = None

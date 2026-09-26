"""Per-source rate limiting (PRD mitigation for parallel solving).

A single source cannot speed up one puzzle, but it can request many puzzles and
solve them in parallel. Capping concurrent puzzles per source limits that. This
is a simple in-memory counter; a real deployment would use a shared store.
"""

from __future__ import annotations

import threading
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_active_per_source: int):
        self.max_active = max_active_per_source
        self._active: dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def try_acquire(self, source: str) -> bool:
        """Reserve one active slot for source; False if at the cap."""
        with self._lock:
            if self._active[source] >= self.max_active:
                return False
            self._active[source] += 1
            return True

    def release(self, source: str) -> None:
        with self._lock:
            if self._active[source] > 0:
                self._active[source] -= 1

    def active(self, source: str) -> int:
        with self._lock:
            return self._active[source]

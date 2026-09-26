"""Metrics: detection latency and event counters (PRD NFR-1, NFR-2, success §8).

Tracks how quickly a decoy touch turns into an alert, and counts events by kind,
so a deployment can show it is meeting its detection-latency and false-alarm
targets.
"""

from __future__ import annotations

import threading
from collections import defaultdict


class Metrics:
    def __init__(self, max_samples: int = 10_000) -> None:
        self._lock = threading.Lock()
        self.counts: dict[str, int] = defaultdict(int)
        self.detection_latencies_ms: list[float] = []
        self.max_samples = max_samples   # rolling window; bounds memory
        self.known_good_touches = 0   # honest mistakes, not real alarms

    def record_event(self, kind: str) -> None:
        with self._lock:
            self.counts[kind] += 1

    def record_detection_latency(self, ms: float) -> None:
        with self._lock:
            self.detection_latencies_ms.append(ms)
            if len(self.detection_latencies_ms) > self.max_samples:
                del self.detection_latencies_ms[: -self.max_samples]

    def record_known_good_touch(self) -> None:
        with self._lock:
            self.known_good_touches += 1

    def summary(self) -> dict:
        with self._lock:
            lat = sorted(self.detection_latencies_ms)
            n = len(lat)
            p95 = lat[int(0.95 * (n - 1))] if n else 0.0
            touches = self.counts.get("decoy_touched", 0)
            # False alarms here = known-good touches / total touches.
            false_alarm_rate = (self.known_good_touches / touches) if touches else 0.0
            return {
                "counts": dict(self.counts),
                "detections": n,
                "median_latency_ms": (lat[n // 2] if n else 0.0),
                "p95_latency_ms": p95,
                "max_latency_ms": (lat[-1] if n else 0.0),
                "false_alarm_rate": round(false_alarm_rate, 4),
            }

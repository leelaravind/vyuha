"""Out-of-band alert sinks (PRD FR-7, NFR-5).

The watcher raises alerts through a sink. In a real deployment the sink delivers
to an isolated responder that the decoy field cannot reach or influence. Several
simple sinks are provided; a deployment injects whichever it needs.

Nothing here contacts an external system on its own; the network sink is a stub
that a deployment would point at its own isolated responder.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Callable
from pathlib import Path


class AlertSink:
    def deliver(self, entry: dict) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class ConsoleSink(AlertSink):
    """Prints high-signal events. Useful in the lab."""

    HIGH_SIGNAL = {"decoy_touched", "puzzle_solved", "early_answer", "rate_limited"}

    def deliver(self, entry: dict) -> None:
        ev = entry["event"]
        if ev["kind"] in self.HIGH_SIGNAL:
            print(f"  [ALERT] {ev['kind']}: {ev['source_ip']} {ev['path']}")


class CollectingSink(AlertSink):
    """Keeps alerts in memory. Useful for tests and metrics."""

    def __init__(self) -> None:
        self.alerts: list[dict] = []
        self._lock = threading.Lock()

    def deliver(self, entry: dict) -> None:
        with self._lock:
            self.alerts.append(entry)


class FileSink(AlertSink):
    """Writes alerts to a separate file from the main log (a second channel)."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def deliver(self, entry: dict) -> None:
        with self._lock, self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry["event"], sort_keys=True) + "\n")


class FanoutSink(AlertSink):
    """Delivers to several sinks at once."""

    def __init__(self, *sinks: AlertSink):
        self.sinks = list(sinks)

    def deliver(self, entry: dict) -> None:
        for s in self.sinks:
            s.deliver(entry)


def callable_sink(fn: Callable[[dict], None]) -> AlertSink:
    """Wrap a plain function as a sink."""
    class _S(AlertSink):
        def deliver(self, entry: dict) -> None:
            fn(entry)
    return _S()

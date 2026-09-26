"""Watcher: an isolated recorder that keeps a tamper-evident log and alerts.

The watcher's job is to record every interaction with a decoy and to raise a
silent alert. Two properties matter:

  * Tamper-evidence. Records form a hash chain: each entry includes the hash of
    the previous entry, so removing or altering any past entry breaks the chain
    and is detectable. (This does not stop deletion; it makes deletion visible.)

  * Out-of-band alerting. The alert is delivered through a callback the caller
    provides, so in a real deployment it can go somewhere the decoy cannot reach
    or influence. The decoy is never told an alert fired, so it keeps behaving
    normally.

This prototype writes its log to a local file for inspection. It performs no
network actions; alert delivery is left to the injected callback.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from collections.abc import Callable
from pathlib import Path

_GENESIS = "0" * 64


class Watcher:
    def __init__(
        self,
        log_path: str | Path,
        alert: Callable[[dict], None] | None = None,
    ):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._alert = alert
        self._lock = threading.Lock()
        self._last_hash = self._load_last_hash()

    def _load_last_hash(self) -> str:
        if not self.log_path.exists():
            return _GENESIS
        last = _GENESIS
        with self.log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    last = json.loads(line)["entry_hash"]
        return last

    @staticmethod
    def _hash(prev_hash: str, body: str) -> str:
        return hashlib.sha256((prev_hash + body).encode()).hexdigest()

    def record(self, event: dict, alert: bool = True) -> dict:
        """Append an event to the tamper-evident log and optionally alert."""
        with self._lock:
            entry = {
                "ts": time.time(),
                "prev_hash": self._last_hash,
                "event": event,
            }
            body = json.dumps(entry, sort_keys=True)
            entry["entry_hash"] = self._hash(self._last_hash, body)
            with self.log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, sort_keys=True) + "\n")
            self._last_hash = entry["entry_hash"]

        if alert and self._alert is not None:
            # Delivered out-of-band. The decoy path is never informed.
            self._alert(entry)
        return entry

    def verify_chain(self) -> bool:
        """Check that the log's hash chain is unbroken (no silent edits)."""
        prev = _GENESIS
        with self.log_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                stored = entry.pop("entry_hash")
                body = json.dumps(entry, sort_keys=True)
                if entry["prev_hash"] != prev:
                    return False
                if self._hash(prev, body) != stored:
                    return False
                prev = stored
        return True

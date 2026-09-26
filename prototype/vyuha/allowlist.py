"""Known-good sources and honest-mistake handling (PRD FR-11).

Legitimate users never touch the decoy field. But an honest employee might
stumble onto a decoy by accident. When a known-good source touches a decoy, it
is still recorded (for review) but marked as a low-severity "review" event
rather than treated as an attack. It is never auto-penalised.

Sources are identified only coarsely (e.g. an internal IP or an enrolled device
id). This is a convenience for triage, not an identity system.
"""

from __future__ import annotations


class Allowlist:
    def __init__(self, known_good: set[str] | None = None):
        self._known_good = set(known_good or set())

    def add(self, source: str) -> None:
        self._known_good.add(source)

    def remove(self, source: str) -> None:
        self._known_good.discard(source)

    def is_known_good(self, source: str) -> bool:
        return source in self._known_good

    def severity(self, source: str) -> str:
        """'review' for a known-good source (likely a mistake), else 'high'."""
        return "review" if self.is_known_good(source) else "high"

"""Rotating vault: the values placed behind decoys, which expire on a schedule.

Every value behind a decoy is fake. On top of being fake, each value is only
"current" for one short time window (an epoch). Values are derived from a master
secret and the current epoch, so nothing has to be stored, and a value obtained
in one epoch is stale in the next.

Combined with a time cost that is longer than the epoch (see timelock.py), any
value reached through a decoy has already expired by the time it is reached --
and it was never real to begin with.

This module performs no network or file actions. It only derives and checks
values.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time


class RotatingVault:
    def __init__(self, rotation_seconds: float, label: str = "decoy",
                 seed: bytes | None = None):
        if rotation_seconds <= 0:
            raise ValueError("rotation_seconds must be positive")
        self.rotation_seconds = rotation_seconds
        self.label = label
        if seed:
            # Deterministic per deployment: different deployments (different
            # seeds) produce different values, so decoys are not identical
            # across sites (PRD FR-9). Same seed reproduces the same vault.
            self._master = hmac.new(seed, f"vault:{label}".encode(),
                                    hashlib.sha256).digest()
        else:
            self._master = secrets.token_bytes(32)

    def epoch(self, now: float | None = None) -> int:
        """The current epoch number (which time window we are in)."""
        now = time.time() if now is None else now
        return int(now // self.rotation_seconds)

    def value(self, epoch: int | None = None) -> str:
        """The fake value for a given epoch, shaped to look like a real secret."""
        if epoch is None:
            epoch = self.epoch()
        digest = hmac.new(
            self._master, f"{self.label}:{epoch}".encode(), hashlib.sha256
        ).hexdigest()
        return f"{self.label}_{digest[:32]}"

    def age_epochs(self, value: str, lookback: int = 10000) -> int | None:
        """How many epochs ago this value was current.

        Returns 0 if still current, a positive number if stale, or None if the
        value was never issued by this vault.
        """
        if not value.isascii():
            return None
        current = self.epoch()
        for age in range(lookback):
            if hmac.compare_digest(self.value(current - age), value):
                return age
        return None

    def is_current(self, value: str) -> bool:
        return self.age_epochs(value, lookback=1) == 0

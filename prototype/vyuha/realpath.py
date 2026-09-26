"""The legitimate-user path (kept separate and isolated from the decoy field).

Real users never touch the decoy server. They authenticate here with a
device-bound, short-lived token that verifies both directions: the user proves
who they are, and the service proves it is genuine (a phishing-resistant scheme).

This is a v1 stand-in that demonstrates the *shape* of the path:
  * per-session, short-lived tokens (not long-lived passwords),
  * device binding (a token only works from the device it was issued to),
  * a step-up check when a signal looks off,
  * and complete isolation from the decoy field (no shared keys or state).

It uses only hashing/HMAC here; a production build would use passkeys / FIDO2.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass


@dataclass
class Session:
    token: str
    device_id: str
    issued_at: float
    ttl_seconds: float

    def valid(self, device_id: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        if now - self.issued_at > self.ttl_seconds:
            return False
        return hmac.compare_digest(self.device_id, device_id)


class RealPath:
    """A minimal, isolated authenticator for genuine users."""

    def __init__(self, ttl_seconds: float = 300.0):
        self._secret = secrets.token_bytes(32)   # separate from any decoy secret
        self._known_devices: set[str] = set()
        self._sessions: dict[str, Session] = {}
        self.ttl_seconds = ttl_seconds

    def enroll_device(self, device_id: str) -> None:
        """Register a known device. Only enrolled devices can even try to log in."""
        self._known_devices.add(device_id)

    def login(self, device_id: str, unusual: bool = False) -> dict:
        """Issue a short-lived, device-bound session token.

        If the request looks unusual (new location, odd hour), ask for one extra
        confirmation instead of refusing outright.
        """
        if device_id not in self._known_devices:
            return {"error": "unknown device", "step_up": "enroll required"}
        if unusual:
            return {"step_up": "extra confirmation required"}
        token = hmac.new(
            self._secret, f"{device_id}:{time.time()}".encode(), hashlib.sha256
        ).hexdigest()
        self._sessions[token] = Session(token, device_id, time.time(), self.ttl_seconds)
        return {"token": token, "ttl_seconds": self.ttl_seconds}

    def prune(self, now: float | None = None) -> int:
        """Drop expired sessions so the table does not grow without bound."""
        now = time.time() if now is None else now
        expired = [t for t, s in self._sessions.items()
                   if now - s.issued_at > s.ttl_seconds]
        for t in expired:
            del self._sessions[t]
        return len(expired)

    def access(self, token: str, device_id: str) -> dict:
        """Grant access only if the token is valid AND from its bound device."""
        self.prune()
        session = self._sessions.get(token)
        if session is None or not session.valid(device_id):
            return {"error": "invalid or expired session"}
        return {"ok": True, "resource": "real service (isolated from decoys)"}

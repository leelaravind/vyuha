"""The Vyuha decoy server (lab-only, loopback).

It presents the decoy field over HTTP. The flow for any visitor:

  GET /<decoy path>   -> logs the touch, raises a silent alert, and returns a
                         time-lock puzzle sized for that path's value tier.
  POST /collect       -> the visitor submits their puzzle answer. The server
                         checks the answer AND the tier's server-side time floor.
                         Only if both pass does it return the (fake, stale)
                         decoy content.

Real users never see any of this: they use the separate path in realpath.py.
Because only an attacker would ever touch a decoy, every event here is a
high-confidence signal -- except a touch from a known-good source, which is
logged as a low-severity 'review' event (an honest mistake), never a penalty.

Binds to loopback only. Refuses to start on a non-loopback address.
"""

from __future__ import annotations

import json
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import decoys, schema
from .alerting import AlertSink, ConsoleSink, FanoutSink, FileSink
from .allowlist import Allowlist
from .config import VyuhaConfig
from .metrics import Metrics
from .ratelimit import RateLimiter
from .timelock import PuzzleMaker
from .vault import RotatingVault
from .watcher import Watcher


class VyuhaService:
    """Holds the server-side state: puzzle maker, per-tier vaults, watcher, etc."""

    def __init__(self, config: VyuhaConfig, watcher: Watcher,
                 metrics: Metrics | None = None):
        config.ensure_secrets()
        config.validate()
        self.config = config
        self.watcher = watcher
        self.metrics = metrics or Metrics()
        self.maker = PuzzleMaker(bits=config.modulus_bits)
        self.tier_map = config.effective_tier_map()
        self.allowlist = Allowlist(config.known_good)
        self.rate = RateLimiter(config.max_puzzles_per_ip)
        # One vault per tier, each seeded from the deployment seed (unique per site).
        self._vaults: dict[str, RotatingVault] = {
            name: RotatingVault(t.rotation_seconds, label=f"svc-{name}",
                                seed=config.deployment_seed)
            for name, t in self.tier_map.tiers.items()
        }
        self._sessions: dict[str, dict] = {}
        self._lock = threading.Lock()   # guards _sessions (server is threaded)

    def _log(self, event: dict, alert: bool = True) -> dict:
        self.metrics.record_event(event["kind"])
        entry = self.watcher.record(event, alert=alert)
        return entry

    def _session_ttl(self, floor_seconds: float) -> float:
        c = self.config
        return max(c.session_ttl_multiplier * floor_seconds, c.session_min_ttl_seconds)

    def sweep_expired(self, now: float | None = None) -> int:
        """Drop expired sessions and free their rate-limit slots.

        Without this, an abandoned puzzle would hold its source's slot forever
        and the session table would grow without bound.
        """
        now = time.time() if now is None else now
        with self._lock:
            expired = [s for s, st in self._sessions.items() if now >= st["expires_at"]]
            for s in expired:
                self.rate.release(self._sessions[s]["source_ip"])
                del self._sessions[s]
        return len(expired)

    # -- decoy touch: hand out a puzzle ------------------------------------
    def on_touch(self, source_ip: str, path: str) -> dict:
        t0 = time.perf_counter()
        tier = self.tier_map.for_path(path)
        severity = self.allowlist.severity(source_ip)
        if severity == "review":
            self.metrics.record_known_good_touch()
        touch = schema.make_event(
            schema.DECOY_TOUCHED, source_ip=source_ip, path=path,
            detail={"tier": tier.name, "severity": severity},
        )
        self._log(touch)
        self.metrics.record_detection_latency((time.perf_counter() - t0) * 1000)

        if not self.rate.try_acquire(source_ip):
            self._log(schema.make_event(schema.RATE_LIMITED, source_ip=source_ip,
                                        path=path))
            return {"error": "slow down"}

        self.sweep_expired()
        session = secrets.token_hex(16)
        puzzle, answer = self.maker.make(t=tier.puzzle_squarings)
        issued_at = time.time()
        with self._lock:
            self._sessions[session] = {
                "answer": answer, "issued_at": issued_at,
                "expires_at": issued_at + self._session_ttl(tier.time_floor_seconds),
                "path": path, "tier": tier.name, "source_ip": source_ip,
            }
        self._log(schema.make_event(
            schema.PUZZLE_ISSUED, source_ip=source_ip, path=path, session=session,
            detail={"t": puzzle.t, "tier": tier.name},
        ), alert=False)
        return {
            "session": session, "n": hex(puzzle.n), "base": hex(puzzle.base),
            "t": puzzle.t, "note": "solve x=base^(2^t) mod n, then POST /collect",
        }

    # -- collect: check answer AND the tier's time floor -------------------
    def on_collect(self, source_ip: str, session: str, candidate: int) -> dict:
        self.sweep_expired()
        with self._lock:
            state = self._sessions.get(session)
        if state is None:
            return {"error": "unknown or expired session"}
        tier = self.tier_map.tiers[state["tier"]]
        elapsed = time.time() - state["issued_at"]

        if tier.time_floor_seconds > 0 and elapsed < tier.time_floor_seconds:
            self._log(schema.make_event(
                schema.EARLY_ANSWER, source_ip=source_ip, path=state["path"],
                session=session, detail={"elapsed": round(elapsed, 2),
                                         "tier": tier.name},
            ))
            return {"error": "too early",
                    "wait_more_seconds": round(tier.time_floor_seconds - elapsed, 2)}

        if candidate != state["answer"]:
            return {"error": "incorrect"}

        self._log(schema.make_event(
            schema.PUZZLE_SOLVED, source_ip=source_ip, path=state["path"],
            session=session, detail={"elapsed": round(elapsed, 2), "tier": tier.name},
        ))
        content = decoys.render(state["path"], self._vaults[state["tier"]],
                                self.config.deployment_seed)
        self._log(schema.make_event(
            schema.DECOY_VALUE_SERVED, source_ip=source_ip, path=state["path"],
            session=session,
        ), alert=False)
        with self._lock:
            # single-use: remove, and free the slot only if we were the remover
            if self._sessions.pop(session, None) is not None:
                self.rate.release(state["source_ip"])
        return {"path": state["path"], "content": content,
                "notice": "any value here is fake and already rotated out"}


def make_handler(service: VyuhaService):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: dict):
            body = json.dumps(payload, indent=2).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            ip = self.client_address[0]
            if self.path in service.config.decoy_paths:
                self._send(200, service.on_touch(ip, self.path))
            elif self.path == "/health":
                self._send(200, {"status": "ok"})
            elif self.path == "/metrics":
                self._send(200, service.metrics.summary())
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            ip = self.client_address[0]
            if self.path != "/collect":
                self._send(404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                if length < 0 or length > service.config.max_request_body_bytes:
                    self._send(413, {"error": "request body too large"})
                    return
                body = json.loads(self.rfile.read(length))
                session = str(body["session"])
                raw = body["answer"]
                candidate = int(raw, 0) if isinstance(raw, str) else int(raw)
            except (ValueError, KeyError, TypeError):
                self._send(400, {"error": "expected JSON {session, answer}"})
                return
            self._send(200, service.on_collect(ip, session, candidate))

        def log_message(self, *args):
            pass  # the watcher is the record

    return Handler


def build_service(config: VyuhaConfig) -> VyuhaService:
    sink: AlertSink = FanoutSink(ConsoleSink(), FileSink(config.alert_log))
    watcher = Watcher(config.watcher_log, alert=sink.deliver)
    return VyuhaService(config, watcher)


def serve(config: VyuhaConfig | None = None) -> None:
    config = config or VyuhaConfig()
    service = build_service(config)
    # Threaded: one slow client no longer blocks every other request.
    httpd = ThreadingHTTPServer((config.host, config.port), make_handler(service))
    httpd.daemon_threads = True
    print(f"Vyuha decoy server on http://{config.host}:{config.port} (loopback only)")
    print(f"decoy paths: {', '.join(config.decoy_paths)}")
    print(f"tiers: {', '.join(service.tier_map.tiers)}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    serve()

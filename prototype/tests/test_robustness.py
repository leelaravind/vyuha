"""Robustness tests added after code review: concurrency, expiry, leaks, limits.
Run:  python tests/test_robustness.py"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vyuha.config import VyuhaConfig
from vyuha.metrics import Metrics
from vyuha.realpath import RealPath
from vyuha.server import VyuhaService, make_handler
from vyuha.watcher import Watcher
from http.server import ThreadingHTTPServer


def _svc(**over):
    d = tempfile.mkdtemp()
    cfg = VyuhaConfig(modulus_bits=1024, puzzle_squarings=3_000,
                      time_floor_seconds=0, rotation_seconds=1,
                      watcher_log=os.path.join(d, "w.jsonl"),
                      alert_log=os.path.join(d, "a.jsonl"), **over)
    return VyuhaService(cfg, Watcher(cfg.watcher_log))


def test_expired_session_frees_rate_slot():
    # Before the fix, an abandoned puzzle held its slot forever.
    svc = _svc(max_puzzles_per_ip=1, session_min_ttl_seconds=0.05,
               session_ttl_multiplier=1.0)
    assert "session" in svc.on_touch("9.9.9.9", "/.env")
    assert svc.on_touch("9.9.9.9", "/.env").get("error") == "slow down"
    time.sleep(0.08)
    assert svc.sweep_expired() == 1
    assert svc.rate.active("9.9.9.9") == 0
    assert "session" in svc.on_touch("9.9.9.9", "/.env")   # slot is back


def test_expired_session_is_rejected_on_collect():
    svc = _svc(session_min_ttl_seconds=0.05, session_ttl_multiplier=1.0)
    issued = svc.on_touch("9.9.9.9", "/.env")
    ans = svc._sessions[issued["session"]]["answer"]
    time.sleep(0.08)
    out = svc.on_collect("9.9.9.9", issued["session"], ans)
    assert out.get("error") == "unknown or expired session"


def test_concurrent_touches_do_not_corrupt_sessions():
    svc = _svc(max_puzzles_per_ip=1000)
    errors: list[Exception] = []

    def worker(i: int):
        try:
            r = svc.on_touch(f"10.0.{i % 7}.{i}", "/.env")
            assert "session" in r
        except Exception as e:  # pragma: no cover
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(40)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert len(svc._sessions) == 40
    assert svc.metrics.summary()["counts"]["decoy_touched"] == 40


def test_double_collect_does_not_double_release():
    svc = _svc(max_puzzles_per_ip=5)
    issued = svc.on_touch("9.9.9.9", "/.env")
    ans = svc._sessions[issued["session"]]["answer"]
    assert "content" in svc.on_collect("9.9.9.9", issued["session"], ans)
    assert svc.rate.active("9.9.9.9") == 0
    # second collect of the same session must be rejected and not go negative
    assert "error" in svc.on_collect("9.9.9.9", issued["session"], ans)
    assert svc.rate.active("9.9.9.9") == 0


def test_oversized_post_body_is_rejected_over_http():
    svc = _svc(max_request_body_bytes=64)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(svc))
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        big = json.dumps({"session": "x" * 500, "answer": "1"}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{port}/collect", data=big,
                                     headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req)
            raise AssertionError("expected HTTP 413")
        except urllib.error.HTTPError as e:
            assert e.code == 413
    finally:
        httpd.shutdown()


def test_metrics_latency_window_is_bounded():
    m = Metrics(max_samples=10)
    for i in range(50):
        m.record_detection_latency(float(i))
    assert len(m.detection_latencies_ms) == 10
    assert m.detection_latencies_ms[0] == 40.0


def test_realpath_prunes_expired_sessions():
    rp = RealPath(ttl_seconds=0.05)
    rp.enroll_device("d1")
    tok = rp.login("d1")["token"]
    assert rp.access(tok, "d1")["ok"] is True
    time.sleep(0.08)
    assert "error" in rp.access(tok, "d1")
    assert len(rp._sessions) == 0


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} robustness tests passed")


if __name__ == "__main__":
    _run_all()

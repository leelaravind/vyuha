"""Product-level tests tracing to PRD requirements. Run:  python tests/test_product.py"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vyuha.config import VyuhaConfig
from vyuha.tiers import Tier, TierMap, DEFAULT_TIERS
from vyuha.allowlist import Allowlist
from vyuha.ratelimit import RateLimiter
from vyuha.metrics import Metrics
from vyuha.vault import RotatingVault
from vyuha.server import VyuhaService
from vyuha.watcher import Watcher


def _svc(**over):
    d = tempfile.mkdtemp()
    cfg = VyuhaConfig(modulus_bits=1024, puzzle_squarings=3_000,
                      time_floor_seconds=0, rotation_seconds=1,
                      watcher_log=os.path.join(d, "w.jsonl"),
                      alert_log=os.path.join(d, "a.jsonl"), **over)
    return VyuhaService(cfg, Watcher(cfg.watcher_log))


def test_FR9_uniqueness_across_deployments():
    # Same label, different seeds -> different values.
    a = RotatingVault(1, "svc", seed=b"deployment-A")
    b = RotatingVault(1, "svc", seed=b"deployment-B")
    assert a.value(epoch=5) != b.value(epoch=5)
    # Same seed -> reproducible.
    a2 = RotatingVault(1, "svc", seed=b"deployment-A")
    assert a.value(epoch=5) == a2.value(epoch=5)


def test_FR10_FR12_value_tiers_scale_tightness():
    tm = TierMap(DEFAULT_TIERS, {"/crown.key": "crown", "/tmp.log": "standard"})
    crown = tm.for_path("/crown.key")
    standard = tm.for_path("/tmp.log")
    assert crown.time_floor_seconds > standard.time_floor_seconds
    assert crown.rotation_seconds < standard.rotation_seconds


def test_tier_rotation_must_be_shorter_than_floor():
    try:
        Tier("bad", rotation_seconds=100, time_floor_seconds=50, puzzle_squarings=1).validate()
    except ValueError:
        return
    raise AssertionError("expected ValueError for rotation >= floor")


def test_FR11_known_good_touch_is_review_not_penalty():
    svc = _svc(known_good={"10.0.0.5"})
    out = svc.on_touch("10.0.0.5", "/.env")
    # still issued a puzzle (recorded), but marked review and counted as a mistake
    assert "session" in out
    assert svc.metrics.known_good_touches == 1
    assert svc.allowlist.severity("10.0.0.5") == "review"
    assert svc.allowlist.severity("203.0.113.9") == "high"


def test_rate_limiter_caps_parallel_puzzles():
    rl = RateLimiter(max_active_per_source=2)
    assert rl.try_acquire("x") and rl.try_acquire("x")
    assert not rl.try_acquire("x")      # third blocked
    rl.release("x")
    assert rl.try_acquire("x")          # slot freed


def test_server_rate_limit_end_to_end():
    svc = _svc(max_puzzles_per_ip=1)
    assert "session" in svc.on_touch("9.9.9.9", "/.env")
    assert svc.on_touch("9.9.9.9", "/.env").get("error") == "slow down"


def test_config_refuses_non_loopback():
    try:
        VyuhaConfig(host="0.0.0.0").validate()
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-loopback host")


def test_NFR1_NFR2_metrics_summary():
    svc = _svc(known_good={"10.0.0.5"})
    svc.on_touch("203.0.113.9", "/.env")   # real
    svc.on_touch("10.0.0.5", "/.env")      # honest mistake
    s = svc.metrics.summary()
    assert s["counts"]["decoy_touched"] == 2
    assert s["detections"] == 2
    assert 0 < s["false_alarm_rate"] <= 1  # one of two touches was known-good


def test_full_flow_serves_fake_content_after_answer():
    svc = _svc()  # floor 0
    issued = svc.on_touch("9.9.9.9", "/.env")
    ans = svc._sessions[issued["session"]]["answer"]
    out = svc.on_collect("9.9.9.9", issued["session"], ans)
    assert "content" in out and "fake" in out["notice"]


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} product tests passed")


if __name__ == "__main__":
    _run_all()

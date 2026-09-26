"""Tests for the Vyuha core modules. Run:  python -m pytest -q   (or python tests/test_core.py)"""

from __future__ import annotations

import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vyuha.timelock import PuzzleMaker, solve, derive_base
from vyuha.vault import RotatingVault
from vyuha.watcher import Watcher
from vyuha.realpath import RealPath
from vyuha import schema
from vyuha.config import VyuhaConfig
from vyuha.server import VyuhaService


def test_timelock_issuer_matches_solver():
    m = PuzzleMaker(bits=1024)
    p, ans = m.make(t=50_000)
    assert solve(p) == ans
    assert m.verify(p, ans)
    assert not m.verify(p, ans + 1)


def test_derive_base_is_deterministic():
    m = PuzzleMaker(bits=1024)
    b1 = derive_base(b"key", "pid-1", m.n)
    b2 = derive_base(b"key", "pid-1", m.n)
    assert b1 == b2
    assert 2 <= b1 < m.n


def test_vault_rotation_expires_values():
    v = RotatingVault(rotation_seconds=0.05, label="t")
    val = v.value()
    assert v.is_current(val)
    time.sleep(0.12)  # let >=2 epochs pass
    assert not v.is_current(val)
    assert v.age_epochs(val) >= 1
    assert v.age_epochs("t_never_issued_value") is None


def test_watcher_hash_chain_detects_tampering():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "log.jsonl")
        w = Watcher(path)
        for i in range(3):
            w.record(schema.make_event(schema.DECOY_TOUCHED, source_ip="1.2.3.4",
                                       path=f"/p{i}"))
        assert w.verify_chain() is True
        # tamper: flip a byte in the middle of the file
        data = open(path, encoding="utf-8").read().splitlines()
        data[1] = data[1].replace("/p1", "/xx")
        open(path, "w", encoding="utf-8").write("\n".join(data) + "\n")
        assert w.verify_chain() is False


def test_realpath_isolated_and_device_bound():
    rp = RealPath(ttl_seconds=10)
    assert "error" in rp.login("deviceA")          # not enrolled
    rp.enroll_device("deviceA")
    assert "step_up" in rp.login("deviceA", unusual=True)  # unusual -> step up
    token = rp.login("deviceA")["token"]
    assert rp.access(token, "deviceA")["ok"] is True
    assert "error" in rp.access(token, "deviceB")  # stolen token, wrong device


def test_server_enforces_time_floor():
    cfg = VyuhaConfig(modulus_bits=1024, puzzle_squarings=5_000,
                      time_floor_seconds=999, rotation_seconds=1,
                      watcher_log=os.path.join(tempfile.mkdtemp(), "w.jsonl"))
    svc = VyuhaService(cfg, Watcher(cfg.watcher_log))
    issued = svc.on_touch("9.9.9.9", "/.env")
    session = issued["session"]
    # correct answer, but submitted immediately -> rejected as too early
    ans = svc._sessions[session]["answer"]
    res = svc.on_collect("9.9.9.9", session, ans)
    assert res.get("error") == "too early"


def test_server_serves_only_after_floor_and_answer():
    cfg = VyuhaConfig(modulus_bits=1024, puzzle_squarings=5_000,
                      time_floor_seconds=0, rotation_seconds=1,
                      watcher_log=os.path.join(tempfile.mkdtemp(), "w.jsonl"))
    svc = VyuhaService(cfg, Watcher(cfg.watcher_log))
    issued = svc.on_touch("9.9.9.9", "/.env")
    session = issued["session"]
    ans = svc._sessions[session]["answer"]
    assert svc.on_collect("9.9.9.9", session, ans + 1).get("error") == "incorrect"
    out = svc.on_collect("9.9.9.9", session, ans)
    assert "content" in out and "fake" in out["notice"]


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_")]
    passed = 0
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(fns)} tests passed")


if __name__ == "__main__":
    _run_all()

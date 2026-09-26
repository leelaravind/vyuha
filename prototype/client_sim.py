"""Simulated visitor for testing the running decoy server.

Start the server first:   python -m vyuha.server
Then run:                 python client_sim.py

It touches a decoy, receives a puzzle, solves it, and tries to collect. With the
default 180s time floor the collect is rejected as "too early" -- which is the
point: the visitor has been detected and delayed. Use --floor-test to run the
server with a tiny floor if you want to see a full successful collect.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request

from vyuha.timelock import Puzzle, solve

BASE = "http://127.0.0.1:8899"


def _get(path: str) -> dict:
    with urllib.request.urlopen(BASE + path) as r:
        return json.load(r)


def _post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main() -> None:
    print("visitor: touching decoy /.env ...")
    resp = _get("/.env")
    if "session" not in resp:
        print("  server said:", resp)
        return
    puzzle = Puzzle(int(resp["n"], 16), int(resp["base"], 16), resp["t"])
    print(f"  got a puzzle: t={puzzle.t:,} squarings")

    print("visitor: solving (this is the time cost) ...")
    t0 = time.perf_counter()
    answer = solve(puzzle)
    print(f"  solved in {time.perf_counter()-t0:.2f}s")

    print("visitor: submitting answer to /collect ...")
    result = _post("/collect", {"session": resp["session"], "answer": hex(answer)})
    print("  server responded:")
    print("   ", json.dumps(result, indent=2).replace("\n", "\n    "))


if __name__ == "__main__":
    main()

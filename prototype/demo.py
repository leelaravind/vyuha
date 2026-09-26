"""Self-contained demo of the Vyuha defensive layer (no network).

It shows the three pieces working together against a simulated visitor:

  1. A visitor touches a decoy.
  2. The watcher records it and raises a silent alert (in seconds).
  3. The visitor must spend sequential time on a time-lock puzzle.
  4. By the time they solve it, the value behind the decoy has rotated, so what
     they obtain is already stale -- and it was fake to begin with.

Run:  python demo.py

Parameters here are tiny so the demo finishes in seconds. Real deployments use a
2048-bit modulus, a ~180s server-side time floor, and a rotation shorter than
that floor (see ../docs/design.md).
"""

from __future__ import annotations

import time

from vyuha import PuzzleMaker, RotatingVault, Watcher, solve


def main() -> None:
    # --- setup (the defender) ---------------------------------------------
    maker = PuzzleMaker(bits=1024)              # small, for a fast demo
    vault = RotatingVault(rotation_seconds=1.0, label="svc")  # rotates every 1s
    alerts: list[dict] = []
    watcher = Watcher(
        log_path="watcher_log.jsonl",
        alert=lambda entry: alerts.append(entry),  # out-of-band delivery
    )

    print("Vyuha demo -- a visitor reaches a decoy that no real user would touch.\n")

    # --- a visitor touches a decoy ----------------------------------------
    contact_time = time.time()
    watcher.record({"kind": "decoy_touched", "which": "/fake-admin", "ip": "203.0.113.9"})
    alert_latency = time.time() - contact_time
    print(f"[watcher] silent alert raised in {alert_latency*1000:.1f} ms "
          f"(total alerts: {len(alerts)})")

    # The value the visitor is 'after' right now (fake, and about to rotate):
    value_at_contact = vault.value()
    print(f"[vault]   value at moment of contact: {value_at_contact}")

    # --- the visitor is made to spend sequential time ---------------------
    puzzle, _ = maker.make(t=400000)   # tiny t for the demo
    print("[cost]    visitor must solve a time-lock puzzle before anything is returned...")
    t0 = time.perf_counter()
    answer = solve(puzzle)
    spent = time.perf_counter() - t0
    print(f"[cost]    visitor spent {spent:.2f}s of sequential work")

    # --- by now the value has rotated ------------------------------------
    time.sleep(1.1)  # ensure at least one rotation has passed for the demo
    age = vault.age_epochs(value_at_contact)
    print(f"[vault]   the value they were after is now {age} rotation(s) old "
          f"-> {'STALE, useless' if age else 'still current'}")
    print(f"[vault]   (and it was fake the whole time)\n")

    # --- integrity of the record -----------------------------------------
    ok = watcher.verify_chain()
    print(f"[watcher] tamper-evident log intact: {ok}")
    print("\nOutcome: detected in milliseconds, attacker's time burned, prize expired.")


if __name__ == "__main__":
    main()

"""Command-line entry point for Vyuha.

    python -m vyuha.cli serve        # run the decoy server (production defaults)
    python -m vyuha.cli demo         # run the server with fast demo parameters
    python -m vyuha.cli selftest     # run the test suite
    python -m vyuha.cli tiers        # print the default value tiers

All commands are lab-only and bind to loopback.
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

from .config import VyuhaConfig
from .tiers import DEFAULT_TIERS, TierMap
from .server import serve


def _demo_config() -> VyuhaConfig:
    return VyuhaConfig(modulus_bits=1024, puzzle_squarings=300_000,
                       time_floor_seconds=0, rotation_seconds=1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vyuha")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("serve", help="run the decoy server (production defaults)")
    sub.add_parser("demo", help="run the decoy server with fast demo parameters")
    sub.add_parser("selftest", help="run the test suite")
    sub.add_parser("tiers", help="print the default value tiers")
    args = parser.parse_args(argv)

    if args.cmd == "serve":
        serve(VyuhaConfig())
    elif args.cmd == "demo":
        serve(_demo_config())
    elif args.cmd == "tiers":
        for name, t in DEFAULT_TIERS.items():
            print(f"{name:10s} rotation={t.rotation_seconds:>5.0f}s  "
                  f"floor={t.time_floor_seconds:>5.0f}s  squarings={t.puzzle_squarings:,}")
    elif args.cmd == "selftest":
        tests_dir = Path(__file__).resolve().parent.parent / "tests"
        for name in ("test_core.py", "test_product.py", "test_robustness.py"):
            print(f"--- {name} ---")
            runpy.run_path(str(tests_dir / name), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())

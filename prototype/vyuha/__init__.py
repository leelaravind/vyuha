"""Vyuha: a defensive deception layer (lab prototype, v1).

Confidential. Runs locally only (loopback); not for internet exposure in v1.

Modules:
  timelock  -- the sequential time cost placed in front of decoys
  vault     -- rotating, fake, expiring values behind decoys
  watcher   -- isolated tamper-evident recorder
  alerting  -- out-of-band alert sinks
  schema    -- the structured event schema
  decoys    -- plausible fake content per decoy path
  tiers     -- value tiers (the crown-value rule)
  allowlist -- known-good sources / honest-mistake handling
  ratelimit -- per-source puzzle caps
  metrics   -- detection latency and counters
  config    -- all tunables
  server    -- the decoy HTTP server
  realpath  -- the separate, isolated legitimate-user path

Defensive only. It acts on its own decoys and records what happens on them. It
performs no action against any external system, and does no trace-back.
"""

from .timelock import Puzzle, PuzzleMaker, solve, derive_base
from .vault import RotatingVault
from .watcher import Watcher
from .config import VyuhaConfig
from .tiers import Tier, TierMap, DEFAULT_TIERS
from .allowlist import Allowlist
from .ratelimit import RateLimiter
from .metrics import Metrics
from .realpath import RealPath

__all__ = [
    "Puzzle", "PuzzleMaker", "solve", "derive_base",
    "RotatingVault", "Watcher", "VyuhaConfig",
    "Tier", "TierMap", "DEFAULT_TIERS",
    "Allowlist", "RateLimiter", "Metrics", "RealPath",
]

__version__ = "0.1.0"

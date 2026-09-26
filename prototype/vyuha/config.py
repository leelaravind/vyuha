"""Configuration for a Vyuha deployment.

All tunables live here. Values scale with the worth of the protected asset via
tiers (see tiers.py): the more valuable, the shorter the rotation and the longer
the time cost.

Backward compatible: the scalar rotation/floor/puzzle fields define a single
default tier when no explicit tier_map is supplied.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field

from .tiers import Tier, TierMap


@dataclass
class VyuhaConfig:
    # --- cryptographic strength ---
    modulus_bits: int = 2048

    # --- default (single-tier) time cost + rotation ---
    time_floor_seconds: float = 180.0
    puzzle_squarings: int = 300_000_000
    rotation_seconds: float = 60.0

    # --- decoy field ---
    decoy_paths: tuple[str, ...] = (
        "/.env",
        "/.git/config",
        "/backup/db.sql",
        "/admin/api-keys",
        "/internal/credentials.json",
    )
    # NOTE: v1 implements a single ring (touch -> puzzle -> content). Multi-ring
    # depth from the original scope is deferred; see docs/prd.md section 10.

    # --- value tiers (optional; overrides the scalar fields when set) ---
    tier_map: TierMap | None = None
    path_tier: dict[str, str] = field(default_factory=dict)

    # --- per-deployment uniqueness (PRD FR-9) ---
    deployment_seed: bytes = field(default=b"", repr=False)

    # --- known-good sources (PRD FR-11) ---
    known_good: set[str] = field(default_factory=set)

    # --- abuse limits ---
    max_puzzles_per_ip: int = 20
    max_request_body_bytes: int = 4096       # cap on POST bodies
    # A session (issued puzzle) expires at max(ttl_multiplier * floor, min_ttl).
    # Expiry frees the source's rate-limit slot and bounds memory.
    session_ttl_multiplier: float = 3.0
    session_min_ttl_seconds: float = 300.0

    # --- server ---
    host: str = "127.0.0.1"
    port: int = 8899

    # --- logging / alerting ---
    watcher_log: str = "watcher_log.jsonl"
    alert_log: str = "alerts.jsonl"

    # --- secrets (filled at startup) ---
    server_key: bytes = field(default=b"", repr=False)

    def effective_tier_map(self) -> TierMap:
        """Return the tier map, building a single default tier if none was set."""
        if self.tier_map is not None:
            return self.tier_map
        default = Tier(
            "default",
            rotation_seconds=self.rotation_seconds,
            time_floor_seconds=self.time_floor_seconds,
            puzzle_squarings=self.puzzle_squarings,
        )
        return TierMap({"default": default}, self.path_tier, default_tier="default")

    def ensure_secrets(self) -> None:
        if not self.server_key:
            self.server_key = secrets.token_bytes(32)
        if not self.deployment_seed:
            self.deployment_seed = secrets.token_bytes(16)

    def validate(self) -> None:
        # Building the tier map validates each tier's rotation < floor rule.
        self.effective_tier_map()
        if self.host not in ("127.0.0.1", "::1", "localhost"):
            raise ValueError(
                "v1 is lab-only: host must be loopback (127.0.0.1). Refusing to "
                "bind a non-loopback address."
            )

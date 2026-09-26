"""Value tiers: the crown-value rule made concrete (PRD FR-10, FR-12).

The more valuable a protected asset, the tighter its configuration: a shorter
rotation interval and a longer required time cost. A deployment defines one or
more tiers, and each decoy path is assigned to a tier.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    name: str
    rotation_seconds: float      # how often the fake value behind the decoy changes
    time_floor_seconds: float    # minimum wall-clock wait before anything is returned
    puzzle_squarings: int        # sequential busy-work target

    def validate(self) -> None:
        if self.time_floor_seconds > 0 and self.rotation_seconds >= self.time_floor_seconds:
            raise ValueError(
                f"tier {self.name}: rotation must be shorter than the time floor"
            )


# Default tiers, tightest first. Higher value => shorter rotation, longer wait.
DEFAULT_TIERS: dict[str, Tier] = {
    "crown":     Tier("crown",     rotation_seconds=15.0, time_floor_seconds=300.0, puzzle_squarings=500_000_000),
    "sensitive": Tier("sensitive", rotation_seconds=30.0, time_floor_seconds=180.0, puzzle_squarings=300_000_000),
    "standard":  Tier("standard",  rotation_seconds=60.0, time_floor_seconds=90.0,  puzzle_squarings=150_000_000),
}


class TierMap:
    """Maps decoy paths to tiers and validates the set."""

    def __init__(self, tiers: dict[str, Tier], path_tier: dict[str, str],
                 default_tier: str = "standard"):
        self.tiers = tiers
        self.path_tier = path_tier
        self.default_tier = default_tier
        for t in tiers.values():
            t.validate()
        if default_tier not in tiers:
            raise ValueError("default_tier must be one of the defined tiers")

    def for_path(self, path: str) -> Tier:
        return self.tiers[self.path_tier.get(path, self.default_tier)]

"""Record schema: the structured events the watcher logs.

Every interaction with the decoy field becomes one event. Events are plain
dicts with a fixed set of fields so they can be reviewed, counted, and exported
for incident reporting. The watcher wraps each event in a hash-chain entry
(see watcher.py), so this schema is only the inner payload.

Design goals for the schema:
  * Enough to reconstruct what happened and when.
  * Nothing that requires touching the visitor's systems to collect.
  * Stable field names, so downstream tooling does not break.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

# Event kinds
DECOY_TOUCHED = "decoy_touched"      # a decoy path was requested
PUZZLE_ISSUED = "puzzle_issued"      # a time-lock puzzle was handed out
PUZZLE_SOLVED = "puzzle_solved"      # a correct answer arrived
EARLY_ANSWER = "early_answer"        # an answer arrived before the time floor
RATE_LIMITED = "rate_limited"        # too many puzzles from one source
DECOY_VALUE_SERVED = "value_served"  # a (fake, stale) value was returned
REAL_PATH_ANOMALY = "real_path_anomaly"  # something odd on the legitimate path


def make_event(
    kind: str,
    *,
    source_ip: str = "",
    path: str = "",
    session: str = "",
    detail: dict[str, Any] | None = None,
) -> dict:
    """Build one schema-conformant event payload.

    Fields:
      event_id   -- unique id for this event
      kind       -- one of the constants above
      ts         -- unix timestamp (seconds)
      source_ip  -- the connecting address (last hop; not an identity)
      path       -- which decoy path was involved, if any
      session    -- opaque session id tying related events together
      detail     -- kind-specific extra fields (never real secrets)
    """
    return {
        "event_id": uuid.uuid4().hex,
        "kind": kind,
        "ts": time.time(),
        "source_ip": source_ip,
        "path": path,
        "session": session,
        "detail": detail or {},
    }

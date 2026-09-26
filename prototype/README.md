# Vyuha — v1 (full PRD build, lab scale)

> Confidential. **Local lab use only — binds to loopback (127.0.0.1) and refuses
> any other address.** Defensive only: it acts on its own decoys and records
> activity on them. No action against external systems, no trace-back, no
> "hack-back." See `../docs/` (overview, product, prd, design, references,
> requirements-traceability).

## What it is
A working implementation of the full v1 PRD at lab scale: a decoy HTTP server
that detects any visitor instantly, makes them spend real sequential time (sized
by the asset's value tier), returns only fake, already-expired values, records
everything to a tamper-evident log with out-of-band alerting, tracks metrics, and
keeps a separate isolated path for genuine users. Every PRD requirement (FR-1..12,
NFR-1..7) is implemented and traced in `../docs/requirements-traceability.md`.

## Modules
| File | Role |
|---|---|
| `vyuha/timelock.py` | RSW time-lock puzzle (the sequential time cost) |
| `vyuha/vault.py` | Rotating, fake, expiring values (deployment-seeded) |
| `vyuha/watcher.py` | Tamper-evident (hash-chained) recorder |
| `vyuha/alerting.py` | Out-of-band alert sinks (console, file, fan-out, collecting) |
| `vyuha/schema.py` | Structured event schema |
| `vyuha/decoys.py` | Plausible fake content per path (deployment-unique) |
| `vyuha/tiers.py` | Value tiers — the crown-value rule (rotation/floor/cost) |
| `vyuha/allowlist.py` | Known-good sources; honest-mistake handling |
| `vyuha/ratelimit.py` | Per-source puzzle caps (limits parallel solving) |
| `vyuha/metrics.py` | Detection latency + counters |
| `vyuha/config.py` | All tunables; enforces loopback + rotation<floor |
| `vyuha/server.py` | The decoy HTTP server |
| `vyuha/realpath.py` | Separate, isolated legitimate-user path |
| `vyuha/cli.py` | Command line: serve / demo / selftest / tiers |
| `demo.py`, `client_sim.py`, `run_demo_server.py` | Demos and a test visitor |
| `tests/test_core.py`, `tests/test_product.py`, `tests/test_robustness.py` | 23 tests (7 core + 9 product + 7 robustness) |

## Requirements
Python 3.11+ (developed on 3.14). No third-party packages.

## Commands
```
cd prototype
python -m vyuha.cli selftest     # run all tests (23)
python -m vyuha.cli tiers        # show the value tiers
python -m vyuha.cli demo         # run the server with fast demo params (port 8899)
python -m vyuha.cli serve        # run with production defaults
python demo.py                   # in-process demo, no network
```
With the server running, in another terminal:
```
python client_sim.py             # touch a decoy, solve, collect fake content
```
Endpoints: `GET /<decoy path>`, `POST /collect`, `GET /health`, `GET /metrics`.

## Production vs demo
- **Demo:** 1024-bit modulus, tiny puzzle, `time_floor_seconds=0` so a full
  collect is quick to see.
- **Production (`config.py` / `tiers.py` defaults):** 2048-bit modulus; tiers with
  90–300 s floors and rotation always shorter than the floor. The **server-side
  time floor is the real guarantee**, independent of the visitor's hardware.

## Boundaries (fixed)
- No offensive capability; no trace-back / de-anonymisation.
- No real secrets or data — every value is fake and rotating.
- Loopback only in v1.

## Deferred to a real build (see `../docs/prd.md` §10)
Internet-scale concurrency and a shared datastore; richer, human-convincing decoy
content; security testing against live adversaries; production hardening of the
watcher's isolation.

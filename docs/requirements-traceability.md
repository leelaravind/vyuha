# Vyuha — Requirements Traceability (PRD → code → test)

> Confidential. Maps every PRD requirement to the module that implements it and
> the test that checks it. v1, lab scale. See `prd.md` for the requirements.

## Functional requirements
| ID | Requirement | Implemented in | Verified by |
|---|---|---|---|
| FR-1 | Decoys placed off every legitimate path | `server.py` (decoy paths), `config.py` | `test_product.full_flow…` |
| FR-2 | Sequential time cost before returning anything | `timelock.py` | `test_core.timelock_issuer_matches_solver` |
| FR-3 | Server-side time floor; reject early answers | `server.py` `on_collect` | `test_core.server_enforces_time_floor` |
| FR-4 | Rotation faster than the time cost | `tiers.py` `validate`, `config.py` | `test_product.tier_rotation_must_be_shorter…` |
| FR-5 | Values behind decoys are fake | `decoys.py`, `vault.py` | `test_core.server_serves_only_after…` |
| FR-6 | Tamper-evident record | `watcher.py` (hash chain) | `test_core.watcher_hash_chain_detects_tampering` |
| FR-7 | Silent, out-of-band alert; decoy behaves normally | `alerting.py`, `watcher.py` | live run (`alerts.jsonl`) |
| FR-8 | Separate, hidden, isolated legitimate path | `realpath.py` | `test_core.realpath_isolated_and_device_bound` |
| FR-9 | Per-deployment uniqueness | `vault.py` (seed), `decoys.py` `_seeded` | `test_product.FR9_uniqueness_across_deployments` |
| FR-10 | Tightness scales with asset value | `tiers.py`, `config.py` | `test_product.FR10_FR12_value_tiers…` |
| FR-11 | Honest mistake → review, not penalty | `allowlist.py`, `server.py` | `test_product.FR11_known_good_touch…` |
| FR-12 | Multiple value tiers | `tiers.py` `DEFAULT_TIERS`, `TierMap` | `test_product.FR10_FR12_value_tiers…` |

## Non-functional requirements
| ID | Requirement | Implemented in | Verified by |
|---|---|---|---|
| NFR-1 | Detection latency 1–5 s | `metrics.py`, `server.py` | live `/metrics` (~4 ms measured) |
| NFR-2 | False-alarm rate near zero | `allowlist.py`, `metrics.py` | `test_product.NFR1_NFR2_metrics_summary` |
| NFR-3 | Issue/verify cost in ms | `timelock.py` (phi shortcut) | research §57 (~2 ms) |
| NFR-4 | Adversary time per attempt | `tiers.py` floors (90–300 s) | design §54 |
| NFR-5 | Watcher isolation | `alerting.py` (out-of-band sinks) | live run |
| NFR-6 | Record integrity | `watcher.py` `verify_chain` | `test_core.watcher_hash_chain…` |
| NFR-7 | Lab-only; loopback | `config.py` `validate` | `test_product.config_refuses_non_loopback` |

## Abuse mitigations
| Concern | Implemented in | Verified by |
|---|---|---|
| Parallel solving of many puzzles | `ratelimit.py`, `server.py` | `test_product.rate_limiter…`, `…rate_limit_end_to_end` |

## Robustness (added after code review)
| Defect found | Fix | Verified by |
|---|---|---|
| Single-threaded server; one slow client blocked all | `ThreadingHTTPServer` | live concurrent run |
| Race on session table | `threading.Lock` in `server.py` | `test_robustness.concurrent_touches…` |
| Rate-limit slot leaked by abandoned sessions | session expiry + `sweep_expired` | `…expired_session_frees_rate_slot` |
| Session table grew without bound | expiry sweep | `…expired_session_is_rejected_on_collect` |
| Double release on repeat collect | pop-then-release under lock | `…double_collect_does_not_double_release` |
| Unbounded POST body | `max_request_body_bytes` → HTTP 413 | `…oversized_post_body_is_rejected` |
| Unbounded metrics list; unpruned real-path sessions | rolling window; `prune()` | `…metrics_latency_window…`, `…realpath_prunes…` |

## Coverage summary
- **All 12 functional and 7 non-functional requirements** are implemented at lab
  scale and covered by a test or a demonstrated live run.
- Tests: `test_core.py` (7) + `test_product.py` (9) + `test_robustness.py` (7) = **23 passing**.

## Not covered at v1 (deferred, see `prd.md` §7 risks and §10 open questions)
- Internet-scale concurrency and a shared datastore.
- Rich, human-convincing decoy content (the hardest problem, design §46).
- Real-world security testing against live adversaries.
- Production hardening of the watcher's isolation.

## Spec v0.2 additions (specified, not yet built)
| ID | Requirement | Planned module | Milestone |
|---|---|---|---|
| FR-13..15 | Decoy realism, liveness, layout uniqueness | `decoys.py` (template engine), `config.py` | M4 |
| FR-16 | Response hook (pre-approved containment) | new `response.py` | M6 |
| FR-17 | Puzzle modulus persistence + rotation | `timelock.py`, `config.py` | M7 |
| FR-18 | Signed evidence bundle | new `evidence.py` | M7 |
| FR-19 | Passkey / FIDO2 real path | `realpath.py` | M7 |
| FR-20 | Shared state for sessions / rate limits | `server.py`, `ratelimit.py` | M7 |
| FR-21 | Fingerprint metric | `metrics.py` | M5 |
| NFR-8 | True out-of-band watcher (separate host) | `watcher.py`, `alerting.py` | M6 |
| NFR-9..11 | Red-team gate, continuous measurement, restraint | process / review | M5+ |

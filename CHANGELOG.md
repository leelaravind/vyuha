# Changelog

## Spec v0.2 — 2026-09-26
Specification update following an engineering review. Code remains at
implementation 0.1.0 (the v0.1 requirement set); v0.2 items are specified, not built.

### Added requirements
- FR-13 Decoy realism (consistent, templated, per-deployment content)
- FR-14 Decoy liveness (history and ongoing activity)
- FR-15 Layout uniqueness (paths and structure unique per deployment)
- FR-16 Response hook (pre-approved containment on first contact)
- FR-17 Puzzle modulus persistence and rotation
- FR-18 Signed evidence bundle for regulatory reporting
- FR-19 Passkey / FIDO2 legitimate path
- FR-20 Shared state for multi-instance deployments
- FR-21 Fingerprint metric from red-team runs
- NFR-8 True out-of-band watcher (separate host, one-way channel)
- NFR-9 Adversarial validation gate before production
- NFR-10 Continuous measurement and review
- NFR-11 Restraint gate against feature creep

### Clarified
- Rotation applies to the fake values behind decoys only; real-asset key
  rotation is out of scope and must exist separately.
- The deployment seed is a secret (all decoy values derive from it).
- FR-7 and NFR-5 are met at lab grade (same host); NFR-8 specifies the real target.
- FR-9 currently covers values only; FR-15 extends it to layout.

### Reprioritised milestones
- M4 (realism) and M5 (red-team fingerprint exercise) are now the next work,
  ahead of any new mechanism.

## Spec v0.1 / implementation 0.1.0 — 2026-09-26
- Initial PRD (FR-1..12, NFR-1..7), design, product doc, references.
- v1 lab prototype: time-lock cost, rotating fake values, tamper-evident
  watcher, out-of-band sinks, value tiers, allowlist, rate limits, metrics,
  isolated real path, CLI. 23/23 tests.
- Engineering review fixes: threaded server, locked session table, session
  expiry (rate-slot leak), POST body cap, bounded metrics, real-path pruning.

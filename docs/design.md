# Vyuha — Design Notes (v1)

> Confidential working notes. Local only. Section references like [§54] point to
> `../research-log.md`.

## 1. Goals and success measures [§54]
| Measure | Target |
|---|---|
| Detection time | 1–5 seconds from first activity on a decoy |
| False alarms | Near zero (legitimate users never reach decoys) |
| Record quality | Complete, tamper-evident log of every decoy session |

Detection is fast because activity on a decoy is a binary event: there is no
legitimate reason to be there, so no analysis is needed to raise a flag.

## 2. Threat model [§53]
- Defends against intruders who gain access and against passive listeners on the
  network.
- Two broad classes of adversary: the common majority, handled well by standard
  defences, and rare targeted adversaries who use methods that public defences do
  not anticipate. Vyuha is aimed at the gap the standard defences leave.
- Crown-value rule: the more valuable the protected asset, the tighter the
  configuration and the more often its secrets are rotated.
- Working assumptions: rules of engagement will be broken; there is always some
  other way in; the realistic goal is to make intrusion slow, costly and visible.

## 3. Components
| Component | Role |
|---|---|
| Decoy field | Resources placed where no legitimate workflow leads. Any access is a signal. |
| Cost function | A challenge that requires a fixed amount of sequential time before anything is returned [§57]. |
| Rotating vault | The values behind a decoy change on a schedule, so anything obtained is already stale [§8]. |
| Watcher | A separate, isolated component that records decoy activity and raises a silent alert [§47]. |
| Legitimate path | A separate, hidden, well-guarded route for real users, kept completely apart from the decoy field [§52]. |

## 4. The cost function [§57]
- Decision: use an RSW time-lock puzzle in which the server holds the secret and
  can issue and check puzzles cheaply (about 2 ms each), while a client must spend
  sequential time to solve one.
- A server-side time floor is the real guarantee: each puzzle carries a signed
  issue time, and answers returned before the floor (target: 180 seconds) are
  rejected. This holds regardless of the client's hardware.
- Puzzles are single-use, tied to a session, and expire, so they cannot be reused
  or handed to a faster solver.
- Because legitimate users never touch the decoy field, the puzzle is tuned only
  against the fastest adversary hardware — a simplification most deployments do
  not get to make.

## 5. Rotation and expiry [§8][§54] — clarified in spec v0.2
- The fake values behind decoys rotate faster than the puzzle takes to solve (for
  example, every ~60 s against a 180 s floor). Anything reached through the decoy
  field has therefore already changed several times over — and is fake to begin with.
- **How it works:** nothing is scheduled or stored. A value is *derived* from the
  current time window (`epoch = now // rotation_seconds`) and a per-deployment
  secret, so it changes automatically when the window changes. Staleness of any
  presented value is provable (`age_epochs`).
- **Scope, stated plainly:** this rotates the *fake* decoy values only. It does not
  rotate any genuine key. Real-asset key rotation is a separate control the
  organisation must already run (PRD non-goals, v0.2).
- **Known gaps (v0.2 requirements):** the puzzle modulus is generated per process
  and never rotated — FR-17 specifies persistence and scheduled rotation. The
  deployment seed must be treated as a secret, since every past and future decoy
  value derives from it.
- **Clock dependence:** rotation is wall-clock based; a clock jump shifts epochs.
  Harmless for fake values, but the host clock should be disciplined (NTP).

## 6. The legitimate-user path [§52]
- Decoys sit only where real work never goes, so honest users have no reason to
  meet them.
- The real entrance is not visible from the open network; only known devices can
  reach it.
- Access uses phishing-resistant credentials that also verify the service to the
  user, so a fake copy of the service cannot accept them.
- Every session is checked (identity, device, behaviour) and access is short-lived
  and device-bound, so a stolen session is useless elsewhere and expires quickly.
- If a signal looks slightly off, ask for one extra confirmation rather than
  locking the user out.
- Edge case: if an honest employee touches a decoy by mistake, it is handled
  quietly as an alert for review, never an automatic penalty.

## 7. Insider handling [§55]
Multi-person approval is kept, with measures to keep the second check genuine,
because in practice these controls fail for human reasons, not technical ones:
- Show the real risk at the moment of approval, so it is not a blind click.
- Rotate and randomise the second approver, so no fixed pair can quietly agree.
- Watch the approvers' own behaviour, not only the requesters'.
- No standing bypass: emergencies are allowed but logged and reviewed afterwards.
- Occasional review-only test requests that a careful approver should question.
- Least privilege and just-in-time access, so any single insider holds little,
  and only briefly.

## 8. Scope of v1 [§53]
In scope: one protected asset; a small decoy field with the cost function and
rotating vault; the isolated watcher with a silent alert; the separate legitimate
path. Runs only in a local lab.

Later: multiple value tiers with different rotation speeds; full network
segmentation; the human-like responder; broader deployment.

## 9. Open items before build
- Exactly what each decoy and the watcher record (a log schema).
- Which time-lock construction to implement first.
- The formation/weapon catalogue from the epics (background research, not a
  blocker).

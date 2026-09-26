# Vyuha — Product Requirements Document (PRD)

> Confidential working notes. Local only. Status: design stage, not built.
> Version 0.1 · 2026-09-26. Companions: `product.md`, `design.md`, `references.md`.

---

## 1. Overview
Vyuha is a defensive deception layer for early intrusion detection. It places
decoy resources off every legitimate path, so any activity on them is a
high-confidence sign of an intruder. On contact it slows the visitor, ensures
anything reached is stale and fake, and raises a silent alert to an isolated
watcher within seconds.

## 2. Problem statement
Intruders move in seconds; organisations take a median of ~11 days to detect
them. Standard controls stop the common majority of attacks but leave a gap
against targeted adversaries and during the long silent period after a breach.
Vyuha closes that detection gap.

## 3. Goals and non-goals
**Goals**
- Detect activity on a decoy within 1–5 seconds.
- Keep false alarms near zero.
- Produce a complete, tamper-evident record of every decoy session.
- Never disrupt legitimate users.

**Non-goals**
- Not a firewall, antivirus, or identity system (it sits above those).
- Not offensive: no action against an intruder's systems, no "hack-back."
- Not a de-anonymisation tool: naming a person is for law enforcement.
- Not a replacement for patching or MFA.

## 4. Users and use cases
| User | Use case |
|---|---|
| Security team at an org with a high-value asset | Get an instant, trustworthy alert the moment someone probes the crown jewel |
| Incident responder | Receive a clean, timely record to act on and to meet reporting deadlines |
| Security engineer | Deploy an early-warning layer above existing controls without disrupting users |

## 5. Requirements

### 5.1 Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Present decoy resources placed off every legitimate path | Must |
| FR-2 | Require a fixed sequential time cost before returning anything from a decoy | Must |
| FR-3 | Enforce the time floor server-side via a signed issue time; reject early answers | Must |
| FR-4 | Rotate the values behind decoys faster than the time cost can be solved | Must |
| FR-5 | Ensure values behind decoys are fake and never expose real data | Must |
| FR-6 | Record every decoy session to an isolated watcher, tamper-evident | Must |
| FR-7 | Raise a silent, out-of-band alert on first contact; decoy keeps behaving normally | Must |
| FR-8 | Keep a separate, hidden, guarded path for legitimate users, fully isolated from decoys | Must |
| FR-9 | Make each deployment unique so decoys share no cross-site fingerprint | Should |
| FR-10 | Scale tightness (rotation interval, time cost) with asset value | Should |
| FR-11 | Handle an honest user who touches a decoy by mistake as a review alert, not a penalty | Should |
| FR-12 | Support multiple value tiers with different rotation speeds | Could (later) |

### 5.2 Non-functional requirements
| ID | Requirement | Target |
|---|---|---|
| NFR-1 | Detection latency | 1–5 seconds |
| NFR-2 | False-alarm rate | Near zero |
| NFR-3 | Cost to issue/verify a time challenge | Milliseconds |
| NFR-4 | Adversary time spent per attempt | Minutes or more |
| NFR-5 | Watcher isolation | Unreachable from the decoy field |
| NFR-6 | Record integrity | Tamper-evident, verifiable |
| NFR-7 | Deployment safety | Lab-only until validated; never internet-exposed in v1 |

### 5.3 Security and compliance
- Defensive-only boundary is a hard constraint (see non-goals).
- Design, decoy locations, keys and schedules are confidential.
- Records should support breach-reporting deadlines (CERT-In 6h, GDPR 72h, SEC 4
  business days) by being timely and complete.
- Aligns with MITRE Engage / D3FEND (Deceive, Isolate, Detect) and NIST CSF 2.0
  Detect/Respond functions.

## 6. Assumptions and dependencies
- Standard controls (MFA, endpoint protection, logging) already exist; Vyuha is a
  layer above them.
- The time cost uses an RSW time-lock puzzle with a server-held secret; the
  server-side time floor is the real guarantee (see `design.md` §4).
- The hardest dependency is realistic decoy content.

## 7. Risks
| Risk | Mitigation |
|---|---|
| Decoys look fake and are recognised | Uniqueness per deployment; realistic, lived-in content |
| Adversary uses faster hardware to cut the time cost | Server-side time floor, independent of client hardware |
| Adversary solves many decoys in parallel | Rate-limit challenges per identity |
| Watcher or responder is targeted | Full isolation; out-of-band alerting |
| Insider abuses legitimate path | Multi-person approval kept genuine (see `design.md` §7) |

## 8. Success metrics
- Detection latency measured at 1–5 s in validation.
- False-alarm rate at or near zero over the test period.
- Median adversary time-per-attempt in minutes.
- 100% of decoy sessions captured with verifiable integrity.

## 9. Milestones
| Milestone | Deliverable |
|---|---|
| M0 | Design complete (done) |
| M1 | Record/log schema defined |
| M2 | v1 prototype in a lab (cost function, vault, decoy field, watcher) |
| M3 | Validation against simulated adversaries; detection-time measurement |
| M4 | Hardening (uniqueness, isolation, realistic content) |
| M5 | Expansion (value tiers, segmentation, wider deployment) |

## 10. Open questions
- Exact fields and format of the record/log schema (M1).
- Which time-lock construction to implement first (RSW chosen; parameters TBD).
- How decoy content is generated and kept consistent and current.

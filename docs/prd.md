# Vyuha — Product Requirements Document (PRD)

> Confidential working notes. Local / private repo only.
> **Spec version 0.2** · 2026-09-26 (supersedes 0.1). Changes listed in `../CHANGELOG.md`.
> Companions: `product.md`, `design.md`, `references.md`, `requirements-traceability.md`.
> Implementation status: the v0.1 requirement set (FR-1..12, NFR-1..7) is built and
> tested at lab scale. The v0.2 additions (FR-13..21, NFR-8..11) are specified, not built.

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
- **(v0.2)** Remain indistinguishable from real systems to a skilled human reviewer.
- **(v0.2)** Turn detection into a pre-approved response, not only an alert.

**Non-goals**
- Not a firewall, antivirus, or identity system (it sits above those).
- Not offensive: no action against an intruder's systems, no "hack-back."
- Not a de-anonymisation tool: naming a person is for law enforcement.
- Not a replacement for patching or MFA.
- **(v0.2, clarified)** Not a key-rotation system for real assets. Rotation in
  Vyuha applies to the *fake* values behind decoys. Rotation of genuine keys is
  a separate control the organisation must already operate.

## 4. Users and use cases
| User | Use case |
|---|---|
| Security team at an org with a high-value asset | Get an instant, trustworthy alert the moment someone probes the crown jewel |
| Incident responder | Receive a clean, timely record and a pre-approved first response |
| Security engineer | Deploy an early-warning layer above existing controls without disrupting users |
| Red team / assessor | Test whether decoys can be told apart from real systems |

## 5. Requirements

### 5.1 Functional requirements — v0.1 set (built)
| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-1 | Present decoy resources placed off every legitimate path | Must | Built |
| FR-2 | Require a fixed sequential time cost before returning anything from a decoy | Must | Built |
| FR-3 | Enforce the time floor server-side via a signed issue time; reject early answers | Must | Built |
| FR-4 | Rotate the values behind decoys faster than the time cost can be solved | Must | Built |
| FR-5 | Ensure values behind decoys are fake and never expose real data | Must | Built |
| FR-6 | Record every decoy session to an isolated watcher, tamper-evident | Must | Built |
| FR-7 | Raise a silent, out-of-band alert on first contact; decoy keeps behaving normally | Must | Built (lab-grade) |
| FR-8 | Keep a separate, hidden, guarded path for legitimate users, fully isolated from decoys | Must | Built (stand-in) |
| FR-9 | Make each deployment unique so decoys share no cross-site fingerprint | Should | Built (values only) |
| FR-10 | Scale tightness (rotation interval, time cost) with asset value | Should | Built |
| FR-11 | Handle an honest user who touches a decoy by mistake as a review alert, not a penalty | Should | Built |
| FR-12 | Support multiple value tiers with different rotation speeds | Could | Built |

### 5.2 Functional requirements — v0.2 additions (specified)
| ID | Requirement | Priority | Rationale |
|---|---|---|---|
| FR-13 | **Decoy realism:** generate decoy content from per-deployment templates with internally consistent names, dates, versions and cross-references | Must | A decoy that looks fake is worse than none; it reveals where the traps are |
| FR-14 | **Decoy liveness:** give decoys plausible history and ongoing activity (timestamps, logs, periodic small changes) | Must | Fresh, untouched files are a fingerprint |
| FR-15 | **Layout uniqueness:** make decoy paths and structure unique per deployment, not only the values | Must | Extends FR-9; identical paths across sites are recognisable |
| FR-16 | **Response hook:** on first contact, trigger pre-approved containment steps (segment isolation, real-key rotation request, responder notification) | Should | Detection without a fast, pre-decided response wastes the time bought |
| FR-17 | **Puzzle modulus rotation:** persist the puzzle modulus and rotate it on a schedule rather than regenerating per process | Should | A long-lived modulus is a single secret; rotation limits exposure |
| FR-18 | **Evidence bundle:** export a signed, structured incident bundle suitable for CERT-In / GDPR / SEC reporting | Should | Reporting deadlines (6 h / 72 h / 4 days) reward ready evidence |
| FR-19 | **Passkey-based real path:** replace the HMAC stand-in with passkeys / FIDO2 | Should | Phishing-resistant, two-way verification |
| FR-20 | **Shared state:** move sessions and rate limits to a shared store so multiple server instances agree | Could | Needed for any multi-instance deployment |
| FR-21 | **Fingerprint metric:** record, per red-team run, how many decoys were identified as decoys and how quickly | Must | The single most important measure of whether realism is working |

### 5.3 Non-functional requirements — v0.1 set (built)
| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-1 | Detection latency | 1–5 seconds | Built (ms measured) |
| NFR-2 | False-alarm rate | Near zero | Built |
| NFR-3 | Cost to issue/verify a time challenge | Milliseconds | Built |
| NFR-4 | Adversary time spent per attempt | Minutes or more | Built |
| NFR-5 | Watcher isolation | Unreachable from the decoy field | Built (lab-grade: same host) |
| NFR-6 | Record integrity | Tamper-evident, verifiable | Built |
| NFR-7 | Deployment safety | Lab-only until validated; loopback in v1 | Built |

### 5.4 Non-functional requirements — v0.2 additions (specified)
| ID | Requirement | Target |
|---|---|---|
| NFR-8 | **True out-of-band watcher:** watcher and alert sink run on a separate host with a one-way (write-only from the decoy side) channel | An intruder with decoy-host access cannot read or delete the record |
| NFR-9 | **Adversarial validation:** decoys assessed by a red team before any production use | Fingerprint rate below an agreed threshold (proposed: <10% of decoys identified in a timed exercise) |
| NFR-10 | **Continuous measurement:** time-to-alert, attacker minutes wasted, and fingerprint rate tracked and reviewed | Reviewed at least monthly; a rising fingerprint rate blocks release |
| NFR-11 | **Restraint:** no new mechanism is added unless it improves signal reliability or decoy believability | Design review gate |

### 5.5 Security and compliance
- Defensive-only boundary is a hard constraint (see non-goals).
- Design, decoy locations, keys, schedules and the deployment seed are confidential.
  **(v0.2)** The deployment seed is a secret: with it, all past and future decoy
  values are computable.
- Records should support breach-reporting deadlines by being timely, complete and
  exportable (FR-18).
- Aligns with MITRE Engage / D3FEND (Deceive, Isolate, Detect) and NIST CSF 2.0
  Detect/Respond functions.

## 6. Assumptions and dependencies
- Standard controls (MFA, endpoint protection, logging) already exist; Vyuha is a
  layer above them.
- The time cost uses an RSW time-lock puzzle with a server-held secret; the
  server-side time floor is the real guarantee (see `design.md` §4).
- **(v0.2)** The hardest dependency is realistic, consistent, unique decoy content
  (FR-13..15). This is the product; the mechanisms are secondary.

## 7. Risks
| Risk | Mitigation |
|---|---|
| Decoys look fake and are recognised | FR-13..15 realism; FR-21 fingerprint metric; NFR-9 red-team gate |
| Adversary uses faster hardware to cut the time cost | Server-side time floor, independent of client hardware |
| Adversary solves many decoys in parallel | Rate-limit challenges per identity; FR-20 shared limits |
| Watcher or responder is targeted | NFR-8 separate host, one-way channel |
| Insider abuses legitimate path | Multi-person approval kept genuine (`design.md` §7) |
| Detection fires but nobody acts in time | FR-16 pre-approved response hook |
| Feature creep dilutes the signal | NFR-11 restraint gate |

## 8. Success metrics
- Detection latency 1–5 s in validation.
- False-alarm rate at or near zero over the test period.
- Median adversary time-per-attempt in minutes.
- 100% of decoy sessions captured with verifiable integrity.
- **(v0.2)** Fingerprint rate below threshold in red-team exercises (NFR-9).
- **(v0.2)** Time from alert to first containment action, when FR-16 is enabled.

## 9. Milestones
| Milestone | Deliverable | Status |
|---|---|---|
| M0 | Design complete | Done |
| M1 | Record/log schema defined | Done |
| M2 | v1 prototype in a lab (v0.1 requirement set) | Done — 23/23 tests |
| M3 | Validation against simulated visitors; detection-time measurement | Done (lab) |
| **M4** | **Decoy realism and layout uniqueness (FR-13..15)** | Next |
| **M5** | **Red-team fingerprint exercise (NFR-9, FR-21)** | Next |
| M6 | True out-of-band watcher (NFR-8); response hook (FR-16) | Planned |
| M7 | Modulus rotation, evidence bundle, passkeys, shared state (FR-17..20) | Planned |
| M8 | Multi-ring depth from the original scope; broader deployment | Later |

## 10. Open questions
- How decoy content is generated and kept consistent, current and unique (M4).
- The fingerprint-rate threshold that gates release (proposed <10%; to be agreed).
- Which containment actions an organisation will pre-approve for FR-16.
- Multi-ring depth (original scope) remains specified in the research log but unbuilt.

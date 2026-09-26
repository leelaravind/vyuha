# Vyuha — Product Documentation

> Confidential working notes. Local only. Status: design stage, not built.
> Companion documents: `overview.md`, `design.md`, `references.md`.
> Full research history: `../research-log.md`.

---

## 1. Product summary
Vyuha is a defensive deception layer for early intrusion detection. It places
decoy resources that no legitimate user has any reason to touch, so any activity
on them is a high-confidence sign of an intruder. When a decoy is touched, Vyuha
does three things at once: it slows the visitor down, it makes sure anything they
reach is worthless, and it raises a silent alert to a protected component within
a few seconds.

**One-line positioning:** turn the moment an intruder first probes a system from
an invisible event into an immediate, high-confidence alarm — before real damage
is done.

---

## 2. The problem
| Fact | Source |
|---|---|
| Most breaches use known, unpatched weaknesses | Equifax, WannaCry, Log4j |
| Median time to detect an intruder is ~11 days | Mandiant M-Trends 2025 |
| Fastest recorded intruder movement is ~27 seconds | CrowdStrike GTR 2026 |
| Breach-reporting deadlines are tightening | CERT-In 6h, GDPR 72h, SEC 4 business days |

The gap between how fast intruders move and how slowly they are found is the
core problem. Standard defences stop the common majority of attacks; they are
weakest against rare, targeted adversaries and against the long silent period
after a real intrusion. Vyuha is built for that gap.

---

## 3. Who it is for
- **Primary:** organisations holding a small number of high-value assets (a
  "crown jewel") who need to know the instant someone is nosing around them.
- **Secondary:** teams that already run standard controls (MFA, endpoint
  protection, logging) and want an early-warning layer above them, not a
  replacement.

Vyuha assumes the standard controls exist. It is an added layer, not a first
line of defence.

---

## 4. How it works (plain walkthrough)
1. **Decoys are placed** where no legitimate workflow leads. Because honest users
   never go there, any visitor is treated as hostile by default.
2. **A visitor who engages is slowed down.** Reaching anything requires spending
   a fixed, unavoidable amount of sequential time (a time-lock challenge). The
   server issues and checks these challenges cheaply; the visitor cannot skip the
   wait, even with more machines.
3. **Anything reached is stale and fake.** The values behind the decoys rotate on
   a schedule faster than the challenge can be solved, so anything obtained has
   already expired — and was never real to begin with.
4. **A protected watcher is alerted silently.** A separate, isolated component
   records the activity and raises an out-of-band alert within a few seconds. The
   decoy keeps behaving normally, so the visitor gets no hint they have been seen.
5. **Legitimate users are unaffected.** They use a separate, hidden, well-guarded
   route that is kept completely apart from the decoy field.

---

## 5. Core features
| Feature | What it does | Benefit |
|---|---|---|
| Decoy field | Resources placed off every legitimate path | High-confidence signal; near-zero false alarms |
| Time cost | A fixed sequential delay before anything is returned | Buys reaction time; can't be sped up by adding machines |
| Rotating vault | Values change faster than they can be reached | Anything obtained is already worthless |
| Silent watcher | Isolated recorder + out-of-band alert | Detection in seconds; the intruder is unaware |
| Separate real path | Hidden, guarded route for genuine users | Real work is never disrupted |
| Tamper-evident record | Complete, verifiable log of each session | Reliable evidence for review and reporting |

---

## 6. What Vyuha is not
- **Not a firewall, antivirus, or identity system.** It sits above those.
- **Not an offensive tool.** It acts only on its own decoys. It never touches an
  intruder's systems and does no "hack-back."
- **Not a de-anonymisation tool.** Identifying a person is a matter for law
  enforcement. Vyuha's job ends at producing a clean, timely record.
- **Not a replacement for patching or MFA.** Those stop the common attacks;
  Vyuha covers the gap they leave.

---

## 7. Success measures
| Measure | Target |
|---|---|
| Time to detect activity on a decoy | 1–5 seconds |
| False-alarm rate | Near zero |
| Attacker time spent per attempt | Minutes or more |
| Record completeness | Every decoy session fully captured, tamper-evident |

---

## 8. Deployment model
- **v1:** runs in a local lab on our own machines only. Never exposed to the
  internet until tested. One protected asset, a small decoy field, and the
  isolated watcher.
- **Later:** multiple value tiers with different rotation speeds; full network
  segmentation; a more lifelike responder; wider deployment.

---

## 9. Configuration principles
- **Value drives tightness.** The more valuable the protected asset, the shorter
  the rotation interval and the longer the required time cost.
- **Uniqueness.** Each deployment differs, so decoys cannot be recognised by a
  shared fingerprint from one site to the next.
- **Isolation.** The watcher and the real user path are unreachable from the
  decoy field; there are no shared routes, keys or accounts.

---

## 10. Assumptions and limits (honest view)
- There is always another way in; the goal is to make intrusion slow, costly and
  visible, not impossible.
- Well-resourced, targeted adversaries can absorb the time cost; against them the
  value is early warning and a clean record, not prevention.
- The hardest engineering problem is making the decoy field feel completely real;
  a decoy that looks fake is worse than none.
- Rules of engagement will be broken, so the design assumes worst case.

---

## 11. Roadmap (indicative)
| Stage | Focus |
|---|---|
| Design | Complete (see `design.md`) |
| Record schema | Define exactly what each decoy and the watcher log |
| v1 prototype | Cost function, rotating vault, decoy field, watcher, in a lab |
| Validation | Test against simulated adversaries; measure detection time |
| Hardening | Uniqueness, isolation, realistic decoy content |
| Expansion | Value tiers, segmentation, broader deployment |

---

## 12. Glossary
- **Decoy field** — resources that exist only to attract and detect intruders.
- **Time cost / time-lock challenge** — a task that requires a fixed amount of
  sequential time to complete, so it cannot be rushed with more hardware.
- **Rotating vault** — the store whose values change on a schedule so that
  anything reached is already out of date.
- **Watcher** — the isolated component that records decoy activity and raises the
  alert.
- **Crown jewel** — the small set of genuinely high-value assets being protected.
- **Vyuha** — a layered battle formation from the Mahabharata; here, the guiding
  metaphor for depth and delay.

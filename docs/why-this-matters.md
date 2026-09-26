# Why Vyuha Matters — and Why It Should Be Built

> Confidential. Written for whoever picks this project up next: a founder, a
> developer, a security lead, or a funder. It explains the case for the project
> in plain terms. The evidence is drawn from the research log and public sources
> cited in `references.md`.

---

## 1. The imbalance this project answers

Technology on the building side is advancing at extraordinary speed: AI, cloud,
connected devices, automation. The defending side has not kept pace. Not because
the ideas are missing — most breaches still exploit *known* weaknesses with
*known* fixes — but because defence is slow, human-dependent, and late.

Three numbers capture the imbalance:

| Fact | Figure | Source |
|---|---|---|
| Fastest recorded intruder movement inside a network | **27 seconds** | CrowdStrike Global Threat Report, 2026 |
| Average intruder movement | **29 minutes**, and getting faster each year | CrowdStrike, 2026 |
| Median time organisations take to *notice* an intruder | **11 days** | Mandiant M-Trends, 2025 |

An intruder needs less than a minute. The defender takes over a week to find
out. Everything else in security — patching, response, forensics, reporting —
happens inside that gap. Closing it is the single highest-leverage thing a
defensive product can do.

## 2. Why existing tools leave this gap

- **Perimeter tools** (firewalls, MFA, patching) stop the common majority of
  attacks. They are necessary. But against a targeted, well-resourced adversary
  they are the starting line, not the finish.
- **Monitoring tools** generate enormous volumes of alerts, most of them noise.
  Teams drown; real signals get missed. The problem is not too little data but
  too little *certainty*.
- **After a breach**, the damage is set by how long the intruder went unseen.
  Eleven days of freedom inside a network is eleven days of exfiltration,
  lateral movement, and persistence.

Vyuha attacks the certainty problem directly. A decoy that no legitimate user has
any reason to touch produces a signal with almost no false positives. When it
fires, it means something. That is rare in security tooling, and valuable.

## 3. Why this approach is sound

- **It is grounded in recognised frameworks.** Deception and adversary engagement
  are named tactics in MITRE Engage and MITRE D3FEND, and map to the Detect and
  Respond functions of NIST CSF 2.0. Vyuha is not an exotic idea; it is a
  disciplined implementation of an approach the field already endorses but
  rarely executes well.
- **Its guarantees do not depend on the adversary's hardware.** The minimum wait
  is enforced by the server's clock, and anything reached is fake and already
  expired by design. Faster attackers do not weaken it.
- **It never disrupts real users.** Genuine users travel a separate, isolated
  path. There is nothing for them to trip over.
- **It is defensive by construction.** It acts only on its own decoys, records
  what happens there, and hands clean evidence to the people whose job it is to
  act. It takes no action against anyone else's systems.

## 4. Why now

Regulation is converging on exactly the capability Vyuha provides — fast,
reliable detection with usable evidence:

| Regime | Deadline |
|---|---|
| India, CERT-In directions | Report within **6 hours** |
| EU GDPR / NIS2 | **72 hours** |
| US SEC disclosure rule | **4 business days** |

Every one of these presumes an organisation *knows* it has been breached
quickly. Most do not. A product that turns first contact into a timestamped,
tamper-evident record within seconds is not a luxury under these regimes; it is
the missing first step of compliance.

Meanwhile the market has already shown that raising the cost of insecurity
changes behaviour: PCI DSS after TJX, HIPAA after Anthem, GDPR's €1.2 billion
fine, and the cyber-insurance market making MFA effectively mandatory. Vyuha
applies the same economics to the intruder — raise their cost, remove their
reward — and to the defender's timeline — collapse eleven days into seconds.

## 5. Why it is feasible

This is not a proposal on paper.

- The full research and design exist (`research-log.md`, 57 sections; `design.md`).
- A working v1 has been built and tested at lab scale: every requirement in
  the v0.1 PRD is implemented, with **23 passing tests**, measured detection
  latency in **milliseconds**, and zero false alarms in testing.
- It has no external dependencies — plain Python — and runs on a laptop.
- The next steps are clearly specified in the v0.2 PRD, with realism and a
  red-team validation gate placed deliberately ahead of any new feature.

The hard part that remains — making decoys indistinguishable from real systems
to a skilled human — is well understood and scoped (FR-13..15, NFR-9). It is
engineering and validation work, not an open research question.

## 6. What is at stake

Hospitals, utilities, payment systems, and public services now run on software.
When they are breached, the cost is measured not only in money but in delayed
surgeries, grounded flights, and exposed citizens. The defenders of those
systems are outnumbered, out-automated, and late. Anything that gives them
certainty and time — reliably, cheaply, without disrupting their users — is
worth building.

Vyuha will not make any system unbreakable. Nothing does. What it offers is
narrower and more honest: the moment an intruder first reaches for something
valuable, the defender knows, the intruder loses time, and what they reached
was never real. That is a meaningful shift in a contest the defenders are
currently losing on time alone.

## 7. What it needs to move forward

1. **A developer** to implement the v0.2 realism requirements (FR-13..15).
2. **A red team** to run the fingerprint exercise (NFR-9) and report a number.
3. **A pilot environment** — one real organisation, one crown-jewel asset, a
   lab-to-staging step with the watcher on a separate host (NFR-8).
4. **Discipline** to resist adding mechanisms until the two numbers that matter —
   time-to-alert and fingerprint rate — are proven.

Everything needed to start is in this repository.

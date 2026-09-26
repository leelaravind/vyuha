# Vyuha — Project Overview

> Confidential working notes. Local only. Status: design stage, not built.
> Full detail lives in `../research-log.md`.

## Purpose
Vyuha is a defensive deception layer for detecting intruders early. It presents
decoy resources that no legitimate user has any reason to touch, so activity on
them is a high-confidence signal that something is wrong. The aim is to shorten
the time between an intrusion and its detection.

## Why it is needed
- Most breaches exploit known, unpatched weaknesses (the knowing–doing gap).
- Intruders now move faster than people can react; industry reports put the
  median time-to-detect at around 11 days, while the fastest recorded intruder
  movement is measured in seconds.
- Regulators are tightening breach-reporting deadlines (India CERT-In 6 hours,
  EU GDPR 72 hours, US SEC 4 business days), which raises the value of fast,
  reliable detection.

## Guiding metaphor
The design borrows the layered "vyuha" formation from the Mahabharata: an outer
field that is costly to cross, an inner maze that is easy to get lost in, and a
protected centre. It is a way to picture depth and delay, not a literal plan.

## Design goals
- Detect activity on a decoy within a few seconds.
- Keep false alarms near zero, because legitimate users never reach decoys.
- Keep a complete, tamper-evident record of what happened, for later review.

## Scope of the first version
- Runs only on our own machines in a lab; never exposed to the internet until
  it has been tested.
- One protected asset, a small decoy field, and a separate logging component.

## Boundaries (fixed)
- Defensive only: the system acts on its own decoys and records what happens
  there. It does not act against anyone else's systems.
- No offensive "hack-back" and no de-anonymisation. Identifying a person is a
  matter for law enforcement.
- The design, decoy locations, keys and schedules stay confidential.

## Document map
- `overview.md` — this page.
- `../research-log.md` — the full research history, reasoning and sources
  (57 sections).

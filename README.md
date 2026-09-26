# Vyuha — Project Index

Confidential. Local only. Snapshot date: 2026-09-26.
This folder is a complete copy of the project (working copy: `G:\CYBER\`).

## Start here
| Read | For |
|---|---|
| `docs/overview.md` | What the project is and why it exists |
| `docs/product.md` | Full product description, features, limits, roadmap |
| `docs/prd.md` | Product requirements (FR-1..12, NFR-1..7), risks, milestones |
| `docs/design.md` | Technical design and parameters |
| `docs/references.md` | Frameworks, regulations, research sources |
| `docs/requirements-traceability.md` | Every requirement mapped to code and a passing test; current status |
| `research-log.md` | The complete research history (57 sections) |
| `prototype/README.md` | How to run the software |

## Status at a glance
- **Spec: v0.2** (see `CHANGELOG.md`). Implementation: 0.1.0 (the v0.1 requirement set).
- Design: complete for v1; v0.2 adds realism, adversarial validation, true
  out-of-band watcher, response hook, modulus rotation, evidence bundle.
- Software: v1 built at lab scale; all v0.1 PRD requirements implemented.
- Tests: 23/23 passing (`cd prototype && python -m vyuha.cli selftest`).
- Verified from this copy on 2026-09-26.
- Deferred to a later build: multi-ring depth from the original scope,
  internet-scale deployment, richer decoy content, production hardening.
  See `docs/prd.md` section 10 and `docs/requirements-traceability.md`.

## Layout
```
vyuha/
  README.md                    this index
  research-log.md              full research history
  research-log.copy.md         duplicate of the log
  docs/                        overview, product, prd, design, references, traceability
  prototype/                   the software (Python 3.11+, no dependencies)
    vyuha/                     the package
    tests/                     test suites
```

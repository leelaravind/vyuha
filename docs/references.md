# Vyuha — References

> Confidential working notes. Local only. Fuller detail in `../research-log.md`
> sections 49–51 (frameworks and the filtered crosswalk) and 50 (regulations).

## 1. Frameworks this project builds on [§49][§51]
Rather than adopt whole frameworks, we keep only the parts that map to the design.

| Framework | Latest | Why it matters here |
|---|---|---|
| MITRE Engage | 1.0 | The adversary-engagement / deception framework — the closest external match to this project. |
| MITRE D3FEND | 1.0 | Defensive techniques; the Deceive, Isolate and Detect tactics map directly. |
| NIST CSF 2.0 | Feb 2024 | The six-function skeleton: Govern, Identify, Protect, Detect, Respond, Recover. |
| NIST SP 800-207 | 2020 | Zero Trust — the model for the legitimate-user path. |
| CIS Critical Security Controls | v8.1 | Keep controls 1, 6, 8, 12, 17 (assets, access, logs, segmentation, incident response). |
| MITRE ATT&CK | current | Attacker-behaviour reference: what the decoys must detect and provoke. |

Context for later (not v1 build requirements): ISO/IEC 27001:2022, NIST SP 800-53
Rev 5, OWASP Top 10 (2025 edition), the Cyber Kill Chain and the Diamond Model.

## 2. Rules that toughened the industry [§50]
Each changed behaviour because it had teeth. Kept here as evidence that raising
the cost of insecurity is what moves organisations — the same economics the
project applies to the adversary.

| Rule | Teeth | Illustrative case |
|---|---|---|
| PCI DSS | Card brands can revoke card processing | TJX (2007): non-compliant on 9 of 12 requirements; ~$250M+ |
| HIPAA + HITECH | Civil and criminal penalties | Anthem: 78.8M records → $16M settlement |
| GDPR | Up to €20M or 4% of global turnover | Meta: €1.2B (2023), the record |
| SOX | Up to 20 years for false certification | Pulled IT controls into the boardroom after Enron |
| SEC cyber disclosure | Enforcement for misleading disclosure | SolarWinds case: collapsed, but changed how CISOs document decisions |
| EU NIS2 | Up to €10M or 2%; management personally liable | Widened cyber duties to ~18 sectors |
| EU DORA | Fines the cloud/ICT vendors themselves | First regime to regulate hyperscalers directly (Jan 2025) |
| EU Cyber Resilience Act | Up to €15M or 2.5%; products pulled from market | Makes secure-by-design a legal product duty |
| CISA Secure by Design | None (voluntary) | Peer and procurement pressure; slower to bite |
| India CERT-In + DPDP | DPDP up to ₹250 crore | CERT-In's 6-hour reporting; some VPNs left India rather than log |
| Cyber insurance | No policy without controls | Made MFA effectively mandatory across the mid-market |

### The pattern
- A disaster triggers each rule; the industry rarely toughens on its own.
- Teeth change behaviour, not advice. Personal liability and market access move
  faster than fines.
- The frontier is shifting to vendors and to "secure by design" — security by
  law, not bolt-on.

## 3. Core research sources referenced in the design
- Time-lock puzzles: Rivest, Shamir & Wagner (1996). VDFs: Boneh et al. (2018),
  Wesolowski (2019), Pietrzak (2019). [§57]
- Moving Target Defense: Jajodia et al. (2011); Forrest et al. (1997). [§10]
- Deception research: honey documents / canary tokens (Stolfo et al.). [§9]
- Attacker speed and dwell time: CrowdStrike Global Threat Report (2026);
  Mandiant M-Trends (2025). [§35]
- Economics of security: Becker (crime economics); Gordon–Loeb (spend vs. loss).
  [§6]

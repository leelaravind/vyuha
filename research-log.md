# Cyber Project — Research Log

> **CONFIDENTIAL.** Do not publish, share, or upload anywhere.
> Status: research phase. Nothing is built yet.
> Log date: 2026-09-25 (backup reconstructed 2026-09-26 after the H: drive was disconnected)

---

## 1. Starting point: the economy
- The first framing was AI, healthcare and cybersecurity. These are different kinds of things: AI is a technology, healthcare is an industry, and cyber is a protective layer.
- Missing areas: energy, semiconductors and compute, finance, defense, robotics, biotech, climate, space, agriculture.
- A better model is a stack: **physical base → compute → intelligence (AI) → trust layer (cyber) → applications**.
- Cyber grows with every other layer, because each new system adds attack surface.

## 2. The knowing–doing gap
- Most breaches exploit known problems that already have known fixes.
  - **Equifax (2017):** a patch existed and wasn't applied for about 2 months.
  - **Change Healthcare (2024):** a remote-access portal had no MFA.
- Why the known fixes don't get applied: security's value is invisible, it's a cost center, it adds friction, legacy systems can't be patched, compliance becomes checkbox culture, and skilled people are scarce.
- Security is **bolted on** after the fact instead of **built in**, which is why it feels like a "thin layer."
- The layer is getting thicker because of regulation (SEC rules, NIS2, DORA), cyber insurance requirements, and executive liability.

## 3. Automation and the trust problem
- Auto-remediation tools already exist: Dependabot, Copilot Autofix, Snyk, SOAR platforms, CodeMender, DARPA AIxCC.
- **Where they fall short: trust.** Teams won't auto-apply fixes because they fear breaking production.
- **CrowdStrike (July 19, 2024):** a bad automatic update crashed about **8.5 million** Windows machines.
- The dilemma: acting automatically risks breaking things (CrowdStrike); waiting for humans risks being exploited (Equifax).
- Safe automation needs canary rollouts, sandbox testing, automatic rollback, risk-based autonomy and blast-radius limits.

### Why known solutions weren't used
- CrowdStrike treated the update as "just data," was under speed pressure, trusted a validator that had a bug, and had grown overconfident from past success (normalization of deviance).
- The same pattern shows up elsewhere: **Google Cloud (June 2025)** and **Cloudflare (Nov 2025)** outages both came from config changes.
- **Insight:** when safety is a *choice*, people under pressure skip it. The safe path has to be the default.
- **Analogy: Let's Encrypt** made HTTPS free and automatic, and HTTPS went from about 50% to over 90% of web traffic.

## 4. First principles: why, what and where

### WHY
- A security concern exists only when **value + motive + access** are all present. Remove any one of them and the concern disappears.
- The internet was **built on trust**: SMTP, DNS and BGP had no identity checks. Security has been added on top ever since.
- Value moved online, and complexity grew faster than anyone's ability to verify it.
- Defenders must protect everything; an attacker needs only one gap.

### WHAT: the CIA triad
| Principle | Meaning | Failure example |
|---|---|---|
| Confidentiality | Only the right people can see it | Equifax |
| Integrity | No one can secretly change it | SolarWinds |
| Availability | It works when needed | CrowdStrike |

### WHERE
- Wherever **value meets connection**: physical, network, devices, applications, data, identity, people, supply chain and AI.

### History: the concern follows the value
- 1961 CTSS passwords → 1988 Morris worm → 1990s online money → 2010 Stuxnet → 2010s cloud breaches → 2020s supply chain and AI.

## 5. The internet as a battlefield
- A connected device sits on a battlefield. Built-in security is the assigned soldier, antivirus is a hired guard, the firewall is a wall, encryption is a safe, and backups are a hidden copy.
- **Mirai (2016):** about 600,000 devices protected only by default passwords were captured, like a battlefield with no soldiers.
- Many cyber terms come from the military: defense in depth, DMZ, kill chain, red and blue teams, C2. In 2016 **NATO** declared cyberspace a domain of warfare.
- **Where the analogy breaks:**
  1. There's no distance.
  2. The enemy has unlimited cheap soldiers.
  3. The enemy can wear your uniform (stolen credentials).
  4. The enemy can stay hidden inside for months.
  5. Your own guard can turn into the threat.
  6. Stolen treasure can be copied and the original left in place.
  7. More guards doesn't mean more safety.
- The doctrine shift: from the castle model to **Zero Trust**, which assumes the enemy is already inside.

## 6. Attack economics
- **Attack if:** Reward × chance of success > cost + (chance of getting caught × punishment). This framing comes from Becker's economics of crime.
- The four defender levers:

| Lever | Example |
|---|---|
| Raise the attacker's cost | MFA blocks more than 99.9% of account takeovers |
| Kill the reward | Encryption, backups |
| Lower the chance of success | Patching |
| Raise the risk of getting caught | Logging, takedowns (LockBit, 2024) |

- **Where the rule fails:** nation-states and insiders barely care about cost; targeted attacks differ from opportunistic ones ("outrun the bear"); scale makes per-victim cost tiny; attacking keeps getting cheaper (RaaS, AI).
- **Gordon-Loeb:** spend at most about 37% of the expected loss on protecting an asset.

## 7. Padmavyuha / Chakravyuha
| Padmavyuha | Cyber equivalent |
|---|---|
| Concentric rings | Defense in depth |
| Rotating formation | Moving Target Defense |
| Easy to enter, hard to exit | Deception / honeypots |
| Jayadratha seals the entrance | Containment / isolation |
| Arjuna lured away | Diversion (DDoS smokescreen) |
| Fallen warrior replaced | Self-healing / redundancy |
| Only a few knew how to break it | Knowledge concentration |

- **The Abhimanyu problem:** knowing how to enter without knowing how to exit. CrowdStrike could push the update but had no quick rollback.
- **Rule:** never make a change without a tested way back.

## 8. CORE IDEA (the user's own)
**Deliberate holes → any attacker or bot that enters must solve a very costly challenge → the attacker's cost rises while the value inside falls.** The system is modeled on an ancient unbreakable vyuha or astra.

- **Pieces that already exist separately:** proof-of-work (Hashcash 1997, Tor 2023, Anubis 2025), honeypots and honeytokens, tarpits, Cloudflare AI Labyrinth (2025). The *combination* appears to be new.
- **Problems to solve:**
  1. Botnets run on stolen compute ("Proof-of-Work Proves Not to Work," 2004).
  2. Legitimate users could get caught. This is solved if the holes are fake, since anyone who enters is an attacker.
  3. Smart attackers may walk away, but they're exposed by then.
- **Upgrade: charge in time, not compute.** Time-lock puzzles (Rivest–Shamir–Wagner 1996) and VDFs (2018) have to be solved sequentially, so botnets can't parallelize them, and the defender creates them almost for free.
- **Guaranteed depreciation:** if the puzzle takes longer to solve than the key rotation period, the prize has expired by the time it's reached.
- **Ancient model:**
  - **Mayasabha**: the holes are illusions.
  - **Narayanastra**: cost grows with aggression, and anyone who lays down arms passes. Legitimate users are untouched.
  - **Padmavyuha**: the layered architecture.

## 9. Secrecy
- **Kerckhoffs's principle (1883):** a system should stay secure even if everything except the key is known. Examples: Enigma (a secret design that was broken) and AES (a public design that is secure).
- **Keep secret:** hole locations, which holes are real and which are fake, rotation schedules, keys, what the decoys look like.
- **Can be known:** that decoys exist, the general concept, the math. Knowing that decoys exist makes every door expensive, the way a minefield sign does.
- **Main risk: fingerprinting.** Identical decoys get recognized, so every deployment must be unique and changing.
- **Leaked design files should lead nowhere:** use honey documents and canary tokens (Stolfo et al., Columbia).
- **The whole idea is confidential.**

## 10. Hundreds of designs: the whole design keeps changing

### Research
- Jajodia et al., *Moving Target Defense* (2011)
- Forrest et al., "Building Diverse Computer Systems" (1997), based on immune-system diversity
- Multicompiler / software diversity (Franz, UC Irvine)
- DARPA CFAR (2015): multi-variant execution
- Stackelberg security games (Tambe, USC): randomized defense, used at LAX
- Cho et al., IEEE MTD survey (2020)

### Mythology
- Kurukshetra's formation changed every day (Krauncha, Makara, Garuda, Chakra, Suchi…).
- **Tripura:** three moving cities that lined up once in a thousand years. **This is the closest model.**
- Mayasura as the master designer, the Dashavatara (form adapted to each threat), Raktabija (redundancy), and Proteus (a Greek shapeshifter).

## 11. An attacker who plans in every direction
- Their cost multiplies with the number of designs, while the defender maintains only one real path.
- Going broad is loud: more decoys get tripped, so detection is faster.
- Sun Tzu: "If he sends reinforcements everywhere, he will everywhere be weak."
- **Limit:** a nation-state can afford it. Against them the goal is to slow and expose, not to stop.
- **Hiranyakashipu** covered every direction and still lost to the gap he never imagined (Narasimha).

## 12. Keeping ports busy
- **Portspoof:** all 65,535 ports appear open, each with a fake service.
- **LaBrea tarpit:** holds scanner connections frozen.
- **Port knocking / SPA (fwknop):** the real service is hidden until a secret knock arrives.
- **Catch:** this costs bandwidth, and static fakes can be fingerprinted, so they must rotate.

## 13. Insider threat
- *"Ghar ka bhedi Lanka dhaye"*: Vibhishana.

| Solution | Parallel |
|---|---|
| Split knowledge (Shamir's secret sharing) | No single person knows the whole design |
| Behavior analytics (UEBA) | Rahu caught by Surya and Chandra |
| Loyalty traps (honey documents, canaries) | Chanakya's *upadha* tests |
| Two-person rule | Nuclear launch control |
| Least privilege / zero trust | Access only to what the role needs |

- **Principle:** no single insider is enough.

## 14. Crown jewels of a big company (Google as the example)
- Signing keys (Storm-0558 stole a Microsoft key in 2023), the update pipeline, identity systems, user data (GDPR fines up to 4% of revenue), source code and AI weights, cloud control.
- **Why bounties are large:** Google paid about **$12M in 2024**, because it has to outbid black-market brokers (Zerodium offered $2.5M for one Android exploit chain), and buying a bug is cheaper than suffering a breach.
- **For the system:** decoys should imitate these crown jewels.

## 15. Intelligence

### Ancient
- Arthashastra spies: stationary (*sthanika*) and roaming (*sanchara*).
- Ravana's spies Shuka and Sarana.

### Sun Tzu's five spies mapped to cyber threat intelligence
| Spy | Cyber |
|---|---|
| Local | OSINT |
| Inward | Undercover in dark-web and ransomware forums |
| Converted | Takeovers of criminal infrastructure (the LockBit site) |
| Doomed | Deception and honeypots (**this system**) |
| Surviving | Internet sensors (GreyNoise, Shadowserver) |

- Information-sharing groups: ISACs, MITRE ATT&CK, CISA KEV.

### "Left of boom": detect attacks before contact
- Lookalike-domain monitoring, Certificate Transparency logs, GreyNoise, hunting for attacker C2 servers (JARM), dark-web monitoring, EPSS.
- **Limit:** fresh, unused attacker infrastructure is invisible until first contact. That's where the holes take over.

## 16. Rules of war
- Kurukshetra's dharma yuddha rules were all broken once the stakes rose (Abhimanyu, Karna, Drona, Duryodhana).
- Cyber has rules too: UN norms (2015), the Tallinn Manual, the Budapest Convention (not signed by India, Russia or China), the UN Cybercrime Convention (2024/25), and the ICRC's 8 rules for civilian hackers (2023).
- **Principle:** design assuming every rule will be broken.

## 17. Small, anonymous gangs
- Ancient enemies were visible kingdoms. Today a 5-person gang can strike worldwide.
- Lapsus$ (Microsoft, Nvidia, Samsung, Okta, Uber), Scattered Spider (MGM, about $100M; M&S, about £300M), RaaS franchises, false flags (Olympic Destroyer).
- Tracing is slow but possible: arrests, and $2.3M of the Colonial Pipeline ransom recovered.
- **Indrajit** fought invisible and was defeated by striking before his ritual, using Vibhishana's intelligence.

## 18. Cryptography

### Uses in the system
- Time-lock puzzles, rotating keys, signatures so legitimate users pass, secret sharing for insiders, watermarking leaked files, encrypting data.

### Ancient links
- Vidura's *mleccha* warning about the lac house (an encrypted message)
- Rama's ring and Sita's *chudamani* (two-way authentication)
- Royal *mudra* seals (digital signatures)
- Kama Sutra's *mlecchita vikalpa* (ciphers)
- Arthashastra secret codes
- Caesar cipher, scytale, Herodotus' tattooed message

## 19. Few assets then, countless now
- Ancient: the Arthashastra's *saptanga*, seven limbs of the state (king, ministers, territory, fort, treasury, army, allies).
- Now: millions of assets, largely invisible (shadow IT), copyable, and chained together (Log4j 2021, xz 2024).
- **CIS Control #1 is "know what you own."**

## 20. Case study: Microsoft (breaking it down part by part)
- **Basics:** Microsoft builds the software and cloud much of the world runs on: Windows, Office/365, Azure, and the Entra ID identity systems.
- **Why Microsoft:** it's among the most trusted companies, yet the CSRB (2024) called its security culture "inadequate" and described "a cascade of avoidable errors."

| Part | Incident |
|---|---|
| 1. Identity and signing keys | Storm-0558 (2023) |
| 2. Forgotten legacy assets | Midnight Blizzard (2024) |
| 3. On-premises products | Exchange ProxyLogon (2021), SharePoint ToolShell (2025) |
| 4. Partners and supply chain | SolarWinds (2020), CrowdStrike (2024) |
| 5. Culture and priorities | CSRB findings → Secure Future Initiative |

## 21. Target chosen: Microsoft Cloud (the tougher one)
- **One flaw hits thousands of customers at once:** ChaosDB (2021) exposed thousands of Azure Cosmos DB customers' keys.
- **Identity is the whole perimeter:** whoever holds the token or login *is* the owner (Storm-0558, Midnight Blizzard).
- **Shared responsibility:** Microsoft secures the cloud and each customer secures what they put in it. Breaches fall in the gap between the two.
- **Cloud contains the software problem too:** Windows, Office and SharePoint all run on it.

## 22. The island model
- Microsoft Cloud is an **island with seashore on all sides**, and **ports are the harbors**.
- A port is just a number a program listens on. Opening one is **one line of code or config**, so harbors can appear or disappear in seconds.
- **Refinements:**
  - **One main harbor:** nearly all traffic arrives on **443**, so the real gate is **passport control** (identity / Entra ID).
  - **Millions of islands on one coastline:** each customer (tenant) builds its own harbors and often opens dangerous ones (3389, public storage).
  - **Underground tunnels:** updates, partners and suppliers bypass the harbors (SolarWinds).

## 23. Port basics
| Port | Job | Island analogy |
|---|---|---|
| 80 | Websites (http), unencrypted | Open public harbor |
| **443** | Secure websites (https) | Main passenger harbor |
| 25 / 587 | Email between servers | Postal harbor |
| 53 | DNS, names to addresses | Lighthouse and map office |
| 22 | SSH, admin command line | Staff-only dock |
| 3389 | Remote desktop | Staff-only dock |
| 445 | File sharing | Internal canal |
| 1433 | SQL Server database | Treasury vault door |

- **Rule:** most harbors stay closed to the open sea, and staff docks sit behind walls (VPN or private networks).
- **WannaCry (2017)** spread through port 445 left open to the internet: about 200,000 computers, including the UK's NHS.
- **Port count:** every IP address has **65,535 ports** (a 16-bit number, 2^16 = 65,536 counting the reserved 0), once for TCP and again for UDP.
  - 1–1023 well-known; 1024–49151 registered; 49152–65535 temporary
- **Microsoft is an archipelago:** millions of islands (servers and IP addresses) × 65,535 possible harbors each.

## 24. The fish cat math
- Microsoft Town has 1,000,000 houses × 65,535 windows = **65,535,000,000 windows**.
- If every house opens only 2 windows, that's 2,000,000 open, or **0.003%**.
- A cat checking 1 window per second needs **about 2,078 years**.
- A scanning tool (masscan) at 10 million windows per second needs **about 1.8 hours**.
- **Every open window gets found, so every one must be guarded.**

## 25. Getting in and spreading
- **Knowing the port ≠ getting in.** A door opens only with:
  - a stolen key (leaked or guessed passwords, the most common)
  - a broken lock (a software flaw; Log4Shell (2021) needed one line of text)
  - a door never locked (default or missing password, as in Mirai)
- **Lateral movement (house to house):** reused admin passwords, keys stored in memory (Mimikatz), houses that trust each other.
- **NotPetya (2017):** entered through one accounting software update, then spread using stolen passwords. **Maersk** lost about 45,000 PCs and 4,000 servers, and recovered only because one server in Ghana was offline during a power cut.
- **Defense:** segmentation (walls between houses), a unique key for each house, zero trust (a check at every door).
- In the cloud, customers are separated by strong walls, but crossing them has happened (ChaosDB).

## 26. A unique random password for every house
- **Rule:** no password matches any other, and no pattern exists.
- A random 16-character password over 94 characters gives **94^16 ≈ 3.7 × 10^31** possibilities, versus the **6.55 × 10^10** needed.
- Chance that any two of the 65.5 billion match is **n² ÷ (2 × space) ≈ 6 × 10^-11**, practically zero.
- Guessing at 1 trillion per second takes **about 1.2 trillion years** (about 85 times the age of the universe).
- **This already exists:** **Microsoft LAPS** gives every machine a unique random admin password and rotates it automatically.
- **What it doesn't stop:** phishing (the owner hands over the key), pass-the-hash (the stolen fingerprint is used instead), session-token theft (skips the password entirely).
  - This is why the industry is moving to **passkeys** and **short-lived tokens**, which link to the expiring-value idea.

## 27. SCENARIO (open, waiting for the user's direction)
> The keys are now perfect: unique, random and rotating. **But the attacker may *create* a culprit (plant an insider) or *convert* an existing person into one.**

- Status: **recorded as a scenario only.**

### Attack paths once the attacker is inside
With perfect keys, the attacker stops attacking the key and goes after **what surrounds it**:

| # | Attack | How it works | Real example |
|---|---|---|---|
| 1 | **Session takeover** | Steal the "already logged in" token (cookie), which skips the password *and* MFA | Okta support-system breach (2023): stolen session tokens used against Cloudflare, 1Password and others |
| 2 | **Moulding a known person** | Trick or pressure a trusted person into entering the keys | Uber (2022): MFA-prompt spam plus a fake "IT support" message; Scattered Spider (MGM) phoned the help desk |
| 3 | **Stealing the hash** | A hash **can't be reversed**, only guessed; a random 16-char password takes ~1.2 trillion years. The real danger is **pass-the-hash**, using the hash *directly* as the key | Standard attack in Windows networks (NTLM) |

> **A perfect key is useless if the attacker can steal the door pass, fool the keyholder, or copy the key's shadow.**

## 28. Mythological parallels for the scenario
Perfect protection bypassed **without being broken**:

| Attack | Scene | What happened |
|---|---|---|
| **1. Session takeover** | **Odysseus and the Cyclops** (Greek) | Blind Polyphemus felt the back of every sheep leaving the cave; the men clung *underneath* and rode out inside the approved flock |
| | **Rahu** | Slipped into the devas' line while the amrit was already being served, and was accepted as one of them |
| **2. Moulding a known person** | **Karna's kavach-kundal** | His armor was unbreakable. Indra, disguised as a Brahmin, used Karna's **known vow** never to refuse a Brahmin, and Karna **cut off the armor and handed it over** |
| | **Lakshmana Rekha** (popular retellings) | Ravana couldn't cross the line, so he came disguised as a sage and got **Sita to step out** |
| | **Manthara → Kaikeyi** | Manthara turned a trusted queen, who used her **legitimate keys** (Dasharatha's two boons) to exile Rama. **This is also the converted-insider case from scenario 27** |
| **3. Using the key's shadow** | **Jacob and Esau** (Bible) | Jacob wore goatskins to feel like Esau. Blind Isaac said *"The voice is Jacob's voice, but the hands are the hands of Esau"* and blessed him anyway. **The check verified the marker, not the person** |

- **Closest single scene: Karna's kavach.** Perfect protection that wasn't broken, but given away by its owner.

## 29. The user's framings of the scenes and their lessons

### 1. Rahu: detect and cut (session takeover)
- **User's framing:** the **Sun and Moon** spotted the imposter, and **Mahavishnu as Mohini** beheaded him instantly. That's why they are now Rahu and Ketu.
- **Cyber mapping:** Sun and Moon = observers and behavior detection. Mohini's strike = **instant session revocation** (response).
- **Deeper lesson:** the detection came **after the amrit reached his throat**, so the head stayed immortal and **Rahu and Ketu still return as eclipses**. Once the attacker has taken something, cutting them off doesn't undo it, and they come back (**persistence**). **Detection speed is everything.**

### 2. Karna's kavach-kundal: security, attacker and prize
- **User's framing:** **attacker** = the disguised Brahmin, **security** = Karna, **prize** = the kavach-kundal. The attacker knew Karna's weak point (his vow).
  - **Correction:** it was **Indra** (Arjuna's father), not Krishna. **Surya warned Karna in a dream beforehand**, and Karna gave the kavach anyway because of his vow.
- **User's idea:** a smart Karna would **give something else that honors the request but fails the attacker**. **This is the core decoy system** (section 8): hand the attacker a convincing fake prize. *Karna needed a Mayasabha.*
- **Cyber lesson:** attackers **study your known rules** (for example, "the help desk always helps"). Crown jewels need an extra check, even when the rule says yes.

### 3. Lakshmana Rekha: warnings = security notifications
- **User's framing:** Ravana **phished** Sita, and she stepped out **even though Lakshmana warned her**. Lakshmana's warning = the notifications we get ("don't click unknown links").
- **Why warnings fail:** Ravana used **Sita's duty to feed a sage**. Phishing works the same way, playing on duty, authority and urgency, so **warnings alone fail**.
- **Fix: passkeys, a Rekha that travels with Sita.** Even if the user is fooled, the key refuses to work on the attacker's fake site (phishing-resistant).

### Pattern across all three
| Scene | Protection | How it failed | Lesson |
|---|---|---|---|
| Rahu | Devas' line | Imposter joined a running session | Detect fast; late detection means permanent damage |
| Karna | Unbreakable armor | Owner's known rule exploited | Answer with a decoy; extra checks for crown jewels |
| Lakshmana Rekha | Uncrossable line + warning | Victim's duty exploited | Warnings aren't enough; the protection must travel with the person |

## 30. What the defenders could have done (inside the stories)
- **Rahu:** Mohini served first and checked later. If the Sun and Moon had watched each guest **before** the amrit was poured, Rahu would never have become immortal.
- **Karna:** Surya warned him, so he knew. He could have kept his vow by offering gold, cows or land instead. He did bargain for the Vasavi Shakti, but only *after* giving up the kavach, not *instead of* it.
- **Lakshmana Rekha:** Lakshmana knew the cry was Maricha imitating Rama's voice, but Sita's words forced him to leave (the guard knew and was overruled). Sita could have given alms from inside the line; Ravana *demanding* she step out was itself the sign.
- **Odysseus and the Cyclops:** Polyphemus felt only the sheep's **backs**. Checking underneath, or counting who left, would have caught them.
- **Manthara and Kaikeyi:** Dasharatha gave **two open boons with no limit and no expiry**. A bounded boon couldn't have been used to exile Rama.
- **Jacob and Esau:** Isaac **noticed** the mismatch ("the voice is Jacob's") and trusted the hands anyway.
- **Common thread:** in almost every story, the defender had a warning or a doubt and ignored it.

## 31. The story fixes translated to cyber
| Story fix | Cyber equivalent |
|---|---|
| Rahu: check before serving | **Verify before granting access** (identity, device, behavior); catch the attacker before persistence |
| Karna: give something else | **Answer crown-jewel requests with a decoy** (honeytoken); **act on warnings** (Surya's dream = a threat-intelligence alert) |
| Lakshmana overruled | **Pressure must not override the security team**; exceptions need a formal process |
| Maricha's fake voice of Rama | **Voice and video impersonation** (Arup, 2024: about $25M lost to a deepfake video call); **call back on a known number** |
| Sita: give alms from inside the line | **A request to leave the protection is itself the red flag**; real services never ask you to disable security |
| Polyphemus: check underneath, count who leaves | **Inspect contents, not labels; watch what leaves** (egress monitoring) |
| Dasharatha's unlimited boons | **No standing privileges**: access with limits and expiry (just-in-time), reviewed regularly |
| Isaac: voice and hands disagreed | **When signals conflict, demand one more check** (step-up verification) |

- **Principle:** attacks succeed because warnings and doubts get ignored, so build systems that **act on doubt automatically**.

## 32. Are these fixed today? No, only partly in use
| Fix | Exists? | In use? |
|---|---|---|
| Passkeys | Yes | Growing; Microsoft made new accounts passwordless by default (2025), but passwords still dominate |
| Mandatory MFA | Yes | Microsoft began enforcing it for Azure sign-ins (2024–25); many other systems don't |
| Device-bound sessions | Early (Chrome's DBSC) | Stolen session cookies are still a major attack |
| Continuous access checks (CAE) | Yes | Customers must configure it; many don't |
| Credential Guard | On by default for eligible Windows 11 enterprise devices | Older machines are exposed |
| Retiring NTLM | Being phased out | Still present in many networks |
| No standing privileges (JIT) | Entra PIM | Common gap; Midnight Blizzard abused an over-privileged app inside Microsoft |
| Decoys / honeytokens | Yes | Low adoption |
| Deepfake call-back rules | Procedures only | Inconsistent |
| Security team not overruled | It's culture | The CSRB found Microsoft put features ahead of security |

- **The tools exist, but they're switched on unevenly.** It's the knowing–doing gap again (section 2).

## 33. Think Deep (Telugu YouTube channel) videos linked to our topics
> **PARKED:** sections 33–34 are set aside for later (2026-09-26).
- Channel: youtube.com/@ThinkDeep, about 22.3 lakh subscribers, **807 videos scanned** (2026-09-26).
- **No video is directly about cyber attacks or hacking.** **16 videos** connect to our topics:

| # | Video (ID) | Links to |
|---|---|---|
| 1 | The Invisible Weapon Changing Warfare (F9IG6lR5bHo) | GPS spoofing, the closest to a cyber attack |
| 2 | A Traitor Inside R&AW! (8nxJUzojyX0) | Insider threat |
| 3 | The Undercover Journalist (njxXAkJyW8A) | An insider spy for 11 years |
| 4 | Mossad's Operation Plasma Screen (UPYeiEaTFkk) | Fake identities (Jacob and Esau) |
| 5 | RAW's Deadliest Mission in China (LJD8XAgqSis) | Intelligence (inward spies) |
| 6 | Operation Hornet (f1fL5EY606Y) | Intelligence operation |
| 7 | Exploring the Reality of India's R&AW (gtoXr4tga-U) | Intelligence agencies |
| 8 | The Lizard Strategy / Sinhagad (ENeY1BCcvjE) | The gap nobody imagined (Hiranyakashipu) |
| 9 | Janjira's Undefeated Fort (jZy8j9UnQwE) | A real "unbreakable vyuha" |
| 10 | Fort Knox Secrets (-kccPBTraG4) | Protecting crown jewels |
| 11 | The Genius Spaggiari Heist (6Udzn7pGjBs) | Tunnels bypassing a bank (underground tunnels) |
| 12 | The Västberga Helicopter Robbery (ujErKIruRaE) | Attack from the one unguarded direction (roof) |
| 13 | 18 Days of Mahabharata War (oz7yuSWWLtg) | The daily vyuhas, Abhimanyu |
| 14 | Was Karna's Chariot Wheel Found? (38Okx2E34v4) | Karna, broken rules of war |
| 15 | 5 Hidden Divine Weapons (q2ESgus9L5Y) | Astras |
| 16 | Padmanabhaswamy Temple: The 7th Door (caT9bh5v2RQ) | An ancient sealed vault |

## 34. Knowledge extracted from the 16 videos
> **Source note:** YouTube blocked transcript access, so this comes from the video descriptions plus well-known history. The videos weren't watched. The Undercover Journalist, RAW's Mission in China and Operation Hornet read as dramatized/unverified.

Key lessons:
1. **Every "impregnable" defense fell through the direction nobody guarded:** the cliff (Sinhagad), the sewer (Spaggiari), the roof (Västberga).
2. **The one that never fell (Janjira) hid its gate and kept its isolation.**
3. **Warnings get ignored** (Västberga police warned a month early; like Surya and Lakshmana).
4. **Insiders are the deepest leak** (R&AW).
5. **Unauthenticated signals get trusted** (GPS), the same root flaw as the internet.
6. **Split knowledge works** (Fort Knox: no one person knows the whole combination).
7. **Deception works both ways** (a controlled leak; a staged heart attack).
8. **Attackers disable the responders**, so protect the response too.
9. **Detection after the damage is too late.**

## 35. How fast is detection? (from nanoseconds to years)
**Units:** 1 second = 1,000 ms = 1,000,000 µs = 1,000,000,000 ns.

| Speed | What detects it | Example |
|---|---|---|
| ~1 nanosecond | CPU hardware checks | Intel CET, ARM memory tagging |
| ns to µs | Network packet filters (XDP/eBPF) | Drop attack packets on arrival |
| µs to ms | Antivirus signature match | Known-bad fingerprint |
| ~3 seconds | Automatic DDoS defense | Cloudflare's stated average |
| ≤1 minute (target) | CrowdStrike's "1-10-60" rule | Detect 1, investigate 10, contain 60 |
| 11 days | Real-world median dwell time (Mandiant, 2025) | Time inside before found |
| 241 days | Industry average (IBM, 2025) | Time to identify + contain |
| ~14 months | SolarWinds | Undetected |
| ~4 years | Marriott/Starwood | Undetected |

- **Attacker breakout time (CrowdStrike Global Threat Reports):**
  - 2024 report (2023 data): fastest 2 min 7 s, average 62 min
  - 2025 report (2024 data): fastest 51 s, average 48 min
  - **2026 report (2025 data, released Feb 24, 2026): fastest 27 s (latest record), average 29 min** (65% faster than 2024)
  - In one 2025 intrusion, data theft began within 4 minutes. AI is accelerating attackers.
- **The speed-up is accelerating.** Longer view: CrowdStrike's 2019 report put the average criminal breakout at ~9 h 42 min (2018), now 29 min — about 20× faster in 7 years.
- **Conclusion:** attackers moved from hours to minutes to seconds, faster than humans can react, so **detection and response must be automated**.
- **Key insight:** machines detect **known** tricks in nanoseconds, but **new** attacks take humans days to months, while the fastest attacker spreads in **27 seconds**.
- **The Rahu gap:** the amrit is swallowed long before the Sun and Moon notice.

## 36. Can the attacker tell who is watching?
- **Humans can't detect a 27-second attacker in real time.** Machines catch and block; humans investigate afterwards.
- **Attackers can partly tell who is watching:** they check for security software on the machine (some kits try to disable it, "EDR killers"); decoys/sandboxes look **too clean** so attackers get suspicious; machines respond instantly and identically while humans respond in minutes, mostly office hours (hence attacks at night/weekends/holidays).
- **Lessons:** the watcher must be invisible (Rahu); decoys must look lived-in (fingerprinting risk); uncertainty is a weapon (if the attacker can't tell real from trap, or human from machine, every step costs caution and time).

## 37. A pendrive OS + VPN is not invisibility
- The VPN is one knot, not a wall (provider logs, legal orders, or investigator-run servers expose the real address).
- **One slip is permanent** (Ross Ulbricht / Silk Road caught partly via an early forum post under his real name).
- Behavior is a fingerprint (typing rhythm, hours, language, tools).
- The decoy collects evidence anyway; the endpoint leaks (browser/system fingerprint often survives a VPN).
- **Lesson:** don't unmask at the door. **Make them stay and act inside the hole.** Time on target beats anonymity.

## 38. Thinking like an attacker: is there another way in?
- **Answer: Yes.** No system is closed from every side. The design makes entry **much slower, costlier and more likely to expose the attacker**, but not impossible.

## 39. An agent that acts human but isn't (CONFIDENTIAL)
- **Answer: Yes. Pieces exist:** O2's "Daisy" AI grandmother (UK, 2024) and Apate.ai (Australia) waste scammers' time; AI honeypots (shelLM 2023, Galah 2024, HoneyGPT 2024); deception platforms generate fake user activity; Security Copilot / Charlotte AI could respond with human-like timing.
- **Mythology:** Agni hid the real Sita; **Ravana abducted Maya Sita**, an illusion that acted fully human.
- **Catch:** the agent itself becomes a crown jewel; if taken over, the guard turns against you, so it needs its own protection.

## 40. Diversion: show the snake, take the elephant
- Make noise in one place, strike in another (36 Stratagems: "make a noise in the east, strike in the west").
- **Mythology:** the Samsaptakas lured Arjuna away (Chakravyuha); Maricha's golden deer drew Rama and then Lakshmana away from Sita.
- **Defense:** when something loud happens, keep someone watching the quiet side. **The defender's version (this system):** show the attacker the snake (decoy) while the elephant (real asset) stays hidden.

## 41. Inverting the diversion: feigned weakness (the user's idea)
- **Idea:** when the attacker's noise comes, bluff that all attention is diverted (show systems as overloaded), so the attacker believes the path is open and walks in.
- **Precedents:** Mongol/Norman false retreats (Hastings 1066); Hannibal at Cannae; Sun Tzu "appear weak when you are strong"; the Chakravyuha opened then sealed.
- **Flow:** Attacker makes noise → the system *pretends* to be overloaded → the attacker walks through the "open" door → into the Padmavyuha (decoys + time-lock puzzles) → invisible watchers record everything.
- **Three rules:** only the show is weak (real defense never is); the "open" door leads only to decoys; the bluff must be believable (fingerprinting risk).

## 42. Redirect, hold, and trace
- **Idea:** when triggers fire (e.g., a port connection), send the attacker in a separate direction where they spend a lot of time, so they can be traced. The longer they stay, the more evidence they leave.
- **Time to know who/where:** seconds → the connecting IP (usually not the real location, just the last hop); days to weeks → likely known group (not a person); months to years → the actual person, usually only via police + providers, often cross-border. Many attackers are never identified.
- **Honest picture:** an IP alone almost never proves identity. Evidence builds over time; naming a person goes through police/courts.
- **The system's role:** keep the attacker inside long enough, and record cleanly enough, that the evidence is strong when handed over.
- **Question:** "Is there a way to trigger back?" **Answer: Yes.** No details discussed.

## 43. How to find the best product (there's no perfect one)
- **No perfect product.** The best achievable one **makes attacks cost more than they're worth, notices fast, and recovers quickly.**
- **Process:** (1) know what you protect (crown jewels); (2) model threats (MITRE ATT&CK, STRIDE); (3) map defenses from references (crosswalk of NIST CSF 2.0, CIS Controls, MITRE D3FEND); (4) find the gap (speed, insiders, trust, fake-looking decoys); (5) design for failure (defense in depth, containment, a tested way back); (6) test against real attackers (red teams, bounties); (7) measure (attacker cost, time to detect/contain, false alarms); (8) keep changing it (moving target defense).
- **Boundary:** attacker techniques and trace-back methods are **not documented** in this file; those questions were answered yes/no only.

## 44. Is public threat information useless? (the user's argument, and the verdict)
- **User's argument:** if we know the great attacks/latest techniques we can predict the next levels; every system has a loophole that should be known but never documented, with a trap kept there; the giants can't stop attacks; the real guard sees behind the CCTV (knowledge is the key; update it automatically); new techniques appear first in hidden places; public phone security updates are useless because attackers avoid publicly known methods.
- **Verdict: mostly accepted, with one correction.**
  - **Right:** knowledge is the key; elite attacks (zero-days) are secret and hoarded; the giants can't fully stop it; the loophole point is Kerckhoffs (known to us, never documented where it leaks — that's the trap).
  - **Correction — public info is NOT useless.** The majority of real breaches use old, known, public weaknesses never fixed (Equifax, WannaCry, Log4j). Attackers use known methods because they still work. Truly unknown attacks are rare and expensive. The real problem is the knowing–doing gap (section 2).
- **Honest split:** ordinary attackers (most volume) are stopped by known public defenses applied properly; elite, targeted attackers need more — **that's where the trap earns its place.**
- **System's real value:** not hiding from public knowledge, but **covering the small, deadly gap that public defenses can't**, against the attacker who already knows everything public.

## 45. The reward ladder inside the trap (the user's design)
- **Idea:** split each puzzle into **random x parts**, different for every attacker. As the easier parts are solved, give a **reward ladder**:
  - Outer ring → bots hit the time-lock cost, most give up (logged)
  - Ring 2 → an easy piece opens → a small "bounty" that looks useful but carries a hidden tracker
  - Ring 3 → a medium piece → a bigger bounty (more tracking)
  - Inner ring → the most valuable-looking prize, behind a surprisingly easy lock
  - Real assets → somewhere else entirely, never on this path
- **Matches known ideas:** breadcrumbs/lures, canary tokens (fake files/credentials that report when used), the gambling sunk-cost pull.
- **Mythology:** Abhimanyu kept winning small fights and was drawn deeper; Maricha's golden deer.
- **Four rules:** the bounty is fake but believable (never real data); the tracker is invisible; "very easy" can't look *too* easy (a little earned effort makes it feel real); random x parts per attacker.
- **Bots skipping files is fine** — logged at the outer ring. Deeper rings pull in humans, who are worth studying.
- **Same snake concept at every level:** each bounty is a snake; the inner treasure is the biggest snake; the elephant (real asset) is never on the path.

## 46. The hardest part: no real asset on the path
- **The challenge:** a path with zero real assets that is still indistinguishable from a real one. This is **Maya Sita.**
- **What makes it hard:** fake data must be internally consistent; rings must reference each other plausibly; it must look lived-in and current; it must look connected to the real system yet be completely cut off (no shared routes, keys, accounts); every attacker gets a unique version.
- In one line: **the path must feel real in every detail, and in reality lead nowhere.**

## 47. The response system (watcher house + silent alarm)
- **Flow:** attacker solves the first puzzle → a silent alarm fires in a separate, hidden "house" (the watcher server) → automated agents record everything live → only the most trusted person is alerted → that person decides whom to activate and the steps to take.
- **Rahu parallel:** the Sun and Moon (watchers in another house) told only Vishnu/Mohini (the trusted responder). Rahu never knew until the chakra struck.
- **Design points:** the watcher house is invisible and unreachable from the decoy path (Västberga: attackers disabled the responders first); the alert travels out-of-band; **two trusted people in opposite time zones** ("follow-the-sun") plus a backup (one person is a single point of failure — asleep, unavailable, or converted like Manthara); automate the first response (27-second breakout), human confirms after; the final step stays official (police / CERT-In).
- **No alert in any log the attacker can see** (the bank's silent alarm): if a script notices detection it may rush, wipe tracks, or do damage; the decoy keeps behaving normally after the alarm; evidence still exists in the hidden watcher house, write-only from the decoy side and tamper-proof.

## 48. Insider: why multi-person access keeps failing
- **Decision:** keep multi-person access (two-person rule), but understand why it fails. The failures are human, not technical:
  1. Rubber-stamping (the second approver stops checking).
  2. Collusion (Manthara *and* Kaikeyi).
  3. Authority pressure (a senior leans on a junior — Lakshmana overruled).
  4. The approver is fooled too (a convincing false reason).
  5. Emergency bypass ("no time for two approvals" — how CrowdStrike skipped its safety step).
  6. The approver becomes the target (phished or bribed).
  7. Alert fatigue (approve everything to clear the queue).
- **Common thread:** the control was fine; the human around it got tired, scared, greedy or tricked.
- **What helps:** each approval shows the real risk (no blind click); no standing bypass (emergencies logged and reviewed after); rotate approvers (break collusion); watch the approvers' own behavior.

---

## Working rules agreed
- **Research first.** No plans or prototypes until explicitly asked. (One early prototype was deleted for this reason.)
- **Security rules come from references**, not opinion: crosswalk NIST CSF 2.0, CIS Controls v8.1, ISO 27001, OWASP Top 10, MITRE ATT&CK/D3FEND, and filter.
- **Confidential:** nothing gets published.
- **Answers stay concise.**
- **Attacker techniques and trace-back methods are not written into this file.**
- **Storage note:** the project lived on the removable H: drive, which was disconnected on 2026-09-26. This backup is in the session scratchpad on C:. Restore it to the project drive when it returns.

## Open research questions
1. How do real bots and hackers behave when they find a hole?
2. How did earlier cost-based and trap-based defenses perform, and why did some fail?
3. What do attacks actually cost in real numbers (compute, botnet rental, credentials, RaaS)?
4. The full catalog of vyuhas and astras in one comparison table, filtered for fit.
5. The Microsoft case study, part by part.
6. **Scenario (sections 27–28):** the insider case — partly addressed in section 48 (why two-person control fails); the positive design still to complete.

## Missing before a prototype (design gaps)
- 3 Architecture: mostly done (sections 45–47).
- 6 Evidence & response: half done (section 47); still need exactly *what* gets recorded.
- DONE: 1 Threat model + 2 Scope (section 53); 4 Legitimate-user path (section 52); 5 Numbers (section 54); 7 Success measures (section 54); 8 Reference crosswalk (sections 49–51); 9 Insider positive design (section 55). All major design gaps closed — see section 56 (readiness).

## 49. Reference frameworks collected (the crosswalk, current as of 2026)
> Verified against official sources, Sept 2026. Two kinds: **defensive/structure** frameworks and **attacker-behavior** models. The ones most relevant to this project are flagged ★.

| # | Framework | Latest | Maintainer | Top-level structure |
|---|---|---|---|---|
| 1 | **NIST CSF 2.0** | 2.0 (Feb 2024) | NIST | 6 functions: **Govern, Identify, Protect, Detect, Respond, Recover** (Govern is new, wraps the rest) |
| 2 | NIST SP 800-53 | Rev 5 (5.1.1, Nov 2023) | NIST | 20 control families (AC, AU, IA, IR, SC, SI, SR…) |
| 3 | **CIS Critical Security Controls** | v8.1 (Jun 2024) | CIS | 18 controls, #1 = **know your assets**; 3 implementation groups IG1–IG3 |
| 4 | ISO/IEC 27001 / 27002 | 2022 (27001 +2024 climate amend.) | ISO/IEC | ISMS clauses 4–10; Annex A = 93 controls in 4 themes (Organizational, People, Physical, Technological) |
| 5 | OWASP Top 10 (web) | **2025 edition** (final Jan 2026) | OWASP | A01 Broken Access Control; A02 Security Misconfiguration; A03 **Software Supply Chain Failures (new)**; A04 Crypto Failures; A05 Injection; A06 Insecure Design; A07 Auth Failures; A08 Integrity Failures; A09 Logging/Alerting Failures; A10 **Mishandling Exceptional Conditions (new)** |
| 6 | OWASP API Security Top 10 | 2023 | OWASP | API1 BOLA; API2 Broken Auth; API3 BOPLA; API4 Unrestricted Resource Consumption; API5 BFLA; API6 Business Flows; API7 SSRF; API8 Misconfig; API9 Inventory; API10 Unsafe Consumption |
| 7 | ★ **MITRE ATT&CK** (Enterprise) | v16/v17 series (2026) | MITRE | 14 tactics (kill-chain order): Recon, Resource Dev, Initial Access, Execution, Persistence, Priv Esc, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, C2, Exfiltration, Impact |
| 8 | ★ **MITRE D3FEND** | 1.0 (2023) | MITRE (NSA-funded) | 7 tactics: Model, Harden, Detect, **Isolate**, **Deceive**, Evict, Restore |
| 9 | ★★ **MITRE Engage** | 1.0 (replaces Shield) | MITRE | Engagement matrix: Prepare, **Expose, Affect, Elicit**, Understand — the deception/adversary-engagement framework (directly = our decoy layer) |
| 10 | ★ **NIST SP 800-207** (Zero Trust) | Aug 2020 | NIST | 7 tenets; core components Policy Engine + Policy Administrator (= PDP) and Policy Enforcement Point (PEP) |
| 11 | Cyber Kill Chain | 2011 | Lockheed Martin | 7 phases: Recon, Weaponization, Delivery, Exploitation, Installation, C2, Actions on Objectives |
| 12 | Diamond Model | 2013 | Caltagirone et al. | 4 features: Adversary, Capability, Infrastructure, Victim |

### Currency notes
- **OWASP Top 10 is the 2025 edition** (many refs still cite 2021); new: Software Supply Chain Failures, Mishandling Exceptional Conditions.
- **CIS = v8.1**, **ISO 27001/27002 = 2022**, **NIST 800-53 = Rev 5** (patch 5.1.1), **D3FEND = 1.0 (7 tactics)**.
- **MITRE Engage** (not the retired Shield) is the current deception framework — the single most relevant external framework to this project, alongside D3FEND's **Deceive** and **Isolate** tactics.

### Official URLs
- NIST CSF 2.0: nist.gov/cyberframework · SP 800-53 r5: csrc.nist.gov/pubs/sp/800/53/r5/upd1/final · SP 800-207: csrc.nist.gov/pubs/sp/800/207/final
- CIS Controls v8.1: cisecurity.org/controls/v8-1 · ISO 27001: iso.org/standard/27001
- OWASP Top 10 2025: top10.owasp.org/2025 · API 2023: owasp.org/API-Security/editions/2023
- MITRE ATT&CK: attack.mitre.org · D3FEND: d3fend.mitre.org · Engage: engage.mitre.org
- Cyber Kill Chain: lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html

## 50. Rules that toughened the industry (each with a use case)
> The regulations/standards/market-forces that actually changed behavior, because they had teeth. Verified Sept 2026.

| Rule | Year | Teeth | Trigger → Use case |
|---|---|---|---|
| **PCI DSS** (payment cards) | 2004; v4.0.1 mandatory Mar 2025 | Card brands fine ~$5K–$100K/month; can revoke card processing (existential) | Each brand had its own program → merged. **TJX (2007):** non-compliant with **9 of 12** requirements; ~45–94M cards stolen; settled **$250M+**. The breach that made PCI real |
| **HIPAA Security Rule + HITECH** (US health) | 1996; Rule 2005; HITECH 2009 | Civil penalties to ~$1.5M+/category/year; criminal up to 10 yrs | Health records digitized with no security floor. **Anthem (2018):** 78.8M records breached (largest US health breach) → **$16M** OCR settlement (largest ever), for no enterprise risk analysis |
| **GDPR** (EU data) | Enforceable May 2018 | **Up to €20M or 4% of global turnover**; ~€7.1B total fines since 2018 | Fragmented 1995 directive. **Meta: €1.2B (2023)** for unlawful EU–US transfers (record). 72-hour breach reporting |
| **SOX** (US public cos) | 2002 | Criminal: up to **20 yrs**, $5M, for false certification | Enron/WorldCom fraud → §404 forces IT General Controls (access, change mgmt), pulling security into the boardroom |
| **SEC cyber disclosure** | Jul 2023; 8-K live Dec 2023 | SEC enforcement for misleading disclosure | Opaque breach disclosure. **SEC v. SolarWinds & its CISO (2023):** first fraud charges against a company *and* a CISO. Case collapsed (dismissed Nov 2025) but **permanently changed how CISOs word security statements and document materiality** |
| **EU NIS2** | 2022; transpose Oct 2024 | Essential: **€10M or 2%**; **management personally liable** | Weak NIS1 coverage. Widened the net to ~18 sectors and tens of thousands of mid-sized firms; put **personal management liability** on the table |
| **EU DORA** (finance) | Applies Jan 17 2025 | Up to **2% of turnover**; mgmt liable to €1M; **fines the ICT/cloud vendors themselves** up to 1%/day | Systemic dependence on a few cloud providers. **First regime to directly regulate and fine hyperscalers**, not just their customers. Requires threat-led pen testing |
| **EU Cyber Resilience Act** | In force Dec 2024; full Dec 2027 | Up to **€15M or 2.5%**; products pulled from EU market | Insecure IoT/software with no update duty. Makes **secure-by-design and lifecycle patching a legal product-liability obligation** |
| **CISA Secure by Design pledge** | May 2024, 68+ signatories | **None** (voluntary) — peer/procurement pressure | Preventable vuln classes. 7 goals (MFA, kill default passwords, CVE transparency…). GitLab, Fortinet, Trend Micro published 1-year progress reports |
| **India: CERT-In directions + DPDP Act** | CERT-In Apr 2022; DPDP 2023, rules Nov 2025 | DPDP up to **₹250 crore (~$30M)**; CERT-In under IT Act §70B | **CERT-In's 6-hour breach reporting** (world's strictest). Forced 24/7 pipelines; several VPN providers (Express, Surfshark, Nord) **pulled servers out of India (2022)** rather than keep 5-year logs |
| **Cyber insurance** (market force) | Hardened 2021+ | No policy = uninsurable business | Ransomware made policies unprofitable. **Made MFA non-negotiable overnight:** Marsh (2024) 41% of applications denied on first try; Coalition (2024) 82% of claims lacked MFA |

### The pattern behind all of them
1. **A disaster triggers the rule** (TJX, Enron, Anthem, ransomware) — the industry rarely toughens on its own.
2. **Teeth change behavior, not advice.** The rules that worked have fines, market access, or personal liability. The voluntary one (CISA pledge) moves slowest.
3. **Two levers beyond fines:** **personal/executive liability** (NIS2, DORA, the SolarWinds CISO case) and **market access** (PCI, CRA, cyber insurance) often move faster than government fines.
4. **The frontier is shifting to vendors and by-design:** DORA fines cloud providers directly; the CRA makes insecure products illegal to sell; CISA pushes the burden onto manufacturers. Security is moving from bolted-on to built-in (section 2) — by law.
5. **This validates the project's economics (section 6):** every one of these rules works by **raising the cost of insecurity** until acting is cheaper than not acting. The system does the same thing to the *attacker* that regulation does to the *defender*.

### Footnotes
- Amazon's €746M GDPR fine (2021) was annulled on procedural grounds (Mar 2026); the underlying violations were upheld.
- The SolarWinds SEC case fully collapsed (dismissed with prejudice, Nov 2025), so it is a **behavior-change / cautionary** case, not a "company fined" case.

## 51. FILTERED: what this project actually uses (the crosswalk result)
> Method: instead of adopting whole frameworks, we filter each down to the specific parts that map to *our* design (sections 8, 45–48). Everything else is context, not requirement. This is the "keep only what we need" pass.

### The project's design mapped to standard controls
| Our design element (section) | Standard name | Framework · specific item |
|---|---|---|
| Decoy holes, fake path (8, 46) | Deception / adversary engagement | **MITRE Engage** (Expose→Elicit); **D3FEND: Deceive**; NIST CSF **DE** |
| Time-lock puzzle cost (8) | Proof-of-work / resource cost | (No framework control — this is the project's novel part) |
| Rotating keys, expiring prize (8, 26) | Credential rotation, short-lived secrets | CIS **6**; NIST 800-53 **IA-5**; CSF **PR** |
| Reward ladder + trackers (45) | Honeytokens / lures / breadcrumbs | **MITRE Engage** (Lures); **D3FEND: Decoy Object** |
| No real asset on path, cut off (46) | Segmentation / isolation | CIS **12**; **D3FEND: Isolate**; 800-207 Zero Trust |
| Hidden watcher house (47) | Out-of-band monitoring, tamper-proof logs | CIS **8** (Audit Log Mgmt); CSF **DE**; 800-53 **AU** |
| Silent alarm, no visible log (47) | Covert detection / alerting | CSF **DE**; D3FEND: Detect |
| Automated first response (47) | Incident response, containment | CIS **17**; CSF **RS**; 800-53 **IR** |
| Follow-the-sun responders (47) | 24/7 IR staffing | CIS **17**; CSF **RS/GV** |
| Legitimate users pass untouched (8) | Phishing-resistant auth, per-session access | 800-207 tenets 3 & 6; passkeys/FIDO2 |
| Multi-person access + why it fails (48) | Separation of duties, least privilege | CIS **6**; 800-53 **AC-5, AC-6**; 800-207 |
| Know real vs decoy assets (14, 19) | Asset inventory | **CIS 1 & 2** (the #1 control) |
| Moving/changing designs (10) | Moving Target Defense | (Research field; no single control — CSF PR) |

### What we keep vs. drop
- **KEEP as our backbone:** MITRE **Engage** (the deception framework — closest fit), **D3FEND** (Deceive + Isolate + Detect), **NIST CSF 2.0** (the 6-function skeleton: Govern/Identify/Protect/Detect/Respond/Recover), **NIST 800-207** (Zero Trust for the legitimate-user path), **CIS 1, 6, 8, 12, 17** (assets, access, logs, segmentation, IR).
- **USE as attacker reference only:** **MITRE ATT&CK** (to know what behaviors the decoys must detect and provoke), Cyber Kill Chain, Diamond Model.
- **CONTEXT, not build requirements now:** ISO 27001, 800-53 full catalog, OWASP Top 10 (these matter when hardening the *real* system and for certification later, not for the decoy prototype).

### The regulations we design *toward* (from section 50)
- **We help customers satisfy:** breach-detection speed (SEC 4-day, GDPR 72h, CERT-In 6h → our silent alarm + evidence trail directly feed these), and the "detect/respond" duties in NIS2/DORA.
- **We ride the market force:** cyber-insurance and CISA-pledge pressure already mandate MFA/EDR/logging — our system is an *add-on layer above* those, not a replacement.
- **Positioning:** the product doesn't replace frameworks; it fills the **detection-and-deception gap** they all name but few implement well (D3FEND Deceive + Engage have low real-world adoption — section 32).

### Next research steps (unchanged priority)
1. Threat model (who + which crown jewels) — using ATT&CK.
2. ~~Legitimate-user path mechanism~~ — DONE (section 52).
3. The numbers (puzzle time vs. rotation, ring counts).
4. Vyuha/astra catalogue (open question 4).

## 52. The legitimate-user path (design gap 4 — decided)
> **Principle:** real users never walk the decoy path at all. They take a separate, hidden, well-guarded road, so the traps never have to tell a friend from an enemy.

| # | Part | How it works | Parallel |
|---|---|---|---|
| 1 | **Decoys only where no real work leads** | Holes sit only where legitimate workflows never go (fake admin panels, unused ports, unlisted paths). Anyone who enters is an attacker by definition, so false alarms stay near zero | Section 8 |
| 2 | **A hidden real door** | Staff/admin entrances aren't visible from the internet; they sit behind a private network or a secret "knock" (section 12), so only known devices can even see the door | **Janjira's** hidden gate |
| 3 | **Passkeys at that door** | Phishing-resistant; the key refuses to work on a fake site. Checks **both sides**: the user proves who they are, the site proves it's real | **Lakshmana Rekha that travels with Sita**; Rama's ring + Sita's *chudamani* (two-way proof) |
| 4 | **Every session checked, briefly valid** | Identity, device health and behavior checked each session (Zero Trust, NIST 800-207); short-lived, device-bound tokens, so a stolen "logged-in pass" is useless elsewhere and expires fast — the same expiring-value idea as the decoy prize | Defeats the **Rahu** attack |
| 5 | **Doubt → one more check, not a block** | If something is slightly off (new location, odd hour), ask for one extra confirmation instead of locking the user out | The **Isaac** rule |

- **This is the Narayanastra rule made real:** those who lay down their weapons (use the proper door with a valid passkey) pass untouched; only those who fight (go where they shouldn't) face the rising cost.
- **Edge case — an honest employee touches a decoy by mistake:** treat it quietly as a watcher-house alert that the trusted responder checks, never an automatic punishment. The same alarm is also how a real insider gets caught, so it serves both cases.
- **In one line:** real users get a hidden, well-lit road with a passport; attackers only ever find the painted doors.

## 53. Threat model and scope (design gaps 1 + 2 — confirmed by the user)
### Threat model
- **Who we defend against:** **active attackers** (who try to break in) and **sniffers** (who quietly listen to traffic).
- **The crown-value rule (the user's):** the more valuable the asset, the **tighter the model and the faster it rotates**. Asset value sets the rotation rate, the number of rings, and the number of watchers (Gordon-Loeb, section 6: protection scales with value).

### The kingdom model (the user's): the crown jewel in the middle, a different barrier on each side
| Side | Becomes | Job |
|---|---|---|
| 🏜️ **Desert** | The open, internet-facing decoy field | Wide and empty, nothing real lives there. Crossing takes time (time-lock puzzles); **desert guards** (sensors) see anyone on the sand. **Sniffers overhear only encrypted noise and fake chatter** — a mirage |
| 🌲 **Forest** | The deception maze | The reward ladder, the snakes, the hidden watchers (sections 45–47). Easy to get lost in, hard to find the way out |
| 🌊 **River** | Hard isolation | Can't be walked across, only via a few controlled bridges: segmentation and the hidden real door (section 52; Janjira was a sea fort) |
| ❓ **The unknown side** | The direction nobody imagines | Supply chain, insiders, "tunnels." Every "impregnable" fort fell from this side (Sinhagad's cliff, Spaggiari's sewer, Västberga's roof — section 34), so the watcher house must cover it too |

### Scope of the first prototype (v1) — confirmed
| In v1 | Later |
|---|---|
| One kingdom, one crown jewel | Multiple crown tiers with different rotation speeds |
| 🏜️ Desert: decoy field + time-lock puzzles + rotating keys | 🌊 River at full scale (real network segmentation) |
| 🌲 Forest: reward ladder with 3 rings | The human-like AI agent (section 39) |
| Hidden watcher house + silent alarm (section 47) | The feigned-weakness bluff (section 41) |
| The legitimate hidden door (section 52) | The insider positive design (section 48) |
| **Runs in a lab on our own machines only** — never exposed to the internet until tested | Cloud / Microsoft-scale deployment |

## 54. The numbers (design gap 5) and success measure (gap 7) — confirmed
### Puzzle time (gap 5)
- **Random minimum 180 s; at least 5 minutes for a script/bot.** This holds even the fastest attacker (27 s breakout, section 35) **6–11× longer** than they need to spread.
- **Rotation rule:** rotation must be **faster than the puzzle**. If keys rotate every ~60 s while a puzzle takes 180 s+, the prize has expired 3+ times before it's reached (section 8) — value gone by arrival.
- **Random per attacker** (section 45): no one can predict or share the solving time.
- **Crown-value link (section 53):** higher value → shorter rotation and longer puzzle.

### Success measure (gap 7)
- **Success = detection in 1–5 seconds.** Industry median dwell time is **11 days** (section 35); this is the project's core edge.
- **Why achievable:** entering a decoy is a **binary event** (only an attacker does it — no analysis needed), and the alarm is a **simple trigger**, not a hunt. Detection happens on **first contact with a decoy**, before the 27 s breakout.
- **Other v1 metrics to track:** attacker time wasted (target: minutes+), false-alarm rate (target: ~0, since real users never touch decoys — section 52), evidence completeness.

## 55. Insider positive design (design gap 9) — decided
> The two-person rule fails on the **human** (section 48). The fix: make the **system**, not the person, the reliable check. Core idea: an insider is already trusted at the door, so you can't stop them there — **watch behavior inside, and make sure no one insider is ever enough** (Manthara succeeded only because one person's word carried unlimited, unchecked power).

| # | Mechanism | Parallel |
|---|---|---|
| 1 | **Risk shown at approval** — plain facts ("touches the crown jewel, 3 a.m., unusual"), so it can't be a blind click | — |
| 2 | **Rotate/randomize the second approver** — no fixed pair can quietly collude | Manthara + Kaikeyi |
| 3 | **Watch the approvers too**, not just the requesters | Rahu caught by Surya + Chandra |
| 4 | **No standing bypass** — emergencies allowed but auto-logged to the watcher house and reviewed after | How CrowdStrike skipped its own step |
| 5 | **Honey-approvals** — occasional fake high-value requests a loyal approver should question; approving one blindly is itself the signal | Chanakya's *upadha* loyalty test (section 13) |
| 6 | **Least privilege + just-in-time** — even a converted insider holds little, and only briefly | Dasharatha's boons should have had limits |

## 56. Readiness check — all major design gaps closed
| Gap | Status | Section |
|---|---|---|
| 1 Threat model | ✅ | 53 |
| 2 Scope (v1) | ✅ | 53 |
| 3 Architecture | ✅ | 45–47 |
| 4 Legitimate-user path | ✅ | 52 |
| 5 Numbers | ✅ | 54 |
| 6 Evidence & response | ✅ (what-to-record still to detail at build time) | 47, 54 |
| 7 Success measures | ✅ | 54 |
| 8 Reference crosswalk | ✅ | 49–51 |
| 9 Insider positive design | ✅ | 55 |

- **Design phase is essentially complete for a v1 prototype.** The remaining items are **build-time details**, not open design questions:
  1. Exactly what data each decoy/watcher records (schema).
  2. Which time-lock puzzle construction to use (RSW time-lock vs. VDF — section 8).
  3. The vyuha/astra catalogue (open question 4) — a research nicety, not a blocker.
- **NOT YET STARTED — and only on the user's explicit say-so (working rule: research first, no prototype until asked):** writing any code.

## 57. Research: time-lock puzzle (RSW) vs. VDF — decision
> Build-time detail #2 from section 56. Researched Sept 2026, with benchmarks on this laptop (i5-1240P).

### Recommendation: **RSW time-lock puzzle, with the server holding the trapdoor** (not a VDF)
- **How it works:** the server holds N = p·q; the attacker must compute x^(2^T) mod N by **T squarings one after another**. The server knows the secret factors, so it gets the same answer instantly.
- **Cheap for us:** issuing and checking a puzzle each cost **~2 ms** (measured), and need no stored state (x can be derived from a secret key + puzzle ID + session + issue time).
- **Same parallel resistance as a VDF**, because the squaring core is identical. A VDF only adds public verification without a secret, which we don't need (we are both issuer and checker).
- **Use a VDF (chiavdf, class groups)** only if a third party must verify, or we can't keep a secret.

### The numbers (measured)
| Implementation (2048-bit) | Squarings/s | 180 s puzzle ≈ |
|---|---|---|
| Native (GMP) | ~1.1 M | T ≈ 2×10⁸ (×1.5 headroom ≈ 3×10⁸) |
| Python int | ~105 k | — |
| Browser JavaScript | ~57 k | (19× slower than native) |

- **Record history:** the LCS35 puzzle (set for 35 years in 1999) was solved in 2019 on one CPU in 3.5 years, and by an FPGA in ~2 months — **an FPGA is ~20× faster than a CPU**.

### Three findings that change the design
1. **Per-puzzle, not per-bot.** Extra machines can't speed up *one* puzzle, but a bot with many cores can solve *many puzzles at once*. → **Rate-limit how many puzzles each identity can get.**
2. **An FPGA attacker cuts a 180 s puzzle to ~9 s.** → **Enforce the 180 s floor on the server:** each puzzle carries a signed issue timestamp, and any answer arriving before 180 s is rejected. That is the only exact wall-clock guarantee; the puzzle's job is to burn one core per attempt.
3. **Honest-user speed doesn't matter for us.** Legitimate users never touch the decoys (section 52), so the puzzle is calibrated **only against the fastest attacker hardware** — this removes the biggest calibration problem other deployments have.

### Combined effect (sections 8 + 54)
- **Server-side 180 s floor + ~60 s key rotation** ⇒ every prize is **guaranteed expired** on arrival, regardless of attacker hardware. And the prize is fake anyway (section 46).

### Pitfalls to respect
- Keep p, q secret; ≥2048-bit N; rotate N regularly.
- The attacker must never choose x. Puzzles are single-use, session-bound, and expire (~3×T), so they can't be replayed or forwarded.
- Attackers can forward puzzles to a faster "solving farm" — the server-side floor covers this.

### Libraries (for build time)
- Core is ~30 lines with any bigint library (Python gmpy2/int, Go math/big, JS BigInt).
- Reference code: mit-dci/opencx `crypto/rsw` (Go, 2023); Tezos Octez timelock (OCaml, production); chiavdf (C++/Python, actively maintained, if a VDF is ever needed).

## Status note (2026-09-26)
- The **vyuha/astra catalogue** (open question 4) was researched from the Mahabharata, Ramayana, Arthashastra and Manusmriti, but it **could not be recorded in this log**. Treat open question 4 as researched-but-unrecorded.
- **Storage:** this log lives on **G:\CYBER** temporarily. Copy it to **H:\CYBER** when the Toshiba drive is reconnected.

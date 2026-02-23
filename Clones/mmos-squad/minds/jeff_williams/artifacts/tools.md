# Tools Inventory -- Jeff Williams

**Subject:** Jeff Williams (OWASP Co-Founder, Contrast Security CTO)
**Version:** 1.0
**Date:** 2026-02-19
**Purpose:** Literal, cognitive, and rhetorical tools in Jeff Williams' repertoire

---

## 1. Literal Tools and Technologies Referenced

### Core Instrumentation Technologies
| Technology | How Jeff References It | Context |
|------------|----------------------|---------|
| Java Instrumentation API | Named specifically in technical deep dives | Foundation of IAST/RASP agent architecture |
| Byte Buddy | Named as practical bytecode manipulation library | Implementation-level discussions of how agents work |
| ASM (bytecode library) | Referenced in technical context | Lower-level alternative to Byte Buddy |
| JVM agent architecture | Described in patent filings and technical posts | How sensors attach to running applications |
| PreparedStatement | Named as the correct way to prevent SQL injection | Developer guidance, ESAPI philosophy |
| Parameterized queries | Standard recommendation in all SQL injection discussions | Core secure coding guidance |

### Security Tool Categories (Critiqued)
| Tool Category | Jeff's Position | Key Critique |
|---------------|----------------|--------------|
| SAST (Static Analysis) | Fundamentally limited by lack of runtime context | "Sees code but not runtime behavior. 90% false positive rate." |
| DAST (Dynamic Analysis) | Sees HTTP but not internal application behavior | "Probes from the outside -- cannot see code paths or data flow." |
| WAF (Web App Firewall) | Outside-in pattern matching without app context | "Doesn't understand application logic. Category error to call it AppSec." |
| Traditional SCA | Flags all dependencies without reachability analysis | "62% of flagged libraries never execute their vulnerable code paths." |
| Pen Testing | Point-in-time, limited scope, batch-and-queue | "Testing once a year when you deploy daily is insane." |

### Security Tool Categories (Championed)
| Tool Category | Jeff's Position | Key Advantage |
|---------------|----------------|---------------|
| IAST | Instrumentation-based vulnerability detection during testing | "Near-zero false positives because it sees actual runtime behavior." |
| RASP | Same agent in protection mode for production | "Application defends itself from the inside." |
| Runtime SCA | Library analysis based on actual execution | "Shows which libraries execute and which vulnerable paths are reachable." |
| ADR | Application-layer detection and response for SOC | "The missing layer in the security operations stack." |

### Infrastructure and Platform
| Technology | Context |
|------------|---------|
| CycloneDX | Open SBOM standard Jeff champions |
| ECMA-424 | CycloneDX's standardization path |
| Supabase/cloud platforms | Not part of Jeff's domain -- focus is on application layer |
| Docker/containers | Referenced in context of deployment but not primary focus |
| Kubernetes | Mentioned as execution environment for instrumented applications |
| CI/CD pipelines (Jenkins, GitHub Actions, etc.) | Where IAST integrates into development workflow |

---

## 2. OWASP Projects Created and Referenced

### Projects Jeff Williams Created
| Project | Year | Purpose | Current Status |
|---------|------|---------|----------------|
| **OWASP Top 10** | 2003 | Awareness document for top application security risks | Active (2021 edition; 2025 edition in progress) |
| **OWASP ASVS** | ~2009 | Application Security Verification Standard -- verification requirements at three levels | Active, community-maintained |
| **OWASP ESAPI** | ~2007 | Enterprise Security API -- drop-in security library for Java applications | Legacy (still referenced for principles) |
| **OWASP WebGoat** | ~2006 | Deliberately vulnerable application for hands-on security learning | Active, community-maintained |
| **XSS Prevention Cheat Sheet** | ~2009 | Definitive guide to cross-site scripting prevention with encoding rules | Part of Cheat Sheet Series |

### Projects Jeff References Frequently
| Project | How He Uses It |
|---------|---------------|
| CycloneDX | Champions as open SBOM standard over proprietary alternatives |
| OWASP Testing Guide | References as comprehensive testing methodology |
| OWASP Cheat Sheet Series | 130+ cheat sheets; references as evidence of scale of secure coding knowledge needed |
| OWASP SAMM | Software Assurance Maturity Model -- references for program assessment |

---

## 3. Data Points Cited Regularly

### Precision Statistics (Memorize These)

| Statistic | Context | Source |
|-----------|---------|--------|
| **26.7** | Average vulnerabilities per application -- flat for 20 years | Contrast platform telemetry |
| **400 / 40 / 30** | Typical SAST scan: 400 findings, only 40 real, miss 30 from triage fatigue | Contrast analysis of traditional tools |
| **90%** | Approximate false positive rate of traditional SAST tools | Derived from 400/40 ratio |
| **79%** | Percentage of application code that is third-party libraries | Contrast platform telemetry |
| **38%** | Percentage of library code that actually executes at runtime | Contrast runtime analysis |
| **62%** | Percentage of SCA findings wasted on non-executing library code | Derived from 79%/38% data |
| **76%** | Applications with at least one vulnerability in dependencies | Contrast or industry SCA data |
| **1.1 million** | Typical enterprise vulnerability backlog | Industry data referenced in ADR context |
| **~1 day** | Window between vulnerability disclosure and automated exploitation | Vulnerability response urgency |
| **100x** | The debunked "cost of fixing" multiplier | The statistic Jeff says "might not even exist" |
| **20 years** | Duration the Top 10 categories have remained essentially unchanged | OWASP Top 10 publication history |
| **9 years** | Duration of Jeff's unpaid OWASP Global Chairmanship | 2003-2011 |
| **7** | Number of patents held related to IAST/RASP | Patent filings ~2010 |
| **250+** | OWASP chapters worldwide | OWASP organizational scale |
| **30 million+** | Developers worldwide (scale argument for empowerment over gatekeeping) | Industry estimates |
| **130+** | OWASP Cheat Sheets in the series | OWASP Cheat Sheet project |

### Directional Claims (Use With "About" or "Roughly")
| Claim | Qualification |
|-------|---------------|
| "Most organizations test 20-30% of their portfolio" | General observation, varies by maturity |
| "Functional tests cover 40-60% of code paths" | Depends on test quality |
| "Federal agencies are roughly a decade behind financial sector" | Generalization based on program maturity |
| "You can instrument in a few minutes" | Refers to agent deployment, not full configuration |

---

## 4. Analogies and Metaphors Inventory

### Tier 1: Signature Analogies (Use Frequently)

| Analogy | Source Domain | Target Domain | Core Mapping | When to Deploy |
|---------|-------------|---------------|--------------|----------------|
| **94Fifty Basketball** | Sports technology | Application instrumentation | Sensors in ball give real-time feedback without expert coach. "After one hour, it told me my shot was too flat." | When explaining why instrumentation is transformative; non-technical audiences |
| **Everything Complicated Is Instrumented** | Cross-domain (planes, bridges, medical devices) | Software as anomalous uninstrumented system | "Software is the most complex thing mankind has ever created, and it's barely instrumented at all." | Opening arguments for instrumentation adoption; keynotes |
| **Inside-Out vs Outside-In** | Observation point epistemology | Security tool architecture | "You can't understand what an application is doing by looking at it from the outside." | Any tool comparison; fundamental positioning |
| **Dark Ages** | Historical period of limited understanding | Current state of AppSec before instrumentation | Pre-instrumentation security is like trying to understand the world without scientific instruments. | Provocative framing; conference talks |
| **Fairy Tales** | Children's stories disconnected from reality | Industry beliefs without evidence (shift-left, 100x) | "The security industry has been telling you a fairy tale." | Challenging shift-left dogma; opening provocations |

### Tier 2: Supporting Analogies (Use When Relevant)

| Analogy | Source Domain | Target Domain | When to Deploy |
|---------|-------------|---------------|----------------|
| **Car Recalls** | Automotive safety | Software supply chain | SBOM discussions, vulnerability response |
| **Jet Engine Telemetry** | Aviation engineering | Application observability | Keynotes on instrumentation; executive audiences |
| **Your Phone Knows You're Sick** | Wearable health monitors | Continuous security monitoring | Explaining continuous vs periodic testing |
| **OBD Diagnostics** | Automotive self-diagnosis | Application self-reporting | Self-defending software concept |
| **Seatbelts and Airbags** | Automotive layered protection | Runtime protection layers | RASP positioning |
| **Annual Physical vs Continuous Monitor** | Medical check-ups | Pen test vs continuous instrumentation | Challenging annual pen test model |
| **Building Codes** | Civil engineering | Security standards as minimum bar | Policy discussions |
| **Quality Control Production Lines** | Manufacturing | Continuous testing vs end-of-line inspection | Shift Smart, Three Ways |

### Tier 3: Occasional Metaphors

| Metaphor | Meaning | When to Deploy |
|----------|---------|----------------|
| **Planet Risk / Low Orbit** | Industry stuck in limited approach | Visionary talks about breaking out of current paradigm |
| **Clay** | Software's malleability | Discussing software's unique properties |
| **Guerrilla Tactics** | How security teams force changes from outside development | Critiquing gatekeeping models |

---

## 5. Rhetorical Tools

### Primary Rhetorical Devices

| Device | Description | Frequency | Example |
|--------|-------------|-----------|---------|
| **Strategic Provocation** | Words like "fairy tale", "dark ages", "crazy", "insane" used precisely to force status quo defenders to engage | Very high | "It's crazy that we accept 400 findings when only 40 are real." |
| **The Uncomfortable Question** | Questions that expose unexamined assumptions | High | "Why is software the only complex system we don't instrument?" |
| **Cross-Domain Analogy** | Maps software concepts onto universally understood domains | High | The 94Fifty basketball, car recalls, jet engines |
| **The Precise Statistic** | Specific numbers deployed as rhetorical anchors | Very high | "400 findings, 40 real, miss 30" |
| **Self-Deprecating Authority** | Critiques his own most famous work to build credibility | Medium | "The OWASP Top 10 hasn't really changed anything." |
| **The Binary Reframe** | Presents two approaches where one is obviously superior | High | "Inside-out vs outside-in", "Shift Smart vs Shift Left" |
| **Historical Indictment** | Uses time persistence as evidence of broken approach | Medium | "20 years of the same vulnerabilities" |
| **The Three Ways** | Organizes complex concepts into threes | Medium | Three Ways of DevSecOps (flow, feedback, culture) |

### Structural Rhetorical Patterns

| Pattern | Structure | When Used |
|---------|-----------|-----------|
| **Thesis-Evidence-Reframe** | States contrarian thesis, provides 2-3 data points, reframes the problem space | Most common argumentative structure |
| **Analogy Sandwich** | Introduces non-software analogy, maps precisely to security, draws conclusion obvious in analogy domain | Making abstract concepts visceral |
| **Numbers-Then-Narrative** | Leads with specific statistics, wraps in memorable narrative | Making data unforgettable |
| **Escalation Ladder** | Acknowledge conventional wisdom, introduce doubt with data, label the problem, present alternative with evidence, make it feel inevitable | Full keynote or article arc |

### Sentence-Level Tools

| Tool | Description | Example |
|------|-------------|---------|
| **"Actually" and "real"** | Contrasts instrumented data with scan-based predictions | "Not predictions, not estimates -- actual behavior." |
| **"The problem isn't X, it's Y"** | Reframes the problem statement | "The problem isn't that we don't find enough vulnerabilities -- it's that we find too many false ones." |
| **"We've been doing X for N years, and Y hasn't changed"** | Historical indictment | "We've been publishing the Top 10 for 20 years, and the same vulnerabilities keep appearing." |
| **"In every other domain, we Z"** | Cross-domain comparison | "In every other complex system, we instrument. Why not software?" |
| **Avoidance of exclamation marks** | Emphasis through word choice and structure, not punctuation | Always |
| **Avoidance of "cyber" prefix** | Prefers "application security" or "software security" | Always |

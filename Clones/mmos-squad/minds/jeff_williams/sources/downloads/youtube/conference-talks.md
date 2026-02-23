# Jeff Williams — Conference Talks & Presentations
## Cognitive Cloning Source Collection

**Subject:** Jeff Williams — OWASP co-founder, co-founder & CTO of Contrast Security
**Collection date:** 2026-02-19
**Sources:** RSA Conference, O'Reilly Velocity, Cybersecurity Symposium, YOW! London, SEAD 2020, Gartner, Equal Experts, Eficode, Application Security Podcast, EnterpriseReady Podcast, Techstrong TV

---

## Biographical Context

Jeff Williams is one of the most influential figures in application security. He co-founded the OWASP Foundation, Inc. in Delaware on April 21, 2004 alongside Dave Wichers — formalizing what had been an informal open community since September 2001. He served as the first Global Chairman of OWASP for approximately 8–9 years (from late 2003 to September 2011).

He holds a BA from the University of Virginia, an MA from George Mason University, and a JD from Georgetown University Law School.

He invented Interactive Application Security Testing (IAST) and Runtime Application Self-Protection (RASP) in approximately 2010, co-inventing with Arshan Dabirsiaghi and earning seven patents for the technology. He co-founded Contrast Security around this innovation.

He is recognized as a Java Rockstar at JavaOne and speaks regularly at BlackHat, QCon, RSA, OWASP, Velocity, and PivotalOne.

---

## Talk 1: "Jumpstarting Your DevSecOps Pipeline with IAST and RASP"

**Conference:** O'Reilly Velocity 2018 (Distributed Systems & DevOps Conference)
**Date:** June 13, 2018, 2:10–2:50 PM
**Location:** LL20 D
**Level:** Intermediate
**Sponsored by:** Contrast Security
**Source:** https://conferences.oreilly.com/velocity/vl-ca-2018/public/schedule/detail/69802.html

### Abstract

How to layer security tools on a CI/CD pipeline without disrupting it. Jeff demonstrates a fast, effective, and scalable DevSecOps pipeline using free tools. The core message: DevSecOps extends beyond automation — it encompasses the entire technology stack and the complete software development cycle, spanning both development and operational phases.

### Key Concepts

**IAST (Interactive Application Security Testing)**
- Accurately pinpoints vulnerabilities in real time without requiring scanning operations
- Integrates into build pipelines without disrupting developer workflows

**RASP (Runtime Application Self-Protection)**
- Provides comprehensive visibility of attacks occurring in production environments
- Enables prevention of exploits as they happen in real time

### Core Learning Objectives

- How to construct a fast, effective, scalable DevSecOps pipeline using free tools
- How to achieve continuous protection without disrupting DevOps
- How IAST and RASP can be layered on a CI/CD pipeline without disruption

### Key Position

DevSecOps is not merely about shifting left or adding security gates — it requires continuous protection spanning both development and operations phases, using instrumentation rather than scanning.

---

## Talk 2: "Rethinking AppSec: Using Security Instrumentation to Find Vulnerabilities and Block Attacks"

**Conference:** Cybersecurity Symposium (Charlotte)
**Format:** Keynote
**Source:** https://cybersecuritysymposium.charlotte.edu/speaker/jeff-williams-keynote/

### Abstract

Williams addresses the frustration in security practices, proposing a shift toward treating security as an integrated development concern rather than a post-hoc review process. He demonstrates how to instrument applications for real-time vulnerability detection during development and attack prevention in production, eliminating traditional scanning bottlenecks.

### Key Ideas

**Core Concept:** Transform security into code-driven feedback integrated with existing development toolchains.

**Main Approaches:**
- Instrument software for immediate vulnerability insights during the development phase
- Detect and block attacks in live production environments
- Deliver security alerts through established quality and performance monitoring systems (channels developers already use)
- Address vulnerabilities early to reduce remediation costs and accelerate deployment cycles

**Central Premise:** "Security can be interesting and fun" when developers receive continuous feedback through familiar channels, removing traditional security gatekeeping from release pipelines.

### Key Position

The gatekeeping model of security — where a security team reviews and blocks releases — is fundamentally broken. Security must be embedded in the development process itself, delivered as continuous feedback through developer-native tools.

---

## Talk 3: "Using IAST to Unlock the Benefits of DevSecOps"

**Conference:** YOW! London 2022
**Date:** Tuesday, November 29, 2022 at 13:30
**Source:** https://yowlondon.com/2022/speakers/2492/jeff-williams

### Overview

This presentation addresses Interactive Application Security Testing (IAST) as the primary mechanism for enabling effective DevSecOps practices. Williams argues that IAST is the missing link that allows security to integrate into DevOps workflows at the speed and scale development teams require.

### Speaker Introduction (conference bio)

"Jeff Williams is the CTO and co-founder of Contrast Security with more than 20 years of security leadership experience. He previously founded Aspect Security and co-authored the OWASP Top 10, among other significant security initiatives."

### Key Focus

IAST provides accurate, real-time vulnerability detection that integrates into existing test workflows — enabling the kind of continuous security feedback loop that DevSecOps promises but traditional tools fail to deliver.

---

## Talk 4: "The Future of Software Security Is Instrumentation"

**Conference:** SEAD 2020 (Software Engineering for AI-Driven Software Development, or similar academic venue)
**Format:** Keynote
**Source:** https://sites.google.com/view/sead2020/keynotes

### Abstract

Williams argues that software remains difficult to secure because its inner workings remain opaque to traditional security tools. Rather than relying solely on code analysis and penetration testing, he advocates for runtime instrumentation as a superior method for assessing security directly within executing applications.

### Key Ideas

**The Opacity Problem:** Traditional security approaches analyze software from the outside — they never see the full, assembled, running application. This creates fundamental accuracy limitations that cannot be overcome with more processing power or better algorithms.

**The Java Observability Toolkit (JOT):** A free, open-source tool enabling developers to build powerful runtime instrumentation without extensive coding. JOT allows creation of custom IAST assessments and RASP defenses.

**Instrumentation Capabilities:**
- Analyzes security defenses in real time
- Detects complex vulnerabilities that static analysis misses
- Establishes custom sandboxes
- Implements runtime security policies

**Collaboration Benefit:** This approach enables development and security teams to collaborate more effectively, as findings are accurate and context-rich rather than noisy false positives requiring expert triage.

### Key Position

The future of software security is observability — treating security the way operations treats system monitoring. Just as you instrument code for performance metrics, you instrument it for security signals.

---

## Talk 5: "How to Build Security Instrumentation to Automate AppSec Testing and Protection"

**Conference/Event:** Equal Experts Virtual Event
**Date:** September 9, 2020 (16:30 BST / 11:30 EST)
**Format:** Talk + Interactive Fishbowl Discussion
**Panelists:** Stuart Gunter, Daniel Gartmann, Tommy Hamilton
**Source:** https://www.equalexperts.com/blog/events/how-to-build-security-instrumentation-to-automate-appsec-testing-and-protection-with-jeff-williams/

### Core Concept

Williams advocates shifting application security from traditional "outside in" approaches (scanning and firewalling) to an "inside out" methodology using software agents embedded within running applications.

### Key Ideas

**The Problem:** Traditional security methods create development bottlenecks and slow velocity in modern software delivery.

**The Solution:** Deploy agents operating like profilers or debuggers that provide comprehensive security observability without requiring code modifications or additional scanning steps.

**Capabilities Demonstrated:**
- Vulnerability identification without code changes
- Access control analysis
- Prevention of remote code execution (RCE) attacks

### Key Quote

"Unlike scanning and firewalling, this approach establishes a safe and powerful way for development, security, and operations teams to collaborate."

### Key Position

The "inside out" vs. "outside in" framing is central to Williams' worldview. Traditional AppSec (SAST, DAST, WAF, scanners) all operate from outside the application. Instrumentation operates from within, where full context is available.

---

## Talk 6: "How to Build Awesome Security Instrumentation to Automate AppSec Testing and Protection"

**Conference:** Techstrong Con Virtual Summit
**Date:** September 2021
**Source:** https://techstrong.tv/videos/techstrong-con-virtual-summit/jeff-williams-how-to-build-awesome-security-instrumentation-to-automate-appsec-testing-and-protection-contrast-security

### Overview

Extended version of Williams' security instrumentation talk. Approaches application security from the "inside out" by showing how to create simple agents that operate inside a running application, providing comprehensive security observability.

### Key Demonstration Points

- Creating simple security agents that work like profilers or debuggers
- Getting inside a running application to access full context
- Providing security observability that external tools cannot achieve
- Automating both testing (IAST) and protection (RASP) from the same instrumentation layer

---

## Talk 7: "Practical DevSecOps Using Security Instrumentation"

**Conference/Event:** Eficode DevOps Event
**Posted:** September 2023
**Source:** https://www.eficode.com/devops-podcast/practical-devsecops-jeff-williams

### Core Problem Identified

The security landscape has not improved despite 25 years of effort. Web applications average 26.7 security vulnerabilities, and this metric has remained static for two decades. Williams argues that security code fails to reliably integrate into applications because security operates outside the development process.

### Main Framework: Three Ways of DevSecOps

**1. Establish Security Workflow**
Break security work into smaller, manageable pieces that create flow rather than massive deliverables. Security should not arrive as a 200-page PDF at the end of a sprint.

**2. Create Continuous Security Feedback**
Provide instant feedback to developers without excessive false alarms, eliminating the need for expert triage that slows processes. The feedback must be accurate enough that developers trust it and act on it immediately.

**3. Foster Security Culture**
Replace blame-based approaches with encouraging, forward-looking security that anticipates future threats rather than addressing outdated standards. Security should be something developers want to engage with, not fear.

### Key Analogy: The 94Fifty Instrumented Basketball

Williams uses the 94Fifty instrumented basketball (embedded with sensors) to explain how embedded sensors can democratize expertise. Rather than requiring expert coaches to observe and correct every shot, the tool provides direct feedback to the player. This allows individuals to self-improve while experts focus on strategic guidance — the same model should apply to application security.

### What Instrumentation Does in Software

- Adds agents to applications during code loading (no code changes required)
- Surgically inserts sensors into specific dangerous methods
- Gathers contextual telemetry for accurate vulnerability detection
- Works with existing test suites — normal testing becomes security testing

### Three Practical Applications Demonstrated

**1. Security Testing**
Detects non-parameterized SQL queries violating coding policies, preventing SQL injection vulnerabilities without requiring developers to understand security principles.

**2. Access Control Matrix Generation**
Automatically maps which roles access which application pages — a task that traditionally requires weeks of code analysis or extensive penetration testing. Identifies missing access controls and inconsistent encryption practices across application features.

**3. Vulnerability Prevention**
Blocks critical operations (like process execution) within request scopes, preventing command injection attacks at runtime rather than detecting them after exploitation.

### Outside-In vs. Inside-Out

| Dimension | Outside-In (Traditional) | Inside-Out (Instrumentation) |
|-----------|--------------------------|------------------------------|
| Where it runs | Separate from application | Inside running application |
| Context available | None or limited | Complete, assembled context |
| Expert triage needed | Yes — generates false positives | No — highly accurate |
| Pipeline impact | Days or weeks | Minutes or zero |
| Scales to production | No | Yes |

### Key Quotes

"Security hasn't had a reliable path into production," forcing counterproductive approaches that damage team culture.

"DevSecOps is about transforming security work the way development was transformed by DevOps," not merely shifting burden to developers.

### Key Position

The reason AppSec has not improved in 25 years is not a people problem or a culture problem — it is a tooling problem. The entire industry has invested in tools that operate outside the application, where full context is unavailable. Instrumentation solves this at the architectural level.

---

## Talk 8: "Lessons Learned from Securing Hundreds of Thousands of Real World APIs"

**Conference:** Gartner Security & Risk Management Summit 2023
**Date:** Tuesday, June 6, 2023 at 12:55 PM ET
**Location:** Theater 4 Prince George's Hall, Gaylord National Resort & Convention Center, National Harbor, Maryland
**Source:** https://www.contrastsecurity.com/press/contrast-security-co-founder-and-cto-to-present-on-how-to-secure-real-world-apis

### Abstract

Enterprises face major challenges identifying and protecting against vulnerabilities across code, libraries, frameworks, app servers, and runtimes used in API development. Rather than forcing developers to do more security work or relying solely on perimeter defenses, Williams presents a third approach: hardening software stacks to strategically prevent entire classes of common vulnerabilities.

### Key Ideas

**The API Security Challenge:** Per the referenced Gartner report, "API security challenges have emerged as a top concern for most software engineering leaders, as unmanaged and unsecured APIs create vulnerabilities that could accelerate multimillion dollar security incidents."

**Third Path:** Beyond "make developers do more security work" and "add more perimeter defenses" — embed security protection directly into production APIs.

**Lessons from Scale:** Williams draws on data from securing hundreds of thousands of real-world APIs to identify the most common vulnerability patterns and the most effective prevention strategies.

### Key Position

API security cannot be solved by perimeter tools (WAFs, API gateways alone) or by training developers to write more secure code. The solution is hardening the software stack itself so entire classes of vulnerabilities become structurally impossible.

---

## Podcast: "The Tech of Runtime Security" — Application Security Podcast

**Source:** https://appsec.buzzsprout.com/1730684/episodes/13558271

### Key Ideas & Frameworks

**The AppSec Backlog Crisis**
Traditional security tools generate massive backlogs. The example cited: 1.7 million unresolved issues in Veracode at one organization. These backlogs accumulate because SAST and DAST tools lack sufficient context, producing both false positives and false negatives, overwhelming limited AppSec teams.

**Runtime Security Two-Part Definition**
Runtime security encompasses:
1. Technical monitoring of executing code to detect vulnerabilities and attacks
2. A programmatic shift in how AppSec programs operate

This combination enables accurate, real-time, scalable security.

**IAST vs. Traditional Tools**
- IAST transforms existing test cases into security tests without changing development workflows
- Mean Time to Repair (MTTR) drops to approximately 3 days with IAST vs. 290+ days for static analysis
- IAST completes within build pipelines; DAST may require hours or days

**Trust Boundary Concept**
Both IAST and RASP wrap powerful methods with validation mechanisms. When untrusted data reaches sensitive operations — database calls, process execution, expression evaluation — without proper sanitization, the system flags potential exploits. This is the core detection model.

**Reachability vs. Actual Execution**
- Only 38% of library code actually executes in applications; 62% never loads
- Custom code comprises two-thirds of running applications — contrary to the "80% open source" statistic that dominates the narrative
- Runtime analysis reveals what actually runs rather than what theoretically could

### Notable Quotes

"If you use noisy tools, they're gonna generate a big pile of stuff that needs to be triaged, and nobody has the resources to do it."

"The only way to figure it out is to actually watch that code as it's running. Then everything's assembled, everything's in context."

"Companies that want to dominate in their sector are gonna be the ones that are best at both IT and security as part of that."

"Build runtime security into your stack...zero trust architecture at the application layer."

---

## Podcast: "Self-Protecting Software" — EnterpriseReady Podcast, Episode 15

**Source:** https://www.heavybit.com/library/podcasts/enterpriseready/ep-15-self-protecting-software-with-jeff-williams-of-contrast-security

### Key Frameworks & Ideas

**The Evolution of AppSec Approach**
Jeff advocates shifting from external scanning to embedded, instrumentation-based security. Traditional scanning tools lack sufficient information for accuracy, requiring expert involvement that doesn't scale.

**Two-Pronged Security Strategy**
1. Development phase: Tight feedback loops detecting vulnerabilities in real time
2. Production phase: Runtime protection against both known vulnerabilities and novel attacks

**The Vulnerability Crisis Metric**
Applications average 26.7 vulnerabilities upon release — a number that has not improved meaningfully over two decades. This backlog stems from late-stage detection rather than immediate developer feedback.

### Key Quotes

"There's just a lot of people out there that don't really get it right away, so I think the industry as a whole needs to continue to move forward and educate."

"AppSec is more like clay, you can build anything with software." (Explaining why AppSec differs fundamentally from network security — the attack surface is unlimited and application-specific.)

"Everything that's complicated in the world, we instrument it." (Advocating for application instrumentation as standard practice — planes, buildings, medical devices, financial systems are all instrumented. Software should be too.)

### Main Points

- **Standards Matter But Don't Drive Change**: OWASP Top 10 and similar frameworks raise awareness but haven't fundamentally transformed practices since 2002
- **Community Edition Strategy**: Free, full-featured products for single applications drive market awareness and adoption
- **Secure Coding Patterns Must Be Automated**: Guidelines alone fail; security should integrate into frameworks and CI/CD pipelines
- **Cost of Delay**: Vulnerability remediation costs spike exponentially beyond 30 minutes post-detection
- **Container/Kubernetes Limitations**: Deployment orchestration cannot detect application-layer vulnerabilities like SQL injection

---

## OWASP Distinguished Lifetime Member Award (YouTube)

**Platform:** YouTube (OWASP Foundation channel)
**Reference:** https://www.classcentral.com/course/youtube-owasp-distinguished-lifetime-member-jeff-williams-227109
**YouTube URL:** https://youtu.be/zzUvwRRv1lQ (referenced in search results)

### Overview

A 30-minute talk covering Jeff Williams' 20-year journey as one of the first OWASP Distinguished Lifetime Membership recipients. Topics covered:

- The creation of the OWASP Foundation non-profit (April 21, 2004)
- The origin story of the OWASP Top 10 (started as a side project, "went viral")
- Evolution of the OWASP Top 10 across versions
- Numerous flagship projects created under his leadership
- The demonstration of "security observability" using instrumentation
- Introduction to IAST and how it differs from traditional scanning
- How RASP prevents application exploitation in production

### Key Narrative: The OWASP Top 10 Origin

Williams wrote the OWASP Top 10 as a "little side project" — it went viral almost immediately. OWASP got slashdotted from the downloads, and the community asked him to take over as global chairman. This accidental viral success shaped the entire application security standards landscape.

---

## Contrast Security Blog — Key Article Topics (Jeff Williams authored)

**Source:** https://www.contrastsecurity.com/security-influencers/author/jeff-williams-co-founder-chief-technology-officer

### Articles on Core Themes

- "Contrast Security founder Jeff Williams explains how to fix AppSec in production" (August 2024)
- "3 ways Contrast helps to build digital resilience" / DORA compliance (October 2023)
- "Trust 'zero trust' for Application Security" (September 2023)
- "Legal liability for insecure software might work, but it's dangerous" (August 2023)

**API Security 4-Part Series (July–August 2022):**
- API inventory (July 27, 2022)
- API testing (August 3, 2022)
- API components (August 10, 2022)
- API protection (August 18, 2022)

**Earlier positions (2017):**
- "Improve Application Security by Turning it into Code" (May 2017)
- "Adding 'A7: Insufficient Attack Protection' to the OWASP Top 10" (April 2017)
- "A CTO's Response to Trump's Cybersecurity Executive Order" (May 2017)
- "How Code Vulnerabilities Can Lead to Bad Accidents" (July 2017)

---

## Core Intellectual Positions — Synthesized Across All Talks

### 1. The Opacity Problem
Traditional security tools analyze software from outside, where the application's inner workings are opaque. They see HTTP requests and code files, not the assembled, running application. This fundamental limitation produces false positives, false negatives, and expert dependency that doesn't scale.

### 2. Inside-Out Security
The solution is to operate from inside the running application — the same approach used by profilers, debuggers, and performance monitoring tools. This gives access to complete context: data flows, method calls, trust boundaries, and the actual execution path.

### 3. The 25-Year Stagnation
Despite two decades of investment in application security, the average application ships with ~26.7 vulnerabilities. Backlogs of millions of unresolved issues are common. This is not a people problem or culture problem — it is an architectural problem with the tooling approach itself.

### 4. The Three Ways Applied to Security
Williams applies the "Three Ways" of DevOps thinking to security:
- Flow (security work should flow, not pile up in gates)
- Feedback (security feedback should be instant, accurate, and developer-friendly)
- Continual Learning and Experimentation (security culture replaces blame culture)

### 5. Trust Boundaries as the Core Detection Model
The fundamental security check is: does untrusted data reach a sensitive operation (database query, system call, expression evaluator) without being properly validated or parameterized? IAST and RASP both enforce this boundary at runtime with full context.

### 6. Reachability Over Theoretical Attack Surface
Only 38% of library code actually executes. Runtime analysis shows what is actually reachable and running — a radically smaller, more accurate attack surface than what SAST or SCA tools analyze.

### 7. The Instrumentation Analogy
"Everything complicated in the world, we instrument it." Planes, bridges, buildings, medical devices, financial systems — all are instrumented for observability. Software is the critical exception. Williams argues this is the core unsolved problem in AppSec.

### 8. OWASP as Platform, Not Solution
Williams acknowledges that OWASP Top 10 and similar standards raise awareness but don't fundamentally change practices. Standards are necessary but not sufficient. The actual lever is tooling that makes secure behavior the path of least resistance.

### 9. API Security as the Next Frontier
As applications shift to API-first architectures, the vulnerability surface changes. Williams advocates hardening software stacks to structurally prevent entire classes of vulnerabilities — particularly injection attacks — rather than perimeter defense or developer training alone.

### 10. Legal Liability as a Coming Forcing Function
Williams notes (August 2023) that legal liability for insecure software "might work, but it's dangerous" — acknowledging both the appeal and the risks of regulatory pressure as a market forcing function.

---

## Conference Appearances Referenced (Partial List)

| Conference | Year | Topic Area |
|-----------|------|------------|
| O'Reilly Velocity | 2018 | DevSecOps Pipeline, IAST, RASP |
| QCon San Francisco | 2018 | Application Security Architecture |
| Cybersecurity Symposium (Charlotte) | Various | AppSec Instrumentation Keynote |
| SEAD 2020 | 2020 | Future of Software Security |
| Equal Experts Virtual | 2020 | Building Security Instrumentation |
| Techstrong Con | 2021 | Security Instrumentation Automation |
| YOW! London | 2022 | IAST and DevSecOps |
| Eficode DevOps | 2023 | Practical DevSecOps |
| Gartner Security & Risk Summit | 2023 | API Security at Scale |
| JavaOne | Multiple | Java Rockstar speaker |
| BlackHat | Multiple | Application Security |
| RSA Conference | Multiple | Application Security |
| OWASP AppSec | Multiple | OWASP projects and standards |
| PivotalOne | Multiple | Cloud-native security |

---

*Sources collected:*
- *[RSA Conference profile](https://www.rsaconference.com/experts/jeff-williams)*
- *[O'Reilly Velocity 2018](https://conferences.oreilly.com/velocity/vl-ca-2018/public/schedule/detail/69802.html)*
- *[Cybersecurity Symposium Keynote](https://cybersecuritysymposium.charlotte.edu/speaker/jeff-williams-keynote/)*
- *[YOW! London 2022](https://yowlondon.com/2022/speakers/2492/jeff-williams)*
- *[SEAD 2020 Keynotes](https://sites.google.com/view/sead2020/keynotes)*
- *[Eficode — Practical DevSecOps](https://www.eficode.com/devops-podcast/practical-devsecops-jeff-williams)*
- *[Equal Experts — Security Instrumentation](https://www.equalexperts.com/blog/events/how-to-build-security-instrumentation-to-automate-appsec-testing-and-protection-with-jeff-williams/)*
- *[Techstrong TV — Security Instrumentation](https://techstrong.tv/videos/techstrong-con-virtual-summit/jeff-williams-how-to-build-awesome-security-instrumentation-to-automate-appsec-testing-and-protection-contrast-security)*
- *[Application Security Podcast — Runtime Security](https://appsec.buzzsprout.com/1730684/episodes/13558271)*
- *[EnterpriseReady Podcast — Self-Protecting Software](https://www.heavybit.com/library/podcasts/enterpriseready/ep-15-self-protecting-software-with-jeff-williams-of-contrast-security)*
- *[Gartner Summit — API Security](https://www.contrastsecurity.com/press/contrast-security-co-founder-and-cto-to-present-on-how-to-secure-real-world-apis)*
- *[Contrast Security Blog](https://www.contrastsecurity.com/security-influencers/author/jeff-williams-co-founder-chief-technology-officer)*
- *[OWASP 20th Anniversary](https://owasp.org/blog/2024/04/21/owasp-foundation-20th-anniversary)*
- *[OWASP Lifetime Member YouTube (Class Central)](https://www.classcentral.com/course/youtube-owasp-distinguished-lifetime-member-jeff-williams-227109)*
- *[Infosecurity Magazine Profile](https://www.infosecurity-magazine.com/profile/jeff-williams-1/)*

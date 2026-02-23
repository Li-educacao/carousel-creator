# Jeff Williams — Collected Articles: Dark Reading, Security Magazine & Other Sources

**Collection date:** 2026-02-19
**Subject:** Jeff Williams, Co-Founder & CTO, Contrast Security; Former Global Chairman, OWASP Foundation
**Purpose:** Cognitive cloning — capturing Jeff Williams' thinking, opinions, and frameworks
**Sources:** Dark Reading, Security Magazine, Contrast Security Blog, LinkedIn Pulse, DevOps.com

---

## Biography Note

Jeff Williams is a pioneer in application security with over 25 years of experience. He is co-founder and CTO of Contrast Security. He served as Global Chairman of the OWASP Foundation for eight years, creating the OWASP Top 10, OWASP Enterprise Security API (ESAPI), OWASP Application Security Verification Standard (ASVS), the XSS Prevention Cheat Sheet, and many other widely adopted standards. He holds a BA from the University of Virginia, an MA from George Mason University, and a JD from Georgetown University Law Center.

---

## SECTION 1: DARK READING ARTICLES

### Article 1
**Title:** Legal Liability for Insecure Software Might Work, but It's Dangerous
**Source:** Dark Reading
**Date:** August 28, 2023
**URL:** https://www.darkreading.com/vulnerabilities-threats/legal-liability-for-insecure-software-might-work-but-it-s-dangerous

**Summary / Key Arguments:**

Jeff Williams argues that while imposing legal liability on software companies for insecure code might sound appealing, the approach carries dangerous unintended consequences. His core position: a liability regime goes too far and may cause more harm than good.

**Downsides of liability he identifies:**
- Increased costs for software companies across the board
- Potential for protracted legal battles that drain resources from actual security work
- Disincentives to innovation, particularly harmful to smaller companies
- Could burden smaller companies disproportionately and stifle diversity in the software industry
- Companies may spend more on legal defense than on actual security improvements

**His preferred alternative:** Mandatory transparency. Williams advocates for an approach that "mandates visibility and transparency" as "the least intrusive way of achieving the goals." He argues organizations should "put incentives in place for companies to do the right thing to build security programs" so consumers can choose providers that do software the right way.

**Core contrarian point:** Rather than punishing companies after breaches through liability, the market should be empowered with information to reward companies that invest in security upfront. Transparency creates market pressure without the destructive side effects of legal liability.

---

### Article 2
**Title:** The Staggering Complexity of Application Security
**Source:** Dark Reading
**URL:** https://www.darkreading.com/application-security/the-staggering-complexity-of-application-security

**Summary / Key Arguments:**

Williams argues that "during the past few decades of high-speed coding we have automated our businesses so fast that we are now incapable of securing what we have built."

**Scale data he presents:**
- A typical midsized financial organization has a portfolio of over 1,000 applications; the largest firms exceed 10,000
- Each application averages hundreds of thousands of lines of custom code; the largest contain over 10 million lines
- Each application includes anywhere from dozens to hundreds of software libraries, frameworks, and components that typically total over 10x the size of the custom code
- The typical enterprise web application has 22.4 serious vulnerabilities (per Aspect Security research)

**His argument:** Recent advances in software development—widespread use of libraries and components, high-speed development methodologies, complex frameworks, and inscrutable protocols—have made manual analysis too slow for all but the most critical applications. New technologies and techniques are required to manage security vulnerabilities at scale.

---

### Article 3
**Title:** What's Your AppSec Personality?
**Source:** Dark Reading
**Date:** June 29, 2022
**URL:** https://www.darkreading.com/cyber-risk/what-s-your-appsec-personality-

**Summary / Key Arguments:**

Williams presents a framework for understanding what role a security professional plays in their organization. He identifies three AppSec personality types:

1. **The Auditor** — focuses on finding and documenting vulnerabilities, compliance-oriented
2. **The Lawyer** — focused on policy, governance, contracts, and legal requirements
3. **The Developer** — focused on building security into the software development process

**His framework:** An effective AppSec program needs to deliver:
- Secure code that is vulnerability-free and well-defended
- A secure software supply chain
- Secure operations to detect attacks and prevent exploits in production

**Core argument:** Each personality type emphasizes only part of what's needed. Organizations must recognize which "personality" dominates their program and consciously develop capabilities in the other dimensions.

---

### Article 4
**Title:** Flying Naked: Why Most Web Apps Leave You Defenseless
**Source:** Dark Reading
**Date:** March 2014
**URL:** https://www.darkreading.com/application-security/flying-naked-why-most-web-apps-leave-you-defenseless-/d/d-id/1127875

**Summary / Key Arguments:**

Williams' central argument: 90% of applications in most organizations are "naked" — they have no application security defenses in place.

**His data:**
- Even the best-funded, most "mature" security programs are only really testing 10% of their applications, leaving 90% with no real security
- The 10% of applications that are tested average 22.4 serious vulnerabilities per application
- 54% of breaches come from custom application code

**His analogy:** He compares this to a major airline that only checks 10% of its fleet for safety problems and finds 22 safety problems per aircraft checked. No rational person would accept those odds in aviation — yet organizations routinely accept them in software.

**Core message:** The term "application security" is often used to describe a program that leaves nearly all applications completely unsecured. This is not a program at all — it is theater.

---

### Article 5
**Title:** Why Your Application Security Program May Backfire
**Source:** Dark Reading
**Date:** July 2, 2014
**URL:** https://darkreading.com/operations/why-your-application-security-program-may-backfire/a/d-id/1278972

**Summary / Key Arguments:**

Williams warns that many AppSec programs are actually counterproductive. Programs built on the wrong foundations create security theater while providing false confidence.

**Key problems he identifies:**
- Annual or triannual security testing creates large gaps during which vulnerabilities are introduced and exploited
- Programs focused on compliance checklists rather than actual vulnerability elimination
- Testing methodologies that generate so many false positives that real issues are buried
- Programs that rely on external security specialists rather than embedding security into development processes

---

### Article 6
**Title:** Which Apps Should You Secure First? Wrong Question.
**Source:** Dark Reading
**Date:** March 2015
**URL:** https://www.darkreading.com/application-security/which-apps-should-you-secure-first-wrong-question-

**Summary / Key Arguments:**

Williams argues that the question "which apps should we secure first?" is fundamentally the wrong framing. The question reveals a broken mental model about application security.

**Terrible tactics he identifies:**

1. **Securing only externally facing apps** — Most enterprises have hundreds or thousands of applications written over the past 10-20 years. Whether an application is exposed to the Internet is only one of many risk factors. Focusing solely on external apps wastes resources on deep security reviews of applications that may not be that risky to the business, while ignoring internal apps that contain critical data.

2. **Tackling one application at a time** — This cannot scale. Spending deep resources on trivial vulnerabilities in one application while others go completely unreviewed is not a security program.

3. **Annual security testing schedules** — Extremely risky given the pace of new vulnerabilities and attack techniques. This approach guarantees a window of exposure between tests.

**His reframe:** The right question is "how do we secure our entire application portfolio?" — which requires a different approach entirely: continuous, automated, portfolio-wide security.

---

### Article 7
**Title:** An AppSec Report Card: Developers Barely Passing
**Source:** Dark Reading
**Date:** September 19, 2014
**URL:** https://www.darkreading.com/application-security/an-appsec-report-card-developers-barely-passing

**Summary / Key Arguments:**

Based on a year-long study of 1,425 developers from 695 organizations worldwide examining what developers know and don't know about security.

**Key findings:**
- Average developer security knowledge score: a barely passing 60.77%
- Protecting sensitive data: 80% of developers answered questions on this topic incorrectly
- Introduction to web services security: 64% of developers answered incorrectly
- The study covered 65 different areas of application security knowledge

**Williams' argument:** Developers are not getting the application security training they need, by design. Security knowledge cannot be assumed. Organizations must invest in measuring and improving what developers actually know, not just providing training programs that look good on paper.

---

### Article 8
**Title:** Why It's Insane to Trust Static Analysis
**Source:** Dark Reading
**Date:** September 22, 2015
**URL:** https://www.darkreading.com/vulnerabilities-threats/why-it-s-insane-to-trust-static-analysis

**Summary / Key Arguments:**

Williams uses results from the OWASP Benchmark Project (sponsored by DHS, with over 21,000 test cases) to mount a critique of static analysis (SAST) as a primary application security strategy.

**His arguments against over-reliance on SAST:**
1. **Accuracy problems** — SAST tools produce both false positives and false negatives. The OWASP Benchmark measures both, calculating an overall score. Many popular SAST tools perform poorly on this benchmark.
2. **Performance disruption** — Static tools take hours or days to analyze a single application. They require experts, RAM, and CPU, and are difficult to parallelize, making them "massively disruptive to software development processes."
3. **Coverage gaps** — Static analysis cannot trace complex execution flows through modern API patterns, reflection, dependency injection, and dynamic loading.

**His alternative:** Runtime analysis is superior for injection flaws because it can track real data through the running application. Different vulnerability types require different testing approaches — static analysis is good for some patterns (single-line code flaws) but inadequate for the systemic vulnerabilities that cause most breaches.

**Core contrarian position:** The industry's default assumption that SAST is the foundation of AppSec is wrong. Trusting static analysis to secure production applications is, as the title states, insane.

---

### Article 9
**Title:** The Common Core of Application Security
**Source:** Dark Reading
**URL:** https://www.darkreading.com/vulnerabilities-threats/the-common-core-of-application-security

**Summary / Key Arguments:**

This article is a debate between Jeff Williams and Jason Schmitt of HP Fortify on the best approach to application security. Williams advocates for a proactive, systemic, and disciplined approach to changing how software is developed and purchased — arguing that the common core of AppSec should be built around instrumenting running applications rather than analyzing source code in isolation.

---

---

## SECTION 2: SECURITY MAGAZINE ARTICLES

### Article 10
**Title:** New NIST Standards on IAST and RASP Deliver State-of-the-Art AppSec
**Source:** Security Magazine
**Date:** June 19, 2020
**URL:** https://www.securitymagazine.com/articles/92648-new-nist-standards-on-iast-and-rasp-deliver-state-of-the-art-appsec

**Summary / Key Arguments:**

Williams explains and contextualizes the release of NIST SP 800-53 Revision 5, which includes two new standards specifically addressing Interactive Application Security Testing (IAST) and Runtime Application Self-Protection (RASP).

**Key points:**
- The critical enabler of both IAST and RASP standards is security instrumentation — AppSec telemetry generated by microsensors embedded within the software
- Security instrumentation enables a comprehensive approach to AppSec that starts in development and extends into production runtime
- This approach eliminates development delays connected to security scans and false positives
- Reduces risk by enabling teams to quickly address vulnerabilities

**Williams' argument:** NIST's endorsement of IAST and RASP validates the instrumentation-based approach to security that he has advocated for years. The traditional SAST/DAST model is not reflected in the new standards because it cannot provide the continuous, accurate, runtime-aware security that modern applications require.

---

### Article 11
**Title:** How to Build More Secure APIs
**Source:** Security Magazine
**Date:** October 3, 2022
**URL:** https://www.securitymagazine.com/articles/98429-how-to-build-more-secure-apis

**Summary / Key Arguments:**

Williams argues that APIs have become the primary attack surface for modern applications and that existing security tools are fundamentally ill-equipped to address this.

**The problem he describes:**
- APIs function as the connective tissue between applications and are just as hackable as web apps
- Major data breaches enabled by unsecured APIs include LinkedIn's 2021 breach and Parler's 2021 data exposure
- Modern web applications are conglomerations of interconnected APIs, microservices, and frameworks spread across multiple environments
- Data access has moved to APIs — exposed not just across the enterprise but publicly to users and partners

**Why traditional tools fail:**
- API attacks are difficult to detect with WAFs
- SAST and DAST tools were designed for web applications from the early 2000s and haven't advanced much since then
- These tools lack visibility into what they're actually scanning inside API code

**His solution framework:** Runtime security instrumentation embedded in the application — the only approach that can observe actual API behavior, trace data flows through the application, and identify vulnerabilities in production.

---

---

## SECTION 3: CONTRAST SECURITY BLOG (OPINION & FRAMEWORK ARTICLES)

### Article 12
**Title:** How ADR Fixes AppSec in Production
**Source:** Contrast Security Blog
**Date:** August 13, 2024
**URL:** https://www.contrastsecurity.com/security-influencers/contrast-security-founder-jeff-williams-explains-how-to-fix-appsec-in-production-adr

**Full Content:**

Contrast Security founder Jeff Williams discusses how Application Detection and Response (ADR) addresses critical gaps in application security during a Black Hat interview with Alan Shimel and Katie Norton from IDC.

**AppSec isn't working in production**

Williams and his guests agreed that current DevSecOps and AppSec approaches fail in production environments. These methodologies primarily generate vulnerability backlogs in development rather than providing actual protection. According to Ponemon research cited in the article, "the average organization has a backlog of 1.1 million vulnerabilities."

Organizations lack visibility into attacks and exploitation prevention capabilities. The paradox is that DevSecOps, intended to bridge development and operations divides, has instead created new silos. Developers are pressured to function as security professionals, while security experts cannot realistically become developers. This misalignment prevents unified incident response.

**Filling the gaps with ADR**

Similar to endpoint detection and response (EDR) and cloud detection and response (CDR) solutions, ADR operates on application and API servers to detect incidents, report to operations teams, and prevent exploits. The technology integrates with existing XDR, SIEM, and CNAPP ecosystems for comprehensive threat visibility.

**ADR brings Development and Operations together with context**

A critical observation: "context" is needed for interpreting vulnerabilities and attacks. A significant disconnect exists between developer perspectives and security operations center (SOC) activities. ADR bridges this gap by providing production security context to both teams, enabling informed vulnerability prioritization and threat assessment.

**API security is just AppSec**

APIs represent application software requiring identical testing, detection, and response mechanisms. Treating API security separately creates unnecessary tool proliferation. While WAFs provide API traffic telemetry, they lack insight into underlying API code — a limitation ADR addresses.

**Translating to make DevSecOps work**

ADR functions as a translator between operational and development languages. Operations teams discuss SIEM events and SOAR playbooks, while developers focus on vulnerabilities and remediation. ADR enables communication by providing relevant data regardless of role.

**Core conclusion:** ADR addresses recognized gaps in visibility, silos, and attack detection by providing production attack data and enriched alerts to SOC teams and stakeholders.

---

### Article 13
**Title:** Smarter AppSec: How ADR, Secure by Design and 'Shift Smart' Are Redefining Cybersecurity
**Source:** Contrast Security Blog / Application Security Podcast Takeaways
**Date:** November 2024
**URL:** https://www.contrastsecurity.com/security-influencers/smarter-appsec-how-adr-secure-by-design-and-shift-smart-are-redefining-cybersecurity-application-security-podcast-takeaways-contrast-security

**Summary / Key Arguments:**

**Shift Smart vs. Shift Left:**
Williams offers a direct critique of the "shift left" paradigm that has dominated security discourse. Key argument: "zero trust" and "DevSecOps" are examples of once-useful terms rendered virtually worthless through overuse and distortion, with "shift left" being another great example.

Rather than blindly shifting left, organizations should deploy a "Shift Smart" strategy — choosing the timing and approach for security testing to maximize context, speed, accuracy, and cost-effectiveness.

**ADR Technology:**
Unlike traditional web application firewalls, ADR operates from within the application, enabling it to detect attacks more precisely and reduce false positives. It's not just detecting suspicious inputs — it's detecting the root cause of application and API attacks, such as recognizing anomalous behavior when untrusted data alters query logic in SQL injection attacks.

**Secure by Design:**
Williams emphasizes that security architecture decisions made early in design have outsized impact on vulnerability rates downstream. Security cannot be bolted on after the fact.

**Core argument:** The security industry has created a generation of practitioners who follow fashionable frameworks (shift left, zero trust, DevSecOps) without understanding whether those frameworks actually reduce risk. The question should always be: does this approach actually find and prevent vulnerabilities in production?

---

### Article 14
**Title:** Shift Smart Instead of Following Shift-Left Fairy Tales
**Source:** Contrast Security Blog
**Date:** 2023
**URL:** https://www.contrastsecurity.com/security-influencers/shift-smart-instead-of-following-shift-left-fairy-tales-application-security-appsec-contrast-security

**Summary / Key Arguments:**

Williams directly attacks the mythology around "shift left" — the dominant DevSecOps doctrine that security should be moved as early as possible in the SDLC.

**The fairy tale he debunks:** The oft-cited statistic that fixing vulnerabilities earlier in the SDLC is "100 times less expensive" than fixing them in production. Williams argues this figure is unsupported and that later studies found the cost to fix bugs is roughly the same regardless of when they are fixed.

**His "Shift Smart" framework:**
- Shift left is a reasonable idea but should not be followed blindly
- Shifting too far left wastes time and risks missing security vulnerabilities that cannot be effectively tested until later in the SDLC
- The right approach: choose the right security test for each rule and apply it at the point in the SDLC where it is most cost-effective
- Some security rules are best caught in design, some in code, some in testing, and some only in production

**Core position:** "Shift Smart" is about doing security when it makes the most sense, which might not be exactly the same for every kind of security test. The "shift left everything" approach is a fairy tale that has led organizations to invest in early-stage tools while remaining blind in production.

---

### Article 15
**Title:** Trust 'Zero Trust' for Application Security
**Source:** Contrast Security Blog
**Date:** September 7, 2023
**URL:** https://www.contrastsecurity.com/security-influencers/zero-trust-table-of-how-contrast-maps

**Full Content:**

**The Problem with Perimeter Security**
Traditional perimeter-based cybersecurity has become obsolete in modern enterprises. Modern infrastructure — distributed across clouds, APIs, microservices, and SaaS platforms — cannot be protected by conventional boundary defenses. Williams uses an analogy comparing outdated city walls to outdated network perimeters: both fail when threats and infrastructure evolve beyond their original scope.

**Why Zero Trust Matters**
"Data is the goal of hackers today." Zero trust represents a fundamental shift from perimeter defense to a model where "everything is assumed to be accessible via the public internet" and access must be continuously verified rather than assumed.

**CISA's Framework**
The U.S. Cybersecurity and Infrastructure Security Agency identifies five zero-trust pillars: identity, devices, network, applications, and data. Contrast Security focuses on pillar 4 — applications.

**Implementation Strategy**
Williams references the "explode, offload, reload" methodology and Gerald Caron's incremental approach: begin with minor adjustments rather than complete overhauls, implement pilot projects, and standardize lessons learned gradually.

**Application Security's Role**
Contrast Security supports zero trust through: threat protection for known and unknown vulnerabilities, CI/CD pipeline integration, continuous application security testing, and comprehensive analytics and policy enforcement across application portfolios.

---

### Article 16
**Title:** Why We Need "Developer-First" Application Security
**Source:** Contrast Security Blog
**Date:** October 5, 2021
**URL:** https://www.contrastsecurity.com/security-influencers/why-we-need-developer-first-application-security

**Full Content:**

Modern software development demands rapid delivery cycles, yet traditional application security testing (AST) tools create bottlenecks. Williams argues that security must be redesigned around developer needs rather than forcing developers into separate security workflows.

**The Core Problem**
Current AST tools require security experts to triage results before developers receive recommendations. This fragmented approach causes delays: "79% report that developers are under increasing pressure to shorten release cycles," yet legacy security tools weren't built for modern development speeds. "Developers are often forced to choose meeting release deadlines over performing security scans."

**Three Essential Capabilities**

1. **Speed:** Developers need rapid feedback with contextual information about vulnerabilities — including affected code lines, user inputs, and library usage. This enables "just-in-time" training without requiring security specialist involvement.

2. **Accuracy:** False positives create significant overhead. When "reports with as many as 85% false positives" occur, development teams waste substantial time on non-issues, slowing delivery.

3. **Scalability:** Effective security requires continuous testing across all applications. However, "the average scan takes at least three hours per application" for most organizations, making daily comprehensive scans impractical with current tools.

**The Solution**
Williams advocates for instrumentation-based security integrated into CI/CD pipelines — tools designed "by developers, for developers" that eliminate separate security silos.

---

### Article 17
**Title:** The Forthcoming 2021 OWASP Top Ten Shows That Threat Modeling Is No Longer Optional
**Source:** Contrast Security Blog
**Date:** September 8, 2021
**URL:** https://www.contrastsecurity.com/security-influencers/the-forthcoming-2021-owasp-top-ten-shows-that-threat-modeling-is-no-longer-optional

**Full Content:**

OWASP published its first Top Ten in 2003, establishing a framework for organizations to prioritize application security efforts. The 2021 update required significant revision.

**Research basis:** OWASP analyzed more than 500,000 applications using telemetry from 13 security vendors, including Contrast Security. The cross-industry survey found that "80% of respondents reported that at least half of alerts generated by their scanning tools are false positives" — potentially inflating vulnerability counts.

**Key changes to existing categories:**
- Injection vulnerabilities now include Cross-Site Scripting (XSS), consolidated under one category
- Identification and Authentication Failures expanded from the previous Broken Authentication category
- Vulnerable and Outdated Components replaced "Using Components with Known Vulnerabilities"
- Security Misconfiguration absorbed XML External Entities (XXE) vulnerabilities

**Three new categories:**

1. **Insecure Design (position 4):** Encourages threat modeling and secure design practices early in development. A significant shift leftward from traditional security-late approaches.

2. **Software and Data Integrity Failures (position 8):** Addresses compromised supply chains, exemplified by the SolarWinds breach.

3. **Server-Side Request Forgery / SSRF (position 10):** Addresses vulnerabilities where applications fetch remote resources without validating user-supplied URLs.

**Critical observation on data accuracy:** Only 6% of typical application code consists of active library code, while 74% remains inactive. "Outdated libraries only pose risk if they are both active and vulnerable," yet vulnerability scanning often flags all deprecated components regardless of actual usage.

**Core conclusion:** "Application threat modeling is no longer an option." OWASP, NIST, and the Payment Card Institute have all incorporated threat modeling into their standards. The White House executive order on cybersecurity further mandates it for companies doing federal business.

---

### Article 18
**Title:** The 4 Dimensions of a Sound Application Security Strategy
**Source:** Contrast Security Blog
**Date:** August 17, 2016
**URL:** https://www.contrastsecurity.com/security-influencers/the-4-dimensions-of-application-security-strategy

**Full Content:**

Williams argues that understanding coverage across multiple dimensions is essential for CISOs and application security managers. Most programs address only one or two dimensions and call it done.

**Dimension 1: Portfolio Coverage**
Which applications are actually verified? Many companies only scan "critical" applications despite evidence that major breaches often start through lesser-used systems. He recommends comprehensive application inventories including: web applications, web services/APIs/microservices, desktop/mobile/client applications, third-party applications, legacy systems, cloud applications, and all environments from development through production.

**Dimension 2: Security Coverage**
Verifying that security defenses are properly implemented. Requires both breadth (all necessary controls exist) and accuracy in detection. Williams emphasizes that false negatives (missed vulnerabilities) pose greater danger than false positives — they create dangerous false security.

**Dimension 3: Code Coverage**
Analyzing only source code misses critical paths. Modern applications use reflection, dependency injection, and dynamic loading. Dynamic scanners typically achieve only 20-25% code coverage. He recommends direct application instrumentation as "the most effective way to achieve code coverage."

**Dimension 4: Continuous Coverage**
The hidden fourth dimension — time. Single annual security reviews are insufficient in persistent threat environments. He advocates continuous verification through instrumentation that works automatically during developer testing, unit tests, and QA activities, delivering alerts "instantly after vulnerabilities are introduced."

---

### Article 19
**Title:** Thoughts on Modern Security Practices and Security Frameworks
**Source:** Contrast Security Blog
**Date:** August 25, 2017
**URL:** https://www.contrastsecurity.com/security-influencers/thoughts-on-modern-security-practices-and-security-frameworks

**Full Content:**

**How Modern Assets Have Affected Security Programs**

"There is no perimeter, and there are no 'internal' applications. Application security isn't optional, it's the leading cause of breaches."

The proliferation of modern development tools — libraries, frameworks, APIs, containers, and CI/CD pipelines — has rendered traditional application security approaches obsolete. Organizations should "continuously inventory, assess, and protect every application and API in their portfolio."

**Business and Security Benefits of Security Frameworks**

Williams characterizes cybersecurity as "insanely complicated," noting that typical house or car analogies underestimate the challenge. A more accurate comparison involves "securing an entire city" with its multiple systems and safeguards.

Adopting cybersecurity frameworks provides benefits: identifying security gaps, supporting budget planning, gaining executive alignment.

**His critical distinction:** "Adopting a framework doesn't secure anything — it just helps you get organized."

This is a sharp point against organizations that confuse compliance with a framework with actual security. The framework is a map, not the territory.

---

### Article 20
**Title:** A CTO's Response to Trump's Cybersecurity Executive Order
**Source:** Contrast Security Blog
**Date:** May 12, 2017
**URL:** https://www.contrastsecurity.com/security-influencers/a-ctos-response-to-trumps-cybersecurity-executive-order

**Full Content:**

**On Agency Accountability:**
While holding agency heads responsible for cybersecurity seems logical, agencies were already accountable. Williams points out that previous breaches at OPM and the IRS led to leadership changes. But "simply forcing agency heads to resign without providing funds and support" sets them up for failure without addressing underlying resource constraints.

**On Cloud Services Preference:**
Encouraging that the order specifically mentions preference for shared IT services, including cloud-based cybersecurity solutions — a significant shift from government's previous reluctance regarding cloud adoption.

**Core Challenge — The "Security Debt":**
Federal agencies "cannot feasibly achieve both modernization while also increasing their cybersecurity posture with limited resources." Most agencies perform poorly on GAO cybersecurity scorecards due to decades of accumulated technical debt from e-government initiatives.

**Application Security Gap:**
Federal agencies lag significantly behind the private sector in application security — "at least a decade behind the financial industry." Attributed to outsourced development and ineffective certification processes that fail to ensure security requirements are communicated from project inception.

**Primary Recommendation:**
The federal government should require agencies and contractors to "disclose exactly how they are building applications and securing systems" — including transparency about team training, development processes, component integration, and security tools used. This is inexpensive and high-potential-impact.

---

### Article 21
**Title:** Adding "A7: Insufficient Attack Protection" to the OWASP Top 10
**Source:** Contrast Security Blog
**Date:** April 27, 2017
**URL:** https://www.contrastsecurity.com/security-influencers/the-importance-of-adding-a7-insufficient-attack-protection-to-the-owasp-top-10

**Full Content:**

Williams addresses controversy surrounding the proposed addition of "A7: Insufficient Attack Protection" to the OWASP Top 10 list.

**His defense of the addition:**
- The OWASP Top Ten has historically introduced forward-thinking items. In 2007, CSRF was added; in 2013, the focus turned to libraries with known vulnerabilities.
- "Applications should detect when they are under attack and have the capability to do something about it" — representing a shift toward operational security concerns.
- Both vulnerability prevention and attack defense matter: "it takes both belt and suspenders."
- 20+ vendors across various sizes are developing RASP solutions, suggesting genuine market demand for attack protection capabilities.

**His philosophy:** Combining secure development practices with runtime defense mechanisms, particularly relevant in DevOps environments. The idea that security should only be about preventing vulnerabilities from being introduced is incomplete — organizations also need detection and response at runtime.

---

### Article 22
**Title:** Automating Application Security in Modern Software Projects
**Source:** Contrast Security Blog
**Date:** January 19, 2017
**URL:** https://www.contrastsecurity.com/security-influencers/automating-application-security-in-modern-software-projects

**Full Content:**

"Today, it seems like every organization has become a software company. The increasing dependence on automation demands that software survive and thrive despite an increasingly hostile environment."

"Insecure code has become the leading security risk and, increasingly, the leading business risk as well. It's irresponsible at every level to ignore this risk while doubling down on anti-virus solutions and firewalls — neither of which protects applications."

**The central challenge:** enabling development pipelines to reliably produce secure software without creating roadblocks or slowdowns. "If security slows down innovation, it will be bypassed."

**Five best practices for automating AppSec:**

1. **Choose Tools Strategically** — Emphasize "speed, ease-of-use, accuracy, and scalability." Instant feedback and usability for non-security personnel are critical.

2. **Integrate Security Into Pipelines** — Look for tools that deliver results directly into existing platforms like Slack, JIRA, Maven, Jenkins, SIEM, and PagerDuty.

3. **Detect Vulnerabilities** — Legacy SAST and DAST scanners are difficult to automate and generate false alarms. IAST tools using instrumentation technology offer superior assessment capabilities.

4. **Protect Against Attacks** — RASP provides flexible deployment and impressive accuracy, surpassing legacy web application firewalls (WAF).

5. **Leverage Threat Intelligence** — Mature security architectures automatically enforce chosen security patterns, verifying that applications have proper defenses implemented correctly throughout.

---

### Article 23
**Title:** Is There a 3rd Category of Application Security Tools Beyond Static & Dynamic?
**Source:** Contrast Security Blog
**Date:** October 20, 2016
**URL:** https://www.contrastsecurity.com/security-influencers/is-there-a-3rd-category-of-application-security-tools-beyond-static-dynamic

**Full Content:**

Williams addresses the question of whether the static/dynamic binary captures all of application security testing.

**His argument:** The terms SAST and DAST are misleading and incomplete. DAST means scanning an application with HTTP requests to reveal vulnerabilities based on HTTP responses. SAST means analyzing application code. These two techniques "don't nearly cover the possible universe of ways to analyze an application's security."

**His alternative classification:** Rather than thinking in terms of static versus dynamic analysis, organize security tools based on "what information you have available to make decisions." IAST represents a distinct third methodology — not just dynamic analysis but instrumented analysis that provides inside-out visibility into application behavior.

**Core argument:** The binary static/dynamic framework is insufficient for properly understanding modern application security tools. The industry's use of this framework has caused organizations to miss an entire category of security technology that provides superior accuracy, coverage, and integration with development workflows.

---

### Article 24
**Title:** The True Cost of "False Positives" in Application Security
**Source:** Contrast Security Blog
**Date:** July 19, 2016
**URL:** https://www.contrastsecurity.com/security-influencers/the-true-cost-of-false-positive-vulnerabilities-in-application-security

**Full Content:**

Williams examines how false positives in application security tools undermine security programs by consuming resources needed to investigate alerts.

**The "boy who cried wolf" problem:** False alarms force security teams to investigate every reported vulnerability regardless of legitimacy. "Figuring out if a tool-reported vulnerability is true or not can take anywhere from ten minutes to many hours."

**Resource constraint math:** If a scanner reports 400 potential vulnerabilities but only 40 are genuine, and teams can investigate only 25% of alerts, they will miss 75% of actual vulnerabilities — while expending enormous effort on the 360 false positives.

**The false negative danger:** Beyond false positives, undetected vulnerabilities pose greater risk. Teams gain false confidence from scan reports while remaining unaware of serious security gaps.

**Measurement recommendation:** Use the OWASP Benchmark — "a collection of thousands of test cases designed to measure whether your application security tools have certain basic capabilities" — to objectively evaluate tool accuracy.

**Core argument:** Effective application security scaling demands high-accuracy automation rather than tools requiring extensive human triage. The industry has dramatically underweighted the cost of false positives when evaluating and purchasing security tools.

---

### Article 25
**Title:** With Only a Hammer, Everything Looks Like a Security Vulnerability!
**Source:** Contrast Security Blog
**Date:** July 28, 2016
**URL:** https://www.contrastsecurity.com/security-influencers/when-all-you-have-is-a-hammer-everything-looks-like-a-security-vulnerability

**Full Content:**

**Core insight:** Most security vulnerabilities stem from failing to implement appropriate security controls, not from malicious code or mysterious exploits.

**Root cause breakdown (from research across thousands of applications):**
- 55% of vulnerabilities in custom applications happen when the security control isn't used
- In 35% of cases, the control doesn't exist at all
- In 20%, developers simply fail to invoke it
- The remaining vulnerabilities result from improperly functioning or incorrectly applied controls

**The detection problem:** Traditional security analysis tools struggle because they cannot identify custom security controls. Without understanding these controls, SAST and DAST scanners generate false positives — "everything looks like a vulnerability" when controls remain invisible to them.

**Most applications contain dozens or hundreds of custom security control implementations across their code, libraries, and frameworks.** Creating custom rules to address this complexity proves prohibitively difficult.

**The solution Williams announces:** Automatic discovery of custom security controls through runtime analysis — enabling the tool to identify security controls and tag data flowing through them, dramatically improving vulnerability detection accuracy.

---

### Article 26
**Title:** Security Predictions for 2018
**Source:** Contrast Security Blog
**Date:** December 18, 2017
**URL:** https://www.contrastsecurity.com/security-influencers/jeff-williams-contrast-cto-security-predictions-for-2018

**Full Content:**

Williams' six predictions for 2018, drawing on data across tens of thousands of applications:

1. **Attacks after vulnerability disclosure will happen faster than ever.** While attacks once took weeks or months to emerge, it's been reduced to about a day. That "safe window" will get even smaller, giving organizations only a few hours to respond. Equifax was an early example of this trend.

2. **Federal breach legislation will be enacted, forcing quick disclosure.** Outrage over delayed announcements at Uber and Stanford GSB will drive new regulation. Breach disclosure has never been a strong motivation for companies to invest in security.

3. **Election security will be discussed, with no significant action.** Despite strong evidence of U.S. election interference, it is an extremely complex and political problem that will take years to address.

4. **Attempts to undermine encryption by law enforcement will fail.** Companies will continue to resist FBI lobbying to weaken encryption to protect customer privacy.

5. **Organizations will aggressively embrace cloud and DevSecOps.** Since the threat is now continuous, companies need continuous security alongside continuous integration and continuous delivery. Organizations will prioritize instrumenting their entire stack for real-time visibility, protection, and control.

6. **Security budgets will increase focus on application security.** Major breaches like Equifax and Uber have shone a light on organizations that are not doing nearly enough to secure their software supply chain. "Today, every organization has an Equifax problem."

---

### Article 27
**Title:** Feeble APIs = Feeble App Security
**Source:** Contrast Security Blog
**Date:** June 29, 2022
**URL:** https://www.contrastsecurity.com/security-influencers/no-api-security-no-appsec

**Full Content:**

**The API Landscape:** Netflix alone operates "over 1,000 microservices," with APIs appearing in mobile apps, IoT devices, and cloud infrastructure. Approximately 200 million public and private APIs exist globally, yet many remain inadequately protected.

**Why API Security Matters:** Multiple high-profile breaches demonstrate API vulnerabilities. LinkedIn, Parler, and Clubhouse suffered data exfiltration through insecure APIs. Gartner research indicated that "90 percent of web-enabled applications would be more exposed to attack by API weaknesses than via the user interface."

**Limitations of Existing Tools:** SAST and DAST struggle with APIs. Dynamic scanning cannot properly invoke complex APIs without understanding their specifications. Static analysis misses vulnerabilities because it cannot trace complex execution flows through modern API patterns.

**The Solution:** Runtime security instrumentation embedded within applications. This approach allows organizations to observe actual application behavior and identify vulnerabilities without requiring external attack simulation.

**Core argument:** API security is not a separate discipline requiring separate tools — it is application security applied to APIs. Organizations that treat them as different problems end up with gaps in both.

---

### Article 28
**Title:** Building a Modern API Security Strategy: A Five-Part Series — Overview
**Source:** Contrast Security Blog
**Date:** July 20, 2022
**URL:** https://www.contrastsecurity.com/security-influencers/building-a-modern-api-security-strategy-a-five-part-series-overview

**Full Content:**

Williams opens with Spring4Shell as a case study: a critical remote code execution vulnerability that exemplifies why API security requires a fundamentally different approach.

**The Spring4Shell example:** The exploit represented "an autobinding vulnerability of the type that can easily apply to APIs." The flaw wasn't anyone's direct fault — Spring had proper defenses, and developers wrote secure code. Rather, dangerous interactions between components created the vulnerability. This demonstrates that "securing APIs is drastically different from securing applications."

**Why Traditional Tools Fall Short:** "Static Analysis Security Testing (SAST) and Dynamic Analysis Security Testing (DAST)...were designed for web applications from the early 2000s, and they haven't advanced much since then." These tools lack visibility into what they're actually scanning. Effective API security requires embedded instrumentation.

**Five Pillars of API Security (Williams' framework):**
1. API inventory — visibility into all APIs
2. API security testing — finding vulnerabilities and addressing OWASP Top 10 issues
3. Components — securing supply chains and identifying vulnerabilities in third-party libraries
4. API protection — identifying and preventing exploits in production
5. API access — implementing strong authentication and authorization

---

### Article 29
**Title:** Cybersecurity Insights with Contrast Co-Founder and CTO Jeff Williams | 11/18
**Source:** Contrast Security Blog
**Date:** November 18, 2022
**URL:** https://www.contrastsecurity.com/security-influencers/cybersecurity-insights-with-contrast-co-founder-and-cto-jeff-williams-11/18

**Full Content:**

Williams shares three key cybersecurity insights:

**Insight 1 — Federal Security Requirements:** Federal authorities are imposing strict deadlines for application and API security attestations from software vendors. OMB 22-18 requires vendors to "publish a statement disclosing how they ensure their applications are secure by October 2023."

**Insight 2 — SBOM Deployment Challenges:** Organizations implementing Software Bill of Materials (SBOMs) face significant obstacles. The core issue: "what's in their code repos doesn't match what's in their running applications." Williams emphasizes focusing on libraries that actually execute in production environments.

**Insight 3 — Source-Binary Mismatch Risk:** A critical vulnerability exists in open source distribution: "an executable open source library in a binary repository like Maven Central doesn't have to match the source code in a source code repository like GitHub." No verification mechanisms exist to detect these discrepancies.

---

### Article 30
**Title:** My Remarks at NIST Cybersecurity Executive Order Workshop
**Source:** LinkedIn Pulse
**Date:** June 3, 2021
**URL:** https://www.linkedin.com/pulse/my-remarks-nist-cybersecurity-executive-order-jeff-williams

**Full Content:**

Williams delivered remarks at a NIST workshop on the President's Cybersecurity Executive Order, arguing for a strategic focus in application security testing. Organizations often waste resources by running excessive tools and testing for irrelevant vulnerabilities.

**Five core recommendations:**

1. **Prioritize Fully Automated AST** — Manual appsec expertise is a bottleneck. Organizations should build automated testing pipelines incrementally rather than attempting comprehensive upfront solutions.

2. **Require Threat Modeling** — Instead of imposing universal testing requirements, NIST should mandate that teams develop simple threat models identifying their greatest risks and defensive strategies. Testing should align directly with these specific organizational threats.

3. **Allow Flexible Testing Methodology** — Different applications require different testing approaches. Rather than prescribing SAST, DAST, or IAST, empower teams to select and justify the optimal tool for each vulnerability type within their specific context.

4. **Measure Success Through Remediation** — "AST accomplishes NOTHING unless there's remediation." Organizations should prioritize mean-time-to-resolution metrics.

5. **Implement "Security in Sunshine"** — Transparency requirements — SBOMs, datasheets, security disclosures — address market failures by providing buyers information to distinguish secure from insecure software.

**Key critique:** Williams challenges the tendency to "overspecify" standards, warning that overly complex requirements become incompatible with actual software development practices and ultimately fail adoption.

---

---

## SECTION 4: COMPLETE ARTICLE LIST (ALL KNOWN TITLES)

### Dark Reading Articles by Jeff Williams

| Date | Title | URL |
|------|-------|-----|
| 2014 (Mar) | Flying Naked: Why Most Web Apps Leave You Defenseless | https://www.darkreading.com/application-security/flying-naked-why-most-web-apps-leave-you-defenseless-/d/d-id/1127875 |
| 2014 (Jul) | Why Your Application Security Program May Backfire | https://darkreading.com/operations/why-your-application-security-program-may-backfire/a/d-id/1278972 |
| 2014 (Sep) | An AppSec Report Card: Developers Barely Passing | https://www.darkreading.com/application-security/an-appsec-report-card-developers-barely-passing |
| 2015 (Mar) | Which Apps Should You Secure First? Wrong Question. | https://www.darkreading.com/application-security/which-apps-should-you-secure-first-wrong-question- |
| 2015 (Sep) | Why It's Insane to Trust Static Analysis | https://www.darkreading.com/vulnerabilities-threats/why-it-s-insane-to-trust-static-analysis |
| Unknown | The Common Core of Application Security | https://www.darkreading.com/vulnerabilities-threats/the-common-core-of-application-security |
| Unknown | The Staggering Complexity of Application Security | https://www.darkreading.com/application-security/the-staggering-complexity-of-application-security |
| 2022 (Jun) | What's Your AppSec Personality? | https://www.darkreading.com/cyber-risk/what-s-your-appsec-personality- |
| 2023 (Aug) | Legal Liability for Insecure Software Might Work, but It's Dangerous | https://www.darkreading.com/vulnerabilities-threats/legal-liability-for-insecure-software-might-work-but-it-s-dangerous |

### Security Magazine Articles by Jeff Williams

| Date | Title | URL |
|------|-------|-----|
| 2020 (Jun 19) | New NIST Standards on IAST and RASP Deliver State-of-the-Art AppSec | https://www.securitymagazine.com/articles/92648-new-nist-standards-on-iast-and-rasp-deliver-state-of-the-art-appsec |
| 2022 (Oct 3) | How to Build More Secure APIs | https://www.securitymagazine.com/articles/98429-how-to-build-more-secure-apis |

### Contrast Security Blog Articles (Chronological — Selected)

| Date | Title | URL |
|------|-------|-----|
| 2013 (Sep) | The *OTHER* Security Problem with Your Insecure Libraries | https://www.contrastsecurity.com/security-influencers/the-other-security-problem-with-your-insecure-libraries |
| 2013 (Dec) | The Guerrilla Guide to Buying an Application Security Tool | https://www.contrastsecurity.com/security-influencers/the-guerilla-guide-to-buying-an-application-security-tool |
| 2013 (Dec) | Secure Code Starts With Measuring What Developers Know | https://www.contrastsecurity.com/security-influencers/secure-code-starts-with-measuring-what-developers-know |
| 2016 (Jul) | The True Cost of "False Positives" in Application Security | https://www.contrastsecurity.com/security-influencers/the-true-cost-of-false-positive-vulnerabilities-in-application-security |
| 2016 (Jul) | With Only a Hammer, Everything Looks Like a Security Vulnerability! | https://www.contrastsecurity.com/security-influencers/when-all-you-have-is-a-hammer-everything-looks-like-a-security-vulnerability |
| 2016 (Aug) | The 4 Dimensions of a Sound Application Security Strategy | https://www.contrastsecurity.com/security-influencers/the-4-dimensions-of-application-security-strategy |
| 2016 (Oct) | Is There a 3rd Category of Application Security Tools Beyond Static & Dynamic? | https://www.contrastsecurity.com/security-influencers/is-there-a-3rd-category-of-application-security-tools-beyond-static-dynamic |
| 2017 (Jan) | Automating Application Security in Modern Software Projects | https://www.contrastsecurity.com/security-influencers/automating-application-security-in-modern-software-projects |
| 2017 (Apr) | Adding "A7: Insufficient Attack Protection" to the OWASP Top 10 | https://www.contrastsecurity.com/security-influencers/the-importance-of-adding-a7-insufficient-attack-protection-to-the-owasp-top-10 |
| 2017 (May) | A CTO's Response to Trump's Cybersecurity Executive Order | https://www.contrastsecurity.com/security-influencers/a-ctos-response-to-trumps-cybersecurity-executive-order |
| 2017 (Aug) | Thoughts on Modern Security Practices and Security Frameworks | https://www.contrastsecurity.com/security-influencers/thoughts-on-modern-security-practices-and-security-frameworks |
| 2017 (Dec) | Security Predictions for 2018 | https://www.contrastsecurity.com/security-influencers/jeff-williams-contrast-cto-security-predictions-for-2018 |
| 2021 (Jun) | My Remarks at NIST Cybersecurity Executive Order Workshop | https://www.linkedin.com/pulse/my-remarks-nist-cybersecurity-executive-order-jeff-williams |
| 2021 (Sep) | The Forthcoming 2021 OWASP Top Ten Shows That Threat Modeling Is No Longer Optional | https://www.contrastsecurity.com/security-influencers/the-forthcoming-2021-owasp-top-ten-shows-that-threat-modeling-is-no-longer-optional |
| 2021 (Oct) | Why We Need "Developer-First" Application Security | https://www.contrastsecurity.com/security-influencers/why-we-need-developer-first-application-security |
| 2022 (Jun) | Feeble APIs = Feeble App Security | https://www.contrastsecurity.com/security-influencers/no-api-security-no-appsec |
| 2022 (Jul) | Building a Modern API Security Strategy: A Five-Part Series — Overview | https://www.contrastsecurity.com/security-influencers/building-a-modern-api-security-strategy-a-five-part-series-overview |
| 2022 (Nov) | Cybersecurity Insights with Contrast Co-Founder and CTO Jeff Williams 11/18 | https://www.contrastsecurity.com/security-influencers/cybersecurity-insights-with-contrast-co-founder-and-cto-jeff-williams-11/18 |
| 2023 (Sep) | Trust 'Zero Trust' for Application Security | https://www.contrastsecurity.com/security-influencers/zero-trust-table-of-how-contrast-maps |
| 2023 | Shift Smart Instead of Following Shift-Left Fairy Tales | https://www.contrastsecurity.com/security-influencers/shift-smart-instead-of-following-shift-left-fairy-tales-application-security-appsec-contrast-security |
| 2024 (Aug) | How ADR Fixes AppSec in Production | https://www.contrastsecurity.com/security-influencers/contrast-security-founder-jeff-williams-explains-how-to-fix-appsec-in-production-adr |
| 2024 (Nov) | Smarter AppSec: How ADR, Secure by Design and 'Shift Smart' Are Redefining Cybersecurity | https://www.contrastsecurity.com/security-influencers/smarter-appsec-how-adr-secure-by-design-and-shift-smart-are-redefining-cybersecurity-application-security-podcast-takeaways-contrast-security |

---

## SECTION 5: KEY INTELLECTUAL THEMES & FRAMEWORKS

The following are the recurring intellectual positions and frameworks that characterize Jeff Williams' thinking across his body of work:

### 1. The Coverage Problem
Williams returns repeatedly to the insight that most AppSec programs only cover 10% of their application portfolio. The other 90% is "flying naked." The fundamental question for any AppSec leader should be "how do we secure our entire portfolio?" — not "which apps should we secure first?"

### 2. SAST/DAST Are Broken by Design
One of Williams' most consistent contrarian positions: static analysis and traditional dynamic scanning are fundamentally inadequate for modern application security. They are slow (hours to days per application), inaccurate (high false positive rates, low coverage), disruptive to development, and blind to the runtime behavior of applications. He has made this argument since at least 2015 and intensified it in subsequent years.

### 3. Instrumentation Is the Answer
Williams' alternative to SAST/DAST is security instrumentation — embedding sensors directly into running applications (IAST for testing, RASP for production protection). This provides inside-out visibility, works in real time, integrates with CI/CD, and achieves near-100% code coverage. All of his commercial work at Contrast Security implements this philosophy.

### 4. False Positives Are Not a Minor Inconvenience
Williams makes the case that false positives are economically catastrophic for AppSec programs. The math: if 85% of reported vulnerabilities are false positives, and teams have finite time to investigate, the actual vulnerabilities are buried. Programs built on high false-positive tools are not just inefficient — they create dangerous false confidence.

### 5. Transparency Over Liability
On the policy side, Williams consistently argues that mandatory transparency (SBOMs, security attestations, public disclosures) is more effective than legal liability. Transparency creates market pressure without the collateral damage of litigation.

### 6. Threat Modeling as Non-Negotiable
Williams has argued since at least 2021 that threat modeling is no longer optional — it is mandated by OWASP, NIST, PCI, and White House executive orders. Organizations that test without first understanding their threat model are spending resources in the wrong places.

### 7. DevSecOps Created New Silos
One of his more provocative recent arguments: DevSecOps, designed to bridge development and operations, has instead created new silos. Developers cannot become security professionals; security professionals cannot become developers. ADR (Application Detection and Response) is his answer — a layer that translates between the two worlds.

### 8. API Security Is AppSec (Not Separate)
Williams consistently argues against the proliferation of API-specific security tools as a separate category. APIs are application software and require the same testing, detection, and response mechanisms as any other application code. Treating API security as a separate discipline creates gaps and unnecessary tool complexity.

### 9. Shift Smart (Not Shift Left)
The "100x cheaper to fix early" statistic is a fairy tale. The right model is not "shift everything left" but "shift smart" — apply each type of security test at the point in the SDLC where it provides the most value, which varies by vulnerability type.

### 10. Production Security Is the Real Gap
Williams' most recent emphasis: production is where actual attacks happen, and most AppSec programs have zero visibility there. DevSecOps generates backlogs; ADR provides actual runtime detection and response. The average organization has a backlog of 1.1 million vulnerabilities — generating more without fixing or protecting against them is counterproductive.

---

*End of collection. Collected 2026-02-19.*

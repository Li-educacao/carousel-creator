# Communication Templates -- Jeff Williams

**Subject:** Jeff Williams (OWASP Co-Founder, Contrast Security CTO)
**Version:** 1.0
**Date:** 2026-02-19
**Purpose:** Ready-to-use response templates based on his documented patterns

---

## 1. How He Opens a Keynote

**Pattern:** Contrarian assertion + surprising data point + escalation ladder

**Template:**
> For the last 20 years, the application security industry has been telling you a fairy tale. The fairy tale goes like this: if you find vulnerabilities early, it costs 100 times less to fix them. Shift everything left. Scan early, scan often.
>
> There's one problem. That 100x number? I went looking for the original source. It might not even exist. It was cited in a book, which cited an internal training chart from a company, which had no supporting documentation. And we built an entire industry strategy on it.
>
> Meanwhile, here's what we do know: the average application has 26.7 vulnerabilities. That number hasn't changed in 20 years. We've been publishing the OWASP Top 10 for two decades, and the same vulnerabilities keep appearing. Something is fundamentally broken.
>
> Today I want to talk about what that something is -- and what we should be doing instead.

**Alternate opener (data-led):**
> 79% of the code in your applications is open-source libraries. Only 38% of that library code actually executes at runtime. Your SCA tool flags every library in the manifest, regardless of whether the vulnerable function is ever called. That means 62% of your remediation effort is going to libraries that don't matter. Let me explain why that happens and how to fix it.

---

## 2. How He Responds to "What Is OWASP?"

**Pattern:** Founding story + mission + honest assessment of impact

**Template:**
> OWASP is the Open Web Application Security Project -- the world's largest open-source community dedicated to application security. I co-founded it back in 2001. The idea was simple: security knowledge should be free and accessible to everyone. Developers, organizations, governments -- everyone should have access to the same information about how to build secure software.
>
> We created the OWASP Top 10, which became the de facto awareness document for application security worldwide. We built WebGoat so developers could learn hands-on. We created ASVS as a verification standard and ESAPI as a security library. All free, all open.
>
> I served as Global Chairman for nine years, unpaid. I'm proud of what we built. OWASP created a shared vocabulary for security risks -- that's genuinely valuable. But I'll be honest: the Top 10 hasn't really changed anything at the systemic level. The same vulnerability classes keep appearing. The average vulnerability count hasn't moved in 20 years. Awareness was necessary, but it was not sufficient. That realization is what led me to instrumentation and to Contrast Security.

---

## 3. How He Explains IAST to a Non-Technical Audience

**Pattern:** Physical-world analogy (94Fifty basketball) + mapping + inevitability

**Template:**
> Let me tell you about a basketball. The 94Fifty is a regular basketball with sensors inside -- accelerometers that measure the spin, the arc, the speed, and the backspin of every shot. I got one, and after about an hour of shooting, it told me my shot was too flat. I didn't need an expert coach. I didn't need a bunch of extra steps. I just got immediate, actionable feedback from the ball itself.
>
> That's exactly what IAST does for applications. Instead of having a security expert scan your application from the outside -- which is like having a basketball coach watch from the sideline and guess what's wrong -- you put sensors inside the application itself. The application monitors its own behavior. It sees exactly how data flows through the code, which libraries are called, which database queries run. When it detects a vulnerability, it tells the developer immediately, with the exact location and how to fix it.
>
> The key insight is that everything complicated in the world, we instrument it. Planes have thousands of sensors. Cars have OBD diagnostics. Your watch monitors your heart rate. Software is the most complex thing mankind has ever created, and it's barely instrumented at all. IAST changes that.

---

## 4. How He Challenges Industry Dogma

**Pattern:** Acknowledge the belief + trace to source + show evidence is weak + reframe

**Template (for "Shift Left"):**
> Look, the intent behind shift left is right. Finding problems early is better than finding them late. Nobody disagrees with that.
>
> But the specific claim -- that fixing bugs in production costs 100 times more than fixing them in design -- I've looked for the original source of that number. It traces back through citations to a training chart at a single company with no supporting data. The entire shift-left economics may be built on a statistic that doesn't exist.
>
> More importantly, "shift left" has been misinterpreted. It's become "shift all security work onto developers as early as possible." But some tests don't work without runtime context. You can't find an injection vulnerability by looking at a code snippet in isolation -- you need to see how data actually flows through the running application. Testing too early with insufficient context doesn't give you accurate results. It gives you false positives. 400 findings, only 40 real, and you miss 30 because your team is buried in noise.
>
> That's why I advocate for Shift Smart. Test at the right time, with the right context, for the right vulnerabilities. Notify developers in their tools, yes -- but perform the detection where the accuracy is highest.

---

## 5. How He Gives Advice to a CISO

**Pattern:** Validate their situation + quantify the problem + reframe strategy + specific recommendation

**Template:**
> I understand the pressure you're under. You've got a growing application portfolio, a limited security team, and a vulnerability backlog that's getting worse, not better. You've invested in SAST, DAST, maybe a WAF. And the numbers aren't improving.
>
> Here's why: your security coverage is multiplicative, not additive. If you test 30% of your portfolio, for 50% of vulnerability types, covering 50% of code paths, 25% of the time -- multiply those together. That's under 2% actual coverage. Adding another tool with the same blind spots doesn't materially change that number.
>
> What would I recommend? Three things. First, instrument your most critical applications with runtime agents. Not scan them -- instrument them. Inside-out visibility, not outside-in scanning. Second, prioritize by reachability. 79% of your code is libraries, but only 38% actually executes. Don't waste remediation effort on vulnerabilities in code that never runs. Third, move from periodic testing to continuous security. Your pen test runs once a year. Your applications deploy weekly. That gap is where the risk lives.

---

## 6. How He Critiques a Security Approach

**Pattern:** Acknowledge intent + identify the information constraint + present evidence + offer alternative

**Template (critiquing SAST):**
> SAST is well-intentioned. Analyzing source code for security flaws before deployment makes intuitive sense. The problem isn't the intent -- it's the information constraint.
>
> SAST sees code but not runtime behavior. It doesn't know which libraries execute, which code paths are reachable with real inputs, or how configuration affects behavior. It's trying to reason about a running system by reading a blueprint. Some things you just can't determine from a blueprint.
>
> The result is predictable: high false positive rates. A typical SAST scan generates about 400 findings. Maybe 40 are real. Your security team triages what they can, maybe 10, and misses 30 real vulnerabilities buried in the noise. The tool creates a situation where the effort goes to waste and the real risks go unaddressed.
>
> The alternative is IAST -- instrument the application and observe actual runtime behavior during your existing functional tests. Same development effort, dramatically more accurate results, near-zero false positives. You're not asking developers to do anything new. The instrumentation does the work.

---

## 7. How He Discusses Policy and Regulation

**Pattern:** Apply legal-technical hybrid lens + prefer transparency + acknowledge complexity + warn of unintended consequences

**Template:**
> My law background tells me that regulation usually has unintended consequences. The question isn't whether software should be more secure -- obviously it should. The question is what mechanism drives improvement most effectively with the fewest side effects.
>
> Legal liability might work as an incentive. But the practical consequences would be unpredictable. You could end up with security theater optimized for courtrooms rather than actual security. Companies would minimize documentation to reduce legal exposure. Open-source contribution would slow down because contributors would fear liability. The cure could be worse than the disease.
>
> What I advocate for instead is mandatory transparency. Require organizations to publish SBOMs -- software bills of materials showing what's in their software. Require standardized security metrics. Give buyers the information to make informed decisions. Markets correct faster with information transparency than with punitive regulation.
>
> SBOM mandates, standardized disclosure, procurement requirements that demand transparency -- these are concrete, measurable, and they create market incentives for improvement without the unintended consequences of a liability regime.

---

## 8. How He Tells the 94Fifty Basketball Story

**Pattern:** Set the scene + demonstrate the analogy + extract the principle + apply to software

**Template:**
> A couple of years ago I got a basketball called the 94Fifty. It looks like a regular basketball, but it has embedded sensors -- accelerometers that measure everything: dribble speed, shot rotation, arc, makes and misses.
>
> I took it to the court. After about an hour, it told me something: my shot was too flat. I'd been shooting for 30 years and never knew that. I didn't need an expert coach to stand there watching and analyzing. I didn't need to change my routine. The ball itself gave me the feedback because it was instrumented.
>
> That's the insight I keep coming back to: instrumentation can democratize whole industries. The 94Fifty democratized basketball coaching. Wearable health monitors are democratizing medicine -- your phone knows you're sick before you do.
>
> Now think about software. The most complex thing mankind has ever created, and it's barely instrumented at all. We're trying to secure it by looking at it from the outside -- scanning, probing, guessing. That's like a basketball coach watching from across the gym through binoculars. Put the sensors inside. Let the application tell you what's going on.

---

## 9. How He Responds to "Isn't SAST Enough?"

**Pattern:** Short challenge + data + reframe

**Template:**
> No, and here's why. SAST operates without runtime context. It sees code, but it doesn't see how that code behaves when the application is assembled, configured, and running with real data.
>
> The result: 400 findings from a typical scan. Only about 40 are real vulnerabilities. Your security team can triage maybe 10 in the time they have. They miss 30 real vulnerabilities -- not because they're lazy, but because they're drowning in noise from the 360 false positives.
>
> SAST is not 90% useful. A tool with a 90% false positive rate is net negative. It trains developers to ignore security findings entirely. The cost of false positives isn't just wasted time -- it's destroyed trust in security tooling. When the real finding comes through and nobody pays attention, that's worse than having no tool at all.

---

## 10. How He Discusses the SOC's Blind Spot

**Pattern:** Industry inventory + gap identification + ADR positioning

**Template:**
> Let's inventory what the SOC has. EDR for endpoints -- they can see what's happening on workstations and servers. NDR for networks -- they can see traffic patterns. Maybe XDR to correlate across sources. Those are all valuable.
>
> Now ask: what can they see happening inside your applications? The answer, for most organizations, is nothing. The application layer -- where your business logic lives, where customer data is processed, where the actual attack targets are -- is a complete blind spot for security operations.
>
> Attackers know this. That's why they increasingly target the application layer. They know the SOC can't see what's happening there. Application Detection and Response -- ADR -- fills that gap. It gives the SOC application-layer telemetry for the first time. It's as inevitable as EDR was a decade ago.

---

## 11. How He Responds to "We Have a Vulnerability Backlog"

**Pattern:** Validate + reframe the problem + offer pragmatic path

**Template:**
> Every organization has a vulnerability backlog. The industry average is staggering -- we're talking about 1.1 million unresolved vulnerabilities across a typical enterprise portfolio. And that number is growing, not shrinking.
>
> Here's the uncomfortable truth: you are never going to fix all of them. The backlog is growing faster than remediation capacity. If your strategy depends on fixing every vulnerability before it can be exploited, your strategy has already failed.
>
> That's why you need two things working together. First, prioritize by reachability. 79% of your code is libraries, but only 38% actually executes. Focus remediation on vulnerabilities in code paths that actually run. Don't waste effort on theoretical risks. Second, deploy runtime protection. RASP -- or what we now call ADR -- protects your applications even when vulnerabilities haven't been patched. It bridges the gap between "we know about it" and "we've fixed it." That gap is where the risk lives.

---

## 12. How He Corrects the DevSecOps Misinterpretation

**Pattern:** State the original intent + identify the misinterpretation + correct with framework

**Template:**
> DevSecOps is really about transforming the work of security. That's the original insight -- not shifting security work onto developers, not bolting SAST onto a CI pipeline and calling it transformation. Transforming the work itself.
>
> What I see in most organizations that claim to do DevSecOps is this: they took the same broken tools -- the same SAST that produces 90% false positives, the same DAST that can't see inside the application -- and they automated running them in the pipeline. That's not transformation. That's automation of the same broken process.
>
> Real DevSecOps follows the Three Ways. Flow: break security work into small, continuous pieces instead of batch-and-queue gates. Feedback: give developers real-time, actionable findings in their tools, not 200-page PDF reports. Culture: make security issues learning opportunities, not blame events. When you transform the work this way, security becomes invisible infrastructure, not a bottleneck.

---

## 13. How He Handles Technical Deep Dives

**Pattern:** Name the specific technology + explain the mechanism + connect to principle

**Template (on Java instrumentation):**
> Here's how it works at the technical level. The Java Instrumentation API allows you to transform bytecode as classes are loaded by the JVM. Libraries like Byte Buddy make this practical at scale. You write sensors that hook into specific methods -- the ones that handle HTTP requests, execute SQL queries, read files, call external services.
>
> When the application runs, the agent sees everything: which data came in from the HTTP request, how it flowed through the controller, whether it passed through a validation function, which library processed it, and whether it reached a dangerous method like executeQuery without being parameterized.
>
> That's why IAST can find a SQL injection with zero false positives. It didn't guess by reading the source code. It watched the actual data flow through the actual running code and confirmed: yes, this specific user input reached this specific SQL query without sanitization through this specific code path. Here's the exact line, here's the data flow trace, here's how to fix it.

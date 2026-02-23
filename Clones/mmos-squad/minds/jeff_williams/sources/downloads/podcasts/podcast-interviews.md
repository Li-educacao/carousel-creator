# Jeff Williams — Podcast Interviews & Interview Transcripts

**Collected for:** Cognitive Cloning Project
**Date collected:** 2026-02-19
**Subject:** Jeff Williams, Co-Founder & CTO of Contrast Security, OWASP Co-Founder & Former Global Chair

---

## Table of Contents

1. [Practical DevSecOps Using Security Instrumentation — Eficode DevOps Sauna Podcast (2020)](#1-practical-devsecops-using-security-instrumentation--eficode-devops-sauna-podcast-2020)
2. [EnterpriseReady Podcast Ep. 15 — Self-Protecting Software (2019)](#2-enterpriseready-podcast-ep-15--self-protecting-software-2019)
3. [LinkedIn Interview with Ron Gula — Contrast Security CTO Q&A (2017)](#3-linkedin-interview-with-ron-gula--contrast-security-cto-qa-2017)
4. [Application Security Podcast — The Tech of Runtime Security (2022)](#4-application-security-podcast--the-tech-of-runtime-security-2022)
5. [Application Security Podcast — Application Detection & Response / ADR (2024)](#5-application-security-podcast--application-detection--response--adr-2024)
6. [TechRound Interview — Meet Jeff Williams, CTO at Contrast Security](#6-techround-interview--meet-jeff-williams-cto-at-contrast-security)
7. [Code Patrol Podcast — OMB M-22-18 Secure Software Development Compliance (2022)](#7-code-patrol-podcast--omb-m-22-18-secure-software-development-compliance-2022)
8. [Code Patrol Podcast — Software Transparency with NIST Fellow Ron Ross (2022)](#8-code-patrol-podcast--software-transparency-with-nist-fellow-ron-ross-2022)
9. [Contrast Security Blog — How ADR Fixes AppSec in Production (2024)](#9-contrast-security-blog--how-adr-fixes-appsec-in-production-2024)
10. [Contrast Security Blog — Shift Smart Instead of Following Shift-Left Fairy Tales (2023)](#10-contrast-security-blog--shift-smart-instead-of-following-shift-left-fairy-tales-2023)
11. [Contrast Security Blog — Zero Trust for Application Security (2023)](#11-contrast-security-blog--zero-trust-for-application-security-2023)
12. [Contrast Security Blog — Smarter AppSec: ADR, Secure by Design & Shift Smart (2024)](#12-contrast-security-blog--smarter-appsec-adr-secure-by-design--shift-smart-2024)
13. [Cybersecurity Insights — Contrast CTO Jeff Williams (November 2022)](#13-cybersecurity-insights--contrast-cto-jeff-williams-november-2022)
14. [CyberScoop Federal — Making Applications More Secure at Federal Agencies (2015)](#14-cyberscoop-federal--making-applications-more-secure-at-federal-agencies-2015)
15. [DevOps Chat — AppSec and DevSecOps (DevOps.com) — Summary](#15-devops-chat--appsec-and-devsecops-devopscom--summary)
16. [DevOps Chat — Shifting Security Left and Right (Security Boulevard 2019) — Summary](#16-devops-chat--shifting-security-left-and-right-security-boulevard-2019--summary)

---

## 1. Practical DevSecOps Using Security Instrumentation — Eficode DevOps Sauna Podcast (2020)

**Source:** https://www.eficode.com/devops-podcast/practical-devsecops-jeff-williams
**Format:** Podcast transcript (recorded at DevOps 2020 event)
**Participants:** Jeff Williams (Co-Founder & CTO, Contrast Security), Lauri (Host, Eficode CMO)

---

### Full Transcript

#### Opening Remarks

Lauri welcomes listeners to DevOps Sauna and explains the podcast originates from recordings of the DevOps 2020 event. He introduces Jeff Williams as the speaker for today's discussion on security instrumentation.

#### Jeff Williams' Main Presentation

**Introduction:**

Jeff Williams states: "I am super excited to talk with you today about the magic of security instrumentation." He identifies himself as co-founder and CTO at Contrast Security, explaining the company offers a DevSecOps platform covering vulnerability testing, library analysis, and runtime protection.

**Background & Problem Statement:**

Williams shares 25 years of experience in both development and security. He presents data showing "the average web application or web API has 26.7 security problems, on average," measured across tens of thousands of applications. Critically, he notes: "That number hasn't changed in the last 20 years."

He diagnoses the core issue: "Security code just isn't making it into all the right places in the application reliably."

**Traditional Security Failures:**

Williams critiques existing approaches, asking rhetorically about security requirements documents nobody reads and secure coding training people "slept through." He emphasizes: "The root cause here is generally security has operated outside development."

He argues this separation forces security into "very destructive guerrilla tactics" to get changes into production.

**DevSecOps Definition:**

Williams clarifies DevSecOps misconceptions: "I think too often when people say the word DevSecOps, what they're really saying is that we should shove all the security work onto developers. That's not fair and it doesn't work."

Instead, he proposes: "DevSecOps is really about transforming the work of security, exactly the way the development work was transformed by DevOps."

**Three Ways of DevSecOps:**

1. **Security Workflow**: "Security work needs to be broken up into smaller chunks to create flow."

2. **Continuous Feedback**: "Security needs to create continuous security feedback. That's not an annual pen test."

3. **Security Culture**: "The security culture can't be about blame and hiding."

#### The 94Fifty Basketball Analogy

Williams introduces instrumentation using an analogy: "This is an instrumented basketball. It tells you dribble speed and shot rotation and the arc of your shot, how many you've made and missed."

He explains the power: "After one hour, the 94Fifty let me know that my shot was too flat." The key insight: "I didn't need an expert coach. I didn't need a bunch of extra steps. I just did it myself."

**Broader Application:**

Williams states: "I believe that instrumentation can democratize whole industries." He applies this to medicine, where "your phone or your watch knows you're sick before you do."

#### How Software Instrumentation Works

**Technical Foundation:**

Williams explains: "Instrumenting software is really easy and it's amazingly powerful. It's a great way to do security testing."

He details the process: "You add an agent to your application." For Java, "this is a JAR file using the Java instrumentation API. For .net it's a profiler, works roughly the same way, and we can do instrumentation in Node, and Ruby, and Python, and Go, and other languages as well."

**The Mechanism:**

As code loads into memory, "our agent hooks that process so that we can add sensors directly into the application to measure exactly what we care about."

**Accuracy & Data Collection:**

"It's accurate because we're measuring the real running application, and our sensors can gather not just a little detail, but all the contexts that we need to really decide whether something's a vulnerability or an attack."

#### Demonstration 1: SQL Injection Detection

**Setup:**

Williams demonstrates using Byte Buddy, a Java instrumentation library. The goal: "We're going to instrument this application to show me anywhere that I'm not using parameterized queries."

**Code Example Explanation:**

He explains the agent searches for "the implementation of the Java SQL statement class" across multiple database drivers and frameworks.

**Execution:**

Williams runs the application: "When we hit submit, you'll see we now just get a dump that says, 'Hey, you used a non-parameterized SQL query. Here's the actual query.'"

**Testing Integration:**

Williams proposes: "Your normal test cases, when you're doing like your end-to-end testing, your normal test cases can fail for security reasons because we just throw an exception and stop this from running."

#### Demonstration 2: Access Control Matrix & Encryption Monitoring

**Multi-Sensor Approach:**

This example uses "sensors in it. We're going to capture some details from the service method. We're going to look at access control calls. We're going to look at encryption calls, and some other sensors related to the ServletRequest and the ServletContext."

**Access Control Testing:**

Williams explains traditionally, "access control is incredibly difficult to test correctly. You either need to spend weeks analyzing the source code or you need to pen test and you need to assume each role and then test the entire application with that."

His solution: "We can do it much faster if we just cheat, and we have the application tell us exactly where all the access control checks are."

**Matrix Results:**

From the demonstration, Williams observes patterns:
- "Access A checks Role A, Access B checks Role B, Access C Role C"
- "Access D doesn't have any access control check. That's a little concerning."
- "Access E here has three different access control checks, which is possible, but a little unusual."

**Freezing & Alerts:**

"Once you have it right, you may decide to freeze it. And if you freeze your access control matrix, then you could even get alerted if anything there changes."

**Test Coverage Tracking:**

Williams demonstrates tracking which user roles tested which pages, identifying gaps in test coverage.

**Encryption Analysis:**

"Access A, B, C, and E have encryption algorithms associated with them, but Access D doesn't. That's potentially concerning."

He observes: "You probably want to standardize on one. That probably should be AES rather than password based encryption or DES."

#### Demonstration 3: Command Injection Prevention

**Sandbox Rule:**

"Our rule is that we want to prevent any operating system processes from being started while we're inside the service method."

**Implementation:**

"We instrument the same way. We're just adding the sandbox advice to the ProcessBuilder. And so here, if we enter that ProcessBuilder method, we've added this code into that method with instrumentation, and it just checks to see if we're in scope, then we're going to block that process."

**Real-World Impact:**

"This would prevent the stretch exploit from a few years ago, which was basically an expression language that caused a native process to start."

Williams characterizes this as: "Quite a powerful sandboxing of a critical capability within the application itself."

#### Inside-Out vs. Outside-In Security

**Traditional Outside-In Approach:**

"You feed your code and your libraries, and some tools, and the output comes out. And then you need a lot of people involved to triage the false positives, to correlate the findings, to create tickets."

Problems: "It's slow and burdensome, often it takes days or weeks to get feedback into the pipeline."

Result: "All the feedback comes back in the form of PDF reports that are full of false positives and generates a big backlog."

**Modern Inside-Out Approach:**

"Instead of just analyzing the pieces separately, imagine we analyze the entire application, put together with some instrumentation, we'll add the instrumentation. And now when we feed this application into the pipeline, we can get instant feedback on vulnerabilities as part of our normal testing."

Key advantage: "We don't need experts involved in this process."

**Continuous Flow:**

"All the way to prod and in production, we can watch for attacks and notify the people that need to know about attacks instantly all with instrumentation."

#### DevSecOps Success Formula

Williams concludes: "Ultimately, that's the secret to DevSecOps is getting this process moving with the three ways that I talked about with getting security flow, tight security feedback loops, and this will allow a culture of instrumentation, of innovation and learning in our DevOps process."

**On Technology's Role:**

"I don't think application security is hopeless, even though it hasn't been making progress in the past. I'm not saying that technology alone can solve our security issues, good security, the mix of culture and people and process and technology."

**Instrumentation's Promise:**

"But with instrumentation, we can create a platform where development and security can finally work together."

**Community Offering:**

Williams promotes Contrast Security's community edition: "If you want to try some powerful instrumentation, you can use our community edition. It's free for one app, full strength instrumentation to find vulnerabilities, protect you against attacks and analyze open source."

#### Q&A Session

**Question 1: Static Code Analysis Alternative**

*Lauri asks:* "Is there a way to use a static code analysis to find security vulnerabilities instead of doing instrumentation?"

*Jeff responds:* "Yeah. So static code analysis can find vulnerabilities, but the problem is it's not very accurate. So it finds tons of false positives and that requires experts, which ultimately that means it's going to slow down your process, and it's kind of the opposite of what we're trying to do here. So instrumentation is a newer better option than static, which has been around for over 15 years and it's not getting better."

**Question 2: Shifting Security Left in Feature-Focused Organizations**

*Lauri asks:* "What are your recommendations to left shift security culture in big organizations where feature development is the primary priority?"

*Jeff responds:* "Yeah, that's exactly the point of this talk is to use instrumentation to enable development teams to do their own security testing, find their own vulnerabilities and fix them and check in clean code."

He elaborates: "It's not something that's easy to do with other kinds of tools because they're inaccurate. And if you're inaccurate, you need experts and if you need experts, it slows down the process. If it slows down the process, then you're impeding feature development. So, it really comes down to getting better telemetry from your application."

**Question 3: Automated vs. Manual Security Testing**

*Lauri asks:* "What's your view on automated security for tools like instrumentation and other ASD tools versus manual security testing by security experts?"

*Jeff responds:* "Yeah. There's always going to be a role for manual security testing. I spent many, many years doing that. I've found tens of thousands of vulnerabilities that way, but it doesn't scale very well and you need experts."

He argues: "We really need automated security testing and it has to be accurate in order to scale. Instrumentation is a way of getting there. It's considerably more powerful than sort of legacy techniques like static analysis and dynamic analysis."

**Final Recommendation:**

"I encourage you to go past just seeking the known vulnerabilities, like the things in the OWASP Top 10. I encourage you to get to where you're testing your own security defenses."

He emphasizes: "I think this technique makes it easy enough that you can create your own security tests for things that historically haven't been automatable."

---

## 2. EnterpriseReady Podcast Ep. 15 — Self-Protecting Software (2019)

**Source:** https://www.enterpriseready.io/podcast/15-jeff-williams-contrast/
**Mirror/Full version:** https://www.heavybit.com/library/podcasts/enterpriseready/ep-15-self-protecting-software-with-jeff-williams-of-contrast-security
**Topics:** OWASP Top 10 origins, AppSec standards, inside-out vs outside-in security, enterprise go-to-market

---

### Key Statements from Jeff Williams

**On His Background:**

"I started writing software in high school, way back in the early 80s, and accidentally got into security along the way."

**On the OWASP Top 10 Origins:**

"I wrote this thing that I called the OWASP Top 10 and it was a little side project, I put it out there and it just went crazy. People started downloading it, OWASP got slashdotted and then a little while later they asked me to take over as a global chair of OWASP."

**On the OWASP Top 10's Limitations:**

"I feel of two minds about it. In one sense, I like the fact that it's out there and it raises awareness of AppSec."

He noted the list hasn't substantially changed since 2002, stating the vulnerabilities remain "the same stuff that's in there...it's 2019 now. It's still the same stuff."

**On Security Standards:**

"There are a ton of standards, and there's really no very well accepted standards in application security."

**On Application Security Philosophy:**

"AppSec is pretty hard...AppSec is more like clay, you can build anything with software. So there's many more degrees of freedom in screwing things up."

**On the Scaling Problem:**

"The biggest problem I see in organizations is the ability to scale AppSec...we need to automate...the transition is about getting from this outside in approach of scanning and firewalling, to an embedded approach where the security is happening within the thing we're trying to protect."

**On the Shocking State of Vulnerabilities:**

"The average application has 26.7 vulnerabilities, which is a horrific number."

**On Contrast Security's Go-to-Market Strategy:**

"We went right for the biggest companies...they pushed us really hard on those enterprise features right away."

**On the Changing Security Landscape:**

"I think the game's changed. It's become an environment where you have to be secure to sell to these big enterprises."

---

## 3. LinkedIn Interview with Ron Gula — Contrast Security CTO Q&A (2017)

**Source:** https://www.linkedin.com/pulse/interview-jeff-williams-contrast-security-cto-ron-gula
**Interviewer:** Ronald Gula (Gula Tech Adventures, investor in Contrast Security)
**Date:** April 20, 2017
**Context:** Gula notes: "I've known Jeff Williams for more than a decade. He is the CTO of Contrast Security. He's done very much to advance the art of web application security auditing and his development team is based in the Natty Boh building in Baltimore. I invested in Contrast for their pioneering RASP technology and how much customers raved about them during diligence."

---

### Full Q&A Transcript

**Q1: Problem Statement & Differentiation**

*Question:* "Contrast helps secure web applications and APIs in a much different way than application firewalls or static source code scanners. What problem does Contrast address and how is it different from web application firewalls and source code auditing?"

*Jeff Williams' Response:*

"The tools available to secure web applications (SAST, DAST, and WAF) were invented in the early 2000's, and they haven't evolved to keep up with modern software. You had to use a bunch of different tools and none of them worked very well. Unlike external scanners and protections, Contrast analyzes and protects applications from within, using a technique called dynamic binary instrumentation. Essentially, Contrast enables applications to protect themselves… turning them into what we call 'self-protecting software.' Working from inside the application allows Contrast to combine the strengths of multiple different analysis techniques, as it has access to code, HTTP traffic, configuration, libraries, backend connections, data flow, and more all at once. This makes Contrast much faster and more accurate than traditional tools. Enabling applications with Contrast is a quick and easy process – and from that point forward, your whole application portfolio is continuously assessed for vulnerabilities and protected against attack."

**Q2: Response to Major Vulnerabilities**

*Question:* "We've had many big web vulnerabilities occur over the past few years including HeartBleed and now the most recent Apache Struts vulnerability. How does Contrast help stop attacks against these vulnerabilities?"

*Jeff Williams' Response:*

"Every organization needs to be able to quickly respond when one of these third-party component vulnerabilities comes out. Attacks on Struts 2 applications started within a day. We have been attacked regularly every day since it came out, and so have all our customers. Contrast works two ways to help organizations survive this kind of threat. First, Contrast automatically blocks attempts to exploit known vulnerabilities in third-party components. We call this 'CVE Shields' and basically Contrast instruments these libraries in a way that makes the known vulnerability unexploitable. The main benefit is that your applications stay online and safe, even if they have a known vulnerability. There really isn't a downside to using CVE Shields, as they're safe, scalable, and automatic. Second, Contrast also inventories all third-party libraries in use everywhere in the enterprise with the exact version number and any known vulnerabilities. This is a 'big data' approach that gives you the ability to know exactly what code you are running in every application and every server… no more surveys."

**Q3: Vulnerabilities Evading Traditional Tools**

*Question:* "Can you give some anecdotal examples of web vulnerabilities in custom code that evaded application firewalls and source code scanners?"

*Jeff Williams' Response:*

"The problem with both application firewalls and source code scanners is that they only have part of the picture. WAFs can only see the HTTP traffic, so they are totally blind to what goes on inside the application. They can only detect SQL injection if something blows up and they can detect the problem in the response. But that doesn't always happen, so they miss a lot. Same thing with source code scanners. They can't see how the application is put together or what's going on in the HTTP traffic. So they have no way to see if your CSRF defenses are correct or whether you're using HTTP headers correctly. One of the biggest problems with source code scanners (SAST) tools is that they are very poor at data flow analysis. It's just too difficult to calculate how data will flow through an application by looking at the source code, particularly in modern applications with lots of libraries and frameworks. APIs are particularly difficult as well. Poor data flow analysis means that you are going to miss a large percentage of SQL Injection, XSS, Command Injection, LDAP Injection, XPath Injection, XXE, SSRF, and other serious vulnerabilities."

**Q4: Deployment Process**

*Question:* "How is Contrast deployed?"

*Jeff Williams' Response:*

"Simple, just add our agent to your application environment. It takes under a minute and it doesn't require any security expertise to install or use. In Development, coders get instant feedback on their code through Eclipse, Slack, HipChat, JIRA, Jenkins, etc... In QA, every test case now doubles as a security test with no extra effort. And in Production, Contrast blocks attacks and alerts the appropriate teams through Splunk, ArcSight, PagerDuty, etc…"

**Q5: SIEM and Incident Response Integration**

*Question:* "Have you seen customers take the output of Contrast and send it to their SIEM, Threat and/or incident response platforms?"

*Jeff Williams' Response:*

"Absolutely. Contrast is the best application security sensor ever created. And while we love our dashboards, we understand that companies need security data in *their* dashboards. So all of Contrast's data feeds into SIEMs and other operational tools easily. Interestingly, we also have a feature called 'log enhancers' which allows organizations to beef up the security logging in their applications without changing any source code, retesting, or redeploying. Basically, you can instantly get much better security telemetry out of your applications, enhancing the results of all the downstream analysis."

**Q6: Learning Resources**

*Question:* "If developers or IT security people want to learn more is there a webinar or white paper you would suggest they read?"

*Jeff Williams' Response:*

"The quickest way to know what Contrast is all about is this three-minute video from the RSA Innovation Sandbox. For a deeper dive into RASP with Contrast Protect, you might enjoy this webinar with one of the inventors of this technology, Contrast's Chief Scientist Arshan Dabirsiaghi. There's much more on our website at http://contrastsecurity.com. And you might like some of my articles about the future of application security. If you're interested in the future of application security in a modern software environment, check out Contrast's 'Continuous Application Security Handbook'."

---

## 4. Application Security Podcast — The Tech of Runtime Security (2022)

**Source:** https://appsec.buzzsprout.com/1730684/episodes/13558271
**Host:** Chris Romeo and Robert Hurlbut
**Topics:** IAST, SAST/DAST limitations, runtime security, mean time to repair, library usage data

---

### Key Statements from Jeff Williams

**On AppSec Backlogs:**

"If you use noisy tools, they're gonna generate a big pile of stuff that needs to be triaged, and nobody has the resources to do it."

**On SAST/DAST Limitations:**

"SAST tools have reached the limit of their evolution...there's no more information there to get better with. It's a lack of context. That's the problem."

**On Runtime Security Approach:**

"The only way to figure it out is to actually watch that code as it's running. Then everything's assembled, everything's in context."

**On IAST for DevOps:**

"IAST is really ideal for DevOps...it turns your normal test cases into security tests...there's literally nothing that you have to change about the way that you build, test, or deploy code."

**On Mean Time To Repair:**

"Our MTTR across hundreds of thousands of applications is like three days. It's not 290 days like static or 315 days like DAST."

**On Vulnerability Rates:**

"A typical project will introduce like four new vulnerabilities per month per project...we see that rate go down to 0.9 new vulnerabilities per month per app after using IAST for a while."

**On Library Usage (a surprising data point):**

"62% of libraries never load. That code never runs. Only 38% of libraries ever even load into memory."

**On AppSec Backlogs as an Anti-Pattern:**

"Maintaining an AppSec backlog and ASPM in general is an anti-pattern...you've gotta fix the vulnerability flow problem."

**Call to Action:**

"Check out runtime security...give it a shot, see if it's applicable to your enterprise."

---

## 5. Application Security Podcast — Application Detection & Response / ADR (2024)

**Source:** https://appsec.buzzsprout.com/1730684/episodes/15805086-jeff-williams-application-detection-response-adr
**Date:** September 24, 2024
**Host:** Chris Romeo and Robert Hurlbut
**Duration:** 51:28
**Topics:** ADR, secure by design, shift smart, runtime security observability

---

### Key Statements from Jeff Williams

**On AppSec Backlogs:**

"If you use noisy tools, they're gonna generate a big pile of stuff that needs to be triaged, and nobody has the resources to do it."

**On ADR's Origins — Pen Testing and Threat Modeling Limitations:**

Williams explained that pen testing and threat modeling are "highly time-pressured" because "every time you start pen testing and threat modeling with a new application, you have to learn everything from scratch."

**On Security Blueprints from ADR:**

He stated that ADR generates detailed application maps showing "all the endpoints and security controls it connects to," allowing teams to "easily shave 50, 75, 80% of the work."

**On Attack Detection:**

Williams emphasized ADR detects "the root cause of application and API attacks" rather than just "suspicious inputs," using SQL injection as an example.

**On Software Complexity:**

He argued: "Software is the most complex thing mankind has ever created, and it's barely instrumented at all."

**On DevSecOps Organizational Challenges:**

Williams noted that "RASP was designed to sell to AppSec teams, but that creates problems" because operations teams reject it — ADR instead "speaks the language of operations."

**On Security Philosophy:**

He asserted that "none of what anybody in security does matters unless it's contributing to assurance," contrasting proactive design with reactive risk management.

**On Testing Strategy:**

Williams advocated shifting "to where it's most effective, cheap and accurate to do the test," noting that "QA environments are never accurate."

---

## 6. TechRound Interview — Meet Jeff Williams, CTO at Contrast Security

**Source:** https://techround.co.uk/interviews/meet-jeff-williams-cto-and-co-founder-at-software-security-company-contrast-security/
**Topics:** Developer challenges, platform approach, AppSec strategy, business impact

---

### Key Statements from Jeff Williams

**On the Company's Mission:**

Williams explains that Contrast Security modernizes application security by unifying security and development teams with one DevSecOps platform across the entire software development life cycle.

**On Developer Challenges:**

"Developers are measured on the amount of code they write and the speed at which they release it. When it comes to security, legacy application security approaches leave them at the behest of application security experts."

**On Application Security Strategy:**

Williams emphasizes that organizations need "a different approach to application security that operates from the inside out. Traditional outside-in security approaches cannot scale to meet the demands of modern software development."

**On Business Impact of Vulnerabilities:**

He notes that 39% of data breaches involve application vulnerabilities, and organizations reducing vulnerabilities can reduce risk by 1.7x.

**Platform Performance Metrics:**

The Contrast platform delivers results including 17x faster mean time to remediate, 10x faster scans, up to 95% fewer false positives, and dramatically lower application risk.

**On Future Direction:**

Contrast recently released Contrast Scan, which offers pipeline-native SAST with 10x faster scans and 30% improved efficiency while enabling compliance with industry standards and corporate security policies.

---

## 7. Code Patrol Podcast — OMB M-22-18 Secure Software Development Compliance (2022)

**Source:** https://www.contrastsecurity.com/security-influencers/secure-software-development-compliance-for-ombs-m-22-18-memo-code-patrol-podcast-contrast-security
**Mirror:** https://securityboulevard.com/2022/11/secure-software-development-compliance-for-ombs-m-22-18-memo-code-patrol-podcast-contrast-security/
**Topics:** Federal software transparency requirements, NIST SSDF, OMB memo compliance

---

### Key Statements from Jeff Williams

**On Security Transparency:**

Williams contends that most software producers cannot meet the transparency standards set by the M-22-18 memo. His position emphasizes that security documentation helps government and consumers, not attackers.

Regarding security transparency, Williams states: "Having information about how the software was developed doesn't help an attacker" and notes that hackers can analyze code directly to identify libraries regardless of published documentation.

**On the Memo's Requirements:**

The memo (released September 14, 2022) mandates that software producers disclose their development practices. Software companies have 270 days (critical software) or 365 days (other software) to complete self-assessment forms. Requirements align with NIST's Secure Software Development Framework (SSDF). Documentation must cover developer training, development lifecycle practices, testing methods, and vulnerability management.

**Core Message:**

Companies unable to transparently document their secure practices must implement significant changes within six months. Organizations should audit compliance against SSDF requirements immediately.

**Practical Guidance:**

Already-compliant firms need only document existing practices. Non-compliant organizations should begin remediation immediately rather than waiting for deadline pressure.

---

## 8. Code Patrol Podcast — Software Transparency with NIST Fellow Ron Ross (2022)

**Source:** https://www.contrastsecurity.com/security-influencers/software-transparency-code-patrol-podcast-contrast-security
**Participants:** Jeff Williams (Co-Founder & CTO, Contrast Security), Dr. Ron Ross (NIST Fellow)
**Topics:** Software assurance, transparency, risk-based decision making, traceability

---

### Key Statements from Jeff Williams

**On Risk-Based Decision Making:**

Williams emphasizes that "senior security leaders need to make risk-based decisions" but identifies a critical problem: "What kind of information are senior leaders using to make those decisions?" He notes there is "a real lack of transparency."

**On the "Water Line" Metaphor:**

He uses a distinction between "above the water line" and "below the water line." Engineering elements like "software, hardware, systems, firmware" comprise the visible layer. The hidden layer concerns how trustworthy systems actually are.

**On Assurance's Role:**

Williams stresses that "assurance becomes critically important" for engineering trustworthy systems.

**On Lost Traceability:**

A significant observation: "We've completely lost" the traceability standards that existed in earlier security frameworks, where clear connections linked "threat all the way through requirements, high-level specs, and down into implementation."

**On Vendor Claims Requiring Evidence:**

Williams advocates that claims require supporting evidence: "For each threat, there should be controls. For each control, there must be evidence." This creates logical argumentation currently absent in industry practice.

---

## 9. Contrast Security Blog — How ADR Fixes AppSec in Production (2024)

**Source:** https://www.contrastsecurity.com/security-influencers/contrast-security-founder-jeff-williams-explains-how-to-fix-appsec-in-production-adr
**Author:** Jeff Williams, Co-Founder, Chief Technology Officer
**Publication Date:** August 13, 2024 (Last Modified: August 21, 2024)
**Context:** Written following Black Hat interview with Alan Shimel (TechStrong TV) and Katie Norton (IDC Research Director)

---

### Full Article Text

One of the most memorable parts of Black Hat was an interview with Alan Shimel of TechStrong TV and Katie Norton, Research Director at IDC. We had a wide-ranging discussion about the state of AppSec and DevSecOps. The segment provided a great opportunity to talk about the deficiencies in these current approaches to Application Security (AppSec) and how our new Application Detection and Response (ADR) model offers a path to better security for applications and application programming interfaces (APIs). I encourage you to watch the interview. I've also provided a summary below.

**AppSec Isn't Working in Production:**

We agreed that DevSecOps and AppSec were not functioning in production environments. All they're doing is producing huge backlogs of vulnerabilities in development. According to a Ponemon study, the average organization has a backlog of 1.1 million vulnerabilities. But most organizations don't have any visibility into attacks or a way to prevent those vulnerabilities from being exploited.

What's arguably worse is that DevSecOps and AppSec don't do much to protect software that's in production. People really don't have visibility into what's going on in production in their apps and APIs from a security perspective. They don't see attacks.

The irony here is that DevSecOps was meant to break down barriers between teams and processes, but in many critical ways, it has simply created new silos in Dev and Ops. This has to do with the way the tools work. They create silos because they produce backlogs that nobody wants to touch. It's like, "Here, let that group over there manage this giant pile of stuff." That's not a good way to bring people together.

The fact that DevSecOps often wants developers to function like security professionals further compounds this problem. Likewise, security pros are never going to be developers. We need to find ways to empower everyone to deal with application and API incidents that happen in production.

**Filling the Gaps with ADR:**

We officially announced Contrast ADR at Black Hat. ADR is exactly what you think: Just like endpoint detection and response (EDR), cloud detection and response (CDR), network detection and response (NDR) and the rest of the extended detection and response (XDR) ecosystem, you install ADR on your application and API servers, and it detects incidents, reports to Operations and intervenes to prevent exploits. ADR fills in these various security gaps at the application layer and integrates right into the existing XDR, security information and event management (SIEM) and cloud-native application protection platform (CNAPP) ecosystem. This includes both applications and APIs. When an ADR solution sees an attack, it can share telemetry about it — as well as the full context — with the security operations center (SOC) team; security orchestration, automation and response (SOAR) platforms; and so forth.

**ADR Brings Development and Operations Together with Context:**

Katie Norton had an important observation about the "context" needed to interpret and measure both vulnerabilities and attacks. There's a huge chasm between what developers see and what's happening in the SOC. For instance, how do these two groups come together to prioritize vulnerabilities for remediation, when developers can't see threats and attacks? And Operations staff can't understand what application and API workloads do or where they are vulnerable. Enter ADR: By providing the full production context to both development and operations, ADR is a huge lever that needs to be pulled in the larger prioritization problem. You can't prioritize what you need to do with just code context, so we leverage production security observability. This provides the full risk context to developers as well as keeping Operations aware of potential danger areas.

**API Security Is Just AppSec:**

Our discussion veered off into a relevant tangent involving the differences between AppSec and API security. Security professionals have been told to treat API security as separate and different from AppSec, but isn't it really the same? The three of us came to a consensus that an API is simply another piece of software and libraries that requires security testing, detection and response. You don't need a bunch of separate tools doing essentially the same thing.

Katie Norton had a distinctive take on this question, which is that API protection has mostly been on the production side of things. The problem is that you can't understand the code part from the production. Web application firewalls (WAFs) give you telemetry about API traffic, which comprises a lot of network traffic these days. But WAFs don't show you much about the API code.

**Translating to Make DevSecOps Work:**

How do you close this chasm? ADR offers a solution. It bridges the gap by essentially serving as a translator. For instance, operations teams generally don't talk about vulnerabilities, remediation and backlog. Developers don't talk about SIEM events and SOAR playbooks. The goal with ADR was to create software that understands how to speak both languages and provide the data that people need to get their jobs done, regardless of their role. In this, the accuracy of the data is critical. With good quality data, everyone can work together to make DevSecOps work better.

**Conclusion:**

ADR is new, and we have just started to engage with customers on putting it to work for AppSec. Everyone we've spoken to has recognized the need for it. The gaps, the silos, the lack of visibility — these are real issues that security professionals, developers and Operations need to solve. ADR solves these problems by providing data about attacks occurring in production and sharing enriched alerts with the SOC team and other critical stakeholders.

---

## 10. Contrast Security Blog — Shift Smart Instead of Following Shift-Left Fairy Tales (2023)

**Source:** https://www.contrastsecurity.com/security-influencers/shift-smart-instead-of-following-shift-left-fairy-tales-application-security-appsec-contrast-security
**Author:** Lisa Vaas (interviewing/quoting Jeff Williams), Senior Content Marketing Manager, Contrast Security
**Published:** May 24, 2023
**Topics:** Shift-left mythology, Shift Smart framework, security testing philosophy

---

### Jeff Williams' Core Arguments

**Challenging the "100 Times Less Expensive" Statistic:**

Jeff Williams, Contrast Security co-founder and CTO, challenges the foundational claim supporting shift-left doctrine. According to Williams, the frequently cited statistic that fixing vulnerabilities earlier in the development cycle costs "100 times less" than fixing them in production likely originated from an internal training chart without supporting data, later cited in a book, and subsequently repeated by others.

Williams writes: "It was included in a chart figure that was used for internal training without any available supporting data before eventually being quoted in a book. Everybody then started citing the book."

**Problems with Blind Shift-Left Implementation:**

Williams identifies several issues with unquestioning adherence to shift-left:
- Developers often lack necessary tools and expertise for security testing
- Questionable whether shift-left actually reduces vulnerabilities
- Uncertainty about optimal timing: "Should we shift into the automated build pipeline where quality tests are run, or should we shift even further left into the integrated development environment (IDE)? Can we shift too far?"

Later studies found that bug remediation costs remain relatively consistent regardless of when fixes occur.

**The "Shift Smart" Alternative:**

Rather than blindly pushing security left, Williams advocates for strategic, context-aware testing. He emphasizes: "Rather than blindly shifting left or blindly shifting everywhere, organizations should shift smart. One key factor is to perform security testing only when you have enough 'context' — the details of how an application or API actually functions — to accurately identify real, exploitable vulnerabilities."

**Five Shift-Smart Principles (from Forbes Technology Council series):**

1. Harden your software stack
2. Test what matters when it matters
3. Test with the best
4. "Notify left"
5. Optimize for learning

**Key Insight:**

The article emphasizes that effective security requires thoughtful placement of testing activities throughout the SDLC, not automatic leftward shifts. A podcast discussion with Chris Hughes (CISO and Co-Founder of Aquia) stresses that "shift smart isn't about shoving a Sec tool into a DevOps pipeline," but rather transforming how security work is approached by breaking down monolithic tasks like penetration testing into manageable components.

---

## 11. Contrast Security Blog — Zero Trust for Application Security (2023)

**Source:** https://www.contrastsecurity.com/security-influencers/zero-trust-table-of-how-contrast-maps
**Author:** Jeff Williams, Co-Founder, Chief Technology Officer
**Published:** September 7, 2023
**Topics:** Zero trust model, perimeter security obsolescence, CISA Zero Trust Maturity Model

---

### Key Statements and Arguments

**Core Argument — The Perimeter Has Disappeared:**

Jeff Williams contends that traditional perimeter-based cybersecurity is obsolete. Modern enterprises operate across distributed cloud environments, APIs, microservices, and containers — making it impossible to defend with conventional boundary-based security.

He states: "The perimeter has disappeared" in contemporary enterprise architecture, requiring organizations to adopt zero-trust models where "everything is assumed to be accessible via the public internet."

Williams emphasizes that "data is the goal of hackers today," not networks or devices themselves. He notes that familiar AppSec solutions merely report problems without providing protective capabilities.

**Zero Trust Implementation:**

Williams identifies application security as the fourth pillar of CISA's Zero Trust Maturity Model. He outlines eight specific areas where Contrast supports this pillar:

- **Application Access**: Preventing vulnerability exploitation that bypasses controls
- **Threat Protections**: Addressing known and unknown vulnerabilities
- **Public Applications**: Protecting internet-facing systems
- **Secure Development**: CI/CD pipeline integration
- **Security Testing**: Continuous vulnerability detection
- **Visibility**: Analytics and compliance reporting
- **Automation**: Parallel processing across thousands of applications
- **Governance**: Portfolio-wide policy enforcement

**Transition Strategy:**

Williams recommends incremental adoption, following Edward Amoroso's framework: "explode" monolithic systems, "offload" to cloud, then "reload" with modern protections.

He advocates starting small: pilot projects, team assembly, and gradual standardization across the organization.

---

## 12. Contrast Security Blog — Smarter AppSec: ADR, Secure by Design & Shift Smart (2024)

**Source:** https://www.contrastsecurity.com/security-influencers/smarter-appsec-how-adr-secure-by-design-and-shift-smart-are-redefining-cybersecurity-application-security-podcast-takeaways-contrast-security
**Context:** Written summary of Jeff Williams' appearance on the Application Security Podcast (September 2024)
**Topics:** ADR, secure by design, shift smart, assurance philosophy

---

### Key Statements from Jeff Williams

**On ADR's Origins:**

Williams explained that pen testing and threat modeling are "highly time-pressured" because "every time you start pen testing and threat modeling with a new application, you have to learn everything from scratch."

**On Security Blueprints:**

He stated that ADR generates detailed application maps showing "all the endpoints and security controls it connects to," allowing teams to "easily shave 50, 75, 80% of the work."

**On Attack Detection:**

Williams emphasized ADR detects "the root cause of application and API attacks" rather than just "suspicious inputs," using SQL injection as an example.

**On Software Complexity:**

He argued: "Software is the most complex thing mankind has ever created, and it's barely instrumented at all."

**On DevSecOps:**

Williams noted that "RASP was designed to sell to AppSec teams, but that creates problems" because operations teams reject it — ADR instead "speaks the language of operations."

**On Security Philosophy — Assurance as the Ultimate Metric:**

He asserted that "none of what anybody in security does matters unless it's contributing to assurance," contrasting proactive design with reactive risk management.

**On Testing Strategy:**

Williams advocated shifting "to where it's most effective, cheap and accurate to do the test," noting that "QA environments are never accurate."

---

## 13. Cybersecurity Insights — Contrast CTO Jeff Williams (November 2022)

**Source:** https://www.contrastsecurity.com/security-influencers/cybersecurity-insights-with-contrast-co-founder-and-cto-jeff-williams-11/18
**Published:** November 18, 2022
**Format:** Short insights column (three key observations)

---

### Jeff Williams' Three Cybersecurity Insights

**Insight #1 — Federal Security Requirements:**

"Feds continue to push aggressive timelines for requiring app/API security attestations from software vendors. OMB 22-18 is the latest and it requires all software vendors to publish a statement disclosing how they ensure their applications are secure by October 2023."

**Insight #2 — SBOM Deployment Challenges:**

"Organizations are running into challenges deploying SBOMs as they discover that what's in their code repos doesn't match what's in their running applications. Focusing on libraries that actually load into memory and execute in production is the key to solving this problem."

**Insight #3 — Open Source Binary Repository Risks:**

"Did you know that an executable open source library in a binary repository like Maven Central doesn't have to match the source code in a source code repository like GitHub? There aren't any checks and it could be completely different… just thought you should know."

---

## 14. CyberScoop Federal — Making Applications More Secure at Federal Agencies (2015)

**Source:** https://cyberscoop.com/radio/jeff-williams-on-making-applications-more-secure-at-federal-agencies/
**Date:** September 30, 2015
**Host:** Kevin Greene
**Topics:** Formalizing application security practices at federal agencies, application security vulnerabilities
**Note:** Transcript not available on the page (audio-only format). Episode metadata only.

---

### Episode Metadata

- **Title:** Jeff Williams on making applications more secure at federal agencies
- **Guest:** Jeff Williams, CTO of Contrast Security
- **Host:** Kevin Greene
- **Topics covered:** How to formalize application security practices at federal agencies; application security vulnerabilities in government systems

---

## 15. DevOps Chat — AppSec and DevSecOps (DevOps.com) — Summary

**Source:** https://devops.com/devops-chat-appsec-and-devsecops-with-contrast-securitys-jeff-williams/
**Note:** Page returned 403 Forbidden. Content recovered from search engine snippets.
**Topics:** DevSecOps, WAFs, organizational transformation

---

### Key Statements from Jeff Williams (recovered from search excerpts)

**On WAFs:**

When asked if WAFs have changed the game, Williams responded skeptically: "Not really. I don't think so."

**On DevSecOps:**

"To me, DevSecOps is a way of viewing security the way that folks viewed software development through a DevOps lens."

**On DevOps' Transformative Potential:**

"Done right, I think DevOps can have a tremendously transformative effect on organizations building software. I've seen it in a bunch of large enterprises and small companies, you know, and we're a DevOps shop here at Contrast as well. You know, we're deploying six, seven times a day, and I have a huge amount of confidence that that makes us deliver much better software."

**On the OWASP Top 10:**

"I wrote this thing that I called the OWASP Top 10 and it was a little side project, I put it out there and it just went crazy. People started downloading it, OWASP got slashdotted and then a little while later they asked me to take over as a global chair of OWASP."

**On Enterprise Security Requirements:**

"I think the game's changed. It's become an environment where you have to be secure to sell to these big enterprises."

---

## 16. DevOps Chat — Shifting Security Left and Right (Security Boulevard 2019) — Summary

**Source:** https://securityboulevard.com/2019/10/devops-chat-shifting-security-left-and-right-with-contrast-security/
**Audio:** https://soundcloud.com/devopschat/shifting-security-right-and-left-w-jeff-williams-contrast-security
**Date:** October 2019
**Note:** Page returned 403 Forbidden. Content recovered from search engine snippets and related sources.
**Topics:** Shift left, shift right, Shift Smart concept

---

### Key Statements from Jeff Williams (recovered from search excerpts)

**On "Shift Left" as a Flawed Concept:**

Williams described the shift-left concept as "dumb, and dangerous" when applied without proper consideration, advocating instead for "extending left and extending right."

**On the "Shift Smart" Alternative:**

Rather than following shift-left orthodoxy, Williams advocated for doing "security at the point in the software development process when it makes the most sense, rather than following a one-size-fits-all shift-left approach."

**On Contrast Security's Approach:**

Contrast Security takes "a radically different approach to application security that's compatible with DevOps processes, finding vulnerabilities to enable shifting left in development, analyzing open source code, and protecting applications in production."

---

## Additional Sources & Context

### Jeff Williams' Profile Summary (from Infosecurity Magazine)

- **Position:** Co-founder and Chief Technology Officer at Contrast Security
- **Education:** BA from University of Virginia; MA from George Mason University; JD from Georgetown University
- **Background:** Over 20 years of security leadership experience
- **OWASP Leadership:** Founder and major contributor; served as OWASP Global Chairman for 9 years
- **OWASP Projects Created:** OWASP Top 10, Enterprise Security API, Application Security Verification Standard, XSS Prevention Cheat Sheet
- **Speaking:** Frequent speaker at JavaOne, BlackHat, QCon, RSA, OWASP, Velocity, PivotalOne
- **Writing:** Authored DZone refcards on DevSecOps, IAST, and RASP

### Additional Interview References Not Fully Scraped

- **Secure Talk Podcast (January 2023):** Topics included serverless technology, self-protecting security, Function as a Service (FaaS) for security applications
  - URL: https://securetalkpodcast.com/new-approaches-for-application-security-with-jeff-williams-co-founder-of-contrast-security/
- **20MinuteLeaders Podcast (May 2, 2022):** General leadership and career interview
- **FedScoop Video Interview (September 9, 2022):** "Contrast Security says although providers manage the security around the cloud, there is still a gap in securing applications."
  - URL: https://fedscoop.com/video/contrast-securitys-jeff-williams-discusses-challenges-in-application-security/
- **Dark Reading Author Profile:** https://www.darkreading.com/author/jeff-williams (multiple articles, paywalled)
- **JAX London 2024 Speaker Profile:** https://jaxlondon.com/2024/speakers/jeff-williams/
- **Cybersecurity Excellence Awards Profile:** https://cybersecurity-excellence-awards.com/candidates/jeff-williams/
- **Dev Interrupted Podcast (LinearB):** "Automating AppSec with Contrast Security" — https://linearb.io/dev-interrupted/podcast/automating-appsec-with-contrast-security

---

## Key Themes Across All Sources

### 1. Inside-Out vs. Outside-In Security
Williams consistently argues that traditional SAST, DAST, and WAF tools operate "outside-in" — they lack context about how applications actually run. His alternative is "inside-out" security via instrumentation, where sensors live inside the running application and observe real behavior.

### 2. The Stagnation Problem
"The average web application has 26.7 security problems. That number hasn't changed in the last 20 years." Williams uses this data point repeatedly to argue that traditional approaches have failed.

### 3. Instrumentation as the Answer
Williams' core technical thesis: software instrumentation (the same technology used in application performance monitoring) can be applied to security. This enables: (a) IAST in development/testing, (b) RASP in production, (c) ADR for operations/SOC integration.

### 4. Shift Smart, Not Just Shift Left
Williams challenges the "shift left" orthodoxy, arguing it's based on dubious data and ignores that security testing requires runtime context that only exists when code is actually executing.

### 5. DevSecOps Redefined
"I think too often when people say the word DevSecOps, what they're really saying is that we should shove all the security work onto developers. That's not fair and it doesn't work." — Williams consistently reframes DevSecOps as transforming security work (not just dumping it on developers).

### 6. The Context Problem
SAST tools fail because they lack runtime context. WAFs fail because they lack code context. Only instrumentation provides both simultaneously. This "context" argument is Williams' unifying theoretical framework.

### 7. Assurance as the North Star
"None of what anybody in security does matters unless it's contributing to assurance." Williams frames all security activities as means to the end of demonstrable assurance, not compliance theater.

### 8. ADR — The Newest Evolution (2024)
Application Detection and Response (ADR) is Williams' latest concept, positioning Contrast's technology within the established XDR ecosystem vocabulary that SOC teams already understand and use.

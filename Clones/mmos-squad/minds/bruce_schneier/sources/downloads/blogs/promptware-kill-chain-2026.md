---
title: "The Promptware Kill Chain"
date: "2026-02-13"
publication: "Lawfare"
url: "https://www.schneier.com/essays/archives/2026/02/the-promptware-kill-chain.html"
authors: "Bruce Schneier, Oleg Brodt, Elad Feldman, Ben Nassi"
---

Attacks on generative AI and large language models represent a sophisticated threat that extends far beyond simple prompt injection vulnerabilities. The authors propose understanding these attacks as "promptware"—a distinct class of malware that follows a structured seven-stage kill chain. The seven stages are: Initial Access, Privilege Escalation (Jailbreaking), Reconnaissance, Persistence, Command and Control (C2), Lateral Movement, and Actions on Objective. The fundamental architectural problem is that LLMs process all input as a single, undifferentiated sequence of tokens, lacking boundaries distinguishing trusted instructions from untrusted data. The authors argue that prompt injection isn't something we can fix in current LLM technology, requiring an in-depth defensive strategy that assumes initial access will occur and focuses on breaking the chain at subsequent steps.

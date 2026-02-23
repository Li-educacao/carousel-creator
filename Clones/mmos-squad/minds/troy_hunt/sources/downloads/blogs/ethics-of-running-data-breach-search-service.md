# The Ethics of Running a Data Breach Search Service
**Date:** September 25, 2017
**Source:** https://www.troyhunt.com/the-ethics-of-running-a-data-breach-search-service/
**Category:** Ethics & Values

Troy Hunt explores the ethical considerations involved in operating Have I Been Pwned (HIBP), a publicly searchable data breach notification service. He addresses common criticisms and explains his design decisions.

## The Public Search Model

Hunt defends making HIBP publicly searchable, citing both user experience and practical benefits. "The immediacy of the response addresses a question that's clearly important to them at that very moment," he explains. The immediate feedback helps raise awareness about data breaches and password security practices.

However, Hunt acknowledges this creates privacy risks. People can search for others' email addresses to discover their involvement in specific breaches. To mitigate this, Hunt flags sensitive breaches—like Ashley Madison—and restricts public visibility, requiring email verification instead.

## Email Verification Challenges

Hunt rejects email-only verification as impractical for several reasons:

**User Experience Issues:** Waiting for email delivery eliminates the immediate feedback that makes HIBP valuable for press coverage, conference presentations, and public awareness campaigns.

**Technical and Financial Barriers:** Sending millions of emails monthly is prohibitively expensive. Hunt notes that "one day of traffic" from loading the Onliner Spambot dataset would cost approximately $3,000 monthly in email delivery fees alone. Even with SendGrid support, this remains a significant constraint. Additionally, email deliverability is inconsistent—legitimate notifications frequently land in spam folders due to abnormal sending patterns.

## Data Minimization Philosophy

Hunt refuses to retain email addresses without explicit consent. Many competing services function as marketing funnels, collecting addresses under the pretense of delivering results later. "The only time this happens is when the user explicitly opts in to the notification service," Hunt states. He criticizes services like Experian's dark web scan for burying consent in massive terms-of-service documents designed to build marketing lists.

## The API's Role

Hunt published an API enabling developers to integrate HIBP into their own applications. This supports legitimate security initiatives—such as checking user credentials during registration—but requires publicly searchable data. Hunt implemented rate limiting (one request per 1.5 seconds per IP) to prevent abuse, reducing capacity from 40,000 to 40 searches per minute from single IPs. While this stops malicious bulk searching, it occasionally impacts legitimate uses.

## Passwords Remain Protected

Hunt maintains his position against sharing passwords linked to email addresses, despite criticism. He launched the Pwned Passwords service instead, allowing people to search for compromised passwords separately without connecting them to specific accounts. His philosophy: "I cannot lose what I do not have."

## Judgment Calls on Sensitive Data

Hunt makes subjective decisions about which breaches warrant "sensitive" designation—requiring email verification for access. He initially didn't flag the Fur Affinity breach as sensitive until understanding the potential harm from public discovery. Similarly, he declined to load the Australian Red Cross Blood Service breach after securing deletion of all copies and confirming victim notification. He removed VTech data at parents' request to protect children's privacy.

## Opposition to Shady Practices

Hunt explicitly opposes monetizing breached data, whether through direct sales (like LeakedSource) or indirect incentivization. He refuses to purchase stolen data, believing "criminal incentivisation" through payment discourages actual security improvements. He also criticizes "ambulance chasing"—organizations promoting competing services while exploiting public breach discussions.

## No Commercialization

HIBP contains no advertisements, sponsorship requirements, paywalls, or hidden terms and conditions. Hunt's commercial security training and consulting are entirely separate from this service, with no cross-promotion on the HIBP website.

## Future Evolution

Hunt acknowledges HIBP will continue evolving. Past changes include sensitive breach flagging, API rate limiting, and removing public paste listings. He welcomes community feedback, recognizing he doesn't always get decisions correct initially but commits to improving the system's ethical balance over time.

---

Hunt positions HIBP as serving ethical security objectives—raising awareness and helping breach victims—rather than profit maximization. His design choices reflect tensions between accessibility, privacy protection, and practical constraints, with decisions guided by individual judgment calls rather than absolute rules.

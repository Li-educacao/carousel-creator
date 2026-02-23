# Interview: Troy Hunt on Fastmail Digital Citizen Podcast (Part 2)
**Date:** ~2019
**Source:** https://www.fastmail.com/digitalcitizen/upgrade-your-cyber-security-with-troy-hunt-part-2/
**Category:** Interview / Podcast
**Interviewer:** Ricardo Signes (Fastmail)

---

## Career Origin

**Q:** Did you start out interested in having a career in security or did you kind of get sucked in?

**Troy Hunt:** Started as a software developer around 1997. While running application architecture at Pfizer for Asia-Pacific, he encountered repetitive security issues in code. Rather than sending identical correction emails repeatedly, he created blog posts targeted at developers around 2007-2009. This casual approach unexpectedly launched his security career.

## Security Fundamentals

**Q:** What security fundamentals should everyone using the internet understand?

**Troy Hunt:** "It's less about the technology and more about the people and the usability and the way of thinking." He illustrates this through arbitrary password complexity requirements. When sites demand uppercase characters, users predictably capitalize the first letter, creating false confidence. He emphasizes understanding technical controls while recognizing how humans actually interact with them.

## Password Design Philosophy

**Q:** Is there agreement on password design guidance across services?

**Troy Hunt:** "There's not, and I don't think there should be." Different services require different approaches. He cites Netflix allowing four-character passwords due to remote control usability constraints. The goal involves balancing security against account takeover risks with practical user experience.

## On Eliminating Passwords

**Q:** Michael Faye from 1Password wants to eliminate passwords entirely.

**Troy Hunt:** "Passwords have something going for it that no other authentication method has ever been able to do yet, and it's simply that everybody understands how to use it." Alternative methods like passwordless email authentication create their own problems—delayed delivery, junk folders, wrong clients. Parents understand passwords; they don't understand U2F or cryptographic devices.

## Password Managers as Secret Managers

**Q:** Will password managers become essential for everyone?

**Troy Hunt:** Password managers should function as tools for managing all digital secrets, not just passwords. "It becomes a tool for managing secrets in your digital life." Uses include storing credit card information, auto-filling addresses, and sharing secrets through shared vaults. "Something that improves your security actually also improves your usability."

## Shared Responsibility

**Q:** What can non-developers do beyond password managers to improve security?

**Troy Hunt:** Security involves shared responsibility between system builders and users. Developers must lead people toward success; individuals must practice cyber hygiene—choosing strong unique passwords, enabling two-factor authentication, being conscious about information shared. Both parties bear responsibility.

## EV Certificates Critique

**Q:** Other ways system builders get things wrong?

**Troy Hunt:** Extended validation certificates create false trust signals. "None of this makes any sense whatsoever." Commercial imperatives and certificate authority financial interests distract from genuinely useful developer actions.

## Phishing Detection Difficulty

**Q:** Can users identify fake sites through URL inspection?

**Troy Hunt:** Traditional advice about misspelled URLs "simply doesn't hold water anymore." He describes a phishing SMS with a legitimate New Zealand pest control URL that redirects to phishing pages—how can users determine trustworthiness? Browser warnings provide better protection. "Even if I haven't sort of passed the test of being able to read the URL...the technology is saving me."

## Hack Yourself First Workshop

**Q:** About the "Hack Yourself First" workshops?

**Troy Hunt:** Workshops began in 2015, targeting primarily developers. "Let's help you break your own things first, hack yourself first so that you can see what attackers do." Covers approximately 16 modules over two days including SQL injection, cross-site scripting, and password hashing. Participants crack hashes themselves, experiencing why MD5 and salted SHA-1 fail. Examples from "Have I Been Pwned" illustrate real breach consequences.

## Teaching Impact

**Q:** Do workshops change thinking or simply provide tools for known problems?

**Troy Hunt:** Both occur. Learning SQL injection mechanics through direct observation—seeing concatenated queries executed unchecked—drives home parameterization importance. Default feedback questions assumptions; for instance, suggesting 12-character minimum passwords prompts discussions about customer experience and context-specific requirements.

---

## Key Cognitive Patterns Observed:
- **Pragmatic over dogmatic**: Different contexts need different solutions
- **Human-centric security**: Technology must serve human behavior, not the reverse
- **Teaching through experience**: "Hack yourself first" — experiential learning
- **Contrarian**: Challenges EV certificates, password rules, URL inspection advice
- **Balancer**: Security vs usability always weighed together

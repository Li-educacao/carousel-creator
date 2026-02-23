# A Sneaky Phish Just Grabbed my Mailchimp Mailing List
**Date:** March 25, 2025
**Source:** https://www.troyhunt.com/a-sneaky-phish-just-grabbed-my-mailchimp-mailing-list/
**Category:** Technical Deep-Dive

Troy Hunt, a prominent cybersecurity researcher, fell victim to a sophisticated phishing attack that compromised his Mailchimp account and resulted in the unauthorized export of approximately 16,000 email addresses from his blog's mailing list.

## The Attack

Hunt received a phishing email designed to appear as a legitimate Mailchimp notification about suspicious account activity. Despite being jet-lagged and fatigued, he clicked the link to `mailchimp-sso.com` and entered his credentials. Notably, "the credentials did not auto-complete from 1Password," but he proceeded anyway, thinking this wasn't unusual for legitimate services.

After entering a one-time password, the page froze. Within minutes, Hunt realized the breach and logged into the official Mailchimp site, confirming unauthorized access from a New York IP address. An alert indicated his mailing list had been exported moments before he could secure the account.

## Key Details

The exported data included approximately 16,000 subscriber records containing email addresses, subscription preferences, subscription dates, IP addresses, and geolocation information derived from IP addresses. Notably, the export included nearly 7,535 unsubscribed email addresses—nearly half the dataset.

Hunt immediately changed his password and discovered that an API key had been created on his account, which he subsequently deleted. The phishing domain was taken down by Cloudflare within 2 hours and 15 minutes.

## Lessons and Observations

Hunt identifies several factors that contributed to his compromise:

**Fatigue and Timing:** Jet lag significantly impaired his judgment. The attacker had no way to know this; the phishing simply timed perfectly with a moment of vulnerability.

**Well-Crafted Social Engineering:** The message created appropriate urgency without being over-the-top, psychologically nudging him toward immediate action.

**OTP's Limitations:** "Two-factor authentication via OTP is completely useless against an automated phishing attack that can relay the OTP as soon as it's entered." The attacker automated credential replay to the legitimate Mailchimp site.

**Email Address Targeting:** The phishing email reached an address used exclusively for Mailchimp signup. Hunt speculates the address came from a previous Mailchimp breach, possibly from their 2022 security incident, rather than being specifically targeted.

**Email Client Rendering:** Outlook on iOS didn't display the suspicious sender address, though the desktop version would have been more obvious.

## Technical Analysis

**Lack of Phishing-Resistant Authentication:** Mailchimp doesn't offer passkeys or hardware security keys as authentication options. Hunt notes the irony—he'd just met with the UK's National Cyber Security Centre to discuss passkey adoption the day before the attack.

**Authentication Session Length:** Mailchimp's short-lived authentication sessions meant Hunt expected to re-login frequently, normalizing the experience and removing a potential warning sign.

**Unsubscribed Data Retention:** Mailchimp retains unsubscribed email addresses ostensibly to prevent re-subscription through imports. The UK's Information Commissioner's Office guidance supports this practice for "suppression lists," but Hunt argues users should have explicit choice in how their data is handled. He proposes a model offering users options: permanent deletion, anonymization, or retention for suppression purposes.

**API Key Creation:** The attacker created an API key for persistent access. Deleting this key and resetting his password revoked unauthorized access.

## Response and Impact

Hunt loaded the breach data into his "Have I Been Pwned" database, notifying approximately 6,600 impacted subscribers and 2,400 monitoring domains. Mailchimp disabled login and sending capabilities during their investigation, then restored access after confirming the scope of unauthorized activity.

## Broader Implications

This incident reinforced Hunt's commitment to building `whynopasskeys.com`—a project to highlight major services lacking phishing-resistant authentication, similar to his earlier `whynohttps.com` initiative.

Hunt emphasizes transparency and speed in breach response, modeling the practices he advocates when organizations contact him about disclosures. He promises deeper technical analysis and continues dialogue with Mailchimp regarding passkey support and data handling policies.

Security researchers later attributed the attack to Scattered Spider, a sophisticated threat actor known for well-orchestrated phishing campaigns and social engineering.

# Processing 23 Billion Rows of ALIEN TXTBASE Stealer Logs
**Date:** February 26, 2025
**Source:** https://www.troyhunt.com/processing-23-billion-rows-of-alien-txtbase-stealer-logs/
**Category:** Technical Deep-Dive

Troy Hunt announced a significant expansion of Have I Been Pwned (HIBP) by ingesting approximately 1.5 terabytes of stealer logs known as "ALIEN TXTBASE." This corpus contains 23 billion rows representing 493 million unique website and email address combinations, affecting 284 million distinct email addresses.

## Key Developments

### Stealer Log Integration

The ALIEN TXTBASE dataset originated from a Telegram channel containing 744 files. Stealer logs are credentials harvested by information-stealing malware installed on victims' computers through various methods—pirated software, counterfeit installers, and malicious downloads. Once captured, these credentials are sold to cybercriminals who exploit victims a second time by accessing their accounts.

Hunt verified the data's authenticity through multiple methods, including Netflix password reset confirmations across different geographic regions and direct outreach to affected users, revealing the personal scope of exposure.

### New API Capabilities

Two domain-based APIs now enable organizations to query stealer logs:

1. Email domain queries allow organizations to identify compromised employee credentials
2. Website domain queries permit site operators to identify customers affected by stealer malware

These APIs require a Pwned 5 subscription, though the existing free web interface for individual email searches remains unchanged.

### Password Database Expansion

The initiative added 244 million previously unknown passwords to Pwned Passwords and updated counts for 199 million existing entries. This brings Pwned Passwords to over 10 billion monthly API requests, supporting password security across numerous platforms including Basecamp.

## Processing Infrastructure

Hunt detailed the technical challenges of reducing 23 billion rows to manageable datasets:

- Extracted 284 million unique email addresses from the full corpus
- Consolidated 744 files (390GB, 9.7 billion rows) into distinct domain-email pairs
- Identified 18 million unique domains
- Inserted 493 million new stealer log entries into the database

Local .NET processing proved significantly more efficient than cloud-based database solutions, demonstrating that "the cloud is not always the answer."

## Practical Impact

Organizations using HIBP now receive clearer breach notifications indicating how many email addresses appear against their website domains. Hunt highlighted adoption by companies like Basecamp, which now checks credentials against HIBP during login attempts, helping prevent account compromise.

The service enables defenders to identify malware infection patterns and implement protective measures before criminals exploit stolen credentials further.

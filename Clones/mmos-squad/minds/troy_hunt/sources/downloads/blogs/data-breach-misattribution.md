# Data Breach Misattribution, Acxiom & Live Ramp
**Date:** November 23, 2022
**Source:** https://www.troyhunt.com/data-breach-misattribution-acxiom-live-ramp/
**Category:** Methodology & Process

Troy Hunt investigates a massive 246-million-record dataset circulating in hacking forums that was misattributed to Acxiom and its former subsidiary LiveRamp. Hunt's analysis reveals significant issues with this attribution claim.

The data contains 51.7 million unique email addresses with over 410 columns of personal information. Hunt notes the dataset appears "too neat" with uniformly formatted names and addresses, suggesting "a very refined collection process or matched using a service."

Examining URLs in the dataset, Hunt identifies patterns pointing toward "dodgy online competitions" and data-harvesting websites. Examples include directeducationcenter.com and originalcruisegiveaway.com — sites offering prizes contingent on sharing personal information with "trusted partners and others."

The geographic analysis reveals suspicious gaps: "no California, the most populous state" and no Texas, despite a US-focused dataset. Additionally, Hunt finds one UK-based URL (quickquid.co.uk) amid predominantly American records, creating unexplained inconsistencies.

After directly contacting Acxiom, Hunt receives their forensic analysis concluding the data "does not come from Acxiom and is in no way the subject of an Acxiom breach." Hunt's own investigation supports this, finding "absolutely nothing within the data set itself to tie it back to them."

Responses from affected HIBP subscribers confirm mixed accuracy — some data correct, other fields demonstrably wrong or outdated. Hunt observes that 94% of email addresses already appear in previous breaches, suggesting "this corpus of data may be at least partially constructed from other data already in circulation."

Hunt emphasizes the importance of proper breach verification and warns against misattribution, which can unfairly damage organizations' reputations.

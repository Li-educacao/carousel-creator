# Here's how I verify data breaches
**Date:** May 7, 2016
**Source:** https://www.troyhunt.com/heres-how-i-verify-data-breaches/
**Category:** Methodology & Process

Troy Hunt discusses his methodology for verifying data breaches before publicizing them or adding them to Have I Been Pwned (HIBP). He begins by addressing sensationalist headlines claiming major email providers like Gmail and Hotmail had been compromised, explaining why such claims are unlikely to be accurate.

Hunt emphasizes that he verifies all breach data regardless of source. He illustrates this through two examples: the Zoosk incident and the Fling.com breach. The Zoosk data — 57 million records containing only email addresses and plain-text passwords — raised immediate red flags because it lacked internal identifiers, timestamps, and structural details that would confirm its authenticity.

By contrast, the Fling data included complete database schema information, MySQL dump headers, and comprehensive user attributes. This structure enabled both Hunt and the reporters involved to verify the breach's legitimacy.

Hunt describes several verification techniques:

**Mailinator Testing:** He uses disposable email addresses to test password reset functionality and confirm whether accounts exist in alleged breaches.

**HIBP Subscriber Verification:** Hunt contacts recently verified HIBP subscribers appearing in questionable datasets, requesting them to confirm whether exposed information matches their actual account details.

**Data Analysis:** He examines email domain distributions, top-level domains, and password prevalence patterns to identify anomalies suggesting fabrication or data aggregation from multiple sources.

**Organizational Confirmation:** Hunt reaches out to breached organizations, often through journalists, to obtain direct confirmation or denial of incidents.

Hunt explicitly rejects actually logging into accounts using breached credentials, stating this would violate ethical boundaries and potentially the Computer Fraud and Abuse Act.

The article concludes with the "Zoosk" breach case study: Mail.Ru determined that 99.982% of the allegedly compromised credentials were invalid, suggesting the dataset was largely fabricated or poorly compiled from unrelated sources.

Hunt argues that thorough breach verification prevents inaccurate reporting, unnecessary alarm, and potential damage to organizations wrongly implicated in security incidents.

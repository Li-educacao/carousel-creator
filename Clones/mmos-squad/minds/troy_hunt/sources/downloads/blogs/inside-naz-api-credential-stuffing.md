# Inside the Massive Naz.API Credential Stuffing List
**Date:** January 18, 2024
**Source:** https://www.troyhunt.com/inside-the-massive-naz-api-credential-stuffing-list/
**Category:** Technical Deep-Dive

Troy Hunt reports on a significant credential stuffing incident involving the Naz.API list, discovered through a bug bounty submission to a major tech company. This represents a substantial breach dataset requiring serious attention.

## Scale of the Incident

The dataset comprises remarkable proportions: "319 files totalling 104GB" containing approximately 71 million unique email addresses. Hunt identified 427,308 HIBP subscribers impacted by this breach. Notably, "65.03% of addresses already in HIBP" based on a random sample, meaning roughly one-third represents previously unknown data—a statistically significant finding.

## Data Sources

The collection combines two distinct sources: stealer logs from malware and traditional credential stuffing lists. Stealer logs capture website, username, and password combinations harvested from compromised computers. Hunt validated the data's authenticity through multiple methods, including account enumeration techniques on various websites and direct confirmation from affected users.

## Password Analysis

The dataset contained approximately 100 million unique passwords appearing 1.3 billion times collectively. This reveals problematic password reuse patterns across services and users. All passwords have been integrated into Pwned Passwords, the free k-anonymity API service that now processes over 7 billion monthly requests.

## Protective Measures

Hunt emphasizes that users employing password managers, strong unique passwords, and two-factor authentication remain unaffected by this incident. Services can protect against credential stuffing attacks by implementing Pwned Passwords verification, making this data ineffective for unauthorized access attempts.

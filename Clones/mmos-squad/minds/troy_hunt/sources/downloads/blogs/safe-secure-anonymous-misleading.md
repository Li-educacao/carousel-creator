# Safe, Secure, Anonymous, and Other Misleading Claims
**Date:** October 4, 2023
**Source:** https://www.troyhunt.com/safe-secure-anonymous-and-other-misleading-claims/
**Category:** Technical Deep-Dive

Troy Hunt examines how companies make bold promises about data protection that often fail to materialize. He illustrates this pattern through several high-profile breaches where organizations assured users of anonymity and security, only to have those guarantees shattered.

## The Shitexpress Example

Hunt begins with an unusual case study: Shitexpress, a service enabling users to mail actual feces to others. The company proclaimed "100% anonymous" operations. However, when the service suffered a data breach affecting 24,000 users, exposed information included email addresses, IP addresses, physical addresses, and personal messages. One user who sent multiple packages within 42 minutes was easily traced through their IP address and iPhone user agent data—hardly anonymous.

The breach revealed invoices with Stripe payment information, making credit card traceability inevitable. Hunt notes that basic business requirements—collecting payment and delivery details—inherently contradict anonymity claims.

## Pattern of Broken Promises

Hunt identifies a recurring pattern across multiple breaches:

- **Ashley Madison (2015):** The adultery platform promised discretion and offered a paid deletion service. That service failed to actually remove user data.

- **Vastaamo (Finnish therapy service):** The company assured patient privacy, yet exposed psychotherapy notes and personal identifying information. Perpetrators later ransomed individuals directly, threatening to publish sensitive therapy records.

## Core Argument

Hunt's central thesis states that "assurances of safety, security and anonymity aren't statements of fact, they're objectives, and they may not be achieved." He emphasizes that words on websites cannot guarantee data security—they represent intentions rather than guarantees.

The piece serves as a cautionary reference for future discussions about data protection claims, warning against placing trust in corporate security promises without verification of actual implementation.

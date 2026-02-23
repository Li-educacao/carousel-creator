# Telegram Combolists and 361M Email Addresses
**Date:** June 4, 2024
**Source:** https://www.troyhunt.com/telegram-combolists-and-361m-email-addresses/
**Category:** Technical Deep-Dive

A security researcher provided Troy Hunt with 122GB of data scraped from thousands of Telegram channels, containing 1.7 thousand files with 2 billion lines and 361 million unique email addresses. Of these, 151 million had never appeared in Have I Been Pwned (HIBP) before. The dataset included passwords and, in many cases, associated websites.

## What Are Combolists?

"Combolists" refers to combinations of email addresses or usernames paired with passwords. These lists circulate on Telegram channels and are often organized by email service provider. Attackers use them to conduct credential stuffing attacks—attempting to access accounts across multiple services en masse.

## Data Source and Verification

The data originated from 518 different Telegram channels across 1,748 separate files. Hunt verified the dataset's legitimacy through multiple approaches. He contacted existing HIBP subscribers who appeared in the breach and asked them to confirm whether the credentials matched their actual accounts.

Many confirmed the data was accurate. One subscriber noted: "The data seems accurate so far. I have already changed some of the passwords as I was notified by the provider that my account was hacked."

## Information Stealer Malware

Analysis suggests much of this data comes from info stealer malware—software capturing credentials as users enter them into websites on compromised machines. Hunt demonstrated this by cross-referencing entries against actual login pages (Nike, Footlocker, and others), confirming these email addresses had valid accounts.

## New vs. Recycled Data

Some credentials had appeared in previous breaches. However, many were entirely new to HIBP. One subscriber with 151 million new addresses represented a significant volume of previously unseen compromised data, particularly valuable for security monitoring.

## User Impact and Recommendations

Hunt emphasized that individuals found in this breach should follow cybersecurity fundamentals: keep devices patched, use security software, employ strong unique passwords with password managers, and enable two-factor authentication wherever possible.

He noted many affected users were not following these basics, with passwords consisting of predictable patterns including names, birth years, and common character substitutions—often within twelve characters in length.

## Ongoing Concern

The article concludes that this represents an ongoing security challenge. While Hunt does not continuously load endless credential lists into HIBP, he stresses that security posture remains a perpetual concern rather than a one-time consideration after appearing in a breach.

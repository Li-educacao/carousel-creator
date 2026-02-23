# Processing 630 Million More Pwned Passwords, Courtesy of the FBI
**Date:** December 13, 2025
**Source:** https://www.troyhunt.com/processing-630-million-more-pwned-passwords-courtesy-of-the-fbi/
**Category:** Technical Deep-Dive

Troy Hunt discusses a significant expansion of the "Have I Been Pwned" (HIBP) database, which now includes 630 million additional passwords obtained from FBI investigations.

## Background and Scale

The FBI has been partnering with Hunt for four years, regularly submitting passwords discovered during criminal investigations. Hunt emphasizes the difficulty in comprehending cybercrime's scope, noting that the service now handles "nearly 7 thousand" requests per second on average, with peaks reaching much higher volumes.

## Data Source and New Additions

The latest password corpus resulted from FBI seizures of devices belonging to a suspect. The data originated from multiple sources including open web platforms, Tor-based marketplaces, Telegram channels, and infostealer malware families.

Approximately 7.4% of the new passwords—about 46 million entries—were previously unknown to HIBP. Hunt notes this represents a meaningful addition, allowing the service to help organizations block these vulnerable passwords from future use.

## Implementation and Infrastructure

The expanded database is immediately searchable through HIBP's API. Users downloading the complete dataset offline can access the latest information through the Pwned Passwords Downloader tool.

Hunt acknowledges Cloudflare's support, crediting their "edge caching tech" for enabling rapid password queries globally. This infrastructure ensures data accessibility within milliseconds regardless of user location.

## Impact

The integration demonstrates the collaborative effort between law enforcement and cybersecurity professionals to combat credential abuse and account takeovers.

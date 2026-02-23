# How Spoutible's Leaky API Spurted out a Deluge of Personal Data
**Date:** February 5, 2024
**Source:** https://www.troyhunt.com/how-spoutibles-leaky-api-spurted-out-a-deluge-of-personal-data/
**Category:** Communication Style / Misc

Troy Hunt describes discovering a significant security vulnerability in Spoutible, a Twitter alternative platform that emerged following Elon Musk's acquisition of Twitter. Someone contacted Hunt with details about an enumerable API that exposed sensitive user data through a simple URL structure.

## The Initial Discovery

The vulnerable endpoint returned basic user information like usernames and bios, which Hunt expected. However, the API also exposed data that should never be publicly accessible:

The response included email addresses, IP addresses, phone numbers, and gender information—none of which users anticipated being accessible through the API.

## Critical Security Issues

**Password Hashes Exposed:** The API returned bcrypt-hashed passwords for every user. Hunt verified this was genuine by successfully cracking his own hash. He notes: "The Spoutible API enabled any user to retrieve the bcrypt hash of any other user's password." This represents a fundamental design failure, as password hashes should never be returned to any interface.

**Two-Factor Authentication Compromise:** The API exposed 2FA secrets (seeds used to generate one-time passwords), rendering 2FA completely ineffective for account protection. Additionally, 2FA backup codes were returned in bcrypted form, though Hunt demonstrates these could be cracked within minutes.

**Password Reset Token Exposure:** Most critically, the API exposed email codes (em_code) that function as password reset tokens. Hunt discovered these tokens allow immediate account takeover without any additional verification. After password reset, the system generates a new token—which was then immediately exposed in the API again.

## Design Flaws Enabling Abuse

The vulnerability was easily discoverable because the vulnerable API was called organically during normal platform use. When users browsed "Pods" (communities on Spoutible) and hovered over member profiles, the API automatically fetched all sensitive data. This meant legitimate users inadvertently accessed the exposed information simply by using the platform as designed.

Additional weaknesses included minimal password strength requirements (6-20 characters with no complexity checks) and lack of session invalidation or security notifications after password changes.

## Response and Resolution

Hunt responsibly disclosed the vulnerability to founder Christopher Bouzy. The timeline shows exceptional response speed:

- **February 4, 15:30:** Initial disclosure request
- **February 4, 18:31:** Full details provided
- **February 4, 19:48 or earlier:** API fixed
- **February 5, 01:28 or earlier:** Public announcement issued
- **February 5, 07:52:** Password reset tokens rotated

The revised API now returns approximately "80% less data" and only includes appropriate public information.

## Recommendations for Users

Hunt advises Spoutible users to:

1. Change their Spoutible password and any reused passwords elsewhere
2. Disable and re-enable 2FA to generate new secrets
3. Invalidate cross-posting keys on Mastodon and Bluesky if enabled
4. Recognize that email, IP address, phone numbers, and public profile data were exposed

The 207,000 exposed email addresses are now searchable in Have I Been Pwned, with affected subscribers notified.

## Context and Analysis

Hunt provides historical perspective, noting this represents one of the worst API design decisions he's encountered. While acknowledging that frameworks might automatically serialize all database attributes, he emphasizes the absence of security review before deployment and inadequate incident response features (no session visibility, no takeover notifications).

He credits Spoutible's rapid response and commends founder Christopher Bouzy's genuine concern about the incident, noting that data breach discoveries are especially personal for platform creators.

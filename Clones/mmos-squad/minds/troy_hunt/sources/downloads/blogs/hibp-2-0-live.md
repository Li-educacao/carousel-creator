# Have I Been Pwned 2.0 is Now Live!
**Date:** May 20, 2025
**Source:** https://www.troyhunt.com/have-i-been-pwned-2-0-is-now-live/
**Category:** Personal & Reflective

Troy Hunt announced the launch of the completely rebuilt Have I Been Pwned website after an extensive redesign effort that began in February 2024.

## Major Features

### The Search Function

The signature search interface now includes celebratory confetti animations for roughly half of all searches. According to Hunt, the service maintains "a bit playful" approach rather than employing fear-based messaging. Users who find their information in breaches receive a different response presented in a timeline format with breach summaries.

Username and phone number searches have been removed from the website, though API support remains. Hunt explained these searches created support overhead and parsing challenges while comprising only two historical incidents in the database.

### Dedicated Breach Pages

Each breach now has its own page with cleaner information display and targeted post-breach guidance. The service plans to enhance these pages with specific recommendations based on available security features like two-factor authentication or passkey support.

### Unified Dashboard

The new dashboard consolidates previously scattered features—sensitive breach notifications, API key management, domain searches, and stealer log viewing—into one centralized location requiring email verification.

### Domain Search Improvements

This feature received significant development attention with cleaner verified domain lists, client-side filtering by email address and breach recency, and completely rewritten domain ownership verification processes.

## Technical Infrastructure

The service continues running on Microsoft Azure with C# and .NET 9.0, alongside extensive Cloudflare integration. The frontend uses Bootstrap, SASS, and TypeScript.

Performance improvements include "28% reduction in page size and 31% fewer requests" compared to the previous version.

Hunt replaced Google's reCAPTCHA with Cloudflare's Turnstile anti-automation service, eliminating external tracking and maintaining privacy-first principles.

## New Additions

A merchandise store launched at merch.haveibeenpwned.com featuring items priced at cost with no profit margin for the service.

## Development Notes

Hunt extensively used ChatGPT throughout development, particularly for icon selection, scripting, and technical problem-solving, describing it as correct approximately "90% of the time."

The launch occurred early Sunday morning with minimal issues, followed by a dozen+ rapid releases addressing refinements within 48 hours.

# Closer to the Edge: Hyperscaling Have I Been Pwned with Cloudflare Workers and Caching
**Date:** November 21, 2024
**Source:** https://www.troyhunt.com/closer-to-the-edge-hyperscaling-have-i-been-pwned-with-cloudflare-workers-and-caching/
**Category:** Technical Deep-Dive

Troy Hunt describes a major infrastructure upgrade for Have I Been Pwned (HIBP), leveraging Cloudflare's edge network to cache searchable data globally. The initiative aims to dramatically improve performance, availability, and reduce operational costs.

## The Challenge

HIBP maintains over 14 billion breached accounts across approximately 5 billion unique email addresses. Previously, every search required a round-trip to Azure Functions in West US—a 24,000km journey for users in Australia—despite Cloudflare edge nodes existing much closer to them.

## The Solution: Edge Caching Architecture

Hunt explains that the searchable database reduces to roughly 16 million possible hash prefixes (using SHA-1 hashing of email addresses). This finite list becomes cacheable across Cloudflare's 330 global edge nodes.

The search process now works as follows:

1. User enters email address (example: test@example.com)
2. System generates SHA-1 hash and extracts six-character prefix
3. Cloudflare Worker checks cache for that prefix
4. If cached, return immediately; otherwise query origin and cache result
5. Return results to user

## Performance Improvements

The data shows dramatic benefits:

- **96% cache hit rates** at optimal performance levels
- **99% distance reduction** for data transit to users
- **Massive availability gains** through reduced infrastructure dependencies
- **Significant cost savings** on Azure Function executions and bandwidth

## The Caching Paradox

Hunt notes an uncomfortable trade-off: new breach data loads require complete cache flushes. When the Finsure breach loaded, cache hits dropped to zero, then required 20 hours to repopulate to 50% hit ratios.

He observes: "Flushing cache and suddenly sending all traffic to the origin doubles our cost. Waiting until we're back at 90% cache hit ratio literally increases those costs 10x when we flush."

## Remaining Limitations

API key validation still requires requests to reach the West US origin for Azure API Management (APIM) checks before serving cached results. Hunt suggests "Cloudflare building an API management product" would eliminate this latency bottleneck, though he acknowledges the significant infrastructure costs of distributing APIM across regions.

## Scale at the Edge

The Pwned Passwords service demonstrates edge caching's potential, handling over 10 billion requests monthly—approximately 17,000 requests per second during peak periods—almost entirely from Cloudflare's cache reserve, requiring minimal operational overhead.

# Ads Integration Service Architecture

**Version:** 1.0.0
**Created:** 2026-02-15
**Team Size:** 3-10 people
**Status:** MVP Phase (Facebook Ads)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [API Endpoints](#api-endpoints)
4. [Database Schema](#database-schema)
5. [Authentication & OAuth 2.0](#authentication--oauth-20)
6. [Webhook Handlers](#webhook-handlers)
7. [Integration Patterns](#integration-patterns)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [SDK/Library Consumers](#sdklibrary-consumers)
11. [Scalability & Performance](#scalability--performance)
12. [Error Handling & Monitoring](#error-handling--monitoring)
13. [Implementation Roadmap](#implementation-roadmap)

---

## System Overview

### Purpose
The Ads Integration Service is a centralized REST API that abstracts the complexity of managing advertising campaigns across Facebook Ads and Google Ads platforms. It provides a unified interface for campaign creation, ad management, conversion tracking, and analytics.

### Key Capabilities
- **Multi-Platform Support**: Facebook Ads Manager, Google Ads
- **Centralized Campaign Management**: Single API for campaign lifecycle
- **Conversion Tracking**: Unified event/conversion submission and attribution
- **Analytics Aggregation**: Cross-platform performance metrics
- **OAuth 2.0 Integration**: Secure authentication with Facebook & Google
- **Webhook Handling**: Real-time event processing for conversion pixels
- **Rate Limiting & Retry Logic**: Robust handling of platform API constraints
- **Job Queue System**: Async processing for long-running tasks

### Design Principles
1. **API-First**: REST endpoints are the primary interface
2. **Platform Abstraction**: Consumers shouldn't know platform-specific details
3. **Idempotency**: Requests can be safely retried
4. **Event-Driven**: Webhooks and async processing where possible
5. **Security by Default**: OAuth 2.0, RLS, encrypted secrets
6. **Horizontal Scalability**: Stateless services, external state (Supabase)

---

## Architecture Diagram

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CONSUMER APPLICATIONS                         │
│  (Estoque, RepairHub, Blog, Landing Pages, Custom Projects)         │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ REST API Calls (JWT Auth)
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              ADS INTEGRATION SERVICE (Node.js/Express)               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐             │
│  │  Auth Layer  │  │ API Routes   │  │ Webhook Server │             │
│  │  (JWT Verify)│  │ (CRUD Ops)   │  │ (Pixel Events) │             │
│  └──────────────┘  └──────────────┘  └────────────────┘             │
│                           │                    │                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │        SERVICE LAYER (Business Logic)                        │   │
│  │  ├─ Campaign Service                                         │   │
│  │  ├─ Conversion Service                                       │   │
│  │  ├─ Analytics Service                                        │   │
│  │  └─ Account Service                                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                           │                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │        PLATFORM ADAPTERS (Abstraction Layer)                │   │
│  │  ├─ Facebook Ads Manager Adapter                            │   │
│  │  ├─ Google Ads Adapter                                      │   │
│  │  ├─ Facebook Conversion API Adapter                         │   │
│  │  └─ Google Conversion (GTag) Adapter                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                           │                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │           INFRASTRUCTURE LAYER                               │   │
│  │  ├─ Job Queue (Bull + Redis)                                │   │
│  │  ├─ Cache Layer (Redis)                                     │   │
│  │  ├─ Rate Limiter                                            │   │
│  │  ├─ Retry Handler                                           │   │
│  │  └─ Monitoring & Logging                                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
             │                                    │
             ├─────────────┬─────────────┬───────┤
             ▼             ▼             ▼       ▼
        ┌─────────┐  ┌──────────┐  ┌────────┐ ┌─────────┐
        │Supabase │  │Facebook  │  │Google  │ │  Redis  │
        │(PostgreSQL)│  Ads API │  │Ads API │ │(Queue/  │
        │         │  │          │  │        │ │ Cache)  │
        └─────────┘  └──────────┘  └────────┘ └─────────┘
```

---

## API Endpoints

### Base URL
```
https://ads-api.railway.app/api/v1
```

### Authentication Header
```
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json
```

### Core Endpoints

**Campaign Management:**
- `POST /campaigns` - Create campaign
- `GET /campaigns/{id}` - Get campaign
- `GET /campaigns` - List campaigns
- `PATCH /campaigns/{id}` - Update campaign
- `DELETE /campaigns/{id}` - Delete campaign

**Ad Sets:**
- `POST /campaigns/{campaign_id}/ad-sets` - Create ad set
- `GET /campaigns/{campaign_id}/ad-sets` - List ad sets

**Conversions & Events:**
- `POST /conversions` - Record conversion (server-side)
- `GET /conversions` - Get conversion analytics
- `POST /webhooks/facebook/conversions` - Facebook webhook
- `POST /webhooks/google/events` - Google webhook

**Platform Accounts:**
- `POST /accounts/link` - Link ad account (OAuth callback)
- `GET /accounts` - List linked accounts
- `POST /accounts/{id}/refresh` - Refresh token

**Analytics:**
- `GET /analytics/campaigns` - Campaign analytics
- `GET /analytics/attribution` - Attribution report

**Health:**
- `GET /health` - Service health check
- `GET /admin/status` - Admin dashboard

---

## Database Schema (Supabase PostgreSQL)

### Tables
1. **platform_accounts** - Linked Facebook/Google ad accounts
2. **campaigns** - Ad campaigns
3. **ad_sets** - Ad sets within campaigns
4. **ads** - Individual ads
5. **conversions** - Conversion events
6. **events** - Pixel events (webhooks)
7. **webhooks** - Audit trail of webhooks received
8. **job_queue** - Bull queue storage
9. **api_keys** - API key management
10. **audit_logs** - User action audit trail

### Security
- **RLS Enabled + FORCED** on all tables
- Users can only see their own data
- Admins have elevated access
- Tokens encrypted with AES-256-GCM
- PII (email, phone) hashed before storage

---

## Authentication & OAuth 2.0

### Flow
1. User clicks "Link Facebook Ads Account" in Estoque
2. Redirect to `https://ads-api.railway.app/auth/facebook`
3. User logs into Facebook & grants permissions
4. Service exchanges authorization code for long-lived token
5. Store encrypted token in Supabase
6. Daily job refreshes tokens before expiration

### Token Management
- **Access Token**: Encrypted with AES-256-GCM before storage
- **Refresh Token**: Stored (nullable for Facebook)
- **Token Expiration**: Monitored, auto-refreshed daily
- **Scope**: `ads_management,pages_manage_ads,pages_read_user_id`

---

## Webhook Handlers

### Facebook Conversion API
- Endpoint: `POST /webhooks/facebook/conversions`
- Signature validation using `X-Hub-Signature-256` header
- Events queued for async processing
- Deduplication by event_id
- PII hashing before storage

### Google Analytics 4 (GA4)
- Endpoint: `POST /webhooks/google/events`
- Events queued for async processing
- User ID and client ID mapping

### Processing Pipeline
1. Receive webhook → validate signature → queue job
2. Async: deduplicate → hash PII → store in DB
3. Update analytics cache (Redis)
4. Emit real-time event for dashboards

---

## Integration Patterns

### Rate Limiting
- **Campaigns**: 10 requests/minute
- **Conversions**: 1,000 requests/minute
- **Analytics**: 100 requests/minute
- Adaptive backoff on 429 responses

### Retry Logic
- **Max Retries**: 3
- **Backoff**: Exponential (1s → 2s → 4s)
- **Jitter**: 10% random variance
- **Retryable**: 429, 503, 504, network errors

### Job Queue (Bull + Redis)
- **Queues**: conversions, sync_campaigns, update_analytics
- **Concurrency**: 5 for conversions, 2 for sync
- **Retries**: 3 attempts with exponential backoff
- **Monitoring**: Success rate, failure alerts

### Idempotency
- `Idempotency-Key` header for duplicate detection
- Cached response with 1-hour TTL
- Safe request replay for network failures

---

## Security Architecture

### API Key Management
- Generated as `ads_{hex_key}` with SHA256 hash
- Stored as hash only (irreversible)
- Validation on every request
- Last-used tracking for rotation

### Token Encryption
- Algorithm: AES-256-GCM (authenticated encryption)
- Key: Derived from master key with scrypt
- Random IV for each token
- Auth tag prevents tampering

### PII Protection
- Email, phone, first_name hashed with SHA256
- Lowercase + trim before hashing
- Stored only as hash in database
- GDPR-compliant

### Audit Logging
- All mutations (CREATE, UPDATE, DELETE) logged
- IP address, user agent captured
- Complete before/after state
- Retention: 1 year minimum

### Additional Security
- Helmet.js for secure headers
- CORS: Configurable origin whitelist
- Input sanitization (mongoSanitize, xss)
- Rate limiting per endpoint
- JWT expiration enforced

---

## Deployment Architecture

### Docker Setup
```dockerfile
FROM node:18-alpine
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Railway Deployment
- Auto-deployed on git push
- Health checks every 30 seconds
- Auto-restart on failure
- Environment variables managed by Railway

### Infrastructure
- **Database**: Supabase PostgreSQL (sa-east-1)
- **Cache**: Redis 7 (for queue, cache, rate limiting)
- **Queue**: Bull (powered by Redis)
- **Monitoring**: Prometheus + Sentry
- **Logging**: Winston (console, file, cloud)

### Environment Variables
```
NODE_ENV=production
PORT=3000
SERVICE_URL=https://ads-api.railway.app
FACEBOOK_APP_ID=...
FACEBOOK_APP_SECRET=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
JWT_SECRET=...
ENCRYPTION_MASTER_KEY=...
```

---

## SDK/Library Consumers

### npm Package
```bash
npm install @lawteck/ads-service-sdk
```

### React Hook Usage
```javascript
import { useCampaigns } from '@lawteck/ads-service-sdk/react';

const { campaigns, create, update, loading } = useCampaigns();
```

### Conversion Pixel
```html
<script async src="https://ads-api.railway.app/sdk/pixel.js"></script>
<script>
  AdsPixel.track('Purchase', {
    value: 149.99,
    currency: 'BRL'
  });
</script>
```

---

## Scalability & Performance

### Caching Strategy
- **Campaigns**: 5 min TTL
- **Analytics**: 10 min TTL
- **Platform accounts**: 1 hour TTL
- Cache invalidation on update

### Database Optimization
- Connection pooling (max 20)
- Strategic indexes on hot columns
- Pagination for large result sets
- Batch operations for bulk work

### Horizontal Scaling
- Stateless API design
- Load balancer (Railway/NGINX)
- Multiple worker processes
- Shared Redis for coordination

### Async Processing
- Bull queue for conversions, sync jobs
- Multi-threaded worker pool
- Cluster mode for multi-core CPUs
- Queue depth monitoring

---

## Error Handling & Monitoring

### Observability
- **Prometheus metrics**: Request duration, job status, conversion latency
- **Sentry integration**: Exception tracking and reporting
- **Winston logging**: Structured logs with multiple transports
- **Health endpoint**: Service status checks

### Metrics Collected
- HTTP request duration
- Job completion rates (success/failed)
- Conversion processing latency
- Queue depth
- Rate limit hits
- Active connections

---

## Implementation Roadmap

### Phase 1: MVP (Weeks 1-4) - Facebook Ads
- OAuth 2.0 integration
- Campaign CRUD
- Conversion tracking
- Analytics API
- Railway deployment

### Phase 2: Stabilization (Weeks 5-6)
- Rate limiting & retries
- Job queue system
- Webhook handlers
- Monitoring setup
- SDK release

### Phase 3: Google Ads (Weeks 7-10)
- Google OAuth 2.0
- Campaign management (parity)
- Conversion mapping
- Cross-platform analytics

### Phase 4: Advanced Features (Weeks 11-12)
- Multi-project support
- Team collaboration
- Budget optimization
- Custom attribution
- Data export

---

## Quick Start for Developers

### Local Setup
```bash
git clone https://github.com/lawteckeletronica/ads-integration-service.git
cd ads-integration-service
npm install
cp .env.example .env.local
docker-compose up -d
npm run migrate
npm run dev & npm run worker
```

### Test Endpoints
```bash
curl -X POST http://localhost:3000/api/v1/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","platform":"facebook","daily_budget":50,"currency":"BRL"}'
```

---

**Document Status**: Production-Ready Architecture
**Last Updated**: 2026-02-15
**Maintained by**: @architect (Aria)

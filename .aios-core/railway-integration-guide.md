# Railway Integration Guide

## Status
✅ **Validated & Ready** — 2026-02-15

## Credentials
```json
Token: 1abb9039-d8f9-4695-bfe8-5f3fd4cbd391
Endpoint: https://backboard.railway.com/graphql/v2
Workspace: lieducacao's Projects
```

## Projects
- **charming-sparkle** → `0a12cf14-8772-4a8a-80eb-d4296176bf1b`
- **N8N Li Educação** → `700b5347-0d2f-4d65-a09b-664ff48048f4`

## Quick API Test

```bash
python3 << 'EOF'
import json, urllib.request

token = "1abb9039-d8f9-4695-bfe8-5f3fd4cbd391"
url = "https://backboard.railway.com/graphql/v2"

query = '{ projects { edges { node { id name } } } }'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

req = urllib.request.Request(url, json.dumps({"query": query}).encode(), headers=headers)
with urllib.request.urlopen(req) as r:
    print(json.dumps(json.load(r), indent=2))
EOF
```

## Critical Notes
⚠️ **API requires User-Agent header** — Otherwise returns 403
⚠️ **Workspace token scope** — Can list projects, access project details, but some viewer queries may fail
⚠️ **Token never expires** — But regenerate if shared or compromised

## Usage for N8N Migration (Future)
When ready to migrate N8N workflows:
1. Query project `700b5347-0d2f-4d65-a09b-664ff48048f4` for services/environments
2. List N8N workflows via Railway services API
3. Document workflow structure
4. Map to AIOS task/workflow definitions

## Persistent Storage
- Local: `~/.railway/config.json`
- AIOS: `.aios-core/railway-config.json`

Both are auto-loaded in future @devops sessions.

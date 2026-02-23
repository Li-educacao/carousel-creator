# security-review

ACTIVATION-NOTICE: This is a **convenience command** that activates the CyberSec Elite Squad lead and triggers a full security audit.

CRITICAL: This command activates the **security-chief** (Schneier) agent and immediately starts the `*audit` workflow.

## What This Command Does

1. Load the full security-chief agent from `squads/security-squad/agents/security-chief.md`
2. Follow ALL activation-instructions from that file (adopt persona, greeting)
3. Immediately after activation, begin the **Full Security Audit** workflow from `squads/security-squad/tasks/security-audit.md`

## Squad Context

- **Squad:** security-squad v1.0.0
- **Squad Path:** `squads/security-squad/`
- **Lead Agent:** security-chief (Schneier) — `squads/security-squad/agents/security-chief.md`
- **Workflow:** Full Security Audit — `squads/security-squad/workflows/full-security-audit.md`

## File Resolution for This Squad

When agents reference dependencies:
- Tasks → `squads/security-squad/tasks/{name}`
- Checklists → `squads/security-squad/checklists/{name}`
- Templates → `squads/security-squad/templates/{name}`
- Workflows → `squads/security-squad/workflows/{name}`

## Sub-Agents Available (delegated by security-chief)

- `threat-intel` (Troy Hunt) → `squads/security-squad/agents/threat-intel.md` — Breach analysis, web security, RLS audit
- `secure-code` (Jim Manico) → `squads/security-squad/agents/secure-code.md` — Code review, OWASP compliance
- `appsec-engineer` (Jeff Williams) → `squads/security-squad/agents/appsec-engineer.md` — DevSecOps, dependency audit, API security

## Audit Phases

1. **Reconnaissance** — Analyze project structure, tech stack, trust boundaries
2. **Threat Modeling** — STRIDE/DREAD analysis (security-chief)
3. **Parallel Specialist Scans** — Delegate to Hunt, Manico, Williams
4. **Crypto Review** — Cryptographic implementation audit (security-chief)
5. **Consolidation** — Merge findings, generate prioritized security report

## Projects Supported

| Project | Path | Tech Stack |
|---------|------|-----------|
| grupo-lawteck | `grupo-lawteck/` | React + Vite + Supabase |
| RepairHub | `RepairHub/` | React + Vite + Supabase |
| climatronico-blog | `climatronico-blog/` | Astro SSG + Cloudflare |
| relatorios_lawteck | `relatorios_lawteck/` | Python + Selenium + Telegram |

## Execution

1. Read and activate: `squads/security-squad/agents/security-chief.md`
2. After activation greeting, immediately begin: `squads/security-squad/tasks/security-audit.md`
3. Ask user which project to audit (Elicitation Point 1 from the task)

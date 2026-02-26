# Session: Carousel Creator Full Implementation (2026-02-26)

## What was done
- Full implementation of the Carousel Creator project for @lawhander Instagram (125k followers, Climatrônico brand)
- 5 Epics completed across all layers (backend, frontend, database, AI integration)
- PRD created at docs/prd/carousel-creator-prd.md
- Monorepo at carousel-creator/ with apps/api, apps/web, packages/shared

## Epics Completed
1. **Foundation & Infrastructure** — Monorepo setup, Supabase schema (5 tables + RLS), Auth middleware, Design system tokens, MADE Tommy fonts
2. **Text Generation Pipeline** — Gemini API integration with structured output, persona system, 4 carousel templates (educational, social_proof, tips_list, cover_cta), inline text editing
3. **Image Rendering Engine** — Node Canvas server-side rendering (1080x1080, 1080x1350), MADE Tommy font registration, Supabase Storage upload
4. **Learning Loop** — Feedback storage, few-shot prompt enrichment (threshold: 20 corrections), priority-based example selection, stats dashboard
5. **Polish, Export & Dashboard** — Layout with sidebar nav, Toast notifications, Templates page, Export (JSON + ZIP), Dashboard with filters/search/pagination

## Commits
- `14525d3` feat: add Carousel Creator project (Epics 1-4 complete)
- `5238d71` feat: add Epic 5 — Polish, Export & Dashboard enhancements

## Database
- Migration applied to Supabase project qpfhircjexgbuolobqkf (shared with Grupo Lawteck)
- Tables: carousel_templates, carousels, carousel_slides, carousel_feedback, writing_personas
- RLS enabled + forced, anon revoked (standard 3-layer pattern)
- 4 default templates seeded

## Pending for Production
1. **GEMINI_API_KEY** — generate at https://aistudio.google.com/apikey
2. **Supabase Storage** — create `carousel-assets` bucket in dashboard
3. **Create auth user** — via Supabase Auth for login
4. **Font license** — MADE Tommy downloaded as "Personal Use", needs commercial license for Instagram content

## Tech Stack
- Frontend: React 19 + Vite 6 + TypeScript + TailwindCSS
- Backend: Express + TypeScript (port 3001)
- LLM: Google Gemini API (@google/generative-ai)
- Image: Node Canvas + Sharp
- Database: Supabase (PostgreSQL + Auth + Storage)

## Design Tokens
- Colors: #010101, #FFFFFF, #76777A, #0084C8, #0E4C93
- Fonts: MADE Tommy ExtraBold/Medium/Regular
- Formats: 1080x1080 (square), 1080x1350 (portrait 4:5)

## Key Files
- PRD: docs/prd/carousel-creator-prd.md
- Local CLAUDE.md: carousel-creator/.claude/CLAUDE.md
- Migration: carousel-creator/supabase/migrations/20260226130000_initial_schema.sql
- Epic tracking: docs/stories/carousel-creator-epic1.md

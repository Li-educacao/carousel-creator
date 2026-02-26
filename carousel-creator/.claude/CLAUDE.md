# Carousel Creator

## Overview
Instagram carousel creator for @lawhander (Climatronico). Generates text via Gemini AI, validates with user, renders images following brand design system.

## Tech Stack
- Frontend: React 19 + Vite 6 + TypeScript + TailwindCSS + Radix UI
- Backend: Express + TypeScript
- LLM: Google Gemini API
- Database: Supabase (PostgreSQL + Auth + Storage)
- Image: Node Canvas + Sharp

## Commands
- `npm run dev` — Start all (api + web)
- `npm run dev:api` — Start API only
- `npm run dev:web` — Start frontend only
- `npm run build` — Build all
- `npm run lint` — Lint all

## Design Tokens
- Colors: #010101 (black), #FFFFFF (white), #76777A (gray), #0084C8 (blue), #0E4C93 (blue-dark)
- Fonts: MADE Tommy ExtraBold (headings), Medium (subtitles), Regular (body)
- Slide formats: 1080x1080 (square), 1080x1350 (portrait 4:5)

## Patterns
- Use cn() from lib/utils for className merging
- Relative imports within each app
- pt-BR for all user-facing text
- API routes: /api/v1/{resource}

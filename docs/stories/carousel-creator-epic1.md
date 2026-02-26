# Epic 1: Foundation & Core Infrastructure

**Project:** Carousel Creator
**PRD:** docs/prd/carousel-creator-prd.md

## Story 1.1: Project Scaffolding & Monorepo Setup

**Status:** [ ] In Progress

**Como** desenvolvedor,
**Quero** um monorepo com frontend (React+Vite) e backend (Express+TS) configurados,
**Para que** tenhamos a base de código pronta para desenvolvimento.

### Acceptance Criteria
- [x] Monorepo criado em `carousel-creator/` com `apps/api`, `apps/web`, `packages/shared`
- [x] Backend Express + TypeScript com endpoint `GET /health` retornando `{ status: "ok" }`
- [x] Frontend React + Vite + TypeScript com página canary
- [x] TailwindCSS configurado com design tokens do @lawhander
- [ ] ESLint + Prettier configurados
- [x] `package.json` raiz com scripts `dev`, `build`, `lint`
- [x] `.claude/CLAUDE.md` local criado
- [x] `.env.example` documentando variáveis necessárias

### File List
- `carousel-creator/package.json`
- `carousel-creator/apps/api/src/index.ts`
- `carousel-creator/apps/web/src/App.tsx`
- `carousel-creator/packages/shared/src/types.ts`
- `carousel-creator/packages/shared/src/constants.ts`

---

## Story 1.2: Supabase Auth & Database Schema

**Status:** [ ] Pending

**Como** usuário,
**Quero** fazer login seguro na aplicação,
**Para que** meu conteúdo fique protegido.

### Acceptance Criteria
- [ ] Supabase client configurado no backend e frontend
- [ ] Login/Logout funcional com email + senha via Supabase Auth
- [ ] Middleware de autenticação no backend validando JWT
- [ ] Tabelas criadas: carousels, carousel_slides, carousel_templates, carousel_feedback
- [ ] RLS habilitado + forçado em todas as tabelas
- [ ] Policies: usuário só acessa seus próprios carrosséis
- [ ] Frontend: tela de login funcional

### File List
- `carousel-creator/apps/api/src/middleware/auth.ts`
- `carousel-creator/apps/api/src/lib/supabase.ts`
- `carousel-creator/apps/web/src/lib/supabase.ts`
- `carousel-creator/apps/web/src/pages/LoginPage.tsx`
- SQL migration files

---

## Story 1.3: Design System & Font Setup

**Status:** [ ] Pending

**Como** usuário,
**Quero** que a interface reflita minha identidade visual,
**Para que** o sistema já pareça profissional desde o início.

### Acceptance Criteria
- [ ] Fontes MADE Tommy carregadas no frontend via @font-face
- [ ] Tailwind config com custom fonts
- [ ] Design tokens no Tailwind
- [ ] Dark mode como default
- [ ] Componentes base: Button, Input, Card, Badge, Modal
- [ ] Fontes registradas no Node Canvas para backend

### File List
- `carousel-creator/fonts/*.otf`
- `carousel-creator/apps/web/src/index.css`
- `carousel-creator/apps/web/src/components/ui/*.tsx`

# Carousel Creator — Product Requirements Document (PRD)

## 1. Goals and Background Context

### 1.1 Goals

- Automatizar a criação de carrosséis para o perfil @lawhander (125k+ seguidores) no Instagram
- Gerar textos de carrossel via IA (Gemini) com validação humana antes da geração de imagens
- Produzir imagens de carrossel fiéis ao design system existente do @lawhander (paleta, fontes, layout)
- Implementar um sistema de aprendizado contínuo que melhora com as correções do usuário
- Criar interface web (frontend + backend) para o fluxo completo de criação

### 1.2 Background Context

Lawhander Silva opera o perfil @lawhander no Instagram (verificado, 125k+ seguidores, 6.471 posts) no nicho de educação técnica em manutenção eletrônica de ar-condicionado (marca "Climatrônico"). O perfil publica carrosséis educacionais, de prova social e de listas/dicas com frequência. Hoje, a criação de carrosséis é manual — desde a ideação dos textos até a montagem das imagens no Canva ou similar.

Este projeto visa automatizar esse processo: o usuário insere um tema/ideia, a IA gera os textos do carrossel, o usuário valida/edita, e o sistema gera automaticamente as imagens seguindo o design system do perfil. A cada correção feita pelo usuário, o sistema aprende e melhora as futuras gerações.

### 1.3 Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-02-26 | 1.0.0 | PRD inicial | @pm (Orion) |

---

## 2. Requirements

### 2.1 Functional Requirements

- **FR1:** O sistema deve aceitar temas/ideias como input (texto livre ou seleção de categorias pré-definidas)
- **FR2:** O sistema deve gerar textos de carrossel via Gemini API (título, subtítulos, corpo de cada slide, CTA)
- **FR3:** O sistema deve apresentar os textos gerados para validação do usuário antes de gerar imagens
- **FR4:** O usuário deve poder editar qualquer texto gerado (inline editing em cada slide)
- **FR5:** Após validação dos textos, o sistema deve gerar imagens de carrossel automaticamente seguindo o design system
- **FR6:** O sistema deve suportar múltiplos templates de carrossel (educacional, prova social, lista/dicas, antes/depois)
- **FR7:** O usuário deve poder fazer upload de imagens próprias para inserir nos slides (fotos de placas, componentes, etc.)
- **FR8:** O sistema deve gerar preview visual dos slides antes da exportação final
- **FR9:** O sistema deve exportar imagens em formato 1080x1080 (quadrado Instagram) ou 1080x1350 (4:5 retrato)
- **FR10:** O sistema deve salvar histórico de carrosséis criados com status (rascunho, validado, exportado, publicado)
- **FR11:** O sistema deve aprender com as correções do usuário — armazenar pares (gerado → corrigido) como exemplos para fine-tuning do prompt
- **FR12:** O sistema deve permitir definir "personas" de escrita (tom do @lawhander: direto, motivacional, técnico mas acessível)
- **FR13:** O sistema deve sugerir hashtags relevantes baseadas no conteúdo do carrossel
- **FR14:** O sistema deve permitir duplicar e re-editar carrosséis existentes como base para novos
- **FR15:** O sistema deve ter autenticação (login) para proteger o conteúdo

### 2.2 Non-Functional Requirements

- **NFR1:** Gemini API como LLM principal (modelos: gemini-2.5-flash para geração rápida, gemini-2.5-pro para refinamento)
- **NFR2:** Tempo de geração de textos: < 10 segundos para carrossel completo
- **NFR3:** Tempo de geração de imagens: < 30 segundos para carrossel completo (até 10 slides)
- **NFR4:** A aplicação deve ser responsiva (funcionar em desktop e mobile)
- **NFR5:** Supabase como banco de dados e autenticação (reutilizar infraestrutura existente)
- **NFR6:** Deploy em ambiente self-hosted ou cloud (Railway/Vercel)
- **NFR7:** O learning loop deve acumular no mínimo 20 exemplos antes de influenciar significativamente as gerações
- **NFR8:** Imagens geradas devem ter qualidade mínima de 300 DPI para impressão e 72 DPI otimizado para Instagram
- **NFR9:** O sistema deve funcionar offline para edição de texto (geração de imagens requer conexão)

---

## 3. User Interface Design Goals

### 3.1 Overall UX Vision

Interface clean e escura (dark mode, alinhada com a identidade visual do @lawhander). Fluxo wizard-like em 4 etapas: Ideia → Textos → Design → Exportar. Foco em velocidade — o usuário deve conseguir gerar um carrossel completo em menos de 5 minutos.

### 3.2 Key Interaction Paradigms

- **Wizard/Stepper:** Fluxo linear de 4 passos com possibilidade de voltar
- **Inline Editing:** Edição direta dos textos nos slides (WYSIWYG)
- **Drag & Drop:** Reordenação de slides e upload de imagens
- **Preview ao Vivo:** Visualização em tempo real das alterações
- **Split View:** Texto à esquerda, preview visual à direita

### 3.3 Core Screens and Views

1. **Dashboard** — Lista de carrosséis criados (rascunhos, validados, exportados), busca, filtros
2. **Nova Ideia** — Input do tema, seleção de template (educacional/prova social/dicas), número de slides
3. **Editor de Textos** — Slides em cards, edição inline, botão "Regenerar", validação/aprovação
4. **Editor Visual** — Preview dos slides renderizados, ajustes de cores/imagens, upload de fotos
5. **Exportação** — Download individual ou ZIP, sugestão de hashtags, caption, preview final
6. **Configurações** — Design tokens (cores, fontes), personas de escrita, histórico de aprendizado

### 3.4 Accessibility

WCAG AA — Contraste mínimo 4.5:1, navegação por teclado, labels em formulários

### 3.5 Branding

| Elemento | Valor |
|----------|-------|
| **Cor primária** | `#0084C8` (azul Climatrônico) |
| **Cor secundária** | `#0E4C93` (azul escuro) |
| **Fundo** | `#010101` (preto) |
| **Texto primário** | `#FFFFFF` (branco) |
| **Texto secundário** | `#76777A` (cinza) |
| **Acento/CTA** | Cores chamativas variáveis (amarelo, verde, laranja) para títulos |
| **Fonte títulos** | MADE Tommy ExtraBold |
| **Fonte subtítulos** | MADE Tommy Medium |
| **Fonte corpo** | MADE Tommy Regular |
| **Formato slides** | 1080x1080 ou 1080x1350 |

### 3.6 Target Platforms

Web Responsive (desktop-first, funcional em mobile)

---

## 4. Technical Assumptions

### 4.1 Repository Structure

**Monorepo** — Similar à estrutura do Tráfego (`apps/api` + `apps/web` + `packages/shared`)

```
carousel-creator/
├── apps/
│   ├── api/          # Express + TypeScript backend
│   └── web/          # React + Vite frontend
├── packages/
│   └── shared/       # Tipos, constantes, schemas compartilhados
├── templates/        # Templates visuais de carrossel (JSON + assets)
├── fonts/            # MADE Tommy (local)
├── docs/
│   ├── prd/          # Este PRD
│   └── stories/      # User stories
└── .claude/          # CLAUDE.md local
```

### 4.2 Service Architecture

**Monolith modular** — API Express única com módulos separados:
- `modules/carousel/` — CRUD de carrosséis
- `modules/generation/` — Integração Gemini (texto)
- `modules/renderer/` — Geração de imagens (Canvas/Sharp)
- `modules/learning/` — Feedback loop e exemplos
- `modules/auth/` — Autenticação via Supabase

### 4.3 Tech Stack

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **Frontend** | React 19 + Vite 6 + TypeScript | Padrão do workspace (Tráfego) |
| **UI Components** | Radix UI + TailwindCSS | Padrão do workspace |
| **Backend** | Express + TypeScript | Padrão do workspace (Tráfego) |
| **LLM** | Google Gemini API (`@google/generative-ai`) | Requisito do usuário |
| **Image Generation** | Node Canvas (`canvas`) + Sharp | Server-side rendering de slides |
| **Database** | Supabase (PostgreSQL + Auth + Storage) | Infraestrutura existente |
| **Storage** | Supabase Storage (bucket `carousel-assets`) | Imagens geradas e uploads |
| **Fonts** | MADE Tommy (self-hosted, carregadas no Canvas) | Identidade visual do @lawhander |

### 4.4 Testing Requirements

- **Unit Tests:** Vitest para frontend e backend
- **Integration Tests:** Testes de API endpoints
- **Visual Tests:** Screenshot comparison dos slides gerados vs templates esperados
- **E2E:** Playwright para fluxo completo (ideia → exportar)

### 4.5 Additional Technical Assumptions

- Gemini API com structured output (JSON mode) para consistência dos textos
- Learning loop armazena pares (prompt → gerado → corrigido) em tabela `carousel_feedback`
- Após N correções (threshold configurável, default 20), o sistema enriquece o system prompt com exemplos
- Templates de carrossel são JSON configuráveis (posição de textos, cores, áreas de imagem)
- Fontes MADE Tommy devem ser registradas no Canvas para renderização server-side
- Supabase project: reutilizar `qpfhircjexgbuolobqkf` (mesmo do Estoque/Tráfego) ou novo projeto dedicado

---

## 5. Epic List

### Epic 1: Foundation & Core Infrastructure
Estabelecer o projeto monorepo, autenticação, banco de dados e setup básico de frontend/backend com health check.

### Epic 2: Text Generation Pipeline
Implementar o fluxo de geração de textos via Gemini, com input de temas, seleção de templates, edição inline e validação.

### Epic 3: Image Rendering Engine
Motor de renderização de imagens dos carrosséis usando os design tokens (cores, fontes, layouts) e templates configuráveis.

### Epic 4: Learning Loop & Intelligence
Sistema de aprendizado contínuo: captura de feedback, armazenamento de correções, enriquecimento do prompt, e métricas de melhoria.

### Epic 5: Polish, Export & Dashboard
Dashboard de gerenciamento, exportação final, histórico, duplicação, sugestão de hashtags e refinamentos de UX.

---

## 6. Epic Details

### Epic 1: Foundation & Core Infrastructure

**Goal:** Criar a base do projeto com monorepo funcional, autenticação Supabase, banco de dados com schema inicial, e canary pages em frontend e backend. Ao final deste epic, temos uma app funcional com login e estrutura pronta para receber as features.

#### Story 1.1: Project Scaffolding & Monorepo Setup

**Como** desenvolvedor,
**Quero** um monorepo com frontend (React+Vite) e backend (Express+TS) configurados,
**Para que** tenhamos a base de código pronta para desenvolvimento.

**Acceptance Criteria:**
1. Monorepo criado em `carousel-creator/` com `apps/api`, `apps/web`, `packages/shared`
2. Backend Express + TypeScript com endpoint `GET /health` retornando `{ status: "ok" }`
3. Frontend React + Vite + TypeScript com página canary ("Carousel Creator" + logo)
4. TailwindCSS configurado com design tokens do @lawhander (cores da paleta)
5. ESLint + Prettier configurados
6. `package.json` raiz com scripts `dev`, `build`, `lint`
7. `.claude/CLAUDE.md` local criado com instruções do projeto
8. `.env.example` documentando variáveis necessárias

#### Story 1.2: Supabase Auth & Database Schema

**Como** usuário,
**Quero** fazer login seguro na aplicação,
**Para que** meu conteúdo fique protegido.

**Acceptance Criteria:**
1. Supabase client configurado no backend (service role) e frontend (anon key)
2. Login/Logout funcional com email + senha via Supabase Auth
3. Middleware de autenticação no backend validando JWT
4. Tabelas criadas via migration:
   - `carousels` (id, user_id, title, theme, template_type, status, slide_count, created_at, updated_at)
   - `carousel_slides` (id, carousel_id, position, headline, body_text, cta_text, image_url, bg_color)
   - `carousel_templates` (id, name, description, layout_config JSONB, is_default)
   - `carousel_feedback` (id, carousel_id, slide_position, field, original_text, corrected_text, created_at)
5. RLS habilitado + forçado em todas as tabelas, anon revogado
6. Policies: usuário só acessa seus próprios carrosséis
7. Frontend: tela de login funcional, redirect para dashboard após login

#### Story 1.3: Design System & Font Setup

**Como** usuário,
**Quero** que a interface reflita minha identidade visual,
**Para que** o sistema já pareça profissional desde o início.

**Acceptance Criteria:**
1. Fontes MADE Tommy (ExtraBold, Medium, Regular) carregadas no frontend via `@font-face`
2. Tailwind config com custom fonts: `font-heading` (ExtraBold), `font-subtitle` (Medium), `font-body` (Regular)
3. Design tokens configurados no Tailwind: `brand-black`, `brand-white`, `brand-gray`, `brand-blue`, `brand-blue-dark`
4. Dark mode como default (fundo `#010101`)
5. Componentes base criados: Button, Input, Card, Badge, Modal (usando Radix UI + Tailwind)
6. Fontes também registradas no Node Canvas para uso no backend de renderização

---

### Epic 2: Text Generation Pipeline

**Goal:** Implementar o fluxo completo de geração de textos para carrosséis via Gemini API. O usuário insere um tema, escolhe um template, a IA gera os textos, e o usuário pode editar/validar antes de prosseguir para geração de imagens.

#### Story 2.1: Gemini Integration & Text Generation Service

**Como** sistema,
**Quero** integrar com a API Gemini para gerar textos de carrossel,
**Para que** a IA produza conteúdo relevante e no tom do @lawhander.

**Acceptance Criteria:**
1. Service `GeminiService` criado em `apps/api/src/services/gemini.service.ts`
2. Structured output (JSON mode) com schema tipado para carrossel
3. System prompt otimizado com persona do @lawhander (tom direto, motivacional, técnico mas acessível, pt-BR)
4. Suporte a 4 templates: educacional, prova social, lista/dicas, antes/depois
5. Configuração de número de slides (3-10)
6. Retry com exponential backoff (padrão do Tráfego)
7. Token tracking por geração
8. Endpoint `POST /api/v1/carousels/generate-text` funcional
9. Response inclui: título do carrossel, array de slides (headline, body, cta), hashtags sugeridas

#### Story 2.2: Carousel Creation Flow (Frontend)

**Como** usuário,
**Quero** inserir um tema e receber textos de carrossel gerados pela IA,
**Para que** eu possa criar carrosséis rapidamente.

**Acceptance Criteria:**
1. Página "Novo Carrossel" com stepper visual (Ideia → Textos → Design → Exportar)
2. Step 1 (Ideia): campo de texto para tema, seleção de template (4 opções com ícone), slider para número de slides
3. Botão "Gerar Textos" chama a API e mostra loading com skeleton
4. Step 2 (Textos): slides renderizados como cards verticais com headline, body, CTA editáveis inline
5. Botão "Regenerar" por slide individual ou carrossel inteiro
6. Botão "Validar Textos" salva no banco e avança para Step 3
7. Navegação entre steps funcional (voltar/avançar)
8. Estado salvo automaticamente como rascunho

#### Story 2.3: Inline Text Editing & Validation

**Como** usuário,
**Quero** editar os textos gerados pela IA diretamente nos cards,
**Para que** eu possa ajustar o conteúdo antes de gerar as imagens.

**Acceptance Criteria:**
1. Cada campo de texto (headline, body, CTA) é editável com clique (contenteditable ou textarea)
2. Contador de caracteres por campo com limites recomendados (headline: 60, body: 200, CTA: 30)
3. Auto-save a cada 3 segundos de inatividade
4. Indicador visual de campos editados (vs original da IA)
5. Botão "Restaurar Original" por campo
6. Endpoint `PATCH /api/v1/carousels/:id/slides/:position` para salvar edições
7. Quando usuário edita e salva, a diferença (original → editado) é registrada em `carousel_feedback`
8. Validação: pelo menos headline preenchida em cada slide para avançar

---

### Epic 3: Image Rendering Engine

**Goal:** Motor de renderização de imagens que transforma textos validados em imagens de carrossel seguindo o design system do @lawhander. Templates configuráveis em JSON, renderização server-side via Node Canvas.

#### Story 3.1: Template Engine & Canvas Renderer

**Como** sistema,
**Quero** renderizar slides de carrossel como imagens PNG,
**Para que** os textos validados se transformem em imagens prontas para o Instagram.

**Acceptance Criteria:**
1. Service `RendererService` em `apps/api/src/services/renderer.service.ts`
2. Fontes MADE Tommy registradas no Canvas (`registerFont`)
3. Renderização de slide 1080x1080 e 1080x1350 (configurável)
4. Template JSON define: áreas de texto (x, y, width, height, fontSize, fontFamily, color, align), áreas de imagem, fundo
5. Pelo menos 4 templates padrão implementados:
   - Educacional: título grande topo, ícone/imagem centro, texto explicativo embaixo
   - Prova Social: screenshot/print centro, texto destaque, badge de valor
   - Lista/Dicas: número grande + título + texto explicativo
   - Capa/CTA: título chamativo full-screen com gradiente
6. Endpoint `POST /api/v1/carousels/:id/render` que gera todas as imagens do carrossel
7. Imagens salvas no Supabase Storage (bucket `carousel-assets`)
8. Response retorna array de URLs signed das imagens geradas

#### Story 3.2: Visual Preview & Image Upload

**Como** usuário,
**Quero** ver preview das imagens e fazer upload de fotos próprias,
**Para que** eu possa ajustar o visual antes de exportar.

**Acceptance Criteria:**
1. Step 3 (Design): grid de previews dos slides renderizados
2. Cada slide mostra a imagem gerada com overlays de edição
3. Upload de imagem própria por slide (drag & drop ou file picker)
4. Imagens uploaded são inseridas na área designada do template
5. Seletor de cor de acento por slide (para títulos chamativos)
6. Botão "Re-renderizar" por slide após mudanças
7. Drag & drop para reordenar slides
8. Preview no tamanho real (1080px) com zoom

#### Story 3.3: Template Management

**Como** usuário,
**Quero** gerenciar templates de carrossel,
**Para que** eu possa criar e personalizar layouts.

**Acceptance Criteria:**
1. Tela de templates listando templates disponíveis (padrão + custom)
2. Cada template mostra preview mockup
3. Endpoint `GET /api/v1/templates` lista templates
4. Endpoint `POST /api/v1/templates` cria template custom (JSON config)
5. Templates padrão não editáveis, apenas duplicáveis
6. Seeds com 4 templates padrão no banco (educacional, prova social, lista, capa)

---

### Epic 4: Learning Loop & Intelligence

**Goal:** Implementar o sistema de aprendizado que melhora com as correções do usuário. A cada edição, o sistema armazena o feedback e progressivamente melhora os textos gerados.

#### Story 4.1: Feedback Collection & Storage

**Como** sistema,
**Quero** capturar e armazenar todas as correções feitas pelo usuário,
**Para que** tenhamos dados para melhorar as gerações futuras.

**Acceptance Criteria:**
1. Tabela `carousel_feedback` já criada (Epic 1) recebe dados automaticamente
2. Quando usuário edita texto e confirma, a diferença é salva: original_text, corrected_text, campo, contexto (template, tema)
3. Endpoint `GET /api/v1/feedback/stats` retorna: total de correções, campos mais editados, padrões de correção
4. Dashboard de feedback mostrando estatísticas visuais
5. Dados de feedback NUNCA são deletados (append-only)
6. Index em `carousel_feedback.carousel_id` e `carousel_feedback.field` para queries eficientes

#### Story 4.2: Prompt Enhancement with Learning

**Como** sistema,
**Quero** usar as correções passadas para melhorar os prompts futuros,
**Para que** a IA gere textos cada vez mais alinhados com o estilo do usuário.

**Acceptance Criteria:**
1. Service `LearningService` em `apps/api/src/services/learning.service.ts`
2. Método `getRelevantExamples(template, theme)` busca os melhores exemplos de correção para o contexto
3. Threshold configurável (default: 20 correções) antes de ativar o learning
4. Exemplos injetados no prompt como few-shot examples: "O usuário prefere X ao invés de Y"
5. Máximo de 5 exemplos por geração (para não estourar contexto)
6. Seleção de exemplos por relevância (mesmo template, tema similar via embedding ou keyword match)
7. Toggle para ativar/desativar learning na UI
8. Log de quais exemplos foram usados em cada geração

#### Story 4.3: Writing Persona Configuration

**Como** usuário,
**Quero** configurar a persona de escrita da IA,
**Para que** o tom e estilo dos textos reflitam minha identidade.

**Acceptance Criteria:**
1. Tela de configuração de persona em Settings
2. Campos: nome, tom de voz (seleção múltipla: direto, motivacional, técnico, informal, formal), exemplos de frases típicas, palavras/expressões para usar, palavras/expressões para evitar
3. Persona default pré-configurada para @lawhander
4. Persona salva no banco (tabela `writing_personas`)
5. Múltiplas personas suportadas (ex: "Tom de aula", "Tom de venda", "Tom de meme")
6. Persona selecionável no Step 1 (Ideia) ao criar carrossel
7. Endpoint CRUD `/api/v1/personas`

---

### Epic 5: Polish, Export & Dashboard

**Goal:** Refinar a experiência completa: dashboard de gerenciamento, exportação final, histórico, duplicação, hashtags e UX polish.

#### Story 5.1: Dashboard & Carousel Management

**Como** usuário,
**Quero** ver todos os meus carrosséis em um dashboard,
**Para que** eu possa gerenciar meu conteúdo.

**Acceptance Criteria:**
1. Dashboard como página principal pós-login
2. Grid de carrosséis com thumbnail do primeiro slide
3. Filtros por status (rascunho, textos validados, imagens geradas, exportado)
4. Busca por título/tema
5. Ordenação por data (mais recente primeiro)
6. Ações por carrossel: editar, duplicar, deletar, exportar
7. Endpoint `GET /api/v1/carousels` com paginação, filtros e busca
8. Contadores de status no topo do dashboard

#### Story 5.2: Export & Download

**Como** usuário,
**Quero** exportar meus carrosséis como imagens prontas para Instagram,
**Para que** eu possa publicar rapidamente.

**Acceptance Criteria:**
1. Step 4 (Exportar): preview final de todos os slides em sequência
2. Download individual por slide (PNG)
3. Download completo em ZIP com todos os slides nomeados sequencialmente
4. Caption sugerido pela IA (texto da legenda do post)
5. Hashtags sugeridas (baseadas no conteúdo + hashtags recorrentes do @lawhander)
6. Botão "Copiar Caption" para clipboard
7. Formato exportado: 1080x1080 ou 1080x1350 (selecionável)
8. Qualidade: 72 DPI otimizado para Instagram

#### Story 5.3: Duplicate, History & UX Polish

**Como** usuário,
**Quero** duplicar carrosséis e ver meu histórico de criação,
**Para que** eu possa reutilizar conteúdo e acompanhar minha produção.

**Acceptance Criteria:**
1. Botão "Duplicar" cria cópia completa (textos + configurações, sem imagens)
2. Histórico de atividade por carrossel (criado, editado, renderizado, exportado) com timestamps
3. Skeleton loaders em todas as telas durante carregamento
4. Toast notifications para ações de sucesso/erro
5. Empty states com ilustrações para dashboard vazio e listas vazias
6. Shortcuts de teclado: Ctrl+S (salvar), Ctrl+Enter (avançar step)
7. Responsividade: layout funcional em telas >= 768px

---

## 7. Team Composition (AIOS Agents)

### Core Team (9 Agents — Time Premium)

| Agent | Role | Squad | Model | Responsibility |
|-------|------|-------|-------|----------------|
| **@pm** | Product Manager | Core AIOS | sonnet | PRD, stories, backlog management |
| **@architect** | Solution Architect | Core AIOS | opus | Arquitetura, decisões técnicas, Gemini integration design |
| **@dev** | Full-Stack Developer | Core AIOS | sonnet | Implementação frontend + backend |
| **@qa** | Quality Assurance | Core AIOS | opus | Testes, validação de acceptance criteria |
| **@aaron-draplin** | Brand & Visual Design | design-system | sonnet | Design tokens, paleta, templates de carrossel, fontes |
| **@paddy-galloway** | Content Strategy | design-system | sonnet | Copy dos carrosséis, hooks, CTR principles, caption optimization |
| **@peter-mckinnon** | Visual Direction | design-system | sonnet | Direção visual, composição dos slides, fotografia |
| **@dave-malouf** | UX/Interaction Design | design-system | sonnet | UX do editor, fluxo wizard, interações drag & drop |
| **@data-engineer** | Data Pipeline | Core AIOS | sonnet | Schema Supabase, learning pipeline, feedback storage |

### Agent Responsibilities per Epic

| Epic | Primary | Support |
|------|---------|---------|
| **1. Foundation** | @dev, @data-engineer | @architect, @aaron-draplin |
| **2. Text Generation** | @dev, @paddy-galloway | @architect (Gemini design) |
| **3. Image Rendering** | @dev, @aaron-draplin, @peter-mckinnon | @dave-malouf (UX preview) |
| **4. Learning Loop** | @dev, @data-engineer | @paddy-galloway (exemplos de copy) |
| **5. Polish & Export** | @dev, @dave-malouf | @qa (full regression) |

---

## 8. Checklist Results Report

*A ser preenchido após execução do pm-checklist.*

---

## 9. Next Steps

### 9.1 UX Expert Prompt

> @dave-malouf — Crie a arquitetura de UX para o Carousel Creator usando este PRD como input. Foque no fluxo wizard de 4 steps, editor de textos com inline editing, preview visual dos slides, e responsividade. Design tokens já definidos na seção 3.5.

### 9.2 Architect Prompt

> @architect — Crie a arquitetura técnica do Carousel Creator usando este PRD. Foco em: integração Gemini com structured output, motor de renderização Canvas, learning loop com feedback storage, e monorepo Express + React + Supabase. Reutilize padrões do Tráfego (apps/api, apps/web pattern).

### 9.3 Design Squad Prompt

> @aaron-draplin + @peter-mckinnon — Criem os templates visuais de carrossel (4 tipos) seguindo o design system: paleta (#010101, #FFFFFF, #76777A, #0084C8, #0E4C93), fontes MADE Tommy (ExtraBold, Medium, Regular), formato 1080x1080/1080x1350. Entreguem os templates como JSON config + mockups.

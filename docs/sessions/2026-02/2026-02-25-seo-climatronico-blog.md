# Session Handoff — SEO Climatronico Blog

**Data:** 2026-02-25
**Projeto:** climatronico-blog (Li-educacao/climatronico-blog)
**Commits:** `25e4d22` (SEO overhaul), `87c7f83` (spam middleware)

## Contexto

Blog climatronico.com.br com 109+ paginas mas apenas ~8 indexadas no Google (<7%). GSC mostrou 17.399 erros 404, 578 paginas rastreadas mas nao indexadas, e sitemaps antigos com 0 paginas.

## O que foi feito

### Fase 1 — Desbloqueio de Indexacao
- **og-default.png** (1200x630) e **logo.png** (512x512) criados via `scripts/generate-og-assets.ts`
- **robots.txt** limpo: removido `Disallow: /_astro/` e `Crawl-delay: 1`
- **SearchAction** removida do SchemaMarkup (apontava para `/busca` inexistente)
- **_redirects** atualizado: 5 tags WordPress, 2 categorias, `/lawhander-climatronico/`, regras 410 para spam
- **Post corrigido:** `erro-e7-electrolux...` tinha category pipe-separated
- **GSC verification:** removido placeholder (GSC ja verificado via dominio)

### Fase 2 — Schema Markup & Rich Results
- **NewsArticle** JSON-LD em todas paginas de noticias
- **BreadcrumbList** ativado em posts (Home > Blog > Categoria > Titulo) e noticias
- **VideoObject** schema automatico para posts com `youtubeId`
- **FAQPage** schema auto-extraido de secoes `## FAQ` no markdown (~10 posts)
- **Autor E-E-A-T:** "Lawhander" com `sameAs` (YouTube, Instagram) em vez de "Climatronico"

### Fase 3 — Otimizacao Tecnica
- **Sitemap:** prioridades diferenciadas (1.0 home, 0.9 blog, 0.8 categorias, 0.7 posts), paginas paginadas excluidas
- **RSS:** incluiu 28 noticias + campo `author`
- **Meta tags:** `og:image:width/height`, `twitter:creator`, removido `meta name="title"` redundante
- **Fonts:** `display=swap` → `display=optional` (Inter + Material Symbols)
- **CWV:** FID depreciado → INP tracking
- **Imagens noticias:** adicionado `width`/`height`/`loading`

### Middleware Anti-Spam
- **`functions/_middleware.ts`** — Cloudflare Pages middleware
- Retorna 410 Gone para: IDs numericos (`/\d{5,}/`), `/zhHant/`, `/search?`, `/product/`, `/wp-*`
- Resolve os ~17k URLs de spam no GSC

## Arquivos modificados (13)
- `astro.config.mjs` — sitemap priorities + filter
- `public/_redirects` — WordPress tags/categories + spam 410
- `public/robots.txt` — cleanup
- `public/og-default.png` — novo
- `public/logo.png` — novo
- `src/components/BaseHead.astro` — meta tags, fonts, INP
- `src/components/SchemaMarkup.astro` — NewsArticle, VideoObject, FAQPage, autor E-E-A-T
- `src/layouts/BaseLayout.astro` — font display=optional
- `src/layouts/PostLayout.astro` — Breadcrumbs, FAQ extraction, VideoObject
- `src/pages/noticias/[...slug].astro` — NewsArticle schema, Breadcrumbs, img attrs
- `src/pages/rss.xml.ts` — noticias + author
- `src/content/posts/erro-e7-electrolux-resolva-com-2-componentes-rapido.md` — fix category
- `scripts/generate-og-assets.ts` — novo
- `functions/_middleware.ts` — novo

## Analise GSC (dados do export)
- **17.399 erros 404:** ~99% spam (843 IDs numericos, 65 zhHant/product, 80 search injection)
- **Apenas ~10 URLs** eram conteudo real do WordPress (tags, categorias) — redirecionadas
- **578 "rastreadas mas nao indexadas"** — devem melhorar com schemas e robots corrigidos
- **211 "pagina alternativa com tag canonica"** — normal, sao variantes www/non-www

## Status GSC (manual pelo usuario)
- [x] GSC ja verificado (dominio)
- [x] Sitemaps antigos removidos (sitemap.xml, sitemap_index.xml)
- [x] Novo sitemap submetido (sitemap-index.xml) — aguardando processamento
- [ ] Solicitar indexacao das paginas principais via "Inspecao de URL"
- [ ] Clicar "Validar correcao" nos erros 404

## Pendencias futuras
- **Acompanhar GSC** em 1-2 semanas — verificar se paginas indexadas subiram
- **Sitemap `lastmod`:** Astro sitemap plugin nao suporta `lastmod` automatico baseado em frontmatter `updatedDate` — requer customizacao futura ou plugin alternativo
- **Self-hosting de fonts:** considerar baixar Inter e hospedar localmente para eliminar request externo
- **Pagina /busca:** se criar no futuro, re-adicionar SearchAction no schema WebSite

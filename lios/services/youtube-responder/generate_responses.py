#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate response drafts for YouTube comments using the Lawhander Climatrônico clone.

Uses Gemini 2.5 Pro with the MMOS system prompt to generate responses that match
Lawhander's real voice, tone, and patterns from 92 real YouTube responses.

Usage:
    python generate_responses.py                # Generate for all pending
    python generate_responses.py --limit 10     # Generate for 10 comments
    python generate_responses.py --dry-run      # Preview without writing
    python generate_responses.py --category technical_question  # Only one category
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

logger = logging.getLogger("generator")

# ─── Clone System Prompt (YouTube Responder specialization) ──────────────────

CLONE_SYSTEM_PROMPT = """Você é o Lawhander Silva — o Climatrônico original. Técnico especialista em reparo de placas eletrônicas de ar-condicionado, educador, criador do Método OET, fundador da AME.

Sua tarefa: RESPONDER COMENTÁRIOS do YouTube no EXATO tom e estilo que o Lawhander real usa.

## REGRAS DE VOZ PARA COMENTÁRIOS DO YOUTUBE

Baseado na análise de 92 respostas REAIS do Lawhander no YouTube:

### PADRÃO 1: Respostas são CURTAS (1-3 frases no máximo)
- NÃO escreva parágrafos longos
- NÃO use templates estruturados (listas, headers, etc.)
- Responda como mensagem de chat, não como artigo

### PADRÃO 2: Tom informal e direto
- Use: "Tmj", "Show", "Valeu", "Bora", "meu patrão", "cara"
- Emojis funcionais: 🤝 👍🏻 🔥 👊 💪 👏🏻 ✅
- Contrações: "tô", "tá", "pra"

### PADRÃO 3: Respostas variam por tipo de comentário

**Elogio/Agradecimento** → Ultra-curto:
- "Tmj. 🤝"
- "Valeu. Tmj"
- "Show demais"
- "Valeu meu parceiro, bora pra cima! 🔥"
- "Show de bola, parabéns 👏🏻 👏🏻 👏🏻 ✅"

**Pergunta Técnica** → Direto ao ponto, sem enrolação:
- "Como não desmontou ainda deve desmontar e ver se o cabo tá oxidado e refazer a medição direto no pino do compressor"
- "Se for a de 9.000 BTUs, ela não tem reator. Se for de 12.000 BTUs pra cima, o reator fica na máquina."
- Nunca começa com "Olá" ou "Bom dia" em respostas técnicas

**Interesse no Curso** → Convida pro contato:
- "Tenho um curso de reparo de placas eletrônica de ar-condicionado. Entra em contato com minha equipe. (85) 99143-6825"
- "Pré-inscrição para a academia da Manutenção Eletrônica - AME: https://lawhander.com.br/mc-caporg"

**Reclamação** → Defende com conteúdo, sem agressividade:
- "Como não, só pelo conteúdo já é pra vocês acompanharem, se aplicar ganha dinheiro com o que ensino. Mas tô aqui pra responder vocês. Fique triste não tmj"

**Pergunta de follow-up** → Pergunta de volta:
- "E os outros LEDs?"
- "qual deles?"
- "Na verificou o manual da máquina?"

**Experiência compartilhada** → Celebra curto:
- "Muito bom! Está seguindo um ótimo caminho 👏🏼👏🏼👏🏼👏🏼"
- "Show. Anotado."

### PADRÃO 4: O que NUNCA fazer
- NUNCA use linguagem formal: "Prezado", "Conforme mencionado", "Recomenda-se"
- NUNCA escreva mais de 4 frases
- NUNCA use markdown (negrito, itálico, headers, listas)
- NUNCA use "Espero que tenha ajudado" ou "Qualquer dúvida estou à disposição"
- NUNCA invente dados técnicos que você não tem certeza
- NUNCA responda spam (retorne SKIP)

### PADRÃO 5: Informações de contato (use quando pedirem sobre curso)
- Telefone equipe: (85) 99143-6825
- Link inscrição: https://lawhander.com.br/mc-caporg
- Nome do curso: Academia da Manutenção Eletrônica (AME)

### PADRÃO 6: Segurança elétrica
- Se envolver tensão alta (>200V, DC-Link, capacitor), SEMPRE alerte sobre segurança
- Use CAPS para segurança: "DESCARREGA os capacitores ANTES"
"""

GENERATION_PROMPT_NO_EXAMPLES = """Responda este comentário do YouTube como Lawhander Climatrônico.

VÍDEO: {video_title}
AUTOR: {author}
COMENTÁRIO: {comment_text}
CATEGORIA: {category}

REGRAS:
1. Responda em 1-3 frases CURTAS (máximo 4 frases para perguntas técnicas complexas)
2. Se for spam, responda APENAS com a palavra: SKIP
3. Se não tiver informação suficiente para resposta técnica precisa, faça uma pergunta de volta
4. Use o tom informal do Lawhander (Tmj, Show, Valeu, cara, meu patrão)
5. NÃO use markdown. Texto puro.

Responda APENAS com o texto da resposta (sem aspas, sem prefixo "Resposta:")."""

GENERATION_PROMPT_WITH_EXAMPLES = """Responda este comentário do YouTube como Lawhander Climatrônico.

EXEMPLOS DE RESPOSTAS APROVADAS (aprenda com estes — são respostas reais que eu aprovei ou corrigi):
{examples}

Agora responda este novo comentário seguindo o mesmo estilo:

VÍDEO: {video_title}
AUTOR: {author}
COMENTÁRIO: {comment_text}
CATEGORIA: {category}

REGRAS:
1. Responda em 1-3 frases CURTAS (máximo 4 frases para perguntas técnicas complexas)
2. Se for spam, responda APENAS com a palavra: SKIP
3. Se não tiver informação suficiente para resposta técnica precisa, faça uma pergunta de volta
4. Use o tom informal do Lawhander (Tmj, Show, Valeu, cara, meu patrão)
5. NÃO use markdown. Texto puro.
6. Priorize o estilo dos exemplos aprovados acima — eles representam como EU realmente respondo.

Responda APENAS com o texto da resposta (sem aspas, sem prefixo "Resposta:")."""


def log(emoji: str, msg: str) -> None:
    print(f"{emoji} {msg}")


def log_step(step: int, total: int, msg: str) -> None:
    print(f"  [{step}/{total}] {msg}")


def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def get_gemini_model():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=CLONE_SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=500,
        ),
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ],
    )


def fetch_feedback_examples(sb: Client, category: str | None = None, limit: int = 10) -> list[dict]:
    """Fetch approved/edited examples for few-shot learning."""
    try:
        query = (
            sb.table("yt_feedback_examples")
            .select("comment_category, comment_text, final_response, feedback_type")
            .in_("feedback_type", ["approved", "edited"])
            .order("reviewed_at", desc=True)
            .limit(limit)
        )
        if category:
            query = query.eq("comment_category", category)

        result = query.execute()
        return result.data or []
    except Exception:
        return []


def format_examples(examples: list[dict]) -> str:
    """Format feedback examples for the prompt."""
    lines = []
    for i, ex in enumerate(examples, 1):
        was_edited = ex["feedback_type"] == "edited"
        tag = " (corrigida por mim)" if was_edited else ""
        lines.append(f"Exemplo {i}{tag}:")
        lines.append(f"  Comentário: {ex['comment_text'][:200]}")
        lines.append(f"  Resposta: {ex['final_response']}")
        lines.append("")
    return "\n".join(lines)


def generate_response(model, video_title: str, author: str, comment_text: str, category: str,
                      feedback_examples: list[dict] | None = None) -> tuple[str, float]:
    """Generate a single response. Returns (response_text, confidence_score)."""
    # Use examples if available (few-shot learning from feedback)
    if feedback_examples:
        examples_text = format_examples(feedback_examples)
        prompt = GENERATION_PROMPT_WITH_EXAMPLES.format(
            examples=examples_text,
            video_title=video_title,
            author=author,
            comment_text=comment_text,
            category=category,
        )
    else:
        prompt = GENERATION_PROMPT_NO_EXAMPLES.format(
            video_title=video_title,
            author=author,
            comment_text=comment_text,
            category=category,
        )

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Check if response was truncated (ends mid-sentence)
    safe_endings = ".!?🤝👍👊💪✅😊😁"
    is_complete = text and (text[-1] in safe_endings
                            or text.lower().endswith("tmj")
                            or text.endswith("🏻")
                            or text.endswith("🏼"))

    if not is_complete and len(text) > 5:
        # Retry with explicit instruction to finish
        retry_prompt = prompt + "\n\nIMPORTANTE: Responda COMPLETO em 2-3 frases CURTAS. Termine a frase com ponto, emoji ou 'Tmj'."
        retry = model.generate_content(retry_prompt)
        retry_text = retry.text.strip()
        if retry_text:
            text = retry_text

    # Calculate rough confidence based on response characteristics
    confidence = 0.8  # base
    if len(text) < 10:
        confidence = 0.95  # short responses are high confidence (simple patterns)
    elif category == "praise":
        confidence = 0.95  # praise responses are predictable
    elif category == "technical_question" and len(text) > 200:
        confidence = 0.6  # long technical responses need more review
    elif category == "course_inquiry":
        confidence = 0.9  # course promotion is templated
    elif "?" in text:
        confidence = 0.85  # asking back is a safe pattern

    return text, confidence


def fetch_pending_comments(sb: Client, category: str | None = None, limit: int = 50) -> list[dict]:
    """Fetch comments that don't have drafts yet, excluding owner comments and spam."""
    query = (
        sb.table("yt_comments")
        .select("id, video_id, author, text, category, comment_date, yt_videos(title)")
        .eq("is_from_owner", False)
        .neq("category", "spam")
        .order("comment_date", desc=True)
        .limit(limit)
    )

    if category:
        query = query.eq("category", category)

    result = query.execute()
    comments = result.data or []

    # Filter out comments that already have drafts
    if not comments:
        return []

    comment_ids = [c["id"] for c in comments]
    existing_drafts = (
        sb.table("yt_response_drafts")
        .select("comment_id")
        .in_("comment_id", comment_ids)
        .execute()
    )
    drafted_ids = {d["comment_id"] for d in (existing_drafts.data or [])}

    return [c for c in comments if c["id"] not in drafted_ids]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate YouTube response drafts")
    parser.add_argument("--limit", type=int, default=50, help="Max comments to process")
    parser.add_argument("--category", type=str, default=None, help="Filter by category")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    sb = get_supabase()
    model = get_gemini_model()

    log("🔍", f"Buscando comentários sem draft (limit={args.limit}, category={args.category or 'todas'})...")
    comments = fetch_pending_comments(sb, category=args.category, limit=args.limit)

    if not comments:
        log("✅", "Nenhum comentário pendente encontrado!")
        return

    log("💬", f"Encontrados {len(comments)} comentários para gerar respostas")

    # Fetch feedback examples for few-shot learning
    feedback_examples = fetch_feedback_examples(sb, limit=15)
    if feedback_examples:
        edited_count = sum(1 for e in feedback_examples if e["feedback_type"] == "edited")
        log("🧠", f"Aprendizado ativo: {len(feedback_examples)} exemplos ({edited_count} com correções)")
    else:
        log("📝", "Sem exemplos de feedback ainda — usando apenas o clone base")

    generated = 0
    skipped = 0
    errors = 0

    for i, comment in enumerate(comments):
        video_title = comment.get("yt_videos", {}).get("title", "Vídeo desconhecido")
        author = comment["author"]
        text = comment["text"]
        category = comment.get("category", "general")

        # Get category-specific examples if available
        cat_examples = [e for e in feedback_examples if e["comment_category"] == category]
        # Fall back to all examples if no category-specific ones
        examples_to_use = cat_examples if len(cat_examples) >= 3 else feedback_examples

        log_step(i + 1, len(comments), f"{author} — {text[:60]}...")

        try:
            response_text, confidence = generate_response(
                model, video_title, author, text, category,
                feedback_examples=examples_to_use if examples_to_use else None
            )

            if response_text.strip().upper() == "SKIP":
                log("  ⏭️", "Pulado (spam/irrelevante)")
                skipped += 1
                continue

            if args.dry_run:
                log("  📝", f"DRAFT: {response_text}")
                log("  📊", f"Confiança: {confidence:.0%}")
                generated += 1
                continue

            # Save draft to database
            sb.table("yt_response_drafts").insert({
                "comment_id": comment["id"],
                "draft_text": response_text,
                "status": "pending",
                "confidence_score": confidence,
                "category_used": category,
                "clone_version": "1.0",
            }).execute()

            generated += 1
            log("  ✅", f"Draft gerado (confiança: {confidence:.0%})")

            # Rate limiting — Gemini has quota limits
            time.sleep(1)

        except Exception as e:
            log("  ❌", f"Erro: {e}")
            errors += 1
            time.sleep(2)  # back off on errors

    log("🎉", f"Concluído! Gerados: {generated} | Pulados: {skipped} | Erros: {errors}")


if __name__ == "__main__":
    main()

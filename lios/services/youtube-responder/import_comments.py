#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import YouTube comments from all_comments_1000.json into yt_videos + yt_comments tables."""

import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

COMMENTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "youtube-comments", "all_comments_1000.json"
)

OWNER_HANDLE = "@lawhander"


def log(emoji: str, msg: str) -> None:
    print(f"{emoji} {msg}")


def log_step(step: int, total: int, msg: str) -> None:
    print(f"  [{step}/{total}] {msg}")


def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def classify_comment(text: str, author: str, is_owner: bool) -> str:
    """Simple rule-based classifier for comment categories."""
    if is_owner:
        return "general"

    lower = text.lower()

    # Spam detection
    if any(w in lower for w in ["ganhe dinheiro", "clique aqui", "http://bit.ly", "whatsapp.com/channel"]):
        return "spam"

    # Course inquiry
    if any(w in lower for w in ["curso", "ame", "academia", "inscrição", "inscrever", "matrícula", "quanto custa", "valor do curso"]):
        return "course_inquiry"

    # Technical question (keywords + question mark)
    tech_words = ["erro", "error", "placa", "compressor", "inverter", "tensão", "voltagem",
                  "capacitor", "ipm", "pfc", "led", "sensor", "resistor", "multímetro",
                  "medição", "ohms", "amperagem", "corrente", "curto", "queimado",
                  "não liga", "não funciona", "defeito", "diagnóstico", "como testar",
                  "como medir", "como resolver", "samsung", "lg", "midea", "springer",
                  "carrier", "consul", "daikin", "fujitsu", "elgin", "electrolux",
                  "condensadora", "evaporadora", "dc-link", "esr"]
    is_question = "?" in text
    has_tech = any(w in lower for w in tech_words)

    if has_tech and is_question:
        return "technical_question"
    if has_tech and len(text) > 100:
        return "technical_question"

    # Complaint
    if any(w in lower for w in ["não responde", "decepcionado", "péssimo", "ruim", "não recomendo"]):
        return "complaint"

    # Praise
    if any(w in lower for w in ["parabéns", "show", "excelente", "top", "obrigado", "obrigada",
                                 "muito bom", "maravilhoso", "fera", "mito", "melhor canal",
                                 "professor", "boa aula", "gratidão"]):
        return "praise"

    # Sharing experience
    if any(w in lower for w in ["consegui", "consertei", "reparei", "faturei", "ganhei",
                                 "na minha bancada", "meu caso", "aqui comigo"]):
        return "share_experience"

    # Correction needed (wrong info)
    if any(w in lower for w in ["na verdade", "errado", "incorreto", "não é bem assim", "discordo"]):
        return "correction_needed"

    return "general"


def ts_to_iso(ts: int | None) -> str | None:
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def main(dry_run: bool = False) -> None:
    log("📂", f"Lendo comentários de {COMMENTS_FILE}")

    with open(COMMENTS_FILE, encoding="utf-8") as f:
        comments = json.load(f)

    log("📊", f"Total de comentários no JSON: {len(comments)}")

    # Group by video
    videos: dict[str, dict] = {}
    for c in comments:
        vid = c["video_id"]
        if vid not in videos:
            videos[vid] = {"title": c["video_title"], "comments": []}
        videos[vid]["comments"].append(c)

    log("🎬", f"Vídeos únicos: {len(videos)}")

    if dry_run:
        log("🔍", "DRY RUN — nada será gravado no banco")
        for vid, data in list(videos.items())[:5]:
            log("  🎬", f"{data['title']} ({len(data['comments'])} comments)")
        return

    sb = get_supabase()

    # Step 1: Upsert videos
    log("🎬", "Importando vídeos...")
    video_rows = []
    for vid, data in videos.items():
        owner_comments = sum(1 for c in data["comments"] if c["author"] == OWNER_HANDLE)
        video_rows.append({
            "youtube_video_id": vid,
            "title": data["title"],
            "comment_count": len(data["comments"]),
            "responded_count": owner_comments,
        })

    result = sb.table("yt_videos").upsert(
        video_rows, on_conflict="youtube_video_id"
    ).execute()
    log("✅", f"Vídeos upserted: {len(result.data)}")

    # Build video_id map (youtube_video_id → uuid)
    all_videos = sb.table("yt_videos").select("id, youtube_video_id").execute()
    vid_map = {v["youtube_video_id"]: v["id"] for v in all_videos.data}

    # Step 2: Import comments in batches
    log("💬", "Importando comentários...")
    comment_rows = []
    for c in comments:
        is_owner = c["author"] == OWNER_HANDLE
        category = classify_comment(c["text"], c["author"], is_owner)
        db_video_id = vid_map.get(c["video_id"])
        if not db_video_id:
            continue

        comment_rows.append({
            "video_id": db_video_id,
            "author": c["author"],
            "text": c["text"],
            "likes": c.get("likes", 0),
            "is_reply": False,
            "category": category,
            "has_response": False,
            "is_from_owner": is_owner,
            "comment_date": ts_to_iso(c.get("timestamp")),
        })

    # Deduplicate by (video_id, author, text) — same as UNIQUE constraint
    seen = set()
    unique_rows = []
    for row in comment_rows:
        key = (row["video_id"], row["author"], row["text"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)
    log("🔄", f"Deduplicados: {len(comment_rows)} → {len(unique_rows)} únicos")
    comment_rows = unique_rows

    # Batch upsert (500 at a time to avoid payload limits)
    batch_size = 500
    imported = 0
    for i in range(0, len(comment_rows), batch_size):
        batch = comment_rows[i : i + batch_size]
        try:
            result = sb.table("yt_comments").upsert(
                batch, on_conflict="video_id,author,text"
            ).execute()
            imported += len(result.data)
            log_step(i // batch_size + 1, (len(comment_rows) // batch_size) + 1,
                     f"{len(result.data)} comentários importados")
        except Exception as e:
            log("❌", f"Erro no batch {i}: {e}")

    log("✅", f"Total importado: {imported} comentários")

    # Step 3: Mark comments that already have owner responses
    log("🔗", "Marcando comentários com respostas do dono...")

    # Get owner comments and their video contexts
    owner_data = (
        sb.table("yt_comments")
        .select("id, video_id, text, comment_date")
        .eq("is_from_owner", True)
        .execute()
    )

    # For each video with owner comments, mark non-owner comments before the response
    # Simple heuristic: if the owner responded in a video, mark earlier non-owner comments as responded
    videos_with_responses = set(c["video_id"] for c in owner_data.data)
    if videos_with_responses:
        updated = 0
        for video_uuid in videos_with_responses:
            result = (
                sb.table("yt_comments")
                .update({"has_response": True})
                .eq("video_id", video_uuid)
                .eq("is_from_owner", False)
                .execute()
            )
            updated += len(result.data) if result.data else 0
        log("✅", f"Marcados {updated} comentários como respondidos")

    # Summary
    stats = sb.table("yt_comments").select("category", count="exact").execute()
    log("📊", "Resumo por categoria:")
    cat_counts: dict[str, int] = {}
    for row in (stats.data or []):
        cat = row.get("category", "general")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        log("  📌", f"{cat}: {count}")

    owner_count = sum(1 for c in comments if c["author"] == OWNER_HANDLE)
    log("📊", f"Comentários do dono (@lawhander): {owner_count}")
    log("📊", f"Comentários de terceiros: {len(comments) - owner_count}")
    log("🎉", "Importação concluída!")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    main(dry_run=dry)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch new YouTube comments using yt-dlp and import to database.

Usage:
    python fetch_new_comments.py                  # Fetch from all videos in video_list.txt
    python fetch_new_comments.py --video ID       # Fetch from a specific video
    python fetch_new_comments.py --recent 10      # Fetch from 10 most recent videos
    python fetch_new_comments.py --dry-run        # Preview without writing
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

OWNER_HANDLE = "@lawhander"

VIDEO_LIST = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "youtube-comments", "video_list.txt"
)


def log(emoji: str, msg: str) -> None:
    print(f"{emoji} {msg}")


def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def fetch_comments_ytdlp(video_id: str) -> list[dict]:
    """Fetch comments for a single video using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--write-comments", "--skip-download", "--dump-json",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=120,
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        comments = []

        for c in data.get("comments", []):
            comments.append({
                "video_id": video_id,
                "video_title": data.get("title", ""),
                "author": f"@{c.get('author_id', c.get('author', 'unknown'))}",
                "text": c.get("text", ""),
                "likes": c.get("like_count", 0),
                "timestamp": c.get("timestamp"),
            })

        return comments

    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        log("❌", f"Erro ao buscar {video_id}: {e}")
        return []


def classify_comment(text: str, is_owner: bool) -> str:
    """Simple rule-based classifier."""
    if is_owner:
        return "general"

    lower = text.lower()

    if any(w in lower for w in ["ganhe dinheiro", "clique aqui", "http://bit.ly"]):
        return "spam"
    if any(w in lower for w in ["curso", "ame", "academia", "inscrição", "quanto custa"]):
        return "course_inquiry"

    tech_words = ["erro", "error", "placa", "compressor", "inverter", "tensão",
                  "capacitor", "ipm", "sensor", "led", "não liga", "defeito"]
    if any(w in lower for w in tech_words) and ("?" in text or len(text) > 100):
        return "technical_question"
    if any(w in lower for w in ["parabéns", "show", "obrigado", "muito bom", "top"]):
        return "praise"
    if any(w in lower for w in ["consegui", "consertei", "faturei"]):
        return "share_experience"

    return "general"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch new YouTube comments")
    parser.add_argument("--video", type=str, help="Specific video ID")
    parser.add_argument("--recent", type=int, default=0, help="Fetch N most recent videos")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Determine which videos to fetch
    video_ids = []

    if args.video:
        video_ids = [args.video]
    elif os.path.exists(VIDEO_LIST):
        with open(VIDEO_LIST) as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    vid = line.split("|")[0].strip()
                    if vid:
                        video_ids.append(vid)

        if args.recent > 0:
            video_ids = video_ids[:args.recent]
    else:
        log("❌", f"Arquivo não encontrado: {VIDEO_LIST}")
        sys.exit(1)

    log("🎬", f"Vídeos para buscar: {len(video_ids)}")

    sb = get_supabase() if not args.dry_run else None
    total_new = 0

    for i, vid in enumerate(video_ids):
        log("🔄", f"[{i+1}/{len(video_ids)}] Buscando {vid}...")
        comments = fetch_comments_ytdlp(vid)

        if not comments:
            continue

        log("  💬", f"Encontrados {len(comments)} comentários")

        if args.dry_run:
            total_new += len(comments)
            continue

        # Upsert video
        title = comments[0]["video_title"] if comments else vid
        owner_count = sum(1 for c in comments if c["author"] == OWNER_HANDLE)

        sb.table("yt_videos").upsert({
            "youtube_video_id": vid,
            "title": title,
            "comment_count": len(comments),
            "responded_count": owner_count,
        }, on_conflict="youtube_video_id").execute()

        # Get video UUID
        video_row = sb.table("yt_videos").select("id").eq("youtube_video_id", vid).single().execute()
        video_uuid = video_row.data["id"]

        # Upsert comments
        rows = []
        for c in comments:
            is_owner = c["author"] == OWNER_HANDLE
            rows.append({
                "video_id": video_uuid,
                "author": c["author"],
                "text": c["text"],
                "likes": c.get("likes", 0),
                "category": classify_comment(c["text"], is_owner),
                "is_from_owner": is_owner,
                "comment_date": datetime.fromtimestamp(c["timestamp"], tz=timezone.utc).isoformat() if c.get("timestamp") else None,
            })

        try:
            result = sb.table("yt_comments").upsert(
                rows, on_conflict="video_id,author,text"
            ).execute()
            total_new += len(result.data)
        except Exception as e:
            log("  ❌", f"Erro: {e}")

    log("🎉", f"Concluído! {total_new} comentários processados")


if __name__ == "__main__":
    main()

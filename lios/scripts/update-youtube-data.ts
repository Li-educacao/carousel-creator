#!/usr/bin/env npx tsx
/**
 * Content Studio — YouTube Data Updater
 *
 * Imports video data from video_list.txt and comments from all_comments.json
 * into the ct_videos and ct_comments Supabase tables.
 *
 * Usage:
 *   npx tsx lios/scripts/update-youtube-data.ts                # Import existing data
 *   npx tsx lios/scripts/update-youtube-data.ts --fetch         # Fetch fresh data via yt-dlp first
 *   npx tsx lios/scripts/update-youtube-data.ts --ideas         # Generate content ideas
 */

import { createClient } from '@supabase/supabase-js';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '../..');

// ─── Supabase client (service_role bypasses RLS) ─────────────────────────────
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://tqpkymereiyfxroiuaip.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || '';

if (!SUPABASE_SERVICE_KEY) {
  console.error('Missing SUPABASE_SERVICE_ROLE_KEY. Set it in .env or export it.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

// ─── Paths ───────────────────────────────────────────────────────────────────
const VIDEO_LIST_PATH = resolve(ROOT, 'youtube-comments/video_list.txt');
const COMMENTS_PATH = resolve(ROOT, 'youtube-comments/all_comments.json');
const CHANNEL_ID = 'UCxxxxxxxxx'; // Climatrônico channel — not needed for local import

// ─── Parse lesson number from title ──────────────────────────────────────────
function parseLessonNumber(title: string): number | null {
  // Match patterns like "AULA #328", "Aula 70", "VIDEO CLASS #315", "Video Lesson #316"
  const match = title.match(/(?:AULA|LESSON|CLASS|aula)\s*#?(\d+)/i);
  return match ? parseInt(match[1], 10) : null;
}

// ─── Import videos from video_list.txt ───────────────────────────────────────
async function importVideos(): Promise<number> {
  if (!existsSync(VIDEO_LIST_PATH)) {
    console.error(`video_list.txt not found at ${VIDEO_LIST_PATH}`);
    return 0;
  }

  const lines = readFileSync(VIDEO_LIST_PATH, 'utf-8')
    .split('\n')
    .filter(Boolean);

  console.log(`Found ${lines.length} videos in video_list.txt`);

  const videos = lines.map((line) => {
    const [videoId, ...titleParts] = line.split('|');
    const title = titleParts.join('|').trim();
    return {
      video_id: videoId.trim(),
      title,
      lesson_number: parseLessonNumber(title),
      views: 0,
      likes: 0,
      comment_count: 0,
      duration: 0,
      metadata: {},
    };
  });

  // Upsert in batches of 50
  let imported = 0;
  for (let i = 0; i < videos.length; i += 50) {
    const batch = videos.slice(i, i + 50);
    const { error } = await supabase
      .from('ct_videos')
      .upsert(batch, { onConflict: 'video_id' });

    if (error) {
      console.error(`Error upserting videos batch ${i}:`, error.message);
    } else {
      imported += batch.length;
    }
  }

  console.log(`Imported ${imported} videos`);
  return imported;
}

// ─── Import comments from all_comments.json ──────────────────────────────────
async function importComments(): Promise<number> {
  if (!existsSync(COMMENTS_PATH)) {
    console.error(`all_comments.json not found at ${COMMENTS_PATH}`);
    return 0;
  }

  const raw = JSON.parse(readFileSync(COMMENTS_PATH, 'utf-8')) as Array<{
    video_id: string;
    video_title: string;
    author: string;
    text: string;
    likes: number;
    timestamp: number;
  }>;

  console.log(`Found ${raw.length} comments in all_comments.json`);

  const comments = raw.map((c) => ({
    video_id: c.video_id,
    author: c.author,
    text: c.text,
    likes: c.likes || 0,
    comment_timestamp: c.timestamp || null,
  }));

  // Upsert in batches of 50
  let imported = 0;
  for (let i = 0; i < comments.length; i += 50) {
    const batch = comments.slice(i, i + 50);
    const { error } = await supabase
      .from('ct_comments')
      .upsert(batch, { onConflict: 'video_id,author,text' });

    if (error) {
      console.error(`Error upserting comments batch ${i}:`, error.message);
    } else {
      imported += batch.length;
    }
  }

  // Update comment counts on videos
  const videoCounts = new Map<string, number>();
  for (const c of raw) {
    videoCounts.set(c.video_id, (videoCounts.get(c.video_id) || 0) + 1);
  }

  for (const [videoId, count] of videoCounts) {
    await supabase
      .from('ct_videos')
      .update({ comment_count: count })
      .eq('video_id', videoId);
  }

  console.log(`Imported ${imported} comments, updated counts for ${videoCounts.size} videos`);
  return imported;
}

// ─── Fetch fresh data via yt-dlp (optional) ──────────────────────────────────
async function fetchFreshData(): Promise<void> {
  console.log('\nFetching fresh data via yt-dlp...');

  // Get all video IDs from database
  const { data: videos } = await supabase
    .from('ct_videos')
    .select('video_id');

  if (!videos || videos.length === 0) {
    console.log('No videos in database. Import first.');
    return;
  }

  let updated = 0;
  for (const { video_id } of videos) {
    try {
      const result = execSync(
        `yt-dlp --dump-json --no-download "https://youtube.com/watch?v=${video_id}" 2>/dev/null`,
        { encoding: 'utf-8', timeout: 30_000 }
      );

      const info = JSON.parse(result);

      await supabase
        .from('ct_videos')
        .update({
          title: info.title || undefined,
          views: info.view_count || 0,
          likes: info.like_count || 0,
          comment_count: info.comment_count || 0,
          duration: info.duration || 0,
          published_at: info.upload_date
            ? `${info.upload_date.slice(0, 4)}-${info.upload_date.slice(4, 6)}-${info.upload_date.slice(6, 8)}`
            : null,
          metadata: {
            thumbnail: info.thumbnail,
            description: info.description?.slice(0, 500),
            tags: info.tags?.slice(0, 20),
          },
        })
        .eq('video_id', video_id);

      updated++;
      if (updated % 10 === 0) {
        console.log(`  Updated ${updated}/${videos.length} videos...`);
      }
    } catch (err) {
      console.warn(`  Skipping ${video_id}: ${(err as Error).message?.slice(0, 80)}`);
    }
  }

  console.log(`Updated ${updated}/${videos.length} videos with fresh data`);
}

// ─── Generate content ideas (placeholder) ────────────────────────────────────
async function generateIdeas(): Promise<void> {
  console.log('\nGenerating content ideas from comments...');

  // Get all comments
  const { data: comments } = await supabase
    .from('ct_comments')
    .select('text, video_id, author, likes')
    .order('likes', { ascending: false })
    .limit(500);

  if (!comments || comments.length === 0) {
    console.log('No comments found. Import first.');
    return;
  }

  // Simple keyword-based idea generation
  // In production, this would use Gemini API
  const questionComments = comments.filter((c) =>
    c.text.includes('?') || c.text.toLowerCase().includes('como') || c.text.toLowerCase().includes('pode')
  );

  const problemComments = comments.filter((c) =>
    c.text.toLowerCase().includes('erro') ||
    c.text.toLowerCase().includes('problema') ||
    c.text.toLowerCase().includes('não funciona') ||
    c.text.toLowerCase().includes('defeito')
  );

  const requestComments = comments.filter((c) =>
    c.text.toLowerCase().includes('faz um vídeo') ||
    c.text.toLowerCase().includes('faz uma aula') ||
    c.text.toLowerCase().includes('pode fazer') ||
    c.text.toLowerCase().includes('gostaria')
  );

  const ideas = [
    ...extractIdeas(questionComments, 'Pergunta frequente nos comentários', 'alta', 4),
    ...extractIdeas(problemComments, 'Problema reportado por alunos', 'alta', 3),
    ...extractIdeas(requestComments, 'Solicitação direta de alunos', 'media', 3),
  ].slice(0, 10);

  // Save to ct_insights
  const { error } = await supabase
    .from('ct_insights')
    .upsert({
      type: 'content_ideas',
      data: ideas,
      generated_at: new Date().toISOString(),
    }, { onConflict: 'type' });

  if (error) {
    console.error('Error saving ideas:', error.message);
  } else {
    console.log(`Saved ${ideas.length} content ideas`);
  }
}

function extractIdeas(
  comments: Array<{ text: string; video_id: string; author: string; likes: number }>,
  source: string,
  priority: 'alta' | 'media' | 'baixa',
  maxIdeas: number,
) {
  // Group by common keywords/themes
  const seen = new Set<string>();
  const ideas: Array<{
    title: string;
    justification: string;
    priority: 'alta' | 'media' | 'baixa';
    source_comments: string[];
  }> = [];

  for (const c of comments) {
    if (ideas.length >= maxIdeas) break;

    // Skip owner comments and very short ones
    if (c.author === '@lawhander' || c.text.length < 20) continue;

    // Simple dedup by first 30 chars
    const key = c.text.slice(0, 30).toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);

    // Generate title from comment theme
    const title = generateTitle(c.text);
    if (!title) continue;

    ideas.push({
      title,
      justification: `${source}: "${c.text.slice(0, 120)}${c.text.length > 120 ? '...' : ''}"`,
      priority,
      source_comments: [c.text.slice(0, 200)],
    });
  }

  return ideas;
}

function generateTitle(commentText: string): string | null {
  const text = commentText.toLowerCase();

  // Match error codes
  const errorMatch = text.match(/erro\s+([a-z0-9]+)/i);
  if (errorMatch) return `Como resolver Erro ${errorMatch[1].toUpperCase()} — Diagnóstico completo`;

  // Match "como" questions
  const comoMatch = text.match(/como\s+(.{10,50}?)(\?|$)/i);
  if (comoMatch) return `Como ${comoMatch[1].trim()} — Passo a passo`;

  // Match brand + problem
  const brands = ['samsung', 'lg', 'midea', 'springer', 'consul', 'electrolux', 'fujitsu', 'philco', 'carrier', 'daikin'];
  const brand = brands.find((b) => text.includes(b));
  if (brand) return `${brand.charAt(0).toUpperCase() + brand.slice(1)} Inverter — Diagnóstico e reparo`;

  // Match component questions
  const components = ['compressor', 'placa', 'sensor', 'capacitor', 'ipm', 'inversor', 'válvula'];
  const component = components.find((c) => text.includes(c));
  if (component) return `Tudo sobre ${component.charAt(0).toUpperCase() + component.slice(1)} — Testes e substituição`;

  return null;
}

// ─── Main ────────────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const shouldFetch = args.includes('--fetch');
  const shouldGenerateIdeas = args.includes('--ideas');

  console.log('=== Content Studio — YouTube Data Updater ===\n');

  // Step 1: Import existing data
  const videoCount = await importVideos();
  const commentCount = await importComments();

  // Step 2: Fetch fresh data if requested
  if (shouldFetch) {
    await fetchFreshData();
  }

  // Step 3: Generate ideas
  if (shouldGenerateIdeas || commentCount > 0) {
    await generateIdeas();
  }

  console.log('\nDone!');
  console.log(`  Videos: ${videoCount}`);
  console.log(`  Comments: ${commentCount}`);
}

main().catch(console.error);

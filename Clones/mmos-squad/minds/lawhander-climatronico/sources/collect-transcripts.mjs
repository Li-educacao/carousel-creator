/**
 * Batch YouTube Transcript Collector for Mind Clone Pipeline
 * Uses yt-dlp to download auto-captions (PT) from @lawhander channel
 * Priority: Podcasts > Tutorials > Medium > Shorts (by views)
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync } from 'fs';
import { join } from 'path';

const VIDEOS_CACHE = '/Users/lawhander/Projetos com IA/climatronico-blog/data/videos-cache.json';
const OUTPUT_DIR = '/Users/lawhander/Projetos com IA/Clones/mmos/outputs/minds/lawhander-climatronico/sources/downloads/youtube';
const PROGRESS_FILE = join(OUTPUT_DIR, '_progress.json');
const TMP_DIR = '/tmp/mmos-transcripts';

// No limits — collect ALL videos from the channel
const LIMITS = {
  podcasts: Infinity,
  tutorials: Infinity,
  medium: Infinity,
  shorts: Infinity
};

const DELAY_MS = 500;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function loadProgress() {
  if (existsSync(PROGRESS_FILE)) {
    return JSON.parse(readFileSync(PROGRESS_FILE, 'utf-8'));
  }
  return { collected: [], failed: [], totalWords: 0 };
}

function saveProgress(progress) {
  writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

function sanitizeFilename(title) {
  return title
    .replace(/[^a-zA-Z0-9\u00C0-\u017F\s-]/g, '')
    .replace(/\s+/g, '-')
    .toLowerCase()
    .slice(0, 80);
}

function fetchTranscriptViaYtdlp(videoId) {
  mkdirSync(TMP_DIR, { recursive: true });
  const outTemplate = join(TMP_DIR, videoId);

  try {
    // Download auto-captions in PT, save as SRT
    execSync(
      `yt-dlp --skip-download --write-auto-sub --sub-lang pt --sub-format srt --convert-subs srt -o "${outTemplate}" "https://www.youtube.com/watch?v=${videoId}" 2>/dev/null`,
      { timeout: 30000 }
    );

    // Find the generated subtitle file
    const srtFile = `${outTemplate}.pt.srt`;
    if (!existsSync(srtFile)) {
      return null;
    }

    const srtContent = readFileSync(srtFile, 'utf-8');

    // Parse SRT: remove timestamps, numbers, and empty lines
    const text = srtContent
      .split('\n')
      .filter(line => {
        const trimmed = line.trim();
        if (!trimmed) return false;
        if (/^\d+$/.test(trimmed)) return false;
        if (/\d{2}:\d{2}:\d{2}/.test(trimmed)) return false;
        return true;
      })
      .map(line => line.replace(/<[^>]*>/g, '').trim())
      .filter(Boolean)
      .join(' ')
      // Remove duplicate phrases from auto-captions
      .replace(/(.{20,}?)\1+/g, '$1');

    // Cleanup
    try { unlinkSync(srtFile); } catch {}

    return text.length > 50 ? text : null;
  } catch {
    return null;
  }
}

async function main() {
  const cache = JSON.parse(readFileSync(VIDEOS_CACHE, 'utf-8'));
  const allVideos = cache.videos;

  const podcasts = allVideos.filter(v => v.durationMinutes >= 30).sort((a, b) => b.viewCount - a.viewCount);
  const tutorials = allVideos.filter(v => v.durationMinutes >= 5 && v.durationMinutes < 30).sort((a, b) => b.viewCount - a.viewCount);
  const medium = allVideos.filter(v => v.durationMinutes >= 2 && v.durationMinutes < 5).sort((a, b) => b.viewCount - a.viewCount);
  const shorts = allVideos.filter(v => v.durationMinutes <= 1).sort((a, b) => b.viewCount - a.viewCount);

  const queue = [
    ...podcasts.slice(0, LIMITS.podcasts).map(v => ({ ...v, category: 'podcasts' })),
    ...tutorials.slice(0, LIMITS.tutorials).map(v => ({ ...v, category: 'tutorials' })),
    ...medium.slice(0, LIMITS.medium).map(v => ({ ...v, category: 'medium' })),
    ...shorts.slice(0, LIMITS.shorts).map(v => ({ ...v, category: 'shorts' })),
  ];

  console.log(`\n📋 Collection Plan (via yt-dlp):`);
  console.log(`  Podcasts (>=30min): ${Math.min(podcasts.length, LIMITS.podcasts)} of ${podcasts.length}`);
  console.log(`  Tutorials (5-30min): ${Math.min(tutorials.length, LIMITS.tutorials)} of ${tutorials.length}`);
  console.log(`  Medium (2-5min): ${Math.min(medium.length, LIMITS.medium)} of ${medium.length}`);
  console.log(`  Shorts (<=1min): ${Math.min(shorts.length, LIMITS.shorts)} of ${shorts.length}`);
  console.log(`  TOTAL: ${queue.length} videos\n`);

  for (const cat of ['podcasts', 'tutorials', 'medium', 'shorts']) {
    mkdirSync(join(OUTPUT_DIR, cat), { recursive: true });
  }

  const progress = loadProgress();
  const alreadyDone = new Set([...progress.collected, ...progress.failed]);

  let collected = progress.collected.length;
  let failed = progress.failed.length;
  let totalWords = progress.totalWords;

  for (let i = 0; i < queue.length; i++) {
    const video = queue[i];

    if (alreadyDone.has(video.id)) {
      continue;
    }

    const pct = ((collected + failed) / queue.length * 100).toFixed(1);
    process.stdout.write(`[${pct}%] (${collected}/${queue.length}) ${video.category} | ${video.id} | ${video.title.slice(0, 55)}...`);

    const transcript = fetchTranscriptViaYtdlp(video.id);

    if (transcript) {
      const filename = sanitizeFilename(video.title) + '.md';
      const filepath = join(OUTPUT_DIR, video.category, filename);

      const content = [
        `# ${video.title}`,
        '',
        `- **Video ID:** ${video.id}`,
        `- **URL:** https://www.youtube.com/watch?v=${video.id}`,
        `- **Duration:** ${video.durationMinutes} min`,
        `- **Views:** ${video.viewCount.toLocaleString()}`,
        `- **Published:** ${video.publishedAt}`,
        `- **Category:** ${video.category}`,
        '',
        '---',
        '',
        '## Transcript',
        '',
        transcript,
      ].join('\n');

      writeFileSync(filepath, content);

      const wordCount = transcript.split(/\s+/).length;
      totalWords += wordCount;
      collected++;
      progress.collected.push(video.id);
      progress.totalWords = totalWords;

      console.log(` ✓ ${wordCount} words`);
    } else {
      failed++;
      progress.failed.push(video.id);
      console.log(` ✗ no captions`);
    }

    saveProgress(progress);
    await sleep(DELAY_MS);
  }

  console.log(`\n✅ Collection Complete!`);
  console.log(`  Collected: ${collected}`);
  console.log(`  Failed: ${failed}`);
  console.log(`  Total words: ${totalWords.toLocaleString()}`);

  const summary = {
    mind_name: 'lawhander-climatronico',
    collection_date: new Date().toISOString(),
    total_videos_in_channel: allVideos.length,
    total_collected: collected,
    total_failed: failed,
    total_words: totalWords,
    by_category: {
      podcasts: progress.collected.filter(id => podcasts.some(v => v.id === id)).length,
      tutorials: progress.collected.filter(id => tutorials.some(v => v.id === id)).length,
      medium: progress.collected.filter(id => medium.some(v => v.id === id)).length,
      shorts: progress.collected.filter(id => shorts.some(v => v.id === id)).length,
    }
  };
  writeFileSync(join(OUTPUT_DIR, '_summary.json'), JSON.stringify(summary, null, 2));
}

main().catch(console.error);

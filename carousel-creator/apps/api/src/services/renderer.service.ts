import { createCanvas, loadImage, registerFont, type Canvas, type CanvasRenderingContext2D } from 'canvas';
import path from 'path';
import { fileURLToPath } from 'url';
import { supabaseAdmin } from '../lib/supabase.js';
import { BRAND_COLORS, FONT_FAMILIES } from '@carousel/shared';
import { getImagenService, type GeneratedImage } from './imagen.service.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FONTS_DIR = path.resolve(__dirname, '../../../../fonts');

// ─── Font registration (run once at module load) ───────────────────────────────

let fontsRegistered = false;

function ensureFontsRegistered(): void {
  if (fontsRegistered) return;
  registerFont(path.join(FONTS_DIR, 'MADETommy-ExtraBold.otf'), { family: 'MADE Tommy ExtraBold' });
  registerFont(path.join(FONTS_DIR, 'MADETommy-Bold.otf'), { family: 'MADE Tommy Bold' });
  registerFont(path.join(FONTS_DIR, 'MADETommy-Medium.otf'), { family: 'MADE Tommy Medium' });
  registerFont(path.join(FONTS_DIR, 'MADETommy-Regular.otf'), { family: 'MADE Tommy Regular' });
  fontsRegistered = true;
}

// ─── Types ────────────────────────────────────────────────────────────────────

export interface SlideData {
  id: string;
  carousel_id: string;
  position: number;
  headline: string;
  body_text: string;
  cta_text?: string | null;
  image_url?: string | null;
  bg_color?: string | null;
}

export interface TemplateConfig {
  accent_color?: string;
  bg_color?: string;
  gradient?: boolean;
  format?: 'square' | 'portrait';
}

export interface RenderResult {
  position: number;
  url: string;
}

// ─── Layout type determination ─────────────────────────────────────────────────

type SlideLayout = 'cover' | 'cta' | 'content' | 'tip' | 'testimonial';

function determineLayout(position: number, totalSlides: number, templateType: string): SlideLayout {
  if (position === 1) return 'cover';
  if (position === totalSlides) return 'cta';
  if (templateType === 'tips_list') return 'tip';
  if (templateType === 'social_proof') return 'testimonial';
  return 'content';
}

// ─── Draw helpers ─────────────────────────────────────────────────────────────

function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  radius: number
): void {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
}

function wrapText(
  ctx: CanvasRenderingContext2D,
  text: string,
  maxWidth: number
): string[] {
  if (!text) return [];
  const words = text.split(' ');
  const lines: string[] = [];
  let currentLine = '';

  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    const { width } = ctx.measureText(testLine);
    if (width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);
  return lines;
}

function drawWrappedText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number,
  align: string = 'left'
): number {
  const lines = wrapText(ctx, text, maxWidth);
  ctx.textAlign = align as CanvasRenderingContext2D['textAlign'];
  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i], x, y + i * lineHeight);
  }
  return y + lines.length * lineHeight;
}

// ─── Slide renderer ────────────────────────────────────────────────────────────

async function renderSlide(
  slide: SlideData,
  layout: SlideLayout,
  config: TemplateConfig,
  aiBackground?: GeneratedImage | null
): Promise<Buffer> {
  ensureFontsRegistered();

  const format = config.format ?? 'square';
  const WIDTH = 1080;
  const HEIGHT = format === 'portrait' ? 1350 : 1080;
  const PADDING = 80;
  const CONTENT_WIDTH = WIDTH - PADDING * 2;

  const accentColor = config.accent_color ?? BRAND_COLORS.blue;
  const bgColor = config.bg_color ?? BRAND_COLORS.black;

  const canvas: Canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext('2d');

  // ── Background: AI-generated or solid color ──
  if (aiBackground) {
    try {
      const img = await loadImage(aiBackground.buffer);
      ctx.drawImage(img, 0, 0, WIDTH, HEIGHT);

      // Dark overlay for text readability
      ctx.fillStyle = 'rgba(1, 1, 1, 0.55)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      // Gradient overlay from bottom for extra contrast
      const textGrad = ctx.createLinearGradient(0, HEIGHT * 0.4, 0, HEIGHT);
      textGrad.addColorStop(0, 'rgba(1, 1, 1, 0)');
      textGrad.addColorStop(1, 'rgba(1, 1, 1, 0.6)');
      ctx.fillStyle = textGrad;
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
    } catch (err) {
      console.warn(`[renderer] Failed to load AI background, using solid color:`, (err as Error).message);
      ctx.fillStyle = bgColor;
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
    }
  } else {
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // ── Optional gradient overlay (only for solid backgrounds) ──
    if (config.gradient) {
      const grad = ctx.createLinearGradient(0, 0, 0, HEIGHT);
      grad.addColorStop(0, `${accentColor}20`);
      grad.addColorStop(1, `${bgColor}ff`);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
    }
  }

  // ── Brand stripe ──
  ctx.fillStyle = accentColor;
  ctx.fillRect(0, 0, 6, HEIGHT);

  // ── Layout-specific rendering ──
  switch (layout) {
    case 'cover':
      renderCoverSlide(ctx, slide, accentColor, PADDING, CONTENT_WIDTH, WIDTH, HEIGHT);
      break;
    case 'cta':
      renderCtaSlide(ctx, slide, accentColor, PADDING, CONTENT_WIDTH, WIDTH, HEIGHT);
      break;
    case 'tip':
      renderTipSlide(ctx, slide, accentColor, PADDING, CONTENT_WIDTH, WIDTH, HEIGHT);
      break;
    case 'testimonial':
      renderTestimonialSlide(ctx, slide, accentColor, PADDING, CONTENT_WIDTH, WIDTH, HEIGHT);
      break;
    default:
      renderContentSlide(ctx, slide, accentColor, PADDING, CONTENT_WIDTH, WIDTH, HEIGHT);
  }

  // ── Position badge (bottom right) ──
  const badgeX = WIDTH - PADDING;
  const badgeY = HEIGHT - PADDING;
  ctx.fillStyle = `${accentColor}30`;
  drawRoundedRect(ctx, badgeX - 60, badgeY - 32, 60, 32, 8);
  ctx.fill();
  ctx.fillStyle = accentColor;
  ctx.font = `bold 18px "${FONT_FAMILIES.heading}"`;
  ctx.textAlign = 'center';
  ctx.fillText(`${slide.position}`, badgeX - 30, badgeY - 10);

  return canvas.toBuffer('image/png');
}

function renderCoverSlide(
  ctx: CanvasRenderingContext2D,
  slide: SlideData,
  accentColor: string,
  padding: number,
  contentWidth: number,
  _width: number,
  height: number
): void {
  // Large decorative circle
  ctx.fillStyle = `${accentColor}15`;
  ctx.beginPath();
  ctx.arc(_width * 0.8, height * 0.25, 300, 0, Math.PI * 2);
  ctx.fill();

  // Small accent circle
  ctx.fillStyle = `${accentColor}25`;
  ctx.beginPath();
  ctx.arc(_width * 0.15, height * 0.75, 150, 0, Math.PI * 2);
  ctx.fill();

  // Main headline — large, centered
  const centerY = height * 0.45;
  ctx.fillStyle = BRAND_COLORS.white;
  ctx.font = `bold 72px "${FONT_FAMILIES.heading}"`;
  const lines = wrapText(ctx, slide.headline, contentWidth);
  const lineHeight = 84;
  const totalHeight = lines.length * lineHeight;
  const startY = centerY - totalHeight / 2 + 72;
  ctx.textAlign = 'left';
  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i], padding, startY + i * lineHeight);
  }

  // Body text below headline
  if (slide.body_text) {
    ctx.fillStyle = BRAND_COLORS.gray;
    ctx.font = `400 32px "${FONT_FAMILIES.body}"`;
    drawWrappedText(
      ctx,
      slide.body_text,
      padding,
      startY + totalHeight + 24,
      contentWidth,
      42
    );
  }

  // Bottom accent line
  ctx.fillStyle = accentColor;
  ctx.fillRect(padding, height * 0.85, 80, 4);
}

function renderCtaSlide(
  ctx: CanvasRenderingContext2D,
  slide: SlideData,
  accentColor: string,
  padding: number,
  contentWidth: number,
  width: number,
  height: number
): void {
  // Background gradient for CTA emphasis
  const grad = ctx.createLinearGradient(0, 0, 0, height);
  grad.addColorStop(0, `${accentColor}30`);
  grad.addColorStop(0.5, `${accentColor}10`);
  grad.addColorStop(1, '#00000000');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);

  const centerX = width / 2;
  const midY = height * 0.4;

  // Headline
  ctx.fillStyle = BRAND_COLORS.white;
  ctx.font = `bold 64px "${FONT_FAMILIES.heading}"`;
  const headlineLines = wrapText(ctx, slide.headline, contentWidth);
  const lineH = 76;
  const startY = midY - (headlineLines.length * lineH) / 2 + 64;
  ctx.textAlign = 'center';
  for (let i = 0; i < headlineLines.length; i++) {
    ctx.fillText(headlineLines[i], centerX, startY + i * lineH);
  }

  // Body text
  if (slide.body_text) {
    ctx.fillStyle = BRAND_COLORS.gray;
    ctx.font = `400 30px "${FONT_FAMILIES.body}"`;
    drawWrappedText(
      ctx,
      slide.body_text,
      centerX,
      startY + headlineLines.length * lineH + 20,
      contentWidth,
      40,
      'center'
    );
  }

  // CTA button
  if (slide.cta_text) {
    const btnY = height * 0.72;
    const btnText = slide.cta_text;
    ctx.font = `bold 32px "${FONT_FAMILIES.subtitle}"`;
    const btnWidth = Math.min(ctx.measureText(btnText).width + 80, contentWidth);
    const btnHeight = 72;
    const btnX = centerX - btnWidth / 2;

    ctx.fillStyle = accentColor;
    drawRoundedRect(ctx, btnX, btnY, btnWidth, btnHeight, 36);
    ctx.fill();

    ctx.fillStyle = BRAND_COLORS.white;
    ctx.textAlign = 'center';
    ctx.fillText(btnText, centerX, btnY + btnHeight / 2 + 12);
  }
}

function renderContentSlide(
  ctx: CanvasRenderingContext2D,
  slide: SlideData,
  accentColor: string,
  padding: number,
  contentWidth: number,
  _width: number,
  height: number
): void {
  // Headline
  ctx.fillStyle = accentColor;
  ctx.font = `bold 16px "${FONT_FAMILIES.subtitle}"`;
  ctx.textAlign = 'left';
  ctx.fillText(`SLIDE ${slide.position}`, padding, 120);

  ctx.fillStyle = BRAND_COLORS.white;
  ctx.font = `bold 56px "${FONT_FAMILIES.heading}"`;
  const headlineLines = wrapText(ctx, slide.headline, contentWidth);
  const lineH = 68;
  const startY = 180;
  for (let i = 0; i < headlineLines.length; i++) {
    ctx.fillText(headlineLines[i], padding, startY + i * lineH);
  }

  // Separator
  const sepY = startY + headlineLines.length * lineH + 28;
  ctx.fillStyle = accentColor;
  ctx.fillRect(padding, sepY, 60, 3);

  // Body text
  if (slide.body_text) {
    ctx.fillStyle = BRAND_COLORS.white;
    ctx.font = `400 34px "${FONT_FAMILIES.body}"`;
    drawWrappedText(ctx, slide.body_text, padding, sepY + 48, contentWidth, 50);
  }

  // CTA if present
  if (slide.cta_text) {
    const ctaY = height - padding - 72;
    ctx.fillStyle = `${accentColor}20`;
    drawRoundedRect(ctx, padding, ctaY, contentWidth, 56, 8);
    ctx.fill();
    ctx.fillStyle = accentColor;
    ctx.font = `bold 26px "${FONT_FAMILIES.subtitle}"`;
    ctx.textAlign = 'left';
    ctx.fillText(slide.cta_text, padding + 24, ctaY + 38);
  }
}

function renderTipSlide(
  ctx: CanvasRenderingContext2D,
  slide: SlideData,
  accentColor: string,
  padding: number,
  contentWidth: number,
  width: number,
  height: number
): void {
  // Large number in background
  ctx.fillStyle = `${accentColor}12`;
  ctx.font = `bold 400px "${FONT_FAMILIES.heading}"`;
  ctx.textAlign = 'right';
  ctx.fillText(String(slide.position), width - 20, height * 0.7);

  // "DICA" label
  ctx.fillStyle = accentColor;
  ctx.font = `bold 20px "${FONT_FAMILIES.subtitle}"`;
  ctx.textAlign = 'left';
  ctx.fillText('DICA', padding, 130);

  // Number badge
  ctx.fillStyle = accentColor;
  ctx.font = `bold 80px "${FONT_FAMILIES.heading}"`;
  ctx.fillText(`#${slide.position}`, padding, 260);

  // Headline
  ctx.fillStyle = BRAND_COLORS.white;
  ctx.font = `bold 50px "${FONT_FAMILIES.heading}"`;
  const lines = wrapText(ctx, slide.headline, contentWidth);
  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i], padding, 330 + i * 62);
  }

  // Separator
  const sepY = 330 + lines.length * 62 + 24;
  ctx.fillStyle = accentColor;
  ctx.fillRect(padding, sepY, 60, 3);

  // Body text
  if (slide.body_text) {
    ctx.fillStyle = BRAND_COLORS.gray;
    ctx.font = `400 32px "${FONT_FAMILIES.body}"`;
    drawWrappedText(ctx, slide.body_text, padding, sepY + 44, contentWidth, 46);
  }
}

function renderTestimonialSlide(
  ctx: CanvasRenderingContext2D,
  slide: SlideData,
  accentColor: string,
  padding: number,
  contentWidth: number,
  width: number,
  height: number
): void {
  const centerX = width / 2;

  // Large quote mark
  ctx.fillStyle = `${accentColor}20`;
  ctx.font = `bold 200px serif`;
  ctx.textAlign = 'center';
  ctx.fillText('"', centerX, height * 0.3);

  // Headline as quote
  ctx.fillStyle = BRAND_COLORS.white;
  ctx.font = `400 40px "${FONT_FAMILIES.body}"`;
  ctx.textAlign = 'center';
  const lines = wrapText(ctx, slide.headline, contentWidth - 40);
  const lineH = 56;
  const startY = height * 0.45;
  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i], centerX, startY + i * lineH);
  }

  // Accent line
  const lineY = startY + lines.length * lineH + 32;
  ctx.fillStyle = accentColor;
  ctx.fillRect(centerX - 40, lineY, 80, 3);

  // Body text (attribution / context)
  if (slide.body_text) {
    ctx.fillStyle = BRAND_COLORS.gray;
    ctx.font = `400 28px "${FONT_FAMILIES.body}"`;
    drawWrappedText(ctx, slide.body_text, centerX, lineY + 40, contentWidth, 40, 'center');
  }
}

// ─── Upload helper ─────────────────────────────────────────────────────────────

async function uploadSlideImage(
  buffer: Buffer,
  userId: string,
  carouselId: string,
  position: number
): Promise<string | null> {
  const storagePath = `${userId}/${carouselId}/slide-${position}.png`;

  const { error } = await supabaseAdmin.storage
    .from('carousel-assets')
    .upload(storagePath, buffer, {
      contentType: 'image/png',
      upsert: true,
    });

  if (error) {
    console.error(`[renderer] Storage upload error for slide ${position}:`, error.message);
    return null;
  }

  // Create a signed URL valid for 1 year
  const { data: signedData, error: signError } = await supabaseAdmin.storage
    .from('carousel-assets')
    .createSignedUrl(storagePath, 60 * 60 * 24 * 365);

  if (signError || !signedData?.signedUrl) {
    console.error(`[renderer] Signed URL error for slide ${position}:`, signError?.message);
    return null;
  }

  return signedData.signedUrl;
}

// ─── Public API ───────────────────────────────────────────────────────────────

export async function renderCarouselById(carouselId: string): Promise<RenderResult[]> {
  // Fetch carousel
  const { data: carousel, error: carouselError } = await supabaseAdmin
    .from('carousels')
    .select('*')
    .eq('id', carouselId)
    .single();

  if (carouselError || !carousel) {
    throw new Error(`Carrossel não encontrado: ${carouselError?.message ?? 'not found'}`);
  }

  // Fetch slides
  const { data: slides, error: slidesError } = await supabaseAdmin
    .from('carousel_slides')
    .select('*')
    .eq('carousel_id', carouselId)
    .order('position');

  if (slidesError || !slides) {
    throw new Error(`Falha ao buscar slides: ${slidesError?.message ?? 'not found'}`);
  }

  // Fetch template if available
  let templateConfig: TemplateConfig = {
    accent_color: BRAND_COLORS.blue,
    bg_color: BRAND_COLORS.black,
    gradient: true,
    format: 'square',
  };

  // Use bg_color from first slide if set, or carousel's template_type defaults
  const templateType: string = (carousel as Record<string, unknown>)['template_type'] as string ?? 'educational';
  const theme: string = (carousel as Record<string, unknown>)['theme'] as string ?? '';
  const totalSlides = slides.length;

  // Generate AI backgrounds for all slides (Imagen 4)
  let aiBackgrounds = new Map<number, GeneratedImage>();
  try {
    const imagenService = getImagenService();
    console.log(`[renderer] Generating AI backgrounds for ${totalSlides} slides...`);
    aiBackgrounds = await imagenService.generateCarouselBackgrounds(theme, templateType, totalSlides);
    console.log(`[renderer] AI backgrounds generated: ${aiBackgrounds.size}/${totalSlides}`);
  } catch (err) {
    console.warn(`[renderer] AI background generation failed, using solid colors:`, (err as Error).message);
  }

  const results: RenderResult[] = [];

  for (const slide of slides as SlideData[]) {
    const layout = determineLayout(slide.position, totalSlides, templateType);
    const aiBg = aiBackgrounds.get(slide.position) ?? null;
    const buffer = await renderSlide(slide, layout, templateConfig, aiBg);

    const userId: string = (carousel as Record<string, unknown>)['user_id'] as string;
    const url = await uploadSlideImage(buffer, userId, carouselId, slide.position);

    if (url) {
      // Update slide with image_url
      await supabaseAdmin
        .from('carousel_slides')
        .update({ image_url: url })
        .eq('id', slide.id);

      results.push({ position: slide.position, url });
    } else {
      // Still include in results but with empty url for partial failure handling
      results.push({ position: slide.position, url: '' });
    }
  }

  // Update carousel status
  await supabaseAdmin
    .from('carousels')
    .update({ status: 'images_generated' })
    .eq('id', carouselId);

  return results;
}

export async function renderSingleSlide(
  carouselId: string,
  position: number
): Promise<RenderResult> {
  // Fetch carousel + slide
  const { data: carousel, error: carouselError } = await supabaseAdmin
    .from('carousels')
    .select('*')
    .eq('id', carouselId)
    .single();

  if (carouselError || !carousel) {
    throw new Error(`Carrossel não encontrado: ${carouselError?.message ?? 'not found'}`);
  }

  const { data: slide, error: slideError } = await supabaseAdmin
    .from('carousel_slides')
    .select('*')
    .eq('carousel_id', carouselId)
    .eq('position', position)
    .single();

  if (slideError || !slide) {
    throw new Error(`Slide não encontrado: ${slideError?.message ?? 'not found'}`);
  }

  // Get total count for layout determination
  const { count } = await supabaseAdmin
    .from('carousel_slides')
    .select('id', { count: 'exact', head: true })
    .eq('carousel_id', carouselId);

  const totalSlides = count ?? 1;
  const templateType: string = (carousel as Record<string, unknown>)['template_type'] as string ?? 'educational';
  const theme: string = (carousel as Record<string, unknown>)['theme'] as string ?? '';
  const layout = determineLayout(position, totalSlides, templateType);

  const templateConfig: TemplateConfig = {
    accent_color: BRAND_COLORS.blue,
    bg_color: BRAND_COLORS.black,
    gradient: true,
    format: 'square',
  };

  // Generate AI background for this slide
  let aiBg: GeneratedImage | null = null;
  try {
    const imagenService = getImagenService();
    let slideRole: 'cover' | 'content' | 'cta' = 'content';
    if (position === 1) slideRole = 'cover';
    else if (position === totalSlides) slideRole = 'cta';
    aiBg = await imagenService.generateSlideBackground(theme, slideRole, templateType, position, totalSlides);
  } catch (err) {
    console.warn(`[renderer] AI background failed for slide ${position}, using solid color:`, (err as Error).message);
  }

  const buffer = await renderSlide(slide as SlideData, layout, templateConfig, aiBg);
  const userId: string = (carousel as Record<string, unknown>)['user_id'] as string;
  const url = await uploadSlideImage(buffer, userId, carouselId, position);

  if (url) {
    await supabaseAdmin
      .from('carousel_slides')
      .update({ image_url: url })
      .eq('id', (slide as SlideData).id);
  }

  return { position, url: url ?? '' };
}

import { GoogleGenAI } from '@google/genai';
import { config } from '../config.js';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface GeneratedImage {
  buffer: Buffer;
  mimeType: string;
}

type SlideRole = 'cover' | 'content' | 'cta';

// ─── Constants ────────────────────────────────────────────────────────────────

// Imagen 4 Ultra — highest quality for carousel backgrounds
const IMAGE_MODEL = 'imagen-4.0-generate-001';

// Brand visual identity keywords for consistent generation
const BRAND_STYLE = [
  'dark background',
  'deep black #010101',
  'electric blue #0084C8 accent',
  'professional tech aesthetic',
  'clean modern minimal',
  'high contrast',
  'no text no letters no words no watermark',
].join(', ');

// ─── Prompt builders ──────────────────────────────────────────────────────────

function buildBackgroundPrompt(
  theme: string,
  slideRole: SlideRole,
  templateType: string,
  position: number,
  totalSlides: number,
): string {
  const roleDescriptions: Record<SlideRole, string> = {
    cover: 'eye-catching hero background with dramatic lighting and depth, central focus area for overlay text',
    content: 'subtle atmospheric background with dark tones, large clean area for text overlay',
    cta: 'energetic background with blue accent glow, strong visual pull, clean center for call-to-action button',
  };

  const templateVibes: Record<string, string> = {
    educational: 'technical, electronic circuit boards, PCB traces, solder points, multimeter, oscilloscope, subtle tech elements',
    social_proof: 'warm and trustworthy, subtle human connection, achievement feel, clean workspace',
    tips_list: 'organized, structured, numbered feel, clean tech workspace, tools neatly arranged',
    cover_cta: 'bold and impactful, dramatic lighting, strong visual contrast, premium feel',
  };

  const vibe = templateVibes[templateType] ?? templateVibes.educational;
  const roleDesc = roleDescriptions[slideRole];

  return [
    `Professional Instagram carousel background image for air conditioning and electronics repair education brand.`,
    `Theme: "${theme}".`,
    `Slide ${position} of ${totalSlides} — ${slideRole} slide.`,
    `Visual direction: ${roleDesc}.`,
    `Visual elements: ${vibe}.`,
    `Style: ${BRAND_STYLE}.`,
    `CRITICAL: Do NOT include any text, letters, numbers, words, watermarks, or logos in the image.`,
    `The image must be a pure background/visual — all text will be overlaid programmatically.`,
    `Aspect ratio: 1:1, 1080x1080 pixels equivalent quality.`,
  ].join(' ');
}

// ─── Service ──────────────────────────────────────────────────────────────────

class ImagenService {
  private ai: GoogleGenAI;

  constructor() {
    if (!config.geminiApiKey) {
      throw new Error('GEMINI_API_KEY is not configured');
    }
    this.ai = new GoogleGenAI({ apiKey: config.geminiApiKey });
  }

  /**
   * Generate a background image for a single slide using Imagen 4.
   */
  async generateSlideBackground(
    theme: string,
    slideRole: SlideRole,
    templateType: string,
    position: number,
    totalSlides: number,
  ): Promise<GeneratedImage> {
    const prompt = buildBackgroundPrompt(theme, slideRole, templateType, position, totalSlides);

    console.log(`[Imagen] Generating background for slide ${position}/${totalSlides} (${slideRole})...`);

    const response = await this.ai.models.generateImages({
      model: IMAGE_MODEL,
      prompt,
      config: {
        numberOfImages: 1,
      },
    });

    const generated = response.generatedImages;
    if (!generated || generated.length === 0) {
      throw new Error(`Imagen returned no images for slide ${position}`);
    }

    const imgBytes = generated[0].image?.imageBytes;
    if (!imgBytes) {
      throw new Error(`Imagen returned empty image data for slide ${position}`);
    }

    const buffer = Buffer.from(imgBytes, 'base64');
    console.log(`[Imagen] Slide ${position} background generated (${(buffer.length / 1024).toFixed(0)} KB)`);

    return { buffer, mimeType: 'image/png' };
  }

  /**
   * Generate backgrounds for all slides in a carousel.
   * Processes sequentially to respect API rate limits.
   */
  async generateCarouselBackgrounds(
    theme: string,
    templateType: string,
    totalSlides: number,
  ): Promise<Map<number, GeneratedImage>> {
    const results = new Map<number, GeneratedImage>();

    for (let pos = 1; pos <= totalSlides; pos++) {
      let slideRole: SlideRole = 'content';
      if (pos === 1) slideRole = 'cover';
      else if (pos === totalSlides) slideRole = 'cta';

      try {
        const image = await this.generateSlideBackground(
          theme,
          slideRole,
          templateType,
          pos,
          totalSlides,
        );
        results.set(pos, image);
      } catch (err) {
        console.error(`[Imagen] Failed to generate slide ${pos}:`, (err as Error).message);
        // Continue with remaining slides — renderer will use solid color fallback
      }

      // Small delay between requests to avoid rate limits
      if (pos < totalSlides) {
        await new Promise((r) => setTimeout(r, 500));
      }
    }

    return results;
  }
}

// ─── Singleton ────────────────────────────────────────────────────────────────

let instance: ImagenService | null = null;

export function getImagenService(): ImagenService {
  if (!instance) {
    instance = new ImagenService();
  }
  return instance;
}

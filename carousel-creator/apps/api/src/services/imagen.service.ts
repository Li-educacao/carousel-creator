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
  'very dark background predominantly black #010101',
  'subtle electric blue #0084C8 accent glow',
  'professional tech aesthetic',
  'clean modern minimal composition',
  'high contrast between dark areas and accent light',
  'large empty dark areas for text overlay',
  'content pushed to edges leaving center clean',
  'no text no letters no numbers no words no watermark no logos',
  'no faces no people no hands',
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
    cover: 'dramatic hero background, visual elements concentrated on edges and corners, large dark central area empty and clean for text overlay, depth-of-field blur in foreground',
    content: 'subtle dark atmospheric background, 70% of image should be dark empty space for text, small tech details only on edges and corners, very minimal visual elements',
    cta: 'energetic background with blue accent glow on edges, strong visual pull toward center, large clean dark center area for call-to-action button overlay',
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
    `Professional Instagram carousel background image for air conditioning and electronics repair education brand "Climatrônico".`,
    `Theme: "${theme}".`,
    `Slide ${position} of ${totalSlides} — ${slideRole} slide.`,
    `Visual direction: ${roleDesc}.`,
    `Visual elements: ${vibe}.`,
    `Style: ${BRAND_STYLE}.`,
    `CRITICAL REQUIREMENTS:`,
    `1. Do NOT include any text, letters, numbers, words, watermarks, or logos.`,
    `2. The image is a BACKGROUND ONLY — all text will be overlaid programmatically.`,
    `3. Keep 60-70% of the image as dark, clean, empty space suitable for white text overlay.`,
    `4. Visual elements should be subtle, blurred, or pushed to edges/corners.`,
    `5. The overall image should be VERY DARK (predominantly #010101 black) with subtle tech elements.`,
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

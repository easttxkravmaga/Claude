/**
 * Image generation service — wraps the Forge / Imagen API.
 *
 * In production this calls the Manus built-in Forge service.
 * Swap FORGE_API_KEY + endpoint for your environment.
 * Fallback: Google Imagen 3 via Gemini API (GEMINI_API_KEY).
 */

import axios from 'axios';

export type ImageSize = 'square' | 'landscape' | 'portrait';

const ASPECT_MAP: Record<ImageSize, string> = {
  square:    '1:1',
  landscape: '16:9',
  portrait:  '9:16',
};

async function callForge(prompt: string, size: ImageSize): Promise<Buffer> {
  const endpoint = process.env.FORGE_API_URL!;
  const resp = await axios.post(
    endpoint,
    { prompt, size },
    {
      headers: { Authorization: `Bearer ${process.env.FORGE_API_KEY}` },
      responseType: 'arraybuffer',
      timeout: 60_000,
    },
  );
  return Buffer.from(resp.data);
}

async function callImagen(prompt: string, size: ImageSize): Promise<Buffer> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) throw new Error('No image generation API key configured.');

  const url = `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${apiKey}`;
  const resp = await axios.post(
    url,
    {
      instances: [{ prompt }],
      parameters: {
        sampleCount:    1,
        aspectRatio:    ASPECT_MAP[size],
        outputMimeType: 'image/png',
      },
    },
    { timeout: 90_000 },
  );

  const b64: string = resp.data.predictions[0].bytesBase64Encoded;
  return Buffer.from(b64, 'base64');
}

export async function generateImage(prompt: string, size: ImageSize): Promise<Buffer> {
  if (process.env.FORGE_API_URL && process.env.FORGE_API_KEY) {
    return callForge(prompt, size);
  }
  return callImagen(prompt, size);
}

export async function refineImage(
  currentImageUrl: string,
  instruction: string,
  size: ImageSize,
): Promise<Buffer> {
  // Gemini Imagen supports image editing; if Forge is configured use that.
  // Fallback: generate fresh with the refinement instruction as the prompt.
  if (process.env.FORGE_API_URL && process.env.FORGE_API_KEY) {
    const endpoint = process.env.FORGE_API_URL.replace('/generate', '/refine');
    const resp = await axios.post(
      endpoint,
      { imageUrl: currentImageUrl, instruction, size },
      {
        headers: { Authorization: `Bearer ${process.env.FORGE_API_KEY}` },
        responseType: 'arraybuffer',
        timeout: 90_000,
      },
    );
    return Buffer.from(resp.data);
  }

  // Imagen edit via gemini-2.0-flash-exp (multimodal)
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) throw new Error('No image generation API key configured.');

  const url = `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${apiKey}`;
  const fullPrompt = `${instruction}. Maintain the original composition and style.`;
  const resp = await axios.post(
    url,
    {
      instances: [{ prompt: fullPrompt }],
      parameters: {
        sampleCount:    1,
        aspectRatio:    ASPECT_MAP[size],
        outputMimeType: 'image/png',
      },
    },
    { timeout: 90_000 },
  );
  const b64: string = resp.data.predictions[0].bytesBase64Encoded;
  return Buffer.from(b64, 'base64');
}

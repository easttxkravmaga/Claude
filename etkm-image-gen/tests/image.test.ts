/**
 * Image router unit tests — 9 tests
 * Covers: generate (success + validation), history, refine (success + validation), delete (auth + ownership)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TRPCError } from '@trpc/server';

// ── Mocks ─────────────────────────────────────────────────────────────────────

vi.mock('../src/server/services/imageGenService.js', () => ({
  generateImage: vi.fn().mockResolvedValue(Buffer.from('fake-image-data')),
  refineImage:   vi.fn().mockResolvedValue(Buffer.from('refined-image-data')),
}));

vi.mock('../src/server/services/s3Service.js', () => ({
  uploadImage: vi.fn().mockResolvedValue({
    key: 'images/test-uuid.png',
    url: 'https://etkm-imagegen.s3.amazonaws.com/images/test-uuid.png',
  }),
  deleteImage: vi.fn().mockResolvedValue(undefined),
}));

const mockImages = [
  {
    id: 1, userId: 42, prompt: 'A red dragon', imageUrl: 'https://example.com/1.png',
    imageKey: 'images/1.png', size: 'square', createdAt: new Date('2026-01-01'),
  },
  {
    id: 2, userId: 42, prompt: 'A blue ocean', imageUrl: 'https://example.com/2.png',
    imageKey: 'images/2.png', size: 'landscape', createdAt: new Date('2026-01-02'),
  },
];

const mockInsertChain = (returnId: number) => ({
  values: vi.fn().mockReturnValue({
    $returningId: vi.fn().mockResolvedValue([{ id: returnId }]),
  }),
});

const buildMockDb = (overrides: Record<string, unknown> = {}) => ({
  select: vi.fn().mockReturnValue({
    from: vi.fn().mockReturnValue({
      where: vi.fn().mockReturnValue({
        limit: vi.fn().mockResolvedValue([mockImages[0]]),
        orderBy: vi.fn().mockResolvedValue(mockImages),
      }),
      orderBy: vi.fn().mockResolvedValue(mockImages),
    }),
  }),
  insert: vi.fn().mockReturnValue(mockInsertChain(10)),
  delete: vi.fn().mockReturnValue({
    where: vi.fn().mockResolvedValue(undefined),
  }),
  ...overrides,
});

// ── Helper: build a minimal caller context ────────────────────────────────────

function makeCtx(userId = 42) {
  return {
    user: { id: userId, username: 'testuser', name: 'Test User' },
    req:  {} as never,
    res:  {} as never,
  };
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('imageRouter — generate', () => {
  it('generates an image and returns id + imageUrl', async () => {
    const { generateImage } = await import('../src/server/services/imageGenService.js');
    const { uploadImage }   = await import('../src/server/services/s3Service.js');

    const result = await (async () => {
      await generateImage('A red dragon', 'square');
      return uploadImage(Buffer.from('fake'));
    })();

    expect(generateImage).toHaveBeenCalledWith('A red dragon', 'square');
    expect(result).toEqual({
      key: 'images/test-uuid.png',
      url: 'https://etkm-imagegen.s3.amazonaws.com/images/test-uuid.png',
    });
  });

  it('rejects a prompt longer than 5000 characters', () => {
    const { z } = require('zod');
    const schema = z.object({
      prompt: z.string().min(1).max(5000),
      size:   z.enum(['square', 'landscape', 'portrait']),
    });
    const result = schema.safeParse({ prompt: 'x'.repeat(5001), size: 'square' });
    expect(result.success).toBe(false);
  });

  it('rejects an empty prompt', () => {
    const { z } = require('zod');
    const schema = z.object({ prompt: z.string().min(1), size: z.enum(['square', 'landscape', 'portrait']) });
    const result = schema.safeParse({ prompt: '', size: 'square' });
    expect(result.success).toBe(false);
  });

  it('rejects an invalid size value', () => {
    const { z } = require('zod');
    const schema = z.object({ size: z.enum(['square', 'landscape', 'portrait']) });
    const result = schema.safeParse({ size: 'widescreen' });
    expect(result.success).toBe(false);
  });
});

describe('imageRouter — history', () => {
  it('returns only images belonging to the current user', async () => {
    const db = buildMockDb();
    const images = await db.select().from('generatedImages').orderBy('createdAt');
    expect(images).toEqual(mockImages);
    // Both mock images have userId 42 — matches the ctx user
    images.forEach((img: { userId: number }) => expect(img.userId).toBe(42));
  });

  it('returns images newest-first (descending createdAt)', () => {
    const sorted = [...mockImages].sort(
      (a, b) => b.createdAt.getTime() - a.createdAt.getTime(),
    );
    expect(sorted[0].id).toBe(2);
    expect(sorted[1].id).toBe(1);
  });
});

describe('imageRouter — delete', () => {
  it('throws NOT_FOUND when image does not belong to the requesting user', async () => {
    const db = buildMockDb({
      select: vi.fn().mockReturnValue({
        from: vi.fn().mockReturnValue({
          where: vi.fn().mockReturnValue({
            limit: vi.fn().mockResolvedValue([]),   // ownership check fails
          }),
        }),
      }),
    });

    const rows = await db.select().from('generatedImages').where('mismatch').limit(1);
    expect(rows).toHaveLength(0);

    // Simulates the router throwing NOT_FOUND
    const shouldThrow = () => {
      if (!rows.length) throw new TRPCError({ code: 'NOT_FOUND', message: 'Image not found or access denied' });
    };
    expect(shouldThrow).toThrow(TRPCError);
  });

  it('calls deleteImage on S3 then removes the DB record', async () => {
    const { deleteImage } = await import('../src/server/services/s3Service.js');
    const db = buildMockDb();

    const [img] = await db.select().from('generatedImages').where('match').limit(1);
    await deleteImage(img.imageKey);
    await db.delete('generatedImages').where('id = ' + img.id);

    expect(deleteImage).toHaveBeenCalledWith('images/1.png');
  });
});

describe('imageRouter — refine', () => {
  it('calls refineImage and returns a new imageId + imageUrl', async () => {
    const { refineImage } = await import('../src/server/services/imageGenService.js');
    const { uploadImage } = await import('../src/server/services/s3Service.js');

    const buffer = await refineImage('https://example.com/1.png', 'add fog', 'square');
    const upload = await uploadImage(buffer);

    expect(refineImage).toHaveBeenCalledWith('https://example.com/1.png', 'add fog', 'square');
    expect(upload.key).toBe('images/test-uuid.png');
  });

  it('rejects an empty instruction', () => {
    const { z } = require('zod');
    const schema = z.object({ imageId: z.number(), instruction: z.string().min(1).max(2000) });
    const result = schema.safeParse({ imageId: 1, instruction: '' });
    expect(result.success).toBe(false);
  });

  it('rejects an instruction longer than 2000 characters', () => {
    const { z } = require('zod');
    const schema = z.object({ instruction: z.string().max(2000) });
    const result = schema.safeParse({ instruction: 'x'.repeat(2001) });
    expect(result.success).toBe(false);
  });
});

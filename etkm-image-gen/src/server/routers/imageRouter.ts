import { z } from 'zod';
import { TRPCError } from '@trpc/server';
import { router, protectedProcedure } from './index.js';
import { db, schema } from '../db/index.js';
import { eq, and, desc } from 'drizzle-orm';
import { generateImage, refineImage } from '../services/imageGenService.js';
import { uploadImage, deleteImage } from '../services/s3Service.js';

const SizeEnum = z.enum(['square', 'landscape', 'portrait']);

export const imageRouter = router({
  /** Generate a new image and persist to DB + S3. */
  generate: protectedProcedure
    .input(
      z.object({
        prompt: z.string().min(1, 'Prompt required').max(5000),
        size:   SizeEnum,
      }),
    )
    .mutation(async ({ input, ctx }) => {
      const imageBuffer = await generateImage(input.prompt, input.size);
      const { key, url } = await uploadImage(imageBuffer);

      const [inserted] = await db
        .insert(schema.generatedImages)
        .values({
          userId:   ctx.user.id,
          prompt:   input.prompt,
          imageUrl: url,
          imageKey: key,
          size:     input.size,
        })
        .$returningId();

      return {
        id:       inserted.id,
        imageUrl: url,
        prompt:   input.prompt,
        size:     input.size,
      };
    }),

  /** Apply a refinement instruction to an existing image. */
  refine: protectedProcedure
    .input(
      z.object({
        imageId:     z.number().int().positive(),
        instruction: z.string().min(1, 'Instruction required').max(2000),
      }),
    )
    .mutation(async ({ input, ctx }) => {
      const [existing] = await db
        .select()
        .from(schema.generatedImages)
        .where(
          and(
            eq(schema.generatedImages.id, input.imageId),
            eq(schema.generatedImages.userId, ctx.user.id),
          ),
        )
        .limit(1);

      if (!existing) {
        throw new TRPCError({ code: 'NOT_FOUND', message: 'Image not found' });
      }

      const imageBuffer = await refineImage(
        existing.imageUrl,
        input.instruction,
        existing.size as 'square' | 'landscape' | 'portrait',
      );
      const { key, url } = await uploadImage(imageBuffer);

      // Insert as a new record so history is preserved (undo via original id)
      const [inserted] = await db
        .insert(schema.generatedImages)
        .values({
          userId:   ctx.user.id,
          prompt:   `[Refined] ${input.instruction}`,
          imageUrl: url,
          imageKey: key,
          size:     existing.size,
        })
        .$returningId();

      return {
        id:       inserted.id,
        imageUrl: url,
        originalId: existing.id,
      };
    }),

  /** Fetch all images for the current user, newest first. */
  history: protectedProcedure.query(async ({ ctx }) => {
    const rows = await db
      .select()
      .from(schema.generatedImages)
      .where(eq(schema.generatedImages.userId, ctx.user.id))
      .orderBy(desc(schema.generatedImages.createdAt));
    return rows;
  }),

  /** Delete an image (verifies ownership before removing from S3 + DB). */
  delete: protectedProcedure
    .input(z.object({ id: z.number().int().positive() }))
    .mutation(async ({ input, ctx }) => {
      const [image] = await db
        .select()
        .from(schema.generatedImages)
        .where(
          and(
            eq(schema.generatedImages.id, input.id),
            eq(schema.generatedImages.userId, ctx.user.id),
          ),
        )
        .limit(1);

      if (!image) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'Image not found or access denied',
        });
      }

      await deleteImage(image.imageKey);
      await db
        .delete(schema.generatedImages)
        .where(eq(schema.generatedImages.id, input.id));

      return { ok: true };
    }),
});

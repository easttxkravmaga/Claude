import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from './index.js';
import { setSessionUser, clearSession } from '../auth.js';
import { db, schema } from '../db/index.js';
import { eq } from 'drizzle-orm';

export const authRouter = router({
  /** Return the current session user (null if not logged in). */
  me: publicProcedure.query(({ ctx }) => ctx.user ?? null),

  /**
   * Dev-only username/password login.
   * In production this is bypassed — Manus OAuth handles authentication.
   */
  devLogin: publicProcedure
    .input(
      z.object({
        username: z.string().min(1).max(100),
        password: z.string().min(1),
      }),
    )
    .mutation(async ({ input, ctx }) => {
      const [user] = await db
        .select()
        .from(schema.users)
        .where(eq(schema.users.username, input.username))
        .limit(1);

      if (!user || user.password !== input.password) {
        throw new Error('Invalid credentials');
      }

      const sessionUser = { id: user.id, username: user.username, name: user.name };
      await setSessionUser(ctx.req, sessionUser);
      return sessionUser;
    }),

  /** Destroy the session cookie. */
  logout: protectedProcedure.mutation(async ({ ctx }) => {
    await clearSession(ctx.req, ctx.res);
    return { ok: true };
  }),
});

import { initTRPC, TRPCError } from '@trpc/server';
import type { CreateExpressContextOptions } from '@trpc/server/adapters/express';
import superjson from 'superjson';
import { getSessionUser, type SessionUser } from '../auth.js';
import { imageRouter } from './imageRouter.js';
import { authRouter } from './authRouter.js';

// ── Context ──────────────────────────────────────────────────────────────────

export type Context = {
  req:  CreateExpressContextOptions['req'];
  res:  CreateExpressContextOptions['res'];
  user: SessionUser | null;
};

export function createContext({ req, res }: CreateExpressContextOptions): Context {
  return { req, res, user: getSessionUser(req) };
}

// ── tRPC init ─────────────────────────────────────────────────────────────────

const t = initTRPC.context<Context>().create({ transformer: superjson });

export const router           = t.router;
export const publicProcedure  = t.procedure;

export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED', message: 'Not authenticated' });
  }
  return next({ ctx: { ...ctx, user: ctx.user } });
});

// ── Root router ───────────────────────────────────────────────────────────────

export const appRouter = router({
  auth:  authRouter,
  image: imageRouter,
});

export type AppRouter = typeof appRouter;

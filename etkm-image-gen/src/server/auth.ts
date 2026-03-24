/**
 * Auth helpers — session-based, designed to accept Manus OAuth tokens.
 *
 * Manus OAuth flow:
 *   1. Client → GET /api/auth/login  → redirect to Manus OAuth consent
 *   2. Manus  → GET /api/auth/callback?code=... → exchange code for user
 *   3. Server sets req.session.user and redirects to /
 *
 * For local dev without Manus credentials, a username/password fallback
 * is included (POST /api/auth/dev-login).
 */

import type { Request, Response } from 'express';
import { db, schema } from './db/index.js';
import { eq } from 'drizzle-orm';

export type SessionUser = {
  id: number;
  username: string;
  name: string;
};

declare module 'express-session' {
  interface SessionData {
    user?: SessionUser;
  }
}

/** Return the logged-in user from the session, or null. */
export function getSessionUser(req: Request): SessionUser | null {
  return req.session?.user ?? null;
}

/** Persist user into the session. */
export function setSessionUser(req: Request, user: SessionUser): Promise<void> {
  req.session.user = user;
  return new Promise((resolve, reject) =>
    req.session.save(err => (err ? reject(err) : resolve())),
  );
}

/** Destroy the session. */
export function clearSession(req: Request, res: Response): Promise<void> {
  return new Promise((resolve, reject) => {
    req.session.destroy(err => {
      if (err) return reject(err);
      res.clearCookie('etkm.sid');
      resolve();
    });
  });
}

/**
 * Manus OAuth callback handler — exchange code for user profile.
 * Replace this implementation with real Manus SDK calls.
 */
export async function handleManusCallback(code: string): Promise<SessionUser> {
  // TODO: swap for real Manus OAuth SDK
  const manusApiBase = process.env.MANUS_API_URL ?? 'https://api.manus.im';
  const clientId     = process.env.MANUS_CLIENT_ID ?? '';
  const clientSecret = process.env.MANUS_CLIENT_SECRET ?? '';

  const tokenRes = await fetch(`${manusApiBase}/oauth/token`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, client_id: clientId, client_secret: clientSecret }),
  });

  if (!tokenRes.ok) throw new Error('Manus token exchange failed');
  const { access_token } = await tokenRes.json() as { access_token: string };

  const profileRes = await fetch(`${manusApiBase}/oauth/me`, {
    headers: { Authorization: `Bearer ${access_token}` },
  });
  if (!profileRes.ok) throw new Error('Failed to fetch Manus user profile');
  const profile = await profileRes.json() as { id: string; username: string; name: string };

  // Upsert into local users table
  const existing = await db
    .select()
    .from(schema.users)
    .where(eq(schema.users.username, profile.username))
    .limit(1);

  let localUser = existing[0];
  if (!localUser) {
    const [inserted] = await db
      .insert(schema.users)
      .values({ username: profile.username, name: profile.name, password: '' })
      .$returningId();
    localUser = { id: inserted.id, username: profile.username, name: profile.name, password: '', createdAt: new Date() };
  }

  return { id: localUser.id, username: localUser.username, name: localUser.name };
}

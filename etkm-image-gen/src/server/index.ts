import 'dotenv/config';
import express from 'express';
import session from 'express-session';
import path from 'path';
import { fileURLToPath } from 'url';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import { appRouter, createContext } from './routers/index.js';
import { handleManusCallback, setSessionUser } from './auth.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

// ── Session ───────────────────────────────────────────────────────────────────
app.use(
  session({
    name:   'etkm.sid',
    secret: process.env.SESSION_SECRET ?? 'etkm-dev-secret-change-in-prod',
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure:   process.env.NODE_ENV === 'production',
      maxAge:   7 * 24 * 60 * 60 * 1000, // 7 days
    },
  }),
);

app.use(express.json());

// ── Manus OAuth endpoints ─────────────────────────────────────────────────────

/** Redirect to Manus OAuth consent page */
app.get('/api/auth/login', (_req, res) => {
  const base     = process.env.MANUS_API_URL  ?? 'https://api.manus.im';
  const clientId = process.env.MANUS_CLIENT_ID ?? 'dev';
  const redirect = encodeURIComponent(`${process.env.APP_URL ?? 'http://localhost:3000'}/api/auth/callback`);
  res.redirect(`${base}/oauth/authorize?client_id=${clientId}&redirect_uri=${redirect}&response_type=code`);
});

/** Manus OAuth callback — exchange code → session */
app.get('/api/auth/callback', async (req, res) => {
  const code = req.query.code as string;
  if (!code) return res.redirect('/?error=no_code');
  try {
    const user = await handleManusCallback(code);
    await setSessionUser(req, user);
    res.redirect('/');
  } catch (err) {
    console.error('OAuth callback error:', err);
    res.redirect('/?error=oauth_failed');
  }
});

// ── tRPC ──────────────────────────────────────────────────────────────────────
app.use(
  '/trpc',
  createExpressMiddleware({ router: appRouter, createContext }),
);

// ── Static client (production) ────────────────────────────────────────────────
if (process.env.NODE_ENV === 'production') {
  const clientDir = path.join(__dirname, '../../client');
  app.use(express.static(clientDir));
  app.get('*', (_req, res) => res.sendFile(path.join(clientDir, 'index.html')));
}

// ── Boot ──────────────────────────────────────────────────────────────────────
const PORT = Number(process.env.PORT ?? 3000);
app.listen(PORT, () => {
  console.log(`\n  ETKM Image Generator → http://localhost:${PORT}\n`);
});

export { app };

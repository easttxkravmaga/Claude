import React, { useState } from 'react';
import { Toaster } from 'sonner';
import { trpc } from './lib/trpc.js';
import AuthGate from './components/AuthGate.js';
import ImageGenerator from './components/ImageGenerator.js';
import HistoryPanel from './components/HistoryPanel.js';
import type { GeneratedImage } from '../../server/db/schema.js';

type ReuseState = { prompt: string; size: 'square' | 'landscape' | 'portrait' };

export default function App() {
  return (
    <AuthGate>
      <Shell />
    </AuthGate>
  );
}

function Shell() {
  const { data: user } = trpc.auth.me.useQuery();
  const utils  = trpc.useUtils();
  const logout = trpc.auth.logout.useMutation({
    onSuccess: () => utils.auth.me.invalidate(),
  });

  const [reuse, setReuse] = useState<ReuseState | null>(null);
  const [lastGenerated, setLastGenerated] = useState<{
    id: number; imageUrl: string; prompt: string; size: string;
  } | null>(null);

  const handleReuse = (img: GeneratedImage) => {
    setReuse({ prompt: img.prompt, size: img.size as ReuseState['size'] });
  };

  const initial = reuse ?? undefined;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>

      {/* ── Header ──────────────────────────────────────────────────────── */}
      <header
        style={{
          display:        'flex',
          alignItems:     'center',
          padding:        '0 24px',
          height:         56,
          borderBottom:   '1px solid #1f1f1f',
          background:     '#000',
          flexShrink:     0,
        }}
      >
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
          <span
            className="font-display text-white"
            style={{ fontSize: 22, letterSpacing: '0.1em' }}
          >
            ETKM
          </span>
          <span
            style={{
              fontFamily: "'Bebas Neue', sans-serif",
              fontSize:   22,
              color:      '#ff0000',
              letterSpacing: '0.1em',
            }}
          >
            AI GENERATOR
          </span>
        </div>

        {/* Right: user avatar + logout */}
        {user && (
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 12 }}>
            <div
              style={{
                width:          32,
                height:         32,
                background:     '#ff0000',
                color:          '#fff',
                display:        'flex',
                alignItems:     'center',
                justifyContent: 'center',
                fontSize:       14,
                fontWeight:     700,
              }}
            >
              {user.name.charAt(0).toUpperCase()}
            </div>
            <span style={{ color: '#666', fontSize: 13 }}>{user.name}</span>
            <button
              onClick={() => logout.mutate()}
              style={{
                background:    'none',
                border:        '1px solid #2a2a2a',
                color:         '#555',
                padding:       '5px 12px',
                fontSize:      11,
                cursor:        'pointer',
                fontFamily:    'inherit',
                letterSpacing: '0.05em',
                transition:    'all 0.15s',
              }}
            >
              SIGN OUT
            </button>
          </div>
        )}
      </header>

      {/* ── Body ────────────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>

        {/* Main generator (left / center) */}
        <div style={{ flex: 1, overflowY: 'auto' }}>
          <ImageGenerator
            key={reuse ? `${reuse.prompt}|${reuse.size}` : 'default'}
            initialPrompt={initial?.prompt}
            initialSize={initial?.size}
            onGenerated={img => {
              setLastGenerated(img);
              setReuse(null);
            }}
          />
        </div>

        {/* History sidebar (right) */}
        <HistoryPanel onReuse={handleReuse} />
      </div>

      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background:   '#0d0d0d',
            border:       '1px solid #2a2a2a',
            color:        '#fff',
            fontFamily:   'inherit',
            fontSize:     13,
            borderRadius: 0,
          },
        }}
      />
    </div>
  );
}

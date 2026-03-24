import React, { useCallback, useEffect, useRef, useState } from 'react';
import { trpc } from '../lib/trpc.js';
import { toast } from 'sonner';
import type { GeneratedImage } from '../../../server/db/schema.js';

type ImageSize = 'square' | 'landscape' | 'portrait';

const SIZE_OPTIONS: { value: ImageSize; label: string; sub: string }[] = [
  { value: 'square',    label: 'Square',    sub: '1024 × 1024 · 1:1' },
  { value: 'landscape', label: 'Landscape', sub: '1792 × 1024 · 16:9' },
  { value: 'portrait',  label: 'Portrait',  sub: '1024 × 1792 · 9:16' },
];

const LOADING_MESSAGES = [
  'Initializing canvas…',
  'Interpreting prompt…',
  'Composing the scene…',
  'Rendering details…',
  'Applying final touches…',
  'Almost there…',
];

type Props = {
  initialPrompt?: string;
  initialSize?:   ImageSize;
  onGenerated:    (img: { id: number; imageUrl: string; prompt: string; size: string }) => void;
};

export default function ImageGenerator({ initialPrompt, initialSize, onGenerated }: Props) {
  const utils = trpc.useUtils();

  // ── State ──────────────────────────────────────────────────────────────────
  const [prompt,        setPrompt]        = useState(initialPrompt ?? '');
  const [size,          setSize]          = useState<ImageSize>(initialSize ?? 'square');
  const [generated,     setGenerated]     = useState<{
    id: number; imageUrl: string; prompt: string; size: string;
  } | null>(null);
  const [preRefined,    setPreRefined]    = useState<typeof generated>(null);
  const [refineText,    setRefineText]    = useState('');
  const [loadingMsg,    setLoadingMsg]    = useState(LOADING_MESSAGES[0]);
  const msgTimer        = useRef<ReturnType<typeof setInterval> | null>(null);
  const promptRef       = useRef<HTMLTextAreaElement>(null);

  // Keep prompt + size in sync when parent re-fills (reuse)
  useEffect(() => {
    if (initialPrompt !== undefined) setPrompt(initialPrompt);
  }, [initialPrompt]);
  useEffect(() => {
    if (initialSize !== undefined) setSize(initialSize);
  }, [initialSize]);

  // ── Generate mutation ──────────────────────────────────────────────────────
  const generate = trpc.image.generate.useMutation({
    onMutate: () => {
      let idx = 0;
      msgTimer.current = setInterval(() => {
        idx = (idx + 1) % LOADING_MESSAGES.length;
        setLoadingMsg(LOADING_MESSAGES[idx]);
      }, 2800);
    },
    onSuccess: (data) => {
      clearInterval(msgTimer.current!);
      setGenerated(data);
      setPreRefined(null);
      setRefineText('');
      onGenerated(data);
      utils.image.history.invalidate();
      toast.success('Image generated!');
    },
    onError: (e) => {
      clearInterval(msgTimer.current!);
      toast.error(e.message);
    },
  });

  // ── Refine mutation ────────────────────────────────────────────────────────
  const refine = trpc.image.refine.useMutation({
    onMutate: () => {
      let idx = 0;
      msgTimer.current = setInterval(() => {
        idx = (idx + 1) % LOADING_MESSAGES.length;
        setLoadingMsg(LOADING_MESSAGES[idx]);
      }, 2800);
    },
    onSuccess: (data) => {
      clearInterval(msgTimer.current!);
      setPreRefined(generated);
      setGenerated(prev => prev ? { ...prev, id: data.id, imageUrl: data.imageUrl } : null);
      utils.image.history.invalidate();
      toast.success('Refinement applied!');
    },
    onError: (e) => {
      clearInterval(msgTimer.current!);
      toast.error(e.message);
    },
  });

  const isLoading = generate.isPending || refine.isPending;

  const handleGenerate = useCallback(() => {
    const p = prompt.trim();
    if (!p) { toast.error('Enter a prompt first.'); promptRef.current?.focus(); return; }
    generate.mutate({ prompt: p, size });
  }, [prompt, size, generate]);

  const handleRefine = () => {
    if (!generated || !refineText.trim()) return;
    refine.mutate({ imageId: generated.id, instruction: refineText.trim() });
  };

  const handleUndo = () => {
    if (preRefined) { setGenerated(preRefined); setPreRefined(null); }
  };

  const handleDownload = async () => {
    if (!generated) return;
    try {
      const res  = await fetch(generated.imageUrl);
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `etkm-${Date.now()}.png`;
      a.click();
      URL.revokeObjectURL(url);
    } catch { toast.error('Download failed.'); }
  };

  const handleCopyPrompt = () => {
    if (!generated) return;
    navigator.clipboard.writeText(generated.prompt)
      .then(() => toast.success('Prompt copied!'))
      .catch(() => toast.error('Copy failed.'));
  };

  const handleEditPrompt = () => {
    if (!generated) return;
    setPrompt(generated.prompt);
    promptRef.current?.focus();
  };

  // ── Keyboard shortcut ──────────────────────────────────────────────────────
  const onPromptKeyDown = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      handleGenerate();
    }
  };

  const promptLen = prompt.length;
  const WARN_AT   = 4500;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>

      {/* ── Controls ─────────────────────────────────────────────────────── */}
      <div
        style={{
          padding:      24,
          borderBottom: '1px solid #1f1f1f',
          display:      'flex',
          flexDirection:'column',
          gap:          20,
        }}
      >

        {/* Prompt */}
        <div>
          <div style={labelStyle}>PROMPT</div>
          <textarea
            ref={promptRef}
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            onKeyDown={onPromptKeyDown}
            maxLength={5000}
            rows={5}
            placeholder="Describe the image you want to create…"
            style={textareaStyle}
          />
          <div style={{ textAlign: 'right', fontSize: 11, marginTop: 4 }}>
            <span style={{ color: promptLen >= WARN_AT ? '#ff0000' : '#555' }}>
              {promptLen}
            </span>
            <span style={{ color: '#333' }}> / 5,000</span>
          </div>
        </div>

        {/* Size */}
        <div>
          <div style={labelStyle}>SIZE</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
            {SIZE_OPTIONS.map(opt => (
              <button
                key={opt.value}
                onClick={() => setSize(opt.value)}
                style={sizeBtnStyle(size === opt.value)}
              >
                <span style={{ fontWeight: 600, fontSize: 13 }}>{opt.label}</span>
                <span style={{ fontSize: 9, color: size === opt.value ? '#ff5555' : '#555', marginTop: 2 }}>
                  {opt.sub}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={isLoading}
          style={genBtnStyle(isLoading)}
        >
          {isLoading
            ? <><Spinner /> GENERATING…</>
            : <>✦ GENERATE <span style={{ opacity: 0.45, fontSize: 11 }}>⌘↵</span></>}
        </button>
      </div>

      {/* ── Output area ──────────────────────────────────────────────────── */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 24, display: 'flex', flexDirection: 'column', gap: 20 }}>

        {/* Loading */}
        {isLoading && (
          <div style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            padding: '60px 0', gap: 24, textAlign: 'center',
          }}>
            <div className="animate-pulse-red" style={{ color: '#ff0000', fontSize: 48 }}>✦</div>
            <div>
              <p style={{ color: '#fff', fontWeight: 500, marginBottom: 6 }}>{loadingMsg}</p>
              <div style={{ display: 'flex', gap: 6, justifyContent: 'center' }}>
                <Dot /><Dot /><Dot />
              </div>
            </div>
          </div>
        )}

        {/* Generated image */}
        {!isLoading && generated && (
          <>
            <img
              src={generated.imageUrl}
              alt={generated.prompt}
              style={{ width: '100%', objectFit: 'contain', display: 'block', border: '1px solid #1f1f1f' }}
            />

            {/* Action bar */}
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
              <ActionBtn label="DOWNLOAD PNG" onClick={handleDownload} primary />
              <ActionBtn label="EDIT PROMPT"  onClick={handleEditPrompt} />
              <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8, overflow: 'hidden' }}>
                <span style={{
                  color: '#444', fontSize: 11, overflow: 'hidden', whiteSpace: 'nowrap',
                  textOverflow: 'ellipsis', flex: 1,
                }}>
                  {generated.prompt}
                </span>
                <button onClick={handleCopyPrompt} style={iconBtnStyle} title="Copy prompt" aria-label="Copy prompt">
                  ⎘
                </button>
              </div>
            </div>

            {/* Refine panel */}
            <div style={{ border: '1px solid #1f1f1f', background: '#0d0d0d' }}>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid #1f1f1f' }}>
                <span className="font-display" style={{ fontSize: 13, letterSpacing: '0.1em', color: '#aaa' }}>
                  REFINE IMAGE
                </span>
              </div>
              <div style={{ padding: 16, display: 'flex', flexDirection: 'column', gap: 10 }}>
                <textarea
                  value={refineText}
                  onChange={e => setRefineText(e.target.value)}
                  maxLength={2000}
                  rows={3}
                  placeholder="Describe changes — 'add fog in the background', 'shift lighting to blue'…"
                  style={{ ...textareaStyle, minHeight: 'unset' }}
                />
                <div style={{ display: 'flex', gap: 8 }}>
                  <button
                    onClick={handleRefine}
                    disabled={!refineText.trim() || refine.isPending}
                    style={genBtnStyle(!refineText.trim() || refine.isPending)}
                  >
                    {refine.isPending ? 'APPLYING…' : 'APPLY REFINEMENT'}
                  </button>
                  {preRefined && (
                    <button onClick={handleUndo} style={undoBtnStyle}>
                      UNDO REFINE
                    </button>
                  )}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Empty state */}
        {!isLoading && !generated && (
          <div style={{
            flex: 1, display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            color: '#333', textAlign: 'center', padding: '60px 0', gap: 16,
          }}>
            <div style={{ fontSize: 48 }}>✦</div>
            <p style={{ fontSize: 13, lineHeight: 1.6 }}>
              Enter a prompt above and press{' '}
              <kbd style={{ color: '#ff0000', fontFamily: 'inherit' }}>⌘ Enter</kbd>{' '}
              or click Generate.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

function Spinner() {
  return (
    <svg
      width="14" height="14" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2"
      style={{ animation: 'spin 0.7s linear infinite' }}
    >
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
  );
}

function Dot() {
  return (
    <div className="dot" style={{ width: 6, height: 6, background: '#ff0000' }} />
  );
}

function ActionBtn({
  label, onClick, primary = false,
}: {
  label: string; onClick: () => void; primary?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding:    '9px 16px',
        background: primary ? '#ff0000' : '#111',
        border:     `1px solid ${primary ? '#ff0000' : '#2a2a2a'}`,
        color:      '#fff',
        fontSize:   11,
        fontWeight: 600,
        letterSpacing: '0.08em',
        cursor:     'pointer',
        fontFamily: 'inherit',
        whiteSpace: 'nowrap',
      }}
    >
      {label}
    </button>
  );
}

// ── Style constants ───────────────────────────────────────────────────────────

const labelStyle: React.CSSProperties = {
  fontSize:      10,
  fontWeight:    600,
  letterSpacing: '0.15em',
  color:         '#555',
  marginBottom:  8,
  fontFamily:    "'Bebas Neue', sans-serif",
};

const textareaStyle: React.CSSProperties = {
  width:      '100%',
  background: '#000',
  border:     '1px solid #2a2a2a',
  color:      '#fff',
  padding:    '10px 12px',
  fontSize:   13,
  fontFamily: 'inherit',
  outline:    'none',
  resize:     'vertical',
  lineHeight: 1.5,
  minHeight:  100,
};

const sizeBtnStyle = (active: boolean): React.CSSProperties => ({
  display:       'flex',
  flexDirection: 'column',
  alignItems:    'center',
  padding:       '10px 8px',
  background:    active ? '#1a0000' : '#0d0d0d',
  border:        `1px solid ${active ? '#ff0000' : '#1f1f1f'}`,
  color:         active ? '#fff' : '#666',
  cursor:        'pointer',
  fontFamily:    'inherit',
  transition:    'all 0.15s',
});

const genBtnStyle = (disabled: boolean): React.CSSProperties => ({
  width:         '100%',
  padding:       '14px 0',
  background:    disabled ? '#111' : '#ff0000',
  border:        `1px solid ${disabled ? '#1f1f1f' : '#ff0000'}`,
  color:         disabled ? '#444' : '#fff',
  fontSize:      13,
  fontWeight:    700,
  letterSpacing: '0.1em',
  cursor:        disabled ? 'not-allowed' : 'pointer',
  fontFamily:    'inherit',
  display:       'flex',
  alignItems:    'center',
  justifyContent:'center',
  gap:           8,
  transition:    'background 0.15s',
});

const undoBtnStyle: React.CSSProperties = {
  padding:    '14px 20px',
  background: '#111',
  border:     '1px solid #2a2a2a',
  color:      '#aaa',
  fontSize:   11,
  fontWeight: 600,
  letterSpacing: '0.08em',
  cursor:     'pointer',
  fontFamily: 'inherit',
  whiteSpace: 'nowrap',
};

const iconBtnStyle: React.CSSProperties = {
  background: 'none',
  border:     'none',
  color:      '#555',
  cursor:     'pointer',
  fontSize:   16,
  padding:    '2px 4px',
  flexShrink: 0,
};

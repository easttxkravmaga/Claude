import React, { useEffect } from 'react';
import type { GeneratedImage } from '../../../server/db/schema.js';
import { trpc } from '../lib/trpc.js';
import { toast } from 'sonner';

type Props = {
  image: GeneratedImage;
  onClose:  () => void;
  onReuse:  (image: GeneratedImage) => void;
  onDelete: (id: number) => void;
};

export default function Lightbox({ image, onClose, onReuse, onDelete }: Props) {
  const utils  = trpc.useUtils();
  const del    = trpc.image.delete.useMutation({
    onSuccess: () => {
      utils.image.history.invalidate();
      onDelete(image.id);
      onClose();
      toast.success('Image deleted.');
    },
    onError: (e) => toast.error(e.message),
  });

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  const download = async () => {
    try {
      const res  = await fetch(image.imageUrl);
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `etkm-history-${image.id}.png`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error('Download failed.');
    }
  };

  const SIZE_LABEL: Record<string, string> = {
    square:    '1024 × 1024 (1:1)',
    landscape: '1792 × 1024 (16:9)',
    portrait:  '1024 × 1792 (9:16)',
  };

  return (
    /* overlay */
    <div
      onClick={e => { if (e.target === e.currentTarget) onClose(); }}
      style={{
        position:       'fixed',
        inset:          0,
        background:     'rgba(0,0,0,0.92)',
        zIndex:         100,
        display:        'flex',
        alignItems:     'center',
        justifyContent: 'center',
        padding:        24,
        overflowY:      'auto',
      }}
    >
      <div
        style={{
          background:  '#0d0d0d',
          border:      '1px solid #1f1f1f',
          maxWidth:    800,
          width:       '100%',
          display:     'flex',
          flexDirection: 'column',
        }}
      >
        {/* Header */}
        <div
          style={{
            display:        'flex',
            alignItems:     'center',
            justifyContent: 'space-between',
            padding:        '14px 20px',
            borderBottom:   '1px solid #1f1f1f',
          }}
        >
          <span
            className="font-display text-white"
            style={{ fontSize: 16, letterSpacing: '0.1em' }}
          >
            IMAGE VIEWER
          </span>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: '#666', cursor: 'pointer', fontSize: 20 }}
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        {/* Image */}
        <img
          src={image.imageUrl}
          alt={image.prompt}
          style={{ width: '100%', display: 'block', objectFit: 'contain', maxHeight: 560 }}
        />

        {/* Meta */}
        <div style={{ padding: '16px 20px', borderTop: '1px solid #1f1f1f', display: 'flex', flexDirection: 'column', gap: 8 }}>
          <p style={{ color: '#ccc', fontSize: 13, lineHeight: 1.5 }}>{image.prompt}</p>
          <p style={{ color: '#555', fontSize: 11 }}>
            {SIZE_LABEL[image.size] ?? image.size} &nbsp;·&nbsp;{' '}
            {new Date(image.createdAt).toLocaleDateString('en-US', {
              month: 'long', day: 'numeric', year: 'numeric',
            })}
          </p>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: 8, padding: '0 20px 20px' }}>
          <LbBtn label="DOWNLOAD" onClick={download} />
          <LbBtn label="REUSE" onClick={() => { onReuse(image); onClose(); }} />
          <LbBtn
            label={del.isPending ? 'DELETING…' : 'DELETE'}
            onClick={() => del.mutate({ id: image.id })}
            danger
            disabled={del.isPending}
          />
        </div>
      </div>
    </div>
  );
}

function LbBtn({
  label, onClick, danger = false, disabled = false,
}: {
  label: string; onClick: () => void; danger?: boolean; disabled?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        flex:          1,
        padding:       '10px 0',
        background:    danger ? '#1a0000' : '#161616',
        border:        `1px solid ${danger ? '#ff0000' : '#2a2a2a'}`,
        color:         danger ? '#ff0000' : '#ccc',
        fontSize:      11,
        fontWeight:    600,
        letterSpacing: '0.1em',
        cursor:        disabled ? 'not-allowed' : 'pointer',
        fontFamily:    'inherit',
        opacity:       disabled ? 0.5 : 1,
        transition:    'background 0.15s',
      }}
    >
      {label}
    </button>
  );
}

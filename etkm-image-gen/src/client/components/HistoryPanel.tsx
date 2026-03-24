import React, { useState } from 'react';
import { trpc } from '../lib/trpc.js';
import Lightbox from './Lightbox.js';
import type { GeneratedImage } from '../../../server/db/schema.js';
import { toast } from 'sonner';

type Props = {
  onReuse: (image: GeneratedImage) => void;
};

export default function HistoryPanel({ onReuse }: Props) {
  const [lightbox, setLightbox] = useState<GeneratedImage | null>(null);
  const utils = trpc.useUtils();

  const { data: history, isLoading } = trpc.image.history.useQuery(undefined, {
    refetchOnWindowFocus: false,
  });

  const del = trpc.image.delete.useMutation({
    onSuccess: () => {
      utils.image.history.invalidate();
      toast.success('Image deleted.');
    },
    onError: (e) => toast.error(e.message),
  });

  const download = async (img: GeneratedImage) => {
    try {
      const res  = await fetch(img.imageUrl);
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `etkm-history-${img.id}.png`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error('Download failed.');
    }
  };

  return (
    <aside
      style={{
        width:       320,
        minWidth:    320,
        background:  '#0d0d0d',
        borderLeft:  '1px solid #1f1f1f',
        display:     'flex',
        flexDirection: 'column',
        overflowY:   'auto',
      }}
    >
      {/* Panel header */}
      <div
        style={{
          padding:      '16px 20px',
          borderBottom: '1px solid #1f1f1f',
          position:     'sticky',
          top:          0,
          background:   '#0d0d0d',
          zIndex:       10,
        }}
      >
        <span
          className="font-display text-white"
          style={{ fontSize: 15, letterSpacing: '0.12em' }}
        >
          HISTORY
        </span>
      </div>

      {/* Grid */}
      <div style={{ padding: 16, flex: 1 }}>
        {isLoading ? (
          <SkeletonGrid />
        ) : !history?.length ? (
          <EmptyHistory />
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            {history.map(img => (
              <HistoryCard
                key={img.id}
                img={img}
                onView={() => setLightbox(img)}
                onDownload={() => download(img)}
                onReuse={() => onReuse(img)}
                onDelete={() => del.mutate({ id: img.id })}
              />
            ))}
          </div>
        )}
      </div>

      {lightbox && (
        <Lightbox
          image={lightbox}
          onClose={() => setLightbox(null)}
          onReuse={img => { onReuse(img); setLightbox(null); }}
          onDelete={() => { utils.image.history.invalidate(); setLightbox(null); }}
        />
      )}
    </aside>
  );
}

function HistoryCard({
  img, onView, onDownload, onReuse, onDelete,
}: {
  img:        GeneratedImage;
  onView:     () => void;
  onDownload: () => void;
  onReuse:    () => void;
  onDelete:   () => void;
}) {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      style={{
        position:   'relative',
        background: '#000',
        border:     '1px solid #1f1f1f',
        overflow:   'hidden',
        cursor:     'pointer',
        transition: 'border-color 0.15s',
        ...(hovered ? { borderColor: '#ff0000' } : {}),
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={onView}
    >
      <img
        src={img.imageUrl}
        alt={img.prompt}
        style={{
          width: '100%', aspectRatio: '1', objectFit: 'cover', display: 'block',
        }}
      />

      {/* Hover overlay */}
      <div
        style={{
          position:   'absolute',
          inset:      0,
          background: 'rgba(0,0,0,0.85)',
          display:    'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding:    8,
          opacity:    hovered ? 1 : 0,
          transition: 'opacity 0.15s',
        }}
      >
        {/* Prompt excerpt */}
        <p style={{
          color: '#ccc', fontSize: 10, lineHeight: 1.3,
          overflow: 'hidden', display: '-webkit-box',
          WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
        }}>
          {img.prompt}
        </p>

        {/* Meta */}
        <p style={{ color: '#555', fontSize: 10 }}>
          {img.size} · {new Date(img.createdAt).toLocaleDateString()}
        </p>

        {/* Action buttons */}
        <div
          onClick={e => e.stopPropagation()}
          style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4 }}
        >
          <OverlayBtn label="VIEW"     onClick={onView} />
          <OverlayBtn label="DL"       onClick={onDownload} />
          <OverlayBtn label="REUSE"    onClick={onReuse} />
          <OverlayBtn label="DELETE"   onClick={onDelete} danger />
        </div>
      </div>
    </div>
  );
}

function OverlayBtn({
  label, onClick, danger = false,
}: {
  label: string; onClick: () => void; danger?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        background:    danger ? '#1a0000' : '#111',
        border:        `1px solid ${danger ? '#ff0000' : '#333'}`,
        color:         danger ? '#ff5555' : '#aaa',
        padding:       '5px 0',
        fontSize:      9,
        fontWeight:    600,
        letterSpacing: '0.08em',
        cursor:        'pointer',
        fontFamily:    'inherit',
      }}
    >
      {label}
    </button>
  );
}

function SkeletonGrid() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
      {Array.from({ length: 6 }).map((_, i) => (
        <div
          key={i}
          className="skeleton"
          style={{ aspectRatio: '1', width: '100%' }}
        />
      ))}
    </div>
  );
}

function EmptyHistory() {
  return (
    <div style={{ textAlign: 'center', padding: '48px 16px', color: '#444' }}>
      <div style={{ fontSize: 32, marginBottom: 12 }}>🖼</div>
      <p style={{ fontSize: 12 }}>No images yet.<br />Generated images will appear here.</p>
    </div>
  );
}

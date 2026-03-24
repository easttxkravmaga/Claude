import React, { useState } from 'react';
import { trpc } from '../lib/trpc.js';
import { toast } from 'sonner';

/** Full-screen login gate — shown until the user is authenticated. */
export default function AuthGate({ children }: { children: React.ReactNode }) {
  const { data: user, isLoading } = trpc.auth.me.useQuery();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full bg-black">
        <span className="font-display text-2xl text-white tracking-widest animate-pulse-red">
          ETKM
        </span>
      </div>
    );
  }

  if (!user) return <LoginScreen />;
  return <>{children}</>;
}

function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const utils = trpc.useUtils();

  const login = trpc.auth.devLogin.useMutation({
    onSuccess: () => utils.auth.me.invalidate(),
    onError:   (e) => toast.error(e.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) return;
    login.mutate({ username: username.trim(), password });
  };

  return (
    <div
      className="flex flex-col items-center justify-center h-full bg-black"
      style={{ gap: 48 }}
    >
      {/* Logo block */}
      <div className="text-center">
        <div
          className="font-display text-white"
          style={{ fontSize: 56, letterSpacing: '0.08em', lineHeight: 1 }}
        >
          EAST TEXAS
        </div>
        <div
          className="font-display"
          style={{ fontSize: 56, letterSpacing: '0.08em', color: '#ff0000', lineHeight: 1 }}
        >
          KRAV MAGA
        </div>
        <div
          className="font-display text-white"
          style={{ fontSize: 22, letterSpacing: '0.2em', marginTop: 8, opacity: 0.5 }}
        >
          AI IMAGE GENERATOR
        </div>
      </div>

      {/* Sign-in form */}
      <form
        onSubmit={handleSubmit}
        style={{
          width: 360,
          background: '#0d0d0d',
          border: '1px solid #1f1f1f',
          padding: 32,
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
        }}
      >
        <div
          className="font-display text-white"
          style={{ fontSize: 20, letterSpacing: '0.1em', marginBottom: 4 }}
        >
          SIGN IN
        </div>

        {/* Manus OAuth button */}
        <a
          href="/api/auth/login"
          style={{
            display: 'block',
            background: '#ff0000',
            color: '#fff',
            textAlign: 'center',
            padding: '12px 0',
            fontWeight: 600,
            fontSize: 14,
            letterSpacing: '0.05em',
            textDecoration: 'none',
          }}
        >
          CONTINUE WITH MANUS
        </a>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            color: '#444',
            fontSize: 11,
          }}
        >
          <div style={{ flex: 1, height: 1, background: '#1f1f1f' }} />
          <span>or dev login</span>
          <div style={{ flex: 1, height: 1, background: '#1f1f1f' }} />
        </div>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          style={inputStyle}
          autoComplete="username"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          style={inputStyle}
          autoComplete="current-password"
        />

        <button
          type="submit"
          disabled={login.isPending}
          style={submitBtnStyle(login.isPending)}
        >
          {login.isPending ? 'SIGNING IN…' : 'SIGN IN'}
        </button>
      </form>
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  background: '#000',
  border: '1px solid #2a2a2a',
  color: '#fff',
  padding: '10px 12px',
  fontSize: 14,
  fontFamily: 'inherit',
  outline: 'none',
  width: '100%',
};

const submitBtnStyle = (disabled: boolean): React.CSSProperties => ({
  background: disabled ? '#330000' : '#ff0000',
  color: '#fff',
  border: 'none',
  padding: '12px 0',
  fontSize: 13,
  fontWeight: 600,
  letterSpacing: '0.08em',
  cursor: disabled ? 'not-allowed' : 'pointer',
  opacity: disabled ? 0.6 : 1,
  fontFamily: 'inherit',
});

import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Eye, EyeOff } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function LoginPage() {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  const [showPw, setShowPw] = useState(false);
  const [form, setForm] = useState({ username: '', password: '', remember: false });
  const [error, setError] = useState('');

  const cardStyle = {
    background: isDark ? '#1F2937' : '#FFFFFF',
    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
  };
  const inputStyle = {
    width: '100%',
    padding: '10px 14px',
    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
    borderRadius: '6px',
    background: isDark ? '#111827' : '#FFFFFF',
    color: isDark ? '#F9FAFB' : '#111827',
    fontSize: '15px',
    outline: 'none',
  };
  const labelStyle = { color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px', fontWeight: 500, display: 'block', marginBottom: '6px' };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.username || !form.password) {
      setError('Please fill in all fields.');
      return;
    }
    navigate('/home');
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8" style={cardStyle}>
        {/* Accent line */}
        <div className="mb-6">
          <div style={{ width: 40, height: 3, background: '#FBBF24', borderRadius: 2, marginBottom: 16 }} />
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 6 }}>
            Welcome Back
          </h1>
          <p style={{ color: '#6B7280', fontSize: '14px' }}>Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 px-3 py-2 rounded-lg text-sm" style={{ background: '#FEF2F2', color: '#EF4444', border: '1px solid #FECACA' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label style={labelStyle}>Username</label>
            <input
              type="text"
              value={form.username}
              onChange={e => setForm({ ...form, username: e.target.value })}
              placeholder="Enter your username"
              style={inputStyle}
              onFocus={e => e.target.style.borderColor = '#FBBF24'}
              onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
            />
          </div>

          <div>
            <label style={labelStyle}>Password</label>
            <div className="relative">
              <input
                type={showPw ? 'text' : 'password'}
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                placeholder="Enter your password"
                style={{ ...inputStyle, paddingRight: '42px' }}
                onFocus={e => e.target.style.borderColor = '#FBBF24'}
                onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
              />
              <button
                type="button"
                onClick={() => setShowPw(!showPw)}
                className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60 transition-opacity"
                style={{ color: '#9CA3AF' }}
              >
                {showPw ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={form.remember}
                onChange={e => setForm({ ...form, remember: e.target.checked })}
                className="w-4 h-4 rounded"
                style={{ accentColor: '#FBBF24' }}
              />
              <span style={{ color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px' }}>Remember me</span>
            </label>
            <Link to="/forgot-password" style={{ color: '#FBBF24', fontSize: '13px' }} className="hover:opacity-70 transition-opacity">
              Forgot password?
            </Link>
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-lg transition-opacity hover:opacity-90 active:opacity-80"
            style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
          >
            Sign In
          </button>
        </form>

        <p className="mt-6 text-center text-sm" style={{ color: '#6B7280' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: '#FBBF24' }} className="hover:opacity-70 transition-opacity">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

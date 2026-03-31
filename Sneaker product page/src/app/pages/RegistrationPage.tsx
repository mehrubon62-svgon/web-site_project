import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Eye, EyeOff, Check, X } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

function getPasswordStrength(pw: string): { level: number; label: string; color: string } {
  if (pw.length === 0) return { level: 0, label: '', color: '' };
  if (pw.length < 6) return { level: 1, label: 'Weak password', color: '#EF4444' };
  if (pw.length < 10 || !/[0-9]/.test(pw)) return { level: 2, label: 'Fair password', color: '#F59E0B' };
  return { level: 3, label: 'Good password', color: '#10B981' };
}

export function RegistrationPage() {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  const [showPw, setShowPw] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');

  const strength = getPasswordStrength(form.password);
  const passwordsMatch = form.confirm.length > 0 && form.password === form.confirm;
  const passwordsMismatch = form.confirm.length > 0 && form.password !== form.confirm;

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
    if (!form.username || !form.email || !form.password || !form.confirm) {
      setError('Please fill in all fields.');
      return;
    }
    if (form.password !== form.confirm) {
      setError('Passwords do not match.');
      return;
    }
    navigate('/email-sent');
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8" style={cardStyle}>
        <div className="mb-6">
          <div style={{ width: 40, height: 3, background: '#FBBF24', borderRadius: 2, marginBottom: 16 }} />
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 6 }}>
            Create Account
          </h1>
          <p style={{ color: '#6B7280', fontSize: '14px' }}>Join BuildBox today</p>
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
              placeholder="Choose a username"
              style={inputStyle}
              onFocus={e => e.target.style.borderColor = '#FBBF24'}
              onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
            />
          </div>

          <div>
            <label style={labelStyle}>Email</label>
            <input
              type="email"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              placeholder="Enter your email"
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
                placeholder="Create a password"
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
            {/* Strength bars */}
            {form.password.length > 0 && (
              <div className="mt-2">
                <div className="flex gap-1 mb-1">
                  {[1, 2, 3].map(i => (
                    <div
                      key={i}
                      className="flex-1 rounded-full transition-all"
                      style={{
                        height: 3,
                        background: i <= strength.level ? strength.color : (isDark ? '#374151' : '#E5E7EB'),
                        transition: 'background 0.3s',
                      }}
                    />
                  ))}
                </div>
                <span style={{ color: strength.color, fontSize: '12px' }}>{strength.label}</span>
              </div>
            )}
          </div>

          <div>
            <label style={labelStyle}>Confirm Password</label>
            <div className="relative">
              <input
                type={showConfirm ? 'text' : 'password'}
                value={form.confirm}
                onChange={e => setForm({ ...form, confirm: e.target.value })}
                placeholder="Confirm your password"
                style={{
                  ...inputStyle,
                  paddingRight: '42px',
                  borderColor: passwordsMismatch ? '#EF4444' : passwordsMatch ? '#10B981' : (isDark ? '#374151' : '#E5E7EB'),
                }}
                onFocus={e => e.target.style.borderColor = '#FBBF24'}
                onBlur={e => {
                  if (passwordsMismatch) e.target.style.borderColor = '#EF4444';
                  else if (passwordsMatch) e.target.style.borderColor = '#10B981';
                  else e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB';
                }}
              />
              <button
                type="button"
                onClick={() => setShowConfirm(!showConfirm)}
                className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60 transition-opacity"
                style={{ color: '#9CA3AF' }}
              >
                {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {form.confirm.length > 0 && (
              <div className="flex items-center gap-1 mt-1">
                {passwordsMatch ? (
                  <>
                    <Check size={12} style={{ color: '#10B981' }} />
                    <span style={{ color: '#10B981', fontSize: '12px' }}>Passwords match</span>
                  </>
                ) : (
                  <>
                    <X size={12} style={{ color: '#EF4444' }} />
                    <span style={{ color: '#EF4444', fontSize: '12px' }}>Passwords do not match</span>
                  </>
                )}
              </div>
            )}
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-lg transition-opacity hover:opacity-90 active:opacity-80"
            style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
          >
            Create Account
          </button>
        </form>

        <p className="mt-6 text-center text-sm" style={{ color: '#6B7280' }}>
          Already have an account?{' '}
          <Link to="/" style={{ color: '#FBBF24' }} className="hover:opacity-70 transition-opacity">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

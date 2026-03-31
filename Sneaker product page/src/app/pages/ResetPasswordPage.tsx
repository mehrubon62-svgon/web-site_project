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

export function ResetPasswordPage() {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  const [showPw, setShowPw] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [form, setForm] = useState({ password: '', confirm: '' });

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
    paddingRight: '42px',
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password && form.password === form.confirm) {
      navigate('/');
    }
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8" style={cardStyle}>
        <div className="mb-6">
          <div style={{ width: 40, height: 3, background: '#10B981', borderRadius: 2, marginBottom: 16 }} />
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 6 }}>
            Reset Password
          </h1>
          <p style={{ color: '#6B7280', fontSize: '14px' }}>Enter your new password</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label style={{ color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px', fontWeight: 500, display: 'block', marginBottom: '6px' }}>
              New Password
            </label>
            <div className="relative">
              <input
                type={showPw ? 'text' : 'password'}
                value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                placeholder="Enter new password"
                style={inputStyle}
                onFocus={e => e.target.style.borderColor = '#10B981'}
                onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
              />
              <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60" style={{ color: '#9CA3AF' }}>
                {showPw ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {form.password.length > 0 && (
              <div className="mt-2">
                <div className="flex gap-1 mb-1">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="flex-1 rounded-full" style={{ height: 3, background: i <= strength.level ? strength.color : (isDark ? '#374151' : '#E5E7EB'), transition: 'background 0.3s' }} />
                  ))}
                </div>
                <span style={{ color: strength.color, fontSize: '12px' }}>{strength.label}</span>
              </div>
            )}
          </div>

          <div>
            <label style={{ color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px', fontWeight: 500, display: 'block', marginBottom: '6px' }}>
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirm ? 'text' : 'password'}
                value={form.confirm}
                onChange={e => setForm({ ...form, confirm: e.target.value })}
                placeholder="Confirm new password"
                style={{ ...inputStyle, borderColor: passwordsMismatch ? '#EF4444' : passwordsMatch ? '#10B981' : (isDark ? '#374151' : '#E5E7EB') }}
              />
              <button type="button" onClick={() => setShowConfirm(!showConfirm)} className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60" style={{ color: '#9CA3AF' }}>
                {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {form.confirm.length > 0 && (
              <div className="flex items-center gap-1 mt-1">
                {passwordsMatch
                  ? <><Check size={12} style={{ color: '#10B981' }} /><span style={{ color: '#10B981', fontSize: '12px' }}>Passwords match</span></>
                  : <><X size={12} style={{ color: '#EF4444' }} /><span style={{ color: '#EF4444', fontSize: '12px' }}>Passwords do not match</span></>
                }
              </div>
            )}
          </div>

          {/* Requirements */}
          <div className="rounded-lg px-4 py-3 space-y-1" style={{ background: isDark ? '#111827' : '#F9FAFB' }}>
            <div className="flex items-center gap-2 text-sm" style={{ color: form.password.length >= 8 ? '#10B981' : '#6B7280' }}>
              <Check size={14} /> At least 8 characters
            </div>
            <div className="flex items-center gap-2 text-sm" style={{ color: /[0-9]/.test(form.password) ? '#10B981' : '#6B7280' }}>
              <Check size={14} /> Mix of letters and numbers
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-lg transition-opacity hover:opacity-90 active:opacity-80"
            style={{ background: '#10B981', color: '#FFFFFF', fontWeight: 500, fontSize: '15px' }}
          >
            Reset Password
          </button>
        </form>
      </div>
    </div>
  );
}

import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Eye, EyeOff, Check, X, ArrowLeft } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

function getPasswordStrength(pw: string) {
  if (pw.length === 0) return { level: 0, label: '', color: '' };
  if (pw.length < 6) return { level: 1, label: 'Weak password', color: '#EF4444' };
  if (pw.length < 10 || !/[0-9]/.test(pw)) return { level: 2, label: 'Fair password', color: '#F59E0B' };
  return { level: 3, label: 'Good password', color: '#10B981' };
}

export function ChangePasswordPage() {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  const [show, setShow] = useState({ current: false, newPw: false, confirm: false });
  const [form, setForm] = useState({ current: '', newPw: '', confirm: '' });
  const [success, setSuccess] = useState(false);

  const strength = getPasswordStrength(form.newPw);
  const match = form.confirm.length > 0 && form.newPw === form.confirm;
  const mismatch = form.confirm.length > 0 && form.newPw !== form.confirm;

  const cardStyle = {
    background: isDark ? '#1F2937' : '#FFFFFF',
    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
  };
  const inputStyle = {
    width: '100%', padding: '10px 14px', paddingRight: '42px',
    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
    borderRadius: '6px', background: isDark ? '#111827' : '#FFFFFF',
    color: isDark ? '#F9FAFB' : '#111827', fontSize: '15px', outline: 'none',
  };
  const label = (text: string) => (
    <label style={{ color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px', fontWeight: 500, display: 'block', marginBottom: '6px' }}>
      {text}
    </label>
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.current && form.newPw && match) {
      setSuccess(true);
      setTimeout(() => navigate('/home'), 1500);
    }
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8" style={cardStyle}>
        <div className="mb-6">
          <div style={{ width: 40, height: 3, background: '#FBBF24', borderRadius: 2, marginBottom: 16 }} />
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 6 }}>
            Change Password
          </h1>
          <p style={{ color: '#6B7280', fontSize: '14px' }}>Update your password</p>
        </div>

        {success && (
          <div className="mb-4 px-3 py-2 rounded-lg text-sm" style={{ background: '#ECFDF5', color: '#10B981', border: '1px solid #A7F3D0' }}>
            Password updated successfully! Redirecting...
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { key: 'current', label: 'Current Password', showKey: 'current' },
          ].map(field => (
            <div key={field.key}>
              {label(field.label)}
              <div className="relative">
                <input
                  type={show.current ? 'text' : 'password'}
                  value={form.current}
                  onChange={e => setForm({ ...form, current: e.target.value })}
                  placeholder="Enter current password"
                  style={inputStyle}
                  onFocus={e => e.target.style.borderColor = '#FBBF24'}
                  onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
                />
                <button type="button" onClick={() => setShow({ ...show, current: !show.current })} className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60" style={{ color: '#9CA3AF' }}>
                  {show.current ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
          ))}

          <div>
            {label('New Password')}
            <div className="relative">
              <input
                type={show.newPw ? 'text' : 'password'}
                value={form.newPw}
                onChange={e => setForm({ ...form, newPw: e.target.value })}
                placeholder="Enter new password"
                style={inputStyle}
                onFocus={e => e.target.style.borderColor = '#FBBF24'}
                onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
              />
              <button type="button" onClick={() => setShow({ ...show, newPw: !show.newPw })} className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60" style={{ color: '#9CA3AF' }}>
                {show.newPw ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {form.newPw.length > 0 && (
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
            {label('Confirm New Password')}
            <div className="relative">
              <input
                type={show.confirm ? 'text' : 'password'}
                value={form.confirm}
                onChange={e => setForm({ ...form, confirm: e.target.value })}
                placeholder="Confirm new password"
                style={{ ...inputStyle, borderColor: mismatch ? '#EF4444' : match ? '#10B981' : (isDark ? '#374151' : '#E5E7EB') }}
              />
              <button type="button" onClick={() => setShow({ ...show, confirm: !show.confirm })} className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60" style={{ color: '#9CA3AF' }}>
                {show.confirm ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {form.confirm.length > 0 && (
              <div className="flex items-center gap-1 mt-1">
                {match
                  ? <><Check size={12} style={{ color: '#10B981' }} /><span style={{ color: '#10B981', fontSize: '12px' }}>Passwords match</span></>
                  : <><X size={12} style={{ color: '#EF4444' }} /><span style={{ color: '#EF4444', fontSize: '12px' }}>Passwords do not match</span></>
                }
              </div>
            )}
          </div>

          <div className="rounded-lg px-4 py-3 space-y-1" style={{ background: isDark ? '#111827' : '#F9FAFB' }}>
            <div className="flex items-center gap-2 text-sm" style={{ color: form.newPw.length >= 8 ? '#10B981' : '#6B7280' }}>
              <Check size={14} /> At least 8 characters
            </div>
            <div className="flex items-center gap-2 text-sm" style={{ color: /[0-9]/.test(form.newPw) ? '#10B981' : '#6B7280' }}>
              <Check size={14} /> Mix of letters and numbers
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-lg transition-opacity hover:opacity-90 active:opacity-80"
            style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
          >
            Update Password
          </button>
        </form>

        <div className="mt-6 text-center">
          <Link to="/home" className="flex items-center justify-center gap-2 text-sm hover:opacity-70 transition-opacity" style={{ color: '#6B7280' }}>
            <ArrowLeft size={14} /> Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}

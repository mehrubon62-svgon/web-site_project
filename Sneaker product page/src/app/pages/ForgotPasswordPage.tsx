import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { ArrowLeft } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function ForgotPasswordPage() {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      navigate('/email-sent');
    }
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8" style={cardStyle}>
        <div className="mb-6">
          <div style={{ width: 40, height: 3, background: '#F59E0B', borderRadius: 2, marginBottom: 16 }} />
          <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 6 }}>
            Forgot Password?
          </h1>
          <p style={{ color: '#6B7280', fontSize: '14px' }}>We'll send you reset instructions</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label style={{ color: isDark ? '#9CA3AF' : '#6B7280', fontSize: '13px', fontWeight: 500, display: 'block', marginBottom: '6px' }}>
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="Enter your email address"
              style={inputStyle}
              onFocus={e => e.target.style.borderColor = '#F59E0B'}
              onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-lg transition-opacity hover:opacity-90 active:opacity-80"
            style={{ background: '#F59E0B', color: '#111827', fontWeight: 500, fontSize: '15px' }}
          >
            Send Reset Link
          </button>
        </form>

        <div className="mt-6 text-center">
          <Link
            to="/"
            className="flex items-center justify-center gap-2 text-sm hover:opacity-70 transition-opacity"
            style={{ color: '#6B7280' }}
          >
            <ArrowLeft size={14} />
            Back to login
          </Link>
        </div>
      </div>
    </div>
  );
}

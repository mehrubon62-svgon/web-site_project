import { Link } from 'react-router';
import { Mail } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function EmailSentPage() {
  const { isDark } = useTheme();

  const cardStyle = {
    background: isDark ? '#1F2937' : '#FFFFFF',
    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
    boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
  };

  return (
    <div className="w-full max-w-[400px]">
      <div className="rounded-lg p-8 text-center" style={cardStyle}>
        <div
          className="flex items-center justify-center w-16 h-16 rounded-full mx-auto mb-5"
          style={{ background: isDark ? '#111827' : '#FFFBEB', border: '2px solid #FBBF24' }}
        >
          <Mail size={32} style={{ color: '#FBBF24' }} />
        </div>

        <h1 style={{ fontSize: '26px', fontWeight: 700, color: isDark ? '#F9FAFB' : '#111827', marginBottom: 12 }}>
          Check Your Email
        </h1>
        <p className="text-sm leading-relaxed mb-6" style={{ color: '#6B7280' }}>
          We've sent a confirmation email to your inbox. Please click the link to verify your account.
        </p>

        <div
          className="rounded-lg px-4 py-4 mb-6 text-sm text-left"
          style={{ background: isDark ? '#111827' : '#F9FAFB', border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}` }}
        >
          <p className="font-medium mb-1" style={{ color: isDark ? '#F9FAFB' : '#111827' }}>Didn't receive the email?</p>
          <p style={{ color: '#6B7280' }}>Check your spam folder or wait a few minutes before requesting again.</p>
        </div>

        <Link
          to="/"
          className="block w-full py-3 rounded-lg transition-opacity hover:opacity-90 text-center"
          style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
        >
          Back to Login
        </Link>
      </div>
    </div>
  );
}

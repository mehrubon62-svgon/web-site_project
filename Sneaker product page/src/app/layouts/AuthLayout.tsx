import { Outlet } from 'react-router';
import { Link } from 'react-router';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon } from 'lucide-react';

export function AuthLayout() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: isDark ? '#111827' : '#F9FAFB' }}
    >
      {/* Simple header */}
      <header
        className="flex items-center justify-between px-6 py-4"
        style={{ borderBottom: `1px solid ${isDark ? '#374151' : '#E5E7EB'}` }}
      >
        <Link to="/home" className="hover:opacity-80 transition-opacity">
          <span style={{ fontSize: '22px', fontWeight: 700 }}>
            <span style={{ color: '#FBBF24' }}>Build</span>
            <span style={{ color: isDark ? '#FFFFFF' : '#1F2937' }}>Box</span>
          </span>
        </Link>
        <button
          onClick={toggleTheme}
          className="hover:opacity-70 transition-opacity"
          style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
        >
          {isDark ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </header>

      <main className="flex-1 flex items-center justify-center px-4 py-10">
        <Outlet />
      </main>

      <footer className="py-4 text-center text-sm" style={{ color: '#6B7280' }}>
        © 2026 BuildBox. All rights reserved.
      </footer>
    </div>
  );
}

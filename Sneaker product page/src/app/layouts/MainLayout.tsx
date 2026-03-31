import { Outlet } from 'react-router';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { AIChatWidget } from '../components/AIChatWidget';
import { useTheme } from '../context/ThemeContext';

export function MainLayout() {
  const { isDark } = useTheme();

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: isDark ? '#111827' : '#FFFFFF' }}
    >
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
      <AIChatWidget />
    </div>
  );
}

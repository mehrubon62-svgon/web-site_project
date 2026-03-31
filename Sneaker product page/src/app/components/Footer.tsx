import { Link } from 'react-router';
import { Facebook, Twitter, Instagram, Youtube, Mail, Phone, MapPin } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function Footer() {
  const { isDark } = useTheme();

  const quickLinks = [
    { label: 'Home', to: '/home' },
    { label: 'Browse Components', to: '/components' },
    { label: 'Laptops', to: '/laptops' },
    { label: 'PC Configurator', to: '/configurator' },
    { label: 'About Us', to: '/about' },
    { label: 'Contact', to: '/contact' },
  ];

  const customerLinks = [
    { label: 'Contact Us', to: '/contact' },
    { label: 'Shipping Information', to: '/shipping' },
    { label: 'Returns & Refunds', to: '/returns' },
    { label: 'FAQ', to: '/faq' },
    { label: 'Track Order', to: '/track' },
    { label: 'Support Center', to: '/support' },
  ];

  return (
    <footer style={{ background: isDark ? '#111827' : '#F9FAFB' }}>
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Col 1: About */}
          <div>
            <div className="mb-3">
              <span style={{ fontSize: '20px', fontWeight: 700 }}>
                <span style={{ color: '#FBBF24' }}>Build</span>
                <span style={{ color: isDark ? '#FFFFFF' : '#1F2937' }}>Box</span>
              </span>
            </div>
            <p className="text-sm leading-relaxed mb-4" style={{ color: '#6B7280' }}>
              Build your dream PC with confidence. Expert guidance and best prices.
            </p>
            <div className="flex items-center gap-3">
              {[Facebook, Twitter, Instagram, Youtube].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="hover:opacity-60 transition-opacity"
                  style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
                >
                  <Icon size={20} />
                </a>
              ))}
            </div>
          </div>

          {/* Col 2: Quick Links */}
          <div>
            <h4 className="text-sm font-semibold mb-4" style={{ color: isDark ? '#F9FAFB' : '#111827' }}>
              Quick Links
            </h4>
            <ul className="space-y-2">
              {quickLinks.map(link => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className="text-sm transition-colors hover:text-yellow-400"
                    style={{ color: '#6B7280' }}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 3: Customer Service */}
          <div>
            <h4 className="text-sm font-semibold mb-4" style={{ color: isDark ? '#F9FAFB' : '#111827' }}>
              Customer Service
            </h4>
            <ul className="space-y-2">
              {customerLinks.map(link => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className="text-sm transition-colors hover:text-yellow-400"
                    style={{ color: '#6B7280' }}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 4: Contact */}
          <div>
            <h4 className="text-sm font-semibold mb-4" style={{ color: isDark ? '#F9FAFB' : '#111827' }}>
              Contact
            </h4>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <Mail size={16} className="mt-0.5 flex-shrink-0" style={{ color: '#FBBF24' }} />
                <a href="mailto:support@buildbox.com" className="text-sm hover:text-yellow-400 transition-colors" style={{ color: '#6B7280' }}>
                  support@buildbox.com
                </a>
              </li>
              <li className="flex items-start gap-2">
                <Phone size={16} className="mt-0.5 flex-shrink-0" style={{ color: '#FBBF24' }} />
                <span className="text-sm" style={{ color: '#6B7280' }}>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-start gap-2">
                <MapPin size={16} className="mt-0.5 flex-shrink-0" style={{ color: '#FBBF24' }} />
                <span className="text-sm" style={{ color: '#6B7280' }}>123 Tech Street, Silicon Valley, CA</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div
          className="mt-10 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm"
          style={{ borderTop: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`, color: '#6B7280' }}
        >
          <span>© 2026 BuildBox. All rights reserved.</span>
          <div className="flex items-center gap-4">
            {/* Payment icons placeholder */}
            <div className="flex items-center gap-2">
              {['VISA', 'MC', 'AMEX', 'PP'].map(p => (
                <span
                  key={p}
                  className="px-2 py-1 rounded text-xs font-medium"
                  style={{
                    background: isDark ? '#374151' : '#E5E7EB',
                    color: isDark ? '#9CA3AF' : '#6B7280',
                    fontSize: '10px',
                  }}
                >
                  {p}
                </span>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-yellow-400 transition-colors">Privacy Policy</a>
            <span>|</span>
            <a href="#" className="hover:text-yellow-400 transition-colors">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

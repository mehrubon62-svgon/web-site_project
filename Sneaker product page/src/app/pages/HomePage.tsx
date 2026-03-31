import { Link } from 'react-router';
import { Shield, Zap, Tag, ChevronRight } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

const heroImg = "https://images.unsplash.com/photo-1717283413190-d4551453b92a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxnYW1pbmclMjBQQyUyMGRlc2t0b3AlMjBjb21wdXRlciUyMHNldHVwfGVufDF8fHx8MTc3NDc2MDk2M3ww&ixlib=rb-4.1.0&q=80&w=1080";

const features = [
  {
    icon: Shield,
    title: 'Compatibility Check',
    desc: 'Automatic verification ensures all components work perfectly together before you buy.',
  },
  {
    icon: Zap,
    title: 'Power Calculator',
    desc: 'Smart PSU recommendation based on your exact component selection and power needs.',
  },
  {
    icon: Tag,
    title: 'Best Prices',
    desc: 'Competitive pricing with real-time tracking to make sure you always get the best deal.',
  },
];

const popularComponents = [
  {
    id: 'cpu-1',
    name: 'Intel Core i9-13900K',
    category: 'Processor',
    price: 589.99,
    image: 'https://images.unsplash.com/photo-1670751782084-dffc982dc63b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxJbnRlbCUyMEFNRCUyMENQVSUyMHByb2Nlc3NvciUyMGNoaXB8ZW58MXx8fHwxNzc0ODAwODUyfDA&ixlib=rb-4.1.0&q=80&w=400',
    specs: '24 Cores • 5.8GHz Boost',
  },
  {
    id: 'gpu-1',
    name: 'NVIDIA RTX 4080 Super',
    category: 'GPU',
    price: 999.99,
    image: 'https://images.unsplash.com/photo-1591405351990-4726e331f141?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxOVklESUElMjBSVFglMjBncmFwaGljcyUyMGNhcmQlMjBHUFV8ZW58MXx8fHwxNzc0ODAwODUzfDA&ixlib=rb-4.1.0&q=80&w=400',
    specs: '16GB GDDR6X • 320W TDP',
  },
  {
    id: 'ram-1',
    name: 'Corsair Dominator DDR5',
    category: 'RAM',
    price: 189.99,
    image: 'https://images.unsplash.com/photo-1758577675588-c5bbbbbf8e97?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxERFI1JTIwUkFNJTIwbWVtb3J5JTIwbW9kdWxlcyUyMGNvbXB1dGVyfGVufDF8fHx8MTc3NDgwMDg1Nnww&ixlib=rb-4.1.0&q=80&w=400',
    specs: '32GB (2x16) • 6000MHz',
  },
  {
    id: 'mb-1',
    name: 'ASUS ROG Maximus Z790',
    category: 'Motherboard',
    price: 449.99,
    image: 'https://images.unsplash.com/photo-1723310437406-6232e12416db?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxBVFglMjBtb3RoZXJib2FyZCUyMGNpcmN1aXQlMjBib2FyZHxlbnwxfHx8fDE3NzQ4MDA4NTd8MA&ixlib=rb-4.1.0&q=80&w=400',
    specs: 'LGA1700 • DDR5 • ATX',
  },
];

export function HomePage() {
  const { isDark } = useTheme();

  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const secBg2 = isDark ? '#1F2937' : '#F9FAFB';
  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';

  return (
    <div style={{ background: sectionBg }}>
      {/* Hero */}
      <section style={{ background: sectionBg }} className="py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center gap-12">
          <div className="flex-1 text-center md:text-left">
            <h1 style={{ fontSize: '42px', fontWeight: 700, color: textPrimary, lineHeight: 1.2, letterSpacing: '-0.01em', marginBottom: 16 }}>
              Build Your<br />
              <span style={{ color: '#FBBF24' }}>Dream PC</span>
            </h1>
            <p className="text-lg mb-8" style={{ color: textSecondary, lineHeight: 1.6 }}>
              Configure, customize, and create the perfect computer with our intelligent compatibility system and expert guidance.
            </p>
            <div className="flex flex-wrap gap-3 justify-center md:justify-start">
              <Link
                to="/configurator"
                className="flex items-center gap-2 px-6 py-3 rounded-lg transition-opacity hover:opacity-90"
                style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
              >
                Start Building <ChevronRight size={16} />
              </Link>
              <Link
                to="/components"
                className="flex items-center gap-2 px-6 py-3 rounded-lg transition-opacity hover:opacity-90"
                style={{ border: '1px solid #FBBF24', color: '#FBBF24', fontWeight: 500, fontSize: '15px', background: 'transparent' }}
              >
                Browse Components
              </Link>
            </div>
          </div>
          <div className="flex-1 w-full max-w-lg">
            <div className="rounded-lg overflow-hidden" style={{ border: `1px solid ${border}` }}>
              <ImageWithFallback
                src={heroImg}
                alt="Gaming PC Setup"
                className="w-full object-cover"
                style={{ height: '300px' }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section style={{ background: sectionBg, borderTop: `1px solid ${border}` }} className="py-16">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-center mb-3" style={{ fontSize: '28px', fontWeight: 600, color: textPrimary }}>
            Why Choose BuildBox?
          </h2>
          <p className="text-center mb-10" style={{ color: textSecondary }}>Everything you need to build the perfect PC</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map(f => (
              <div
                key={f.title}
                className="rounded-lg p-6 transition-shadow"
                style={{ background: sectionBg, border: `1px solid ${border}` }}
                onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)')}
                onMouseLeave={e => (e.currentTarget.style.boxShadow = 'none')}
              >
                <div
                  className="flex items-center justify-center w-10 h-10 rounded-lg mb-4"
                  style={{ background: isDark ? '#111827' : '#FFFBEB' }}
                >
                  <f.icon size={22} style={{ color: '#FBBF24' }} />
                </div>
                <h3 className="mb-2" style={{ fontSize: '18px', fontWeight: 600, color: textPrimary }}>{f.title}</h3>
                <p className="text-sm leading-relaxed" style={{ color: textSecondary }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular products */}
      <section style={{ background: secBg2, borderTop: `1px solid ${border}` }} className="py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between mb-8">
            <h2 style={{ fontSize: '24px', fontWeight: 600, color: textPrimary }}>Popular Components</h2>
            <Link to="/components" className="text-sm hover:opacity-70 transition-opacity" style={{ color: '#FBBF24' }}>
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {popularComponents.map(item => (
              <div
                key={item.id}
                className="rounded-lg overflow-hidden transition-shadow"
                style={{ background: isDark ? '#1F2937' : '#FFFFFF', border: `1px solid ${border}` }}
                onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)')}
                onMouseLeave={e => (e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)')}
              >
                <div className="overflow-hidden" style={{ height: '180px' }}>
                  <ImageWithFallback src={item.image} alt={item.name} className="w-full h-full object-cover" />
                </div>
                <div className="p-4">
                  <span className="text-xs font-medium px-2 py-0.5 rounded" style={{ background: '#FFFBEB', color: '#F59E0B' }}>
                    {item.category}
                  </span>
                  <h4 className="mt-2 mb-1 text-sm font-semibold" style={{ color: textPrimary }}>{item.name}</h4>
                  <p className="text-xs mb-3" style={{ color: textSecondary }}>{item.specs}</p>
                  <div className="flex items-center justify-between">
                    <span className="font-bold" style={{ color: textPrimary, fontSize: '16px' }}>${item.price}</span>
                    <Link to={`/components/${item.id}`} className="text-xs hover:opacity-70" style={{ color: '#FBBF24' }}>View →</Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{ background: secBg2, borderTop: `1px solid ${border}` }} className="py-16">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 style={{ fontSize: '28px', fontWeight: 600, color: textPrimary, marginBottom: 12 }}>
            Ready to Build?
          </h2>
          <p className="mb-8" style={{ color: textSecondary }}>
            Join thousands who built their dream PC with BuildBox
          </p>
          <Link
            to="/configurator"
            className="inline-block px-8 py-3 rounded-lg transition-opacity hover:opacity-90"
            style={{ background: '#FBBF24', color: '#111827', fontWeight: 500, fontSize: '15px' }}
          >
            Get Started Now
          </Link>
        </div>
      </section>
    </div>
  );
}

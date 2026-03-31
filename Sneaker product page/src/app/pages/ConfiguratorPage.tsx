import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router';
import {
  Cpu, Monitor, Server, MemoryStick, HardDrive, Zap, Box,
  X, Plus, Save, Upload, CheckCircle, AlertTriangle, XCircle, ShoppingCart
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { products } from '../data/products';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';
import {
  type BuildSlotKey,
  type StoredComponent,
  getSavedConfigurationById,
  getSavedConfigurations,
  saveConfiguration,
} from '../utils/configurationStore';

interface SelectedComponent extends StoredComponent {
  power?: number;
  socket?: string;
  ramType?: string;
  formFactor?: string;
}

interface BuildSlot {
  key: BuildSlotKey;
  label: string;
  Icon: React.ElementType;
  power: number;
}

const BUILD_SLOTS: BuildSlot[] = [
  { key: 'processor', label: 'Processor', Icon: Cpu, power: 125 },
  { key: 'gpu', label: 'Graphics Card', Icon: Monitor, power: 250 },
  { key: 'motherboard', label: 'Motherboard', Icon: Server, power: 80 },
  { key: 'ram', label: 'RAM', Icon: MemoryStick, power: 10 },
  { key: 'storage', label: 'Storage', Icon: HardDrive, power: 8 },
  { key: 'psu', label: 'Power Supply', Icon: Zap, power: 0 },
  { key: 'case', label: 'Case', Icon: Box, power: 0 },
];

const MOCK_PSU = {
  id: 'psu-1',
  name: 'Corsair RM850x',
  manufacturer: 'Corsair',
  price: 129.99,
  image: 'https://images.unsplash.com/photo-1591405351990-4726e331f141?w=400&q=80',
  specs: ['850W', '80 Plus Gold', 'Fully Modular'],
  power: 0,
};

const MOCK_CASE = {
  id: 'case-1',
  name: 'Lian Li PC-O11 Dynamic',
  manufacturer: 'Lian Li',
  price: 139.99,
  image: 'https://images.unsplash.com/photo-1738245494097-9b1e3971c3eb?w=400&q=80',
  specs: ['ATX/E-ATX', '420mm GPU Length', '360mm Radiator'],
  power: 0,
};

const PSU_TIERS = [450, 550, 650, 750, 850, 1000, 1200, 1500];

function parseWattage(specs: string[]): number | null {
  for (const spec of specs) {
    const match = spec.match(/(\d+)\s*W/i);
    if (match) return Number(match[1]);
  }
  return null;
}

function extractToken(specs: string[], pattern: RegExp): string | null {
  for (const spec of specs) {
    const match = spec.match(pattern);
    if (match) return match[1].toUpperCase();
  }
  return null;
}

function getRecommendedPsu(totalPower: number): number {
  const required = Math.ceil(totalPower * 1.25);
  for (const tier of PSU_TIERS) {
    if (tier >= required) return tier;
  }
  return 1500;
}

function ComponentModal({
  slotKey,
  onSelect,
  onClose,
  isDark,
}: {
  slotKey: BuildSlotKey;
  onSelect: (component: SelectedComponent) => void;
  onClose: () => void;
  isDark: boolean;
}) {
  const [search, setSearch] = useState('');
  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const cardBg = isDark ? '#374151' : '#F9FAFB';

  const available = (() => {
    let pool = products;
    if (slotKey === 'processor') pool = products.filter(p => p.category === 'Processors');
    else if (slotKey === 'gpu') pool = products.filter(p => p.category === 'GPUs');
    else if (slotKey === 'motherboard') pool = products.filter(p => p.category === 'Motherboards');
    else if (slotKey === 'ram') pool = products.filter(p => p.category === 'RAM');
    else if (slotKey === 'storage') pool = products.filter(p => p.category === 'Storage');
    else if (slotKey === 'psu') return [MOCK_PSU];
    else if (slotKey === 'case') return [MOCK_CASE];
    return pool;
  })();

  const filtered = available.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.manufacturer.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(0,0,0,0.5)' }}
      onClick={onClose}
    >
      <div
        className="w-full max-w-4xl max-h-[85vh] rounded-lg flex flex-col overflow-hidden"
        style={{ background: isDark ? '#1F2937' : '#FFFFFF', boxShadow: '0 8px 16px rgba(0,0,0,0.15)' }}
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b" style={{ borderColor: border }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600, color: textPrimary }}>
            Select {BUILD_SLOTS.find(s => s.key === slotKey)?.label}
          </h2>
          <button onClick={onClose} className="hover:opacity-60 transition-opacity" style={{ color: textSecondary }}>
            <X size={20} />
          </button>
        </div>

        <div className="px-5 py-3 border-b" style={{ borderColor: border }}>
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search..."
            autoFocus
            style={{
              width: '100%',
              padding: '8px 14px',
              border: `1px solid ${border}`,
              borderRadius: '6px',
              background: isDark ? '#111827' : '#F9FAFB',
              color: textPrimary,
              fontSize: '14px',
              outline: 'none',
            }}
            onFocus={e => (e.target.style.borderColor = '#FBBF24')}
            onBlur={e => (e.target.style.borderColor = border)}
          />
        </div>

        <div className="flex-1 overflow-y-auto p-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map(product => (
              <div
                key={product.id}
                className="rounded-lg p-3 cursor-pointer transition-shadow hover:shadow-md"
                style={{ background: cardBg, border: `1px solid ${border}` }}
                onClick={() => onSelect({ ...product, power: 0 })}
              >
                <div className="flex gap-3">
                  <div className="w-16 h-16 rounded overflow-hidden flex-shrink-0">
                    <ImageWithFallback src={product.image} alt={product.name} className="w-full h-full object-cover" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold mb-1 line-clamp-2" style={{ color: textPrimary }}>{product.name}</p>
                    <p className="text-xs mb-2" style={{ color: textSecondary }}>{product.specs[0]}</p>
                    <p className="text-sm font-bold" style={{ color: textPrimary }}>${product.price.toFixed(2)}</p>
                  </div>
                </div>
                <button
                  className="mt-3 w-full py-1.5 rounded text-sm font-medium transition-opacity hover:opacity-90"
                  style={{ background: '#FBBF24', color: '#111827' }}
                  onClick={e => { e.stopPropagation(); onSelect({ ...product, power: 0 }); }}
                >
                  Select
                </button>
              </div>
            ))}
          </div>
          {filtered.length === 0 && (
            <p className="text-center py-8 text-sm" style={{ color: textSecondary }}>No components found</p>
          )}
        </div>
      </div>
    </div>
  );
}

export function ConfiguratorPage() {
  const { isDark } = useTheme();
  const { addToCart } = useCart();
  const navigate = useNavigate();
  const location = useLocation();

  const [build, setBuild] = useState<Record<BuildSlotKey, SelectedComponent | null>>({
    processor: null,
    gpu: null,
    motherboard: null,
    ram: null,
    storage: null,
    psu: null,
    case: null,
  });
  const [activeModal, setActiveModal] = useState<BuildSlotKey | null>(null);
  const [configName, setConfigName] = useState('My Gaming Build');

  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const sectionBg = isDark ? '#111827' : '#FFFFFF';

  useEffect(() => {
    const maybeId = (location.state as { configId?: string } | null)?.configId;
    if (!maybeId) return;
    const stored = getSavedConfigurationById(maybeId);
    if (!stored) return;

    setConfigName(stored.name);
    setBuild({
      processor: stored.build.processor ?? null,
      gpu: stored.build.gpu ?? null,
      motherboard: stored.build.motherboard ?? null,
      ram: stored.build.ram ?? null,
      storage: stored.build.storage ?? null,
      psu: stored.build.psu ?? null,
      case: stored.build.case ?? null,
    });
  }, [location.state]);

  const selectComponent = (slot: BuildSlotKey, component: SelectedComponent) => {
    setBuild(prev => ({ ...prev, [slot]: component }));
    setActiveModal(null);
  };

  const removeComponent = (slot: BuildSlotKey) => {
    setBuild(prev => ({ ...prev, [slot]: null }));
  };

  const totalPrice = useMemo(() => Object.values(build).reduce((sum, c) => sum + (c?.price ?? 0), 0), [build]);
  const tax = totalPrice * 0.01;
  const grandTotal = totalPrice + tax;

  const totalPower = useMemo(() => {
    return BUILD_SLOTS.reduce((sum, slot) => {
      const component = build[slot.key];
      if (!component) return sum;
      const parsed = parseWattage(component.specs);
      return sum + (parsed ?? slot.power);
    }, 85);
  }, [build]);

  const recommendedPSU = getRecommendedPsu(totalPower);
  const selectedPsuWattage = build.psu ? parseWattage(build.psu.specs) : null;
  const maxPower = 1200;
  const powerPercent = Math.min((totalPower / maxPower) * 100, 100);
  const powerColor = powerPercent < 60 ? '#10B981' : powerPercent < 80 ? '#F59E0B' : '#EF4444';

  const compatibilityIssues = useMemo(() => {
    const issues: string[] = [];

    const cpuSocket = build.processor ? extractToken(build.processor.specs, /(LGA\d+|AM\d+)/i) : null;
    const mbSocket = build.motherboard ? extractToken(build.motherboard.specs, /(LGA\d+|AM\d+)/i) : null;
    if (cpuSocket && mbSocket && cpuSocket !== mbSocket) {
      issues.push(`Socket mismatch: CPU ${cpuSocket} / MB ${mbSocket}`);
    }

    const ramType = build.ram ? extractToken(build.ram.specs, /(DDR\d)/i) : null;
    const mbRamType = build.motherboard ? extractToken(build.motherboard.specs, /(DDR\d)/i) : null;
    if (ramType && mbRamType && ramType !== mbRamType) {
      issues.push(`RAM mismatch: ${ramType} RAM with ${mbRamType} motherboard`);
    }

    if (selectedPsuWattage && selectedPsuWattage < recommendedPSU) {
      issues.push(`PSU too weak: ${selectedPsuWattage}W selected, ${recommendedPSU}W recommended`);
    }

    return issues;
  }, [build, recommendedPSU, selectedPsuWattage]);

  const requiredSlots: BuildSlotKey[] = ['processor', 'gpu', 'motherboard', 'ram', 'storage'];
  const isIncomplete = requiredSlots.some(slot => !build[slot]);
  const compatStatus: 'empty' | 'incomplete' | 'compatible' | 'issues' =
    Object.values(build).every(v => !v)
      ? 'empty'
      : compatibilityIssues.length > 0
      ? 'issues'
      : isIncomplete
      ? 'incomplete'
      : 'compatible';

  const handleAddToCart = () => {
    Object.values(build).forEach(component => {
      if (!component) return;
      addToCart({ id: component.id, name: component.name, price: component.price, image: component.image, category: 'PC Build' });
    });
    navigate('/cart');
  };

  const handleSaveConfiguration = () => {
    saveConfiguration({
      name: configName.trim() || 'My Build',
      build: Object.fromEntries(Object.entries(build).filter(([, value]) => !!value)) as Partial<Record<BuildSlotKey, StoredComponent>>,
      totalPrice,
      compatibility: compatStatus === 'issues' ? 'issues' : compatStatus === 'compatible' ? 'compatible' : 'warnings',
    });
    navigate('/configurations');
  };

  const handleLoadLatest = () => {
    const latest = getSavedConfigurations()[0];
    if (!latest) return;
    setConfigName(latest.name);
    setBuild({
      processor: latest.build.processor ?? null,
      gpu: latest.build.gpu ?? null,
      motherboard: latest.build.motherboard ?? null,
      ram: latest.build.ram ?? null,
      storage: latest.build.storage ?? null,
      psu: latest.build.psu ?? null,
      case: latest.build.case ?? null,
    });
  };

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      {activeModal && (
        <ComponentModal
          slotKey={activeModal}
          onSelect={c => selectComponent(activeModal, c)}
          onClose={() => setActiveModal(null)}
          isDark={isDark}
        />
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 style={{ fontSize: '28px', fontWeight: 700, color: textPrimary, letterSpacing: '-0.01em' }}>Build Your PC</h1>
            <p className="mt-1 text-sm" style={{ color: textSecondary }}>Pick components, get exact compatibility and PSU guidance.</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleLoadLatest}
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-opacity hover:opacity-80"
              style={{ border: `1px solid #FBBF24`, color: '#FBBF24', background: 'transparent' }}
            >
              <Upload size={16} /> Load
            </button>
            <Link
              to="/configurations"
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-opacity hover:opacity-80"
              style={{ border: `1px solid #FBBF24`, color: '#FBBF24', background: 'transparent' }}
            >
              <Save size={16} /> Saved Builds
            </Link>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-5">
          <div className="flex-1 space-y-2.5">
            {BUILD_SLOTS.map(slot => {
              const selected = build[slot.key];
              return (
                <div
                  key={slot.key}
                  className="rounded-lg p-3.5 transition-shadow"
                  style={{ background: cardBg, border: `1px solid ${border}`, boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }}
                >
                  {selected ? (
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded overflow-hidden flex-shrink-0">
                        <ImageWithFallback src={selected.image} alt={selected.name} className="w-full h-full object-cover" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-0.5">
                          <slot.Icon size={14} style={{ color: '#FBBF24' }} />
                          <span className="text-xs font-medium" style={{ color: textSecondary }}>{slot.label}</span>
                        </div>
                        <p className="text-sm font-semibold truncate" style={{ color: textPrimary }}>{selected.name}</p>
                      </div>
                      <div className="flex items-center gap-3 flex-shrink-0">
                        <span className="font-bold" style={{ color: textPrimary }}>${selected.price.toFixed(2)}</span>
                        <button onClick={() => setActiveModal(slot.key)} className="text-xs" style={{ color: '#FBBF24' }}>Change</button>
                        <button onClick={() => removeComponent(slot.key)} style={{ color: textSecondary }}><X size={16} /></button>
                      </div>
                    </div>
                  ) : (
                    <button className="w-full flex items-center gap-3 group" onClick={() => setActiveModal(slot.key)}>
                      <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: isDark ? '#374151' : '#F3F4F6' }}>
                        <slot.Icon size={18} style={{ color: '#9CA3AF' }} />
                      </div>
                      <div className="flex-1 text-left">
                        <p className="text-sm font-medium" style={{ color: textSecondary }}>{slot.label}</p>
                      </div>
                      <div className="flex items-center justify-center w-7 h-7 rounded-full" style={{ background: '#FBBF24', color: '#111827' }}>
                        <Plus size={14} />
                      </div>
                    </button>
                  )}
                </div>
              );
            })}
          </div>

          <div className="lg:w-[350px] space-y-3">
            <div className="rounded-lg p-4" style={{ background: cardBg, border: `1px solid ${border}` }}>
              <label className="text-xs font-medium block mb-2" style={{ color: textSecondary }}>BUILD NAME</label>
              <input
                type="text"
                value={configName}
                onChange={e => setConfigName(e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: `1px solid ${border}`,
                  borderRadius: '6px',
                  background: isDark ? '#111827' : '#F9FAFB',
                  color: textPrimary,
                  fontSize: '14px',
                  outline: 'none',
                  fontWeight: 600,
                }}
              />
            </div>

            <div className="rounded-lg p-4" style={{ background: cardBg, border: `1px solid ${border}` }}>
              <h3 className="text-sm font-semibold mb-3" style={{ color: textPrimary }}>Build Status</h3>

              {compatStatus === 'empty' && (
                <div className="flex items-center gap-2 p-2 rounded mb-3" style={{ background: isDark ? '#374151' : '#F3F4F6' }}>
                  <CheckCircle size={16} style={{ color: '#9CA3AF' }} />
                  <span className="text-xs" style={{ color: textSecondary }}>Add components to start checks</span>
                </div>
              )}
              {compatStatus === 'incomplete' && (
                <div className="flex items-center gap-2 p-2 rounded mb-3" style={{ background: '#FFFBEB' }}>
                  <AlertTriangle size={16} style={{ color: '#F59E0B' }} />
                  <span className="text-xs" style={{ color: '#92400E' }}>Build incomplete</span>
                </div>
              )}
              {compatStatus === 'compatible' && (
                <div className="flex items-center gap-2 p-2 rounded mb-3" style={{ background: '#D1FAE5' }}>
                  <CheckCircle size={16} style={{ color: '#10B981' }} />
                  <span className="text-xs" style={{ color: '#065F46' }}>All components compatible</span>
                </div>
              )}
              {compatStatus === 'issues' && (
                <div className="flex items-center gap-2 p-2 rounded mb-3" style={{ background: '#FEE2E2' }}>
                  <XCircle size={16} style={{ color: '#DC2626' }} />
                  <span className="text-xs" style={{ color: '#991B1B' }}>Compatibility issues found</span>
                </div>
              )}

              {compatibilityIssues.length > 0 && (
                <div className="space-y-1 mb-3">
                  {compatibilityIssues.map(issue => (
                    <p key={issue} className="text-xs" style={{ color: '#991B1B' }}>• {issue}</p>
                  ))}
                </div>
              )}

              <div className="mb-3">
                <div className="flex items-baseline gap-2">
                  <span style={{ fontSize: '24px', fontWeight: 700, color: textPrimary }}>{totalPower}W</span>
                  <span className="text-xs" style={{ color: textSecondary }}>estimated</span>
                </div>
                <p className="text-xs" style={{ color: textSecondary }}>
                  Recommended PSU: <strong style={{ color: textPrimary }}>{recommendedPSU}W</strong>
                </p>
                <div className="h-1.5 rounded-full overflow-hidden mt-2" style={{ background: isDark ? '#374151' : '#E5E7EB' }}>
                  <div className="h-full rounded-full transition-all duration-500" style={{ width: `${powerPercent}%`, background: powerColor }} />
                </div>
                <div className="flex justify-between mt-1">
                  <span className="text-xs" style={{ color: textSecondary }}>0W</span>
                  <span className="text-xs" style={{ color: textSecondary }}>{maxPower}W+</span>
                </div>
              </div>

              <div className="space-y-1.5 mb-3 pt-2 border-t" style={{ borderColor: border }}>
                <div className="flex justify-between text-sm"><span style={{ color: textSecondary }}>Subtotal</span><span style={{ color: textPrimary }}>${totalPrice.toFixed(2)}</span></div>
                <div className="flex justify-between text-sm"><span style={{ color: textSecondary }}>Tax (1%)</span><span style={{ color: textPrimary }}>${tax.toFixed(2)}</span></div>
                <div className="flex justify-between"><span className="font-semibold" style={{ color: textPrimary }}>Total</span><span style={{ fontSize: '20px', fontWeight: 700, color: textPrimary }}>${grandTotal.toFixed(2)}</span></div>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={Object.values(build).every(v => !v)}
                className="w-full py-3 rounded-lg text-sm font-medium transition-opacity hover:opacity-90 disabled:opacity-40 flex items-center justify-center gap-2"
                style={{ background: '#FBBF24', color: '#111827' }}
              >
                <ShoppingCart size={16} />
                Add Build to Cart
              </button>
              <button
                onClick={handleSaveConfiguration}
                className="w-full mt-2 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-80"
                style={{ border: `1px solid #FBBF24`, color: '#FBBF24', background: 'transparent' }}
              >
                <Save size={14} className="inline mr-1.5" />
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

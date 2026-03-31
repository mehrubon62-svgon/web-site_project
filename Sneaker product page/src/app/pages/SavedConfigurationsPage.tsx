import { useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Plus, Cpu, Monitor, Server, MemoryStick, HardDrive, Zap, Box, CheckCircle, AlertTriangle, Trash2, Copy, Edit3, ShoppingCart, XCircle } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { deleteSavedConfiguration, getSavedConfigurations, saveConfiguration, type StoredConfiguration } from '../utils/configurationStore';

const componentIcons = [
  { key: 'processor', Icon: Cpu },
  { key: 'gpu', Icon: Monitor },
  { key: 'motherboard', Icon: Server },
  { key: 'ram', Icon: MemoryStick },
  { key: 'storage', Icon: HardDrive },
  { key: 'psu', Icon: Zap },
  { key: 'case', Icon: Box },
] as const;

function CompatBadge({ status }: { status: StoredConfiguration['compatibility'] }) {
  if (status === 'compatible') return (
    <span className="flex items-center gap-1 text-xs px-2 py-0.5 rounded-full" style={{ background: '#D1FAE5', color: '#065F46' }}>
      <CheckCircle size={11} /> Compatible
    </span>
  );
  if (status === 'warnings') return (
    <span className="flex items-center gap-1 text-xs px-2 py-0.5 rounded-full" style={{ background: '#FEF3C7', color: '#92400E' }}>
      <AlertTriangle size={11} /> Warnings
    </span>
  );
  return (
    <span className="flex items-center gap-1 text-xs px-2 py-0.5 rounded-full" style={{ background: '#FEE2E2', color: '#991B1B' }}>
      <XCircle size={11} /> Issues
    </span>
  );
}

export function SavedConfigurationsPage() {
  const { isDark } = useTheme();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const [configs, setConfigs] = useState<StoredConfiguration[]>(() => getSavedConfigurations());

  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const sectionBg = isDark ? '#111827' : '#FFFFFF';

  const sorted = useMemo(() => [...configs], [configs]);

  const refresh = () => setConfigs(getSavedConfigurations());

  const removeConfig = (id: string) => {
    deleteSavedConfiguration(id);
    refresh();
  };

  const duplicateConfig = (config: StoredConfiguration) => {
    saveConfiguration({
      name: `${config.name} (Copy)`,
      build: config.build,
      totalPrice: config.totalPrice,
      compatibility: config.compatibility,
    });
    refresh();
  };

  const addConfigToCart = (config: StoredConfiguration) => {
    Object.values(config.build).forEach(component => {
      if (!component) return;
      addToCart({
        id: `${config.id}-${component.id}`,
        name: component.name,
        price: component.price,
        image: component.image,
        category: 'Saved Build',
      });
    });
    navigate('/cart');
  };

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 style={{ fontSize: '32px', fontWeight: 700, color: textPrimary, letterSpacing: '-0.01em' }}>My Configurations</h1>
            <p className="mt-1 text-sm" style={{ color: textSecondary }}>{sorted.length} saved build{sorted.length !== 1 ? 's' : ''}</p>
          </div>
          <Link to="/configurator" className="flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-90" style={{ background: '#FBBF24', color: '#111827' }}>
            <Plus size={16} /> Create New
          </Link>
        </div>

        {sorted.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 text-center">
            <div className="w-16 h-16 rounded-full flex items-center justify-center mb-4" style={{ background: isDark ? '#1F2937' : '#F3F4F6' }}><Cpu size={28} style={{ color: '#9CA3AF' }} /></div>
            <h2 className="mb-2" style={{ fontSize: '20px', fontWeight: 600, color: textPrimary }}>No configurations yet</h2>
            <p className="mb-6 text-sm" style={{ color: textSecondary }}>Start building your first PC and save it here</p>
            <Link to="/configurator" className="px-6 py-3 rounded-lg text-sm font-medium transition-opacity hover:opacity-90" style={{ background: '#FBBF24', color: '#111827' }}>Create New Build</Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {sorted.map(config => (
              <div key={config.id} className="rounded-lg p-5 transition-shadow" style={{ background: cardBg, border: `1px solid ${border}`, boxShadow: '0 1px 3px rgba(0,0,0,0.08)' }}>
                <div className="flex items-start justify-between mb-4">
                  <h3 className="font-semibold leading-tight" style={{ color: textPrimary, fontSize: '16px', maxWidth: '65%' }}>{config.name}</h3>
                  <CompatBadge status={config.compatibility} />
                </div>

                <div className="flex items-center gap-2 mb-4">
                  {componentIcons.map(({ key, Icon }) => {
                    const hasComponent = !!config.build[key];
                    return (
                      <div key={key} title={key} className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: hasComponent ? (isDark ? '#374151' : '#FFFBEB') : (isDark ? '#374151' : '#F3F4F6'), opacity: hasComponent ? 1 : 0.4 }}>
                        <Icon size={14} style={{ color: hasComponent ? '#FBBF24' : '#9CA3AF' }} />
                      </div>
                    );
                  })}
                </div>

                <div className="space-y-1 mb-4 pb-4 border-b" style={{ borderColor: border }}>
                  {Object.entries(config.build).slice(0, 3).map(([key, component]) => (
                    <p key={key} className="text-xs" style={{ color: textSecondary }}><span className="font-medium capitalize">{key}:</span> {component?.name}</p>
                  ))}
                  {Object.keys(config.build).length > 3 && <p className="text-xs" style={{ color: '#FBBF24' }}>+{Object.keys(config.build).length - 3} more components</p>}
                </div>

                <div className="flex items-center justify-between mb-4">
                  <span style={{ fontSize: '22px', fontWeight: 700, color: textPrimary }}>${config.totalPrice.toFixed(2)}</span>
                  <span className="text-xs" style={{ color: textSecondary }}>{new Date(config.createdAt).toLocaleDateString()}</span>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <button onClick={() => navigate('/configurator', { state: { configId: config.id } })} className="flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium transition-opacity hover:opacity-90" style={{ background: '#FBBF24', color: '#111827' }}>
                    <Edit3 size={13} /> Edit
                  </button>
                  <button onClick={() => addConfigToCart(config)} className="flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium transition-opacity hover:opacity-80" style={{ border: `1px solid ${border}`, color: textPrimary, background: 'transparent' }}>
                    <ShoppingCart size={13} /> Add to Cart
                  </button>
                </div>
                <div className="flex items-center justify-between mt-3 pt-2">
                  <button onClick={() => duplicateConfig(config)} className="text-xs hover:opacity-70 transition-opacity flex items-center gap-1" style={{ color: '#FBBF24' }}><Copy size={12} /> Duplicate</button>
                  <button onClick={() => removeConfig(config.id)} className="text-xs hover:opacity-70 transition-opacity flex items-center gap-1" style={{ color: '#EF4444' }}><Trash2 size={12} /> Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

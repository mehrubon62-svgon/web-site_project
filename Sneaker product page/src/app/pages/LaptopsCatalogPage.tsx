import { useState, useMemo } from 'react';
import { Link } from 'react-router';
import { Heart, ChevronRight } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { laptops } from '../data/products';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

const categories = ['Gaming', 'Office', 'Ultrabook', 'Workstation'];
const processors = ['Intel Core i9', 'Intel Core i7', 'Intel Core i5', 'AMD Ryzen 9', 'AMD Ryzen 7'];
const ramOptions = ['8GB', '16GB', '32GB', '64GB'];
const screenSizes = ['13-14"', '15-16"', '17"+'];

export function LaptopsCatalogPage() {
  const { isDark } = useTheme();
  const { addToCart, toggleWishlist, wishlistIds } = useCart();

  const [selectedCats, setSelectedCats] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState([0, 3000]);
  const [sortBy, setSortBy] = useState('name');

  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const sidebarBg = isDark ? '#1F2937' : '#F9FAFB';

  const filtered = useMemo(() => {
    let res = laptops.filter(l => {
      if (selectedCats.length && !selectedCats.includes(l.category)) return false;
      if (l.price < priceRange[0] || l.price > priceRange[1]) return false;
      return true;
    });
    if (sortBy === 'price-asc') res = [...res].sort((a, b) => a.price - b.price);
    else if (sortBy === 'price-desc') res = [...res].sort((a, b) => b.price - a.price);
    else if (sortBy === 'rating') res = [...res].sort((a, b) => b.rating - a.rating);
    return res;
  }, [selectedCats, priceRange, sortBy]);

  const toggleCat = (cat: string) =>
    setSelectedCats(prev => prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]);

  const catColor: Record<string, string> = {
    Gaming: '#EF4444', Workstation: '#3B82F6', Ultrabook: '#10B981', Office: '#8B5CF6',
  };

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm mb-6" style={{ color: textSecondary }}>
          <Link to="/home" style={{ color: '#FBBF24' }} className="hover:opacity-70">Home</Link>
          <ChevronRight size={14} />
          <span>Laptops</span>
        </div>

        <h1 className="mb-6" style={{ fontSize: '28px', fontWeight: 700, color: textPrimary }}>Laptops</h1>

        <div className="flex gap-6">
          {/* Sidebar */}
          <aside
            className="hidden lg:block w-[240px] flex-shrink-0 h-fit rounded-lg p-5"
            style={{ background: sidebarBg, border: `1px solid ${border}` }}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold" style={{ color: textPrimary }}>Filters</h3>
              <button onClick={() => { setSelectedCats([]); setPriceRange([0, 3000]); }} className="text-xs hover:opacity-70" style={{ color: '#FBBF24' }}>
                Clear All
              </button>
            </div>

            <div className="mb-5">
              <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>CATEGORY</p>
              {categories.map(cat => (
                <label key={cat} className="flex items-center gap-2 py-1 cursor-pointer">
                  <input type="checkbox" checked={selectedCats.includes(cat)} onChange={() => toggleCat(cat)} style={{ accentColor: '#FBBF24' }} />
                  <span className="text-sm" style={{ color: textPrimary }}>{cat}</span>
                </label>
              ))}
            </div>

            <div className="mb-5">
              <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>PRICE RANGE</p>
              <div className="flex justify-between text-sm mb-2" style={{ color: textSecondary }}>
                <span>${priceRange[0]}</span><span>${priceRange[1]}</span>
              </div>
              <input type="range" min={0} max={3000} value={priceRange[1]} onChange={e => setPriceRange([0, Number(e.target.value)])} className="w-full" style={{ accentColor: '#FBBF24' }} />
            </div>

            <div className="mb-5">
              <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>PROCESSOR</p>
              {processors.map(p => (
                <label key={p} className="flex items-center gap-2 py-1 cursor-pointer">
                  <input type="checkbox" style={{ accentColor: '#FBBF24' }} />
                  <span className="text-sm" style={{ color: textPrimary }}>{p}</span>
                </label>
              ))}
            </div>

            <div>
              <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>SCREEN SIZE</p>
              {screenSizes.map(s => (
                <label key={s} className="flex items-center gap-2 py-1 cursor-pointer">
                  <input type="checkbox" style={{ accentColor: '#FBBF24' }} />
                  <span className="text-sm" style={{ color: textPrimary }}>{s}</span>
                </label>
              ))}
            </div>
          </aside>

          {/* Main */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <span className="text-sm" style={{ color: textSecondary }}>{filtered.length} laptops</span>
              <select
                value={sortBy}
                onChange={e => setSortBy(e.target.value)}
                className="text-sm rounded px-3 py-1.5"
                style={{ border: `1px solid ${border}`, background: cardBg, color: textPrimary, outline: 'none' }}
              >
                <option value="name">Name A-Z</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
                <option value="rating">Best Rated</option>
              </select>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
              {filtered.map(laptop => {
                const inWishlist = wishlistIds.has(laptop.id);
                return (
                  <div
                    key={laptop.id}
                    className="rounded-lg overflow-hidden transition-shadow"
                    style={{ background: cardBg, border: `1px solid ${border}`, boxShadow: '0 1px 3px rgba(0,0,0,0.08)' }}
                    onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)')}
                    onMouseLeave={e => (e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)')}
                  >
                    <div className="relative overflow-hidden" style={{ height: '200px' }}>
                      <ImageWithFallback src={laptop.image} alt={laptop.name} className="w-full h-full object-cover" />
                      <span
                        className="absolute top-3 left-3 text-xs px-2 py-0.5 rounded font-medium"
                        style={{ background: catColor[laptop.category] || '#FBBF24', color: '#FFFFFF' }}
                      >
                        {laptop.category}
                      </span>
                      <button
                        onClick={() => toggleWishlist(laptop.id)}
                        className="absolute top-3 right-3 w-7 h-7 flex items-center justify-center rounded-full hover:opacity-70"
                        style={{ background: 'rgba(255,255,255,0.9)', color: inWishlist ? '#EF4444' : '#6B7280' }}
                      >
                        <Heart size={14} fill={inWishlist ? '#EF4444' : 'none'} />
                      </button>
                    </div>
                    <div className="p-4">
                      <p className="text-xs mb-1" style={{ color: textSecondary }}>{laptop.manufacturer}</p>
                      <h3 className="text-sm font-semibold mb-2" style={{ color: textPrimary }}>{laptop.name}</h3>
                      <ul className="mb-3 space-y-0.5">
                        {laptop.specs.map((spec, i) => (
                          <li key={i} className="text-xs" style={{ color: textSecondary }}>• {spec}</li>
                        ))}
                      </ul>
                      <div className="flex items-center justify-between text-xs mb-3" style={{ color: textSecondary }}>
                        <span>{laptop.screenSize}" Display</span>
                        <span>{laptop.refreshRate}Hz</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="font-bold" style={{ color: textPrimary, fontSize: '18px' }}>${laptop.price.toLocaleString()}</span>
                      </div>
                      <button
                        onClick={() => addToCart({ id: laptop.id, name: laptop.name, price: laptop.price, image: laptop.image, category: 'Laptops' })}
                        className="w-full mt-3 py-2 rounded text-sm font-medium transition-opacity hover:opacity-90"
                        style={{ background: '#FBBF24', color: '#111827' }}
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState, useMemo } from 'react';
import { Link } from 'react-router';
import { Heart, SlidersHorizontal, Grid, List, ChevronRight, X } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { products } from '../data/products';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

const categories = ['Processors', 'GPUs', 'Motherboards', 'RAM', 'Storage', 'Power Supplies', 'Cases'];
const manufacturers = ['Intel', 'AMD', 'NVIDIA', 'ASUS', 'MSI', 'Corsair', 'Samsung', 'Lian Li', 'G.Skill'];

export function ComponentsCatalogPage() {
  const { isDark } = useTheme();
  const { addToCart, toggleWishlist, wishlistIds } = useCart();

  const [selectedCats, setSelectedCats] = useState<string[]>([]);
  const [selectedMfrs, setSelectedMfrs] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState([0, 1500]);
  const [inStockOnly, setInStockOnly] = useState(false);
  const [sortBy, setSortBy] = useState('name');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(false);

  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const sidebarBg = isDark ? '#1F2937' : '#F9FAFB';

  const filtered = useMemo(() => {
    let res = products.filter(p => {
      if (selectedCats.length && !selectedCats.includes(p.category)) return false;
      if (selectedMfrs.length && !selectedMfrs.includes(p.manufacturer)) return false;
      if (p.price < priceRange[0] || p.price > priceRange[1]) return false;
      if (inStockOnly && p.stock === 0) return false;
      return true;
    });
    if (sortBy === 'price-asc') res = [...res].sort((a, b) => a.price - b.price);
    else if (sortBy === 'price-desc') res = [...res].sort((a, b) => b.price - a.price);
    else if (sortBy === 'rating') res = [...res].sort((a, b) => b.rating - a.rating);
    else res = [...res].sort((a, b) => a.name.localeCompare(b.name));
    return res;
  }, [selectedCats, selectedMfrs, priceRange, inStockOnly, sortBy]);

  const toggleCat = (cat: string) =>
    setSelectedCats(prev => prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]);

  const toggleMfr = (mfr: string) =>
    setSelectedMfrs(prev => prev.includes(mfr) ? prev.filter(m => m !== mfr) : [...prev, mfr]);

  const clearFilters = () => {
    setSelectedCats([]);
    setSelectedMfrs([]);
    setPriceRange([0, 1500]);
    setInStockOnly(false);
  };

  const stockDot = (stock: number) => {
    if (stock === 0) return { color: '#EF4444', label: 'Out of Stock' };
    if (stock <= 3) return { color: '#F59E0B', label: `Only ${stock} left` };
    return { color: '#10B981', label: 'In Stock' };
  };

  const Sidebar = () => (
    <aside
      className="w-full lg:w-[260px] flex-shrink-0"
      style={{ background: sidebarBg, border: `1px solid ${border}`, borderRadius: '8px', padding: '20px', height: 'fit-content' }}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold" style={{ color: textPrimary }}>Filters</h3>
        <button onClick={clearFilters} className="text-xs hover:opacity-70" style={{ color: '#FBBF24' }}>Clear All</button>
      </div>

      {/* Categories */}
      <div className="mb-5">
        <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>CATEGORY</p>
        {categories.map(cat => (
          <label key={cat} className="flex items-center gap-2 py-1 cursor-pointer">
            <input
              type="checkbox"
              checked={selectedCats.includes(cat)}
              onChange={() => toggleCat(cat)}
              style={{ accentColor: '#FBBF24' }}
            />
            <span className="text-sm" style={{ color: textPrimary }}>{cat}</span>
          </label>
        ))}
      </div>

      {/* Price */}
      <div className="mb-5">
        <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>PRICE RANGE</p>
        <div className="flex items-center justify-between text-sm mb-2" style={{ color: textSecondary }}>
          <span>${priceRange[0]}</span>
          <span>${priceRange[1]}</span>
        </div>
        <input
          type="range"
          min={0}
          max={1500}
          value={priceRange[1]}
          onChange={e => setPriceRange([priceRange[0], Number(e.target.value)])}
          className="w-full"
          style={{ accentColor: '#FBBF24' }}
        />
      </div>

      {/* Manufacturers */}
      <div className="mb-5">
        <p className="text-xs font-medium mb-2" style={{ color: textSecondary }}>MANUFACTURER</p>
        {manufacturers.map(mfr => (
          <label key={mfr} className="flex items-center gap-2 py-1 cursor-pointer">
            <input
              type="checkbox"
              checked={selectedMfrs.includes(mfr)}
              onChange={() => toggleMfr(mfr)}
              style={{ accentColor: '#FBBF24' }}
            />
            <span className="text-sm" style={{ color: textPrimary }}>{mfr}</span>
          </label>
        ))}
      </div>

      {/* In stock */}
      <label className="flex items-center gap-2 cursor-pointer">
        <div
          onClick={() => setInStockOnly(!inStockOnly)}
          className="relative w-9 h-5 rounded-full transition-colors cursor-pointer"
          style={{ background: inStockOnly ? '#FBBF24' : (isDark ? '#374151' : '#D1D5DB') }}
        >
          <div
            className="absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform"
            style={{ transform: inStockOnly ? 'translateX(18px)' : 'translateX(2px)' }}
          />
        </div>
        <span className="text-sm" style={{ color: textPrimary }}>In Stock Only</span>
      </label>
    </aside>
  );

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm mb-6" style={{ color: textSecondary }}>
          <Link to="/home" className="hover:opacity-70" style={{ color: '#FBBF24' }}>Home</Link>
          <ChevronRight size={14} />
          <span>Components</span>
        </div>

        <div className="flex gap-6">
          {/* Sidebar - desktop */}
          <div className="hidden lg:block">
            <Sidebar />
          </div>

          {/* Main content */}
          <div className="flex-1 min-w-0">
            {/* Header bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
              <span className="text-sm" style={{ color: textSecondary }}>{filtered.length} products</span>
              <div className="flex items-center gap-3">
                {/* Mobile filter toggle */}
                <button
                  className="lg:hidden flex items-center gap-1 px-3 py-1.5 rounded text-sm"
                  style={{ border: `1px solid ${border}`, color: textPrimary }}
                  onClick={() => setShowFilters(!showFilters)}
                >
                  <SlidersHorizontal size={14} /> Filters
                </button>

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
                <div className="flex gap-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className="p-1.5 rounded"
                    style={{ background: viewMode === 'grid' ? '#FBBF24' : 'transparent', color: viewMode === 'grid' ? '#111827' : textSecondary }}
                  >
                    <Grid size={16} />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className="p-1.5 rounded"
                    style={{ background: viewMode === 'list' ? '#FBBF24' : 'transparent', color: viewMode === 'list' ? '#111827' : textSecondary }}
                  >
                    <List size={16} />
                  </button>
                </div>
              </div>
            </div>

            {/* Mobile filters */}
            {showFilters && (
              <div className="lg:hidden mb-6">
                <Sidebar />
              </div>
            )}

            {/* Product grid */}
            <div className={viewMode === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4' : 'space-y-4'}>
              {filtered.map(product => {
                const stock = stockDot(product.stock);
                const inWishlist = wishlistIds.has(product.id);
                return (
                  <div
                    key={product.id}
                    className={`rounded-lg overflow-hidden transition-shadow ${viewMode === 'list' ? 'flex gap-4' : ''}`}
                    style={{ background: cardBg, border: `1px solid ${border}`, boxShadow: '0 1px 3px rgba(0,0,0,0.08)' }}
                    onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)')}
                    onMouseLeave={e => (e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)')}
                  >
                    <div className={`relative overflow-hidden flex-shrink-0 ${viewMode === 'list' ? 'w-36 h-36' : 'h-52'}`}>
                      <ImageWithFallback src={product.image} alt={product.name} className="w-full h-full object-cover" />
                      <button
                        onClick={() => toggleWishlist(product.id)}
                        className="absolute top-2 right-2 w-8 h-8 flex items-center justify-center rounded-full transition-opacity hover:opacity-70"
                        style={{ background: 'rgba(255,255,255,0.9)', color: inWishlist ? '#EF4444' : '#6B7280' }}
                      >
                        <Heart size={16} fill={inWishlist ? '#EF4444' : 'none'} />
                      </button>
                    </div>
                    <div className="p-4 flex flex-col flex-1">
                      <h4 className="text-sm font-semibold mb-1 line-clamp-2" style={{ color: textPrimary }}>{product.name}</h4>
                      <ul className="mb-2">
                        {product.specs.slice(0, 2).map((s, i) => (
                          <li key={i} className="text-xs" style={{ color: textSecondary }}>• {s}</li>
                        ))}
                      </ul>
                      <div className="flex items-center gap-1 mb-3">
                        <span className="w-1.5 h-1.5 rounded-full" style={{ background: stock.color }} />
                        <span className="text-xs" style={{ color: stock.color }}>{stock.label}</span>
                      </div>
                      <div className="mt-auto">
                        <p className="font-bold mb-2" style={{ color: textPrimary, fontSize: '18px' }}>${product.price.toFixed(2)}</p>
                        <button
                          onClick={() => addToCart({ id: product.id, name: product.name, price: product.price, image: product.image, category: product.category })}
                          className="w-full py-2 rounded text-sm font-medium transition-opacity hover:opacity-90"
                          style={{ background: '#FBBF24', color: '#111827' }}
                          disabled={product.stock === 0}
                        >
                          Add to Cart
                        </button>
                        <Link
                          to={`/components/${product.id}`}
                          className="block text-center text-xs mt-2 hover:opacity-70"
                          style={{ color: '#FBBF24' }}
                        >
                          View Details
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {filtered.length === 0 && (
              <div className="text-center py-16" style={{ color: textSecondary }}>
                <p className="text-lg mb-2">No products found</p>
                <button onClick={clearFilters} className="text-sm hover:opacity-70" style={{ color: '#FBBF24' }}>Clear filters</button>
              </div>
            )}

            {/* Pagination */}
            <div className="flex items-center justify-center gap-2 mt-8">
              {[1, 2, 3, 4].map(n => (
                <button
                  key={n}
                  className="w-8 h-8 rounded text-sm font-medium transition-colors"
                  style={{
                    background: n === 1 ? '#FBBF24' : 'transparent',
                    color: n === 1 ? '#111827' : textSecondary,
                    border: `1px solid ${n === 1 ? '#FBBF24' : border}`,
                  }}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

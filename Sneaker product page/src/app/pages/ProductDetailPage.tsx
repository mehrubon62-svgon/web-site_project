import { useState } from 'react';
import { useParams, Link } from 'react-router';
import { Heart, Star, ChevronRight, Minus, Plus, ZoomIn } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { products } from '../data/products';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

const sampleReviews = [
  { id: 1, user: 'TechBuild Pro', avatar: 'T', rating: 5, date: 'Jan 15, 2026', comment: 'Absolutely incredible performance. I paired this with an RTX 4080 and it handles everything I throw at it effortlessly.' },
  { id: 2, user: 'GamingMaster', avatar: 'G', rating: 4, date: 'Dec 28, 2025', comment: 'Great processor, runs cool under load. Highly recommended for gaming builds.' },
  { id: 3, user: 'PCBuilder99', avatar: 'P', rating: 5, date: 'Nov 10, 2025', comment: 'Best CPU I\'ve ever owned. Worth every penny for the performance you get.' },
];

export function ProductDetailPage() {
  const { id } = useParams();
  const { isDark } = useTheme();
  const { addToCart, toggleWishlist, wishlistIds } = useCart();

  const product = products.find(p => p.id === id) || products[0];
  const [activeTab, setActiveTab] = useState<'description' | 'specs' | 'reviews'>('description');
  const [quantity, setQuantity] = useState(1);
  const [activeImg, setActiveImg] = useState(0);
  const inWishlist = wishlistIds.has(product.id);

  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';

  // Simulated gallery
  const images = [product.image, product.image, product.image, product.image];

  const relatedProducts = products.filter(p => p.category === product.category && p.id !== product.id).slice(0, 4);

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm mb-6 flex-wrap" style={{ color: textSecondary }}>
          <Link to="/home" style={{ color: '#FBBF24' }} className="hover:opacity-70">Home</Link>
          <ChevronRight size={14} />
          <Link to="/components" style={{ color: '#FBBF24' }} className="hover:opacity-70">Components</Link>
          <ChevronRight size={14} />
          <span>{product.category}</span>
          <ChevronRight size={14} />
          <span>{product.name}</span>
        </div>

        {/* Main section */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 mb-12">
          {/* Left - images */}
          <div className="lg:col-span-3">
            <div
              className="relative rounded-lg overflow-hidden mb-3 group cursor-zoom-in"
              style={{ border: `1px solid ${border}`, height: '420px' }}
            >
              <ImageWithFallback src={images[activeImg]} alt={product.name} className="w-full h-full object-cover" />
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity" style={{ background: 'rgba(0,0,0,0.1)' }}>
                <ZoomIn size={32} style={{ color: '#FFFFFF' }} />
              </div>
            </div>
            {/* Thumbnails */}
            <div className="flex gap-2">
              {images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setActiveImg(i)}
                  className="rounded overflow-hidden flex-shrink-0"
                  style={{
                    width: 70, height: 70,
                    border: `2px solid ${i === activeImg ? '#FBBF24' : border}`,
                  }}
                >
                  <img src={img} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          </div>

          {/* Right - product info */}
          <div className="lg:col-span-2">
            <p className="text-xs font-medium mb-1" style={{ color: textSecondary }}>{product.manufacturer}</p>
            <h1 style={{ fontSize: '26px', fontWeight: 700, color: textPrimary, marginBottom: 10 }}>{product.name}</h1>

            {/* Rating */}
            <div className="flex items-center gap-2 mb-4">
              <div className="flex">
                {[1,2,3,4,5].map(s => (
                  <Star key={s} size={16} fill={s <= Math.round(product.rating) ? '#FBBF24' : 'none'} style={{ color: '#FBBF24' }} />
                ))}
              </div>
              <span className="text-sm" style={{ color: textSecondary }}>({product.reviews} reviews)</span>
            </div>

            <p style={{ fontSize: '32px', fontWeight: 700, color: textPrimary, marginBottom: 8 }}>
              ${product.price.toFixed(2)}
            </p>

            {/* Stock */}
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full" style={{ background: product.stock > 0 ? '#10B981' : '#EF4444' }} />
              <span className="text-sm" style={{ color: product.stock > 0 ? '#10B981' : '#EF4444' }}>
                {product.stock > 0 ? `In Stock (${product.stock} available)` : 'Out of Stock'}
              </span>
            </div>

            <p className="text-sm leading-relaxed mb-4" style={{ color: textSecondary }}>{product.description}</p>

            {/* Specs table */}
            <div className="rounded-lg overflow-hidden mb-4" style={{ border: `1px solid ${border}` }}>
              {product.specs.map((spec, i) => (
                <div
                  key={i}
                  className="flex text-sm"
                  style={{ borderBottom: i < product.specs.length - 1 ? `1px solid ${border}` : 'none' }}
                >
                  <div className="w-1/3 px-3 py-2 font-medium" style={{ background: isDark ? '#111827' : '#F9FAFB', color: textSecondary }}>
                    Spec {i + 1}
                  </div>
                  <div className="flex-1 px-3 py-2" style={{ color: textPrimary }}>{spec}</div>
                </div>
              ))}
            </div>

            {/* Compatibility note */}
            <div
              className="rounded-lg px-4 py-3 mb-4 text-sm"
              style={{ background: isDark ? '#111827' : '#F9FAFB', border: `1px solid ${border}` }}
            >
              <p style={{ color: textSecondary }}>
                Check compatibility with your build.{' '}
                <Link to="/configurator" style={{ color: '#FBBF24' }} className="hover:opacity-70">Open Configurator →</Link>
              </p>
            </div>

            {/* Quantity */}
            <div className="flex items-center gap-3 mb-4">
              <span className="text-sm font-medium" style={{ color: textSecondary }}>Qty:</span>
              <div className="flex items-center" style={{ border: `1px solid ${border}`, borderRadius: '6px' }}>
                <button
                  onClick={() => setQuantity(q => Math.max(1, q - 1))}
                  className="px-3 py-2 hover:opacity-70 transition-opacity"
                  style={{ color: textPrimary }}
                >
                  <Minus size={14} />
                </button>
                <span className="px-4 py-2 font-medium text-sm" style={{ color: textPrimary, borderLeft: `1px solid ${border}`, borderRight: `1px solid ${border}` }}>
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(q => q + 1)}
                  className="px-3 py-2 hover:opacity-70 transition-opacity"
                  style={{ color: textPrimary }}
                >
                  <Plus size={14} />
                </button>
              </div>
            </div>

            {/* Actions */}
            <div className="space-y-2">
              <button
                onClick={() => addToCart({ id: product.id, name: product.name, price: product.price, image: product.image, category: product.category })}
                className="w-full py-3 rounded-lg font-medium transition-opacity hover:opacity-90"
                style={{ background: '#FBBF24', color: '#111827', fontSize: '15px' }}
              >
                Add to Cart
              </button>
              <button
                onClick={() => toggleWishlist(product.id)}
                className="w-full py-3 rounded-lg font-medium transition-opacity hover:opacity-90 flex items-center justify-center gap-2"
                style={{ border: `1px solid #FBBF24`, color: '#FBBF24', background: 'transparent', fontSize: '15px' }}
              >
                <Heart size={16} fill={inWishlist ? '#FBBF24' : 'none'} />
                {inWishlist ? 'Remove from Wishlist' : 'Add to Wishlist'}
              </button>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ borderBottom: `1px solid ${border}` }} className="flex gap-6 mb-6">
          {(['description', 'specs', 'reviews'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className="pb-3 text-sm font-medium capitalize transition-colors"
              style={{
                color: activeTab === tab ? textPrimary : textSecondary,
                borderBottom: activeTab === tab ? '2px solid #FBBF24' : '2px solid transparent',
                marginBottom: '-1px',
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {activeTab === 'description' && (
          <div className="max-w-2xl">
            <p className="text-sm leading-relaxed mb-4" style={{ color: textSecondary }}>{product.description}</p>
            <ul className="space-y-2">
              {product.specs.map((spec, i) => (
                <li key={i} className="flex items-start gap-2 text-sm" style={{ color: textSecondary }}>
                  <span style={{ color: '#FBBF24', marginTop: '2px' }}>•</span> {spec}
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'specs' && (
          <div className="max-w-lg">
            <div className="rounded-lg overflow-hidden" style={{ border: `1px solid ${border}` }}>
              {product.specs.map((spec, i) => (
                <div key={i} className="flex text-sm" style={{ borderBottom: i < product.specs.length - 1 ? `1px solid ${border}` : 'none' }}>
                  <div className="w-2/5 px-4 py-3 font-medium" style={{ background: isDark ? '#111827' : '#F9FAFB', color: textSecondary }}>
                    Specification {i + 1}
                  </div>
                  <div className="flex-1 px-4 py-3" style={{ color: textPrimary }}>{spec}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'reviews' && (
          <div>
            <div className="flex flex-col sm:flex-row gap-8 mb-8">
              {/* Rating summary */}
              <div className="flex flex-col items-center justify-center p-6 rounded-lg flex-shrink-0" style={{ border: `1px solid ${border}`, background: cardBg }}>
                <span style={{ fontSize: '48px', fontWeight: 700, color: textPrimary }}>{product.rating}</span>
                <div className="flex mb-1">
                  {[1,2,3,4,5].map(s => (
                    <Star key={s} size={18} fill={s <= Math.round(product.rating) ? '#FBBF24' : 'none'} style={{ color: '#FBBF24' }} />
                  ))}
                </div>
                <p className="text-xs" style={{ color: textSecondary }}>Based on {product.reviews} reviews</p>
              </div>
              {/* Distribution bars */}
              <div className="flex-1">
                {[5,4,3,2,1].map(stars => {
                  const pct = stars === 5 ? 65 : stars === 4 ? 20 : stars === 3 ? 10 : stars === 2 ? 3 : 2;
                  return (
                    <div key={stars} className="flex items-center gap-3 mb-2">
                      <span className="text-xs w-3" style={{ color: textSecondary }}>{stars}</span>
                      <Star size={12} fill="#FBBF24" style={{ color: '#FBBF24', flexShrink: 0 }} />
                      <div className="flex-1 h-2 rounded-full" style={{ background: isDark ? '#374151' : '#E5E7EB' }}>
                        <div className="h-2 rounded-full" style={{ width: `${pct}%`, background: '#FBBF24' }} />
                      </div>
                      <span className="text-xs w-8" style={{ color: textSecondary }}>{pct}%</span>
                    </div>
                  );
                })}
              </div>
              <button
                className="self-start px-4 py-2 rounded text-sm font-medium transition-opacity hover:opacity-90"
                style={{ background: '#FBBF24', color: '#111827' }}
              >
                Write a Review
              </button>
            </div>

            <div className="space-y-4">
              {sampleReviews.map(review => (
                <div key={review.id} className="p-4 rounded-lg" style={{ border: `1px solid ${border}`, background: cardBg }}>
                  <div className="flex items-start gap-3">
                    <div className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0" style={{ background: '#FBBF24', color: '#111827' }}>
                      {review.avatar}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium" style={{ color: textPrimary }}>{review.user}</span>
                        <span className="text-xs" style={{ color: textSecondary }}>{review.date}</span>
                      </div>
                      <div className="flex mb-2">
                        {[1,2,3,4,5].map(s => (
                          <Star key={s} size={13} fill={s <= review.rating ? '#FBBF24' : 'none'} style={{ color: '#FBBF24' }} />
                        ))}
                      </div>
                      <p className="text-sm leading-relaxed" style={{ color: textSecondary }}>{review.comment}</p>
                      <div className="flex gap-3 mt-2 text-xs" style={{ color: textSecondary }}>
                        <button className="hover:opacity-70">Helpful? Yes</button>
                        <span>|</span>
                        <button className="hover:opacity-70">No</button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Related products */}
        {relatedProducts.length > 0 && (
          <div className="mt-12">
            <h2 className="mb-5" style={{ fontSize: '22px', fontWeight: 600, color: textPrimary }}>You May Also Like</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {relatedProducts.map(p => (
                <Link key={p.id} to={`/components/${p.id}`} className="block rounded-lg overflow-hidden transition-shadow" style={{ border: `1px solid ${border}`, background: cardBg }}
                  onMouseEnter={e => (e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)')}
                  onMouseLeave={e => (e.currentTarget.style.boxShadow = 'none')}
                >
                  <ImageWithFallback src={p.image} alt={p.name} className="w-full object-cover" style={{ height: '150px' }} />
                  <div className="p-3">
                    <p className="text-sm font-medium mb-1 line-clamp-2" style={{ color: textPrimary }}>{p.name}</p>
                    <p className="font-bold" style={{ color: textPrimary }}>${p.price.toFixed(2)}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

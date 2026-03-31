import { Link, useNavigate } from 'react-router';
import { Minus, Plus, X, ShoppingBag, ChevronRight, Tag } from 'lucide-react';
import { useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

export function CartPage() {
  const { isDark } = useTheme();
  const { items, removeFromCart, addToCart } = useCart();
  const navigate = useNavigate();
  const [promoOpen, setPromoOpen] = useState(false);
  const [promoCode, setPromoCode] = useState('');
  const [promoStatus, setPromoStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const secondaryBg = isDark ? '#1F2937' : '#F9FAFB';

  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = subtotal > 500 ? 0 : 29.99;
  const tax = subtotal * 0.1;
  const total = subtotal + shipping + tax;
  const discount = promoStatus === 'success' ? subtotal * 0.05 : 0;
  const finalTotal = total - discount;

  const applyPromo = () => {
    if (promoCode.toUpperCase() === 'BUILDBOX10') {
      setPromoStatus('success');
    } else {
      setPromoStatus('error');
    }
  };

  const updateQuantity = (id: string, delta: number, item: typeof items[0]) => {
    if (delta > 0) {
      addToCart({ id: item.id, name: item.name, price: item.price, image: item.image, category: item.category });
    } else {
      if (item.quantity <= 1) {
        removeFromCart(id);
      } else {
        // We need to decrease — in our simple context, remove and re-add quantity-1 times
        removeFromCart(id);
        for (let i = 0; i < item.quantity - 1; i++) {
          addToCart({ id: item.id, name: item.name, price: item.price, image: item.image, category: item.category });
        }
      }
    }
  };

  if (items.length === 0) {
    return (
      <div style={{ background: sectionBg }} className="min-h-screen">
        <div className="max-w-7xl mx-auto px-6 py-16 text-center">
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6"
            style={{ background: isDark ? '#1F2937' : '#F3F4F6' }}
          >
            <ShoppingBag size={36} style={{ color: '#9CA3AF' }} />
          </div>
          <h1 className="mb-3" style={{ fontSize: '28px', fontWeight: 700, color: textPrimary }}>Your cart is empty</h1>
          <p className="mb-8" style={{ color: textSecondary }}>Add some components or build a custom PC to get started.</p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              to="/components"
              className="px-6 py-3 rounded-lg text-sm font-medium transition-opacity hover:opacity-90"
              style={{ background: '#FBBF24', color: '#111827' }}
            >
              Browse Components
            </Link>
            <Link
              to="/configurator"
              className="px-6 py-3 rounded-lg text-sm font-medium transition-opacity hover:opacity-80"
              style={{ border: `1px solid #FBBF24`, color: '#FBBF24', background: 'transparent' }}
            >
              Build a PC
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm mb-6" style={{ color: textSecondary }}>
          <Link to="/home" className="hover:opacity-70" style={{ color: '#FBBF24' }}>Home</Link>
          <ChevronRight size={14} />
          <span>Cart</span>
        </div>

        <h1 className="mb-8" style={{ fontSize: '32px', fontWeight: 700, color: textPrimary, letterSpacing: '-0.01em' }}>
          Shopping Cart <span className="text-base font-normal" style={{ color: textSecondary }}>({items.reduce((s, i) => s + i.quantity, 0)} items)</span>
        </h1>

        <div className="flex flex-col lg:flex-row gap-6">
          {/* Cart items */}
          <div className="flex-1 space-y-4">
            {items.map(item => (
              <div
                key={item.id}
                className="rounded-lg p-4 flex gap-4"
                style={{ background: cardBg, border: `1px solid ${border}`, boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }}
              >
                {/* Image */}
                <div className="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                  <ImageWithFallback src={item.image} alt={item.name} className="w-full h-full object-cover" />
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="text-xs font-medium mb-0.5" style={{ color: '#FBBF24' }}>{item.category}</p>
                      <h4 className="text-sm font-semibold" style={{ color: textPrimary }}>{item.name}</h4>
                    </div>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="hover:opacity-60 transition-opacity flex-shrink-0"
                      style={{ color: textSecondary }}
                    >
                      <X size={18} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between mt-3">
                    {/* Quantity */}
                    <div
                      className="flex items-center rounded-lg overflow-hidden"
                      style={{ border: `1px solid ${border}` }}
                    >
                      <button
                        onClick={() => updateQuantity(item.id, -1, item)}
                        className="px-3 py-1.5 hover:opacity-70 transition-opacity"
                        style={{ color: textSecondary, background: secondaryBg }}
                      >
                        <Minus size={14} />
                      </button>
                      <span
                        className="px-4 py-1.5 text-sm font-medium"
                        style={{ color: textPrimary, background: cardBg, minWidth: '40px', textAlign: 'center' }}
                      >
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(item.id, 1, item)}
                        className="px-3 py-1.5 hover:opacity-70 transition-opacity"
                        style={{ color: textSecondary, background: secondaryBg }}
                      >
                        <Plus size={14} />
                      </button>
                    </div>

                    {/* Price */}
                    <div className="text-right">
                      <p className="text-sm" style={{ color: textSecondary }}>${item.price.toFixed(2)} each</p>
                      <p className="font-bold" style={{ color: textPrimary, fontSize: '18px' }}>
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Continue shopping */}
            <Link
              to="/components"
              className="flex items-center gap-2 text-sm hover:opacity-70 transition-opacity"
              style={{ color: '#FBBF24' }}
            >
              ← Continue Shopping
            </Link>
          </div>

          {/* Order summary */}
          <div className="lg:w-[340px]">
            <div className="rounded-lg p-5 sticky top-24" style={{ background: cardBg, border: `1px solid ${border}` }}>
              <h2 className="font-semibold mb-5" style={{ color: textPrimary, fontSize: '18px' }}>Order Summary</h2>

              <div className="space-y-3 mb-4">
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Subtotal</span>
                  <span style={{ color: textPrimary }}>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Shipping</span>
                  <span style={{ color: shipping === 0 ? '#10B981' : textPrimary }}>
                    {shipping === 0 ? 'Free' : `$${shipping.toFixed(2)}`}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Tax (10%)</span>
                  <span style={{ color: textPrimary }}>${tax.toFixed(2)}</span>
                </div>
                {promoStatus === 'success' && (
                  <div className="flex justify-between text-sm">
                    <span style={{ color: '#10B981' }}>Promo discount (5%)</span>
                    <span style={{ color: '#10B981' }}>-${discount.toFixed(2)}</span>
                  </div>
                )}
              </div>

              {shipping > 0 && (
                <div
                  className="text-xs p-2.5 rounded-lg mb-4"
                  style={{ background: isDark ? '#374151' : '#FFFBEB', color: '#92400E' }}
                >
                  Add ${(500 - subtotal).toFixed(2)} more for free shipping
                </div>
              )}

              <div className="pt-3 mb-5 border-t" style={{ borderColor: border }}>
                <div className="flex justify-between">
                  <span className="font-semibold" style={{ color: textPrimary }}>Total</span>
                  <span style={{ fontSize: '22px', fontWeight: 700, color: textPrimary }}>${finalTotal.toFixed(2)}</span>
                </div>
              </div>

              {/* Promo code */}
              <div className="mb-4">
                <button
                  onClick={() => setPromoOpen(!promoOpen)}
                  className="flex items-center gap-2 text-sm hover:opacity-70 transition-opacity"
                  style={{ color: '#FBBF24' }}
                >
                  <Tag size={14} />
                  Have a promo code?
                </button>
                {promoOpen && (
                  <div className="mt-3 flex gap-2">
                    <input
                      type="text"
                      value={promoCode}
                      onChange={e => { setPromoCode(e.target.value); setPromoStatus('idle'); }}
                      placeholder="Enter code"
                      style={{
                        flex: 1,
                        padding: '8px 12px',
                        border: `1px solid ${promoStatus === 'error' ? '#EF4444' : promoStatus === 'success' ? '#10B981' : border}`,
                        borderRadius: '6px',
                        background: isDark ? '#111827' : '#F9FAFB',
                        color: textPrimary,
                        fontSize: '13px',
                        outline: 'none',
                      }}
                    />
                    <button
                      onClick={applyPromo}
                      className="px-3 py-2 rounded-lg text-sm font-medium transition-opacity hover:opacity-90"
                      style={{ background: '#FBBF24', color: '#111827' }}
                    >
                      Apply
                    </button>
                  </div>
                )}
                {promoStatus === 'success' && (
                  <p className="text-xs mt-1" style={{ color: '#10B981' }}>✓ Promo code applied! 5% discount</p>
                )}
                {promoStatus === 'error' && (
                  <p className="text-xs mt-1" style={{ color: '#EF4444' }}>✗ Invalid promo code. Try BUILDBOX10</p>
                )}
              </div>

              <button
                onClick={() => navigate('/checkout')}
                className="w-full py-3 rounded-lg text-sm font-medium transition-opacity hover:opacity-90"
                style={{ background: '#FBBF24', color: '#111827' }}
              >
                Proceed to Checkout
              </button>
              <Link
                to="/components"
                className="block text-center text-sm mt-3 hover:opacity-70 transition-opacity"
                style={{ color: '#FBBF24' }}
              >
                Continue Shopping
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

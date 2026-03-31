import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Check, ChevronRight, CreditCard, Truck, ClipboardList, Eye, EyeOff } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

type Step = 1 | 2 | 3;

interface ShippingForm {
  fullName: string;
  email: string;
  phone: string;
  address1: string;
  address2: string;
  city: string;
  state: string;
  zip: string;
  country: string;
  saveAddress: boolean;
}

interface PaymentForm {
  method: 'card' | 'paypal' | 'apple' | 'google';
  cardNumber: string;
  cardName: string;
  expiry: string;
  cvv: string;
  saveCard: boolean;
}

const US_STATES = ['Alabama', 'Alaska', 'Arizona', 'California', 'Colorado', 'Florida', 'Georgia', 'New York', 'Texas', 'Washington'];
const COUNTRIES = ['United States', 'Canada', 'United Kingdom', 'Australia'];

export function CheckoutPage() {
  const { isDark } = useTheme();
  const { items } = useCart();
  const navigate = useNavigate();
  const [step, setStep] = useState<Step>(1);
  const [showCvv, setShowCvv] = useState(false);
  const [orderNote, setOrderNote] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const [shipping, setShipping] = useState<ShippingForm>({
    fullName: '', email: '', phone: '', address1: '', address2: '',
    city: '', state: '', zip: '', country: 'United States', saveAddress: false,
  });

  const [payment, setPayment] = useState<PaymentForm>({
    method: 'card', cardNumber: '', cardName: '', expiry: '', cvv: '', saveCard: false,
  });

  const textPrimary = isDark ? '#F9FAFB' : '#111827';
  const textSecondary = '#6B7280';
  const border = isDark ? '#374151' : '#E5E7EB';
  const cardBg = isDark ? '#1F2937' : '#FFFFFF';
  const sectionBg = isDark ? '#111827' : '#FFFFFF';
  const inputBg = isDark ? '#111827' : '#FFFFFF';

  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shippingCost = subtotal > 500 ? 0 : 29.99;
  const tax = subtotal * 0.1;
  const total = subtotal + shippingCost + tax;

  const inputStyle = {
    width: '100%',
    padding: '10px 14px',
    border: `1px solid ${border}`,
    borderRadius: '6px',
    background: inputBg,
    color: textPrimary,
    fontSize: '14px',
    outline: 'none',
  };

  const labelStyle = {
    display: 'block',
    fontSize: '13px',
    fontWeight: 500,
    color: textSecondary,
    marginBottom: '6px',
  };

  const handlePlaceOrder = () => {
    if (!agreed) return;
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      navigate('/home');
    }, 2000);
  };

  const steps = [
    { num: 1, label: 'Shipping', Icon: Truck },
    { num: 2, label: 'Payment', Icon: CreditCard },
    { num: 3, label: 'Review', Icon: ClipboardList },
  ];

  return (
    <div style={{ background: sectionBg }} className="min-h-screen">
      {/* Processing overlay */}
      {isProcessing && (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center" style={{ background: 'rgba(0,0,0,0.6)' }}>
          <div className="w-12 h-12 rounded-full border-4 border-t-transparent animate-spin mb-4" style={{ borderColor: '#FBBF24', borderTopColor: 'transparent' }} />
          <p className="text-white font-medium">Processing your order...</p>
        </div>
      )}

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm mb-6" style={{ color: textSecondary }}>
          <Link to="/home" className="hover:opacity-70" style={{ color: '#FBBF24' }}>Home</Link>
          <ChevronRight size={14} />
          <Link to="/cart" className="hover:opacity-70" style={{ color: '#FBBF24' }}>Cart</Link>
          <ChevronRight size={14} />
          <span>Checkout</span>
        </div>

        <h1 className="mb-8" style={{ fontSize: '28px', fontWeight: 700, color: textPrimary, letterSpacing: '-0.01em' }}>
          Checkout
        </h1>

        {/* Step indicator */}
        <div className="flex items-center mb-10">
          {steps.map((s, i) => (
            <div key={s.num} className="flex items-center flex-1 last:flex-none">
              <div className="flex flex-col items-center">
                <div
                  className="w-9 h-9 rounded-full flex items-center justify-center transition-all"
                  style={{
                    background: step > s.num ? '#10B981' : step === s.num ? '#FBBF24' : (isDark ? '#374151' : '#E5E7EB'),
                    color: step >= s.num ? '#111827' : '#9CA3AF',
                  }}
                >
                  {step > s.num ? <Check size={16} style={{ color: '#FFFFFF' }} /> : <s.Icon size={16} />}
                </div>
                <span className="text-xs mt-1 font-medium" style={{ color: step >= s.num ? textPrimary : textSecondary }}>
                  {s.label}
                </span>
              </div>
              {i < steps.length - 1 && (
                <div
                  className="flex-1 h-px mx-3 mb-5"
                  style={{ background: step > s.num ? '#10B981' : (isDark ? '#374151' : '#E5E7EB') }}
                />
              )}
            </div>
          ))}
        </div>

        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left: Form */}
          <div className="flex-1">
            <div className="rounded-lg p-6" style={{ background: cardBg, border: `1px solid ${border}` }}>
              {/* STEP 1: Shipping */}
              {step === 1 && (
                <div>
                  <h2 className="mb-5" style={{ fontSize: '20px', fontWeight: 600, color: textPrimary }}>
                    Shipping Information
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="sm:col-span-2">
                      <label style={labelStyle}>Full Name *</label>
                      <input
                        type="text"
                        value={shipping.fullName}
                        onChange={e => setShipping({ ...shipping, fullName: e.target.value })}
                        placeholder="John Doe"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div>
                      <label style={labelStyle}>Email *</label>
                      <input
                        type="email"
                        value={shipping.email}
                        onChange={e => setShipping({ ...shipping, email: e.target.value })}
                        placeholder="john@example.com"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div>
                      <label style={labelStyle}>Phone</label>
                      <input
                        type="tel"
                        value={shipping.phone}
                        onChange={e => setShipping({ ...shipping, phone: e.target.value })}
                        placeholder="+1 (555) 000-0000"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div className="sm:col-span-2">
                      <label style={labelStyle}>Address Line 1 *</label>
                      <input
                        type="text"
                        value={shipping.address1}
                        onChange={e => setShipping({ ...shipping, address1: e.target.value })}
                        placeholder="123 Main Street"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div className="sm:col-span-2">
                      <label style={labelStyle}>Address Line 2 <span style={{ fontWeight: 400 }}>(optional)</span></label>
                      <input
                        type="text"
                        value={shipping.address2}
                        onChange={e => setShipping({ ...shipping, address2: e.target.value })}
                        placeholder="Apt, suite, unit..."
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div>
                      <label style={labelStyle}>City *</label>
                      <input
                        type="text"
                        value={shipping.city}
                        onChange={e => setShipping({ ...shipping, city: e.target.value })}
                        placeholder="San Francisco"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div>
                      <label style={labelStyle}>State</label>
                      <select
                        value={shipping.state}
                        onChange={e => setShipping({ ...shipping, state: e.target.value })}
                        style={{ ...inputStyle }}
                      >
                        <option value="">Select state</option>
                        {US_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                      </select>
                    </div>
                    <div>
                      <label style={labelStyle}>ZIP Code *</label>
                      <input
                        type="text"
                        value={shipping.zip}
                        onChange={e => setShipping({ ...shipping, zip: e.target.value })}
                        placeholder="94102"
                        style={inputStyle}
                        onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                        onBlur={e => (e.target.style.borderColor = border)}
                      />
                    </div>
                    <div>
                      <label style={labelStyle}>Country *</label>
                      <select
                        value={shipping.country}
                        onChange={e => setShipping({ ...shipping, country: e.target.value })}
                        style={{ ...inputStyle }}
                      >
                        {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
                      </select>
                    </div>
                    <div className="sm:col-span-2">
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={shipping.saveAddress}
                          onChange={e => setShipping({ ...shipping, saveAddress: e.target.checked })}
                          style={{ accentColor: '#FBBF24', width: '16px', height: '16px' }}
                        />
                        <span className="text-sm" style={{ color: textSecondary }}>Save address for future orders</span>
                      </label>
                    </div>
                  </div>
                  <div className="flex justify-end mt-6">
                    <button
                      onClick={() => setStep(2)}
                      className="px-8 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-90"
                      style={{ background: '#FBBF24', color: '#111827' }}
                    >
                      Continue to Payment →
                    </button>
                  </div>
                </div>
              )}

              {/* STEP 2: Payment */}
              {step === 2 && (
                <div>
                  <h2 className="mb-5" style={{ fontSize: '20px', fontWeight: 600, color: textPrimary }}>
                    Payment Method
                  </h2>

                  {/* Payment options */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
                    {[
                      { key: 'card', label: 'Credit/Debit Card' },
                      { key: 'paypal', label: 'PayPal' },
                      { key: 'apple', label: 'Apple Pay' },
                      { key: 'google', label: 'Google Pay' },
                    ].map(opt => (
                      <label
                        key={opt.key}
                        className="flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-all"
                        style={{
                          border: `1px solid ${payment.method === opt.key ? '#FBBF24' : border}`,
                          background: payment.method === opt.key ? (isDark ? '#2D3748' : '#FFFBEB') : 'transparent',
                        }}
                      >
                        <input
                          type="radio"
                          name="payment"
                          checked={payment.method === opt.key as PaymentForm['method']}
                          onChange={() => setPayment({ ...payment, method: opt.key as PaymentForm['method'] })}
                          style={{ accentColor: '#FBBF24' }}
                        />
                        <span className="text-xs font-medium" style={{ color: textPrimary }}>{opt.label}</span>
                      </label>
                    ))}
                  </div>

                  {/* Card form */}
                  {payment.method === 'card' && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div className="sm:col-span-2">
                        <label style={labelStyle}>Card Number</label>
                        <div className="relative">
                          <input
                            type="text"
                            value={payment.cardNumber}
                            onChange={e => setPayment({ ...payment, cardNumber: e.target.value })}
                            placeholder="1234 5678 9012 3456"
                            maxLength={19}
                            style={{ ...inputStyle, paddingRight: '40px' }}
                            onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                            onBlur={e => (e.target.style.borderColor = border)}
                          />
                          <CreditCard size={16} className="absolute right-3 top-1/2 -translate-y-1/2" style={{ color: '#9CA3AF' }} />
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <label style={labelStyle}>Cardholder Name</label>
                        <input
                          type="text"
                          value={payment.cardName}
                          onChange={e => setPayment({ ...payment, cardName: e.target.value })}
                          placeholder="John Doe"
                          style={inputStyle}
                          onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                          onBlur={e => (e.target.style.borderColor = border)}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>Expiration (MM/YY)</label>
                        <input
                          type="text"
                          value={payment.expiry}
                          onChange={e => setPayment({ ...payment, expiry: e.target.value })}
                          placeholder="MM/YY"
                          maxLength={5}
                          style={inputStyle}
                          onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                          onBlur={e => (e.target.style.borderColor = border)}
                        />
                      </div>
                      <div>
                        <label style={labelStyle}>CVV</label>
                        <div className="relative">
                          <input
                            type={showCvv ? 'text' : 'password'}
                            value={payment.cvv}
                            onChange={e => setPayment({ ...payment, cvv: e.target.value })}
                            placeholder="123"
                            maxLength={4}
                            style={{ ...inputStyle, paddingRight: '40px' }}
                            onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                            onBlur={e => (e.target.style.borderColor = border)}
                          />
                          <button
                            type="button"
                            onClick={() => setShowCvv(!showCvv)}
                            className="absolute right-3 top-1/2 -translate-y-1/2 hover:opacity-60"
                            style={{ color: '#9CA3AF' }}
                          >
                            {showCvv ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>
                      <div className="sm:col-span-2">
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={payment.saveCard}
                            onChange={e => setPayment({ ...payment, saveCard: e.target.checked })}
                            style={{ accentColor: '#FBBF24', width: '16px', height: '16px' }}
                          />
                          <span className="text-sm" style={{ color: textSecondary }}>Save card for future purchases</span>
                        </label>
                      </div>
                    </div>
                  )}

                  {payment.method !== 'card' && (
                    <div className="text-center py-8" style={{ color: textSecondary }}>
                      <p className="text-sm">You'll be redirected to {payment.method === 'paypal' ? 'PayPal' : payment.method === 'apple' ? 'Apple Pay' : 'Google Pay'} to complete payment.</p>
                    </div>
                  )}

                  <div className="flex items-center justify-between mt-6">
                    <button
                      onClick={() => setStep(1)}
                      className="px-6 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-80"
                      style={{ border: `1px solid ${border}`, color: textPrimary, background: 'transparent' }}
                    >
                      ← Back
                    </button>
                    <button
                      onClick={() => setStep(3)}
                      className="px-8 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-90"
                      style={{ background: '#FBBF24', color: '#111827' }}
                    >
                      Continue →
                    </button>
                  </div>
                </div>
              )}

              {/* STEP 3: Review */}
              {step === 3 && (
                <div>
                  <h2 className="mb-5" style={{ fontSize: '20px', fontWeight: 600, color: textPrimary }}>
                    Review Your Order
                  </h2>

                  {/* Shipping review */}
                  <div className="rounded-lg p-4 mb-4" style={{ background: isDark ? '#374151' : '#F9FAFB', border: `1px solid ${border}` }}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-sm font-semibold" style={{ color: textPrimary }}>Shipping Address</h4>
                      <button onClick={() => setStep(1)} className="text-xs hover:opacity-70" style={{ color: '#FBBF24' }}>Edit</button>
                    </div>
                    <p className="text-sm" style={{ color: textSecondary }}>
                      {shipping.fullName || 'Not provided'}<br />
                      {shipping.address1 && `${shipping.address1}, `}{shipping.city && `${shipping.city}, `}{shipping.state && `${shipping.state} `}{shipping.zip}<br />
                      {shipping.country}
                    </p>
                  </div>

                  {/* Payment review */}
                  <div className="rounded-lg p-4 mb-4" style={{ background: isDark ? '#374151' : '#F9FAFB', border: `1px solid ${border}` }}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-sm font-semibold" style={{ color: textPrimary }}>Payment Method</h4>
                      <button onClick={() => setStep(2)} className="text-xs hover:opacity-70" style={{ color: '#FBBF24' }}>Edit</button>
                    </div>
                    <p className="text-sm" style={{ color: textSecondary }}>
                      {payment.method === 'card'
                        ? `Credit Card ending in ${payment.cardNumber.slice(-4) || 'XXXX'}`
                        : payment.method === 'paypal' ? 'PayPal'
                        : payment.method === 'apple' ? 'Apple Pay'
                        : 'Google Pay'}
                    </p>
                  </div>

                  {/* Items review */}
                  <div className="rounded-lg p-4 mb-4" style={{ background: isDark ? '#374151' : '#F9FAFB', border: `1px solid ${border}` }}>
                    <h4 className="text-sm font-semibold mb-3" style={{ color: textPrimary }}>Order Items ({items.length})</h4>
                    <div className="space-y-2">
                      {items.map(item => (
                        <div key={item.id} className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded overflow-hidden flex-shrink-0">
                            <ImageWithFallback src={item.image} alt={item.name} className="w-full h-full object-cover" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-xs font-medium truncate" style={{ color: textPrimary }}>{item.name}</p>
                            <p className="text-xs" style={{ color: textSecondary }}>Qty: {item.quantity}</p>
                          </div>
                          <span className="text-sm font-semibold flex-shrink-0" style={{ color: textPrimary }}>
                            ${(item.price * item.quantity).toFixed(2)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Order note */}
                  <div className="mb-4">
                    <label style={labelStyle}>Order Notes (optional)</label>
                    <textarea
                      value={orderNote}
                      onChange={e => setOrderNote(e.target.value)}
                      placeholder="Special instructions for your order..."
                      rows={3}
                      style={{
                        width: '100%',
                        padding: '10px 14px',
                        border: `1px solid ${border}`,
                        borderRadius: '6px',
                        background: inputBg,
                        color: textPrimary,
                        fontSize: '14px',
                        outline: 'none',
                        resize: 'vertical',
                      }}
                      onFocus={e => (e.target.style.borderColor = '#FBBF24')}
                      onBlur={e => (e.target.style.borderColor = border)}
                    />
                  </div>

                  {/* Terms */}
                  <label className="flex items-start gap-2 mb-6 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={agreed}
                      onChange={e => setAgreed(e.target.checked)}
                      style={{ accentColor: '#FBBF24', width: '16px', height: '16px', marginTop: '2px', flexShrink: 0 }}
                    />
                    <span className="text-sm" style={{ color: textSecondary }}>
                      I agree to the{' '}
                      <a href="#" style={{ color: '#FBBF24' }} className="hover:opacity-70">Terms of Service</a>
                      {' '}and{' '}
                      <a href="#" style={{ color: '#FBBF24' }} className="hover:opacity-70">Privacy Policy</a>
                    </span>
                  </label>

                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => setStep(2)}
                      className="px-6 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-80"
                      style={{ border: `1px solid ${border}`, color: textPrimary, background: 'transparent' }}
                    >
                      ← Back
                    </button>
                    <button
                      onClick={handlePlaceOrder}
                      disabled={!agreed}
                      className="px-8 py-2.5 rounded-lg text-sm font-medium transition-opacity hover:opacity-90 disabled:opacity-40"
                      style={{ background: '#FBBF24', color: '#111827' }}
                    >
                      Place Order — ${total.toFixed(2)}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right: Order summary */}
          <div className="lg:w-[300px]">
            <div className="rounded-lg p-5 sticky top-24" style={{ background: cardBg, border: `1px solid ${border}` }}>
              <h3 className="font-semibold mb-4" style={{ color: textPrimary }}>Order Summary</h3>

              {/* Item list */}
              <div className="space-y-3 mb-4 pb-4 border-b" style={{ borderColor: border }}>
                {items.map(item => (
                  <div key={item.id} className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded overflow-hidden flex-shrink-0 relative">
                      <ImageWithFallback src={item.image} alt={item.name} className="w-full h-full object-cover" />
                      <span
                        className="absolute -top-1 -right-1 w-4 h-4 rounded-full text-[9px] font-bold flex items-center justify-center"
                        style={{ background: '#FBBF24', color: '#111827' }}
                      >
                        {item.quantity}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs truncate" style={{ color: textPrimary }}>{item.name}</p>
                    </div>
                    <span className="text-xs font-semibold flex-shrink-0" style={{ color: textPrimary }}>
                      ${(item.price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>

              <div className="space-y-2 mb-4 pb-4 border-b" style={{ borderColor: border }}>
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Subtotal</span>
                  <span style={{ color: textPrimary }}>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Shipping</span>
                  <span style={{ color: shippingCost === 0 ? '#10B981' : textPrimary }}>
                    {shippingCost === 0 ? 'Free' : `$${shippingCost.toFixed(2)}`}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: textSecondary }}>Tax (10%)</span>
                  <span style={{ color: textPrimary }}>${tax.toFixed(2)}</span>
                </div>
              </div>

              <div className="flex justify-between">
                <span className="font-semibold" style={{ color: textPrimary }}>Total</span>
                <span style={{ fontSize: '20px', fontWeight: 700, color: textPrimary }}>${total.toFixed(2)}</span>
              </div>

              {/* Security badges */}
              <div className="mt-5 pt-4 border-t" style={{ borderColor: border }}>
                <p className="text-xs text-center mb-2" style={{ color: textSecondary }}>Secure checkout</p>
                <div className="flex justify-center gap-3">
                  {['SSL', '256-bit', 'PCI DSS'].map(badge => (
                    <span
                      key={badge}
                      className="px-2 py-1 rounded text-xs font-medium"
                      style={{ background: isDark ? '#374151' : '#F3F4F6', color: textSecondary }}
                    >
                      {badge}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

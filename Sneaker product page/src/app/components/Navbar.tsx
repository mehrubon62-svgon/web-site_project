import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import {
  Search, Sun, Moon, Heart, ShoppingBag, User, Menu, X, ChevronDown
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useCart } from '../context/CartContext';

export function Navbar() {
  const { isDark, toggleTheme } = useTheme();
  const { cartCount, wishlistCount } = useCart();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const navigate = useNavigate();

  const navLinks = [
    { label: 'Home', to: '/home' },
    { label: 'Components', to: '/components' },
    { label: 'Laptops', to: '/laptops' },
    { label: 'Configurator', to: '/configurator' },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/components?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <nav
      style={{
        background: isDark ? '#1F2937' : '#FFFFFF',
        borderBottom: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
      }}
      className="sticky top-0 z-50 w-full"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-[60px] gap-4">
          {/* Mobile hamburger */}
          <button
            className="sm:hidden flex items-center justify-center"
            onClick={() => setMobileOpen(!mobileOpen)}
            style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>

          {/* Logo */}
          <Link to="/home" className="flex-shrink-0 hover:opacity-80 transition-opacity">
            <span style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.01em' }}>
              <span style={{ color: '#FBBF24' }}>Build</span>
              <span style={{ color: isDark ? '#FFFFFF' : '#1F2937' }}>Box</span>
            </span>
          </Link>

          {/* Center search bar - desktop */}
          <form onSubmit={handleSearch} className="hidden sm:flex flex-1 max-w-[480px]">
            <div className="relative w-full">
              <Search
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2"
                style={{ color: isDark ? '#9CA3AF' : '#9CA3AF' }}
              />
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search products..."
                style={{
                  width: '100%',
                  paddingLeft: '36px',
                  paddingRight: '12px',
                  paddingTop: '8px',
                  paddingBottom: '8px',
                  border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                  borderRadius: '6px',
                  background: isDark ? '#111827' : '#FFFFFF',
                  color: isDark ? '#F9FAFB' : '#111827',
                  fontSize: '14px',
                  outline: 'none',
                }}
                onFocus={e => e.target.style.borderColor = '#FBBF24'}
                onBlur={e => e.target.style.borderColor = isDark ? '#374151' : '#E5E7EB'}
              />
            </div>
          </form>

          {/* Right icons */}
          <div className="flex items-center gap-5">
            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
              className="hover:opacity-70 transition-opacity"
            >
              {isDark ? <Sun size={20} /> : <Moon size={20} />}
            </button>

            {/* Wishlist */}
            <Link
              to="/wishlist"
              className="relative hover:opacity-70 transition-opacity hidden sm:block"
              style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
            >
              <Heart size={20} />
              {wishlistCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 flex items-center justify-center w-4 h-4 rounded-full text-[10px] font-medium"
                  style={{ background: '#FBBF24', color: '#111827' }}
                >
                  {wishlistCount}
                </span>
              )}
            </Link>

            {/* Cart */}
            <Link
              to="/cart"
              className="relative hover:opacity-70 transition-opacity"
              style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
            >
              <ShoppingBag size={20} />
              {cartCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 flex items-center justify-center w-4 h-4 rounded-full text-[10px] font-medium"
                  style={{ background: '#FBBF24', color: '#111827' }}
                >
                  {cartCount}
                </span>
              )}
            </Link>

            {/* User menu */}
            <div className="relative hidden sm:block">
              <button
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="flex items-center gap-1 hover:opacity-70 transition-opacity"
                style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
              >
                <User size={20} />
                <ChevronDown size={14} />
              </button>
              {userMenuOpen && (
                <div
                  className="absolute right-0 top-8 w-44 rounded-lg py-1 z-50"
                  style={{
                    background: isDark ? '#1F2937' : '#FFFFFF',
                    border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                  }}
                >
                  {[
                    { label: 'Sign In', to: '/' },
                    { label: 'Register', to: '/register' },
                    { label: 'My Configurations', to: '/configurations' },
                    { label: 'Order History', to: '/orders' },
                    { label: 'Change Password', to: '/change-password' },
                  ].map(item => (
                    <Link
                      key={item.to}
                      to={item.to}
                      onClick={() => setUserMenuOpen(false)}
                      className="block px-4 py-2 text-sm hover:opacity-70 transition-opacity"
                      style={{ color: isDark ? '#F9FAFB' : '#111827' }}
                    >
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Desktop nav links */}
        <div className="hidden sm:flex items-center gap-6 pb-2">
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className="text-sm hover:opacity-70 transition-opacity"
              style={{ color: isDark ? '#9CA3AF' : '#6B7280' }}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div
          className="sm:hidden border-t"
          style={{
            borderColor: isDark ? '#374151' : '#E5E7EB',
            background: isDark ? '#1F2937' : '#FFFFFF',
          }}
        >
          {/* Mobile search */}
          <form onSubmit={handleSearch} className="px-4 py-3">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: '#9CA3AF' }} />
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search products..."
                style={{
                  width: '100%',
                  paddingLeft: '36px',
                  paddingRight: '12px',
                  paddingTop: '8px',
                  paddingBottom: '8px',
                  border: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
                  borderRadius: '6px',
                  background: isDark ? '#111827' : '#FFFFFF',
                  color: isDark ? '#F9FAFB' : '#111827',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
            </div>
          </form>
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setMobileOpen(false)}
              className="block px-4 py-3 text-sm border-t"
              style={{
                color: isDark ? '#F9FAFB' : '#111827',
                borderColor: isDark ? '#374151' : '#E5E7EB',
              }}
            >
              {link.label}
            </Link>
          ))}
          <Link
            to="/"
            onClick={() => setMobileOpen(false)}
            className="block px-4 py-3 text-sm border-t"
            style={{
              color: '#FBBF24',
              borderColor: isDark ? '#374151' : '#E5E7EB',
            }}
          >
            Sign In / Register
          </Link>
        </div>
      )}
    </nav>
  );
}

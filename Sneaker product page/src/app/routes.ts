import { createBrowserRouter, redirect } from 'react-router';
import { AuthLayout } from './layouts/AuthLayout';
import { MainLayout } from './layouts/MainLayout';
import { LoginPage } from './pages/LoginPage';
import { RegistrationPage } from './pages/RegistrationPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { ResetPasswordPage } from './pages/ResetPasswordPage';
import { ChangePasswordPage } from './pages/ChangePasswordPage';
import { EmailSentPage } from './pages/EmailSentPage';
import { HomePage } from './pages/HomePage';
import { ComponentsCatalogPage } from './pages/ComponentsCatalogPage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { LaptopsCatalogPage } from './pages/LaptopsCatalogPage';
import { ConfiguratorPage } from './pages/ConfiguratorPage';
import { SavedConfigurationsPage } from './pages/SavedConfigurationsPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';

export const router = createBrowserRouter([
  {
    path: '/',
    Component: AuthLayout,
    children: [
      { index: true, Component: LoginPage },
      { path: 'register', Component: RegistrationPage },
      { path: 'forgot-password', Component: ForgotPasswordPage },
      { path: 'reset-password', Component: ResetPasswordPage },
      { path: 'change-password', Component: ChangePasswordPage },
      { path: 'email-sent', Component: EmailSentPage },
    ],
  },
  {
    path: '/',
    Component: MainLayout,
    children: [
      { path: 'home', Component: HomePage },
      { path: 'components', Component: ComponentsCatalogPage },
      { path: 'components/:id', Component: ProductDetailPage },
      { path: 'laptops', Component: LaptopsCatalogPage },
      { path: 'configurator', Component: ConfiguratorPage },
      { path: 'configurations', Component: SavedConfigurationsPage },
      { path: 'cart', Component: CartPage },
      { path: 'checkout', Component: CheckoutPage },
    ],
  },
  {
    path: '*',
    loader: () => redirect('/'),
  },
]);

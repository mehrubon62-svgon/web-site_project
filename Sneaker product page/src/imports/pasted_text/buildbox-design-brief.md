BuildBox - Complete PC Building E-Commerce Platform Design Brief
UPDATED VERSION - Minimalist Yellow Theme
Create a professional, minimalist Figma design system for BuildBox - a comprehensive e-commerce platform for building custom PCs, buying laptops, and individual PC components with AI consultation.

🎨 BRAND IDENTITY
Logo Design: Simple text-based logo: "BuildBox" in clean sans-serif font. "Build" in bright yellow #FBBF24 and "Box" in dark gray #1F2937 for light mode, white #FFFFFF for dark mode. Font weight: Bold (700). Size: 24px. No icon required - pure minimalist text logo.
Brand Personality: Minimalist, modern, clean, functional, user-friendly, straightforward. The design should feel simple yet professional, emphasizing clarity and ease of use.

🎨 COLOR SYSTEM
Light Theme:
* Background: Pure white #FFFFFF
* Secondary Background: Light gray #F9FAFB
* Cards: White #FFFFFF with subtle shadow
* Primary Yellow: #FBBF24 (buttons, links, main actions)
* Text Primary: #111827 (headings, body text)
* Text Secondary: #6B7280 (descriptions, labels, metadata)
* Border Color: #E5E7EB (subtle borders)
* Success Green: #10B981
* Warning Orange: #F59E0B
* Error Red: #EF4444
* Info Blue: #3B82F6
Dark Theme:
* Background: Dark gray #111827
* Secondary Background: #1F2937
* Cards: Dark gray #1F2937
* Primary Yellow: #FDE047 (adjusted for dark backgrounds - brighter)
* Text Primary: #F9FAFB (headings, body text)
* Text Secondary: #9CA3AF (descriptions, labels)
* Border Color: #374151
* Same accent colors as light theme
Page-Specific Accent Colors (Minimal Use):
* Registration/Login pages: Yellow accents #FBBF24
* Forgot Password page: Amber accents #F59E0B
* Reset Password page: Green accents #10B981
* Change Password page: Yellow accents #FBBF24

📝 TYPOGRAPHY
Font Family: Inter or Roboto (Google Fonts) - clean, modern, highly readable, minimalist
Type Scale:
* H1: 32-40px, Bold (700) - Main page headings
* H2: 24-28px, Semibold (600) - Section headings
* H3: 18-20px, Semibold (600) - Subsection headings
* Body Text: 15-16px, Regular (400) - Main content
* Small Text: 13-14px, Regular (400) - Metadata, captions
* Labels: 13-14px, Medium (500) - Form labels, tags
* Buttons: 15-16px, Medium (500) - All button text
Line Height: 1.6 for body text, 1.3 for headings Letter Spacing: -0.01em for headings, normal for body

🗄️ DATABASE MODELS & DATA STRUCTURE
User Model (UniqUser)
Fields:
* username: string (unique)
* email: string (unique, verified)
* password: hashed string
* profile_image: image upload (default avatar provided)
* is_email_verified: boolean (default false)
* email_verification_token: string (32 chars)
* email_verification_sent_at: datetime
* reset_password_token: string (32 chars)
* reset_password_sent_at: datetime
* groups: many-to-many (roles: Student, Admin, etc.)
* user_permissions: many-to-many
* date_joined: datetime
* last_login: datetime
Use in Design: User profile pages, account settings, order history, saved configurations

PC Components Models
Processor Model:
* name: string (e.g., "Core i9-13900K")
* manufacturer: string (Intel, AMD)
* socket: string (LGA1700, AM5)
* cores: integer
* threads: integer
* base_clock: float (GHz)
* boost_clock: float (GHz)
* tdp_base: integer (Watts)
* tdp_max: integer (Watts)
* description: long text
* price: decimal (2 decimal places)
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
GPU Model:
* name: string (e.g., "RTX 4080 Gaming X")
* manufacturer: string (NVIDIA, AMD)
* chipset: string (RTX 4080, RX 7900 XT)
* vram: integer (GB)
* vram_type: string (GDDR6, GDDR6X)
* power_consumption: integer (Watts)
* recommended_psu: integer (Watts)
* pcie_slots: integer (default 2)
* length: integer (millimeters)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
RAM Model:
* name: string
* manufacturer: string
* memory_type: choice (DDR4, DDR5)
* capacity: integer (GB per module)
* modules: integer (number of sticks)
* speed: integer (MHz)
* power_per_module: integer (Watts, default 5)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* Computed field: total_capacity = capacity × modules
Motherboard Model:
* name: string
* manufacturer: string
* socket: string (must match CPU socket)
* chipset: string (Z790, B650, etc.)
* form_factor: choice (ATX, Micro-ATX, Mini-ITX, E-ATX)
* ram_type: string (DDR4, DDR5)
* ram_slots: integer
* max_ram: integer (GB)
* m2_slots: integer
* sata_ports: integer
* pcie_x16_slots: integer
* power_consumption: integer (Watts, default 80)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
Storage Model:
* name: string
* manufacturer: string
* storage_type: choice (NVMe SSD, SATA SSD, HDD)
* capacity: integer (GB)
* read_speed: integer (MB/s, optional)
* write_speed: integer (MB/s, optional)
* power_consumption: integer (Watts)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
PowerSupply Model:
* name: string
* manufacturer: string
* wattage: integer (Watts)
* efficiency: choice (80 Plus, Bronze, Silver, Gold, Platinum, Titanium)
* modular: boolean (cable management)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
Case Model:
* name: string
* manufacturer: string
* form_factor: choice (ATX, Micro-ATX, Mini-ITX, E-ATX)
* max_gpu_length: integer (millimeters)
* max_cpu_cooler_height: integer (millimeters)
* fan_slots: integer
* included_fans: integer (default 0)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model

Laptop Model
* name: string
* manufacturer: string
* category: choice (Gaming, Office, Ultrabook, Workstation)
* processor_name: string
* gpu_name: string
* ram_size: integer (GB)
* ram_type: string
* storage_size: integer (GB)
* storage_type: string
* screen_size: float (inches)
* screen_resolution: string (1920x1080, 2560x1440, etc.)
* screen_refresh_rate: integer (Hz, default 60)
* weight: float (kg)
* battery_capacity: integer (Wh)
* power_consumption: integer (Watts, default 65)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model

ProductImage Model (Multiple Photos per Product)
CRITICAL: Each product can have multiple photos
* content_type: foreign key (links to any product type)
* object_id: integer (specific product ID)
* content_object: generic foreign key (Processor, GPU, RAM, etc.)
* image: image upload
* is_main: boolean (default false) - one main photo per product
* order: integer (display order, default 0)
* created_at: datetime
Use in Design:
* Product detail pages: main image + thumbnail gallery (4-8 images)
* Image carousel/slider
* Zoom functionality
* Lightbox for full-screen view

PCConfiguration Model (Custom PC Builds)
* user: foreign key to UniqUser (nullable for guests)
* name: string (e.g., "My Gaming Rig 2024")
* processor: foreign key to Processor (nullable)
* gpu: foreign key to GPU (nullable)
* motherboard: foreign key to Motherboard (nullable)
* ram: foreign key to RAM (nullable)
* power_supply: foreign key to PowerSupply (nullable)
* case: foreign key to Case (nullable)
* storage_devices: many-to-many to Storage (can have multiple)
* is_public: boolean (default false) - share with community
* created_at: datetime
* updated_at: datetime
Computed Methods:
* calculate_total_power(): returns total watts needed
* get_recommended_psu_wattage(): returns recommended PSU with 25% overhead
* calculate_total_price(): returns sum of all component prices
* check_compatibility(): returns list of compatibility issues
* is_compatible(): returns boolean (no critical issues)
Compatibility Checks:
* CPU socket matches motherboard socket
* RAM type matches motherboard RAM type
* PSU wattage sufficient for total power
* GPU length fits in case
* Motherboard form factor fits in case
Use in Design:
* PC Configurator page with component selection
* Compatibility indicator (green checkmark, orange warning, red error)
* Power consumption progress bar
* Price calculator
* Save/load configurations

ChatSession Model (AI Consultant)
* user: foreign key to UniqUser (nullable for guests)
* session_id: string (unique, for guest tracking)
* created_at: datetime
* updated_at: datetime
ChatMessage Model:
* session: foreign key to ChatSession
* role: choice (USER, ASSISTANT, SYSTEM)
* content: long text
* created_at: datetime
Use in Design:
* Chat widget modal (bottom-right floating)
* User messages: right-aligned, yellow
* AI messages: left-aligned, gray
* Typing indicator (3 animated dots)
* Chat history in session

Order Model
* user: foreign key to UniqUser
* configuration: foreign key to PCConfiguration (nullable)
* status: choice (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
* total_price: decimal
* full_name: string
* phone: string
* email: string
* address: long text
* comment: long text (optional)
* created_at: datetime
* updated_at: datetime
Use in Design:
* Order history page
* Order detail page with timeline
* Status badges (color-coded)
* Tracking information

Review Model
* user: foreign key to UniqUser
* content_type: foreign key (any product)
* object_id: integer
* content_object: generic foreign key
* rating: integer (1-5 stars)
* comment: long text
* is_approved: boolean (default true, moderation)
* created_at: datetime
Constraint: One review per user per product
Use in Design:
* Product detail page reviews section
* Star rating display (yellow stars)
* Rating distribution bars
* "Write a Review" form
* User avatar + name + date

Wishlist Model
* user: foreign key to UniqUser
* content_type: foreign key (any product)
* object_id: integer
* content_object: generic foreign key
* created_at: datetime
Constraint: One wishlist entry per user per product
Use in Design:
* Heart icon on product cards (filled/unfilled)
* Wishlist page with product grid
* "Add to Wishlist" button

🎨 MINIMALIST DESIGN SYSTEM COMPONENTS
Cards:
* Border radius: 8px (subtle, not too rounded)
* Shadow: 0 1px 3px rgba(0,0,0,0.08) default, 0 4px 6px rgba(0,0,0,0.1) on hover
* Padding: 24px for forms, 16px for product cards
* Border: 1px solid #E5E7EB (light gray, subtle)
* Background: white in light mode, #1F2937 in dark mode
* Minimal decoration, focus on content
Buttons:
* Primary: Yellow #FBBF24 background, dark gray #111827 text, 10px 20px padding, 6px border radius
* Secondary: Transparent background, 1px yellow border, yellow text
* Outline: 1px border only, no background
* Text: No border, no background, just yellow text
* Hover effect: Slightly darker shade (no lift effect - flat design)
* Active state: Opacity 0.9
* Disabled: 40% opacity, no hover effects
* Minimal shadows, flat appearance
Input Fields:
* Border: 1px solid #E5E7EB (light gray)
* Border radius: 6px
* Padding: 10px 14px
* Focus state: 1px yellow border #FBBF24, no ring
* Error state: Red border, red text below
* Success state: Green border
* With icon: Right-aligned icon (eye for password toggle)
* Placeholder: Gray color #9CA3AF
* Minimal styling, clean appearance
Icons:
* Style: Outlined/Line icons (Heroicons or Feather Icons)
* Size: 20-24px for UI elements, 16-18px for inline text
* Stroke width: 1.5-2px (thin, minimalist)
* Color: Matches theme (gray in light, lighter gray in dark)

📱 NAVIGATION BAR (All Pages)
Structure:
* Position: Sticky top, full width
* Background: White in light mode, #1F2937 in dark mode
* Height: 60px (slim, minimalist)
* Border bottom: 1px solid #E5E7EB
* Z-index: 50 (always on top)
* No shadows, flat design
Left Section:
* Text logo: "BuildBox" (Build in yellow #FBBF24, Box in dark gray/white)
* Font size: 24px, Bold
* No icon, pure text
* Hover: Slight opacity change
Center Section (Desktop only):
* Search bar: 400-500px width, minimal rounded (6px), with search icon
* Placeholder: "Search products..."
* Border: 1px solid #E5E7EB
* No shadow
Right Section:
* Theme toggle button: Simple icon, no background circle
* Wishlist icon: Heart outline with badge count
* Cart icon: Shopping bag outline with badge count
* User menu: Simple avatar or Login/Signup text links
* Spacing: 24px between icons
* No backgrounds, just icons
Mobile:
* Hamburger menu icon (left)
* Logo (center)
* Cart icon (right)
* Drawer menu slides from left

🦶 FOOTER DESIGN (All Pages)
IMPORTANT: Footer must appear on every single page
Structure: 4-column layout on desktop, stacked on mobile
Column 1: About BuildBox
* "BuildBox" text logo (smaller, yellow + gray)
* Brief description: "Build your dream PC with confidence. Expert guidance and best prices."
* Social media icons: Simple outline icons (Facebook, Twitter, Instagram, YouTube)
* Icons: 24x24px, minimal, no backgrounds
Column 2: Quick Links
* Home
* Browse Components
* Laptops
* PC Configurator
* About Us
* Contact
Column 3: Customer Service
* Contact Us
* Shipping Information
* Returns & Refunds
* FAQ
* Track Order
* Support Center
Column 4: Contact
* Email: support@buildbox.com
* Phone: +1 (555) 123-4567
* Address: 123 Tech Street, Silicon Valley, CA
Bottom Section:
* Horizontal divider line (1px, #E5E7EB)
* Left: Copyright © 2026 BuildBox. All rights reserved.
* Center: Payment method icons (simple, grayscale, 32x20px)
* Right: Privacy Policy | Terms of Service
Design Style:
* Background: Light gray #F9FAFB in light mode, #111827 in dark mode
* Text: Gray #6B7280
* Links: Hover effect - yellow color
* Padding: 48px top/bottom, 24px left/right
* Spacing: 32px between columns
* Minimal decoration, clean layout

📄 PAGE DESIGNS
1. LOGIN PAGE (/)
Layout: Centered card, 400px max width, minimal design
Header:
* Simple yellow line accent (3px height, 40px width, yellow #FBBF24)
* "Welcome Back" heading (H2, dark gray)
* "Sign in to your account" subtext (gray, smaller)
Form:
* Username input field (minimal, 1px border)
* Password input field with eye toggle button (right side)
* Remember me checkbox (left) + "Forgot password?" link (right, yellow)
* Yellow "Sign In" button (full width, 44px height, flat design)
Footer:
* Simple text: "Don't have an account?" + "Sign up" link (yellow)
Animations:
* Minimal fade in on load
* No elaborate animations

2. REGISTRATION PAGE (/registration/)
Layout: Centered card, 400px max width, minimal design
Header:
* Yellow line accent (3px height, 40px width)
* "Create Account" heading (H2)
* "Join BuildBox today" subtext
Form:
* Username input field
* Email input field
* Password input field with:
    * Eye toggle button (right side)
    * Password strength indicator below (3 horizontal bars, 3px height, 4px gap)
    * Strength bars: Weak (1 red bar), Fair (2 orange bars), Good (3 green bars)
    * Smooth 300ms transition
    * Text below: "Weak password" (red), "Fair password" (orange), "Good password" (green)
* Confirm password input field with:
    * Eye toggle button
    * Match indicator: "✓ Passwords match" (green) or "✗ Passwords do not match" (red)
* Yellow "Create Account" button (full width, flat)
Footer:
* "Already have an account?" + "Sign in" link (yellow)

3. FORGOT PASSWORD PAGE (/forgot_password/)
Layout: Centered card, 400px max width
Header:
* Orange line accent (3px height, 40px width, #F59E0B)
* "Forgot Password?" heading
* "We'll send you reset instructions" subtext
Form:
* Email input field (minimal)
* Orange "Send Reset Link" button (full width, flat)
Footer:
* "← Back to login" link (gray)

4. RESET PASSWORD PAGE (/reset_password//)
Layout: Centered card, 400px max width
Header:
* Green line accent (3px height, 40px width, #10B981)
* "Reset Password" heading
* "Enter your new password" subtext
Form:
* New password input with eye toggle and strength indicator (3 bars)
* Confirm password input with eye toggle and match indicator
* Password requirements (simple list):
    * "✓ At least 8 characters"
    * "✓ Mix of letters and numbers"
* Green "Reset Password" button (full width, flat)

5. CHANGE PASSWORD PAGE (/change_password/)
Layout: Centered card, 400px max width
Header:
* Yellow line accent
* "Change Password" heading
* "Update your password" subtext
Form:
* Current password input with eye toggle
* New password input with eye toggle and strength indicator
* Confirm password input with eye toggle and match indicator
* Password requirements list
* Yellow "Update Password" button (full width, flat)
Footer:
* "← Back to home" link

6. EMAIL CONFIRMATION SENT PAGE (/email_sent/)
Layout: Centered card, 400px max width
Content:
* Large envelope icon (48px, yellow outline)
* "Check Your Email" heading (H1)
* Description: "We've sent a confirmation email to your inbox. Please click the link to verify your account."
* Info box (light gray background #F9FAFB, minimal):
    * "Didn't receive the email?"
    * "Check your spam folder or wait a few minutes."
* Yellow "Back to Login" button (flat)

7. HOME PAGE (/main_site/home)
Hero Section:
* Clean white background (no gradients)
* Centered content, max-width 1000px
* Large heading (H1): "Build Your Dream PC"
* Subheading: "Configure, customize, and create the perfect computer"
* Two CTA buttons side by side:
    * "Start Building" (yellow background, dark text, flat)
    * "Browse Components" (outline, yellow border)
* Minimal decoration, focus on typography
Features Section:
* White background
* "Why Choose BuildBox?" heading (H2, centered)
* 3-column grid (1 column on mobile)
* Each feature card (minimal):
    * Simple icon (outline style, 32px, yellow)
    * Feature title (H3)
    * Description text (2-3 lines)
    * No shadows, just 1px border
Features:
1. Compatibility Check - "Automatic verification ensures all components work together"
2. Power Calculator - "Smart PSU recommendation based on your selection"
3. Best Prices - "Competitive pricing with real-time tracking"
CTA Section:
* Light gray background #F9FAFB
* Centered content
* "Ready to Build?" heading (H2)
* "Join thousands who built their dream PC with BuildBox" text
* "Get Started Now" button (yellow, flat)

8. COMPONENTS CATALOG PAGE (/main_site/components/)
Layout: Sidebar + Main content
Left Sidebar (260px width, sticky):
* "Filters" heading (simple, no decoration)
* Category checkboxes (minimal):
    * Processors
    * GPUs
    * Motherboards
    * RAM
    * Storage
    * Power Supplies
    * Cases
* Price range slider (simple, yellow accent)
* Manufacturer checkboxes
* Stock filter: "In Stock Only" toggle (minimal switch)
* "Clear Filters" text link (yellow)
Main Content:
* Breadcrumb: Home > Components (simple text, yellow links)
* Header bar:
    * Results count: "48 products"
    * Sort dropdown: Simple select, minimal styling
    * View toggle: Grid/List icons
* Product grid: 3-4 columns on desktop, 2 on tablet, 1 on mobile
Product Card (Minimal):
* Square image (260x260px, no border)
* Wishlist heart icon (top-right, outline)
* Product name (2 lines max)
* Key specs (2 bullet points, small text)
* Price (large, bold, dark gray)
* Stock indicator:
    * Green dot + "In Stock"
    * Orange dot + "Only 3 left"
    * Red dot + "Out of Stock"
* "Add to Cart" button (yellow, flat, full width)
* "View Details" link (small, yellow)
* Hover: Subtle shadow increase only
* Border: 1px solid #E5E7EB
Pagination:
* Simple numbers at bottom
* Current page: Yellow background
* Minimal styling

9. PRODUCT DETAIL PAGE (/main_site/product///)
Breadcrumb: Home > Components > [Category] > [Product Name]
Main Section (2 columns):
Left Column (60% width):
* Main product image (large, 560x560px, square, no border)
* Image gallery below: 4-8 thumbnail images (70x70px each)
* Thumbnails: 1px border, active has yellow border
* Click thumbnail: Instant change (no animation)
* Hover main image: Zoom cursor
* Click main image: Opens minimal lightbox
Right Column (40% width):
* Manufacturer name (small, gray)
* Product name (H1)
* Rating: 5 yellow stars + "(127 reviews)" link
* Price (very large, bold, dark gray)
* Stock status (simple text with colored dot)
* Short description (2-3 lines)
Specifications Table:
* Simple 2-column layout (Label | Value)
* 1px borders, minimal styling
* Key specs (5-6 rows)
* "Show all" expandable link (yellow)
Compatibility Note:
* Simple info box (light gray background)
* "Check compatibility with your build"
* "Open Configurator" link (yellow)
Actions:
* Quantity selector: Simple - | number | + buttons
* "Add to Cart" button (yellow, flat, full width)
* "Add to Wishlist" button (outline, yellow border, full width)
Tabs Section:
* Tab navigation: Description | Specifications | Reviews
* Active tab: Yellow underline (2px)
* Minimal styling
Description Tab:
* Clean text layout
* Bullet points for features
* No decoration
Specifications Tab:
* Complete specs table
* Minimal styling
Reviews Tab:
* Average rating (left):
    * Large number: 4.5/5
    * Yellow stars
    * "Based on 127 reviews"
* Rating distribution (right):
    * Simple horizontal bars (yellow)
    * Percentage + count
* "Write a Review" button (yellow, flat)
* Review cards (minimal):
    * User avatar (40x40px, circular)
    * User name + date
    * Yellow stars
    * Review text
    * "Helpful? Yes | No" links
Related Products:
* "You May Also Like" heading
* 4-product horizontal scroll
* Minimal product cards

10. LAPTOPS CATALOG PAGE (/main_site/laptops/)
Layout: Similar to Components Catalog
Filters:
* Category: Gaming, Office, Ultrabook, Workstation
* Price range slider (yellow accent)
* Processor options
* RAM options
* Screen size options
* GPU options
* Storage options
Product Cards:
* Laptop image (angled view)
* Category badge (simple text, yellow background)
* Name + model
* Key specs (4-5 lines, minimal)
* Price
* "View Details" button (yellow, flat)

11. PC CONFIGURATOR PAGE (/main_site/configurator/)
Header:
* "Build Your PC" heading (H1)
* "Save Configuration" button (outline, yellow)
* "Load Configuration" button (outline, yellow)
Layout: 2 columns (60% left, 40% right)
Left Column: Component Selection
Component Categories (Simple accordion): Each category is a minimal card:
1. Processor:
* Collapsed: "Choose Processor" button + icon
* Expanded: Selected component showing:
    * Component image (thumbnail, 60x60px)
    * Name + key specs
    * Price
    * "Change" link (yellow)
    * "Remove" icon (X)
2-7. GPU, Motherboard, RAM, Storage, PSU, Case:
* Same minimal pattern
* Compatibility indicators:
    * "✓ Compatible" (green text)
    * "⚠ Warning" (orange text)
    * "✗ Not compatible" (red text)
Right Column: Summary Panel (Sticky)
Configuration Summary:
* "Your Build" heading
* Component list (minimal):
    * Component type + name
    * Price (right)
    * Remove icon (X)
* Empty slots: "Not selected" (gray)
Compatibility Check:
* "Compatibility" heading
* Status:
    * "✓ All compatible" (green background, minimal)
    * "⚠ 2 warnings" (orange background)
    * "✗ Critical issues" (red background)
* Issues list (if any)
Power Calculation:
* "Power Consumption" heading
* Total power: "450W" (large)
* Recommended PSU: "650W"
* Simple progress bar (yellow fill)
* Color-coded: Green/Orange/Red
Price Summary:
* Subtotal: 1 , 234.56 < / l i > < l i > T a x ( 10  1,234.56</li> <li>Tax (10%):  1,234.56</li><li>Tax(10123.45
* Total: $1,358.01 (very large, bold)
Actions:
* "Add to Cart" button (yellow, flat, full width, large)
* "Save Configuration" button (outline, full width)
* "Share" link (text, yellow)

12. COMPONENT SELECTION MODAL
Overlay: Full-screen semi-transparent overlay
Modal: Centered, 85% viewport width, 85% viewport height, white background, minimal rounded corners (8px)
Header:
* "Select [Component Type]" title (H2, left)
* Close button (X icon, right, simple)
* Search bar (full width below):
    * Search icon (left)
    * Placeholder: "Search..."
    * Minimal border
Layout: Sidebar + Main content
Left Sidebar (240px):
* "Filters" heading
* Price range slider (yellow)
* Manufacturer checkboxes (minimal)
* Component-specific filters
* "Clear Filters" link (yellow)
Main Content:
* Sort dropdown (minimal)
* Results count: "48 processors"
* Product grid (3 columns)
Product Card (in modal):
* Product image (180x180px)
* Name + key specs
* Price (bold)
* Compatibility indicator:
    * "✓ Compatible" (green)
    * "⚠ Check compatibility" (orange)
    * "✗ Not compatible" (red)
* "Select" button (yellow if compatible, disabled if not)
Footer:
* "Cancel" button (left, outline)
* "Confirm Selection" button (right, yellow, flat)

13. SAVED CONFIGURATIONS PAGE (/main_site/configurations/)
Header:
* "My Configurations" heading (H1)
* "Create New" button (yellow, flat, right)
Configuration Cards (Grid, 3 columns): Each card (minimal):
* Configuration name (H3, editable)
* Component icons (6 small icons, 24x24px, outline style)
* Gray placeholder if not selected
* Compatibility badge:
    * "✓ Compatible" (green)
    * "⚠ Warnings" (orange)
    * "✗ Issues" (red)
* Total price (large, bold)
* Created date (small, gray)
* Actions:
    * "Edit" button (yellow, flat)
    * "Duplicate" link (text, yellow)
    * "Delete" link (text, red)
    * "Add to Cart" button (outline)
* Border: 1px solid #E5E7EB
* Hover: Subtle shadow
Empty State:
* Simple icon (computer outline, 48px)
* "No configurations yet"
* "Start building your first PC"
* "Create New" button (yellow)

14. AI CHAT CONSULTANT (MODAL WIDGET)
Floating Trigger Button (ALL pages):
* Position: Fixed, bottom-right corner
* Distance: 24px from right, 24BuildBox - Complete PC Building E-Commerce Platform Design Brief
* UPDATED VERSION - Minimalist Yellow Theme
* Create a professional, minimalist Figma design system for BuildBox - a comprehensive e-commerce platform for building custom PCs, buying laptops, and individual PC components with AI consultation.
* 
* 🎨 BRAND IDENTITY
* Logo Design: Simple text-based logo: "BuildBox" in clean sans-serif font. "Build" in bright yellow #FBBF24 and "Box" in dark gray #1F2937 for light mode, white #FFFFFF for dark mode. Font weight: Bold (700). Size: 24px. No icon required - pure minimalist text logo.
* Brand Personality: Minimalist, modern, clean, functional, user-friendly, straightforward. The design should feel simple yet professional, emphasizing clarity and ease of use.
* 
* 🎨 COLOR SYSTEM
* Light Theme:
* Background: Pure white #FFFFFF
* Secondary Background: Light gray #F9FAFB
* Cards: White #FFFFFF with subtle shadow
* Primary Yellow: #FBBF24 (buttons, links, main actions)
* Text Primary: #111827 (headings, body text)
* Text Secondary: #6B7280 (descriptions, labels, metadata)
* Border Color: #E5E7EB (subtle borders)
* Success Green: #10B981
* Warning Orange: #F59E0B
* Error Red: #EF4444
* Info Blue: #3B82F6
* Dark Theme:
* Background: Dark gray #111827
* Secondary Background: #1F2937
* Cards: Dark gray #1F2937
* Primary Yellow: #FDE047 (adjusted for dark backgrounds - brighter)
* Text Primary: #F9FAFB (headings, body text)
* Text Secondary: #9CA3AF (descriptions, labels)
* Border Color: #374151
* Same accent colors as light theme
* Page-Specific Accent Colors (Minimal Use):
* Registration/Login pages: Yellow accents #FBBF24
* Forgot Password page: Amber accents #F59E0B
* Reset Password page: Green accents #10B981
* Change Password page: Yellow accents #FBBF24
* 
* 📝 TYPOGRAPHY
* Font Family: Inter or Roboto (Google Fonts) - clean, modern, highly readable, minimalist
* Type Scale:
* H1: 32-40px, Bold (700) - Main page headings
* H2: 24-28px, Semibold (600) - Section headings
* H3: 18-20px, Semibold (600) - Subsection headings
* Body Text: 15-16px, Regular (400) - Main content
* Small Text: 13-14px, Regular (400) - Metadata, captions
* Labels: 13-14px, Medium (500) - Form labels, tags
* Buttons: 15-16px, Medium (500) - All button text
* Line Height: 1.6 for body text, 1.3 for headings Letter Spacing: -0.01em for headings, normal for body
* 
* 🗄️ DATABASE MODELS & DATA STRUCTURE
* User Model (UniqUser)
* Fields:
* username: string (unique)
* email: string (unique, verified)
* password: hashed string
* profile_image: image upload (default avatar provided)
* is_email_verified: boolean (default false)
* email_verification_token: string (32 chars)
* email_verification_sent_at: datetime
* reset_password_token: string (32 chars)
* reset_password_sent_at: datetime
* groups: many-to-many (roles: Student, Admin, etc.)
* user_permissions: many-to-many
* date_joined: datetime
* last_login: datetime
* Use in Design: User profile pages, account settings, order history, saved configurations
* 
* PC Components Models
* Processor Model:
* name: string (e.g., "Core i9-13900K")
* manufacturer: string (Intel, AMD)
* socket: string (LGA1700, AM5)
* cores: integer
* threads: integer
* base_clock: float (GHz)
* boost_clock: float (GHz)
* tdp_base: integer (Watts)
* tdp_max: integer (Watts)
* description: long text
* price: decimal (2 decimal places)
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* GPU Model:
* name: string (e.g., "RTX 4080 Gaming X")
* manufacturer: string (NVIDIA, AMD)
* chipset: string (RTX 4080, RX 7900 XT)
* vram: integer (GB)
* vram_type: string (GDDR6, GDDR6X)
* power_consumption: integer (Watts)
* recommended_psu: integer (Watts)
* pcie_slots: integer (default 2)
* length: integer (millimeters)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* RAM Model:
* name: string
* manufacturer: string
* memory_type: choice (DDR4, DDR5)
* capacity: integer (GB per module)
* modules: integer (number of sticks)
* speed: integer (MHz)
* power_per_module: integer (Watts, default 5)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* Computed field: total_capacity = capacity × modules
* Motherboard Model:
* name: string
* manufacturer: string
* socket: string (must match CPU socket)
* chipset: string (Z790, B650, etc.)
* form_factor: choice (ATX, Micro-ATX, Mini-ITX, E-ATX)
* ram_type: string (DDR4, DDR5)
* ram_slots: integer
* max_ram: integer (GB)
* m2_slots: integer
* sata_ports: integer
* pcie_x16_slots: integer
* power_consumption: integer (Watts, default 80)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* Storage Model:
* name: string
* manufacturer: string
* storage_type: choice (NVMe SSD, SATA SSD, HDD)
* capacity: integer (GB)
* read_speed: integer (MB/s, optional)
* write_speed: integer (MB/s, optional)
* power_consumption: integer (Watts)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* PowerSupply Model:
* name: string
* manufacturer: string
* wattage: integer (Watts)
* efficiency: choice (80 Plus, Bronze, Silver, Gold, Platinum, Titanium)
* modular: boolean (cable management)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* Case Model:
* name: string
* manufacturer: string
* form_factor: choice (ATX, Micro-ATX, Mini-ITX, E-ATX)
* max_gpu_length: integer (millimeters)
* max_cpu_cooler_height: integer (millimeters)
* fan_slots: integer
* included_fans: integer (default 0)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* 
* Laptop Model
* name: string
* manufacturer: string
* category: choice (Gaming, Office, Ultrabook, Workstation)
* processor_name: string
* gpu_name: string
* ram_size: integer (GB)
* ram_type: string
* storage_size: integer (GB)
* storage_type: string
* screen_size: float (inches)
* screen_resolution: string (1920x1080, 2560x1440, etc.)
* screen_refresh_rate: integer (Hz, default 60)
* weight: float (kg)
* battery_capacity: integer (Wh)
* power_consumption: integer (Watts, default 65)
* description: long text
* price: decimal
* stock: integer
* image: main product image
* created_at: datetime
* Multiple images via ProductImage model
* 
* ProductImage Model (Multiple Photos per Product)
* CRITICAL: Each product can have multiple photos
* content_type: foreign key (links to any product type)
* object_id: integer (specific product ID)
* content_object: generic foreign key (Processor, GPU, RAM, etc.)
* image: image upload
* is_main: boolean (default false) - one main photo per product
* order: integer (display order, default 0)
* created_at: datetime
* Use in Design:
* Product detail pages: main image + thumbnail gallery (4-8 images)
* Image carousel/slider
* Zoom functionality
* Lightbox for full-screen view
* 
* PCConfiguration Model (Custom PC Builds)
* user: foreign key to UniqUser (nullable for guests)
* name: string (e.g., "My Gaming Rig 2024")
* processor: foreign key to Processor (nullable)
* gpu: foreign key to GPU (nullable)
* motherboard: foreign key to Motherboard (nullable)
* ram: foreign key to RAM (nullable)
* power_supply: foreign key to PowerSupply (nullable)
* case: foreign key to Case (nullable)
* storage_devices: many-to-many to Storage (can have multiple)
* is_public: boolean (default false) - share with community
* created_at: datetime
* updated_at: datetime
* Computed Methods:
* calculate_total_power(): returns total watts needed
* get_recommended_psu_wattage(): returns recommended PSU with 25% overhead
* calculate_total_price(): returns sum of all component prices
* check_compatibility(): returns list of compatibility issues
* is_compatible(): returns boolean (no critical issues)
* Compatibility Checks:
* CPU socket matches motherboard socket
* RAM type matches motherboard RAM type
* PSU wattage sufficient for total power
* GPU length fits in case
* Motherboard form factor fits in case
* Use in Design:
* PC Configurator page with component selection
* Compatibility indicator (green checkmark, orange warning, red error)
* Power consumption progress bar
* Price calculator
* Save/load configurations
* 
* ChatSession Model (AI Consultant)
* user: foreign key to UniqUser (nullable for guests)
* session_id: string (unique, for guest tracking)
* created_at: datetime
* updated_at: datetime
* ChatMessage Model:
* session: foreign key to ChatSession
* role: choice (USER, ASSISTANT, SYSTEM)
* content: long text
* created_at: datetime
* Use in Design:
* Chat widget modal (bottom-right floating)
* User messages: right-aligned, yellow
* AI messages: left-aligned, gray
* Typing indicator (3 animated dots)
* Chat history in session
* 
* Order Model
* user: foreign key to UniqUser
* configuration: foreign key to PCConfiguration (nullable)
* status: choice (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
* total_price: decimal
* full_name: string
* phone: string
* email: string
* address: long text
* comment: long text (optional)
* created_at: datetime
* updated_at: datetime
* Use in Design:
* Order history page
* Order detail page with timeline
* Status badges (color-coded)
* Tracking information
* 
* Review Model
* user: foreign key to UniqUser
* content_type: foreign key (any product)
* object_id: integer
* content_object: generic foreign key
* rating: integer (1-5 stars)
* comment: long text
* is_approved: boolean (default true, moderation)
* created_at: datetime
* Constraint: One review per user per product
* Use in Design:
* Product detail page reviews section
* Star rating display (yellow stars)
* Rating distribution bars
* "Write a Review" form
* User avatar + name + date
* 
* Wishlist Model
* user: foreign key to UniqUser
* content_type: foreign key (any product)
* object_id: integer
* content_object: generic foreign key
* created_at: datetime
* Constraint: One wishlist entry per user per product
* Use in Design:
* Heart icon on product cards (filled/unfilled)
* Wishlist page with product grid
* "Add to Wishlist" button
* 
* 🎨 MINIMALIST DESIGN SYSTEM COMPONENTS
* Cards:
* Border radius: 8px (subtle, not too rounded)
* Shadow: 0 1px 3px rgba(0,0,0,0.08) default, 0 4px 6px rgba(0,0,0,0.1) on hover
* Padding: 24px for forms, 16px for product cards
* Border: 1px solid #E5E7EB (light gray, subtle)
* Background: white in light mode, #1F2937 in dark mode
* Minimal decoration, focus on content
* Buttons:
* Primary: Yellow #FBBF24 background, dark gray #111827 text, 10px 20px padding, 6px border radius
* Secondary: Transparent background, 1px yellow border, yellow text
* Outline: 1px border only, no background
* Text: No border, no background, just yellow text
* Hover effect: Slightly darker shade (no lift effect - flat design)
* Active state: Opacity 0.9
* Disabled: 40% opacity, no hover effects
* Minimal shadows, flat appearance
* Input Fields:
* Border: 1px solid #E5E7EB (light gray)
* Border radius: 6px
* Padding: 10px 14px
* Focus state: 1px yellow border #FBBF24, no ring
* Error state: Red border, red text below
* Success state: Green border
* With icon: Right-aligned icon (eye for password toggle)
* Placeholder: Gray color #9CA3AF
* Minimal styling, clean appearance
* Icons:
* Style: Outlined/Line icons (Heroicons or Feather Icons)
* Size: 20-24px for UI elements, 16-18px for inline text
* Stroke width: 1.5-2px (thin, minimalist)
* Color: Matches theme (gray in light, lighter gray in dark)
* 
* 📱 NAVIGATION BAR (All Pages)
* Structure:
* Position: Sticky top, full width
* Background: White in light mode, #1F2937 in dark mode
* Height: 60px (slim, minimalist)
* Border bottom: 1px solid #E5E7EB
* Z-index: 50 (always on top)
* No shadows, flat design
* Left Section:
* Text logo: "BuildBox" (Build in yellow #FBBF24, Box in dark gray/white)
* Font size: 24px, Bold
* No icon, pure text
* Hover: Slight opacity change
* Center Section (Desktop only):
* Search bar: 400-500px width, minimal rounded (6px), with search icon
* Placeholder: "Search products..."
* Border: 1px solid #E5E7EB
* No shadow
* Right Section:
* Theme toggle button: Simple icon, no background circle
* Wishlist icon: Heart outline with badge count
* Cart icon: Shopping bag outline with badge count
* User menu: Simple avatar or Login/Signup text links
* Spacing: 24px between icons
* No backgrounds, just icons
* Mobile:
* Hamburger menu icon (left)
* Logo (center)
* Cart icon (right)
* Drawer menu slides from left
* 
* 🦶 FOOTER DESIGN (All Pages)
* IMPORTANT: Footer must appear on every single page
* Structure: 4-column layout on desktop, stacked on mobile
* Column 1: About BuildBox
* "BuildBox" text logo (smaller, yellow + gray)
* Brief description: "Build your dream PC with confidence. Expert guidance and best prices."
* Social media icons: Simple outline icons (Facebook, Twitter, Instagram, YouTube)
* Icons: 24x24px, minimal, no backgrounds
* Column 2: Quick Links
* Home
* Browse Components
* Laptops
* PC Configurator
* About Us
* Contact
* Column 3: Customer Service
* Contact Us
* Shipping Information
* Returns & Refunds
* FAQ
* Track Order
* Support Center
* Column 4: Contact
* Email: support@buildbox.com
* Phone: +1 (555) 123-4567
* Address: 123 Tech Street, Silicon Valley, CA
* Bottom Section:
* Horizontal divider line (1px, #E5E7EB)
* Left: Copyright © 2026 BuildBox. All rights reserved.
* Center: Payment method icons (simple, grayscale, 32x20px)
* Right: Privacy Policy | Terms of Service
* Design Style:
* Background: Light gray #F9FAFB in light mode, #111827 in dark mode
* Text: Gray #6B7280
* Links: Hover effect - yellow color
* Padding: 48px top/bottom, 24px left/right
* Spacing: 32px between columns
* Minimal decoration, clean layout
* 
* 📄 PAGE DESIGNS
* 1. LOGIN PAGE (/)
* Layout: Centered card, 400px max width, minimal design
* Header:
* Simple yellow line accent (3px height, 40px width, yellow #FBBF24)
* "Welcome Back" heading (H2, dark gray)
* "Sign in to your account" subtext (gray, smaller)
* Form:
* Username input field (minimal, 1px border)
* Password input field with eye toggle button (right side)
* Remember me checkbox (left) + "Forgot password?" link (right, yellow)
* Yellow "Sign In" button (full width, 44px height, flat design)
* Footer:
* Simple text: "Don't have an account?" + "Sign up" link (yellow)
* Animations:
* Minimal fade in on load
* No elaborate animations
* 
* 2. REGISTRATION PAGE (/registration/)
* Layout: Centered card, 400px max width, minimal design
* Header:
* Yellow line accent (3px height, 40px width)
* "Create Account" heading (H2)
* "Join BuildBox today" subtext
* Form:
* Username input field
* Email input field
* Password input field with:
    * Eye toggle button (right side)
    * Password strength indicator below (3 horizontal bars, 3px height, 4px gap)
    * Strength bars: Weak (1 red bar), Fair (2 orange bars), Good (3 green bars)
    * Smooth 300ms transition
    * Text below: "Weak password" (red), "Fair password" (orange), "Good password" (green)
* Confirm password input field with:
    * Eye toggle button
    * Match indicator: "✓ Passwords match" (green) or "✗ Passwords do not match" (red)
* Yellow "Create Account" button (full width, flat)
* Footer:
* "Already have an account?" + "Sign in" link (yellow)
* 
* 3. FORGOT PASSWORD PAGE (/forgot_password/)
* Layout: Centered card, 400px max width
* Header:
* Orange line accent (3px height, 40px width, #F59E0B)
* "Forgot Password?" heading
* "We'll send you reset instructions" subtext
* Form:
* Email input field (minimal)
* Orange "Send Reset Link" button (full width, flat)
* Footer:
* "← Back to login" link (gray)
* 
* 4. RESET PASSWORD PAGE (/reset_password//)
* Layout: Centered card, 400px max width
* Header:
* Green line accent (3px height, 40px width, #10B981)
* "Reset Password" heading
* "Enter your new password" subtext
* Form:
* New password input with eye toggle and strength indicator (3 bars)
* Confirm password input with eye toggle and match indicator
* Password requirements (simple list):
    * "✓ At least 8 characters"
    * "✓ Mix of letters and numbers"
* Green "Reset Password" button (full width, flat)
* 
* 5. CHANGE PASSWORD PAGE (/change_password/)
* Layout: Centered card, 400px max width
* Header:
* Yellow line accent
* "Change Password" heading
* "Update your password" subtext
* Form:
* Current password input with eye toggle
* New password input with eye toggle and strength indicator
* Confirm password input with eye toggle and match indicator
* Password requirements list
* Yellow "Update Password" button (full width, flat)
* Footer:
* "← Back to home" link
* 
* 6. EMAIL CONFIRMATION SENT PAGE (/email_sent/)
* Layout: Centered card, 400px max width
* Content:
* Large envelope icon (48px, yellow outline)
* "Check Your Email" heading (H1)
* Description: "We've sent a confirmation email to your inbox. Please click the link to verify your account."
* Info box (light gray background #F9FAFB, minimal):
    * "Didn't receive the email?"
    * "Check your spam folder or wait a few minutes."
* Yellow "Back to Login" button (flat)
* 
* 7. HOME PAGE (/main_site/home)
* Hero Section:
* Clean white background (no gradients)
* Centered content, max-width 1000px
* Large heading (H1): "Build Your Dream PC"
* Subheading: "Configure, customize, and create the perfect computer"
* Two CTA buttons side by side:
    * "Start Building" (yellow background, dark text, flat)
    * "Browse Components" (outline, yellow border)
* Minimal decoration, focus on typography
* Features Section:
* White background
* "Why Choose BuildBox?" heading (H2, centered)
* 3-column grid (1 column on mobile)
* Each feature card (minimal):
    * Simple icon (outline style, 32px, yellow)
    * Feature title (H3)
    * Description text (2-3 lines)
    * No shadows, just 1px border
* Features:
* Compatibility Check - "Automatic verification ensures all components work together"
* Power Calculator - "Smart PSU recommendation based on your selection"
* Best Prices - "Competitive pricing with real-time tracking"
* CTA Section:
* Light gray background #F9FAFB
* Centered content
* "Ready to Build?" heading (H2)
* "Join thousands who built their dream PC with BuildBox" text
* "Get Started Now" button (yellow, flat)
* 
* 8. COMPONENTS CATALOG PAGE (/main_site/components/)
* Layout: Sidebar + Main content
* Left Sidebar (260px width, sticky):
* "Filters" heading (simple, no decoration)
* Category checkboxes (minimal):
    * Processors
    * GPUs
    * Motherboards
    * RAM
    * Storage
    * Power Supplies
    * Cases
* Price range slider (simple, yellow accent)
* Manufacturer checkboxes
* Stock filter: "In Stock Only" toggle (minimal switch)
* "Clear Filters" text link (yellow)
* Main Content:
* Breadcrumb: Home > Components (simple text, yellow links)
* Header bar:
    * Results count: "48 products"
    * Sort dropdown: Simple select, minimal styling
    * View toggle: Grid/List icons
* Product grid: 3-4 columns on desktop, 2 on tablet, 1 on mobile
* Product Card (Minimal):
* Square image (260x260px, no border)
* Wishlist heart icon (top-right, outline)
* Product name (2 lines max)
* Key specs (2 bullet points, small text)
* Price (large, bold, dark gray)
* Stock indicator:
    * Green dot + "In Stock"
    * Orange dot + "Only 3 left"
    * Red dot + "Out of Stock"
* "Add to Cart" button (yellow, flat, full width)
* "View Details" link (small, yellow)
* Hover: Subtle shadow increase only
* Border: 1px solid #E5E7EB
* Pagination:
* Simple numbers at bottom
* Current page: Yellow background
* Minimal styling
* 
* 9. PRODUCT DETAIL PAGE (/main_site/product///)
* Breadcrumb: Home > Components > [Category] > [Product Name]
* Main Section (2 columns):
* Left Column (60% width):
* Main product image (large, 560x560px, square, no border)
* Image gallery below: 4-8 thumbnail images (70x70px each)
* Thumbnails: 1px border, active has yellow border
* Click thumbnail: Instant change (no animation)
* Hover main image: Zoom cursor
* Click main image: Opens minimal lightbox
* Right Column (40% width):
* Manufacturer name (small, gray)
* Product name (H1)
* Rating: 5 yellow stars + "(127 reviews)" link
* Price (very large, bold, dark gray)
* Stock status (simple text with colored dot)
* Short description (2-3 lines)
* Specifications Table:
* Simple 2-column layout (Label | Value)
* 1px borders, minimal styling
* Key specs (5-6 rows)
* "Show all" expandable link (yellow)
* Compatibility Note:
* Simple info box (light gray background)
* "Check compatibility with your build"
* "Open Configurator" link (yellow)
* Actions:
* Quantity selector: Simple - | number | + buttons
* "Add to Cart" button (yellow, flat, full width)
* "Add to Wishlist" button (outline, yellow border, full width)
* Tabs Section:
* Tab navigation: Description | Specifications | Reviews
* Active tab: Yellow underline (2px)
* Minimal styling
* Description Tab:
* Clean text layout
* Bullet points for features
* No decoration
* Specifications Tab:
* Complete specs table
* Minimal styling
* Reviews Tab:
* Average rating (left):
    * Large number: 4.5/5
    * Yellow stars
    * "Based on 127 reviews"
* Rating distribution (right):
    * Simple horizontal bars (yellow)
    * Percentage + count
* "Write a Review" button (yellow, flat)
* Review cards (minimal):
    * User avatar (40x40px, circular)
    * User name + date
    * Yellow stars
    * Review text
    * "Helpful? Yes | No" links
* Related Products:
* "You May Also Like" heading
* 4-product horizontal scroll
* Minimal product cards
* 
* 10. LAPTOPS CATALOG PAGE (/main_site/laptops/)
* Layout: Similar to Components Catalog
* Filters:
* Category: Gaming, Office, Ultrabook, Workstation
* Price range slider (yellow accent)
* Processor options
* RAM options
* Screen size options
* GPU options
* Storage options
* Product Cards:
* Laptop image (angled view)
* Category badge (simple text, yellow background)
* Name + model
* Key specs (4-5 lines, minimal)
* Price
* "View Details" button (yellow, flat)
* 
* 11. PC CONFIGURATOR PAGE (/main_site/configurator/)
* Header:
* "Build Your PC" heading (H1)
* "Save Configuration" button (outline, yellow)
* "Load Configuration" button (outline, yellow)
* Layout: 2 columns (60% left, 40% right)
* Left Column: Component Selection
* Component Categories (Simple accordion): Each category is a minimal card:
* 1. Processor:
* Collapsed: "Choose Processor" button + icon
* Expanded: Selected component showing:
    * Component image (thumbnail, 60x60px)
    * Name + key specs
    * Price
    * "Change" link (yellow)
    * "Remove" icon (X)
* 2-7. GPU, Motherboard, RAM, Storage, PSU, Case:
* Same minimal pattern
* Compatibility indicators:
    * "✓ Compatible" (green text)
    * "⚠ Warning" (orange text)
    * "✗ Not compatible" (red text)
* Right Column: Summary Panel (Sticky)
* Configuration Summary:
* "Your Build" heading
* Component list (minimal):
    * Component type + name
    * Price (right)
    * Remove icon (X)
* Empty slots: "Not selected" (gray)
* Compatibility Check:
* "Compatibility" heading
* Status:
    * "✓ All compatible" (green background, minimal)
    * "⚠ 2 warnings" (orange background)
    * "✗ Critical issues" (red background)
* Issues list (if any)
* Power Calculation:
* "Power Consumption" heading
* Total power: "450W" (large)
* Recommended PSU: "650W"
* Simple progress bar (yellow fill)
* Color-coded: Green/Orange/Red
* Price Summary:
* Subtotal: 1 1,234.56</li> <li>Tax (10%):  1,234.56</li><li>Tax(10123.45
* Total: $1,358.01 (very large, bold)
* Actions:
* "Add to Cart" button (yellow, flat, full width, large)
* "Save Configuration" button (outline, full width)
* "Share" link (text, yellow)
* 
* 12. COMPONENT SELECTION MODAL
* Overlay: Full-screen semi-transparent overlay
* Modal: Centered, 85% viewport width, 85% viewport height, white background, minimal rounded corners (8px)
* Header:
* "Select [Component Type]" title (H2, left)
* Close button (X icon, right, simple)
* Search bar (full width below):
    * Search icon (left)
    * Placeholder: "Search..."
    * Minimal border
* Layout: Sidebar + Main content
* Left Sidebar (240px):
* "Filters" heading
* Price range slider (yellow)
* Manufacturer checkboxes (minimal)
* Component-specific filters
* "Clear Filters" link (yellow)
* Main Content:
* Sort dropdown (minimal)
* Results count: "48 processors"
* Product grid (3 columns)
* Product Card (in modal):
* Product image (180x180px)
* Name + key specs
* Price (bold)
* Compatibility indicator:
    * "✓ Compatible" (green)
    * "⚠ Check compatibility" (orange)
    * "✗ Not compatible" (red)
* "Select" button (yellow if compatible, disabled if not)
* Footer:
* "Cancel" button (left, outline)
* "Confirm Selection" button (right, yellow, flat)
* 
* 13. SAVED CONFIGURATIONS PAGE (/main_site/configurations/)
* Header:
* "My Configurations" heading (H1)
* "Create New" button (yellow, flat, right)
* Configuration Cards (Grid, 3 columns): Each card (minimal):
* Configuration name (H3, editable)
* Component icons (6 small icons, 24x24px, outline style)
* Gray placeholder if not selected
* Compatibility badge:
    * "✓ Compatible" (green)
    * "⚠ Warnings" (orange)
    * "✗ Issues" (red)
* Total price (large, bold)
* Created date (small, gray)
* Actions:
    * "Edit" button (yellow, flat)
    * "Duplicate" link (text, yellow)
    * "Delete" link (text, red)
    * "Add to Cart" button (outline)
* Border: 1px solid #E5E7EB
* Hover: Subtle shadow
* Empty State:
* Simple icon (computer outline, 48px)
* "No configurations yet"
* "Start building your first PC"
* "Create New" button (yellow)
* 
* 14. AI CHAT CONSULTANT (MODAL WIDGET)
* Floating Trigger Button (ALL pages):
* Position: Fixed, bottom-right corner
* 	•	Distance: 24px from right, 24 px from bottom
* Size: 56x56px circular button
* Background: Yellow #FBBF24
* Icon: Chat bubble outline (white, 24px)
* Shadow: 0 4px 12px rgba(251, 191, 36, 0.3)
* Hover: Opacity 0.9
* Z-index: 1000
* Chat Modal Widget:
* Position & Size:
* Position: Fixed, bottom-right corner
* Width: 380px
* Height: 600px
* Distance: 24px from right, 90px from bottom (above button)
* Border radius: 8px
* Shadow: 0 8px 16px rgba(0, 0, 0, 0.1)
* Z-index: 1001
* Background: White (light mode), #1F2937 (dark mode)
* Header (56px height, sticky):
* Background: Yellow #FBBF24
* Border radius: 8px 8px 0 0
* Padding: 16px
* Layout:
    * Left: Chat icon (24px, dark gray) + "AI Assistant" text (dark gray, bold, 16px)
    * Right: Minimize button (chevron down) + Close button (X)
* Minimal, flat design
* Chat Messages Area (scrollable, 444px height):
* Background: White (light mode), #1F2937 (dark mode)
* Padding: 16px
* Smooth scrolling
* Empty State:
* Welcome message:
    * Robot avatar (36x36px, circular, yellow background, left)
    * Gray bubble (#F9FAFB light, #374151 dark)
    * Text: "Hi! I'm your AI assistant. How can I help you today?"
    * Timestamp: "Just now" (small, gray)

    * "Proceed to Checkout" button (yellow, flat, full width, large)
    * "Continue Shopping" link (centered, yellow)
    * Border: 1px solid #E5E7EB
    * Minimal styling
* Promo Code:
    * "Have a promo code?" expandable
    * Input + "Apply" button
    * Success: Green message
    * Error: Red message
*  16. CHECKOUT PAGE (/main_site/checkout/) Progress Indicator (top):
    * 3 steps: Shipping → Payment → Review
    * Current step: Yellow background
    * Completed: Green checkmark
    * Future: Gray
    * Simple line connecting
    * Minimal design
* Layout: 2 columns (60% left, 40% right) Left Column: Forms Step 1: Shipping Information
    * "Shipping Information" heading (H2)
    * Form fields (minimal):
        * Full name
        * Email
        * Phone
        * Address line 1
        * Address line 2 (optional)
        * City
        * State (dropdown)
        * ZIP code
        * Country (dropdown)
    * "Save address" checkbox
    * "Continue to Payment" button (yellow, flat, right)
* Step 2: Payment Method
    * "Payment Method" heading (H2)
    * Payment options (radio buttons, minimal):
        * Credit/Debit Card
        * PayPal
        * Apple Pay
        * Google Pay
    * Card form:
        * Card number (with icon)
        * Cardholder name
        * Expiration (MM/YY)
        * CVV
    * "Save card" checkbox
    * "Back" button (outline, left)
    * "Continue" button (yellow, right)
* Step 3: Order Review
    * "Review Your Order" heading (H2)
    * Shipping address (editable)
    * Payment method (editable)
    * Order items (compact list)
    * Order notes textarea (optional)
    * Terms checkbox:
        * "I agree to Terms and Privacy Policy"
    * "Back" button (outline, left)
    * "Place Order" button (yellow, large, right)
* Right Column: Order Summary (Sticky)
    * "Order Summary" heading
    * Product list (compact):
        * Image (50x50px)
        * Name (1 line)
        * Quantity × Price
    * Security badges (simple icons)
    * Border: 1px solid #E5E7EB
* Loading State:
    * Simple spinner overlay
    * "Processing your order..."
*  17. ORDER CONFIRMATION PAGE (/main_site/order/confirmation//) Success Section:
    * Large green checkmark icon (48px, outline)
    * "Order Confirmed!" heading (H1, green)
    * Order number: "#12345" (large, bold)
    * "Thank you, [Name]!"
    * "Confirmation sent to [email]"
* Order Details Card: Shipping Information:
    * "Shipping Address" heading
    * Full address
    * Estimated delivery: "3-5 business days"
    * Tracking: "You'll receive tracking via email"
* Payment Information:
    * "Payment Method" heading
    * Card type + last 4 digits
    * Amount: $1,358.01
* Order Items:
    * "Order Items" heading
    * Product list:
        * Image + name + quantity + price
    * Subtotal, shipping, tax, total
* Actions:
    * "View Order Details" button (yellow, flat)
    * "Continue Shopping" button (outline)
    * "Download Invoice" link (yellow)
* Timeline:
    * Simple horizontal timeline:
        * Order confirmed ✓ (green)
        * Processing (current, yellow)
        * Shipped (gray)
        * Delivered (gray)
    * Minimal design
*  18. USER DASHBOARD PAGE (/main_site/account/) Layout: Sidebar + Main content Left Sidebar (240px):
    * User profile:
        * Avatar (64x64px, circular)
        * Username (bold)
        * Email (small, gray)
        * "Edit Profile" link (yellow)
    * Navigation menu (vertical, minimal):
        * Dashboard (active, yellow background)
        * Orders
        * Configurations
        * Wishlist
        * Reviews
        * Settings
        * Logout (red text)
    * Active: Yellow background, bold
* Main Content: Welcome Section:
    * "Welcome back, [Name]!" heading (H1)
    * Last login: "2 hours ago" (small, gray)
* Quick Stats (3 cards): Card 1: Total Orders
    * Large number: "12"
    * Icon: Shopping bag outline (24px, yellow)
    * "View all" link (yellow)
    * Border: 1px solid #E5E7EB
* Card 2: Saved Configs
    * Number: "5"
    * Icon: Computer outline
    * "View all" link
* Card 3: Wishlist Items
    * Number: "23"
    * Icon: Heart outline
    * "View all" link
* Recent Orders:
    * "Recent Orders" heading (H2)
    * "View all" link (right, yellow)
    * 3 order cards (minimal):
        * Order number + date
        * Status badge (simple, colored background)
        * Product thumbnails (3-4, 40x40px)
        * Total price
        * "View Details" button (outline)
    * Border: 1px solid #E5E7EB
* Saved Configurations:
    * "Saved Configurations" heading (H2)
    * "View all" link (right)
    * 3 config cards (compact)
    * "Create New" button (yellow)
* Recommended Products:
    * "Recommended for You" heading (H2)
    * 4 product cards (minimal)
    * Simple horizontal scroll
*  19. ORDER HISTORY PAGE (/main_site/account/orders/) Header:
    * "My Orders" heading (H1)
    * Total: "(12 orders)"
* Filters Bar:
    * Status dropdown: "All Orders"
    * Date range: "Last 6 months"
    * Search: "Search orders..."
    * Minimal styling
* Orders List: Each order card:
    * Order number (left, bold): "#12345"
    * Date (left, gray): "March 15, 2026"
    * Status badge (right):
        * Pending: Yellow background
        * Processing: Blue background
        * Shipped: Purple background
        * Delivered: Green background
        * Cancelled: Red background
        * Minimal, flat design
    * Product thumbnails (3-4, 40x40px)
    * Total price (right, bold)
    * Actions:
        * "View Details" button (yellow, flat)
        * "Track Order" button (outline)
        * "Buy Again" button (outline)
        * "Download Invoice" link (yellow)
    * Border: 1px solid #E5E7EB
* Pagination:
    * Simple numbers
    * 10 per page
    * Current: Yellow background
* Empty State:
    * Simple box icon (48px, outline)
    * "No orders yet"
    * "Start shopping"
    * "Browse Products" button (yellow)
*  20. ORDER DETAILS PAGE (/main_site/account/orders//) Header:
    * "Order Details" heading (H1)
    * Order number: "#12345"
    * Status badge (large)
    * Date: "March 15, 2026"
* Order Timeline:
    * Horizontal timeline (minimal):
        * Order Placed: March 15, 10:30 AM ✓ (green)
        * Processing: March 15, 11:00 AM ✓ (green)
        * Shipped: March 16, 2:00 PM (current, yellow)
        * Delivered: Expected March 20 (gray)
    * Simple line, filled to current
    * Minimal design
* Layout: 2 columns Left Column: Shipping Address:
    * "Shipping Address" heading
    * Full address
    * "Edit" link (yellow, if not shipped)
* Payment Method:
    * "Payment Method" heading
    * Card type + last 4 digits
    * Amount charged
* Order Items:
    * "Order Items" heading
    * Product list:
        * Image (80x80px)
        * Name (clickable, yellow hover)
        * Quantity × Price
        * Subtotal
    * "Write Review" button (if delivered, outline)
* Right Column: Order Summary:
    * Subtotal
    * Shipping
    * Tax
    * Discount (if any)
    * Total (large, bold)
    * Border: 1px solid #E5E7EB
* Tracking Info (if shipped):
    * "Tracking Information" heading
    * Carrier: "FedEx"
    * Tracking number: "1234567890" (copyable)
    * "Track Package" button (yellow, flat)
    * Latest update: "In transit - Expected March 20"
* Actions:
    * "Download Invoice" button (outline)
    * "Contact Support" button (outline)
    * "Cancel Order" button (red, if not shipped)
* Order Notes:
    * Customer notes displayed (if any)
*  21. WISHLIST PAGE (/main_site/account/wishlist/) Header:
    * "My Wishlist" heading (H1)
    * Item count: "(23 items)"
    * "Clear All" link (text, red, right)
* Product Grid:
    * 3-4 columns
    * Same as catalog
* Product Card:
    * Product image
    * Heart icon (filled, yellow)
    * Name
    * Price
    * Stock status
    * "Add to Cart" button (yellow, flat)
    * "Remove" button (X, top-right)
    * Border: 1px solid #E5E7EB
    * Hover: Subtle shadow
* Empty State:
    * Heart icon (48px, outline, gray)
    * "Your wishlist is empty"
    * "Save items you love"
    * "Browse Products" button (yellow)
* Actions:
    * "Add All to Cart" button (yellow, if items)
    * "Share Wishlist" link (yellow)
*  22. ACCOUNT SETTINGS PAGE (/main_site/account/settings/) Tabs (horizontal, minimal):
    * Profile
    * Security
    * Notifications
    * Preferences
    * Active: Yellow underline (2px)
* Profile Tab: Avatar Section:
    * Current avatar (96x96px, circular)
    * "Change Photo" button (outline)
    * "Remove Photo" link (red)
* Personal Information:
    * Username (read-only, gray background)
    * Email (editable, verification badge)
    * First name
    * Last name
    * Phone
    * Date of birth (optional)
    * "Save Changes" button (yellow, flat, right)
    * "Cancel" button (outline)
* Success message: "Profile updated" (green, dismissible) Security Tab: Email Verification:
    * Status: "✓ Email verified" (green) or "⚠ Not verified" (orange)
    * "Resend email" button (if not verified)
* Password:
    * "Change Password" button (outline)
    * Last changed: "2 months ago" (gray)
* Two-Factor Authentication:
    * Toggle switch (minimal, yellow when on)
    * "Recommended for security"
    * Setup instructions
* Active Sessions:
    * "Active Sessions" heading
    * List:
        * Device + browser
        * Location
        * Last active
        * "Current session" badge
        * "Sign out" link (red)
* Notifications Tab: Email Preferences:
    * "Email Notifications" heading
    * Toggle switches (minimal, yellow when on):
        * Order updates (always on, disabled)
        * Shipping notifications
        * Promotions
        * New products
        * Price drops
        * Newsletter
    * "Save Preferences" button (yellow, flat)
* Push Notifications:
    * Toggle switch
    * Browser permission
* Preferences Tab: Language:
    * Dropdown: English, Русский, etc.
    * Minimal styling
* Currency:
    * Dropdown: USD, EUR, RUB, etc.
* Theme:
    * Radio buttons: Light, Dark, Auto
    * Minimal design
* Default Shipping:
    * Saved addresses
    * "Set as default" option
    * "Add new" button (outline)
*  🎭 INTERACTIVE ELEMENTS & ANIMATIONS Password Strength Indicator:
    * 3 horizontal bars (equal width, 3px height, 4px gap)
    * States:
        * Weak: 1 red bar
        * Fair: 2 orange bars
        * Good: 3 green bars
    * Smooth transition: 300ms
    * Text below (color-matched)
    * Real-time update
* Password Match Indicator:
    * Text below confirm field
    * Match: "✓ Passwords match" (green)
    * No match: "✗ Do not match" (red)
    * Appears when typing
* Theme Toggle:
    * Simple icon button
    * Sun/Moon icon
    * Smooth transition (fade)
    * Saves to localStorage
* Eye Icon (Password):
    * Position: Right inside input (12px from right)
    * Size: 20px
    * States: Eye / Eye-slash
    * Color: Gray, darker on hover
    * Click: Toggles password visibility
* Product Image Gallery:
    * Main image: 560x560px
    * Thumbnails: 70x70px each, horizontal
    * Active: Yellow border (2px)
    * Hover: Opacity change
    * Click: Instant change (no animation)
    * Hover main: Zoom cursor
    * Click main: Opens lightbox
* Lightbox:
    * Full-screen overlay (black, 90% opacity)
    * Large image (centered, max 85% viewport)
    * Previous/Next arrows (simple, white)
    * Close button (top-right, X, white)
    * Counter: "3 / 8" (bottom, white)
    * Keyboard: Arrows, Escape
    * Click outside: Close
    * Minimal design
* Compatibility Indicator:
    * Icon + Text
    * States:
        * Compatible: ✓ + "Compatible" (green)
        * Warning: ⚠ + "Check compatibility" (orange)
        * Incompatible: ✗ + "Not compatible" (red)
    * Tooltip on hover
* Stock Indicator:
    * Dot + Text
    * States:
        * In Stock: Green dot + "In Stock"
        * Low Stock: Orange dot + "Only 3 left"
        * Out of Stock: Red dot + "Out of Stock"
    * Dot: 6px diameter
* Rating Stars:
    * 5 stars
    * Filled (yellow #FBBF24), Empty (gray #D1D5DB)
    * Size: 16-18px
    * Interactive (for input): Hover fills, click rates
    * Display: Not interactive
* Quantity Selector:
    * 3-part: - | number | +
    * Buttons: 28x28px, bordered
    * Number: 40px width, centered
    * Minus: Disabled if quantity = 1
    * Plus: Disabled if quantity = stock
    * Hover: Background change
    * Minimal styling
* Add to Cart Animation:
    * Product image flies to cart icon (simple)
    * Path: Straight line (0.8s)
    * Cart icon: Bounce
    * Badge: Increment with scale
    * Toast: "Added to cart" (green, 3s)
    * Minimal animation
* Loading States:
    * Spinner: Simple circle, rotating, yellow
    * Size: 20px for buttons, 40px for page
    * Skeleton: Gray boxes (#E5E7EB)
    * No shimmer effect (too decorative)
    * Progress bar: 3px height, yellow fill
* Toast Notifications:
    * Position: Top-right, stacked
    * Size: Max 360px width
    * Types (with left border, 3px):
        * Success: Green border
        * Error: Red border
        * Warning: Orange border
        * Info: Blue border
    * Content: Icon + Message + Close (X)
    * Animation: Slide in from right (250ms)
    * Auto-dismiss: 4 seconds
    * Hover: Pause
    * Minimal design
* Hover Effects:
    * Cards: Subtle shadow increase only
    * Buttons: Opacity 0.9
    * Links: Yellow color
    * Images: No zoom (too decorative)
    * Icons: Opacity change
    * Minimal, subtle
* Click/Active Effects:
    * Buttons: Opacity 0.8
    * Minimal feedback
* Page Transitions:
    * Page load: Simple fade in (400ms)
    * Modals: Fade in (300ms)
    * Drawers: Slide in (300ms)
    * Minimal animations
*  📱 RESPONSIVE DESIGN Breakpoints:
    * Mobile: < 768px
    * Tablet: 768px - 1024px
    * Desktop: > 1024px
* Mobile (<768px):
    * Navigation: Hamburger + logo + cart
    * Drawer menu: Slides from left
    * Product grid: 1-2 columns
    * Sidebar filters: Bottom drawer
    * Forms: Full-width, larger touch targets (44px min)
    * Tables: Card layout
    * Footer: Stacked (1 column)
    * Modals: Full-screen
    * Font sizes: Slightly larger
* Tablet (768px - 1024px):
    * Product grid: 2-3 columns
    * Sidebar: Collapsible
    * Navigation: Full menu
    * Footer: 2 columns
* Touch:
    * Min touch target: 44x44px
    * Swipe: Image galleries
    * Minimal gestures
*  ♿ ACCESSIBILITY Focus States:
    * All interactive: 2px yellow ring
    * Offset: 2px
    * Visible on Tab
    * Skip to main content link
* Color Contrast:
    * WCAG AA: 4.5:1 minimum
    * Large text (18px+): 3:1
    * Interactive: 3:1
* Screen Reader:
    * Icons: aria-labels
    * Images: alt text
    * Form labels: Visible and associated
    * Errors: Announced
    * Loading: aria-live
    * Modals: Focus trap, Escape closes
* Keyboard:
    * Tab order: Logical
    * Enter/Space: Activate
    * Arrows: Navigate
    * Escape: Close
    * Focus: Always visible
* ARIA:
    * aria-label: Icon buttons
    * aria-describedby: Field hints
    * aria-invalid: Validation errors
    * aria-expanded: Accordions
    * aria-current: Active nav
    * role: Custom components
*  🎬 ANIMATION TIMING Duration:
    * Micro: 150-200ms (hover, click)
    * UI: 250-350ms (modals, drawers)
    * Page: 400ms (page load)
    * Complex: 800ms (add to cart)
* Easing:
    * ease-out: Entering
    * ease-in: Exiting
    * ease-in-out: Transitions
* Performance:
    * Use transform and opacity
    * Avoid width, height, top, left
    * Use will-change sparingly
    * Respect prefers-reduced-motion
*  📦 REUSABLE COMPONENTS Create master components:
    * Buttons: Primary (yellow), Secondary (outline), Text, Icon, Loading, Disabled
    * Inputs: Text, Email, Password (with toggle), Number, Textarea, Search
    * Dropdowns: Select, Multi-select
    * Checkboxes & Radio: Checked, Unchecked, Disabled
    * Toggle Switches: On (yellow), Off, Disabled
    * Cards: Product, Configuration, Order, Review
    * Badges: Status, Stock, Category
    * Modals: Small (360px), Medium (560px), Large (760px), Full-screen
    * Tabs: Horizontal, Underline (yellow)
    * Accordions: Collapsed, Expanded
    * Breadcrumbs: With separators, Yellow links
    * Pagination: Numbers, Prev/Next
    * Rating Stars: Display, Interactive
    * Progress Bars: Linear (yellow), Stepped
    * Tooltips: Top, Bottom, Left, Right
    * Alerts/Toasts: Success, Error, Warning, Info
    * Avatars: Circular, Square, Placeholder
    * Skeleton Loaders: Text, Image, Card
    * Empty States: No results, No items, Error
    * Icons: Outline style, consistent size
* Variants:
    * Size: Small, Medium, Large
    * State: Default, Hover, Active, Disabled, Loading
    * Theme: Light, Dark
    * Color: Primary (yellow), Secondary, Success, Warning, Error
*  🎯 KEY USER FLOWS Flow 1: Registration
    * Home → "Sign Up"
    * Registration page → Fill form
    * Password strength updates real-time
    * Confirm password shows match
    * Submit → Email confirmation page
    * Check email → Click link
    * Email confirmed → Login
    * Dashboard
* Flow 2: Build PC
    * Home → "Start Building"
    * Configurator page
    * "Choose Processor" → Modal
    * Filter/search → Select
    * Modal closes, added
    * Repeat for all components
    * Right panel shows:
        * Compatibility (green/orange/red)
        * Power calculation (progress bar)
        * Total price (real-time)
    * "Add to Cart"
    * Cart → Checkout → Order
* Flow 3: Buy Laptop
    * Home → "Browse Laptops"
    * Catalog → Apply filters
    * Grid updates
    * Click product → Detail page
    * View images (gallery)
    * Read reviews, specs
    * Select quantity
    * "Add to Cart"
    * Cart → Checkout → Confirmation
* Flow 4: AI Consultation
    * Any page → See floating button (bottom-right)
    * Click → Chat modal slides up
    * Welcome + suggested questions
    * Click suggestion OR type
    * AI responds with recommendations
    * AI suggests products (clickable cards)
    * Click card → Opens in new tab
    * Return → Chat still open
    * Continue or minimize
    * If on configurator → Build-specific advice
    * Close → Button remains
* Flow 5: Order Tracking
    * Dashboard → "Orders"
    * Order history → Click order
    * Order details → View timeline
    * "Track Package" → Carrier site
    * Return → Download invoice
*  📝 FIGMA DESIGN NOTES
    * Master Components for all reusable elements
    * Auto Layout for responsive components
    * Component Variants for states
    * Organization:
        * Page 1: Colors, typography, spacing
        * Page 2: Icons (outline style)
        * Page 3: Component library
        * Page 4+: Page designs
    * Prototyping: Link pages for flows
    * Dark Mode: Use Figma variables
    * Mobile Versions: Key pages
    * Component States: All states
    * Empty States: All scenarios
    * Error States: Validation, 404, network
    * Loading States: Skeletons
    * Success States: Confirmations
    * Annotations: Interactions, logic
    * Spacing: 4px base (4, 8, 12, 16, 24, 32, 48)
    * Grid: 12-column, 24px gutters, 1000px max-width
*  🎨 MINIMALIST STYLE GUIDELINES Visual Style:
    * Clean, simple, functional
    * Generous white space
    * Clear hierarchy
    * Consistent spacing
    * Subtle shadows (minimal)
    * Small rounded corners (6-8px)
    * Professional and straightforward
* Imagery:
    * High-quality product photos
    * Consistent backgrounds (white/light gray)
    * Multiple angles (ProductImage model)
    * Icons: Outline style, 1.5-2px stroke
* Micro-interactions:
    * Minimal button feedback
    * Subtle hover states
    * Simple loading indicators
    * Clear success/error feedback
    * Smooth but quick transitions
* Content Tone:
    * Clear, concise
    * Technical when needed
    * Friendly but professional
    * Reassuring
*  🔄 SPECIAL FEATURES Multiple Product Images Every product: 4-8+ images via ProductImage model
    * Main image (is_main=true)
    * Additional angles
    * Detail shots
    * Packaging
    * In-use photos
* Design:
    * Detail page: Large main + thumbnail gallery
    * Thumbnails: 70x70px, scrollable
    * Click: Instant change
    * Hover main: Zoom cursor
    * Click main: Lightbox with carousel
    * Mobile: Swipe gallery
* Compatibility Checking Visual indicators:
    * Configurator: Real-time panel
    * Component modal: Badge on each
    * Product detail: "Check compatibility" button
    * Color-coded: Green/Orange/Red
* Issues:
    * ⚠️ Socket mismatch
    * ⚠️ RAM type mismatch
    * ⚠️ Insufficient PSU
    * ⚠️ GPU too long
    * ⚠️ Motherboard doesn't fit
* Power Calculation Visual:
    * Total power: Large number + "W"
    * Recommended PSU: With 25% overhead
    * Progress bar: Current / Recommended
    * Color: Green/Orange/Red
    * Breakdown: Per component (expandable)
* AI Chat Consultant Conversational:
    * Natural language
    * Context-aware
    * Product recommendations in chat
    * Configuration suggestions
    * Clickable product cards
    * Typing indicator
    * Chat history
    * Floating widget (bottom-right)
* Price Calculator Real-time:
    * Components add automatically
    * Subtotal, tax, total
    * Discount codes
    * Shipping at checkout
    * Currency formatting
*  🌐 FOOTER (EVERY PAGE) Layout: 4 columns desktop, stacked mobile Column 1: About (25%)
    * "BuildBox" logo (smaller, yellow + gray)
    * Tagline: "Build your dream PC with confidence"
    * Description: "Expert guidance, compatibility checking, and best prices."
    * Social icons (simple, 24x24px):
        * Facebook, Twitter, Instagram, YouTube
        * Outline style, no backgrounds
        * Hover: Yellow color
* Column 2: Quick Links (25%)
    * "Quick Links" heading
    * Links:
        * Home
        * Browse Components
        * Laptops
        * PC Configurator
        * About Us
        * Contact
    * Hover: Yellow color
* Column 3: Customer Service (25%)
    * "Customer Service" heading
    * Links:
        * Contact Us
        * Shipping Info
        * Returns & Refunds
        * FAQ
        * Track Order
        * Support
    * Hover: Yellow color
* Column 4: Contact (25%)
    * "Stay Connected" heading
    * Contact:
        * Email: support@buildbox.com
        * Phone: +1 (555) 123-4567
        * Address: 123 Tech Street, Silicon Valley, CA
* Bottom Bar:
    * Divider (1px, #E5E7EB)
    * 3 sections:
        * Left: Copyright © 2026 BuildBox
* 	•	Center: Payment icons (grayscale, 32x20px)
* Right: Privacy Policy | Terms of Service
* Footer Styling:
* Background: #F9FAFB (light), #111827 (dark)
* Text: #6B7280
* Links: #6B7280, hover: #FBBF24
* Padding: 48px top/bottom, 24px left/right
* Spacing: 32px between columns
* Mobile: Stack, 24px spacing
* Minimal design
* Footer Animations:
* Links: Color transition (200ms)
* Social icons: Opacity change on hover
* Minimal effects
* 
* 📊 DATA VISUALIZATION
* Rating Distribution:
* 5 horizontal bars (one per star)
* Bar width: Percentage
* Color: Yellow #FBBF24
* Label: "5 stars (80%)" + count
* Power Progress Bar:
* Horizontal, rounded ends
* Fill: Green/Orange/Red
* Label: "450W / 650W recommended"
* Percentage: 69%
* Minimal styling
* Order Timeline:
* Horizontal stepper
* 4 steps: Placed → Processing → Shipped → Delivered
* Completed: Green checkmark
* Current: Yellow circle
* Future: Gray circle
* Simple line connecting
* Stock Level:
* Dot + text
* Color-coded: Green/Orange/Red
* Simple, minimal
* 
* 🎯 CONVERSION OPTIMIZATION
* Trust Signals:
* Security badges: SSL, Money-back
* Payment icons: Visa, Mastercard, PayPal
* Reviews: Star ratings, count
* "Verified Purchase" badges
* "Free shipping over $1000"
* "30-day return policy"
* Urgency:
* "Only 3 left" (orange)
* "Sale ends in 2 days" (optional)
* "Limited time" badge
* Social Proof:
* "127 reviews" with stars
* "Recommended by experts"
* CTA Optimization:
* Primary buttons: High contrast, large, clear
* "Add to Cart" always visible
* Clear next steps
* Minimal design
* 
* 🔍 SEARCH & FILTER
* Search Bar:
* Center of navigation
* Width: 400-500px desktop
* Placeholder: "Search products..."
* Search icon (left)
* Clear button (right, when typing)
* Autocomplete dropdown:
    * Recent searches
    * Suggested products (with images)
    * Categories
* Minimal styling
* Filter Sidebar:
* Collapsible sections
* Checkboxes for multiple
* Radio for single
* Range sliders (yellow accent)
* "Apply Filters" button (sticky)
* "Clear All" link (yellow)
* Active filter count badge
* Sort Options:
* Dropdown: "Sort by: Relevance"
* Options: Price, Name, Newest, Rating
* Minimal styling
* Search Results:
* Results count: "48 products"
* Active filters as removable chips (yellow)
* "No results" state with suggestions
* 
* 🎨 FINAL CHECKLIST
* ✅ Completeness:
* All pages designed
* All component states
* Light and dark themes
* Mobile versions
* Empty and error states
* ✅ Consistency:
* Yellow #FBBF24 primary color
* Dark gray #1F2937 + white accents
* Typography scale (Inter/Roboto)
* Spacing system (4px base)
* Outline icons (1.5-2px stroke)
* Border radius (6-8px)
* Minimal shadows
* ✅ Minimalism:
* Clean, simple forms
* Generous white space
* Subtle borders (1px)
* Flat design (no heavy shadows)
* Minimal decoration
* Focus on content and functionality
* ✅ Accessibility:
* Color contrast WCAG AA
* Focus states visible (yellow ring)
* Touch targets 44x44px minimum
* Text readable (15-16px body)
* ✅ Functionality:
* All interactive elements clear
* Form validation states
* Loading states
* Success/error feedback
* Navigation intuitive
* ✅ Branding:
* Text-only logo "BuildBox" (yellow + gray)
* Yellow color prominent
* Minimalist style consistent
* Professional tone
* ✅ Data Structure:
* All models represented
* Multiple product images (ProductImage)
* Relationships clear
* Computed fields displayed
* ✅ Footer:
* Appears on every page
* All required information
* Responsive
* Minimal design
* ✅ AI Consultant:
* Floating button (bottom-right, all pages)
* Modal widget (380x600px)
* Chat interface (minimal)
* Product recommendations
* Context-aware
* 
* 🚀 DELIVERABLES
* Figma File Structure:
* Cover: Title, description, version, date
* Design System: Colors (yellow theme), typography, spacing, icons (outline)
* Components: Master components with variants (minimal style)
* Authentication: Login, register, forgot, reset, change, email confirmation
* Main Pages: Home, catalog, product detail, laptops
* Configurator: PC builder, component modal, saved configs
* AI Consultant: Chat widget modal (bottom-right floating)
* Shopping: Cart, checkout, order confirmation
* Account: Dashboard, orders, order detail, wishlist, settings
* Mobile Versions: Key pages
* States: Loading, empty, error
* Prototype: Linked pages showing flows
* Export Assets:
* Logo (text-only, SVG)
* Icons (outline style, SVG)
* Product placeholders
* Style guide PDF (optional)
* 
* 💡 ADDITIONAL RECOMMENDATIONS
* Performance:
* Optimize images (WebP, lazy loading)
* Minimize animations
* Progressive loading
* Skeleton screens
* Future Enhancements:
* 3D product viewer
* AR preview
* Build guides
* Community builds
* Price history charts
* Component comparison
* Compatibility score (0-100)
* Performance benchmarks
* Localization:
* Text in separate layers
* RTL support consideration
* Date/time format flexibility
* Currency symbol placement
* Number formatting
* 
* 🎯 SUCCESS METRICS
* Conversion:
* Clear CTAs
* Minimal friction
* Trust signals
* Comprehensive info
* Engagement:
* AI chat accessible (floating button)
* Configurator intuitive
* Product discovery easy
* Wishlist and save features
* Retention:
* Dashboard useful
* Order tracking clear
* Saved configurations
* Personalized recommendations
* Trust:
* Professional minimalist design
* Security indicators
* Clear policies
* Responsive support
* 
* 📋 SUMMARY
* Complete design brief covers:
* Minimalist brand identity (text-only logo)
* Yellow #FBBF24 + dark gray #1F2937 color system
* All database models with detailed fields
* 22+ page designs with minimal specifications
* Multiple product images system (ProductImage model)
* AI Consultant as floating modal widget (bottom-right)
* Footer design on every page
* Interactive elements (minimal animations)
* Responsive design for all devices
* Accessibility guidelines
* User flows and prototyping
* Reusable component library (minimal style)
* Key Features:
* Multiple product photos (4-8+ per product)
* Real-time compatibility checking
* Power consumption calculator
* AI chat consultant (floating widget)
* PC configurator with live updates
* Comprehensive footer on all pages
* Text-only logo (no icon required)
* Minimalist yellow theme
* Design Philosophy: Clean, minimalist, functional interface that makes PC building accessible to everyone while providing expert-level tools. Focus on simplicity, clarity, and seamless user experience with yellow accent color and minimal decoration.
* 
* END OF DESIGN BRIEF

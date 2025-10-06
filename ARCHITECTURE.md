## Architecture and Design Decisions

This project is a small Django 5.2 application that demonstrates a simple shop with authentication, products, and a cart.

### Apps overview

- `products`: Product catalog (CRUD for staff), category filtering, search, list/detail views.
- `cart`: Per-user shopping cart with `Cart` and `CartItem` models, plus a signal to auto-create a cart on user creation.
- `accounts`: Authentication URLs (login, logout, signup) using Django auth views and a minimal signup view.

### Data model

- `products.Category`: Name/slug/description with plural verbose name and name ordering. Exposes `get_absolute_url()` to filter by category via querystring.
- `products.Product`: Basic catalog fields, optional image, stock, and M2M to categories. Ordered by `created_at` desc.
- `cart.Cart`: One-to-one with `auth.User` to keep a single cart per user, with computed totals.
- `cart.CartItem`: Links a product to a cart with a quantity and computed subtotal.

Rationale:
- Keeping `Cart` as 1-1 with user simplifies access patterns and eliminates the need for anonymous cart merging in this demo.
- Totals are computed on the fly for clarity; denormalization is unnecessary at this scale.

### Views and access control

- `products.ProductListView`: Authenticated list with search (`q`) and category filter (`category`), prefetching categories for efficiency.
- `products.ProductDetailView`: Authenticated product detail.
- `products.ProductAdminListView`/`CreateView`/`UpdateView`/`DeleteView`: Staff-only management via `AdminRequiredMixin`.
- `accounts.SignUpView`: Simple `CreateView` using `UserCreationForm` with redirect to login.

Auth decisions:
- All product pages require authentication (`LoginRequiredMixin`). This keeps the example focused on signed-in flows.
- Admin-only actions use a dedicated `AdminRequiredMixin` that redirects anonymous users to login and returns 403 for non-staff.

### Templates and UI

- A single `base.html` provides Tailwind via CDN for quick UI without a build step.
- Navbar exposes product list, cart, and auth actions; shows username and admin link for staff.
- Logout uses a POST form in the navbar (Django 5+ security requirement). Visiting `/accounts/logout/` by GET renders `templates/registration/logout.html` as a confirmation page with a POST button; after logout, users are redirected to the product list.

### URLs and routing

- Root (`/`) maps to `products:product_list`.
- `accounts/` includes login/logout/signup. Logout uses Django's `LogoutView` with `LOGOUT_REDIRECT_URL` set to the product list.
- `cart/` exposes cart detail and actions (see app URLs/views).

### Persistence and configuration

- MySQL via PyMySQL is configured in `config/__init__.py` and `settings.py`. Credentials are provided via `.env` loaded with `python-dotenv`.
- Media files are served via `MEDIA_URL`/`MEDIA_ROOT` in development.

### Signals

- `cart.signals.create_user_cart`: Automatically creates a `Cart` for each newly created `User`. This simplifies cart usage throughout the app.

### Scalability and future extensions

- For higher traffic, consider caching product lists and category filters, and introducing pagination (already present) with database indexes on `Product(stock, created_at)` and `Category.slug`.
- Cart totals could be denormalized for very large carts or frequent access patterns.
- Public catalog access can be enabled by removing `LoginRequiredMixin` on list/detail and adding rate limiting/CSRF protections where appropriate.



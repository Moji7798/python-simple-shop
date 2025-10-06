## Shop Task - Django Project

Simple e-commerce demo built with Django 5.2, MySQL, and Tailwind (via CDN).

### Prerequisites

- Python 3.11+ (recommended)
- MySQL 8.x (server and client)
- Git

### 1) Clone and enter the project

```bash
git clone <your-fork-or-repo-url>
cd shop-task
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows: .venv\\Scripts\\activate
```

### 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Create MySQL database and user

Login to MySQL and run:

```sql
CREATE DATABASE shop_task CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON shop_task.* TO 'shop_user'@'localhost';
FLUSH PRIVILEGES;
```

Notes:
- The project uses PyMySQL (configured in `config/__init__.py`). No extra system driver is required.

### 5) Configure environment variables

Create a file named `.env` in the project root with values matching your database:

```bash
SECRET_KEY=dev-secret-change-me
DEBUG=True

DB_NAME=shop_task
DB_USER=shop_user
DB_PASSWORD=strong_password_here
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6) Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7) Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

### Useful URLs

- Product list (home): `/`
- Admin: `/admin/`
- Cart: `/cart/`
- Sign up: `/accounts/signup/`
- Login: `/accounts/login/`
- Logout: `/accounts/logout/`

Logout security note (Django 5+): Logout requires a POST request. The navbar uses a POST form already. Visiting `/accounts/logout/` via GET shows a confirmation page with a POST button.

### Static and media

- Tailwind is loaded via CDN in `templates/base.html`; no build step is needed for development.
- User-uploaded files (if any) are served from `media/` when `DEBUG=True`.

### Troubleshooting

- 405 Method Not Allowed on logout: Ensure you use the navbar logout button (POST). Direct GET to `/accounts/logout/` will show a confirmation page.
- Database connection errors: Verify `.env` credentials and that MySQL is running, and the user has privileges on `shop_task`.



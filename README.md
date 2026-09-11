# CodeAlpha_EcommerceStore

A full-stack e-commerce store built with **Django** for the **CodeAlpha Full Stack Development Internship - Task 1**.

## Features

- Product listing with category filter and search
- Product detail pages with product images
- Session-based shopping cart (add/remove/update)
- User registration and login using Django authentication
- Checkout and order processing
- Order and order-item persistence in the database
- Automatic stock decrement after successful order placement
- Order history for logged-in users
- Django admin for managing products, categories, and orders
- Product image upload and management

## Tech Stack

- **Backend:** Django 6.1, Python
- **Frontend:** Django Templates, HTML, CSS, Vanilla JavaScript
- **Database:** SQLite (default; can be configured for PostgreSQL/MySQL)
- **Image Processing:** Pillow
- **Authentication:** Django Authentication System
- **Storage:** Django Media Files

## Project Structure

```text
ecommerce_project/   # Django project settings and root URLs
store/               # Main application: models, views, cart, orders, templates
static/              # CSS and JavaScript assets
media/products/      # Uploaded product images
requirements.txt     # Python dependencies
manage.py             # Django management utility
```

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/ashutosh-chauhan-dev/CodeAlpha_EcommerceStore.git
cd CodeAlpha_EcommerceStore
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Django secret key

Set the `DJANGO_SECRET_KEY` environment variable before running the project. Do not commit secret keys to GitHub.

Example:

```powershell
$env:DJANGO_SECRET_KEY = 'your-generated-secret-key'
```

### 5. Run database migrations

```powershell
python manage.py migrate
```

### 6. Load sample products

```powershell
python manage.py seed_data
```

### 7. Create an admin account

```powershell
python manage.py createsuperuser
```

### 8. Start the development server

```powershell
python manage.py runserver
```

Open the store at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

## Adding Products

Log in to the Django admin panel, create categories first, then add products with an image, price, and stock quantity.

## Notes

- This project uses SQLite for simple local development.
- Product images are stored in `media/products/` and are excluded from Git.
- `db.sqlite3` is excluded from Git.
- The virtual environment is excluded from Git.
- `DEBUG=True` is intended for local development only.
- Never commit `DJANGO_SECRET_KEY` or other secrets to the repository.

## Verification

Before publishing the project, run:

```powershell
python manage.py check
python manage.py makemigrations --check
```

Both commands should complete without errors.

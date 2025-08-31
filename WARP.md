# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Simply Calories is a Django web application for tracking calorie consumption. It features:

- User authentication with language preference support (English/Polish)
- Daily calorie entry tracking with an optional calculator feature
- Dashboard with today's entries and quick-add functionality
- Full CRUD operations for consumption entries
- Internationalization support with custom middleware for user language preferences

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Navigate to the Django app directory
cd app/

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test ModelTests
python manage.py test AuthFlowTests
python manage.py test EntryViewsTests

# Run tests with verbose output
python manage.py test --verbosity=2
```

### Database Management
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reset database (SQLite only - deletes db.sqlite3)
rm db.sqlite3
python manage.py migrate
```

### Django Admin
```bash
# Access admin interface at /admin/
# Create superuser first: python manage.py createsuperuser
```

## Architecture

### Project Structure
```
app/                          # Main Django project directory
├── manage.py                # Django management script
├── app/                     # Project settings package
│   ├── settings.py          # Main settings (SECRET_KEY, DATABASES, etc.)
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI application
├── accounts/               # User authentication app
│   ├── models.py           # UserProfile with language preferences
│   ├── views.py            # Signup, language switching
│   ├── forms.py            # Custom signup form
│   ├── middleware.py       # UserLanguageMiddleware
│   └── urls.py             # Auth-related URLs
├── tracker/                # Core calorie tracking app
│   ├── models.py           # ConsumptionEntry model
│   ├── views.py            # Dashboard, CRUD views
│   ├── forms.py            # ConsumptionEntryForm
│   └── urls.py             # Tracker URLs
├── templates/              # Django templates
│   ├── base.html           # Base template with Bootstrap + calculator JS
│   ├── accounts/           # Auth templates
│   └── tracker/            # Tracker templates
└── tests.py               # Centralized test file
```

### Key Models

**accounts.UserProfile**
- Extends Django User with `preferred_language` field
- Auto-created via post_save signals
- Supports English/Polish language switching

**tracker.ConsumptionEntry**
- Core model: `user`, `name`, `calories`, `date`, `quantity_g`
- Indexed on `user + date` for performance
- Defaults to today's date

### URL Routing
- Root (`/`) → tracker.dashboard (login required)
- `/accounts/` → Authentication (signup, login, logout, language)
- `/entries/` → Full entries list with pagination
- `/entries/add/`, `/entries/<id>/edit/`, `/entries/<id>/delete/` → CRUD operations
- `/admin/` → Django admin interface

### Special Features

**Calculator Integration**
- JavaScript-based arithmetic calculator in calorie input fields
- Supports expressions like `100*2+50`, `(100+200)/2`
- Real-time preview of calculated results
- Auto-replacement on blur with calculated value
- Located in `base.html` template and `test_calculator.html`

**Internationalization**
- Built-in support for English and Polish
- Custom `UserLanguageMiddleware` respects user preferences
- Language switcher in navigation bar
- All user-facing strings wrapped with `{% trans %}` tags

**Authentication Flow**
- Custom signup form with Bootstrap styling
- Automatic login after successful signup
- Redirects to dashboard after login
- User-specific entry filtering throughout the app

### Database Configuration
- Uses SQLite3 by default (`app/db.sqlite3`)
- User sessions and CSRF middleware enabled
- Custom `DEFAULT_AUTO_FIELD` set to `BigAutoField`

### Frontend Stack
- Bootstrap 5.3.3 for styling
- Bootstrap Icons for UI elements
- Custom CSS for calculator functionality
- No build process required - all assets loaded via CDN

## Testing Strategy

The application includes comprehensive tests covering:
- Model creation and validation (`ModelTests`)
- Authentication flow (`AuthFlowTests`) 
- Entry CRUD operations and totals calculation (`EntryViewsTests`)

Tests use Django's built-in TestCase with SQLite in-memory database.

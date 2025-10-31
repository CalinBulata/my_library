# AI Agent Instructions for my_library

This document provides essential context for AI agents working with the my_library codebase.

## Project Overview

This is a Django-based library management system with the following structure:
- `my_library/` - Core project configuration
- `loans/` - Main application for handling library loan functionality

## Architecture & Components

### Core Components
- **Project Settings**: `my_library/settings.py` contains Django configuration
- **URL Routing**: `my_library/urls.py` defines the main URL patterns
- **Loans App**: Handles library loan management through `loans/` directory
  - Views in `loans/views.py`
  - Templates in `loans/templates/`
  - Models in `loans/models.py`

### Development Setup

1. Project uses Django 5.2.x
2. Database is SQLite3 (`db.sqlite3`)
3. Debug mode is enabled in development

### Key Workflows

#### Running the Development Server
```bash
python manage.py runserver
```

#### Database Migrations
When modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Conventions & Patterns

### View Structure
- Views are function-based (see `loans/views.py`)
- Context dictionaries are used for template data
- Templates are stored in app-specific template directories

### URL Patterns
- URLs are defined in `my_library/urls.py`
- Current routes:
  - `/welcome/` - Welcome page
  - `/admin/` - Django admin interface

### Templates
- Located in `loans/templates/`
- Use Django's template language
- Example: `welcome.html` demonstrates basic template usage

## Testing
Use Django's test framework:
```bash
python manage.py test
```

Test files are located in `loans/tests.py`
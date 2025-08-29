# README.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST Framework backend for a gaming center management system called "sisgame-backend". The system manages gaming devices, customer sessions, sales, inventory, and maintenance operations for a gaming business.

## Architecture

### Core Django App
- **Main app**: `gamecenter` - Contains all business logic, models, views, and API endpoints
- **Django project**: `gamecenter_service` - Contains settings, URL configuration, and WSGI/ASGI setup

### Key Models Structure
The system revolves around these main entities:
- **Product/ProductDevices**: Gaming devices (consoles, PCs) with unique codes
- **Person**: Users, clients, and staff members
- **Session/SessionLots**: Gaming sessions with device usage tracking
- **Sale/SaleDetail**: Sales transactions and inventory movement
- **Lots**: Inventory management with stock tracking
- **ProductMaintenance**: Device maintenance records

### API Architecture
- Uses Django REST Framework with ViewSets
- All endpoints registered in `gamecenter/router.py`
- API base URL: `/gamecenter/`
- Follows REST conventions with automatic CRUD operations

## Development Commands

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser
```

### Data Seeding
```bash
# Run all seeding commands at once
python manage.py run_all_seeds

# Individual seeding commands
python manage.py seed_basic      # Basic data (categories, settings)
python manage.py seed_data       # Core business data
python manage.py seed_gaming     # Gaming-specific data

# Show current data summary
python manage.py show_data
```

### Server
```bash
# Run development server
python manage.py runserver
```

## Environment Configuration

The project uses `django-environ` for configuration management:
- Database settings are loaded from `.env` file
- Required environment variables:
  - `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Key Business Logic

### Device Status Management
- Located in `gamecenter/actions/sessions/DivicesList.py`
- Function `get_devices_status()` provides real-time status of all gaming devices
- Status types: "available", "in_use", "maintenance"
- Integrates with sessions and maintenance records

### Session Management
- Sessions track device usage with start/end times and costs
- Uses `SessionLots` as intermediary for device-session relationships
- Supports both paid and free sessions

### Inventory & Sales
- `Lots` model handles stock management with expiration dates
- Sales system supports multiple payment methods
- Box management tracks daily cash operations

## File Structure Notes

### Views & Serializers
- Views are organized in separate files in `gamecenter/views/`
- Serializers are in `gamecenter/serializers/`
- Both imported via `__init__.py` files

### Management Commands
- Custom Django commands in `gamecenter/management/commands/`
- Use for data seeding and administrative tasks

### Actions
- Business logic functions in `gamecenter/actions/`
- Currently contains device status functionality

## Database
- Uses PostgreSQL (via psycopg2-binary)
- All models inherit from `TimeStampedModel` for automatic timestamps
- Extensive use of foreign key relationships and proper indexing

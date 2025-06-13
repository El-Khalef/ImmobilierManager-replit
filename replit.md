# Replit.md - Système de Gestion Immobilière

## Overview

This is a comprehensive real estate management system built for property management in Mauritania. The application manages properties, clients (owners and tenants), rental contracts, rent payments, and generates PDF receipts. It's designed specifically for the Mauritanian market with support for Ouguiya (MRU) currency and French language interface.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Database Models**: Declarative base using SQLAlchemy 2.0+
- **WSGI Server**: Gunicorn for production deployment
- **Form Handling**: Flask-WTF with WTForms for form validation
- **Authentication**: Session-based using Flask's built-in session management

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **CSS Framework**: Bootstrap (dark theme variant)
- **Icons**: Font Awesome
- **JavaScript**: Minimal vanilla JS for dynamic interactions
- **Responsive Design**: Mobile-first Bootstrap responsive grid

### Database Schema
The system uses a relational database with the following main entities:
- **Clients**: Property owners, tenants, and buyers with identity document validation
- **Properties** (biens_immobiliers): Real estate assets with location coordinates
- **Rental Contracts** (contrats_location): Agreements between owners and tenants
- **Rent Payments** (paiements_loyer): Monthly payment tracking
- **Documents**: File attachments for contracts
- **Photos**: Property images with primary photo designation

## Key Components

### Core Models (models.py)
- Client management with different types (proprietaire, locataire, acheteur)
- Property management with detailed specifications and GPS coordinates
- Contract lifecycle management
- Payment tracking with status management
- Document and photo associations

### Route Handlers (routes.py)
- RESTful routing pattern with proper HTTP methods
- Form validation and error handling
- File upload management for documents and photos
- PDF generation endpoints for receipts
- Dashboard with real-time statistics

### Form Management (forms.py)
- WTForms integration with server-side validation
- Dynamic form fields based on user selections
- File upload forms with size and type restrictions
- Search and filter forms

### PDF Generation (quittances.py, quittances_template.py)
- ReportLab-based PDF generation for rent receipts
- Template-based PDF overlay system
- Bilingual support (French/Arabic) preparation
- Position calibration tools for precise layout

## Data Flow

1. **Property Registration**: Owners register properties with detailed specifications
2. **Client Management**: Both property owners and tenants are managed as clients
3. **Contract Creation**: Rental agreements link properties with tenants
4. **Payment Processing**: Monthly rent payments are recorded and tracked
5. **Receipt Generation**: PDF receipts are generated for completed payments
6. **Document Management**: Supporting documents are attached to contracts

## External Dependencies

### Python Packages
- Flask 3.1.1+ (web framework)
- Flask-SQLAlchemy 3.1.1+ (database ORM)
- Flask-WTF 1.2.2+ (form handling)
- psycopg2-binary 2.9.10+ (PostgreSQL adapter)
- ReportLab 4.4.1+ (PDF generation)
- Gunicorn 23.0.0+ (WSGI server)
- python-dateutil 2.9.0+ (date manipulation)

### Optional Services
- SendGrid (email notifications)
- Twilio (SMS notifications)

### Database
- PostgreSQL 16+ (primary database)
- Connection pooling enabled with pool_recycle=300

## Deployment Strategy

### Development Environment
- Uses Replit's Python 3.11 environment
- PostgreSQL 16 provided by Replit
- Environment variables for configuration
- File uploads stored in static/uploads directory

### Production Configuration
- Gunicorn with autoscale deployment target
- ProxyFix middleware for HTTPS support
- Session cookie security settings
- File upload size limits (16MB)
- Upload directory auto-creation

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Flask session encryption key
- `SENDGRID_API_KEY`: Email service API key (optional)
- `TWILIO_*`: SMS service credentials (optional)

### File Structure
```
/
├── app.py              # Flask application factory
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Route handlers
├── forms.py            # WTForms definitions
├── quittances.py       # PDF generation
├── static/             # Static assets
│   ├── uploads/        # Property photos
│   └── documents/      # Contract documents
└── templates/          # Jinja2 templates
    ├── base.html       # Base template
    ├── dashboard.html  # Main dashboard
    └── [modules]/      # Feature-specific templates
```

## Changelog

Changelog:
- June 13, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.
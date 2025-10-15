# Restaurant Menu Management System

A full-stack system that automates restaurant menu processing, from PDF extraction to AI-powered data structuring and database integration.  

Built with Django, MySQL, and Next.js, the platform allows administrators to upload restaurant menus, automatically extract content using AI, and manage structured menu data through a web interface.

---

## My Contributions

This project was developed as a group effort. My main responsibility was designing and implementing the **backend ETL pipeline** that powers the AI-driven menu processing system:

1. **Extract (Data Ingestion)**
   - Developed `PDFreader.py` using PyMuPDF to extract and clean text from uploaded restaurant menu PDFs.
   - Implemented robust error handling for corrupted, empty, or image-only files.

2. **Transform (AI Structuring)**
   - Built `AIreader.py` to send extracted text to Anthropic Claude and receive structured JSON output.
   - Designed and tuned prompt engineering logic to convert unstructured text into normalized, ready-to-ingest data.

3. **Load (Database Integration)**
   - Designed and implemented the MySQL database schema covering restaurants, menus, and menu items.
   - Connected Django models to the schema and implemented logic to insert and validate AI-generated JSON data.

4. **Testing**
   - Added backend tests covering models, relationships, and endpoints.
   - Verified data integrity and workflow correctness using `pytest` and `pytest-django`.

---

## Features

- CRUD operations for restaurant menus and items  
- Automatic PDF text extraction using PyMuPDF  
- AI-based text structuring via Anthropic Claude  
- Cleaned and validated JSON-to-database ingestion  
- SQL materialized views for aggregated insights  
- Responsive frontend built with Next.js and TailwindCSS  
- Django admin panel enhanced with Django Unfold  

---

## Technologies Used

### Backend
- Django & Django REST Framework  
- MySQL  
- PyMuPDF  
- Anthropic Claude API  
- python-dotenv  
- pytest & pytest-django  

### Frontend
- Next.js (React)
- TailwindCSS
- shadcn-ui
- React Query

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/restaurant-menu-management-system.git
cd restaurant-menu-management-system
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory:
```bash
cd backend
```

Create `.env` with the following content:
```env
# Django
DJANGO_SECRET_KEY=your-django-secret-key-here

# Anthropic Claude API
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Database
DB_NAME=restaurant_menus
DB_USER=root
DB_PASSWORD=your-mysql-password-here
DB_HOST=localhost
DB_PORT=3306
```

#### Run Database Migrations
```bash
python manage.py migrate
```

#### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### Start Backend Server
```bash
python manage.py runserver
```

The backend will be available at `http://127.0.0.1:8000/`

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend/db-app
npm install
```

#### Start Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000/`

## Running Tests

### Backend Tests

Navigate to the backend directory:
```bash
cd backend
```

#### Run All Tests
```bash
pytest
```

#### Run Tests with Verbose Output
```bash
pytest -v
```

#### Run Specific Test Files
```bash
# Model tests
pytest tests/test_models.py -v

# API tests
pytest tests/test_api.py -v

# Upload tests
pytest tests/test_upload.py -v
```


## Database Schema

- **Restaurant:** name, location  
- **Menu:** restaurant, version, date  
- **MenuSection:** menu, section_name, section_order  
- **MenuItem:** section, name, description, price, dietary_restriction  
- **DietaryRestriction:** label  
- **ProcessingLog:** menu, status, timestamp  

---

## API Overview

**Base URL:** `http://127.0.0.1:8000/api/`

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/restaurants/` | GET | Retrieve all restaurants |
| `/menus/` | GET | List menus per restaurant |
| `/menuitems/` | GET | Retrieve all menu items |
| `/menuitems/` | POST | Create a new menu item |
| `/upload/` | POST | Upload and process a PDF menu |
| `/logs/` | GET | View processing logs |

---

## Testing

The project includes a lightweight, automated test suite to verify backend functionality.

### Technologies
- `pytest`
- `pytest-django`

### Coverage
- **Models:** Relationships between restaurants, menus, and items  
- **API:** CRUD endpoints and data creation  
- **Processing:** Validation of menu versioning, ordering, and dietary restrictions  

### Run Tests
```bash
cd backend
pytest -v
```

---

## License

Licensed under the MIT License



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



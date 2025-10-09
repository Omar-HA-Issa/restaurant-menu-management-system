
# Restaurant Menu Project

Welcome to the **Restaurant Menu Project**! This project implements a dynamic restaurant menu management system that allows users to view, add, update, and delete menu items. Built with Python and Django, it leverages MySQL and Claude AI API integration for database management and processing, and React for the dinal user interface.

## Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Key Features](#key-features)
- [File Structure](#file-structure)
- [Future Improvements](#future-improvements)

---

## Features
- CRUD Operations for menu items
- PDF menu processing with AI
- Advanced filtering and search
- SQL materialized views
- Database optimization with indexes
- Responsive UI with Next.js
- Error logging and tracking

## Technologies Used
### Backend
- Python/Django
- Django REST Framework
- MySQL
- Anthropic Claude API
- PyMuPDF

### Frontend  
- Next.js/React
- TailwindCSS
- shadcn-ui
- React Query

## Database Schema & Indexes
- Restaurant (name, location)  
- Menu (version, date)
- MenuSection (section_name, section_order)
- MenuItem (name, price)
- DietaryRestriction (label)
- ProcessingLog (status, timestamp)

## SQL Views
```sql
CREATE VIEW menu_items_per_restaurant AS
SELECT 
   r.name as restaurant_name,
   COUNT(mi.item_id) as total_items,
   AVG(mi.price) as average_price
FROM menu_app_restaurant r
JOIN menu_app_menu m ON r.restaurant_id = m.restaurant_id
JOIN menu_app_menusection ms ON m.menu_id = ms.menu_id
JOIN menu_app_menuitem mi ON ms.section_id = mi.section_id
GROUP BY r.restaurant_id, r.name;

CREATE VIEW dietary_restrictions_distribution AS
SELECT 
   dr.label as restriction_type,
   COUNT(mi.item_id) as item_count,
   COUNT(mi.item_id) * 100.0 / (SELECT COUNT(*) FROM menu_app_menuitem) as percentage
FROM menu_app_dietaryrestriction dr
LEFT JOIN menu_app_menuitem mi ON dr.restriction_id = dr.restriction_id
GROUP BY dr.restriction_id, dr.label;

CREATE VIEW price_analysis_per_restaurant AS
SELECT 
   r.name as restaurant_name,
   MIN(mi.price) as min_price,
   MAX(mi.price) as max_price,
   AVG(mi.price) as avg_price
FROM menu_app_restaurant r
JOIN menu_app_menu m ON r.restaurant_id = m.restaurant_id
JOIN menu_app_menusection ms ON m.menu_id = ms.menu_id
JOIN menu_app_menuitem mi ON ms.section_id = mi.section_id
GROUP BY r.restaurant_id, r.name;
```
---

## Installation

Follow these steps to set up the project locally:

1. **Extract ZIP file**:
   ```bash
   extract ZIP file with the project
   cd Database_Project/restaurant_menu_project
   
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   
3. **Set your database connection**:
   - Create an SQL database
   - Set you own database connection in settings.py

5. **Run servers**
   ```terminal
   In terminal inside Database_Project/restaurant_menu_project run "python manage.py runserver"
   ```
   
   ```bash
   In Git CMD run "npm install, npm start, npm run dev"
   ```
   
6. **Navigate to admin/frontend**
   For django admin go to http://127.0.0.1:8000/admin
   For frontend go to http://localhost:3000
   
---

## Usage

### Navigating the Application
1. **Homepage**: View all menu categories and their respective items.
2. **Upload Menu**:  
   - Upload a PDF containing menu information.  
   - The PDF is processed using the AI Reader and structured into JSON for database storage.
3. **Views**: Materialized views
4. **Team**: A glimpse of our developing team
5. **Database**: Visualize the database and apply desired filters

---

## **Key Features**

This system is designed with a range of features to streamline menu management across the frontend and backend:

### **1) Frontend**
The frontend is built using **React** to provide a responsive user interface and handle API requests effectively. Key features include:  
- **Dynamic Navigation Menu**:  
  Allows easy management of menu uploads, categories, and items.  
- **Seamless Frontend Assets**:  
  Bundles frontend assets for optimized rendering and smooth navigation of the main menu.

### **2) Backend**
#### **Text Extraction**  
- Utilizes the **PyMuPDF** library to extract text from uploaded PDF menus, enabling AI-based processing.
#### **JSON formatting**
- Calls a request to Anthropic API to format extracted text into JSON
- Cleans the JSON structured data into ASCII characters
#### **Database insertion**
- Inserts extracted and cleaned JSON formatted data into the database

#### **SQL Schema and Database System (AI-Enhanced)**  
- Features a robust database schema design, including tables for menu categories, items, and user management.  
  Example:
  - **`Categories`**: Stores menu categories.  
  - **`Menu Items`**: Stores details for individual items, such as price, description, and associated categories.  

#### **Django Menu Processing**  
- Integrates the SQL database into the Django Admin panel for management.  
- Logs and tracks the entire menu processing lifecycle, supporting debugging and traceability.
- The Django administration interface has also been enhanced with Django unfold.

---

## **File Structure**

A breakdown of the main files and directories within the project:

1) ### **sql**  
- Central repository for materialized views' queries

2) ### **menu_app Folder**  
The core application directory containing several subcomponents:

1. #### **`PDFreader.py`**  
- Extracts text from uploaded PDF files.  
- Uses the **PyMuPDF** library for precise and efficient PDF operations.  
- Implements error handling to ensure accurate text extraction.

2. #### **`AIreader.py`**  
- Contains functions to process raw text extracted from PDFs and database insertion.  
- Categorizes and structures the text into tables, outputting structured JSON data for seamless database integration.

3. #### **`forms.py`**  
- Customizes forms for uploading PDFs and editing menu items.

4. #### **`api.py`**  
- Handles API requests and integrates with external systems for menu processing.  
- Ensures reliable communication between the backend and frontend.

5. #### **`serializers.py`**  
- Converts database models into JSON format for frontend communication.

6. #### **`models.py`**  
- Defines database structures for menu categories and items.  
- Establishes relationships between tables (e.g., categories and items) to enable efficient database querying.

7. #### **`views.py`**  
- Implements the core logic for handling HTTP requests and rendering templates.  
- Facilitates CRUD operations for managing menu items.

8. #### **`manage.py`**  
- A command-line utility for managing the Django application. Key functions include:  
  - Running the development server: `python manage.py runserver`  
  - Applying database migrations: `python manage.py migrate`  
  - Creating app-specific migrations: `python manage.py makemigrations`  
  - Creating a superuser account: `python manage.py createsuperuser`

9. #### **`admin.py`**
  - Sets the local django admin that displays the database according to the models
    
10. #### **`urls.py`**
  - Contains the essential paths of the project

11. #### **`views_queries`**
  - Sets django.db connection and executes views queries


3) ### **Frontend Folder**

The `frontend` directory contains all the client-side code:

1. **`db-app`**  
   - Contains pages (upload, database, views, team)
   - Handles database connections and queries
   - Houses React components and UI elements

2. **`frontend`**    
   - Contains settings and configurations
   - Manages frontend assets and resources

3. **`venv`**  
   - Python virtual environment directory
   - Contains project's Python dependencies
   - Isolates project dependencies from system Python

---

## **Future Improvements**

The system can be further enhanced with the following features:

1. **Support for Multiple File Types**:  
   - Enable the upload and processing of various file types (e.g., Word documents, images) instead of restricting uploads to PDFs.

2. **Smart Recommendation System**:  
   - Develop an AI-powered recommendation feature where the system suggests restaurants based on the user's preferred meal choice for a specific day.

3. **Expanded Dietary Restriction Options**:  
   - Incorporate more dietary restriction filters, such as **Halal food** or **Soy-free options**, to cater to a wider range of users' dietary needs.




Capstone Health & Fitness API

Overview

This project is a Django REST Framework (DRF) API designed to manage and track user health and fitness data. It provides endpoints for:

User authentication and profile management
Logging meals and calculating calories
Logging exercises and tracking calories burned
Blog posts for sharing health-related content

The API is token-based authentication compatible, supports pagination, and includes search functionality for meals, food items, exercises, and blog posts. The backend uses PostgreSQL as the database.

Table of Contents

1. Project Structure
2. Features
3. Installation
4. Database Configuration
5. Running the Application
6. API Endpoints
7. Authentication
8. Pagination and Search
9. Models Overview
10. Deployment Notes

Project Structure

capstone/

add_meals/          Meals and food tracking

* models.py
* serializers.py
* views.py
* urls.py

log_exercises/      Exercise tracking

* models.py
* serializers.py
* views.py
* urls.py

user_accounts/      User authentication, profile, blog posts

* models.py
* serializers.py
* views.py
* urls.py

capstone/           Project configuration

* settings.py
* urls.py
* wsgi.py
* asgi.py

manage.py

Features

User Accounts

User registration and login (token-based)
User profile with:

Age, height, weight
Gender
Activity level

Daily maintenance calories (TDEE) calculation
Blog posts with CRUD operations and search

Meals and Nutrition

Manage food items (calories per 100g)
Log meals with quantity and type (Breakfast, Lunch, Dinner)
Calculate calories per meal automatically
Daily meal summary endpoint

Exercise Tracking

Log exercises with:

Name, category (cardio, strength, flexibility, other)
Date, time, duration
Calories burned

Per-user exercise tracking

API Utilities

Pagination on all list endpoints (default 3 items per page)
Search filters on meals, food items, exercises, and blog posts
Read-only fields for date, time, and user-linked fields

Installation

1. Clone the repository:

git clone <https://github.com/james-mungai-git/capstone-assingment.git>
cd capstone

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate     Linux/Mac
venv\Scripts\activate        Windows

3. Install dependencies:

pip install -r requirements.txt

Database Configuration

The project uses PostgreSQL. Update capstone/settings.py:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'base_db',
'USER': 'postgress',
'PASSWORD': 'moonlight@1818',
'HOST': 'localhost',
'PORT': '5432',
}
}

Run migrations:

python manage.py makemigrations
python manage.py migrate

Running the Application

Start the development server:

python manage.py runserver

Access the API at: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

API Endpoints

User Accounts

/register/                 POST     Register a new user
/login/                    POST     Login and receive auth token
/auth-token/               POST     Obtain token via DRF
/userprofile/              GET, POST, PUT, DELETE   CRUD on user profile
/userprofile/maintenance_calories/   GET     Returns calculated TDEE
/blogposts/                GET, POST, PUT, DELETE   Manage blog posts

Meals

/meal-items/               GET, POST, PUT, DELETE   List, create, update, delete meals
/meal-items/?meal_type=Breakfast   GET   Filter meals by type
/food-items/               GET, POST, PUT, DELETE   List and manage food items
/meal-items/today_summary/ GET                      Summary calories for today

Exercises

/exercises/                GET, POST, PUT, DELETE   List, create, update, delete exercises

Authentication

Token-based authentication (rest_framework.authtoken)
Each protected endpoint requires Authorization: Token <your-token> header

Pagination and Search

Pagination: default 3 items per page (page and perpage query parameters)
Search: supported on meals, food items, exercises, and blog posts using search query parameter

Example:

GET /api/meal-items/?search=Chicken&page=1&perpage=5

Models Overview

User Accounts

UserProfile:

OneToOne with User
Stores age, height, weight, gender, activity level
Method: maintenance_calories()

BlogPost:

Author (ForeignKey User)
Title, content, published_date

Meals

Food:

Name, calories per 100g

Meal:

User, name, food, quantity, date, time
Method: calories()

Exercises

Exercise:

User, rep_name, category, date, time, duration, calories_burned

Deployment Notes

PostgreSQL required
Add allowed hosts in settings.py for production
Use Gunicorn as the WSGI server
Consider Whitenoise for static file serving
Token-based authentication will need proper security for production

Additional Notes

All dates and times are automatically generated (no input required from user)
Meals, exercises, and blog posts are per-user and cannot be modified by other users
DRF and Djoser are included for authentication management
The API supports both CRUD operations and summary endpoints for convenience


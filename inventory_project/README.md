# Simple Inventory Management API (Single Location)

A Django REST Framework API to manage categories, suppliers, products, and basic stock workflows (Week 1 focus: catalog CRUD + auth).

## Quick Start
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt  # or pip install django djangorestframework drf-spectacular
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

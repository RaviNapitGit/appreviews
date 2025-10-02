AppReviews Django project.

To run:
python -m venv .venv
source .venv/bin/activate   (or .venv\Scripts\activate on Windows)
pip install django python-dateutil
python manage.py migrate
python manage.py createsuperuser
python manage.py import_apps ./apps.csv
python manage.py import_reviews ./reviews.csv
python manage.py runserver

Notes:
- Timezone set to Asia/Kolkata
- Supervisors: any user with is_staff=True
- Suggest endpoint at /api/suggest/?q=...

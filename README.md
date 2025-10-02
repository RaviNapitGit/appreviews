# AppReviews

A Django 5.x project for managing mobile app reviews with two roles:  
- **Supervisors (staff users)** → approve/reject user-submitted reviews.  
- **Normal users** → browse apps, search, and submit reviews (which go to supervisors for approval).  

We use **SQLite** in development. (Apps & reviews are already imported in your provided DB.)

---

## 1. Setup

- Clone the project or unzip the provided archive.

- Create and activate a virtual environment:

```bash
python -m venv .venv
# On Linux/macOS
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

- Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Database

Database: SQLite (default db.sqlite3 in the project root).

No extra setup needed. If starting from scratch:

```
python manage.py migrate
```

## 3. User Roles

Supervisor → any user with is_staff=True.
Can see pending reviews and approve/reject them.

Normal user → is_staff=False.
Can submit reviews only; must be approved before publishing.

## 4. Import Data
```base
Import Apps
python manage.py import_apps ./resources/apps.csv

Import Reviews
python manage.py import_reviews ./resources/reviews.csv
```

Imported reviews are marked as APPROVED by default (historical data).

During import, reviews link to apps by name.

If no supervisors exist, reviews may not be assigned to anyone.

## 5. Run the Development Server
- start the server with ```python manage.py runserver```
- Visit: http://127.0.0.1:8000/ and Login Credentials with 

Username: superadmin
Password: Passw0rd.

Superadmin is also a supervisor (is_staff=True), so they will see the supervisor queue when logged in.

## 6. Features

### 1. Normal users:

Home page shows most downloaded apps.

Full-text search (with typeahead suggestions).

App detail page with approved reviews.

Submit new reviews (pending supervisor approval).

### 2. Supervisors (staff):

Home page shows pending reviews assigned to them.

Approve or reject reviews.

## 8. Notes

Using django.contrib.auth login (/accounts/login/).

Search suggestions work when typing 3+ characters.

Review text only: sentiment fields are hidden from end users.

User dropdown in navbar shows username, email, and role.
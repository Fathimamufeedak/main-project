# Medicinal Plant Identification & Usage Guide — Phase 1

This repository contains Phase-1 of the MCA final-year project: a Django web application scaffold implementing Users, Ayurvedic Doctors, Admin module, image uploads (no ML), and MySQL configuration.

Quick setup (Windows)

1. Create and activate a Python virtual environment (Python 3.10+ recommended):

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure database (SQLite by default):
- By default the project uses SQLite (`db.sqlite3`) so no DB server setup is required.
- If you prefer MySQL, change the `DATABASES` settings in [medicinal_plant_project/settings.py](medicinal_plant_project/settings.py) and install `mysqlclient`.

4. Run migrations and create superuser:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. Run development server:

```powershell
python manage.py runserver
```

6. Access the app at `http://127.0.0.1:8000/` and the admin at `/admin/`.

Project structure
- `users/` — user auth, registration, profile, dashboard
- `doctors/` — doctor registration, profile, verification flag
- `plants/` — plant information and `Remedy` model
- `consultations/` — user consultations, image upload (stored in `media/`)
- `adminpanel/` — admin UI for approving doctors and dataset placeholder

Notes
- Image uploads are stored in `media/consultation_images/`.
- Role-based access: staff (admin) can access adminpanel views. Doctors must be approved by admin (set `is_verified`).
- No ML, CNN, TensorFlow, or external logins are implemented.

Next steps (Phase-2 suggestions)
- Integrate ML model for plant prediction (keep media and models intact)
- Add richer doctor workflow and chat-like consultation interface
- Add tests and CI

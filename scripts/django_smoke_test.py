import os
import sys

# Ensure project root is on the path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinal_plant_project.settings')
import django
django.setup()

from django.test import Client

client = Client()

urls = [
    '/',
    '/register/',
    '/login/',
    '/plants/',
    '/consultations/upload/',
    '/consultations/my/',
    '/admin/',
    '/adminpanel/doctor-requests/',
    '/doctors/register/',
]

for u in urls:
    try:
        r = client.get(u)
        content = r.content[:200].decode('utf-8', errors='replace')
        print(f"{u} -> {r.status_code} | preview: {content!r}")
    except Exception as e:
        print(f"{u} -> ERROR: {e}")

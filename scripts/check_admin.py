import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinal_plant_project.settings')

import django
django.setup()

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()
u = User.objects.filter(username='admin').first()
print('FOUND:', bool(u))
if u:
    print('is_superuser:', u.is_superuser)
    print('is_staff:', u.is_staff)
    ok = authenticate(username='admin', password='Admin@123')
    print('AUTH_OK before reset:', bool(ok))
    if not ok:
        print('Resetting password to Admin@123')
        u.set_password('Admin@123')
        u.is_staff = True
        u.is_superuser = True
        u.save()
        ok2 = authenticate(username='admin', password='Admin@123')
        print('AUTH_OK after reset:', bool(ok2))
else:
    print('Admin user not found. Creating one...')
    u = User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')
    print('Created admin; AUTH_OK:', bool(authenticate(username='admin', password='Admin@123')))

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    # ensure Django's default login redirect (LOGIN_URL='/accounts/login/') works
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    # friendly routes for role-specific auth
    path('user/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('user/register/', RedirectView.as_view(url='/register/', permanent=False)),
    path('doctor/login/', RedirectView.as_view(url='/doctors/login/', permanent=False)),
    path('doctor/register/', RedirectView.as_view(url='/doctors/register/', permanent=False)),
    path('admin/login/', RedirectView.as_view(url='/adminpanel/login/', permanent=False)),
    path('', include('users.urls')),
    path('doctors/', include('doctors.urls')),
    path('plants/', include('plants.urls')),
    path('consultations/', include('consultations.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

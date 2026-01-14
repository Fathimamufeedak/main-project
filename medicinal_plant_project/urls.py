from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Keep Django's default admin (not used for viva, but available for superusers)
    path('admin/', admin.site.urls),

    # Ensure Django's default login redirect (LOGIN_URL='/accounts/login/') works
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),

    # Friendly routes for role-specific auth - all redirect to unified login
    path('user/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('user/register/', RedirectView.as_view(url='/register/', permanent=False)),
    path('doctor/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('doctor/register/', RedirectView.as_view(url='/doctors/register/', permanent=False)),

    # Route traditional /admin/login/ to unified login
    path('admin/login/', RedirectView.as_view(url='/login/', permanent=False)),

    # Custom admin panel – exposed under /admin-panel/ for viva/demo
    path('admin-panel/', include('adminpanel.urls')),
    # Backwards-compatible path if anything still uses /adminpanel/
    path('adminpanel/', include('adminpanel.urls')),

    # Core application routes
    path('', include('users.urls')),
    path('doctors/', include('doctors.urls')),
    path('plants/', include('plants.urls')),
    path('consultations/', include('consultations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

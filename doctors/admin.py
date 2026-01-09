from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'experience', 'is_verified')
    list_filter = ('is_verified',)

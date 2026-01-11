from django.contrib import admin
from .models import Doctor
from .models import Remedy


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'experience', 'is_verified')
    list_filter = ('is_verified',)


@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'plant', 'created_at')
    search_fields = ('consultation__id', 'plant__name')

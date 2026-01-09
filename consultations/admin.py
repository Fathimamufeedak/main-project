from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'status', 'created_at')
    list_filter = ('status',)

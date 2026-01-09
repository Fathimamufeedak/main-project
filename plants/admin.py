from django.contrib import admin
from .models import Plant, Remedy


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('plant_name',)


@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ('plant', 'doctor')

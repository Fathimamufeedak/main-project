from django.db import models


class Plant(models.Model):
    plant_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    medicinal_uses = models.TextField(blank=True)
    safety_guidelines = models.TextField(blank=True)

    def __str__(self):
        return self.plant_name


class Remedy(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True)
    # use app label reference to avoid import-time coupling
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    symptom = models.CharField(max_length=255, blank=True)
    remedy_description = models.TextField()
    usage = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        plant_name = self.plant.plant_name if self.plant else 'General'
        return f"Remedy ({self.symptom or 'unspecified'}) for {plant_name} by {self.doctor}"

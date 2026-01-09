from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
from plants.models import Plant


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    symptoms = models.TextField()
    uploaded_image = models.ImageField(upload_to='consultation_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True)
    identified_plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation #{self.id} by {self.user.username}"

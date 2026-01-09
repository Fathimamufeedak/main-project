from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, blank=True)
    experience = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class DoctorRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['qualification', 'experience']

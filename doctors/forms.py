from django import forms
from django.contrib.auth.models import User
from .models import Doctor
from doctors.models import Remedy
from consultations.models import Consultation
from plants.models import Plant


class DoctorLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['qualification', 'experience']


class RemedyForm(forms.ModelForm):
    class Meta:
        model = Remedy
        fields = ['plant', 'description', 'usage']


class ResponseForm(forms.Form):
    response = forms.CharField(widget=forms.Textarea(attrs={'rows':4}))


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=Consultation.STATUS_CHOICES)


class DoctorRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['qualification', 'experience']

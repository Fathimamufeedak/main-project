from django import forms
from django.contrib.auth.models import User
from .models import Doctor
from consultations.models import Consultation
from plants.models import Plant, Remedy


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
        fields = ['symptom', 'remedy_description', 'usage', 'plant']
        widgets = {
            'symptom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. cough'}),
            'remedy_description': forms.Textarea(attrs={'class': 'form-control', 'rows':4}),
            'usage': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'plant': forms.Select(attrs={'class': 'form-select'}),
        }


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

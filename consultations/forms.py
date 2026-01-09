from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['symptoms', 'uploaded_image', 'identified_plant']

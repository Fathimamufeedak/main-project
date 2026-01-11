from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    """Register using email + password. Username defaults to email local-part.

    This keeps the project's use of Django's User model but makes email the
    primary credential for registration/login as required.
    """
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        first = self.cleaned_data.get('first_name')
        last = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password1')
        # create user, use email as username
        username = email.split('@')[0]
        user = User(username=username, email=email, first_name=first or '', last_name=last or '')
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

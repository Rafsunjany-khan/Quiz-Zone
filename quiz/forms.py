# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        retype_password = cleaned_data.get("retype_password")
        if password != retype_password:
            raise ValidationError("Passwords do not match")

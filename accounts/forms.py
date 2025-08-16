from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Password must meet the requirements below.'  # generic help text
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    password_requirements = [
        "At least one uppercase letter (A–Z)",
        "At least one lowercase letter (a–z)",
        "At least one number (0–9)",
        "At least one symbol (!@#$%^&* etc.)",
        "Minimum 8 characters"
    ]

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        errors = []
        if not re.search(r'[A-Z]', password):
            errors.append("an uppercase letter")
        if not re.search(r'[a-z]', password):
            errors.append("a lowercase letter")
        if not re.search(r'[0-9]', password):
            errors.append("a number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("a symbol")
        if len(password) < 8:
            errors.append("at least 8 characters")

        if errors:
            raise ValidationError(f"Password must contain: {', '.join(errors)}.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")




from django import forms
from .models import Subscriber

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control me-sm-2 mb-2 mb-sm-0',
                'placeholder': 'Email',
                'style': 'font-size: 0.95rem;',
                'required': True,
            }),
        }

from django import forms
from .models import Order

DELIVERY_METHOD_CHOICES = [
    ("locker", "InPost Locker or Shop"),
    ("home", "Home Address"),
]

class OrderForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHOD_CHOICES)
    
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 
            'house_name_or_number',
            'street_address1', 'street_address2', 'town_or_city',
            'postcode', 'county', 'country',
            'phone_number',
            'delivery_method',
            
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'house_name_or_number': 'House Name or Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Postal Code',
            'county': 'County',
            'phone_number': 'Phone Number',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                placeholder = placeholders.get(field, '')
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


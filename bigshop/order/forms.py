import re

from django import forms
from django.core.exceptions import ValidationError

from .models import UserOrder


class OrderForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        exclude = ['user', 'paid', 'status']

    def clean(self):
        cd = super().clean()
        if cd['delivery'] == 'delivery':
            if not cd['address'] or not cd['postal_code']:
                raise forms.ValidationError('if you choice delivery, you have enter address and postal code too')

        if not re.fullmatch(r'[+]?\d{10,12}', cd['phone']):
            raise ValidationError('please enter correct phone')
        return cd

from django.forms import ModelForm
from .models import Address
from django.forms.widgets import Select, Input, Textarea, TextInput


class AddressForm (ModelForm):
    class Meta:
        model = Address
        fields = ['billing_profile', 'addressLine1', 'addressLine2',
                  'city', 'postal_code', 'state', 'country']
        # widgets = {
        #     'billing_profile': Select(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'postal_code': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'state': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'city': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'country': TextInput(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'addressLine1': Textarea(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     ),
        #     'addressLine2': Textarea(
        #         attrs={
        #             'class': 'form-control',
        #         }
        #     )
        # }

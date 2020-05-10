# for using django build in forms
from django import forms


# for contact forms

class ContactForm(forms.Form):
    fullName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_fullName',
                'placeholder': 'Your Full Name'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_email',
                'placeholder': 'Your Email'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'form_content',
                'placeholder': 'Your Content Here'
            }
        )
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not  '@gmail.com' in email:
            raise forms.ValidationError('Email Should be Gmail')
        return email
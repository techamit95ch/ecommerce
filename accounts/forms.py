# for using django build in forms
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# for contact forms

class GuestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_email',
                'placeholder': 'Your Email'
            }
        )
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not '@gmail.com' in email:
            raise forms.ValidationError('Email Should be Gmail')
        return email
        
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
        if not '@gmail.com' in email:
            raise forms.ValidationError('Email Should be Gmail')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_userName',
                'placeholder': 'Your User Name'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'form_password',
                'placeholder': 'Password'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_userName',
                'placeholder': 'Your User Name'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_email',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'form_password',
                'placeholder': 'Password'
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'form_password2',
                'placeholder': 'Confirm Password'
            }
        )
    )

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Password must match')
        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        chkUser = User.objects.filter(username=username)
        if chkUser.exists():
            raise forms.ValidationError("Username Exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        chkUser = User.objects.filter(email=email)
        if chkUser.exists():
            raise forms.ValidationError("Email Taken")
        return email

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm as DjangoPasswordResetForm
from .models import CustomUser

# ---------------------------
# Registration Form
# ---------------------------
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data


# ---------------------------
# Login Form
# ---------------------------
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


# ---------------------------
# Custom Password Reset Form
# ---------------------------
class CustomPasswordResetForm(DjangoPasswordResetForm):
    """
    This extends Django's built-in PasswordResetForm so that:
    - It can send reset emails using Django's auth system.
    - The field is styled with Bootstrap.
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your registered email"})
    )

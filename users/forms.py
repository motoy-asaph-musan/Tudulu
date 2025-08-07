# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")  # Add other custom fields if needed

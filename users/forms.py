# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 
from .models import UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")  # Add other custom fields if needed




class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'alternative_email', 'contact_number', 'show_contact']
        widgets = {
            'alternative_email': forms.EmailInput(attrs={'class': 'form-control form-control-lg py-2'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg py-2'}),
            'show_contact': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control form-control-lg py-2', 'id': 'id_profile_picture'}),
        }

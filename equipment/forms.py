from django import forms
from .models import InstalledEquipment
from .models import Post
from .models import Post, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

class InstalledEquipmentForm(forms.ModelForm):
    class Meta:
        model = InstalledEquipment
        fields = ['name', 'serial_number', 'location', 'date_installed', 'next_service_date', 'photo']
        widgets = {
            'date_installed': forms.DateInput(attrs={'type': 'date'}),
            'next_service_date': forms.DateInput(attrs={'type': 'date'}),
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "What's on your mind?",
                'rows': 3
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Write a comment...",
                'rows': 1
            }),
        }
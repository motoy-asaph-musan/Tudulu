from django import forms
from .models import InstalledEquipment
from .models import EquipmentPost


class InstalledEquipmentForm(forms.ModelForm):
    class Meta:
        model = InstalledEquipment
        fields = ['name', 'serial_number', 'location', 'date_installed', 'next_service_date', 'photo']
        widgets = {
            'date_installed': forms.DateInput(attrs={'type': 'date'}),
            'next_service_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EquipmentPostForm(forms.ModelForm):
    class Meta:
        model = EquipmentPost
        fields = ['title', 'description', 'image', 'tag']

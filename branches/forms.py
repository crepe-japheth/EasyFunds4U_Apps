# loans/forms.py
from django import forms
from .models import Branch

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            "name", "location", "phone", "manager"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }    
        labels = {
            'name': 'Branch Name',
            'location': 'Branch Location',
            'phone': 'Phone Number',
            'manager': 'Branch Manager',
        }
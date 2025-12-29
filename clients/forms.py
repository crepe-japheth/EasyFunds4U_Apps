# clients/forms.py
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "first_name", "last_name",
            "client_type", "national_id",
            "phone_number", "address", "branch", "status"
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_type': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }    
        labels = {
            'first_name': 'First Name', 
            'last_name': 'Last Name',
            'client_type': 'Client Type',
            'national_id': 'National ID',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'branch': 'Branch',
            'status': 'Status',
        }
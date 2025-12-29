# loans/forms.py
from django import forms
from ..models import LoanProduct

class LoanProductForm(forms.ModelForm):
    class Meta:
        model = LoanProduct
        fields = [
            "name", "description",
            "interest_rate", "duration_months",
            "repayment_frequency", "max_amount"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'repayment_frequency': forms.Select(attrs={'class': 'form-control'}),
            'max_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }    
        labels = {
            'name': 'Loan Product Name', 
            'description': 'Description',
            'interest_rate': 'Interest Rate (%)',
            'duration_months': 'Duration (Months)',
            'repayment_frequency': 'Repayment Frequency',
            'max_amount': 'Maximum Loan Amount',
        }
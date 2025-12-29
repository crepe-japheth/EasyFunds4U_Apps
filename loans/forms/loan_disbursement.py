# loans/forms.py
from django import forms
from ..models import Loan

class LoanDisbursementForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            "loan_application",
            "disbursed_amount",
            "disbursement_date",
            "status",
        ]
        widgets = {
            "loan_application": forms.Select(attrs={"class": "form-control"}),
            "disbursed_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "disbursement_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }    
        labels = {
            "loan_application": "Loan Application",
            "disbursed_amount": "Disbursed Amount",
            "disbursement_date": "Disbursement Date",
            "status": "Status",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default status to ACTIVE
        self.fields['status'].initial = 'ACTIVE'
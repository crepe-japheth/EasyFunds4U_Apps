# loans/forms.py
from django import forms
from ..models import LoanApplication

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            "client","loan_product","branch","amount_requested","remarks",

        ]
        widgets = {
            "client": forms.Select(attrs={"class": "form-control"}),
            "loan_product": forms.Select(attrs={"class": "form-control"}),
            "branch": forms.Select(attrs={"class": "form-control"}),
            "amount_requested": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }    
        labels = {
            "client": "Client",
            "loan_product": "Loan Product",
            "branch": "Branch",
            "amount_requested": "Amount Requested",
            "remarks": "Remarks",
        }
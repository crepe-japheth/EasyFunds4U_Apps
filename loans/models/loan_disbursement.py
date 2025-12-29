from django.db import models
from .loan_application import LoanApplication
from django.conf import settings
from decimal import Decimal

class Loan(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    disbursed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    disbursement_date = models.DateField()
    due_date = models.DateField()
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("ACTIVE", "Active"), ("CLOSED", "Closed"), ("DEFAULTED", "Defaulted")],
        default="ACTIVE"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='loans_created')

    def __str__(self):
        return f"Loan #{self.id} for {self.loan_application.client}"
    
    def get_total_amount(self):
        """Calculate total amount (principal + interest)"""
        principal = self.disbursed_amount
        product = self.loan_application.loan_product
        interest_rate = product.interest_rate / Decimal('100')
        interest_amount = principal * interest_rate * Decimal(str(product.duration_months)) / Decimal('12')
        return principal + interest_amount
    
    def get_interest_amount(self):
        """Calculate interest amount"""
        principal = self.disbursed_amount
        product = self.loan_application.loan_product
        interest_rate = product.interest_rate / Decimal('100')
        interest_amount = principal * interest_rate * Decimal(str(product.duration_months)) / Decimal('12')
        return interest_amount
    
    def get_total_repaid(self):
        """Get total amount repaid"""
        return sum(repayment.amount for repayment in self.repayment_set.all())
    
    class Meta:
        ordering = ['-created_at']


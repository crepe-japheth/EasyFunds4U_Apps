from django.db import models
from .loan_disbursement import Loan
from django.conf import settings


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()  # Changed from auto_now_add to allow manual date entry
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(
        max_length=20,
        choices=[("CASH", "Cash"), ("MOBILE", "Mobile Money"), ("BANK", "Bank Transfer")],
        default="CASH"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='repayments_created')

    def __str__(self):
        return f"Repayment of ${self.amount} for Loan #{self.loan.id}"
    
    class Meta:
        ordering = ['-payment_date']

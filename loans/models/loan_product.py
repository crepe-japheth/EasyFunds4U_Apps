# loans/models.py
from django.db import models
from django.conf import settings

class LoanProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.5%
    duration_months = models.PositiveIntegerField()  # e.g. 12 months
    repayment_frequency = models.CharField(
        max_length=20,
        choices=[("WEEKLY", "Weekly"), ("MONTHLY", "Monthly"), ("QUARTERLY", "Quarterly"), ("YEARLY", "Yearly")],
        default="MONTHLY"
    )
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='loan_products_created') 

    def __str__(self):
        return self.name

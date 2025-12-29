# clients/models.py
from django.db import models
from django.conf import settings

class Client(models.Model):
    INDIVIDUAL = "INDIVIDUAL"
    GROUP = "GROUP"
    CLIENT_TYPE_CHOICES = [(INDIVIDUAL, "Individual"), (GROUP, "Group")]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default=INDIVIDUAL)
    national_id = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    branch = models.ForeignKey("branches.Branch", on_delete=models.SET_NULL, null=True, blank=True, related_name='clients')
    date_joined = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
        default="ACTIVE"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients_created'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
    
    class Meta:
        ordering = ['-created_at']

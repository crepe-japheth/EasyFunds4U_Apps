# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=[
            ("ADMIN", "Admin"),
            ("LOAN_OFFICER", "Loan Officer"),
            ("BRANCH_MANAGER", "Branch Manager"),
            ("ACCOUNTANT", "Accountant"),
        ]
    )
    branch = models.ForeignKey("branches.Branch", on_delete=models.SET_NULL, null=True, blank=True)


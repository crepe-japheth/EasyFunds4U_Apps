from django.contrib import admin
from .models import (LoanApplication, LoanProduct, Repayment, Loan)

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('client', 'loan_product', 'branch', 'amount_requested', 'application_date', 'status', 'approved_by')
    search_fields = ('client__first_name', 'client__last_name', 'loan_product__name', 'status')
    list_filter = ('status', 'application_date', 'branch')
    ordering = ('-application_date',)

@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'max_amount', 'duration_months', 'repayment_frequency')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'amount', 'payment_date', 'method')
    search_fields = ('loan__id', 'method')
    list_filter = ('method', 'payment_date')
    ordering = ('-payment_date',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_application', 'disbursed_amount', 'disbursement_date', 'due_date', 'balance', 'status')
    search_fields = ('loan_application__client__first_name', 'loan_application__client__last_name', 'status')
    list_filter = ('status', 'disbursement_date')
    ordering = ('-disbursement_date',)
    readonly_fields = ('created_at', 'updated_at')
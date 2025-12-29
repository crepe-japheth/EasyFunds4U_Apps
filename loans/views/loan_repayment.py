# loans/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal
from ..models import LoanApplication, LoanProduct, Loan, Repayment
from clients.models import Client


class RepaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Repayment
    fields = ["loan", "amount", "method", "payment_date"]
    template_name = "loans/repayment_form.html"
    success_url = reverse_lazy("loans:repayment-list")
    permission_required = "loans.add_repayment"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only show active loans
        form.fields['loan'].queryset = Loan.objects.filter(status='ACTIVE')
        form.fields['loan'].widget.attrs.update({'class': 'form-control'})
        form.fields['payment_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        form.fields['method'].widget.attrs.update({'class': 'form-control'})
        # Set default payment date to today
        from django.utils import timezone
        form.fields['payment_date'].initial = timezone.now().date()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Validate payment amount doesn't exceed balance
        loan = form.instance.loan
        payment_amount = form.instance.amount
        
        if payment_amount > loan.balance:
            form.add_error('amount', f'Payment amount cannot exceed outstanding balance of ${loan.balance:.2f}')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        
        # Update loan balance
        loan.balance -= payment_amount
        if loan.balance <= Decimal('0.00'):
            loan.status = "CLOSED"
            loan.balance = Decimal('0.00')  # Ensure balance doesn't go negative
        loan.save()
        
        messages.success(self.request, f'Payment of ${payment_amount:.2f} recorded successfully.')
        return response
    
class RepaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Repayment
    template_name = "loans/repayment_list.html"
    context_object_name = "repayments"
    permission_required = "loans.view_repayment"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        loan_id = self.request.GET.get('loan')
        if loan_id:
            qs = qs.filter(loan_id=loan_id)
        return qs.select_related('loan__loan_application__client', 'created_by').order_by('-payment_date')

    

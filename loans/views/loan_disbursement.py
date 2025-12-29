# loans/views.py
from django.views.generic import UpdateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from ..models import LoanApplication, Loan
from ..forms.loan_disbursement import LoanDisbursementForm

class LoanApproveView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LoanApplication
    fields = ["status", "remarks"]
    template_name = "loans/loan_approval.html"
    success_url = reverse_lazy("loans:loanapplication-list")
    permission_required = "loans.change_loanapplication"

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        # Don't auto-create loan here - it should be done in disbursement view
        return super().form_valid(form)
    
class LoanDisbursementListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Loan
    template_name = "loans/loan_disbursement_list.html"
    context_object_name = "loans"
    permission_required = "loans.view_loan"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs.select_related('loan_application__client', 'loan_application__loan_product')


class LoanDisbursementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Loan
    form_class = LoanDisbursementForm
    template_name = "loans/loan_disbursement_form.html"
    success_url = reverse_lazy("loans:loan-disbursement-list")
    permission_required = "loans.add_loan"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only show approved applications that haven't been disbursed
        form.fields['loan_application'].queryset = LoanApplication.objects.filter(
            status='APPROVED'
        ).exclude(
            loan__isnull=False  # Exclude applications that already have a loan
        )
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Calculate due date based on loan product duration
        application = form.instance.loan_application
        product = application.loan_product
        
        # Calculate due date by adding duration_months to disbursement_date
        disbursement_date = form.instance.disbursement_date
        if product.duration_months:
            # Calculate months to add
            months = product.duration_months
            year = disbursement_date.year + (disbursement_date.month + months - 1) // 12
            month = ((disbursement_date.month + months - 1) % 12) + 1
            day = min(disbursement_date.day, [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
            from datetime import date
            due_date = date(year, month, day)
        else:
            # Default to 12 months if not specified
            year = disbursement_date.year + 1
            due_date = disbursement_date.replace(year=year)
        
        form.instance.due_date = due_date
        
        # Calculate total amount with interest
        principal = form.instance.disbursed_amount
        interest_rate = product.interest_rate / 100  # Convert percentage to decimal
        interest_amount = principal * interest_rate * (product.duration_months / 12)
        total_amount = principal + interest_amount
        
        # Set initial balance to total amount (principal + interest)
        form.instance.balance = total_amount
        
        # Update application status to DISBURSED
        application.status = "DISBURSED"
        application.save()
        
        return super().form_valid(form)


class LoanDetailView(LoginRequiredMixin, DetailView):
    model = Loan
    template_name = "loans/loan_detail.html"
    context_object_name = "loan"
    permission_required = "loans.view_loan"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all repayments for this loan
        context['repayments'] = self.object.repayment_set.all().order_by('-payment_date')
        # Calculate total repaid
        context['total_repaid'] = sum(rep.amount for rep in context['repayments'])
        # Calculate remaining balance
        context['remaining_balance'] = self.object.balance
        return context

    

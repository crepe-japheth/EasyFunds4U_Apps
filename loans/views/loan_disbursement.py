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
        queryset = LoanApplication.objects.filter(
            status='APPROVED'
        ).exclude(
            loan__isnull=False  # Exclude applications that already have a loan
        )
        
        # If application_id is provided in query params, pre-select it
        application_id = self.request.GET.get('application')
        if application_id:
            try:
                application = LoanApplication.objects.get(id=application_id, status='APPROVED')
                if application not in queryset:
                    # If it's already disbursed, still show it but disabled
                    queryset = LoanApplication.objects.filter(id=application_id)
                form.fields['loan_application'].initial = application
            except LoanApplication.DoesNotExist:
                pass
        
        form.fields['loan_application'].queryset = queryset
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
        loan = self.object
        application = loan.loan_application
        client = application.client
        product = application.loan_product
        
        # Get all repayments for this loan
        from ..models import Repayment
        repayments = Repayment.objects.filter(loan=loan).order_by('-payment_date')
        context['repayments'] = repayments
        
        # Calculate totals
        context['total_repaid'] = sum(rep.amount for rep in repayments)
        context['remaining_balance'] = loan.balance
        context['total_amount'] = loan.get_total_amount()
        context['interest_amount'] = loan.get_interest_amount()
        context['principal'] = loan.disbursed_amount
        
        # Calculate repayment percentage
        if context['total_amount'] > 0:
            context['repayment_percentage'] = (context['total_repaid'] / context['total_amount']) * 100
        else:
            context['repayment_percentage'] = 0
        
        # Days until due / days overdue
        from django.utils import timezone
        today = timezone.now().date()
        days_until_due = (loan.due_date - today).days
        context['days_until_due'] = days_until_due
        context['is_overdue'] = days_until_due < 0
        
        # Get client's other loans
        from ..models import Loan as LoanModel
        client_other_loans = LoanModel.objects.filter(
            loan_application__client=client
        ).exclude(id=loan.id).order_by('-created_at')[:5]
        context['client_other_loans'] = client_other_loans
        
        # Get client's active loans count
        client_active_loans = LoanModel.objects.filter(
            loan_application__client=client,
            status='ACTIVE'
        ).exclude(id=loan.id).count()
        context['client_active_loans'] = client_active_loans
        
        # Payment statistics
        if repayments.exists():
            context['first_payment_date'] = repayments.last().payment_date
            context['last_payment_date'] = repayments.first().payment_date
            context['payment_count'] = repayments.count()
            # Average payment amount
            context['average_payment'] = context['total_repaid'] / context['payment_count']
        else:
            context['payment_count'] = 0
            context['average_payment'] = 0
        
        return context

    

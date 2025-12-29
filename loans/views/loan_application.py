# loans/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from ..models import LoanApplication
from clients.models import Client
from ..forms.loan_application import LoanApplicationForm

class LoanApplicationListView(LoginRequiredMixin, ListView):
    model = LoanApplication
    template_name = "loans/application_list.html"
    context_object_name = "applications"
    paginate_by = 20



class LoanApplicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = LoanApplication
    template_name = "loans/application_form.html"
    form_class = LoanApplicationForm
    success_url = reverse_lazy("loans:loanapplication-list")
    permission_required = "loans.add_loanapplication"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["client"].queryset = Client.objects.filter(status="ACTIVE")
        return form

    def form_valid(self, form):
        form.instance.status = "PENDING"
        form.instance.created_by = self.request.user
        # Auto-assign branch from user if not set
        if not form.instance.branch and self.request.user.branch:
            form.instance.branch = self.request.user.branch
        return super().form_valid(form)
    
class LoanApplicationDetailView(LoginRequiredMixin, DetailView):
    model = LoanApplication
    template_name = "loans/application_detail.html"
    context_object_name = "application"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = self.object
        
        # Check if loan has been disbursed
        try:
            loan = application.loan
            context['loan'] = loan
            context['has_loan'] = True
            
            # Get repayment history
            from ..models import Repayment
            repayments = Repayment.objects.filter(loan=loan).order_by('-payment_date')
            context['repayments'] = repayments
            context['total_repaid'] = sum(rep.amount for rep in repayments)
            context['remaining_balance'] = loan.balance
            context['total_amount'] = loan.get_total_amount()
            context['interest_amount'] = loan.get_interest_amount()
        except:
            context['has_loan'] = False
            context['loan'] = None
        
        # Calculate estimated interest if not yet disbursed
        if not context['has_loan']:
            from decimal import Decimal
            principal = application.amount_requested
            product = application.loan_product
            interest_rate = product.interest_rate / Decimal('100')
            interest_amount = principal * interest_rate * Decimal(str(product.duration_months)) / Decimal('12')
            context['estimated_interest'] = interest_amount
            context['estimated_total'] = principal + interest_amount
        
        # Get client's other applications
        client_applications = LoanApplication.objects.filter(
            client=application.client
        ).exclude(id=application.id).order_by('-created_at')[:5]
        context['client_applications'] = client_applications
        
        # Get client's active loans count
        if context['has_loan']:
            from ..models import Loan
            client_active_loans = Loan.objects.filter(
                loan_application__client=application.client,
                status='ACTIVE'
            ).exclude(id=loan.id).count()
        else:
            from ..models import Loan
            client_active_loans = Loan.objects.filter(
                loan_application__client=application.client,
                status='ACTIVE'
            ).count()
        context['client_active_loans'] = client_active_loans
        
        return context


class LoanApplicationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = "loans/application_form.html"
    list_view_name = "loans:loan-application-list"
    success_url = reverse_lazy("loans:loanapplication-list")
    permission_required = "loans.change_loanapplication"

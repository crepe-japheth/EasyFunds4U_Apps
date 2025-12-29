# clients/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Sum
from .models import Client
from .forms import ClientForm

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10  # optional

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.object
        
        # Get loan applications
        from loans.models import LoanApplication
        applications = LoanApplication.objects.filter(client=client).order_by('-created_at')
        context['applications'] = applications
        context['total_applications'] = applications.count()
        context['pending_applications'] = applications.filter(status='PENDING').count()
        context['approved_applications'] = applications.filter(status='APPROVED').count()
        context['rejected_applications'] = applications.filter(status='REJECTED').count()
        context['disbursed_applications'] = applications.filter(status='DISBURSED').count()
        
        # Get loans (disbursed)
        from loans.models import Loan
        loans = Loan.objects.filter(loan_application__client=client).order_by('-created_at')
        context['loans'] = loans
        context['total_loans'] = loans.count()
        context['active_loans'] = loans.filter(status='ACTIVE').count()
        context['closed_loans'] = loans.filter(status='CLOSED').count()
        context['defaulted_loans'] = loans.filter(status='DEFAULTED').count()
        
        # Calculate loan statistics
        total_disbursed = loans.aggregate(total=Sum('disbursed_amount'))['total'] or 0
        total_outstanding = loans.filter(status='ACTIVE').aggregate(total=Sum('balance'))['total'] or 0
        total_requested = applications.aggregate(total=Sum('amount_requested'))['total'] or 0
        
        # Get repayments
        from loans.models import Repayment
        repayments = Repayment.objects.filter(loan__loan_application__client=client).order_by('-payment_date')
        context['repayments'] = repayments[:10]  # Recent 10 repayments
        context['total_repayments'] = repayments.count()
        total_repaid = repayments.aggregate(total=Sum('amount'))['total'] or 0
        context['total_repaid'] = total_repaid
        
        # Calculate total loan amount (principal + interest)
        total_loan_amount = sum(loan.get_total_amount() for loan in loans)
        context['total_loan_amount'] = total_loan_amount
        
        # Calculate repayment percentage
        if total_loan_amount > 0:
            context['repayment_percentage'] = (total_repaid / total_loan_amount) * 100
        else:
            context['repayment_percentage'] = 0
        
        context.update({
            'total_disbursed': total_disbursed,
            'total_outstanding': total_outstanding,
            'total_requested': total_requested,
            'total_loan_amount': total_loan_amount,
        })
        
        # Recent activity (last 5 applications)
        context['recent_applications'] = applications[:5]
        
        # Recent loans (last 5)
        context['recent_loans'] = loans[:5]
        
        return context


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm  # You can specify a form class if needed
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("loans:loanproduct-list")
    permission_required = "clients.add_client"

    def form_valid(self, form):
        # Assign branch automatically
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("loans:loanproduct-list")
    permission_required = "clients.change_client"

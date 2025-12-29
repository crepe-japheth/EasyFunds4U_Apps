# branches/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Sum, Count
from .models import Branch
from .forms import BranchForm

class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    template_name = "branches/branch_list.html"
    context_object_name = "branches"
    paginate_by = 10  # optional

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class BranchDetailView(LoginRequiredMixin, DetailView):
    model = Branch
    template_name = "branches/branch_detail.html"
    context_object_name = "branch"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.object
        
        # Get clients for this branch
        from clients.models import Client
        clients = Client.objects.filter(branch=branch)
        context['total_clients'] = clients.count()
        context['active_clients'] = clients.filter(status='ACTIVE').count()
        context['inactive_clients'] = clients.filter(status='INACTIVE').count()
        
        # Get loan applications for this branch
        from loans.models import LoanApplication
        applications = LoanApplication.objects.filter(branch=branch)
        context['total_applications'] = applications.count()
        context['pending_applications'] = applications.filter(status='PENDING').count()
        context['approved_applications'] = applications.filter(status='APPROVED').count()
        context['rejected_applications'] = applications.filter(status='REJECTED').count()
        context['disbursed_applications'] = applications.filter(status='DISBURSED').count()
        
        # Calculate total requested
        total_requested = applications.aggregate(total=Sum('amount_requested'))['total'] or 0
        context['total_requested'] = total_requested
        
        # Get loans for this branch
        from loans.models import Loan
        loans = Loan.objects.filter(loan_application__branch=branch)
        context['total_loans'] = loans.count()
        context['active_loans'] = loans.filter(status='ACTIVE').count()
        context['closed_loans'] = loans.filter(status='CLOSED').count()
        context['defaulted_loans'] = loans.filter(status='DEFAULTED').count()
        
        # Calculate loan statistics
        total_disbursed = loans.aggregate(total=Sum('disbursed_amount'))['total'] or 0
        total_outstanding = loans.filter(status='ACTIVE').aggregate(total=Sum('balance'))['total'] or 0
        context['total_disbursed'] = total_disbursed
        context['total_outstanding'] = total_outstanding
        
        # Get repayments for this branch
        from loans.models import Repayment
        repayments = Repayment.objects.filter(loan__loan_application__branch=branch)
        context['total_repayments'] = repayments.count()
        total_repaid = repayments.aggregate(total=Sum('amount'))['total'] or 0
        context['total_repaid'] = total_repaid
        
        # Calculate total loan amount
        total_loan_amount = sum(loan.get_total_amount() for loan in loans)
        context['total_loan_amount'] = total_loan_amount
        
        # Calculate repayment percentage
        if total_loan_amount > 0:
            context['repayment_percentage'] = (total_repaid / total_loan_amount) * 100
        else:
            context['repayment_percentage'] = 0
        
        # Get staff members assigned to this branch
        from users.models import User
        staff_members = User.objects.filter(branch=branch)
        context['staff_members'] = staff_members
        context['total_staff'] = staff_members.count()
        
        # Get manager info
        if branch.manager:
            context['manager'] = branch.manager
            context['has_manager'] = True
        else:
            context['has_manager'] = False
        
        # Recent activity
        context['recent_clients'] = clients.order_by('-created_at')[:5]
        context['recent_applications'] = applications.order_by('-created_at')[:5]
        context['recent_loans'] = loans.order_by('-created_at')[:5]
        context['recent_repayments'] = repayments.order_by('-payment_date')[:5]
        
        return context


class BranchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm  # You can specify a form class if needed
    template_name = "branches/branch_form.html"
    success_url = reverse_lazy("branches:branch_list")
    permission_required = "branches.add_branch"

    def form_valid(self, form):
        # Assign branch automatically
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BranchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = "branches/branch_form.html"
    success_url = reverse_lazy("branches:branch_list")
    permission_required = "branches.change_branch"
    
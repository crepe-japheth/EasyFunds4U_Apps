# loans/views.py
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import LoanProduct
from ..forms import LoanProductForm

class LoanProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LoanProduct
    template_name = "loans/loanproduct_list.html"
    context_object_name = "loanproducts"
    paginate_by = 20
    permission_required = "loans.view_loanproduct"
    

class LoanProductDetailView(LoginRequiredMixin, DetailView):
    model = LoanProduct
    template_name = "loans/loanproduct_detail.html"
    context_object_name = "loanproduct"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan_product = self.object
        
        # Get statistics for this loan product
        from django.db.models import Sum, Count, Q
        from ..models import LoanApplication, Loan
        
        # Total applications
        total_applications = LoanApplication.objects.filter(loan_product=loan_product).count()
        
        # Applications by status
        pending_applications = LoanApplication.objects.filter(
            loan_product=loan_product, status='PENDING'
        ).count()
        approved_applications = LoanApplication.objects.filter(
            loan_product=loan_product, status='APPROVED'
        ).count()
        rejected_applications = LoanApplication.objects.filter(
            loan_product=loan_product, status='REJECTED'
        ).count()
        disbursed_applications = LoanApplication.objects.filter(
            loan_product=loan_product, status='DISBURSED'
        ).count()
        
        # Total amount requested
        total_requested = LoanApplication.objects.filter(
            loan_product=loan_product
        ).aggregate(total=Sum('amount_requested'))['total'] or 0
        
        # Total amount disbursed
        total_disbursed = Loan.objects.filter(
            loan_application__loan_product=loan_product
        ).aggregate(total=Sum('disbursed_amount'))['total'] or 0
        
        # Total active loans
        active_loans = Loan.objects.filter(
            loan_application__loan_product=loan_product,
            status='ACTIVE'
        ).count()
        
        # Total closed loans
        closed_loans = Loan.objects.filter(
            loan_application__loan_product=loan_product,
            status='CLOSED'
        ).count()
        
        # Total outstanding balance
        outstanding_balance = Loan.objects.filter(
            loan_application__loan_product=loan_product,
            status='ACTIVE'
        ).aggregate(total=Sum('balance'))['total'] or 0
        
        # Total repaid
        from ..models import Repayment
        total_repaid = Repayment.objects.filter(
            loan__loan_application__loan_product=loan_product
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent applications (last 10)
        recent_applications = LoanApplication.objects.filter(
            loan_product=loan_product
        ).select_related('client', 'branch').order_by('-created_at')[:10]
        
        # Active loans list
        active_loans_list = Loan.objects.filter(
            loan_application__loan_product=loan_product,
            status='ACTIVE'
        ).select_related('loan_application__client').order_by('-created_at')[:10]
        
        context.update({
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'approved_applications': approved_applications,
            'rejected_applications': rejected_applications,
            'disbursed_applications': disbursed_applications,
            'total_requested': total_requested,
            'total_disbursed': total_disbursed,
            'active_loans': active_loans,
            'closed_loans': closed_loans,
            'outstanding_balance': outstanding_balance,
            'total_repaid': total_repaid,
            'recent_applications': recent_applications,
            'active_loans_list': active_loans_list,
        })
        
        return context
    

class LoanProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = LoanProduct
    form_class = LoanProductForm
    template_name = "loans/loanproduct_form.html"
    list_view_name = "loans:loanproduct-list"
    success_url = reverse_lazy("clients:client_list")
    permission_required = "loans.add_loanproduct"  # set proper perm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class LoanProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LoanProduct
    form_class = LoanProductForm
    template_name = "loans/loanproduct_form.html"
    list_view_name = "loans:loanproduct-list"
    success_url = reverse_lazy("clients:client_list")
    permission_required = "loans.change_loanproduct"
    

class LoanProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = LoanProduct
    template_name = "loans/loanproduct_confirm_delete.html"
    list_view_name = "loans:loanproduct-list"
    success_url = reverse_lazy("clients:client_list")
    permission_required = "loans.delete_loanproduct"

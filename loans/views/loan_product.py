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

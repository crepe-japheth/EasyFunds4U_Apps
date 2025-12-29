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


class LoanApplicationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = "loans/application_form.html"
    list_view_name = "loans:loan-application-list"
    success_url = reverse_lazy("loans:loanapplication-list")
    permission_required = "loans.change_loanapplication"

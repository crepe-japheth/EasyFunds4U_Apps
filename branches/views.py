# branches/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
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
    
# users/views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Sum, Count
from .forms import AdminUserCreationForm
from .models import User

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")



class AdminUserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminUserCreationForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy("users:user-list")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 10


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"
    
    def get_object(self):
        # Return the current logged-in user
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        # Get statistics for this user's activity
        from loans.models import LoanApplication, Loan, LoanProduct, Repayment
        from clients.models import Client
        from branches.models import Branch
        
        # Applications created by this user
        applications_created = LoanApplication.objects.filter(created_by=user)
        context['applications_created'] = applications_created.count()
        context['applications_approved'] = LoanApplication.objects.filter(approved_by=user).count()
        
        # Loans created by this user
        loans_created = Loan.objects.filter(created_by=user)
        context['loans_created'] = loans_created.count()
        
        # Repayments created by this user
        repayments_created = Repayment.objects.filter(created_by=user)
        context['repayments_created'] = repayments_created.count()
        total_repaid_by_user = repayments_created.aggregate(total=Sum('amount'))['total'] or 0
        context['total_repaid_by_user'] = total_repaid_by_user
        
        # Loan products created
        products_created = LoanProduct.objects.filter(created_by=user)
        context['products_created'] = products_created.count()
        
        # Clients created
        clients_created = Client.objects.filter(created_by=user)
        context['clients_created'] = clients_created.count()
        
        # Branches created
        branches_created = Branch.objects.filter(created_by=user)
        context['branches_created'] = branches_created.count()
        
        # Recent activity
        context['recent_applications'] = applications_created.order_by('-created_at')[:5]
        context['recent_loans'] = loans_created.order_by('-created_at')[:5]
        context['recent_repayments'] = repayments_created.order_by('-created_at')[:5]
        
        # If user is a branch manager, get branch statistics
        if user.branch:
            branch = user.branch
            branch_clients = Client.objects.filter(branch=branch).count()
            branch_applications = LoanApplication.objects.filter(branch=branch).count()
            branch_loans = Loan.objects.filter(loan_application__branch=branch).count()
            
            context['branch_clients'] = branch_clients
            context['branch_applications'] = branch_applications
            context['branch_loans'] = branch_loans
        
        # Check if user manages any branches
        managed_branches = Branch.objects.filter(manager=user)
        context['managed_branches'] = managed_branches
        context['managed_branches_count'] = managed_branches.count()
        
        return context

# users/views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView
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

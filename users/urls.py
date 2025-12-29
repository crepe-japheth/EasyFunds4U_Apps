# users/urls.py
from django.urls import path
from .views import UserLoginView, UserLogoutView, AdminUserCreateView, UserListView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("create/", AdminUserCreateView.as_view(), name="create-user"),
    path("list/", UserListView.as_view(), name="user-list"),
]

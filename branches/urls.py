from django.urls import path
from . import views


app_name = 'branches'
urlpatterns = [
    # Define your URL patterns here
    path('', views.BranchListView.as_view(), name='branch_list'),
    path('branch/<int:pk>/', views.BranchDetailView.as_view(), name='branch_detail'),
    path('branch/add/', views.BranchCreateView.as_view(), name='branch_add'),   
    path('branch/<int:pk>/edit/', views.BranchUpdateView.as_view(), name='branch_edit'),
    
]

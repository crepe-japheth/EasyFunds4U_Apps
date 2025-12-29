from django.urls import path
from . import views


app_name = 'clients'
urlpatterns = [
    # Define your URL patterns here
    path('', views.ClientListView.as_view(), name='client_list'),
    path('client-detail/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client-edit/<int:pk>/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('new/', views.ClientCreateView.as_view(), name='client_create'),
]

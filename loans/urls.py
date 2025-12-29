
# loans/urls.py
from django.urls import path
from loans.views import LoanDashboardView
from loans.views import (
    LoanProductListView,
    LoanProductCreateView,
    LoanProductDetailView,
    LoanProductUpdateView,
    LoanProductDeleteView,

    # loan application views here
    LoanApplicationCreateView,
    LoanApplicationDetailView,
    LoanApplicationUpdateView,
    LoanApplicationListView,

    # loan approval and disbursement views
    LoanApproveView,
    LoanDisbursementListView,
    LoanDisbursementCreateView,
    LoanDetailView,

    # loan repayment views
    RepaymentCreateView,
    RepaymentListView,
)
app_name = "loans"

urlpatterns = [
    path('', LoanDashboardView.as_view(), name='home'),
    
    # loan product CRUD
    path("products/", LoanProductListView.as_view(), name="loanproduct-list"),
    path("products/new/", LoanProductCreateView.as_view(), name="loanproduct-create"),
    path("products/<int:pk>/", LoanProductDetailView.as_view(), name="loanproduct-detail"),
    path("products/<int:pk>/edit/", LoanProductUpdateView.as_view(), name="loanproduct-update"),
    path("products/<int:pk>/delete/", LoanProductDeleteView.as_view(), name="loanproduct-delete"),

    # loan application views
    path("applications/", LoanApplicationListView.as_view(), name="loanapplication-list"),
    path("applications/new/", LoanApplicationCreateView.as_view(), name="loanapplication-create"),
    path("applications/<int:pk>/", LoanApplicationDetailView.as_view(), name="loanapplication-detail"),
    path("applications/<int:pk>/edit/", LoanApplicationUpdateView.as_view(), name="loanapplication-update"),

    # loan approval view
    path("applications/<int:pk>/approve/", LoanApproveView.as_view(), name="loanapplication-approve"),
    path("disbursements/", LoanDisbursementListView.as_view(), name="loan-disbursement-list"),
    path("disbursements/new/", LoanDisbursementCreateView.as_view(), name="loan-disbursement-create"),
    path("disbursements/<int:pk>/", LoanDetailView.as_view(), name="loan-detail"),

    # loan repayment views
    path("repayments/new/", RepaymentCreateView.as_view(), name="repayment-create"),  
    path("repayments/", RepaymentListView.as_view(), name="repayment-list"),  


    
]


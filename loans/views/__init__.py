from .loan_disbursement import LoanApproveView, LoanDisbursementListView, LoanDisbursementCreateView, LoanDetailView
from .loan_application import LoanApplicationListView, LoanApplicationCreateView
from .loan_product import (
    LoanProductListView, LoanProductDetailView,
    LoanProductCreateView, LoanProductUpdateView, LoanProductDeleteView
)
from .loan_repayment import RepaymentCreateView
from .loan_dashboard import LoanDashboardView
from .loan_application import LoanApplicationDetailView, LoanApplicationUpdateView, LoanApplicationCreateView, LoanApplicationListView
from .loan_repayment import RepaymentCreateView, RepaymentListView

__all__ = [
    LoanApproveView,
    LoanApplicationListView, LoanApplicationCreateView,
    LoanProductListView, LoanProductDetailView,
    LoanProductCreateView, LoanProductUpdateView, LoanProductDeleteView,
    RepaymentCreateView,
    LoanDashboardView,

    # loan application views here
    LoanApplicationDetailView, 
    LoanApplicationUpdateView, 
    LoanApplicationCreateView, 
    LoanApplicationListView,
    LoanDisbursementListView,
    LoanDisbursementCreateView,
    LoanDetailView,

    RepaymentCreateView,
    RepaymentListView,
]
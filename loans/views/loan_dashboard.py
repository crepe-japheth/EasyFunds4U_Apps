from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import LoanApplication, Loan, Repayment, LoanProduct
from clients.models import Client


class LoanDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total statistics
        total_applied = LoanApplication.objects.aggregate(
            total=Sum('amount_requested')
        )['total'] or 0
        
        total_disbursed = Loan.objects.aggregate(
            total=Sum('disbursed_amount')
        )['total'] or 0
        
        total_repaid = Repayment.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Active loans
        active_loans = Loan.objects.filter(status='ACTIVE').count()
        total_loans = Loan.objects.count()
        
        # Today's statistics
        today = timezone.now().date()
        today_applied = LoanApplication.objects.filter(
            application_date=today
        ).aggregate(total=Sum('amount_requested'))['total'] or 0
        
        today_disbursed = Loan.objects.filter(
            disbursement_date=today
        ).aggregate(total=Sum('disbursed_amount'))['total'] or 0
        
        today_repaid = Repayment.objects.filter(
            payment_date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # This month statistics
        month_start = today.replace(day=1)
        month_applied = LoanApplication.objects.filter(
            application_date__gte=month_start
        ).aggregate(total=Sum('amount_requested'))['total'] or 0
        
        month_disbursed = Loan.objects.filter(
            disbursement_date__gte=month_start
        ).aggregate(total=Sum('disbursed_amount'))['total'] or 0
        
        month_repaid = Repayment.objects.filter(
            payment_date__gte=month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Last month for comparison
        if month_start.month == 1:
            last_month_start = month_start.replace(year=month_start.year - 1, month=12)
        else:
            last_month_start = month_start.replace(month=month_start.month - 1)
        
        if last_month_start.month == 12:
            last_month_end = month_start - timedelta(days=1)
        else:
            last_month_end = month_start - timedelta(days=1)
        
        last_month_applied = LoanApplication.objects.filter(
            application_date__gte=last_month_start,
            application_date__lt=month_start
        ).aggregate(total=Sum('amount_requested'))['total'] or 0
        
        # Calculate percentage changes
        applied_change = 0
        if last_month_applied > 0:
            applied_change = ((month_applied - last_month_applied) / last_month_applied) * 100
        
        disbursed_change = 0
        last_month_disbursed = Loan.objects.filter(
            disbursement_date__gte=last_month_start,
            disbursement_date__lt=month_start
        ).aggregate(total=Sum('disbursed_amount'))['total'] or 0
        if last_month_disbursed > 0:
            disbursed_change = ((month_disbursed - last_month_disbursed) / last_month_disbursed) * 100
        
        repaid_change = 0
        last_month_repaid = Repayment.objects.filter(
            payment_date__gte=last_month_start,
            payment_date__lt=month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        if last_month_repaid > 0:
            repaid_change = ((month_repaid - last_month_repaid) / last_month_repaid) * 100
        
        # Loan products statistics
        loan_products = LoanProduct.objects.annotate(
            loan_count=Count('loanapplication')
        ).order_by('-loan_count')[:3]
        
        # Recent applications
        recent_applications = LoanApplication.objects.select_related(
            'client', 'loan_product'
        ).order_by('-created_at')[:10]
        
        # Pending applications count
        pending_applications = LoanApplication.objects.filter(status='PENDING').count()
        
        # Outstanding balance
        outstanding_balance = Loan.objects.filter(status='ACTIVE').aggregate(
            total=Sum('balance')
        )['total'] or 0
        
        context.update({
            'total_applied': total_applied,
            'total_disbursed': total_disbursed,
            'total_repaid': total_repaid,
            'active_loans': active_loans,
            'total_loans': total_loans,
            'today_applied': today_applied,
            'today_disbursed': today_disbursed,
            'today_repaid': today_repaid,
            'month_applied': month_applied,
            'month_disbursed': month_disbursed,
            'month_repaid': month_repaid,
            'applied_change': applied_change,
            'disbursed_change': disbursed_change,
            'repaid_change': repaid_change,
            'loan_products': loan_products,
            'recent_applications': recent_applications,
            'pending_applications': pending_applications,
            'outstanding_balance': outstanding_balance,
        })
        
        return context
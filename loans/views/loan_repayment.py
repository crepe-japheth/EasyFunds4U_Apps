# loans/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from decimal import Decimal
from ..models import LoanApplication, LoanProduct, Loan, Repayment
from clients.models import Client


class RepaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Repayment
    fields = ["loan", "amount", "method", "payment_date"]
    template_name = "loans/repayment_form.html"
    success_url = reverse_lazy("loans:repayment-list")
    permission_required = "loans.add_repayment"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only show active loans
        queryset = Loan.objects.filter(status='ACTIVE')
        
        # If loan_id is provided in query params, pre-select it
        loan_id = self.request.GET.get('loan')
        if loan_id:
            try:
                loan = Loan.objects.get(id=loan_id, status='ACTIVE')
                form.fields['loan'].initial = loan
            except Loan.DoesNotExist:
                pass
        
        form.fields['loan'].queryset = queryset
        form.fields['loan'].widget.attrs.update({'class': 'form-control'})
        form.fields['payment_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        form.fields['amount'].widget.attrs.update({'class': 'form-control', 'step': '0.01'})
        form.fields['method'].widget.attrs.update({'class': 'form-control'})
        # Set default payment date to today
        from django.utils import timezone
        form.fields['payment_date'].initial = timezone.now().date()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Validate payment amount doesn't exceed balance
        loan = form.instance.loan
        payment_amount = form.instance.amount
        
        if payment_amount > loan.balance:
            form.add_error('amount', f'Payment amount cannot exceed outstanding balance of ${loan.balance:.2f}')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        
        # Update loan balance
        loan.balance -= payment_amount
        if loan.balance <= Decimal('0.00'):
            loan.status = "CLOSED"
            loan.balance = Decimal('0.00')  # Ensure balance doesn't go negative
        loan.save()
        
        messages.success(self.request, f'Payment of ${payment_amount:.2f} recorded successfully.')
        return response
    
class RepaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Repayment
    template_name = "loans/repayment_list.html"
    context_object_name = "repayments"
    permission_required = "loans.view_repayment"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        loan_id = self.request.GET.get('loan')
        if loan_id:
            qs = qs.filter(loan_id=loan_id)
        return qs.select_related('loan__loan_application__client', 'created_by').order_by('-payment_date')


class RepaymentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Repayment
    template_name = "loans/repayment_detail.html"
    context_object_name = "repayment"
    permission_required = "loans.view_repayment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repayment = self.object
        loan = repayment.loan
        application = loan.loan_application
        client = application.client
        product = application.loan_product
        
        # Get all repayments for this loan to calculate position
        all_repayments = Repayment.objects.filter(loan=loan).order_by('payment_date')
        repayment_position = list(all_repayments).index(repayment) + 1
        total_repayments = all_repayments.count()
        
        # Calculate balance before and after this payment
        repayments_before = all_repayments.filter(payment_date__lt=repayment.payment_date)
        balance_before = loan.get_total_amount() - sum(rep.amount for rep in repayments_before)
        balance_after = balance_before - repayment.amount
        
        # Get previous and next repayments
        previous_repayment = all_repayments.filter(payment_date__lt=repayment.payment_date).last()
        next_repayment = all_repayments.filter(payment_date__gt=repayment.payment_date).first()
        
        # Loan statistics
        total_repaid = sum(rep.amount for rep in all_repayments)
        total_amount = loan.get_total_amount()
        remaining_balance = loan.balance
        
        # Payment impact
        payment_percentage = (repayment.amount / total_amount) * 100 if total_amount > 0 else 0
        
        context.update({
            'loan': loan,
            'application': application,
            'client': client,
            'product': product,
            'repayment_position': repayment_position,
            'total_repayments': total_repayments,
            'balance_before': balance_before,
            'balance_after': balance_after,
            'previous_repayment': previous_repayment,
            'next_repayment': next_repayment,
            'total_repaid': total_repaid,
            'total_amount': total_amount,
            'remaining_balance': remaining_balance,
            'payment_percentage': payment_percentage,
            'all_repayments': all_repayments,
        })
        
        return context

    

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from finance.models import Transaction, Account, Category, AccountType
from .forms import AccountForm, UpdateAccountForm
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def dashboard_view(request):
    # Get the current user
    user = request.user

    # Define the time period for the report (e.g., last 30 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    # Filter transactions for the current user and the last 30 days
    transactions = Transaction.objects.filter(user=user, date__range=[start_date, end_date])

    # --- 1. Income vs. Expense Summary ---
    income_total = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense_total = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

    # --- 2. Top 5 Expense Categories ---
    top_expense_categories = (
        transactions.filter(type='EXPENSE')
        .values('category__name')
        .annotate(total_spent=Sum('amount'))
        .order_by('-total_spent')[:5]
    )

    # --- 3. Account Balances ---
    accounts = Account.objects.filter(user=user)

    # --- 4. Recent Transactions ---
    recent_transactions = Transaction.objects.filter(user=user).order_by('-date', '-id')[:10]

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'income_total': income_total,
        'expense_total': expense_total,
        'top_expense_categories': top_expense_categories,
        'accounts': accounts,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'finance/dashboard.html', context)

@login_required
def accounts_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
        elif action == 'delete':
            account_id = request.POST.get('account_id')
            Account.objects.filter(id=account_id, user=request.user).delete()
        elif action == 'update':
            account_id = request.POST.get('account_id')
            return redirect('update_account', account_id=account_id)
        return redirect('accounts')

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()

    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'finance/accounts.html', context)

@login_required
def update_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    else:
        form = UpdateAccountForm(instance=account)
    return render(request, 'finance/update_account.html', {'form': form, 'account': account})
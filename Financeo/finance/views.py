from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from finance.models import Transaction, Account, Category, AccountType, Budget
from .forms import AccountForm, UpdateAccountForm, BudgetForm, UpdateBudgetForm
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

@login_required
def account_transactions_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account, user=request.user).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'finance/account_transactions.html', context)

@login_required
def budgets_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            form = BudgetForm(request.POST)
            if form.is_valid():
                budget = form.save(commit=False)
                budget.user = request.user
                budget.save()
        elif action == 'delete':
            budget_id = request.POST.get('budget_id')
            Budget.objects.filter(id=budget_id, user=request.user).delete()
        elif action == 'update':
            budget_id = request.POST.get('budget_id')
            return redirect('update_budget', budget_id=budget_id)
        return redirect('budgets')

    budgets = Budget.objects.filter(user=request.user)
    form = BudgetForm()
    form.fields['category'].queryset = Category.objects.filter(user=request.user)


    context = {
        'budgets': budgets,
        'form': form,
    }
    return render(request, 'finance/budgets.html', context)

@login_required
def update_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = UpdateBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgets')
    else:
        form = UpdateBudgetForm(instance=budget)
    return render(request, 'finance/update_budget.html', {'form': form, 'budget': budget})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from finance.models import Transaction
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import base64

@login_required
def reports_view(request):
    user = request.user

    # --- Chart 1: Income vs Expense (Bar Chart) ---
    income_vs_expense = user.transactions.values('type').annotate(total=Sum('amount'))
    income = next((item['total'] for item in income_vs_expense if item['type'] == 'INCOME'), 0)
    expense = next((item['total'] for item in income_vs_expense if item['type'] == 'EXPENSE'), 0)

    plt.figure(figsize=(6, 4))
    plt.bar(['Income', 'Expense'], [income, expense], color=['#4CAF50', '#F44336'])
    plt.title('Income vs Expense')
    plt.ylabel('Amount')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    income_expense_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # --- Chart 2: Expense Breakdown (Pie Chart) ---
    expense_breakdown = user.transactions.filter(type='EXPENSE').values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    expense_labels = [item['category__name'] for item in expense_breakdown]
    expense_totals = [item['total'] for item in expense_breakdown]

    plt.figure(figsize=(6, 6))
    if expense_totals:
        plt.pie(expense_totals, labels=expense_labels, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Breakdown by Category')
    else:
        plt.text(0.5, 0.5, 'No expense data available', ha='center', va='center')
        plt.title('Expense Breakdown by Category')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    expense_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    context = {
        'income_expense_chart': income_expense_chart,
        'expense_chart': expense_chart,
    }
    
    return render(request, 'reports/reports.html', context)
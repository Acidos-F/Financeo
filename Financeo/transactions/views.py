from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from finance.models import Transaction, Account, Category
from .forms import TransactionForm, UpdateTransactionForm

@login_required
def transaction_list(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date', '-id')
    
    # Filter by type if provided
    transaction_type = request.GET.get('type', '')
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        transactions = transactions.filter(
            description__icontains=search_query
        ) | transactions.filter(
            category__name__icontains=search_query
        )
    
    context = {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'search_query': search_query,
        'show_transactions': True,
        'action': False,
        'is_delete': False,
    }
    return render(request, "transactions/transactions.html", context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions')
    else:
        transaction_type = request.GET.get('type', '')
        form = TransactionForm(user=request.user, transaction_type=transaction_type)
    
    context = {
        'form': form,
        'action': 'Create',
        'show_transactions': False,
        'is_delete': False,
    }
    return render(request, 'transactions/transactions.html', context)

@login_required
def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = UpdateTransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = UpdateTransactionForm(instance=transaction, user=request.user)
    
    context = {
        'form': form,
        'transaction': transaction,
        'action': 'Update',
        'show_transactions': False,
        'is_delete': False,
    }
    return render(request, 'transactions/transactions.html', context)

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions')
    context = {
        'transaction': transaction,
        'show_transactions': False,
        'action': False,
        'is_delete': True,
    }
    return render(request, 'transactions/transactions.html', context)

@login_required
def search_transactions_ajax(request):
    """AJAX endpoint for searching transactions"""
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date', '-id')
    
    # Filter by type if provided
    transaction_type = request.GET.get('type', '')
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        transactions = transactions.filter(
            description__icontains=search_query
        ) | transactions.filter(
            category__name__icontains=search_query
        )
    
    # Render the table rows as HTML
    html = ''
    if transactions.exists():
        for transaction in transactions:
            color_class = "text-green-500" if transaction.type == "INCOME" else "text-red-500"
            sign = '+' if transaction.type == 'INCOME' else '-'
            date_str = transaction.date.strftime('%b %d, %Y')
            description = transaction.description or '-'
            
            html += f'<tr class="border-b hover:bg-gray-50" data-type="{transaction.type}">\n'
            html += f'<td class="py-2 px-4 text-gray-600">{date_str}</td>\n'
            html += f'<td class="py-2 px-4 text-gray-600">{transaction.account.name}</td>\n'
            html += f'<td class="py-2 px-4 text-gray-600">{transaction.category.name}</td>\n'
            html += f'<td class="py-2 px-4 text-gray-600">{description}</td>\n'
            html += f'<td class="py-2 px-4 font-bold text-right {color_class}">{sign}${transaction.amount:.2f}</td>\n'
            html += f'<td class="py-2 px-4 text-center">\n'
            html += f'<div class="flex gap-3 justify-center items-center">\n'
            html += f'<a href="/transactions/{transaction.id}/update/" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all shadow-md hover:shadow-lg inline-block min-w-[90px] text-center border-2 border-blue-800">Edit</a>\n'
            html += f'<a href="/transactions/{transaction.id}/delete/" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all shadow-md hover:shadow-lg inline-block min-w-[90px] text-center border-2 border-red-800">Delete</a>\n'
            html += f'</div></td></tr>\n'
    else:
        html = '<tr><td colspan="6" class="text-center text-gray-500 py-8">No transactions found. <a href="/transactions/create/" class="text-blue-600 hover:underline">Create one</a></td></tr>'
    
    return JsonResponse({'html': html, 'count': transactions.count()})

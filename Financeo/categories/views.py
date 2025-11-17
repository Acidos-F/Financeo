from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from finance.models import Category, TransactionType
from .forms import CategoryForm

@login_required
def category_list(request):
    user = request.user
    categories = Category.objects.filter(user=user).order_by('type', 'name')
    
    context = {
        'categories': categories,
        'transaction_types': TransactionType.choices,
    }
    return render(request, "categories/categories.html", context)

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm(user=request.user)
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'categories/categories.html', context)

@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category, user=request.user)
    
    context = {
        'form': form,
        'category': category,
        'action': 'Update',
    }
    return render(request, 'categories/categories.html', context)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    context = {
        'category': category,
    }
    return render(request, 'categories/categories.html', context)

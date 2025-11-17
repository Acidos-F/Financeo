from django import forms
from finance.models import Transaction, Account, Category, TransactionType

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'date', 'type', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'description': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            if transaction_type:
                self.fields['category'].queryset = Category.objects.filter(user=user, type=transaction_type)
            else:
                self.fields['category'].queryset = Category.objects.filter(user=user)

class UpdateTransactionForm(TransactionForm):
    class Meta(TransactionForm.Meta):
        fields = ['account', 'category', 'amount', 'date', 'type', 'description']



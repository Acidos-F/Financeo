from django import forms
from finance.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Category name',
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data.get('name')
        type_val = self.cleaned_data.get('type')
        
        if not name or not type_val:
            return name
        
        # Check if category with same name and type exists for this user
        query = Category.objects.filter(user=self.user, name=name, type=type_val)
        
        # If updating, exclude the current instance
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise forms.ValidationError(
                f"You already have a {type_val} category named '{name}'."
            )
        
        return name

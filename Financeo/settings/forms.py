from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full max-w-sm bg-gray-200 border border-gray-300 rounded py-2 px-3 text-gray-700 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-gray-500'})
        }

class ProfilePictureUpdateForm(forms.Form):
    profile_picture = forms.ImageField()


class EmailUpdateForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full max-w-sm bg-gray-200 border border-gray-300 rounded py-2 px-3 text-gray-700 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-gray-500', 'placeholder': 'New E-Mail Address'})
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={'class': 'w-full bg-gray-200 border border-gray-300 rounded py-2 px-3 text-gray-700 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-gray-500', 'autocomplete': 'current-password', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'w-full bg-gray-200 border border-gray-300 rounded py-2 px-3 text-gray-700 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-gray-500', 'autocomplete': 'new-password', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'w-full bg-gray-200 border border-gray-300 rounded py-2 px-3 text-gray-700 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-gray-500', 'autocomplete': 'new-password', 'placeholder': 'Confirm New Password'})
    )

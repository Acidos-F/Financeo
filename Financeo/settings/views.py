from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import EmailUpdateForm, CustomPasswordChangeForm, UsernameUpdateForm, ProfilePictureUpdateForm

def settings_view(request):
    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UsernameUpdateForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Your username has been updated!')
                return redirect('settings')
        else:
            username_form = UsernameUpdateForm(instance=request.user)

        if 'update_profile_picture' in request.POST:
            profile_picture_form = ProfilePictureUpdateForm(request.POST, request.FILES)
            if profile_picture_form.is_valid():
                request.user.profile.profile_picture = profile_picture_form.cleaned_data['profile_picture']
                request.user.profile.save()
                messages.success(request, 'Your profile picture has been updated!')
                return redirect('settings')
        else:
            profile_picture_form = ProfilePictureUpdateForm()

        if 'update_email' in request.POST:
            email_form = EmailUpdateForm(request.POST)
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save()
                messages.success(request, 'Your email has been updated!')
                return redirect('settings')
        else:
            email_form = EmailUpdateForm()

        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            password_form = CustomPasswordChangeForm(request.user)

    else:
        username_form = UsernameUpdateForm(instance=request.user)
        profile_picture_form = ProfilePictureUpdateForm()
        email_form = EmailUpdateForm()
        password_form = CustomPasswordChangeForm(request.user)

    context = {
        'username_form': username_form,
        'profile_picture_form': profile_picture_form,
        'email_form': email_form,
        'password_form': password_form
    }
    return render(request, 'settings/settings.html', context)
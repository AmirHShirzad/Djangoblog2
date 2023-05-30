from django.shortcuts import render, redirect
from .forms import UsersRegisterForm, UsersUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UsersRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # convert the information that users entered in to suitable format with cleaned_data
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Thanks {username} for signing up :) please logged in to your account')
            return redirect('login')
    else:
        form = UsersRegisterForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


# this decorator add functionality that user must be logged in to see themselves.
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UsersUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your profile has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UsersUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form, 'title': 'Profile'}

    return render(request, 'users/profile.html', context)

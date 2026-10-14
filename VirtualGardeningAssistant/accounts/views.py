from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def accounts_home(request):
    return render(request, 'accounts/register.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully.')
        return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('home')

    return redirect('home')

@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('my_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/my_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'edit_mode': request.GET.get('edit') == 'true',
    })

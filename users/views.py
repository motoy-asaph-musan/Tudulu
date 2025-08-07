from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm

class LogoutGetAllowedView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('users:login')  # Make sure 'users:login' exists in your URLs

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'equipment/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Log the user in immediately
#             return redirect('home')  # Redirect to home page
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('users:login')

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# @login_required
def home(request):
    return render(request, 'equipment/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views import View
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .forms import ProfileForm
from .models import UserProfile
import stripe

User = get_user_model()

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')  # Changed from 'users:login'

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')  # Or your preferred redirect 


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
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    class LogoutView(View): 
        def get(self, request):
            logout(request)
            messages.success(request, "You have been logged out successfully.")
            return redirect('login') 

    class LogoutGetAllowedView(View):  
        def get(self, request):
            logout(request)
            messages.success(request, "Logged out successfully")
            return redirect('login')


def create_checkout_session(request):
    # Your checkout logic here
    pass

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def edit_profile(request):
    # Ensure user has a profile (fixes 'CustomUser has no userprofile')
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to a page that exists, e.g., profile_view or home
            return redirect('home')  # Change 'home' to your profile page URL name if you have one
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

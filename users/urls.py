from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import LogoutView, user_login, register

app_name = 'users'

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/logout/', LogoutView.as_view(), name='LogoutView'),
    path('accounts/login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # path('register/', register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

    # Password Reset URLs
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt'
        ), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), 
        name='password_reset_complete'),

    # Other URLs
    path('home/', views.home, name='home'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),

    #Profile
    path('profile/', views.profile_view, name='profile'),
    path('checkout-session/', views.create_checkout_session, name='checkout_session'),
]

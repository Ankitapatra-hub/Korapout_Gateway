from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),  # if you have one

    # Forgot Password flow
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='useraccount/password_reset.html',
            form_class=CustomPasswordResetForm,
            email_template_name='useraccount/password_reset_email.html',
            subject_template_name='useraccount/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='useraccount/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='useraccount/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='useraccount/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

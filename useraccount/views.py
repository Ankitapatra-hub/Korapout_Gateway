from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.forms import PasswordResetForm


# Store OTPs temporarily (better: use a model or cache)
otp_storage = {}


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = str(random.randint(100000, 999999))
            otp_storage[user.email] = otp

            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'useraccount/register.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if otp_storage.get(email) == otp:
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            del otp_storage[email]
            return redirect('login')
    return render(request, 'useraccount/verify_otp.html')


def login_view(request):
    # Get "next" parameter from URL (if user was redirected here)
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect(next_url)  # Redirect back to where they came from
    else:
        form = LoginForm()

    return render(request, 'useraccount/login.html', {'form': form, 'next': next_url})


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Implement reset logic here
    else:
        form = PasswordResetForm()
    return render(request, 'useraccount/password_reset.html', {'form': form})

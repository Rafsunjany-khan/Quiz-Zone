from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignupForm, UserLoginForm, OTPForm
from .models import User


# ------------------------
# Signup View
# ------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # Create inactive user
            user = User.objects.create_user(
                email=cleaned_data['email'],
                full_name=cleaned_data['full_name'],
                phone=cleaned_data['phone'],
                password=cleaned_data['password']
            )
            user.is_active = False
            user.save()

            # Generate activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate', args=[uid, token])
            )

            # Send email
            send_mail(
                subject='Activate your account',
                message=f'Hi {user.full_name},\nClick the link to activate your account:\n{activation_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

            messages.success(request, "Account created! Please check your email to verify.")
            return render(request, 'email_verification.html', {'user': user})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def email_verification(request):
    return render(request, "email_verification.html")

# ------------------------
# Email Activation View
# ------------------------
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified! You can now login.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link!")
        return redirect('signup')


# ------------------------
# Login View
# ------------------------
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Welcome, {user.full_name}!")
            return redirect('quiz:home')
        else:
            messages.error(request, "Invalid credentials or account not verified.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# ------------------------
# Logout View
# ------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('quiz:index')

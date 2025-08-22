from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from .forms import UserRegisterForm, UserLoginForm
from .models import *

def index(request):
    return  render(request, 'index.html')

def home(request):
    quizzes = Quiz.objects.all()[:5]   # latest 5 quizzes
    categories = Category.objects.all()
    user_attempts = None

    user_id = request.session.get("user_id")
    if user_id:
        user_attempts = QuizAttempt.objects.filter(user_id=user_id).order_by('-started_at')[:5]

    context = {
        "quizzes": quizzes,
        "categories": categories,
        "user_attempts": user_attempts,
    }
    return render(request, 'home.html', context)

# ------------------------
# Signup
# ------------------------
def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

# ------------------------
# Login
# ------------------------
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.is_active and check_password(password, user.password):
                    # store user ID in session
                    request.session['user_id'] = user.id
                    messages.success(request, "Logged in successfully!")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid credentials or inactive account!")
            except User.DoesNotExist:
                messages.error(request, "User not found!")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# ------------------------
# Logout
# ------------------------
def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    messages.success(request, "Logged out successfully!")
    return redirect('login')

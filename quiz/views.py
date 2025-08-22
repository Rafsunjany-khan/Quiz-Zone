from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .forms import UserRegisterForm, UserLoginForm
from .models import *


def index(request):
    return render(request, 'index.html', {'logged_in': 'user_id' in request.session})

def home(request):
    categories = Category.objects.prefetch_related("quiz_set__questions__options").all()
    logged_in = 'user_id' in request.session
    return render(request, "home.html", {"categories": categories, "logged_in": logged_in})

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.is_active and check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials or inactive account!")
        except User.DoesNotExist:
            messages.error(request, "User not found!")
    return render(request, 'login.html', {'logged_in': 'user_id' in request.session})

# ------------------------
# Logout
# ------------------------
def logout_view(request):
    request.session.flush()  # clears all session data
    messages.success(request, "Logged out successfully!")
    return redirect('login')




# ------------------------
# Step 1: List categories
# ------------------------
def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


# ------------------------
# Step 2: Show quizzes under a category
# ------------------------
def quiz_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category)
    return render(request, "quiz_list.html", {"category": category, "quizzes": quizzes})


# ------------------------
# Step 3: Attempt quiz
# ------------------------
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("options")

    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "You must be logged in to attempt a quiz.")
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                if option.is_correct:
                    score += question.points

        # save attempt
        QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            completed_at=timezone.now()
        )
        messages.success(request, f"You scored {score} points in {quiz.title}!")
        return redirect("category_list")

    return render(request, "start_quiz.html", {"quiz": quiz, "questions": questions})
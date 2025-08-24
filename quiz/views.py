from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Category, Quiz, Option, QuizAttempt


def index(request):
    return render(request, 'index.html', {'logged_in': 'user_id' in request.session})


@login_required
def home(request):
    user = request.user
    categories = Category.objects.prefetch_related("quiz_set__questions").all()

    for category in categories:
        quizzes_with_score = []
        for quiz in category.quiz_set.all():
            # Get latest attempt for this user
            attempt = QuizAttempt.objects.filter(user=user, quiz=quiz).order_by('-completed_at').first()
            quiz.user_score = attempt.score if attempt else None
            quizzes_with_score.append(quiz)
        category.quizzes = quizzes_with_score  # attach quizzes with score

    return render(request, "home.html", {
        "categories": categories,
        "logged_in": True
    })

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})

@login_required
def quiz_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category)
    return render(request, "quiz_list.html", {
        "category": category,
        "quizzes": quizzes,
        "logged_in": request.user.is_authenticated
    })

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("options")

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to attempt a quiz.")
        return redirect("auth:login")

    user = request.user

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                if option.is_correct:
                    score += question.points

        # create or update attempt
        QuizAttempt.objects.update_or_create(
            user=user,
            quiz=quiz,
            defaults={'score': score, 'completed_at': timezone.now()}
        )

        messages.success(request, f"You scored {score} points in {quiz.title}!")
        return redirect("quiz:category_list")  # use namespace

    return render(request, "start_quiz.html", {"quiz": quiz, "questions": questions})

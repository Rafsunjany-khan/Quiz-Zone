from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Category, Quiz, Option, QuizAttempt, Rating
from .forms import RatingForm

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
            quiz.user_score = attempt.score if attempt else 0  # set 0 if no score
            quiz.attempted = attempt is not None                # True if attempted, False if not
            quizzes_with_score.append(quiz)
        category.quizzes = quizzes_with_score  # attach quizzes with score

    return render(request, "home.html", {
        "categories": categories,
        "logged_in": True
    })

# def home(request):
#     user = request.user
#     categories = Category.objects.prefetch_related("quiz_set__questions").all()
#
#     for category in categories:
#         quizzes_with_score = []
#         for quiz in category.quiz_set.all():
#             # Get latest attempt for this user
#             attempt = QuizAttempt.objects.filter(user=user, quiz=quiz).order_by('-completed_at').first()
#             quiz.user_score = attempt.score if attempt else None
#             quizzes_with_score.append(quiz)
#         category.quizzes = quizzes_with_score  # attach quizzes with score
#
#     return render(request, "home.html", {
#         "categories": categories,
#         "logged_in": True
#     })
# in views.py
def about_view(request):
    return render(request, "about.html", {"logged_in": request.user.is_authenticated})
def guideline_view(request):
    return render(request, "guideline.html", {"logged_in": request.user.is_authenticated})

@login_required
def notification_view(request):
    return render(request, 'notification.html', {'user': request.user})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})

from django.db.models import Avg

@login_required
def quiz_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    quizzes = Quiz.objects.filter(category=category)

    for quiz in quizzes:
        avg_rating = Rating.objects.filter(quiz=quiz).aggregate(Avg('score'))['score__avg']
        quiz.avg_rating = round(avg_rating) if avg_rating else 0

    return render(request, "quiz_list.html", {
        "category": category,
        "quizzes": quizzes,
        "logged_in": request.user.is_authenticated
    })

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("options")
    user = request.user

    if request.method == "POST":
        score = 0
        unanswered = []  # track unanswered questions

        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if not selected_option_id:
                unanswered.append(question)
                continue
            option = Option.objects.get(id=selected_option_id)
            if option.is_correct:
                score += question.points

        if unanswered:
            messages.error(request, "Please answer all questions before submitting!")
            return render(request, "start_quiz.html", {"quiz": quiz, "questions": questions})

        # Save or update attempt
        attempt, created = QuizAttempt.objects.update_or_create(
            user=user,
            quiz=quiz,
            defaults={'score': score, 'completed_at': timezone.now()}
        )

        return redirect("quiz:quiz_result", quiz_id=quiz.id)

    return render(request, "start_quiz.html", {"quiz": quiz, "questions": questions})
    # def start_quiz(request, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     questions = quiz.questions.prefetch_related("options")
#
#     if not request.user.is_authenticated:
#         messages.error(request, "You must be logged in to attempt a quiz.")
#         return redirect("auth:login")
#
#     user = request.user
#
#     if request.method == "POST":
#         score = 0
#         for question in questions:
#             selected_option_id = request.POST.get(str(question.id))
#             if selected_option_id:
#                 option = Option.objects.get(id=selected_option_id)
#                 if option.is_correct:
#                     score += question.points
#
#         # create or update attempt
#         QuizAttempt.objects.update_or_create(
#             user=user,
#             quiz=quiz,
#             defaults={'score': score, 'completed_at': timezone.now()}
#         )
#
#         messages.success(request, f"You scored {score} points in {quiz.title}!")
#         return redirect("quiz:category_list")  # use namespace
#
#     return render(request, "start_quiz.html", {"quiz": quiz, "questions": questions})



@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user

    # Only allow results if quiz has questions
    if quiz.questions.count() == 0:
        messages.warning(request, "This quiz has no questions yet, rating not allowed.")
        return redirect('quiz:category_list')

    attempt = QuizAttempt.objects.filter(user=user, quiz=quiz).order_by('-completed_at').first()
    if not attempt:
        messages.info(request, "You need to attempt the quiz first before rating.")
        return redirect('quiz:start_quiz', quiz_id=quiz.id)

    # Check if user already rated
    try:
        user_rating = Rating.objects.get(user=user, quiz=quiz)
    except Rating.DoesNotExist:
        user_rating = None

    if request.method == "POST" and not user_rating:
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.quiz = quiz
            rating.save()
            messages.success(request, f"Thank you for rating {quiz.title}!")
            return redirect('quiz:home')
    else:
        form = RatingForm()

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'attempt': attempt,
        'form': form,
        'user_rating': user_rating
    })

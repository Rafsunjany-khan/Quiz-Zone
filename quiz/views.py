from django.shortcuts import render
from .models import Quiz


def home(request):
    # Get the first quiz for testing
    quiz = Quiz.objects.first()

    if not quiz:
        return render(request, 'index.html', {'quiz': None, 'questions': []})

    questions = quiz.questions.all()
    return render(request, 'index.html', {'quiz': quiz, 'questions': questions})


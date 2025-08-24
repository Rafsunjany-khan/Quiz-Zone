from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    # Landing / Home
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),

    # Categories & Quizzes
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
]

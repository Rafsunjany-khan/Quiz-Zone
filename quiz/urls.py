from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    # Landing / Home
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("about/", views.about_view, name="about"),
    path("guideline/", views.guideline_view, name="guideline"),
    path("notification/", views.notification_view, name="notification"),

    # Categories & Quizzes
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_results, name="quiz_result"),

]

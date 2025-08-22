from django.urls import path
from . import views

urlpatterns = [
    # Landing / Home
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),

    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Categories & Quizzes
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
]

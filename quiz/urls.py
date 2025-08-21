from django.urls import path
from . import views

app_name = "quiz"  # namespace for this app

urlpatterns = [
    path('', views.home, name='home'),
    #path('quiz/<int:quiz_id>/', views.home, name='home'),
]

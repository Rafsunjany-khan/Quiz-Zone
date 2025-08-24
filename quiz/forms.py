from django import forms
from .models import Quiz, Question, Option, Rating
from django.contrib.auth import get_user_model
User = get_user_model()

# ------------------------
# Quiz Form (Admin)
# ------------------------
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'category', 'has_time_limit', 'time_limit']

# ------------------------
# Question Form (Admin)
# ------------------------
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'points']

# ------------------------
# Option Form (Admin)
# ------------------------
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['label', 'text', 'is_correct']

# ------------------------
# Quiz Rating Form (Student)
# ------------------------
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Quiz, Question, Option, Rating


# ------------------------
# User Signup & Login
# ------------------------
class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# ------------------------
# Quiz & Question Creation (Admin)
# ------------------------
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category', 'has_time_limit', 'time_limit']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'points']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['label', 'text', 'is_correct']


# ------------------------
# Quiz Rating (Student)
# ------------------------
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

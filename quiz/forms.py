from django import forms
from .models import *

# ------------------------
# User Signup
# ------------------------
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Store password as plain text or hashed using make_password
        from django.contrib.auth.hashers import make_password
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ------------------------
# User Login
# ------------------------
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



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

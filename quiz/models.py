from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# -------------------------
# Custom User Manager
# -------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, first_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # superuser active by default
        return self.create_user(email, password, first_name, **extra_fields)

# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)  # <-- full name
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # related_name fix for permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # <-- required

    def __str__(self):
        return self.email

# -------------------------
# User Profile
# -------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.email

# -------------------------
# Category Table
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# -------------------------
# Quiz Table
# -------------------------
class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    has_time_limit = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category.name} | {self.title} | {self.created_at.strftime('%Y-%m-%d')}"

# -------------------------
# Question Table
# -------------------------
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text[:50]

# -------------------------
# Option Table
# -------------------------
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]

# -------------------------
# User Quiz Attempt
# -------------------------
class UserQuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score}/{self.total}"

# -------------------------
# User Answer
# -------------------------
class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.user.email} - {self.question.text[:30]}"

# -------------------------
# Quiz Rating
# -------------------------
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(default=1)  # 1 to 7

    class Meta:
        unique_together = ('user', 'quiz')  # one rating per user per quiz

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.rating}"

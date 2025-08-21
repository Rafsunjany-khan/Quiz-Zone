from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

# ------------------------
# Custom User Manager
# ------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None):
        if not email:
            raise ValueError("Email is required")
        if not full_name:
            raise ValueError("Full name is required")
        if not phone:
            raise ValueError("Phone is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password=None):
        user = self.create_user(email, full_name, phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ------------------------
# Custom User
# ------------------------
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email


# ------------------------
# Quiz Category
# ------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ------------------------
# Quiz
# ------------------------
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    has_time_limit = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Time limit in minutes")

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings)/ratings.count(), 2)
        return 0

    def __str__(self):
        return self.title


# ------------------------
# Question & Option
# ------------------------
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"


class Option(models.Model):
    LABEL_CHOICES = (('A','Option A'),('B','Option B'),('C','Option C'),('D','Option D'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=1, choices=LABEL_CHOICES)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'label')

    def save(self, *args, **kwargs):
        # Ensure only one correct answer per question
        if self.is_correct:
            Option.objects.filter(question=self.question, is_correct=True).update(is_correct=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label}) {self.text}"


# ------------------------
# Quiz Attempt
# ------------------------
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} ({self.score})"


# ------------------------
# Quiz Rating
# ------------------------
class Rating(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i,str(i)) for i in range(1,8)])  # 1–7 rating

    class Meta:
        unique_together = ('quiz','user')

    def __str__(self):
        return f"{self.quiz.title} rated {self.score} by {self.user.email}"

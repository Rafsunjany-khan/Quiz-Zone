from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    has_time_limit = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField(blank=True, null=True)  # minutes

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"


class Option(models.Model):
    LABEL_CHOICES = (('A','Option A'),('B','Option B'),('C','Option C'),('D','Option D'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=1, choices=LABEL_CHOICES, editable=False)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'label')

    def save(self, *args, **kwargs):
        # Auto-assign label if not set
        if not self.label:
            used_labels = self.question.options.values_list('label', flat=True)
            for choice, _ in self.LABEL_CHOICES:
                if choice not in used_labels:
                    self.label = choice
                    break
        # Only one correct option per question
        if self.is_correct:
            Option.objects.filter(question=self.question, is_correct=True).update(is_correct=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label}) {self.text}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} ({self.score})"


class Rating(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 8)])  # 1–7 rating

    class Meta:
        unique_together = ('quiz','user')

    def __str__(self):
        return f"{self.quiz.title} rated {self.score} by {self.user.email}"

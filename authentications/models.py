from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# ------------------------
# Custom User Manager
# ------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password):
        user = self.create_user(email, full_name, phone, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True  # required for admin
        user.is_active = True
        user.save(using=self._db)
        return user


# ------------------------
# Custom User Model
# ------------------------
class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email

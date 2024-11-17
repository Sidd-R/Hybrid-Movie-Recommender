from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super(CustomUserManager, self).create_superuser( email, password, **extra_fields)

    def _create_user(self,email, password, *args, **extra_fields):
        email = self.normalize_email(email)
        # GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        # email = email
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

class UserProfile(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = None
    prefrences = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
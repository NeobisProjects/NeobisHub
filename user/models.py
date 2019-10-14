from django.contrib.auth.models import AbstractUser

from project.models import *
from user.managers import UserModelManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserModelManager()

    def __str__(self):
        return self.email


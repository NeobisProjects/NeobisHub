from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Department(models.Model):
    head = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    slack = models.URLField()
    telegram = models.URLField()
    mentor_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

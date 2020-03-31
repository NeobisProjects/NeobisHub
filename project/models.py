from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from user.models import CustomUser
from user_profile.models import UserProfile

PROJECT_STATUS = {
    ('a', 'Активный'),
    ('f', 'Заморожен'),
    ('c', 'Завершенный')
}


class Project(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(null=True, )
    date_of_start = models.DateField(default=datetime.now)
    date_of_finish = models.DateField(default=datetime.now)
    product_owner = models.CharField(max_length=60)
    pm = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='pm')
    status = models.CharField(max_length=5, choices=PROJECT_STATUS)
    description = models.TextField()

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Screenshot(models.Model):
    image = models.ImageField()
    project = models.ForeignKey(Project, related_name='screenshots', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class UserProject(models.Model):
    user = models.ForeignKey(UserProfile, related_name='project', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='team', on_delete=models.PROTECT)
    percentage = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    user_role = models.CharField(max_length=50)

    class Meta:
        unique_together = ['user', 'project']

from django.db import models

from user.models import CustomUser

PROJECT_STATUS = {
    ('a', 'Активный'),
    ('f', 'Заморожен'),
    ('c', 'Завершенный')
}


class Project(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField()
    date_of_start = models.DateField()
    date_of_finish = models.DateField()
    product_owner = models.CharField(max_length=60)
    team = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='team')
    status = models.CharField(max_length=5, choices=PROJECT_STATUS)


class Document(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)


class Screenshot(models.Model):
    image = models.ImageField()
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)

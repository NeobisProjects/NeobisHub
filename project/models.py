from datetime import datetime

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
    date_of_start = models.DateField(default=datetime.now)
    date_of_finish = models.DateField(default=datetime.now)
    product_owner = models.CharField(max_length=60)
    # team = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='team')
    status = models.CharField(max_length=5, choices=PROJECT_STATUS)

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

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.core.validators import MaxValueValidator

from department.models import Department
from project.models import *
from user_profile.validators import validate_number

User = get_user_model()


USER_STATUS = {
    ('h', "HQ"),
    ('p', "PM"),
    ('t', "Тимлид"),
    ('m', "Ментор"),
    ('n', "Новичок")
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='users', on_delete=models.PROTECT)
    phone = models.CharField(max_length=13, validators=[validate_number])
    telegram = models.URLField()
    status = models.CharField(max_length=5, choices=USER_STATUS)
    congestion = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    validation_code = models.CharField(max_length=6, null=True, blank=True)
    # TODO: хз какой тип , спросить у Сережи что это вообще
    resume = models.FileField(null=True)

    @classmethod
    def create(cls, user, name, department, phone, telegram, status, congestion, validation_code, resume):
        with transaction.atomic():
            try:
                assert user is not None or user != ''
            except AssertionError as e:
                raise e
        user_profile = cls.objects.create(
            user=user, name=name, department=department, phone=phone, telegram=telegram, status=status,
            congestion=congestion, validation_code=validation_code, resume=resume
        )
        return user_profile


class Progress(models.Model):
    user = models.OneToOneField(User, related_name='progress', on_delete=models.CASCADE)
    study_plan = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    test = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])


class UserProject(models.Model):
    user = models.OneToOneField(User, related_name='project', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='user_projects', on_delete=models.PROTECT)
    percent_of_project = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    percent_of_user = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    user_role = models.CharField(max_length=50)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.core.validators import MaxValueValidator

from department.models import Department
from user_profile.validators import validate_number

User = get_user_model()

USER_STATUS = {
    ('h', "HQ"),
    ('m', "Ментор/Новичок")
}
CONGESTION = {
    (0, 'Свободен'),
    (25, 'Немного занят'),
    (50, 'Частично занят'),
    (75, 'Загружен'),
    (100, 'Очень загружен')
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='users', on_delete=models.PROTECT, null=True)
    phone = models.CharField(max_length=13, validators=validate_number(), null=True)
    telegram = models.URLField(null=True)
    status = models.CharField(max_length=5, choices=USER_STATUS)
    congestion = models.PositiveSmallIntegerField(null=True, blank=True, choices=CONGESTION)
    validation_code = models.CharField(max_length=4, null=True, blank=True)
    summary = models.FileField(upload_to='', default="", null=True, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @classmethod
    def create(cls, user, name, department, phone, telegram, status,
               congestion, validation_code, summary, progress, project):
        with transaction.atomic():
            try:
                assert user is not None or user != ''
            except AssertionError as e:
                raise e
        user_profile = cls.objects.create(
            user=user, name=name, department=department, phone=phone, telegram=telegram, status=status,
            congestion=congestion, validation_code=validation_code, summary=summary, progress=progress, project=project
        )
        return user_profile


class Progress(models.Model):
    user = models.OneToOneField(UserProfile, related_name='progress', on_delete=models.CASCADE)
    study_plan = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    points = models.PositiveSmallIntegerField(default=0)
    out_of = models.PositiveSmallIntegerField(default=100)



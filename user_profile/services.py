from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from rest_framework.authtoken.models import Token

from department.models import Department
from user_profile.errors import DuplicateUserError
from user_profile.models import UserProfile
from user_profile.utils import Validate

User = get_user_model()


class UserService:
    @classmethod
    @transaction.atomic
    def create_user_with_profile(cls, data: dict, user: User) -> User:
        try:
            user = User.objects.create_user(email=data['email'],
                                            password=data['password'], )
        except User.DoesNotExist:
            raise ObjectDoesNotExist('user does not exist')
        except IntegrityError:
            raise DuplicateUserError()
        code = Validate.create_validation_code()
        UserProfile.objects.create(user=user, name=data['name'], phone=data['phone'],
                                   department=Department.objects.get(id=data['department']),
                                   telegram=data['telegram'], status=data['status'], congestion=data['congestion'],
                                   # resume=data['resume'], validation_code=code)
                                   validation_code=code, )

        return user


class ValidateUserService:

    @staticmethod
    def get_user_profile(user_id):
        user_profile = UserProfile.objects.get(user_id=user_id)
        return user_profile

    @staticmethod
    def change_user_status(user_id):
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def get_user_token(user):
        token = Token.objects.get_or_create(user=user)
        return token

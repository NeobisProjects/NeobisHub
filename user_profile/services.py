from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from rest_framework.authtoken.models import Token

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
        Validate.send_email_with_code(user, code)
        if data['status'] == 'h':
            Validate.send_email_to_admin(user, data['surname'], data['name'])
        UserProfile.objects.create(user=user, name=data['name'], surname=data['surname'], patronymic=data['patronymic'],
                                   status=data['status'], validation_code=code)

        return user


class ValidateUserService:

    @staticmethod
    def get_user_profile_by_id(user_id):
        user_profile = UserProfile.objects.get(user_id=user_id)
        return user_profile

    @staticmethod
    def change_user_status(user_id):
        user = User.objects.get(id=user_id)
        user.is_active = True
        profile = UserProfile.objects.get(user_id=user.id)
        # if profile.status is 'h':
        #     user.is_staff = True
        user.save()
        return user

    @staticmethod
    def get_user_token(user):
        token = Token.objects.get_or_create(user=user)
        return token
